"""
generate_configs.py

Generates Boltz-2 input YAML files for each DnaK mutant job listed in
jobs.csv. Each job specifies one or two sequence positions (using the
PDB residue numbering of 4B9Q chain A, e.g. 390, 391, 429, 435) and a
CCD code for the substituting non-canonical amino acid.

Predictions were run via the tamarind.bio Boltz-2 web interface; this
script produces the equivalent YAML configs for reproducibility / local
use with the open-source Boltz-2 model.

Note on numbering
------------------
Positions in jobs.csv use PDB author numbering (390, 391, 429, 435),
matching the residue numbers in 4B9Q, the job names, and the PyMOL figure
labels used throughout the thesis. This was confirmed against the actual
Boltz-2 output: the predicted NVA residues in the 390-391NVA model appear
at residue numbers 390 and 391, exactly as intended.

generate_configs.py writes these positions directly into the YAML
"modifications" field.

Usage
-----
    python generate_configs.py --fasta 4b9q_chainA.fasta --jobs jobs.csv --outdir inputs/
"""

import argparse
import csv
import os

import yaml


def read_fasta_sequence(path):
    seq_lines = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line.startswith(">") or not line:
                continue
            seq_lines.append(line)
    return "".join(seq_lines)


def build_config(sequence, positions, ccd):
    config = {
        "version": 1,
        "sequences": [
            {
                "protein": {
                    "id": "A",
                    "sequence": sequence,
                }
            }
        ],
    }
    if positions:
        config["modifications"] = [
            {"position": pos, "ccd": ccd} for pos in positions
        ]
    return config


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fasta", required=True, help="FASTA file with the DnaK chain A sequence (4B9Q)")
    parser.add_argument("--jobs", default="jobs.csv", help="CSV listing jobs (job_name, positions, ccd, description)")
    parser.add_argument("--outdir", default="inputs", help="Output directory for YAML configs")
    args = parser.parse_args()

    sequence = read_fasta_sequence(args.fasta)
    os.makedirs(args.outdir, exist_ok=True)

    with open(args.jobs) as f:
        reader = csv.DictReader(f)
        for row in reader:
            job_name = row["job_name"]
            positions_raw = row["positions"].strip()
            positions = [int(p) for p in positions_raw.split(",") if p] if positions_raw else []
            ccd = row["ccd"].strip() or None

            config = build_config(sequence, positions, ccd)
            out_path = os.path.join(args.outdir, f"{job_name}.yaml")
            with open(out_path, "w") as out_f:
                yaml.dump(config, out_f, sort_keys=False)
            print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
