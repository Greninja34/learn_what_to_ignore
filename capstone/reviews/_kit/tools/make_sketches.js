// Hand-drawn sketches for the deck, in the Claude Design template's style:
// rough.js, roughness 1, bowing 1, 2 px strokes at 1280 wide, solid fills, fixed seed.
// Run: node tools/make_sketches.js   (writes into assets/sketch/)
// Layout constants are mirrored by the HTML label overlays in deck.md; change both together.
// loop.svg and the h3_*.svg files come from the Claude Design template (recoloured), not from here.
const fs = require('fs');
const path = require('path');
const rough = require('roughjs/bundled/rough.cjs.js');

const INK = '#12151B', CARD = '#EBF0F4', META = '#59606B';
const ACCENT = '#0078CD', ACCENT_FILL = '#E0ECF9';
const OUT = path.join(__dirname, '..', 'assets', 'sketch');

function sketch(name, width, height, seed, draw) {
  const g = rough.generator();
  const parts = [];
  const opts = (o) => Object.assign({ roughness: 1, bowing: 1, strokeWidth: 2, seed: seed++, fillStyle: 'solid' }, o);
  const add = (drawable, dash) => {
    for (const p of g.toPaths(drawable)) {
      const d = dash && p.fill === undefined ? ` stroke-dasharray="${dash}"` : '';
      parts.push(`<path d="${p.d}" stroke="${p.stroke}" stroke-width="${p.strokeWidth}" fill="${p.fill || 'none'}" stroke-linecap="round" stroke-linejoin="round"${d}/>`);
    }
  };
  const api = {
    box: (x, y, w, h, o = {}) => add(g.rectangle(x, y, w, h, opts(o)), o.dash),
    line: (x1, y1, x2, y2, o = {}) => add(g.line(x1, y1, x2, y2, opts(o)), o.dash),
    dot: (x, y, d, o = {}) => add(g.circle(x, y, d, opts(o))),
    // straight arrow with an open head of two short strokes at ±27°
    arrow: (x1, y1, x2, y2, o = {}) => {
      api.line(x1, y1, x2, y2, o);
      const a = Math.atan2(y2 - y1, x2 - x1), L = 13, t = (27 * Math.PI) / 180;
      api.line(x2, y2, x2 - L * Math.cos(a - t), y2 - L * Math.sin(a - t), { ...o, dash: undefined });
      api.line(x2, y2, x2 - L * Math.cos(a + t), y2 - L * Math.sin(a + t), { ...o, dash: undefined });
    },
  };
  draw(api);
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}" viewBox="0 0 ${width} ${height}">${parts.join('')}</svg>`;
  fs.writeFileSync(path.join(OUT, name), svg);
  console.log('wrote', name);
}

// A row of boxes between two terminals, joined by arrows: [term] -> box ... box -> [term]
function chain(s, L, accentIdx = []) {
  const mid = L.boxY + L.boxH / 2;
  s.box(2, mid - L.termH / 2, L.termW - 4, L.termH, { fill: CARD, stroke: INK });
  s.box(L.W - L.termW + 2, mid - L.termH / 2, L.termW - 4, L.termH, { fill: CARD, stroke: INK });
  s.arrow(L.termW + 4, mid, L.boxX0 - 6, mid, { stroke: INK });
  for (let i = 0; i < L.n; i++) {
    const x = L.boxX0 + i * (L.boxW + L.gap);
    const ours = accentIdx.includes(i);
    s.box(x, L.boxY, L.boxW, L.boxH, { fill: ours ? ACCENT_FILL : CARD, stroke: ours ? ACCENT : INK });
    const next = i < L.n - 1 ? x + L.boxW + L.gap : L.W - L.termW;
    s.arrow(x + L.boxW + 5, mid, next - 6, mid, { stroke: INK });
  }
}

// ---- general OCR pipeline: image -> 5 stages -> text (1152 x 130) ----
const PIPE = { W: 1152, n: 5, termW: 92, termH: 56, boxX0: 128, boxW: 152, gap: 34, boxY: 6, boxH: 118 };
sketch('ocr_pipeline_general.svg', PIPE.W, 130, 7, (s) => chain(s, PIPE, [3]));

// ---- inside text recognition: 4 stage boxes, each with a tree of algorithms below (1152 x 340) ----
// Branch tips are at REC.tips; the HTML labels sit just right of each tip.
const REC = { boxW: 240, gap: 64, boxY: 4, boxH: 140, rows: [190, 232, 274] };
// tree: a trunk dropping from (x, y0) with an arrow to each row, ending at x + len
const tree = (s, x, y0, ys, len) => {
  s.line(x, y0, x, ys[ys.length - 1], { stroke: INK, strokeWidth: 1.6 });
  ys.forEach((y) => s.arrow(x, y, x + len, y, { stroke: INK, strokeWidth: 1.6 }));
};
sketch('recognition_stages.svg', 1152, 340, 21, (s) => {
  const top = REC.boxY + REC.boxH;
  for (let i = 0; i < 4; i++) {
    const x = i * (REC.boxW + REC.gap);
    s.box(x + 2, REC.boxY, REC.boxW - 4, REC.boxH, { fill: CARD, stroke: INK });
    if (i < 3) s.arrow(x + REC.boxW + 6, REC.boxY + REC.boxH / 2, x + REC.boxW + REC.gap - 6, REC.boxY + REC.boxH / 2, { stroke: INK });
    if (i === 0 || i === 2) tree(s, x + 28, top, REC.rows.slice(0, 2), 30);  // 1: TPS, STN   3: BiLSTM, Transformer
    if (i === 1) tree(s, x + 28, top, REC.rows, 30);                         // 2: VGG, ResNet, ViT
    if (i === 3) {                                       // 4: CTC -> CRNN, Rosetta; Attention -> RARE, SAR, PARSeq
      tree(s, x + 22, top, [REC.rows[0]], 22);
      tree(s, x + 34, REC.rows[0] + 14, [REC.rows[1], REC.rows[2]], 22);
      tree(s, x + 132, top, [REC.rows[0]], 20);
      tree(s, x + 144, REC.rows[0] + 14, [REC.rows[1], REC.rows[2], REC.rows[2] + 42], 20);
    }
  }
});

// ---- today vs this project: two rows of four equal boxes (1152 x 350) ----
const TVP = { x0: 176, boxW: 216, gap: 36, boxH: 130, rows: [10, 210] };
sketch('today_vs_project.svg', 1152, 350, 41, (s) => {
  TVP.rows.forEach((y, r) => {
    for (let i = 0; i < 4; i++) {
      const x = TVP.x0 + i * (TVP.boxW + TVP.gap);
      s.box(x, y, TVP.boxW, TVP.boxH, r ? { fill: ACCENT_FILL, stroke: ACCENT } : { fill: CARD, stroke: META });
      if (i < 3) s.arrow(x + TVP.boxW + 5, y + TVP.boxH / 2, x + TVP.boxW + TVP.gap - 6, y + TVP.boxH / 2, { stroke: r ? ACCENT : META });
    }
  });
});

// ---- research-question charts (330 x 240 each; axes origin at (36, 170)) ----
const AX = { x: 36, y: 170, top: 30, right: 320 };
const axes = (s) => {
  s.line(AX.x, AX.top, AX.x, AX.y, { stroke: INK });
  s.line(AX.x, AX.y, AX.right, AX.y, { stroke: INK });
};
const BAR = { w: 66, centres: [92, 180, 268] };
const bars = (s, heights, lastIsQuestion) => heights.forEach((h, i) => {
  const q = lastIsQuestion && i === heights.length - 1;
  s.box(BAR.centres[i] - BAR.w / 2, AX.y - h, BAR.w, h,
    q ? { fill: ACCENT_FILL, stroke: ACCENT, dash: '7 6' } : { fill: CARD, stroke: META });
});
sketch('rq1.svg', 330, 240, 61, (s) => { axes(s); bars(s, [118, 92, 62], true); });
sketch('rq2.svg', 330, 240, 71, (s) => { axes(s); bars(s, [120, 82, 44]); s.arrow(AX.x + 8, 210, AX.right, 210, { stroke: META, strokeWidth: 1.6 }); });
sketch('rq3.svg', 330, 240, 81, (s) => {
  axes(s);
  s.line(AX.x + 14, 156, AX.right - 10, 52, { stroke: ACCENT, dash: '8 7' });
  [[64, 150], [92, 146], [120, 128], [150, 124], [178, 108], [206, 112], [236, 92], [262, 88], [290, 70]]
    .forEach(([x, y]) => s.dot(x, y, 9, { fill: META, stroke: META, roughness: 0.6 }));
});
