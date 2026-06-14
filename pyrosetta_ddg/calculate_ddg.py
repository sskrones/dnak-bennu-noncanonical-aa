"""
calculate_ddg.py

Computes PyRosetta ddG (Delta Delta G) values for non-canonical amino acid
substitutions in the E. coli DnaK chaperone (PDB: 4B9Q, chain A).

Two structurally and functionally critical regions are targeted:
  - Interdomain linker:        L390, L391  (pose numbering: 381, 382)
  - SBD beta-sandwich:         A429, A435  (pose numbering: 418, 424)

Method
------
For each (position, amino acid) pair:
  1. Score the wild-type pose with the ref2015 energy function.
  2. Mutate the target residue using PyRosetta's mutate_residue utility.
  3. Re-score the mutant pose with the same energy function.
  4. ddG = E_mutant - E_wild_type   (Rosetta Energy Units, REU)

No backbone minimization is applied (rigid-backbone approximation). This is
fast and useful for first-pass screening, but can overestimate ddG for
bulky substitutions -- see the "Limitations" section of the thesis report.

Non-canonical amino acids are specified via their Rosetta / CCD three-letter
codes. Codes without a registered rotamer library (NLE -> "NLU", ABA, B3A)
will raise a RotamerLibraryError, which is caught and logged as "ERROR" in
the results table.

Requirements
------------
    pip install pyrosetta-installer
    python -c "import pyrosetta_installer; pyrosetta_installer.install_pyrosetta()"

Usage
-----
    python calculate_ddg.py --pdb 4b9q.pdb --out ddg_results.csv
"""

import argparse
import csv
import sys

import pyrosetta
from pyrosetta import pose_from_pdb, get_fa_scorefxn
from pyrosetta.toolbox import mutate_residue


# ---------------------------------------------------------------------------
# Target positions (pose numbering for chain A of 4B9Q)
# ---------------------------------------------------------------------------
POSITIONS = {
    "L390": 381,   # interdomain linker
    "L391": 382,   # interdomain linker
    "A429": 418,   # SBD beta-sandwich
    "A435": 424,   # SBD beta-sandwich
}

# Pairs evaluated as double mutants
DOUBLE_MUTANTS = {
    "L390+L391": ("L390", "L391"),
    "A429+A435": ("A429", "A435"),
}

# Non-canonical amino acid CCD / Rosetta three-letter codes
# (NLE, ABA, B3A do not have registered rotamer libraries in standard
#  PyRosetta builds and are expected to raise an error -- this is reported
#  in the thesis as a methodological limitation, not a bug.)
AMINO_ACIDS = {
    "NVA": "NVL",   # norvaline
    "VAL": "VAL",   # valine  (canonical, used as a comparison point)
    "ILE": "ILE",   # isoleucine (canonical, used as a comparison point)
    "AIB": "AIB",   # alpha-aminoisobutyric acid
    "NLE": "NLU",   # norleucine -- expected ERROR (no rotamer library)
    "ABA": "ABA",   # alpha-aminobutyric acid -- expected ERROR
    "B3A": "B3A",   # beta-alanine -- expected ERROR (backbone incompatible)
}


def score_pose(pose, scorefxn):
    return scorefxn(pose)


def calc_single_ddg(wt_pose, scorefxn, pose_index, ccd_code):
    """Return ddG (REU) for a single-position substitution, or None on error."""
    mutant = wt_pose.clone()
    mutate_residue(mutant, pose_index, ccd_code)
    return score_pose(mutant, scorefxn)


def calc_double_ddg(wt_pose, scorefxn, pose_index_a, pose_index_b, ccd_code):
    """Return ddG (REU) for a simultaneous double substitution."""
    mutant = wt_pose.clone()
    mutate_residue(mutant, pose_index_a, ccd_code)
    mutate_residue(mutant, pose_index_b, ccd_code)
    return score_pose(mutant, scorefxn)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdb", required=True, help="Path to 4B9Q PDB file (chain A)")
    parser.add_argument("--out", default="ddg_results.csv", help="Output CSV path")
    args = parser.parse_args()

    pyrosetta.init("-mute all")
    scorefxn = get_fa_scorefxn()  # ref2015

    wt_pose = pose_from_pdb(args.pdb)
    e_wt = score_pose(wt_pose, scorefxn)
    print(f"Wild-type ref2015 score: {e_wt:.3f} REU")

    rows = []

    # Single-position substitutions
    for label, pose_idx in POSITIONS.items():
        for aa_name, ccd in AMINO_ACIDS.items():
            try:
                e_mut = calc_single_ddg(wt_pose, scorefxn, pose_idx, ccd)
                ddg = e_mut - e_wt
                rows.append([aa_name, label, f"{ddg:.3f}", "OK"])
                print(f"{aa_name:>4s} {label:>6s}: ddG = {ddg:+.3f} REU")
            except RuntimeError as exc:
                rows.append([aa_name, label, "ERROR", str(exc).splitlines()[0]])
                print(f"{aa_name:>4s} {label:>6s}: ERROR ({exc})", file=sys.stderr)

    # Double-position substitutions
    for label, (pos_a, pos_b) in DOUBLE_MUTANTS.items():
        idx_a, idx_b = POSITIONS[pos_a], POSITIONS[pos_b]
        for aa_name, ccd in AMINO_ACIDS.items():
            try:
                e_mut = calc_double_ddg(wt_pose, scorefxn, idx_a, idx_b, ccd)
                ddg = e_mut - e_wt
                rows.append([aa_name, label, f"{ddg:.3f}", "OK"])
                print(f"{aa_name:>4s} {label:>10s}: ddG = {ddg:+.3f} REU")
            except RuntimeError as exc:
                rows.append([aa_name, label, "ERROR", str(exc).splitlines()[0]])
                print(f"{aa_name:>4s} {label:>10s}: ERROR ({exc})", file=sys.stderr)

    with open(args.out, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["amino_acid", "position", "ddg_REU", "status"])
        writer.writerows(rows)

    print(f"\nResults written to {args.out}")


if __name__ == "__main__":
    main()
