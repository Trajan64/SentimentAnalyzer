#!/usr/bin/python2

import LSA
import SentimentAnalyzer
import SentimentXMLCorpusBuilder


import sys
from random import random

# options:
#	-top20
#	-get-infos <commend id>
#	-get-all-infos
#	-get-lexicon

#default: print accuarcy


def displayCommentInformations(comment_id):
	informations = sentiment_analyser.getCommentInformations(comment_id)
	
	if (informations['handgathered_opinion'] < 0):
		handgathered_opinion_string = "negative"
	else:
		handgathered_opinion_string = "positive"
	
	print '%i.' % (comment_id)
	print 'handgathered opinion: \t%s' % (handgathered_opinion_string)
	print 'original text: \t\t%s' % (informations['original_text'])
	print 'comment polarity: \t%4.2f' % (informations['polarity']),
	if (informations['polarity'] < 0):
		print '(negative)'
	else:
		print '(positive)'
	print '-'*32


	
def displayUsage():

	print 'usage: python main.py -buildXML'
	print '                      -analyzeXML'
	print '                      -analyzeXML -top20'
	print '                      -analyzeXML -get-infos <comment id>'
	print '                      -analyzeXML -get-all-infos'
	print '                      -analyzeXML -get-lexicon'

	
	
argv = sys.argv
argc = len(sys.argv)

print '-'*32

if (argc < 2):
	
	displayUsage()
	exit(0)

if (argv[1] == '-buildXML'):

	XML_corpus_builder = SentimentXMLCorpusBuilder.SentimentXMLCorpusBuilder("comments.txt", "structurizedCorpus.xml")
	
	print 'building XML corpus...'
	XML_corpus_builder.buildXML()
	print 'XML corpus built'
	
	exit(0)

if (argv[1] == '-analyzeXML'):
	
	# check if XMLcorpus is inside current directory	
	
	
	# setup sentiment analyzer
	sentiment_analyser = SentimentAnalyzer.SentimentAnalyzer("structurizedCorpus.xml")
	print "building lexicon.."
	sentiment_analyser.buildLexicon()
	print "computing semantic orientation scores.."
	sentiment_analyser.polarizeLexicon()
	
	

	if (argc < 3):
		
		# no options provided: evaluate comments and display statistics
		
		print "evaluating comments.."
		sentiment_analyser.evaluateAllComments()

		print 'accuarcy: %4.2f' % (sentiment_analyser.getAccuarcy() * 100) + str('%') 
		print 'correct guesses: %i' % (sentiment_analyser.getCorrectGuesses())
		print 'total number of comments: %i' % (sentiment_analyser.getNumberOfComments())
		exit(0)

	else:
		if (argv[2] == '-top20'):
			
			# display the 20 best negative and positive words
			
			range_value = 20
			
			polarized_words = sentiment_analyser.getPolarizedWords()
			print 'best positive words:\n'
			for i in range(range_value):
				print '\t %4.2f - %s' % (polarized_words[-i-1][0], polarized_words[-i-1][1])
			print ''
			print 'best negative words:\n'
			for i in range(range_value):
				print '\t%4.2f - %s' % (polarized_words[i][0], polarized_words[i][1])
				
			exit(0)
				
		if (argv[2] == '-get-lexicon'):
			
			# print the entire lexicon
			
			polarized_words = sentiment_analyser.getPolarizedWords()
			
			print 'displaying polarized values for each of the words inside XML corpus:'
			
			for i in range(len(polarized_words)):
				print '\t %4.2f - %s' % (polarized_words[i][0], polarized_words[i][1])
		
			exit(0)

		print "evaluating comments.."
		sentiment_analyser.evaluateAllComments()			

		if (argv[2] == '-get-all-infos'):
			
			# get the informations of all the comments
			
			for i in range(sentiment_analyser.getNumberOfComments()):
				displayCommentInformations(i)
			
			exit(0)
				
		if (argv[2] == '-get-infos'):
			
			n_comments = sentiment_analyser.getNumberOfComments()
			
			if (argc < 3):
				
				# no argument was provided to the option: use a randomly generated comment id
				print 'using a randomly generated comment id..'
				comment_id = int(random() * n_comments)
				
			else:
				try:
					comment_id = int(argv[3])
				except:
					print 'error: argument is not an integer'
					exit(1)
				
			if (comment_id >= n_comments):
				print 'error: provided comment id is out of range'
				
			displayCommentInformations(comment_id)
		
			exit(0)
			
		else:
		
			# unrecognized option
			
			displayUsage()
			exit(0)
			
			
# no arguments were provided: display usage
displayUsage()