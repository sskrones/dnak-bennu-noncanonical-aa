# Boltz-2 Structure Predictions

This folder contains the input configurations used to generate AI-based
3D structure predictions for wild-type and mutant DnaK with Boltz-2,
run via the [tamarind.bio](https://www.tamarind.bio/) platform.

## Files

- **`jobs.csv`** — List of all 11 completed prediction jobs (job name,
  mutated position(s) in PDB residue numbering, CCD code, description).
- **`generate_configs.py`** — Generates Boltz-2 YAML input configs from
  `jobs.csv` and a FASTA file containing the DnaK chain A sequence.
- **`4b9q_chainA.fasta`** — DnaK chain A sequence (587 aa, 4B9Q).
- **`inputs/`** — Generated YAML configs, one per job.

## Completed Jobs

| Job | Region | Mutation |
|---|---|---|
| `wild_type` | — | none (reference) |
| `390NVA` | Linker | L390 → NVA |
| `391NVA` | Linker | L391 → NVA |
| `390-391NVA` | Linker | L390+L391 → NVA |
| `390-391ILE` | Linker | L390+L391 → ILE |
| `390-391VAL` | Linker | L390+L391 → VAL |
| `390-391AIB` | Linker | L390+L391 → AIB |
| `429NVA` | SBD | A429 → NVA |
| `429ILE` | SBD | A429 → ILE |
| `435ILE` | SBD | A435 → ILE |
| `429-435ILE` | SBD | A429+A435 → ILE |

## Numbering

Positions in `jobs.csv` use **PDB author numbering** (390, 391, 429, 435),
matching the residue numbers in 4B9Q itself, the job names, and the PyMOL
figure labels used throughout the thesis.

This was verified directly against the Boltz-2 output structure: in the
`390-391NVA` model, the predicted NVA residues are located at residue
numbers **390 and 391**, exactly matching L390/L391 in the wild-type
structure. The tamarind.bio Boltz-2 runner correctly handles PDB-numbered
positions.

## Usage

```bash
pip install pyyaml
python generate_configs.py --fasta 4b9q_chainA.fasta --jobs jobs.csv --outdir inputs/
```

Upload the resulting YAML files to a Boltz-2 runner (e.g. tamarind.bio, or
a local Boltz-2 installation). Predicted structures were superimposed on
the wild-type structure in PyMOL — see `../pymol_visualizations/`.
