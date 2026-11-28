#!/usr/bin/python3
"""Convert Ergogen scaffolds to KiCad 9 sources and Specctra routing inputs."""
import os
for key, value in [('XDG_CACHE_HOME','/tmp/kicad-cache'),('XDG_CONFIG_HOME','/tmp/kicad-config'),('XDG_DATA_HOME','/tmp/kicad-data')]:
    os.environ.setdefault(key,value)
import pcbnew as k
from pathlib import Path
Path('output/kicad').mkdir(parents=True, exist_ok=True)
for side in ('left','right'):
    b=k.LoadBoard(f'output/pcbs/{side}.kicad_pcb')
    ds=b.GetDesignSettings()
    ds.m_MinClearance=k.FromMM(0.2)
    ds.m_TrackMinWidth=k.FromMM(0.2)
    ds.m_MinThroughDrill=k.FromMM(0.3)
    ds.m_ViasMinSize=k.FromMM(0.6)
    ds.m_CopperEdgeClearance=k.FromMM(0.5)
    nc=ds.m_NetSettings.GetDefaultNetclass()
    nc.SetClearance(k.FromMM(0.2)); nc.SetTrackWidth(k.FromMM(0.25))
    nc.SetViaDiameter(k.FromMM(0.6)); nc.SetViaDrill(k.FromMM(0.3))
    for f in b.GetFootprints():
        if f.GetReference().startswith('S'):
            f.SetValue('Kailh MX CPG151101S11')
        if f.GetReference().startswith('MCU'):
            f.SetValue('nice!nano v2, components up')
    b.SetCopperLayerCount(2)
    k.SaveBoard(f'output/kicad/{side}.kicad_pcb',b)
    k.ExportSpecctraDSN(b, f'output/kicad/{side}.dsn')
