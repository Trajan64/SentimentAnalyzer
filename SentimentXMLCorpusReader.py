import xml.etree.ElementTree as ET

# this class provides different methods to extract sentiment related data from an XML corpus file (following a certain format).
class SentimentXMLCorpusReader:

	def __init__(self, sentiment_xml_filepath):
	
		self.tree = ET.parse(sentiment_xml_filepath)
		self.root = self.tree.getroot()
		self.current_comment_id = 0
		self.n_comments = len(self.root)
		
	# move pointer to the next comment
	# return 1 if operation successfull; 0 otherwise (no succeeding comments left to parse)
	def moveToNextComment(self):
	
		if ((self.current_comment_id+1) < self.n_comments):
		
			# increase comment pointer
			self.current_comment_id += 1
			return 1
		
		return 0
	
	# move pointer to the given comment
	# return 1 if operation successfull; 0 otherwise (comment indice is out of range)
	def moveToComment(self, comment_id):
		
		# set given index as comment pointer if it doesn't go beyond the total number of comments 
		if (comment_id < self.n_comments):
			self.current_comment_id = comment_id
			return 1

		return 0

	# get the value inside the 'opinion' node at current comment level
	def getCurrentCommentOpinion(self):
		
		if (self.root[self.current_comment_id][0].text.strip() == 'negative'):
			return -1
		return 1
	
	# get the value inside the 'original' node at current comment level
	def getCurrentCommentOriginalText(self):
		
		return self.root[self.current_comment_id][1].text.strip()
	
	# get all the tokens inside the 'tokens' node at current comment level
	# each of the token will be sent as a tuple containing both an attribute dictionary and a word string
	def getCurrentCommentTokens(self):
	
		tokens = []
			
		# points toward the tokenized node
		tokenized = self.root[self.current_comment_id][2]
		
		
		for i in range(len(tokenized)):
		
			# this dictionary will contain the different word attributes.
			attributes = {}
			
			# add 'negated' key-value in dictionary
			attributes['negated'] = int(tokenized[i].attrib['negated'])
			
			word = tokenized[i].text.strip()
			
			tokens.append( (attributes, word) )
			
		return tokens
	
	
	# get the total number of comments inside XML corpus
	def getNumberOfComments(self):
		return self.n_comments