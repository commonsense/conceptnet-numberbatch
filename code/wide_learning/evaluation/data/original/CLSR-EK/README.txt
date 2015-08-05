
			Cross-Lingual Evaluation Dataset
			   ==========================
			   	   Version 1.0
				  June 7th, 2009

			    Rada Mihalcea, Samer Hassan
			Language and Information Technologies
				University of North Texas

				  rada@cs.unt.edu
				   samer@unt.edu


CONTENTS
1. Introduction
2. Data Set
3. Annotation Guidelines
4. Format
5. Feedback
6. References
7. Citation Info

=======================
1. Introduction

This README v1.0 (June, 2009) for the cross-lingual evaluation dataset
comes from the archive hosted at the following URL
http://lit.csci.unt.edu/index.php/Downloads

======================= 
2. Data Set

The dataset builds over Miller-Charles (Miller and Charles, 1998) and
WordSimilarity-353 (Finkelstein et al., 2001) English word relatedness
datasets by providing the corresponding translations in Arabic, Spanish,
and Romanian.

The Miller-Charles dataset (Miller and Charles, 1998) consists of 30-word
pairs ranging from synonymy pairs (e.g., car - automobile) to completely
unrelated terms (e.g., noon - string). The relatedness of each word pair
was rated by 38 human subjects, using a scale from 0 (not-related) to 4
(perfect synonymy). The dataset is available only in English and has been
widely used in previous semantic relatedness evaluations (e.g., Resnik,
1995;  Hughes and Ramage, 2007; Zesch et al., 2008).

The WordSimilarity-353 dataset (also known as Finkelstein-353)
(Finkelstein et al., 2001)  consists of 353 word pairs annotated by 13
human experts, on a scale from 0 (unrelated) to 10 (very closely related
or identical).  The Miller-Charles set is a subset in the
WordSimilarity-353 data set. Unlike the Miller-Charles data set, which
consists only of single words, the WordSimilarity-353 set also features
phrases (e.g., "Wednesday news"), therefore creating an additional degree
of difficulty for a relatedness metric applied on this data set.

=======================
3. Annotation Guidelines

Native speakers of Spanish, Romanian and Arabic, who were also highly
proficient in English, were asked to translate the words in the two data
sets. The annotators were provided one word pair at a time, and asked to
provide the appropriate translation for each word while taking into
account their relatedness within the word pair. The relatedness was meant
as a hint to disambiguate the words, when multiple translations were
possible. The annotators were also instructed not to use multi-word
expressions in their translations. They were also allowed to use
replacement words to overcome slang or culturally-biased terms.

To test the ability of the bilingual judges to provide correct
translations by using this annotation setting, we carried out the
following experiment.  We collected Spanish translations from five
different human judges, which were then merged into a single selection
based on the annotators' translation agreement; the merge was done by a
sixth human judge, who also played the role of adjudicator when no
agreement was reached between the initial annotators. Subsequently, five
additional human experts rescored the word-pair Spanish translations by
using the same scale that was used in the construction of the English data
set. The correlation between the relatedness scores assigned during this
experiment and the scores assigned in the original English experiment was
0.86, indicating that the translations provided by the bilingual judges
were correct and preserved the word relatedness. For the translations
provided by the five human judges, in more than 74% of the cases at least
three human judges agreed on the same translation for a word pair. When
the judges did not provide identical translations, they typically used a
close synonym. The high agreement between their translations indicates
that the annotation setting was effective in pinpointing the correct
translation for each word, even in the case of ambiguous words.

=======================
4. Format

Each dataset has a corresponding comma separated Unicode (UTF8) where the
first line is a header indicating the column name in the form
"EN.1";"EN.2";"RO.1";"RO.2";"AR.1";"AR.2";"ES.1";"ES.2";"score"

a) "EN.1";"EN.2": represents the original English word-pair

b) "RO.1";"RO.2";"AR.1";"AR.2";"ES.1";"ES.2": represents the corresponding
translations in Romanian, Arabic, and Spanish respectively (where RO.1
corresponds to EN.1, RO.2 corresponds to EN.2, etc. )

c) "Score": is the original relatedness score reported in the English
dataset.


=======================
5. Feedback

For further questions or inquiries about this data set, you can contact:
Samer Hassan (samer@unt.edu) or Rada Mihalcea (rada@cs.unt.edu).


=======================
6. References

(Finkelstein et al., 2001)  L. Finkelstein, E. Gabrilovich, Y. Matias, E.
Rivlin, Z. Solan, G. Wolfman, and E. Ruppin. 2001. Placing search in
context: the concept revisited. In Proceedings of the Conference on the
World Wide Web, pages 406-414.

(Hughes and Ramage, 2007) T. Hughes and D. Ramage. 2007. Lexical semantic
knowledge with random graph walks. In Proceedings of the Conference on
Empirical Methods in Natural Language Processing, Prague, Czech Republic.

(Miller and Charles 1998) G. Miller and W. Charles. 1998. Contextual
correlates of semantic similarity. Language and Cognitive Processes, 6(1).

(Resnik 1995) Resnik. 1995. Using information content to evaluate semantic
similarity. In Proceedings of the 14th International Joint Conference on
Artificial Intelligence, Montreal, Canada.

(Zesch et al., 2008) T. Zesch, C. M"uller, and I. Gurevych. 2008. Using
Wiktionary for Computing Semantic Relatedness. In Proceedings of the
American Association for Artificial Intelligence, Chicago.



=======================
7. Citation Info 

If you use this data set, please cite:

@InProceedings{Hassan09a,
  author =   	   {Samer Hassan, Rada Mihalcea},
  title = {Cross-lingual Semantic Relatedness Using Encyclopedic
           Knowledge},
  booktitle =    {Proceedings of the conference on Empirical Methods in 
           Natural Language Processing}, 
  address =      {Singapore},
  year =         {2009}
}

