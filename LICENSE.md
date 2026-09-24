# Licensing

DaMuSc contains three kinds of material with different rights, and they are
licensed separately. Nothing in this file grants rights that the DaMuSc
maintainers do not hold.

| Material | Where | Licence |
|---|---|---|
| Code | `Src/` and any other scripts | MIT ([LICENSE-MIT.txt](LICENSE-MIT.txt)) |
| Database: compilation, annotations, metadata | `Data/`, `Metadata/`, `example_scales.csv`, and any scale record files added in future | CC BY 4.0 ([LICENSE-CC-BY-4.0.txt](LICENSE-CC-BY-4.0.txt)) |
| Third-party materials | see below | Not licensed by DaMuSc; rights remain with their owners |

## 1. Code — MIT

Copyright (c) 2022–2026 John M. McBride and contributors. Full text in
`LICENSE-MIT.txt`.

## 2. Database — CC BY 4.0

The selection, arrangement, and annotation of scales in DaMuSc, together
with the society table, column definitions, inclusion criteria, and notes,
are © 2022–2026 John M. McBride and contributors and are released under
the Creative Commons Attribution 4.0 International licence. Full text in
`LICENSE-CC-BY-4.0.txt`; summary at
<https://creativecommons.org/licenses/by/4.0/>.

You may share and adapt the database for any purpose, including
commercially, provided you give appropriate credit. The requested citation
is:

> McBride JM, Passmore S, Tlusty T (2023) Convergent evolution in a large
> cross-cultural database of musical scales. PLoS ONE 18(12): e0284851.
> <https://doi.org/10.1371/journal.pone.0284851>

Where you use individual scales, please also cite the original source
listed for that scale in `Metadata/sources.csv`.

## 3. Third-party materials

DaMuSc is a compilation. The numerical values in it (intervals, frequencies,
tunings) were transcribed from the published sources listed in
`Metadata/sources.csv`, and from measurements made by the maintainers. The
maintainers do not claim copyright in those values: measured and reported
facts are not subject to copyright, and each value is attributed to its
source. The CC BY licence above covers DaMuSc's own contribution, namely
the selection, arrangement, annotation, and metadata, and does not purport
to license the underlying publications.

The following are **excluded** from the CC BY licence:

- **Evidence images.** Where the repository includes an image of a table,
  figure, or passage from a published source, that image is reproduced
  solely so that the transcription can be verified against the original.
  Copyright in each such image remains with its original publisher or
  author. Each image is accompanied by a record of its rights status
  (public domain; reproduced as a short quotation for verification; or
  reproduced with permission). Images of public-domain works may be
  reused freely; all others may be reused only as permitted by the
  rights holder or by applicable law. Rights holders who object to the
  inclusion of an image may contact the maintainers and it will be
  removed.

- **Society and language metadata** drawn from external databases.
  Identifiers and, where present, coordinates and language classifications
  in `Metadata/societies.csv` reference [Glottolog](https://glottolog.org)
  and [D-PLACE](https://d-place.org), both released under CC BY 4.0. Their
  contribution is attributed here and remains under their licence.

- **Pitch traces and extraction outputs** derived from audio recordings,
  where included, are DaMuSc's own derived data and fall under CC BY 4.0,
  but the underlying audio is not included and is not licensed by DaMuSc.

## Disclaimer

This licence statement reflects the maintainers' understanding of their
rights and is provided in good faith. It is not legal advice. If you need
certainty about a particular use, consult the rights holder of the
material concerned.
