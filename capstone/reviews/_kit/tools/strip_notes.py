import sys
from pptx import Presentation
from pptx.opc.constants import RELATIONSHIP_TYPE as RT
for path in sys.argv[1:]:
    prs = Presentation(path)
    n = 0
    for slide in prs.slides:
        for rId, rel in list(slide.part.rels.items()):
            if rel.reltype == RT.NOTES_SLIDE:
                slide.part.drop_rel(rId); n += 1
    prs.save(path)
    print(path, 'notes removed from', n, 'slides')
