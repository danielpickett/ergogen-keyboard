#!/usr/bin/env python3
"""Package only explicit Gerber/drill outputs and bind them to validated sources."""
import hashlib,json,sys,zipfile
from pathlib import Path
stage=Path(sys.argv[1]);out=Path('fabrication');out.mkdir(exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
manifest={'board_spec':{'layers':2,'thickness_mm':1.6,'copper_oz':1,'material':'FR4','minimum_track_mm':0.2,'minimum_clearance_mm':0.2,'minimum_via_drill_mm':0.3,'minimum_copper_edge_mm':0.5},'boards':{}}
for side in ['left','right']:
 files=sorted(p for p in (stage/side).iterdir() if p.suffix.lower() in {'.gtl','.gbl','.gts','.gbs','.gto','.gbo','.gm1','.drl'})
 assert {p.suffix.lower() for p in files}=={'.gtl','.gbl','.gts','.gbs','.gto','.gbo','.gm1','.drl'},files
 assert len(files)==9 and sum(p.suffix=='.drl' for p in files)==2
 for p in files:
  assert p.stat().st_size>40
  assert ('M30' if p.suffix=='.drl' else 'M02*') in p.read_text()
 target=out/f'pickett46-{side}-jlcpcb.zip'
 with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as z:
  for p in files:z.write(p,p.name)
 with zipfile.ZipFile(target) as z:assert z.testzip() is None
 manifest['boards'][side]={'source_sha256':sha(Path(f'hardware/{side}.kicad_pcb')),'rules_sha256':sha(Path(f'hardware/{side}.kicad_dru')),'drc_sha256':sha(Path(f'validation/{side}-drc.json')),'zip':target.name,'zip_sha256':sha(target),'files':{p.name:sha(p) for p in files}}
(out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Packaged and CRC-checked both fabrication ZIPs.')
