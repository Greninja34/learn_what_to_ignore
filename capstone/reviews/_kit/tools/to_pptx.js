// Editable PowerPoint export: opens the rendered Marp deck in headless Chrome, reads every
// slide's boxes, text, tables and images with their exact positions, and rebuilds them as
// native PowerPoint objects (text boxes, shapes, tables, pictures) with pptxgenjs.
//
// Run from deck/ (build.sh does this):
//   node tools/to_pptx.js out/deck_bare.html out/gantt_bare.html out/notes.txt out/deck.pptx
// Needs the research2 env (pptxgenjs + Marp's puppeteer-core on NODE_PATH) and Google Chrome.
const fs = require('fs');
const path = require('path');
const puppeteer = require('puppeteer-core');
const PptxGenJS = require('pptxgenjs');

const [deckHtml, ganttHtml, notesFile, outFile] = process.argv.slice(2);
const PX = 96;                       // CSS px per inch; the slide is 1280 x 720 px = 13.333" x 7.5"
const SCALE = 2;                     // screenshot resolution for pictures and sketches
const CHROME = process.env.CHROME || '/usr/bin/google-chrome';

// ---------------------------------------------------------------- in-page extraction
// Runs inside Chrome for one <section>; returns a flat, paint-ordered list of items.
function extractSection(slideIndex) {
  const svg = document.querySelectorAll('body > svg[data-marpit-svg]')[slideIndex];
  const sec = svg.querySelector('section:not([data-marpit-advanced-background="background"]):not([data-marpit-advanced-background="pseudo"])');
  const bgSec = svg.querySelector('section[data-marpit-advanced-background="background"]');
  const bgImage = bgSec ? bgSec.innerHTML.match(/url\(["']?([^"')]+)/) : null;
  const origin = sec.getBoundingClientRect();
  const items = [];
  const INLINE = new Set(['inline', 'inline-block', 'inline-flex', 'inline-grid', 'contents']);
  const rgba = (c) => {
    const m = c && c.match(/rgba?\(([^)]+)\)/);
    if (!m) return null;
    const [r, g, b, a = 1] = m[1].split(/[ ,/]+/).filter(Boolean).map(Number);
    if (a === 0) return null;
    return { hex: [r, g, b].map((v) => Math.round(v).toString(16).padStart(2, '0')).join('').toUpperCase(), a };
  };
  const box = (r) => ({ x: r.left - origin.left, y: r.top - origin.top, w: r.width, h: r.height });
  const visible = (el, cs) => cs.display !== 'none' && cs.visibility !== 'hidden' && parseFloat(cs.opacity) > 0;
  const isInline = (el) => INLINE.has(getComputedStyle(el).display);
  const hasText = (el) => el.textContent.replace(/\s+/g, '').length > 0;
  // a "text block": block-level element with text whose element children are all inline
  const isTextBlock = (el) => {
    if (!hasText(el) || isInline(el)) return false;
    if (['TABLE', 'UL', 'OL'].includes(el.tagName)) return false;
    return [...el.children].every((c) => isInline(c) || !hasText(c));
  };

  function shapeOf(el, cs, r) {
    const fill = rgba(cs.backgroundColor);
    const sides = ['Top', 'Right', 'Bottom', 'Left'].map((s) => ({
      s, w: parseFloat(cs[`border${s}Width`]) || 0, c: rgba(cs[`border${s}Color`]), st: cs[`border${s}Style`],
    })).filter((b) => b.w > 0 && b.c && b.st !== 'none');
    if (!fill && !sides.length) return;
    const rad = Math.min(parseFloat(cs.borderTopLeftRadius) || 0, r.width / 2, r.height / 2);
    const uniform = sides.length === 4 && sides.every((b) => b.w === sides[0].w && b.c.hex === sides[0].c.hex);
    items.push({
      kind: 'shape', ...box(r), radius: rad, ellipse: rad >= Math.min(r.width, r.height) / 2 - 0.5 && Math.abs(r.width - r.height) < 2,
      fill, line: uniform ? { ...sides[0].c, w: sides[0].w, dash: sides[0].st } : null,
    });
    if (!uniform) for (const b of sides) {           // one-sided borders become thin bars
      const t = b.w;
      const rr = { Top: [r.left, r.top, r.width, t], Bottom: [r.left, r.bottom - t, r.width, t],
                   Left: [r.left, r.top, t, r.height], Right: [r.right - t, r.top, t, r.height] }[b.s];
      items.push({ kind: 'shape', x: rr[0] - origin.left, y: rr[1] - origin.top, w: rr[2], h: rr[3], radius: 0, fill: b.c, line: null });
    }
  }

  function pseudo(el, r, which) {                      // absolutely positioned ::before / ::after bars and dots
    const ps = getComputedStyle(el, which);
    if (!ps || ps.content === 'none' || ps.display === 'none' || ps.position !== 'absolute') return;
    const fill = rgba(ps.backgroundColor);
    if (!fill) return;
    const L = parseFloat(ps.left), T = parseFloat(ps.top), R = parseFloat(ps.right);
    const W = ps.width !== 'auto' ? parseFloat(ps.width) : r.width - L - (R || 0);
    const H = parseFloat(ps.height);
    if (!(W > 0 && H > 0)) return;
    const rad = Math.min(parseFloat(ps.borderTopLeftRadius) || 0, W / 2, H / 2);
    items.push({ kind: 'shape', x: r.left - origin.left + L, y: r.top - origin.top + T, w: W, h: H, radius: rad,
                 ellipse: rad >= Math.min(W, H) / 2 - 0.5, fill, line: null });
  }

  // runs of styled text inside an inline subtree
  function runs(el) {
    const out = [];
    const walk = (node, link) => {
      if (node.nodeType === 3) {
        const cs = getComputedStyle(node.parentElement);
        let t = node.textContent.replace(/\s+/g, ' ');
        if (!t) return;
        if (cs.textTransform === 'uppercase') t = t.toUpperCase();
        const c = rgba(cs.color) || { hex: '000000', a: 1 };
        const fam = cs.fontFamily.split(',')[0].replace(/["']/g, '').trim();
        const wt = parseInt(cs.fontWeight);
        out.push({ text: t, font: fam, weight: wt, size: parseFloat(cs.fontSize),
                   bold: wt >= 700, italic: cs.fontStyle === 'italic', color: c.hex,
                   spacing: parseFloat(cs.letterSpacing) || 0, sub: node.parentElement.closest('sub') !== null, link });
      } else if (node.nodeType === 1) {
        if (node.tagName === 'BR') { out.push({ br: true }); return; }
        const cs = getComputedStyle(node);
        if (!visible(node, cs)) return;
        const a = node.tagName === 'A' ? node.href : link;
        node.childNodes.forEach((n) => walk(n, a));
      }
    };
    el.childNodes.forEach((n) => walk(n, el.closest('a') ? el.closest('a').href : null));
    // trim the ends and around line breaks
    for (let i = 0; i < out.length; i++) {
      if (out[i].br) continue;
      if (i === 0 || out[i - 1].br) out[i].text = out[i].text.replace(/^ /, '');
      if (i === out.length - 1 || out[i + 1].br) out[i].text = out[i].text.replace(/ $/, '');
    }
    return out.filter((x) => x.br || x.text);
  }

  function textItem(el, cs, r, extra = {}) {
    const pl = parseFloat(cs.paddingLeft) + parseFloat(cs.borderLeftWidth), pr = parseFloat(cs.paddingRight) + parseFloat(cs.borderRightWidth);
    const pt = parseFloat(cs.paddingTop) + parseFloat(cs.borderTopWidth), pb = parseFloat(cs.paddingBottom) + parseFloat(cs.borderBottomWidth);
    const fs = parseFloat(cs.fontSize);
    const lh = cs.lineHeight === 'normal' ? fs * 1.2 : parseFloat(cs.lineHeight);
    // single line in the browser? then PowerPoint must not wrap it either
    const range = document.createRange(); range.selectNodeContents(el);
    const tops = [];
    for (const q of [...range.getClientRects()].sort((a, b) => a.top - b.top))
      if (q.height > 0 && !tops.some((t) => Math.abs(t - q.top) < lh * 0.6)) tops.push(q.top);
    const lines = tops.length;
    let align = cs.textAlign; if (align === 'start') align = 'left'; if (align === 'end') align = 'right';
    if (align === 'justify') align = 'left';
    // flex containers centring their text
    let valign = 'top';
    if (cs.display.includes('flex')) {
      const col = cs.flexDirection.startsWith('column');
      const main = cs.justifyContent, cross = cs.alignItems;
      if ((col ? main : cross) === 'center') valign = 'middle';
      if ((col ? cross : main) === 'center') align = 'center';
    }
    items.push({ kind: 'text', x: r.left - origin.left + pl, y: r.top - origin.top + pt, w: r.width - pl - pr, h: r.height - pt - pb,
                 runs: runs(el), align, lineHeight: lh / fs, fontSize: fs, singleLine: lines <= 1, valign, ...extra });
  }

  function listItem(el, cs, r) {
    const paras = [...el.children].filter((li) => li.tagName === 'LI').map((li) => {
      const lcs = getComputedStyle(li);
      return { runs: runs(li), after: parseFloat(lcs.marginBottom) || 0 };
    });
    const pl = parseFloat(cs.paddingLeft);
    const fs = parseFloat(cs.fontSize);
    const lh = cs.lineHeight === 'normal' ? fs * 1.2 : parseFloat(cs.lineHeight);
    items.push({ kind: 'list', x: r.left - origin.left, y: r.top - origin.top, w: r.width, h: r.height, indent: pl,
                 numbered: el.tagName === 'OL', paras, lineHeight: lh / fs, fontSize: fs, markerColor: (rgba(cs.color) || {}).hex });
  }

  function tableItem(el, r) {
    const rows = [...el.querySelectorAll('tr')].map((tr) => ({
      h: tr.getBoundingClientRect().height,
      cells: [...tr.children].map((td) => {
        const cs = getComputedStyle(td);
        return { runs: runs(td), fill: rgba(cs.backgroundColor), border: rgba(cs.borderTopColor), bw: parseFloat(cs.borderTopWidth) || 1,
                 pad: [cs.paddingTop, cs.paddingRight, cs.paddingBottom, cs.paddingLeft].map(parseFloat),
                 valign: cs.verticalAlign === 'middle' ? 'middle' : 'top', fontSize: parseFloat(cs.fontSize), lineHeight: (cs.lineHeight === 'normal' ? 1.2 : parseFloat(cs.lineHeight) / parseFloat(cs.fontSize)) };
      }),
    }));
    const colW = [...el.querySelector('tr').children].map((c) => c.getBoundingClientRect().width);
    items.push({ kind: 'table', ...box(r), rows, colW });
  }

  let imgId = 0;
  function visit(el) {
    const cs = getComputedStyle(el);
    if (!visible(el, cs)) return;
    const r = el.getBoundingClientRect();
    if (r.width < 0.5 || r.height < 0.5) { if (cs.display !== 'contents') return; }
    if (el.tagName === 'IMG') {
      const id = `s${slideIndex}img${imgId++}`;
      el.setAttribute('data-pptx-img', id);
      items.push({ kind: 'image', id, ...box(r) });
      return;
    }
    if (el.tagName === 'STYLE' || el.tagName === 'SCRIPT') return;
    if (el !== sec) shapeOf(el, cs, r);
    pseudo(el, r, '::before');
    if (el.tagName === 'TABLE') { tableItem(el, r); return; }
    if ((el.tagName === 'UL' || el.tagName === 'OL') && cs.display === 'block' && cs.columnCount === 'auto'
        && [...el.children].every((li) => isTextBlock(li))) { listItem(el, cs, r); return; }
    if (el !== sec && isTextBlock(el)) {
      // a block-level text element may still contain inline images (rare): treat text only
      textItem(el, cs, r, el.tagName === 'LI' ? { bullet: true } : {});
      return;
    }
    for (const c of el.children) visit(c);
    pseudo(el, r, '::after');
  }

  const bg = rgba(getComputedStyle(sec).backgroundColor);
  for (const c of sec.children) visit(c);
  return { bg: bg ? bg.hex : 'FFFFFF', items, bgImage: bgImage ? bgImage[1] : null };
}

// ---------------------------------------------------------------- browser side
async function extract(browser, file) {
  const page = await browser.newPage();
  await page.setViewport({ width: 1280, height: 720, deviceScaleFactor: SCALE });
  await page.goto('file://' + path.resolve(file), { waitUntil: 'networkidle0' });
  await page.evaluate(() => document.fonts.ready);
  // lay the slides out one per viewport-height, unscaled
  await page.addStyleTag({ content: 'html,body{height:auto!important;overflow:visible!important;scroll-snap-type:none!important} body>svg{width:1280px!important;height:720px!important}' });
  const n = await page.evaluate(() => document.querySelectorAll('body > svg[data-marpit-svg]').length);
  await page.addStyleTag({ content: 'html.pptx-solo, html.pptx-solo body{background:transparent!important} .pptx-solo body *{visibility:hidden!important} .pptx-solo body .pptx-show{visibility:visible!important}' });
  const slides = [];
  for (let i = 0; i < n; i++) {
    const s = await page.evaluate(`(${extractSection.toString()})(${i})`);
    // pictures: show only this slide at the top-left of the page, hide everything but one <img>, screenshot its box
    await page.evaluate((i) => {
      document.querySelectorAll('body > svg[data-marpit-svg]').forEach((svg, k) => { svg.style.display = k === i ? '' : 'none'; });
      window.scrollTo(0, 0);
    }, i);
    // images in a slide that was hidden are decoded again lazily: wait for them, then two frames
    await page.evaluate(async (i) => {
      const svg = document.querySelectorAll('body > svg[data-marpit-svg]')[i];
      await Promise.all([...svg.querySelectorAll('img')].map((im) => im.decode().catch(() => {})));
      await new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r)));
    }, i);
    await new Promise((r) => setTimeout(r, 150));
    const origin = await page.evaluate((i) => {
      const svg = document.querySelectorAll('body > svg[data-marpit-svg]')[i];
      const r = svg.getBoundingClientRect();
      return { x: r.left, y: r.top };
    }, i);
    for (const it of s.items.filter((x) => x.kind === 'image')) {
      await page.evaluate((id) => {
        document.documentElement.classList.add('pptx-solo');
        document.querySelector(`[data-pptx-img="${id}"]`).classList.add('pptx-show');
      }, it.id);
      await page.evaluate(() => new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r))));
      it.png = await page.screenshot({ clip: { x: origin.x + it.x, y: origin.y + it.y, width: it.w, height: it.h }, omitBackground: true, encoding: 'base64' });
      await page.evaluate((id) => {
        document.documentElement.classList.remove('pptx-solo');
        document.querySelector(`[data-pptx-img="${id}"]`).classList.remove('pptx-show');
      }, it.id);
    }
    await page.evaluate(() => document.querySelectorAll('body > svg[data-marpit-svg]').forEach((svg) => { svg.style.display = ''; }));
    slides.push(s);
  }
  await page.close();
  return slides;
}

// ---------------------------------------------------------------- pptx side
const inch = (px) => px / PX;
const pt = (px) => px * 0.75;

const NAMED = { 300: ' Light', 500: ' Medium', 600: ' SemiBold', 800: ' ExtraBold' };
function face(r) {   // static font files name their weights as separate families, e.g. "Nunito SemiBold"
  if (/virgil/i.test(r.font)) return 'Virgil';
  return r.font + (NAMED[Math.round(r.weight / 100) * 100] || '');
}
function runOpts(r) {
  const o = { fontFace: face(r), fontSize: pt(r.size), bold: r.bold, italic: r.italic, color: r.color };
  if (r.spacing) o.charSpacing = pt(r.spacing);
  if (r.sub) o.subscript = true;
  if (r.link) o.hyperlink = { url: r.link };
  return o;
}
function toTextProps(runs, base = {}) {
  const out = [];
  runs.forEach((r, i) => {
    if (r.br) { if (out.length) out[out.length - 1].options.breakLine = true; return; }
    out.push({ text: r.text, options: { ...runOpts(r), ...base } });
  });
  return out;
}

function addSlide(pres, s, note) {
  const slide = pres.addSlide();
  slide.background = { color: s.bg };
  for (const it of s.items) {
    const pos = { x: inch(it.x), y: inch(it.y), w: inch(it.w), h: inch(it.h) };
    if (it.kind === 'shape') {
      const o = { ...pos, fill: it.fill ? { color: it.fill.hex, transparency: Math.round((1 - it.fill.a) * 100) } : { type: 'none' },
                  line: it.line ? { color: it.line.hex, width: pt(it.line.w), dashType: it.line.dash === 'dashed' ? 'dash' : it.line.dash === 'dotted' ? 'sysDot' : 'solid' } : { type: 'none' } };
      if (it.ellipse) slide.addShape(pres.ShapeType.ellipse, o);
      else if (it.radius > 0.5) slide.addShape(pres.ShapeType.roundRect, { ...o, rectRadius: inch(it.radius) });
      else slide.addShape(pres.ShapeType.rect, o);
    } else if (it.kind === 'image') {
      slide.addImage({ data: 'image/png;base64,' + it.png, ...pos });
    } else if (it.kind === 'text') {
      if (!it.runs.length) continue;
      const slack = it.singleLine ? Math.max(8, it.w * 0.08) : 3;   // PowerPoint's text is a touch wider than Chrome's
      let x = pos.x, w = inch(it.w + slack);
      if (it.align === 'center') x -= inch(slack / 2);
      if (it.align === 'right') x -= inch(slack);
      slide.addText(toTextProps(it.runs), {
        x, y: pos.y, w, h: pos.h, margin: 0, align: it.align, valign: it.valign, isTextBox: true,
        lineSpacing: +pt(it.lineHeight * it.fontSize).toFixed(1), wrap: !it.singleLine, fit: 'none',
        ...(it.bullet ? { bullet: true } : {}),
      });
    } else if (it.kind === 'list') {
      const paras = [];
      it.paras.forEach((p, k) => {
        const tp = toTextProps(p.runs);
        if (!tp.length) return;
        tp[0].options.bullet = it.numbered ? { type: 'number', indent: pt(it.indent) } : { indent: pt(it.indent) };
        tp[0].options.paraSpaceAfter = pt(p.after);
        if (k < it.paras.length - 1) tp[tp.length - 1].options.breakLine = true;
        paras.push(...tp);
      });
      slide.addText(paras, { x: pos.x, y: pos.y, w: inch(it.w + 4), h: pos.h, margin: 0, valign: 'top', isTextBox: true,
                             lineSpacing: +pt(it.lineHeight * it.fontSize).toFixed(1), fit: 'none' });
    } else if (it.kind === 'table') {
      const rows = it.rows.map((row) => row.cells.map((c) => ({
        text: toTextProps(c.runs).map((t, i, a) => i === a.length - 1 ? t : t),
        options: { fill: c.fill ? { color: c.fill.hex } : { color: 'FFFFFF' }, valign: c.valign,
                   margin: c.pad.map((p) => pt(p)), lineSpacing: +pt(c.lineHeight * c.fontSize).toFixed(1),
                   border: { type: 'solid', pt: pt(c.bw), color: c.border ? c.border.hex : 'DFE6EB' } },
      })));
      slide.addTable(rows, { x: pos.x, y: pos.y, w: pos.w, colW: it.colW.map(inch), rowH: it.rows.map((r) => inch(r.h)), autoPage: false });
    }
  }
  if (note) slide.addNotes(note);
}

(async () => {
  const browser = await puppeteer.launch({ executablePath: CHROME, headless: true, args: ['--allow-file-access-from-files', '--no-sandbox'] });
  const deck = await extract(browser, deckHtml);
  const gantt = ganttHtml ? await extract(browser, ganttHtml) : [];
  await browser.close();

  const notes = fs.readFileSync(notesFile, 'utf8').split(/\n\n---\n\n/).map((s) => s.trim());
  const md = fs.readFileSync(process.env.DECK_MD || 'deck.md', 'utf8');   // build.sh sets DECK_MD=_slides.md
  const titleMatch = md.match(/^title:\s*"?(.*?)"?\s*$/m);

  const pres = new PptxGenJS();
  pres.layout = 'LAYOUT_WIDE';                      // 13.333" x 7.5" = 1280 x 720 px
  pres.title = titleMatch ? titleMatch[1] : 'Deck';
  pres.author = 'Team 147';
  deck.forEach((s, i) => {
    // the Gantt slide is a background picture in the Marp deck; use its own editable slide instead
    const isGantt = gantt.length && s.bgImage && /gantt/i.test(s.bgImage);
    addSlide(pres, isGantt ? gantt[0] : s, notes[i] || '');
  });
  await pres.writeFile({ fileName: outFile });
  console.log(`wrote ${outFile}: ${deck.length} slides`);
})().catch((e) => { console.error(e); process.exit(1); });
