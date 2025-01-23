# DaMuSc: Database of Musical Scales

The purpose of this database is to collect musical scales that are found in societies across the world.

For those who are interested in an exhaustive list of microtonal scales for composing, the [Scala database](https://www.huygens-fokker.org/scala/) is more suitable.

At the moment, the majority of the scales are theory scales (scales with exact theoretical values for scale degrees), and measurements of instrument tunings. About 10% of measured data comes from computational analysis of recordings. We hope to add scales as they are measured in ongoing work. Anyone interested in contributing scales to DaMuSc should prepare them in the format shown in "example_scales.csv".

## Scales Data

### Data/theory_scales.csv
Scales where intervals and scale degrees are exactly specified by frequency ratios. These are mainly available in symbolic notation, and need to be further processed before scale degrees are available in cents.

### Data/measured_scales.csv
A mixture of instrument tunings and scales inferred from recordings. These are given in cents, and are presented as found in the original sources.

### Data/octave_scales.csv
Combination of the two sets of raw data, after being processed so that each scale spans an octave. This  set can be re-created with different parameters using the code provided.

## Metadata

### Metadata/societies.csv
Description of societies covered in the database, with unique identifiers. Where possible, the societies are matched to corresponding entries in the Ethnographic Atlas, Glottolog and Binford Hunter-gatherer datasets.

### Metadata/sources.csv
List of sources for all scales in the database. Notes are included on measurement techniques, and other points of interest.

### Metadata/column_key.csv
Descriptions of data columns.

### Metadata/inclusion_criteria.csv
Guide to decisions made about including / excluding data or sources from the database.


## Code for processing scales

### Src/process_csv.py

This can be used as a standalone module, or run from the command line:
> python Src/process_csv.py

There are several options when processing the raw data:
- "--n_min {n}" :: Set a minimum number of notes in a scale (Default n = 4)
- "--n_max {n}" :: Set a maximum number of notes in a scale (Default n = 9)
- "--octave_cutoff {O}" :: Set the allowed tolerance for deviations from a perfect octave of 1200 cents (Default O = 50 cents)
- "--use_specific_variants {True/False}" :: Set True to allow multiple scales to be drawn from a single tuning, if this information is specified by the original source (Default True)
- "--use_all_variants {True/False}" :: Set True to allow all possible scales to be drawn from a single tuning, including all circular permutations, but without skipping notes (Default False)

Here is an example of how you would run with a set of specific parameters:
> python Src/process_csv.py --n_min 4 --n_max 9 --octave_cutoff 50 --use_specific_variants True --use_all_variants False


Requirements:
Python3.7
Numpy
Pandas

## Citing DaMuSc
If you use this database in your work, please cite as, "McBride JM, Passmore S, Tlusty T (2023) Convergent evolution in a large cross-cultural database of musical scales. PLoS ONE 18(12): e0284851. [https://doi.org/10.1371/journal.pone.0284851](https://doi.org/10.1371/journal.pone.0284851)"

All scales are associated with a primary or secondary source, so it is encouraged to also cite sources individual scales when appropriate.
