# conceptnet-numberbatch

The main location of this repository is on GitHub, which may contain updates:

  http://github.com/commonsense/conceptnet-numberbatch

The code and paper for the previous version of this system, also referred to as
the 'ConceptNet Vector Ensemble', are available in a branch of this repository:

  https://github.com/commonsense/conceptnet-numberbatch/tree/16.04

## Introduction

This is the data from an ensemble that combines ConceptNet, word2vec, and GloVe
using a variation on retrofitting.  It was previously known as the "ConceptNet
Vector Ensemble".

ConceptNet Numberbatch consists of high-quality term vectors (that is, word
embeddings) that can be used directly as a representation of word meanings or
as a starting point for further machine learning.

Here is [a paper we wrote about the previous version](https://arxiv.org/pdf/1604.01692v1.pdf) in early 2016.

The code and paper were created as a research project of [Luminoso Technologies, Inc.][luminoso], by Rob Speer and Joshua Chin.


## License and attribution

These vectors are distributed under the [CC-By-SA 4.0][cc-by-sa] license. In
short, if you distribute a transformed or modified version of these vectors,
you must release them under a compatible Share-Alike license and give due
credit to [Luminoso][luminoso].

Some suggested text:

    This data contains semantic vectors from Conceptnet Numberbatch, by
    Luminoso Technologies, Inc. You may redistribute or modify the
    data under the terms of the CC-By-SA 4.0 license.

[cc-by-sa]: https://creativecommons.org/licenses/by-sa/4.0/
[luminoso]: http://luminoso.com

If you build on this data, you should cite it. We recommend citing the
arXiV preprint for now:

> Robert Speer and Joshua Chin. "An Ensemble Method to Produce High-Quality Word Embeddings." arXiv preprint arXiv:1604.01692 (2016).

In BibTeX form, the citation is:

    @article{speer2016ensemble,
      title={An Ensemble Method to Produce High-Quality Word Embeddings},
      author={Speer, Robert and Chin, Joshua},
      journal={arXiv preprint arXiv:1604.01692},
      year={2016}
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

# Available languages
Conceptnet-Numberbatch contains entities for 78 languages. This entities are aligned between languages, so '/c/en/mother' ~= '/c/fr/mère'.

The available languages are :

| language| n_entities |
|---------|------------|
| en      | 426572     |
| fr      | 298650     |
| de      | 129382     |
| ja      | 121508     |
| it      | 91821      |
| fi      | 56882      |
| zh      | 50437      |
| pt      | 47586      |
| la      | 46722      |
| nl      | 45238      |
| es      | 44756      |
| ru      | 37498      |
| sh      | 31503      |
| sv      | 28516      |
| cs      | 25937      |
| pl      | 22387      |
| ms      | 20979      |
| bg      | 20873      |
| ca      | 20402      |
| eo      | 18821      |
| hu      | 17512      |
| el      | 16926      |
| no      | 14590      |
| is      | 12645      |
| sl      | 11457      |
| ro      | 10872      |
| ga      | 10865      |
| vi      | 10576      |
| lv      | 10127      |
| grc     | 9896       |
| tr      | 9876       |
| da      | 9700       |
| ar      | 9293       |
| fa      | 8620       |
| ko      | 7732       |
| hy      | 7593       |
| eu      | 7436       |
| fro     | 7361       |
| io      | 7317       |
| oc      | 7008       |
| gd      | 6852       |
| gl      | 6378       |
| nrf     | 6190       |
| ka      | 6130       |
| th      | 6121       |
| he      | 5940       |
| sq      | 5511       |
| fo      | 4760       |
| te      | 4617       |
| mk      | 4369       |
| se      | 4329       |
| mul     | 4239       |
| et      | 4122       |
| gv      | 4071       |
| sk      | 4060       |
| xcl     | 4033       |
| hi      | 3979       |
| af      | 3753       |
| ang     | 3661       |
| lt      | 3486       |
| ast     | 3429       |
| uk      | 3075       |
| cy      | 2761       |
| nv      | 2698       |
| mg      | 2696       |
| kk      | 2462       |
| rup     | 2317       |
| sa      | 2257       |
| non     | 2247       |
| vo      | 2115       |
| be      | 2097       |
| sw      | 1995       |
| ur      | 1834       |
| ku      | 1813       |
| fil     | 1571       |
| az      | 976        |
| ta      | 925        |
| hsb     | 740        |
