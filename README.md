# Quick description #

This project implements a sentiment analyzer capable of automatically evaluating the emotional
polarities (good/bad) of a serie of comments, contained within a text file.

# Usage #

Once in the project directory, to interact with the sentiment analyzer, it is necessary to call
the python script `main.py`

## 1. Building the XML corpus. ##

Before doing anything related to sentiment analysis, we first need to build the XML corpus
from the text document file.

The python script `main.py` must then be called with the option `-buildXML`, just as
follow:

`python main.py -buildXML`

## 2. Sentiment analysis ##

After the creation of the XML corpus we then can get to the evaluation of the product
comments.

To do so, the python script `main.py` must be called followed by the option `-analyzeXML`.
Without providing any other options, the script is going to evaluate the emotional polarity of
each of the comments, and output the global level of accuracy of the results produced (the
number of correct guesses over the total count of comments).
It is however possible to provide other options (following the `-analyzeXML` option) in order
to observe some of the data produced by the sentiment analyzer:

• If we add the option `-top20`, the script will output the first twenty words holding the
highest good/bad scores:

Example:

`python main.py -analyzeXML -top20`

• The option -get-lexicon will output the entire scored lexicon built during the
unsupervised learning procedure.

Example:

`python main.py -analyzeXML -get-lexicon`

• The option `-get-infos` will output relative informations regarding a comment whose
id will have to be supplied as argument to the option.
The output of the command will display:
_ the comment's content.
_ the comment's computed emotional polarity score.
_ the comment's referential (hand-gathered) sentiment value.

Example:

`python main.py -analyzeXML -get-infos 2`

• Finally, the option -get-all-infos will do the same operation as the one stated
before. Except that here, the program will output informations regarding all the
comments inside the XML corpus.

Example:

`python main.py -analyzeXML -get-all-infos`
