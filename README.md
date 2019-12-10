# conceptnet-numberbatch

This repository describes and implements an ensemble method that combines
ConceptNet, word2vec, GloVe, and PPDB using a variation on retrofitting.
It was previously known as the "ConceptNet Vector Ensemble", including in
[a paper we've written about the system](https://arxiv.org/pdf/1604.01692v1.pdf).

The `paper/` directory contains the LaTeX source of our paper.  The `code/`
directory contains a Python module called `conceptnet_retrofitting`,
implementing the code that was used in the paper.

This code produces high-quality term vectors (that is, word embeddings) that
can be used directly as a representation of word meanings or as a starting
point for further machine learning. Instead of setting up the dependencies for
this code, you may just want to download them directly: see "Downloading the
term vectors" below.

The code and paper were created as a research project of [Luminoso
Technologies, Inc.][luminoso], by Robyn Speer and Joshua Chin.


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

> Robyn Speer and Joshua Chin. "An Ensemble Method to Produce High-Quality Word Embeddings." arXiv preprint arXiv:1604.01692 (2016).

In BibTeX form, the citation is:

    @article{speer2016ensemble,
      title={An Ensemble Method to Produce High-Quality Word Embeddings},
      author={Speer, Robyn and Chin, Joshua},
      journal={arXiv preprint arXiv:1604.01692},
      year={2016}
    }


This data is itself built on:

  - [ConceptNet 5.4][conceptnet], which contains data from Wiktionary,
    WordNet, and many contributors to Open Mind Common Sense projects,
    edited by Robyn Speer

  - [GloVe][glove], by Jeffrey Pennington, Richard Socher, and Christopher
    Manning

  - [word2vec][], by Tomas Mikolov and Google Research

  - [PPDB][ppdb], by Juri Ganitkevitch, Benjamin Van Durme, and Chris
    Callison-Burch

[conceptnet]: http://conceptnet5.media.mit.edu
[glove]: http://nlp.stanford.edu/projects/glove/
[word2vec]: https://code.google.com/archive/p/word2vec/
[ppdb]: http://www.cis.upenn.edu/~ccb/ppdb/


## Downloading the term vectors

To use these vectors, you should download one of the following two matrices, as
well as the text file of row labels, a UTF-8 plain text file which associates
natural-language terms with the vectors that form the rows of that matrix. Each
line of the text file corresponds to a row of the matrix, in order.

* Matrices in NumPy format: [600 dimensions][600d] or [300 dimensions][300d]
* [Row labels][row-labels] in ConceptNet normalized form

[600d]: http://conceptnet-api-1.media.mit.edu/downloads/vector-ensemble/conceptnet-ensemble-201603-600d.npy
[300d]: http://conceptnet-api-1.media.mit.edu/downloads/vector-ensemble/conceptnet-ensemble-201603-300d.npy
[row-labels]: http://conceptnet-api-1.media.mit.edu/downloads/vector-ensemble/conceptnet-ensemble-201603-labels.txt

The 300d matrix is just the first 300 columns of the 600d matrix; the 600d
matrix may be slightly more accurate, but of course it requires twice as much
computation to use.

The `conceptnet` Python package can transform text into ConceptNet normalized
form. This transformation is important to the performance of the term vectors.
If you run `pip install conceptnet==5.4.2`, you should then be able to transform text
like this:

```python
>>> from conceptnet5.nodes import standardized_concept_uri

>>> standardized_concept_uri('en', 'this is an example')
'/c/en/be_example'
```

ConceptNet 5.5 will handle stemming differently and require a new version of Numberbatch,
so make sure to get version 5.4.2 when reproducing this paper.


## Building

Sadly, this version of the code is no longer reproducible unless you happen to have the input data.
Because we chose at the time to rely on the unusable and unmaintainable `git-annex`, we don't.
We recommend using [the updated build process that has been incorporated into ConceptNet](https://github.com/commonsense/conceptnet5/wiki/Build-process).
