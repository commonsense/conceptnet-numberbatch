# conceptnet-numberbatch

The main location of this repository is on GitHub, which may contain updates:

  http://github.com/commonsense/conceptnet-numberbatch

The code and paper for the previous version of this system, also referred to as
the 'ConceptNet Vector Ensemble', are available in a branch of this repository:

  https://github.com/commonsense/conceptnet-numberbatch/tree/16.04

## Introduction

This is the data from an ensemble that combines ConceptNet, word2vec, and GloVe
using a variation on retrofitting.

ConceptNet Numberbatch consists of high-quality term vectors (that is, word
embeddings) that can be used directly as a representation of word meanings or
as a starting point for further machine learning.

It is described in the paper [ConceptNet 5.5: An Open Multilingual Graph of General Knowledge][cn55paper],
presented at AAAI 2017.

[cn55paper]: https://arxiv.org/abs/1612.03975

The code and paper were created as a research project of [Luminoso Technologies, Inc.][luminoso], by Rob Speer, Joshua Chin, and Catherine Havasi.


## License and attribution

These vectors are distributed under the [CC-By-SA 4.0][cc-by-sa] license. In
short, if you distribute a transformed or modified version of these vectors,
you must release them under a compatible Share-Alike license and give due
credit to [Luminoso][luminoso].

Some suggested text:

    This data contains semantic vectors from ConceptNet Numberbatch, by
    Luminoso Technologies, Inc. You may redistribute or modify the
    data under the terms of the CC-By-SA 4.0 license.

[cc-by-sa]: https://creativecommons.org/licenses/by-sa/4.0/
[luminoso]: http://luminoso.com

If you build on this data, you should cite it. Here is a straightforward citation:

> Robert Speer, Joshua Chin, and Catherine Havasi (2017). "ConceptNet 5.5: An Open Multilingual Graph of General Knowledge." In proceedings of AAAI 2017.

In BibTeX form, the citation is:

    @inproceedings{speer2017conceptnet,
        author    = {Robert Speer and Joshua Chin and Catherine Havasi},
        title     = {ConceptNet 5.5: An Open Multilingual Graph of General Knowledge},
        book      = {AAAI},
        year      = {2017},
        url       = {http://arxiv.org/abs/1612.03975}
    }

This data is itself built on:

  - [ConceptNet 5.5][conceptnet], which contains data from Wiktionary,
    WordNet, and many contributors to Open Mind Common Sense projects,
    edited by Rob Speer

  - [GloVe][glove], by Jeffrey Pennington, Richard Socher, and Christopher
    Manning

  - [word2vec][], by Tomas Mikolov and Google Research

[conceptnet]: http://conceptnet5.media.mit.edu
[glove]: http://nlp.stanford.edu/projects/glove/
[word2vec]: https://code.google.com/archive/p/word2vec/


## Downloading the term vectors

The `*.txt.gz` files of term vectors are too large to include in the GitHub
repository for this package.  You should follow the links provided here to
download them.

## Format of the term vectors

The term vectors are in the text format used by GloVe, which is similar to
the format used by word2vec but without a header line.

Each line contains a term label followed by 300 floating-point numbers,
separated by spaces:

    /c/en/absolute_value -0.1410 -0.0641 -0.0618 0.2627 -0.0177 -0.2862 -0...
    /c/en/absolute_zero 0.0074 -0.0272 -0.1510 0.0817 0.0648 -0.2144 -0.03...
    /c/en/absoluteless 0.3960 -0.0599 0.0875 0.1853 -0.1459 -0.0827 0.0142...
    /c/en/absolutely -0.0455 -0.1817 0.1297 0.0954 0.0150 0.0417 0.0772 0....
    /c/en/absolutely_convergent 0.4119 0.1030 -0.0579 0.2609 -0.0179 -0.29...

To make this into word2vec format, add a header line with two numbers
representing the height and width of the matrix. These dimensions are listed
below.

There are four files available for download, providing different representations
of the data:

* [`conceptnet-numberbatch-201609_uris_main.txt.gz`][uris_main] (1928481 × 300)
  contains terms from many languages, specified by their complete ConceptNet
  URI (the strings starting with `/c/en/` in the example above).

* [`conceptnet-numberbatch-201609_en_main.txt.gz`][en_main] (426572 × 300)
  contains only English terms, and strips the `/c/en/` prefix to provide just
  the term text.  This form is the most compatible with other systems, as long
  as you only want English.

* [`conceptnet-numberbatch-201609_en_extra.txt.gz`][en_extra] (233488 × 300)
  contains additional single words of English whose vectors could be inferred
  as the average of their neighbors in ConceptNet.

* [`conceptnet-numberbatch-201609.h5`][h5] contains the data in
  its native HDF5 format, which can be loaded with the Python library `pandas`.

If you have the ConceptNet database, the `extra` data should be redundant,
but it provides a convenient way to expand the vocabulary without looking
terms up in ConceptNet.

[uris_main]: http://conceptnet5.media.mit.edu/downloads/conceptnet-numberbatch-16.09/conceptnet-numberbatch-201609_uris_main.txt.gz
[en_main]: http://conceptnet5.media.mit.edu/downloads/conceptnet-numberbatch-16.09/conceptnet-numberbatch-201609_en_main.txt.gz
[en_extra]: http://conceptnet5.media.mit.edu/downloads/conceptnet-numberbatch-16.09/conceptnet-numberbatch-201609_en_extra.txt.gz
[h5]: http://conceptnet5.media.mit.edu/downloads/conceptnet-numberbatch-16.09/conceptnet-numberbatch-201609.h5

We have included here the code necessary to convert text into ConceptNet URIs,
in `text_to_uri.py`.
