import LSA
import SentimentXMLCorpusReader

class SentimentAnalyzer:

	def __init__(self, sentiment_xml_filepath):
		self.xml_reader = SentimentXMLCorpusReader.SentimentXMLCorpusReader(sentiment_xml_filepath)
		self.n_comments = self.xml_reader.getNumberOfComments()
		self.vsm = LSA.LSA(self.n_comments)
		self.evaluated_comments_value = []
		self.correct_evaluations = 0

	
	# insert all the tokens found inside the XML file into the VSM matrix
	def buildLexicon(self):
		
		if (not self.n_comments):
			return 0
		
		continuing = True
		while (continuing):
		
			words_current_comment = []
			
			# acquires tokens
			tokens = self.xml_reader.getCurrentCommentTokens()
			
			# process tokens
			words_current_comment = self._convertToFormatedWords(tokens)
			
			# feed them to the lexicon builder
			self.vsm.add(words_current_comment)
			
			# get to the next comment
			continuing = self.xml_reader.moveToNextComment()
				
		return 1
				
	
	# get the total number of comments
	def getNumberOfComments(self):
		return self.n_comments
	
	
	# convert tokens (tuple containing a list of attributes and a word) into single words
	def _convertToFormatedWords(self, tokens):
	
		words = []
		for token in tokens:
			if (token[0]['negated'] == 1):
					# negated tokens will be presented as words with '_neg' as suffix
					words.append(token[1] + '_neg')
			else:
					words.append(token[1])
					
		return words
		
	
	# set emotional polarity scores for each of the words inside LSA's lexicon.
	def polarizeLexicon(self):
		self.vsm.polarize()
		
		
	# compute the opinions of every comments inside the XML corpus.
	def evaluateAllComments(self):
			
		if (not self.n_comments):
			return
			
		# move file cursor at the beginning of the file.
		self.xml_reader.moveToComment(0)
		
		
		continuing = True
		while (continuing):
		
			words_current_comment = []
			
			# acquires tokens
			tokens = self.xml_reader.getCurrentCommentTokens()
			
			# process tokens
			words_current_comment = self._convertToFormatedWords(tokens)
			
			# this will hold the comment (computed) overall opinion. 
			polarity = 0.0
			
			# calculate average polarity 
			for word in words_current_comment:
				polarity += self.vsm.getPolarity(word)		
			if (polarity != 0.0):
				polarity = float(polarity) / float(len(words_current_comment))
				
			self.evaluated_comments_value.append(polarity)
			
			# check if the computed polarity is correct
			hand_gathered_opinion = self.xml_reader.getCurrentCommentOpinion()
			if (hand_gathered_opinion < 0 and polarity < 0) or (hand_gathered_opinion > 0 and polarity > 0):
				self.correct_evaluations += 1
			
			# set reader pointer to next comment
			continuing = self.xml_reader.moveToNextComment()		
	
	
	# return the ratio of the number of correct guesses (done by the sentiment analyser parser) to the total number of comments
	def getAccuarcy(self):
		
		return float(self.correct_evaluations) / float(self.n_comments)
	
	
	# retrieve all words with their polarization values (sorted from low to high)
	def getPolarizedWords(self):
		
		polarized_words = self.vsm.getPolarizedWords()
		
		# sort from low to high
		polarized_words.sort()
		
		return polarized_words
		
	
	# return all the informations about the given comment.
	# this includes the XML comment data as well as the overall polarized value.
	def getCommentInformations(self, comment_id):
		
		self.xml_reader.moveToComment(comment_id)
		
		informations = {}
		
		informations['handgathered_opinion'] = self.xml_reader.getCurrentCommentOpinion()
		informations['original_text'] = self.xml_reader.getCurrentCommentOriginalText()
		informations['polarity'] = self.evaluated_comments_value[comment_id]
		
		return informations
		
	# return the number of comments for which the computed opinions matched the handgathered ones
	def getCorrectGuesses(self):
		
		return self.correct_evaluations
