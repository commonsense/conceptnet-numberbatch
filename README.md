# conceptnet-numberbatch

This repository describes and implements an ensemble method that combines
ConceptNet, word2vec, GloVe, and PPDB using a variation on retrofitting.
It was previously known as the "ConceptNet Vector Ensemble", including in
a paper we've written about the system.

The `paper/` directory contains the LaTeX source of our paper.  The `code/`
directory contains a Python module called `conceptnet_retrofitting`,
implementing the code that was used in the paper.

This code produces high-quality term vectors (that is, word embeddings) that
can be used directly as a representation of word meanings or as a starting
point for further machine learning. Instead of setting up the dependencies for
this code, you may just want to download them directly: see "Downloading the
term vectors" below.

The code and paper were created as a research project of [Luminoso
Technologies, Inc.][luminoso], by Rob Speer and Joshua Chin.


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

  - [ConceptNet 5.4][conceptnet], which contains data from Wiktionary,
    WordNet, and many contributors to Open Mind Common Sense projects,
    edited by Rob Speer

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


## Installing the code

If you want to be able to run the code included here, to reproduce the results
or build a similar set of term vectors:

- Install base dependencies such as Python 3, NumPy, and SciPy.

- Install [git-annex](http://git-annex.branchable.com) and
  [ninja](http://ninja-build.org).

- Set up the Python package:

```sh
cd code
python setup.py develop
```

Next you'll need to set up git-annex so you can get the large data files and
track them when they change:

- Read the git-annex walkthrough at
  https://git-annex.branchable.com/walkthrough/.  git-annex is very useful but
  you don't want to do anything to your files behind its back. If you find that
  git-annex has prevented you from modifying a file, don't override it. It is
  probably stopping you from doing something dumb.

- Get the files (this should default to downloading them over the web):

```sh
git annex get
```

Finally, start the build process that will create and evaluate the various
spaces of term embeddings that are described in the paper:

```sh
cd ..                # this should return you to the `code/` directory
python ninja.py      # generate the build script
ninja                # run the build
```

The code itself is distributed under the MIT license; see MIT-LICENSE.


### Requirements for building

- A POSIX-compatible system with utilities such as `grep` and `cut`
- **System dependencies**: git-annex, ninja-build, Python 3.3 or later
- **Python dependencies**: numpy, scipy, pandas, ftfy, scikit-learn, wordfreq,
  and ordered-set. These will mostly be installed automatically via `setup.py`,
  but large dependencies such as numpy and scipy may be easier to install
  separately.
- 32 GB of RAM

