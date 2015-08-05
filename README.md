# wide-learning-paper

This package contains the LaTeX source of our paper on retrofitting with
ConceptNet in the `paper/` directory. It also contains the code that
implements it in the `code/` directory, in a module named
`wide_learning`.

## Building the paper

To build the paper, run `ninja` in the `paper/` directory. The result will
be in `wordsim_paper.pdf`.

## Installing the code

- Install dependencies such as the master versions of ConceptNet 5.4 and
  wordfreq 1.0.

- Run `python setup.py develop` in the `code/` directory.

Next you'll need to set up git-annex so you can get the large data files and
track them when they change:

- Install `git annex` if you don't already have it.

- Read its walkthrough at https://git-annex.branchable.com/walkthrough/.
  git-annex is very useful but you don't want to do anything to your files
  behind its back. If you find that git-annex has prevented you from modifying
  a file, don't override it. It is probably stopping you from doing something
  dumb.

- Set up a remote that knows about the files, on an appropriate shared
  computer:

    git remote add SERVERNAME SERVERNAME:/data/annex/

- Make sure you can connect to the server without a password. In my case, that
  required me to add `eval ssh-agent` to the end of my `.bashrc`.

- Get the files:

    cd code/data
    git annex get
