![ConceptNet Numberbatch](conceptnet-numberbatch.png)

The main location of this repository is on GitHub, which may contain updates:

  http://github.com/commonsense/conceptnet-numberbatch


## The best word embeddings you can use

ConceptNet Numberbatch consists of state-of-the-art semantic vectors (also
known as word embeddings) that can be used directly as a representation of word
meanings or as a starting point for further machine learning.

It is built using an ensemble that combines data from ConceptNet, word2vec,
GloVe, and (since 17.02) OpenSubtitles 2016, using a variation on
retrofitting. It is described in the paper [ConceptNet 5.5: An Open
Multilingual Graph of General Knowledge][cn55-paper], presented at AAAI 2017.

ConceptNet Numberbatch took first place in both subtasks at SemEval 2017 task
2, "[Multilingual and Cross-lingual Semantic Word Similarity][semeval17-2]".
Within that task, it was also the first-place system in each of English,
German, Italian, and Spanish. The result is described in our ACL 2017 SemEval
paper, "[Extending Word Embeddings with Multilingual Relational Knowledge][semeval-paper]".

[cn55-paper]: https://arxiv.org/abs/1612.03975
[semeval17-2]: http://alt.qcri.org/semeval2017/task2/
[semeval-paper]: https://arxiv.org/abs/1704.03560

The code and papers were created as a research project of [Luminoso
Technologies, Inc.][luminoso], by Rob Speer, Joshua Chin, Catherine Havasi, and
Joanna Lowry-Duda.

![Graph of performance on English evaluations](eval_graph.png)


### Now with more fairness

Word embeddings are prone to learn human-like stereotypes and prejudices.
ConceptNet Numberbatch 17.04 counteracts this as part of its build process,
leading to word vectors that are less prejudiced than competitors such as
word2vec and GloVe. See [our blog post on reducing
bias](https://blog.conceptnet.io/?p=642&shareadraft=58f92dfc71aad).

![Graph of biases](bias_graph.png)


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

    @paper{speer2017conceptnet,
        author = {Robert Speer and Joshua Chin and Catherine Havasi},
        title = {ConceptNet 5.5: An Open Multilingual Graph of General Knowledge},
        conference = {AAAI Conference on Artificial Intelligence},
        year = {2017},
        pages = {4444--4451},
        keywords = {ConceptNet; knowledge graph; word embeddings},
        url = {http://aaai.org/ocs/index.php/AAAI/AAAI17/paper/view/14972}
    }

This data is itself built on:

  - [ConceptNet 5.5][conceptnet], which contains data from Wiktionary,
    WordNet, and many contributors to Open Mind Common Sense projects,
    edited by Rob Speer

  - [GloVe][glove], by Jeffrey Pennington, Richard Socher, and Christopher
    Manning

  - [word2vec][], by Tomas Mikolov and Google Research

  - Parallel text from [OpenSubtitles 2016][opensubtitles], by Pierre Lison
    and Jörg Tiedemann, analyzed using [fastText][], by Piotr Bojanowski,
    Edouard Grave, Armand Joulin, and Tomas Mikolov

[conceptnet]: http://conceptnet5.media.mit.edu
[glove]: http://nlp.stanford.edu/projects/glove/
[word2vec]: https://code.google.com/archive/p/word2vec/
[opensubtitles]: http://opus.lingfil.uu.se/OpenSubtitles2016.php
[fastText]: https://github.com/facebookresearch/fastText


## Downloading the term vectors

The `*.txt.gz` files of term vectors are too large to include in the GitHub
repository for this package.  You should follow the links provided here to
download them.

The term vectors are in the text format used by word2vec, GloVe, and fastText.

The first line of the file contains the dimensions of the matrix:

    1984681 300

Each line contains a term label followed by 300 floating-point numbers,
separated by spaces:

    /c/en/absolute_value -0.0847 -0.1316 -0.0800 -0.0708 -0.2514 -0.1687 -...
    /c/en/absolute_zero 0.0056 -0.0051 0.0332 -0.1525 -0.0955 -0.0902 0.07...
    /c/en/absoluteless 0.2740 0.0718 0.1548 0.1118 -0.1669 -0.0216 -0.0508...
    /c/en/absolutely 0.0065 -0.1813 0.0335 0.0991 -0.1123 0.0060 -0.0009 0...
    /c/en/absolutely_convergent 0.3752 0.1087 -0.1299 -0.0796 -0.2753 -0.1...

* [`numberbatch-17.04.txt.gz`][nb1702] contains this data in 77 languages.

* [`numberbatch-en-17.04.txt.gz`][nb1702-en] contains just the English subset
  of the data, with the `/c/en/` prefix removed.

This data is sufficient to work as a drop-in replacement for word2vec or GloVe.
However, to achieve the best results and reproduce our performance at SemEval,
you will also need the ConceptNet database and its strategy for looking up
words, including those that are out-of-vocabulary. You'll find this in the
`conceptnet5.vectors` sub-package of the [ConceptNet
code](https://github.com/commonsense/conceptnet5).

We have included here the code necessary to convert text into ConceptNet URIs,
in `text_to_uri.py`.

[nb1704]: http://conceptnet.s3.amazonaws.com/downloads/2017/numberbatch/numberbatch-17.04.txt.gz
[nb1704-en]: http://conceptnet.s3.amazonaws.com/downloads/2017/numberbatch/numberbatch-en-17.04.txt.gz


## Previous versions

### February 2017

Numberbatch 17.02 contains the updates that were made for SemEval and
its following paper, but not the de-biasing.

* [`numberbatch-17.02.txt.gz`][nb1702] contains the data in 77 languages.

* [`numberbatch-en-17.02.txt.gz`][nb1702-en] contains just the English subset.

[nb1702]: http://conceptnet.s3.amazonaws.com/downloads/2017/numberbatch/numberbatch-17.02.txt.gz
[nb1702-en]: http://conceptnet.s3.amazonaws.com/downloads/2017/numberbatch/numberbatch-en-17.02.txt.gz


### September 2016

The September 2016 version (ConceptNet Numberbatch 16.09) is available in these files:

* [`conceptnet-numberbatch-201609_uris_main.txt.gz`][uris_main] (1928481 × 300)
  contains terms from many languages, specified by their complete ConceptNet
  URI (the strings starting with `/c/en/`, for example).

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


### April 2016

The code and paper for the April 2016 version of this system, also referred to as
the 'ConceptNet Vector Ensemble', are available in a branch of this repository:

  https://github.com/commonsense/conceptnet-numberbatch/tree/16.04


## Language statistics

The multilingual data in ConceptNet Numberbatch represents 78 different language
codes, though some have vocabularies with much more coverage than others. The following
table lists the languages and their vocabulary size.

You may notice a focus on even the smaller and historical languages of Europe,
and under-representation of widely-spoken languages from outside Europe, which
is an effect of the availability of linguistic resources for these languages.
We would like to change this, but it requires finding good source data for
ConceptNet in these under-represented languages.

These vocabulary sizes were last updated for ConceptNet Numberbatch 17.02,
but they should not have changed significantly in 17.04.

| code | language                      | vocab size |
|:-----|:------------------------------|-----------:|
| en   | English                       |     484557 |
| fr   | French                        |     296987 |
| de   | German                        |     129405 |
| ja   | Japanese                      |     121683 |
| it   | Italian                       |      91828 |
| fi   | Finnish                       |      56900 |
| zh   | Chinese (Simp. + Trad.)       |      50185 |
| pt   | Portuguese                    |      47592 |
| la   | Latin                         |      46720 |
| nl   | Dutch                         |      45245 |
| es   | Spanish                       |      44756 |
| ru   | Russian                       |      37503 |
| sh   | Bosnian + Croatian + Serbian  |      31516 |
| sv   | Swedish                       |      28519 |
| cs   | Czech                         |      25934 |
| pl   | Polish                        |      22388 |
| ms   | Malay + Indonesian            |      20981 |
| bg   | Bulgarian                     |      20870 |
| ca   | Catalan                       |      20391 |
| eo   | Esperanto                     |      18820 |
| hu   | Hungarian                     |      17512 |
| el   | Greek                         |      16925 |
| no   | Norwegian (Bokmål + Nynorsk)  |      14591 |
| is   | Icelandic                     |      12645 |
| sl   | Slovenian                     |      11457 |
| ro   | Romanian                      |      10873 |
| ga   | Irish (Gaelic)                |      10865 |
| vi   | Vietnamese                    |      10341 |
| lv   | Latvian                       |      10129 |
| grc  | Ancient Greek                 |       9897 |
| tr   | Turkish                       |       9878 |
| da   | Danish                        |       9702 |
| ar   | Arabic                        |       9293 |
| fa   | Persian (Farsi)               |       8623 |
| ko   | Korean                        |       7770 |
| hy   | Armenian                      |       7593 |
| eu   | Basque                        |       7436 |
| fro  | Old French                    |       7361 |
| io   | Ido                           |       7316 |
| oc   | Occitan                       |       7000 |
| gd   | Scottish Gaelic               |       6851 |
| gl   | Galician                      |       6380 |
| nrf  | Jèrriais / Guernésiais        |       6190 |
| th   | Thai                          |       6133 |
| ka   | Georgian                      |       6130 |
| he   | Hebrew                        |       5940 |
| sq   | Albanian                      |       5511 |
| fo   | Faroese                       |       4761 |
| te   | Telugu                        |       4617 |
| mk   | Macedonian                    |       4369 |
| se   | Northern Sami                 |       4328 |
| mul  | (Multilingual conventions)    |       4316 |
| et   | Estonian                      |       4122 |
| gv   | Manx                          |       4071 |
| sk   | Slovak                        |       4059 |
| xcl  | Classical Armenian            |       4033 |
| hi   | Hindi                         |       3979 |
| af   | Afrikaans                     |       3753 |
| ang  | Old English                   |       3661 |
| lt   | Lithuanian                    |       3486 |
| ast  | Asturian                      |       3429 |
| uk   | Ukrainian                     |       3073 |
| cy   | Welsh                         |       2759 |
| nv   | Navajo                        |       2698 |
| mg   | Malagasy                      |       2696 |
| kk   | Kazakh                        |       2462 |
| rup  | Aromanian                     |       2317 |
| sa   | Sanskrit                      |       2257 |
| non  | Old Norse                     |       2247 |
| vo   | Volapük                       |       2115 |
| be   | Belarusian                    |       2097 |
| sw   | Swahili                       |       1995 |
| ur   | Urdu                          |       1834 |
| ku   | Kurdish                       |       1813 |
| fil  | Filipino (Tagalog)            |       1571 |
| az   | Azeri                         |        976 |
| ta   | Tamil                         |        925 |
| hsb  | Upper Sorbian                 |        740 |

