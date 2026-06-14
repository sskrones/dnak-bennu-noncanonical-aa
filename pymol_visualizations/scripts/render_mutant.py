"""
render_mutant.py

Generates the three standard PyMOL views (close, mid, wide) used in the
thesis figures for each DnaK mutant: a superposition of the wild-type
structure (4B9Q) and the corresponding Boltz-2-predicted mutant structure,
with the mutated residue(s) shown as sticks.

Color scheme
------------
    Wild-type cartoon : blue / slate
    Mutant cartoon    : depends on amino acid
        NVA -> green
        ILE -> orange
        VAL -> cyan
        AIB -> magenta
    Wild-type side chain at mutated position : orange/yellow sticks
    Mutant side chain at mutated position    : yellow sticks (mutant-specific)

Three views per mutant
-----------------------
    *_close.png  : tight zoom on the mutated residue(s) and immediate
                    surroundings (beta-sandwich / linker pocket)
    *_wt.png     : mid-range view showing the domain (SBD or NBD-SBD
                    linker region) containing the mutation
    *_zoom.png   : whole-protein view showing the global fold

Requirements
------------
    PyMOL (open-source build): conda install -c conda-forge pymol-open-source

Usage
-----
    pymol -cq render_mutant.py -- \\
        --wt wild_type.pdb \\
        --mutant 390-391NVA.pdb \\
        --positions 390,391 \\
        --color green \\
        --outprefix 390-391NVA
"""

import argparse
import sys

from pymol import cmd


MUTANT_COLORS = {
    "NVA": "green",
    "ILE": "orange",
    "VAL": "cyan",
    "AIB": "magenta",
}


def render(wt_path, mutant_path, positions, mutant_color, outprefix):
    cmd.reinitialize()
    cmd.load(wt_path, "wt")
    cmd.load(mutant_path, "mut")

    # Superimpose mutant onto wild-type
    cmd.align("mut", "wt")

    # Base cartoon coloring
    cmd.hide("everything")
    cmd.show("cartoon", "wt or mut")
    cmd.color("slate", "wt")
    cmd.color(mutant_color, "mut")
    cmd.set("cartoon_transparency", 0.0)
    cmd.bg_color("black")

    # Highlight mutated residue side chains
    resi_sel = "+".join(str(p) for p in positions)
    cmd.show("sticks", f"wt and resi {resi_sel} and not name C+N+O")
    cmd.show("sticks", f"mut and resi {resi_sel} and not name C+N+O")
    cmd.color("yelloworange", f"wt and resi {resi_sel}")
    cmd.color("yellow", f"mut and resi {resi_sel}")

    cmd.orient(f"resi {resi_sel}")
    cmd.zoom(f"resi {resi_sel}", buffer=6)
    cmd.ray(1200, 900)
    cmd.png(f"{outprefix}_close.png", dpi=150)

    # Mid view: zoom out to show the surrounding domain
    cmd.zoom(f"resi {resi_sel}", buffer=20)
    cmd.ray(1200, 900)
    cmd.png(f"{outprefix}_wt.png", dpi=150)

    # Wide view: whole protein
    cmd.orient("wt or mut")
    cmd.zoom("wt or mut", buffer=4)
    cmd.ray(1200, 900)
    cmd.png(f"{outprefix}_zoom.png", dpi=150)

    print(f"Wrote {outprefix}_close.png, {outprefix}_wt.png, {outprefix}_zoom.png")


def main(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wt", required=True, help="Wild-type structure (PDB/CIF)")
    parser.add_argument("--mutant", required=True, help="Boltz-2 mutant structure (PDB/CIF)")
    parser.add_argument("--positions", required=True, help="Comma-separated mutated residue numbers, e.g. 390,391")
    parser.add_argument("--color", choices=MUTANT_COLORS.values(), help="Override mutant cartoon color")
    parser.add_argument("--aa", choices=MUTANT_COLORS.keys(), help="Amino acid code (used to pick color if --color not given)")
    parser.add_argument("--outprefix", required=True, help="Output filename prefix")
    args = parser.parse_args(argv)

    positions = [int(p) for p in args.positions.split(",")]
    color = args.color or MUTANT_COLORS.get(args.aa, "green")

    render(args.wt, args.mutant, positions, color, args.outprefix)


if __name__ == "__main__":
    # PyMOL passes script args after "--"
    if "--" in sys.argv:
        main(sys.argv[sys.argv.index("--") + 1:])
    else:
        main(sys.argv[1:])
