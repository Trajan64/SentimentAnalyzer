import nltk

class Tokenizer:
	
	def __init__(self):
		self.neg_words = [\
			"no", \
			"never", \
			"nothing", \
			"nowhere", \
			"noone", \
			"none", \
			"not", \
			"havent", \
			"hasnt", \
			"hadnt", \
			"cant", \
			"couldnt", \
			"shouldnt", \
			"wont", \
			"wouldnt", \
			"dont", \
			"didnt", \
			"isnt", \
			"arent", \
			"aint" \
			"n't" \
		 ]
		self.allowed_types = [ \
			"JJ",
			"JJR",
			"JJS",
			"NN",
			"NNS",
			"NNP",
			"NNPS",
			"FW",
			"VB",
			"VBD",
			"VBG",
			"VBN",
			"VBP",
			"RR",
			"RBR",
			"RBS"
		]
		 
		self.stoppers = ".,:;?!"
	
	
	def _split(self, tokens):
		
		splitted = [[]]
		row_id = 0
		
		for i in range(len(tokens)):
			splitted[row_id].append(tokens[i])
			if (tokens[i][-1:] in self.stoppers and i != len(tokens)-1):
				splitted.append([])
				row_id += 1
		
		return splitted
	

	
	def tokenize(self, text):
		
		# first: tokenize input
		words = nltk.word_tokenize(text)
		
		splitted = self._split(words)		
		
		negate_rest_sentence = False
		processed_words = []
		
		# for each of the tokens
		for j in range(len(splitted)):
			
			# get grammatical types of each of the tokens 
			tagged = nltk.pos_tag(splitted[j])
			negate_rest_sentence = False
			
			# for each tagged tokens
			for i in range(len(tagged)):
				
				# check if the current token is a negation operator
				if (tagged[i][0] in self.neg_words):
					
					# if so, indicate that every tokens from this point up to a clausal form
					# must be interpretated as 'negated'
					negate_rest_sentence = True
					continue
				
				# skip if the tag isn't part of the allowed types 
				if (tagged[i][1] not in self.allowed_types):
					continue
								
				# add a special property if 'negate_rest_sentence' is set to true
				if (negate_rest_sentence):
					processed_words.append((1, tagged[i][0]))
					continue
					
				processed_words.append((0, tagged[i][0]))
				
		return processed_words
		
