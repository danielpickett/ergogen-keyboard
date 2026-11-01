#!/usr/bin/python3
"""Audit layout, component counts and electrical pin assignments independently of DRC."""
import json, os
from pathlib import Path
os.environ.setdefault('XDG_CONFIG_HOME','/tmp/kicad-config')
import pcbnew as k
original=json.loads(Path('validation/original-layout.json').read_text())
cols=['P006','P008','P017','P020','P022','P024'];rows=['P115','P002','P029']
controller=['P006','P008','GND','GND','P017','P020','P022','P024','P100','P011','P104','P106','P009','P010','P111','P113','P115','P002','P029','P031','VCC','RST','GND','RAW']
report={}
for side in ['left','right']:
 b=k.LoadBoard(f'hardware/{side}.kicad_pcb');fs={f.GetReference():f for f in b.GetFootprints()}
 assert len(fs)==50,(side,len(fs))
 assert b.GetCopperLayerCount()==2
 def pads(ref):return {p.GetNumber():p for p in fs[ref].Pads() if p.GetNumber()}
 def nets(ref):return {n:p.GetNetname() for n,p in pads(ref).items()}
 for i in range(1,24):
  ref=f'S{i}';f=fs[ref];o=original[side][ref];x,y=k.ToMM(f.GetPosition())
  assert abs(x-o['x'])<0.0001 and abs(y-o['y'])<0.0001
  assert abs(f.GetOrientationDegrees()-o['rotation'])<1e-5
  s=nets(ref);d=nets(f'D{i}')
  c=cols[(i-1)//3] if i<=18 else cols[i-18]
  r=rows[(i-1)%3] if i<=18 else 'P113'
  assert s['1']==c and s['2']==d['2'] and d['1']==r,(side,ref,s,d)
  for part in (ref,f'D{i}'):
   assert all(p.GetAttribute()==k.PAD_ATTRIB_SMD and p.IsOnLayer(k.B_Cu) and not p.IsOnLayer(k.F_Cu) for p in pads(part).values())
  assert sum(p.GetAttribute()==k.PAD_ATTRIB_NPTH for p in f.Pads())==5
 assert nets('MCU1')=={str(n):v for n,v in enumerate(controller,1)}
 assert fs['MCU1'].GetOrientationDegrees()==-90
 assert nets('JST1')=={'1':'pos','2':'GND'}
 assert nets('B1')=={'1':'GND','2':'RST'}
 assert nets('T1')=={'1':'pos','2':'RAW','3':''}
 assert len(list(b.Zones()))==1 and next(iter(b.Zones())).GetIsRuleArea()
 assert len(list(b.GetTracks()))>0
 report[side]={'keys':23,'diodes':23,'controllers':1,'battery_connectors':1,'copper_layers':2,'layout_unchanged':True,'pin_assignment_audit':'PASS','tracks_and_vias':len(list(b.GetTracks())), 'plated_drill_hits':sum(p.GetAttribute()==k.PAD_ATTRIB_PTH for f in fs.values() for p in f.Pads())+sum(isinstance(t,k.PCB_VIA) for t in b.GetTracks()), 'nonplated_drill_hits':sum(p.GetAttribute()==k.PAD_ATTRIB_NPTH for f in fs.values() for p in f.Pads())}
 # Compare every exported drill coordinate/diameter independently of hit counts.
 drills={'plated':[], 'nonplated':[]}
 for f in fs.values():
  for p in f.Pads():
   if p.GetAttribute() not in (k.PAD_ATTRIB_PTH,k.PAD_ATTRIB_NPTH):continue
   x,y=k.ToMM(p.GetPosition());dx,dy=k.ToMM(p.GetDrillSize());assert abs(dx-dy)<1e-7
   drills['nonplated' if p.GetAttribute()==k.PAD_ATTRIB_NPTH else 'plated'].append([x,-y,dx])
 for t in b.GetTracks():
  if isinstance(t,k.PCB_VIA):
   x,y=k.ToMM(t.GetPosition());drills['plated'].append([x,-y,k.ToMM(t.GetDrillValue())])
 report[side]['drills_mm']=drills
Path('validation/electrical-layout-audit.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({s:{k:v for k,v in r.items() if k!='drills_mm'} for s,r in report.items()},indent=2))
