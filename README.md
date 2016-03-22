# conceptnet-vector-ensemble

This repository describes implements an ensemble method that combines
ConceptNet, word2vec, GloVe, and PPDB using a variation on retrofitting.

The `paper/` directory contains the LaTeX source of our paper.  The `code/`
directory contains a Python module called `conceptnet_retrofitting`,
implementing the code that was used in the paper.


## Downloading the term vectors

This code produces high-quality term vectors (that is, word embeddings) that
can be used directly as a representation of word meanings or as a starting
point for further machine learning. Instead of setting up the dependencies
for this code, you may just want to download them directly.

You will need to download one of the two matrices, as well as the text file of
row labels, a UTF-8 plain text file which associates natural-language terms
with the vectors that form the rows of that matrix. Each line of the text file
corresponds to a row of the matrix, in order.

The 300d matrix is just the first 300 columns of the 600d matrix; the 600d
matrix may be slightly more accurate, but of course it requires twice as much
computation to use.

* Matrices in NumPy format: [600 dimensions][600d] or [300 dimensions][300d]
* [Row labels][row-labels] in ConceptNet normalized form

[600d]: http://conceptnet-api-1.media.mit.edu/downloads/annex/vector-ensemble/7cb/7f4/SHA256E-s6976070480--8ee85f7ad8475b2f4c21549017cbae88941d1c8875dbcbefaa08ad6433a36b00.npy/SHA256E-s6976070480--8ee85f7ad8475b2f4c21549017cbae88941d1c8875dbcbefaa08ad6433a36b00.npy
[300d]: http://conceptnet-api-1.media.mit.edu/downloads/annex/vector-ensemble/8cb/960/SHA256E-s3488035280--c0f86dec8dd44798792d7a14b1d1af8c6b4dd61dc442727c030e442f1d1dc7e2.300d.npy/SHA256E-s3488035280--c0f86dec8dd44798792d7a14b1d1af8c6b4dd61dc442727c030e442f1d1dc7e2.300d.npy
[row-labels]: http://conceptnet-api-1.media.mit.edu/downloads/annex/vector-ensemble/d9f/1e3/SHA256E-s23653394--89ea9d55f598edab60715d2523d3c7aacf6b444b777625a179da4cbeddeaed9b/SHA256E-s23653394--89ea9d55f598edab60715d2523d3c7aacf6b444b777625a179da4cbeddeaed9b

<!-- The URLs are horrible because they come directly from our git-annex. -->


## Installing the code

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
cd code/data
git annex get
```

Finally, start the build process that will create and evaluate the various
spaces of term embeddings that are described in the paper:

```sh
cd ..                # this should return you to the `code/` directory
python ninja.py      # generate the build script
ninja                # run the build
```

## Requirements for building

- A POSIX-compatible system with utilities such as `grep` and `cut`
- **System dependencies**: git-annex, ninja-build, Python 3.3 or later
- **Python dependencies**: numpy, scipy, pandas, ftfy, scikit-learn, wordfreq,
  and ordered-set. These will mostly be installed automatically via `setup.py`,
  but large dependencies such as numpy and scipy may be easier to install
  separately.
- 32 GB of RAM

