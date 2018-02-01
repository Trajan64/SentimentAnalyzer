import xml.dom.minidom as xml

import Tokenizer

# this class creates an XML structured corpus from the content of a .txt corpus file (containing sentiment related data).
class SentimentXMLCorpusBuilder:
	
	def __init__(self, corpus_filepath, XML_output):
		self.corpus = open(corpus_filepath, 'r')
		self.XML_output = open(XML_output, 'w')
		self.tokenizer = Tokenizer.Tokenizer()
		
	
	# retrieve the next comment inside corpus file.
	#
	# the sentiment corpus txt file is structured in a way so that each line contains a comment.
	# each one of those lines contains a character indicating the commment's general opinion (set by hand) as well as the comment's textual data
	def _retrieveNextComment(self):
		
		# retrieve line
		comment = self.corpus.readline()
		
		# check if we reached EOF
		if (comment == ""):
			return 0
						
		# the letter 'p' indicates a positive comment, the letter 'n' a negative one
		if (comment[0] == 'p'):
			opinion = 'positive'
		else:
			opinion = 'negative'
		
		# retrieve text data
		text = comment[2:]
		
		return (opinion, text)
				
				
	# creates the XML corpus file
	def buildXML(self):
		
		# create XML document
		document = xml.Document()
		
		# setup root node
		root = 	document.createElement("XML")
		
		# extract first comment
		comment = self._retrieveNextComment()
		
		# add root node to document
		document.appendChild(root)
		
		while (comment != 0):
			
			# add sub nodes
			XML_comment = document.createElement("comment")
			root.appendChild(XML_comment)
			XML_opinion = document.createElement("opinion")
			XML_original = document.createElement("original")
			XML_tokenized = document.createElement("tokenized")
			XML_comment.appendChild(XML_opinion)
			XML_comment.appendChild(XML_original)
			XML_comment.appendChild(XML_tokenized)
			XML_opinion.appendChild(document.createTextNode(comment[0]))
			XML_original.appendChild(document.createTextNode(comment[1]))
			
			# tokenize the extracted text data
			tokens = self.tokenizer.tokenize(comment[1])
			
			# for each of those tokens:
			for token in tokens:
				
				# create a new subnode tagged as 'token'
				XML_token = document.createElement("token")
				
				# give it an attribute indicating if the word was preceded by a negation 
				XML_token.setAttribute('negated', str(token[0]))
				
				# add raw comment text
				XML_token.appendChild(document.createTextNode(token[1]))
		
				XML_tokenized.appendChild(XML_token)
			
			# retrieve next comment
			comment = self._retrieveNextComment()
		
		# output XML data into a file
		document.writexml(self.XML_output,  indent ="   ", addindent="   ", newl='\n')
		
		document.unlink()
