#!/usr/bin/env python3
"""Parse fabrication ZIPs independently and check layers, drills, hashes and cap clearance.
Requires scripts/requirements-validation.txt. Does not alter manufacturing files.
"""
import hashlib,json,math
from pathlib import Path
from gerbonara import LayerStack
from shapely.geometry import box
from shapely.affinity import rotate,translate
from itertools import combinations
manifest=json.loads(Path('fabrication/manifest.json').read_text())
audit=json.loads(Path('validation/electrical-layout-audit.json').read_text())
original=json.loads(Path('validation/original-layout.json').read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
reports={}
for side in ['left','right']:
 m=manifest['boards'][side];p=Path('fabrication')/m['zip']
 assert sha(p)==m['zip_sha256']
 assert sha(Path(f'hardware/{side}.kicad_pcb'))==m['source_sha256']
 assert sha(Path(f'hardware/{side}.kicad_dru'))==m['rules_sha256']
 assert sha(Path(f'validation/{side}-drc.json'))==m['drc_sha256']
 stack=LayerStack.open(p)
 expected={(s,u) for s in ['top','bottom'] for u in ['copper','mask','silk']}|{('mechanical','outline')}
 assert set(stack.graphic_layers)==expected
 assert len(stack.drill_pth.objects)==audit[side]['plated_drill_hits']
 assert len(stack.drill_npth.objects)==audit[side]['nonplated_drill_hits']==119
 for kind,layer in [('plated',stack.drill_pth),('nonplated',stack.drill_npth)]:
  pending=list(audit[side]['drills_mm'][kind])
  for obj in layer.objects:
   actual=(obj.x,obj.y,obj.aperture.diameter)
   match=min(range(len(pending)),key=lambda i:sum((a-b)**2 for a,b in zip(actual,pending[i])))
   assert max(abs(a-b) for a,b in zip(actual,pending.pop(match)))<.001, (side,kind,actual)
  assert not pending
 assert len(stack['top','copper'].objects)>100 and len(stack['bottom','copper'].objects)>100
 keys=[]
 for ref,f in original[side].items():
  w,h=f['keycap_width'],f['keycap_height']
  keys.append((ref,translate(rotate(box(-w/2,-h/2,w/2,h/2),-f['rotation'],origin=(0,0)),f['x'],f['y'])))
 minimum=min((a.distance(b),ra,rb) for (ra,a),(rb,b) in combinations(keys,2))
 assert minimum[0]>.749
 # nice!nano module body envelope, USB-up, with 15.24 mm socket row spacing.
 cx=214.5 if side=='left' else 255.5
 module=box(cx-8.89,104.22,cx+8.89,137.24)
 controller_gap=min(poly.distance(module) for _,poly in keys)
 assert controller_gap>1.48
 # The canonical preview uses explicit colors without SVG filters.
 for face in ['top','bottom']:
  colors={f'{face} copper':'#ad6518',f'{face} silk':'#1c4770','mechanical outline':'#222222','drill pth':'#ffffff','drill npth':'#555555'}
  svg=str(stack.to_svg(colors=colors,side_re=f'{face}|mechanical',margin=1))
  Path(f'docs/previews/{side}-{face}.svg').write_text(svg)
 reports[side]={'parse':'PASS','layers':sorted('/'.join(x) for x in expected),'plated_drill_hits':len(stack.drill_pth.objects),'nonplated_drill_hits':len(stack.drill_npth.objects),'minimum_keycap_gap_mm':minimum[0],'closest_keycaps':minimum[1:],'minimum_controller_keycap_gap_mm':controller_gap,'bounds_including_outline_stroke_mm':stack.bounding_box(),'source_and_zip_hashes':'PASS','drill_coordinates_and_diameters':'PASS'}
Path('validation/gerber-mechanical-audit.json').write_text(json.dumps(reports,indent=2)+'\n')
print(json.dumps(reports,indent=2))
