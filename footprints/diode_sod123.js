// 1N4148W, SOD-123: pad 1 = cathode (row), pad 2 = anode (switch).
// Land pattern matches KiCad Diode_SMD:D_SOD-123. Bottom assembly only.
module.exports = {
  params: { designator: 'D', from: undefined, to: undefined },
  body: p => `(module D_SOD123 (layer B.Cu) ${p.at}
    (fp_text reference "${p.ref}" (at 0 2 ${p.r}) (layer B.SilkS)
      (effects (font (size 0.8 0.8) (thickness 0.12)) (justify mirror)))
    (fp_text value "1N4148W" (at 0 0) (layer B.Fab) hide (effects (font (size 0.8 0.8) (thickness 0.12))))
    (fp_line (start -1.4 -1) (end 1.4 -1) (layer B.SilkS) (width 0.12))
    (fp_line (start -1.4 1) (end 1.4 1) (layer B.SilkS) (width 0.12))
    (fp_line (start -2.7 -1) (end -2.7 1) (layer B.SilkS) (width 0.15))
    (fp_line (start -2.7 -1.1) (end 2.7 -1.1) (layer B.CrtYd) (width 0.05))
    (fp_line (start 2.7 -1.1) (end 2.7 1.1) (layer B.CrtYd) (width 0.05))
    (fp_line (start 2.7 1.1) (end -2.7 1.1) (layer B.CrtYd) (width 0.05))
    (fp_line (start -2.7 1.1) (end -2.7 -1.1) (layer B.CrtYd) (width 0.05))
    (pad 1 smd rect (at -1.65 0 ${p.r}) (size 1.4 1.2) (layers B.Cu B.Paste B.Mask) ${p.to})
    (pad 2 smd rect (at 1.65 0 ${p.r}) (size 1.4 1.2) (layers B.Cu B.Paste B.Mask) ${p.from}))`
};
