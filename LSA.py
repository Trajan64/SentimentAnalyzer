from math import sqrt, log

class LSA:
	
	def __init__(self, n_documents):		
		
		self.positive_seed = ["good", 	"great", 	"amazing", 		"love"]
		self.negative_seed = ["bad", 	"horrible", "worst", 		"hate"]
		
		self.matrix = []
		self.n_rows = 0
		self.n_columns = 0
		
		self.n_documents = n_documents
		self.n_documents_words_counts = []
		
		self.positive_rows = []
		self.negative_rows = []
		
		self.vocabulary = {}
		
		self.scores = [] # this will contain the polarity scores
		
		self.vocabulary_size = 0
		
	
	def _applyTDIDF(self):
		
		for row in self.matrix:
			
			# compute the word's inverse document frequency
			idf = log( float(self.n_documents) / float(self.n_documents - row.count(0)) )
			
			for column_id in range(self.n_documents):
			
				# calculate term frequency
				tf = float(row[column_id]) / float(self.n_documents_words_counts[column_id])
				
				row[column_id] = tf * idf		
				
		
	
	def add(self, words):
		
		occurences = {}
		unique_words = []
		
		
		self.n_documents_words_counts.append( len(words) )
		
		# identify unique words
		for word in words:
			
			if word not in unique_words:
				unique_words.append(word)
				occurences[word] = 1
				
			else:
				occurences[word] += 1
		
		# get the word's occurences and add the value to the matrix
		for current_word in unique_words:
			
			# check if word is a new word:
			if current_word not in self.vocabulary:
				
				# setup new row
				new_row = [0] * self.n_documents
				
				new_row[self.n_columns] = occurences[current_word]
				
				self.vocabulary[current_word] = self.vocabulary_size
				
				self.matrix.append(new_row)	

				self.vocabulary_size += 1
			
			# else: word already has a row in the matrix
			else:
				
				self.matrix[self.vocabulary[current_word]][self.n_columns] = occurences[current_word]
				
		self.n_columns += 1
		
	
	
	# compute the polarity of all the words inside matrix
	def polarize(self):
				
		self.n_columns = self.vocabulary_size
		
		self._applyTDIDF()
		
		# find the rows inside matrix that are related to the seed words.
		self._identifySeedRows()
				
		# compute the polarity of all the words
		for word in self.vocabulary:
			
			# calculate semantic orientation
			SO = self._computeSemanticOrientation(self.matrix[self.vocabulary[word]], self.positive_rows, self.negative_rows)
			
			# if the word doesn't hold a neutral semantic orientation value:
			if (SO != 0.0):
				# add to the returned list a tupple containing the score as well as the word string
				self.scores.append((SO, word))
		
		# sort the list so that it will be ordered from negative to positive
		self.scores.sort()
	
	
	def _applyIF(self):
		for row in self.matrix:
			
			weight = log( float(self.n_columns) / float(self.n_columns - row.count(0)) )

			for i in range(self.n_columns):
				row[i] *= weight	
	
	
	# identify the words inside matrix that are part of a bag of words
	def _identifySeedRows(self):
		
		for word in self.vocabulary:
		
			if   (word in self.positive_seed):
				self.positive_rows.append(self.matrix[self.vocabulary[word]])
				
			elif (word in self.negative_seed):
				self.negative_rows.append(self.matrix[self.vocabulary[word]])

	
	
	
	# compute the semantic orientation of a given word.
	def _computeSemanticOrientation(self, word, positive, negative):	
				
		negativeSO = 0
		positiveSO = 0
				
		for vector in positive:
			positiveSO += self._cosim(word, vector)
		
		for vector in negative:
			negativeSO += self._cosim(word, vector)
		
		return positiveSO - negativeSO
	
	
	
	def _cosim(self, V1, V2):
				
		r1 = 0
		r2 = 0
		r3 = 0
		
		for i in range(len(V1)):
			r1 += V1[i] * V2[i]
			r2 += V1[i]**2
			r3 += V2[i]**2
				
		return float(r1) / float((sqrt(r2)*sqrt(r3)))
	
	
	
	# return the polarity score of every words inside lexicon
	def getPolarizedWords(self):
		return self.scores
	
	
	# return the polarity of the given word
	def getPolarity(self, word):
	
		for i in range(len(self.scores)):
			if (self.scores[i][1] == word):
				return self.scores[i][0]
		return 0
		
		
