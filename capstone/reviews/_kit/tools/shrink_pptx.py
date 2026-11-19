# Re-encode large opaque PNG pictures in a .pptx as JPEG (q=85, longest side <= 2000 px)
# and point the slide relationships at the new files. Pictures whose only transparency is
# their rounded corners are flattened onto their slide's background colour first.
import sys, zipfile, io, re
import numpy as np
from PIL import Image
src, dst = sys.argv[1:3]
zin = zipfile.ZipFile(src)
renamed = {}
media = {}
# media file -> background colour of the slide that uses it
bg_of = {}
for n in zin.namelist():
    m = re.match(r'ppt/slides/_rels/(slide\d+)\.xml\.rels$', n)
    if not m:
        continue
    slide = zin.read(f'ppt/slides/{m.group(1)}.xml').decode()
    c = re.search(r'<p:bg>.*?srgbClr val="([0-9A-Fa-f]{6})"', slide)
    colour = tuple(int(c.group(1)[i:i+2], 16) for i in (0, 2, 4)) if c else (255, 255, 255)
    for t in re.findall(r'media/([^"]+)"', zin.read(n).decode()):
        bg_of[t] = colour
for info in zin.infolist():
    n = info.filename
    if n.startswith('ppt/media/') and n.endswith('.png') and info.file_size > 150_000:
        im = Image.open(io.BytesIO(zin.read(n)))
        rgba = im.convert('RGBA')
        alpha = np.asarray(rgba.getchannel('A'))
        if (alpha < 255).mean() > 0.005:
            continue                # really uses transparency: keep as PNG
        flat = Image.new('RGB', im.size, bg_of.get(n.split('/')[-1], (255, 255, 255)))
        flat.paste(rgba, mask=rgba.getchannel('A'))
        im = flat
        if max(im.size) > 2000:
            im.thumbnail((2000, 2000), Image.LANCZOS)
        buf = io.BytesIO(); im.save(buf, 'JPEG', quality=85, optimize=True)
        new = n[:-4] + '.jpg'
        renamed[n.split('/')[-1]] = new.split('/')[-1]
        media[new] = buf.getvalue()
        print(f'{n}: {info.file_size//1024} KB -> {len(buf.getvalue())//1024} KB')
zout = zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED)
for info in zin.infolist():
    n = info.filename
    if n.split('/')[-1] in renamed and n.startswith('ppt/media/'):
        new = 'ppt/media/' + renamed[n.split('/')[-1]]
        zout.writestr(new, media[new]); continue
    data = zin.read(n)
    if n.endswith('.rels'):
        s = data.decode()
        for old, new in renamed.items():
            s = s.replace(f'media/{old}"', f'media/{new}"')
        data = s.encode()
    if n == '[Content_Types].xml':
        s = data.decode()
        if 'Extension="jpg"' not in s:
            s = s.replace('<Default ', '<Default Extension="jpg" ContentType="image/jpeg"/><Default ', 1)
        data = s.encode()
    zout.writestr(info, data)
zout.close()
