# PyRosetta ΔΔG Calculations

This folder contains the scripts and results used to estimate the free
energy impact (ΔΔG) of substituting non-canonical amino acids at four
positions in *E. coli* DnaK (PDB: [4B9Q](https://www.rcsb.org/structure/4B9Q), chain A).

## Files

- **`calculate_ddg.py`** — PyRosetta script that performs the substitutions
  and computes ΔΔG = E_mutant − E_wild-type using the `ref2015` energy
  function (rigid-backbone, no minimization).
- **`ddg_results.csv`** — Full results table (41 rows): amino acid,
  position, ΔΔG in Rosetta Energy Units (REU), and a qualitative effect
  label.

## Target Positions

| Label | Pose index (4B9Q) | Region |
|---|---|---|
| L390 | 381 | Interdomain linker |
| L391 | 382 | Interdomain linker |
| A429 | 418 | SBD β-sandwich |
| A435 | 424 | SBD β-sandwich |

## Amino Acids Tested

| Code | Name | Rosetta/CCD code | Notes |
|---|---|---|---|
| NVA | Norvaline | NVL | |
| VAL | Valine | VAL | canonical, comparison point |
| ILE | Isoleucine | ILE | canonical, comparison point |
| AIB | α-Aminoisobutyric acid | AIB | |
| NLE | Norleucine | NLU | no rotamer library → ERROR |
| ABA | α-Aminobutyric acid | ABA | no rotamer library → ERROR |
| B3A | β-Alanine | B3A | backbone-incompatible → not computed |

## Running

```bash
pip install pyrosetta-installer
python -c "import pyrosetta_installer; pyrosetta_installer.install_pyrosetta()"

python calculate_ddg.py --pdb 4b9q.pdb --out ddg_results.csv
```

## Key Result

Norvaline (NVA) at the linker double-mutant position (L390+L391) produced
the strongest stabilization observed in the study: **ΔΔG = −6.090 REU**.
Isoleucine (ILE) at the SBD double-mutant position (A429+A435) produced
the strongest destabilization: **ΔΔG = +517.966 REU**.
