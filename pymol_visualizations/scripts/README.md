# PyMOL Visualizations

This folder contains the rendered structural comparison figures (30 PNGs)
and the script used to generate them.

## Images (`images/`)

For each mutant, three views are provided:

| Suffix | Description |
|---|---|
| `_close` | Tight view on the mutated residue(s) and immediate pocket |
| `_wt` | Mid-range view of the containing domain (linker or SBD) |
| `_zoom` | Whole-protein view showing the global fold |

## Color Scheme

| Element | Color |
|---|---|
| Wild-type cartoon | Blue / slate |
| NVA mutant cartoon | Green |
| ILE mutant cartoon | Orange |
| VAL mutant cartoon | Cyan |
| AIB mutant cartoon | Magenta |
| Wild-type side chain at mutation site | Orange/yellow sticks |
| Mutant side chain at mutation site | Yellow sticks |

## Script (`scripts/render_mutant.py`)

Generates all three views for a given wild-type / mutant structure pair.

```bash
pymol -cq render_mutant.py -- \
    --wt wild_type.pdb \
    --mutant 390-391NVA.pdb \
    --positions 390,391 \
    --aa NVA \
    --outprefix 390-391NVA
```

Requires the open-source PyMOL build:

```bash
conda install -c conda-forge pymol-open-source
```

## Mutants Visualized

Linker region (L390–L391): `390NVA`, `391NVA`, `390-391NVA`, `390-391ILE`,
`390-391VAL`, `390-391AIB`

SBD region (A429–A435): `429NVA`, `429ILE`, `435ILE`, `429-435ILE`
