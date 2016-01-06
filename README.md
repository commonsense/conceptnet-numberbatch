# conceptnet-retrofitting-ensemble

This package contains the LaTeX source of our paper on retrofitting with
ConceptNet in the `paper/` directory. It also contains the code that
implements it in the `code/` directory, in a Python module named
`conceptnet_retrofitting`.

## Installing the code

- Install base dependencies such as NumPy and SciPy.

- Run `python setup.py develop` in the `code/` directory.

Next you'll need to set up git-annex so you can get the large data files and
track them when they change:

- Install `git-annex` if you don't already have it.

- Read its walkthrough at https://git-annex.branchable.com/walkthrough/.
  git-annex is very useful but you don't want to do anything to your files
  behind its back. If you find that git-annex has prevented you from modifying
  a file, don't override it. It is probably stopping you from doing something
  dumb.

- Get the files (this should default to downloading them over the web):

    cd code/data
    git annex get
