![ConceptNet Numberbatch](conceptnet-numberbatch.png)


## The best word embeddings you can use

ConceptNet Numberbatch consists of state-of-the-art semantic vectors (also
known as word embeddings) that can be used directly as a representation of word
meanings or as a starting point for further machine learning.

ConceptNet Numberbatch is part of the [ConceptNet](http://conceptnet.io) open data
project. ConceptNet provides lots of ways to compute with word meanings, one of which
is word embeddings. ConceptNet Numberbatch is a snapshot of just the word embeddings.

It is built using an ensemble that combines data from ConceptNet, word2vec,
GloVe, and OpenSubtitles 2016, using a variation on retrofitting. It is
described in the paper [ConceptNet 5.5: An Open Multilingual Graph of General
Knowledge][cn55-paper], presented at AAAI 2017.


### Evaluation and publications

ConceptNet Numberbatch took first place in both subtasks at SemEval 2017 task
2, "[Multilingual and Cross-lingual Semantic Word Similarity][semeval17-2]".
Within that task, it was also the first-place system in each of English,
German, Italian, and Spanish. The result is described in our ACL 2017 SemEval
paper, "[Extending Word Embeddings with Multilingual Relational Knowledge][semeval-paper]".

[cn55-paper]: https://arxiv.org/abs/1612.03975
[semeval17-2]: http://alt.qcri.org/semeval2017/task2/
[semeval-paper]: https://arxiv.org/abs/1704.03560

The code and papers were created as a research project of [Luminoso
Technologies, Inc.][luminoso], by Robyn Speer, Joshua Chin, Catherine Havasi, and
Joanna Lowry-Duda.

![Graph of performance on English evaluations](eval-graph.png)


### Now with more fairness

Word embeddings are prone to learn human-like stereotypes and prejudices.
ConceptNet Numberbatch 17.04 counteracts this as part of its build process,
leading to word vectors that are less prejudiced than competitors such as
word2vec and GloVe. See [our blog post on reducing
bias](https://blog.conceptnet.io/2017/04/24/conceptnet-numberbatch-17-04-better-less-stereotyped-word-vectors/).

![Graph of biases](bias-graph.png)


## Code

Since 2016, the code for building ConceptNet Numberbatch is part of the [ConceptNet
code base][conceptnet5], in the `conceptnet5.vectors` package.

A preliminary paper we put on arXiV in April 2016 described the ConceptNet
Vector Ensemble, a previous version of this system. The code for that version
is still available in the `16.04` branch:

  https://github.com/commonsense/conceptnet-numberbatch/tree/16.04

The only code contained in _this_ repository is `text_to_uri.py`, which normalizes natural-language text into
the ConceptNet URI representation, allowing you to look up rows in these tables without requiring the entire
ConceptNet codebase. For all other purposes, please refer to the [ConceptNet code][conceptnet5].

[conceptnet5]: https://github.com/commonsense/conceptnet5


## Downloads

[ConceptNet Numberbatch 17.06][nb1706-main] is the current recommended download.

This table lists the downloads and formats available for multiple recent versions:

| Version | Multilingual                            | English-only                              | HDF5                         |
| ------- | --------------------------------------- | ----------------------------------------- | ---------------------------- |
| 17.06   | [numberbatch-17.06.txt.gz][nb1706-main] | [numberbatch-en-17.06.txt.gz][nb1706-en]  | [17.06/mini.h5][nb1706-mini] |
| 17.04   | [numberbatch-17.04.txt.gz][nb1704-main] | [numberbatch-en-17.04b.txt.gz][nb1704-en] | [17.05/mini.h5][nb1704-mini] |
| 17.02   | [numberbatch-17.02.txt.gz][nb1704-main] | [numberbatch-en-17.02.txt.gz][nb1702-en]  |                              |
| 16.09   |                                         |                                           | [16.09/numberbatch.h5][nb1609-h5] |

The 16.09 version was the version published at AAAI 2017. You can reproduce its results using a Docker snapshot of the conceptnet5 repository.
See the instructions on the [ConceptNet wiki](https://github.com/commonsense/conceptnet5/wiki/Running-your-own-copy#reproducing-the-word-embedding-evaluation).

[nb1706-main]: https://conceptnet.s3.amazonaws.com/downloads/2017/numberbatch/numberbatch-17.06.txt.gz
[nb1706-en]: https://conceptnet.s3.amazonaws.com/downloads/2017/numberbatch/numberbatch-en-17.06.txt.gz
[nb1706-mini]: http://conceptnet.s3.amazonaws.com/precomputed-data/2016/numberbatch/17.06/mini.h5

[nb1704-main]: https://conceptnet.s3.amazonaws.com/downloads/2017/numberbatch/numberbatch-17.04.txt.gz
[nb1704-en]: https://conceptnet.s3.amazonaws.com/downloads/2017/numberbatch/numberbatch-en-17.04b.txt.gz
[nb1704-mini]: http://conceptnet.s3.amazonaws.com/precomputed-data/2016/numberbatch/17.05/mini.h5

[nb1702-main]: http://conceptnet.s3.amazonaws.com/downloads/2017/numberbatch/numberbatch-17.02.txt.gz
[nb1702-en]: http://conceptnet.s3.amazonaws.com/downloads/2017/numberbatch/numberbatch-en-17.02.txt.gz

[nb1609-h5]: http://conceptnet.s3.amazonaws.com/precomputed-data/2016/numberbatch/16.09/numberbatch.h5


The .txt.gz files of term vectors are in the text format used by word2vec, GloVe, and fastText.

The first line of the file contains the dimensions of the matrix:

    1984681 300

Each line contains a term label followed by 300 floating-point numbers,
separated by spaces:

    /c/en/absolute_value -0.0847 -0.1316 -0.0800 -0.0708 -0.2514 -0.1687 -...
    /c/en/absolute_zero 0.0056 -0.0051 0.0332 -0.1525 -0.0955 -0.0902 0.07...
    /c/en/absoluteless 0.2740 0.0718 0.1548 0.1118 -0.1669 -0.0216 -0.0508...
    /c/en/absolutely 0.0065 -0.1813 0.0335 0.0991 -0.1123 0.0060 -0.0009 0...
    /c/en/absolutely_convergent 0.3752 0.1087 -0.1299 -0.0796 -0.2753 -0.1...

The HDF5 files are the format that ConceptNet uses internally. They are data
tables that can be loaded into Python using a library such as `pandas` or
`pytables`. The "mini.h5" files trade off a little bit of accuracy for a lot of
memory savings, taking up less than 150 MB in RAM, and are used to power the
[ConceptNet API](https://github.com/commonsense/conceptnet5/wiki/API).


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

> Robyn Speer, Joshua Chin, and Catherine Havasi (2017). "ConceptNet 5.5: An Open Multilingual Graph of General Knowledge." In proceedings of AAAI 2017.

In BibTeX form, the citation is:

    @paper{speer2017conceptnet,
        author = {Robyn Speer and Joshua Chin and Catherine Havasi},
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
    edited by Robyn Speer

  - [GloVe][glove], by Jeffrey Pennington, Richard Socher, and Christopher
    Manning

  - [word2vec][], by Tomas Mikolov and Google Research

  - Parallel text from [OpenSubtitles 2016][opensubtitles], by Pierre Lison
    and Jörg Tiedemann, analyzed using [fastText][], by Piotr Bojanowski,
    Edouard Grave, Armand Joulin, and Tomas Mikolov

[conceptnet]: http://conceptnet.io/
[glove]: http://nlp.stanford.edu/projects/glove/
[word2vec]: https://code.google.com/archive/p/word2vec/
[opensubtitles]: http://opus.lingfil.uu.se/OpenSubtitles2016.php
[fastText]: https://github.com/facebookresearch/fastText


## Language statistics

The multilingual data in ConceptNet Numberbatch represents 78 different language
codes, though some have vocabularies with much more coverage than others. The following
table lists the languages and their vocabulary size.

You may notice a focus on even the smaller and historical languages of Europe,
and under-representation of widely-spoken languages from outside Europe, which
is an effect of the availability of linguistic resources for these languages.
We would like to change this, but it requires finding good source data for
ConceptNet in these under-represented languages.

These vocabulary sizes were last updated for ConceptNet Numberbatch 17.02.

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

## Image credit

The otter logo was designed by [Christy
Presler](https://thenounproject.com/cnpresler/) for The Noun Project, and is
used under a Creative Commons Attribution license.
