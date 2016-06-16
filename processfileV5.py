import sys
import codecs
import re
# filename: processfileV5.py
#
# text-mines mpaa data file and builds a set of Movie objects
#
# Fifth iteration of file, used after analysis of early iteration results


# Movie class
class Movie:

	def __init__(self, called, when):
		self.name = called
		self.year = when
		self.reasons = []	# list of reasons
		self.lines = ''

	def rate(self, rated):
		self.rating = rated

	def addreason(self, reason):
		self.reasons.append(reason)

	def addline(self, line):
		self.lines = self.lines + line

# main procedure
def main():
	# for handling between loops
	activeobject = None
	# stores the Movie objects
	movies = []
	# all unique reason 'names' get stored with their frequencies
	reasons = {}
	# line count
	lcount = 0

	# initial object creation
	print('creating movie objects..')

	# open file
	with codecs.open('edited-reasons.list', "r", encoding='utf-8', errors='ignore') as fdata:
		for line in fdata:
			lcount += 1
			if line[0] == '-':
				# ignore because just separator
				continue

			if line[0] == 'M':
				string = line[3:].strip(' ')
				tokens = string.split('(')
				if len(tokens) > 3:
					print('error af')
				name = tokens[0]
				year_ = tokens[1]
				year = year_[0:4]
				# make new Movie object
				new = Movie(name,year)
				if activeobject is not None:
					movies.append(activeobject)
				activeobject = new

			if line[0] == 'R':
				if activeobject is None:
					print('Error: No Active Object')


				activeobject.addline(line[4:-1])

				tokens = line.split()
				if len(tokens) > 1 and tokens[1].upper() == 'RATED':
					# begins with Rated, must be followed with a rating
					rating = tokens[2]
					activeobject.rate(rating)

					'''
					for tok in tokens[4:]:
						token = tok.lower()
						# store token in object and in reasons dictionary
						if token not in reasons:
							reasons[token] = 1
						else:
							reasons[token] += 1
						activeobject.addreason(token)
					'''
				'''	
				else:
					for tok in tokens[1:]:
						token = tok.lower()
						# store token
						if token not in reasons:
							reasons[token] = 1
						else:
							reasons[token] += 1
						activeobject.addreason(token)
				'''

	print('done\nreading acjectives and nouns...')

	outv = open('validation_1984', 'w')
	outt = open('training_1984', 'w')
	afile = open('adj', 'r')
	nfile = open('noun','r')
	adjectives = []
	nouns = []
	for line in afile:
		adjectives.append(line.strip())
	for line in nfile:
		nouns.append(line.strip())

	l = []
	print('done\nReasoning...')

	for m_i in range(0,len(movies)):
		movie = movies[m_i]

		for i in range(0,len(movie.lines)):
			c = movie.lines[i]
			if c == '/':
				movie.lines = movie.lines[:i+1]+' '+movie.lines[i+1:]
		
		# remove stuff in parens
		movie.lines = a(movie.lines)

		tokens = movie.lines.split()

		active = ''						# this guy is where we hold a 'reason' in progress
		
		for i in range(3,len(tokens)):
			slash = False
			token = tokens[i].strip(',.')	
			if '/' in token:
				slash = True
				token = token[:len(token)-1]
			if '/' in token:
				print('Error: Unhandled Slash')

			if token.lower() in adjectives:
				active = active + token + ' '

			elif token.lower() in nouns:
				if slash:
					temp = active + token
					movie.addreason(temp)
				else:
					active = active + token
					movie.addreason(active)
					active = ''		# clear
			elif token.lower() != 'and':
				active = ''		# clear



	print('done\nCounting...')

	for movie in movies:
		for reason in movie.reasons:
			if reason in reasons:
				reasons[reason] += 1
			else:
				reasons[reason] = 1

	# dictionaries
	ars = {}
	thr = {}
	pgs = {}
	gen = {}
	nc7 = {}

	for movie in movies:
		r = movie.rating
		for reason in movie.reasons:
			if reason not in gen:
				gen[reason] = 0
				pgs[reason] = 0
				thr[reason] = 0
				ars[reason] = 0
				nc7[reason] = 0
				
			if r == 'G':
				gen[reason] += 1
			elif r == 'PG':
				pgs[reason] += 1

			elif r == 'PG-13':
				thr[reason] += 1

			elif r == 'R':
				ars[reason] += 1

			elif r == 'NC-17':
				nc7[reason] += 1
				


	print('done\nWriting...')

	#for reason in reasons:
		#line = reason+', ' +str(reasons[reason])+', ' 
		#+str(gen[reason])+', ' +str(pgs[reason])+', ' 
		#+str(thr[reason])+', ' +str(ars[reason])+', ' 
		#+str(nc7[reason])+'\n'

	pfile = open('phrases', 'r')

	phrases = []

	for line in pfile:
		phrases.append(line.strip())


	m_id = 1
	for movie in movies:
		try:
			nu = int(movie.year)
		except:
			continue
			 
		if nu < 1985:
			continue
		line = movie.rating
		for phrase in phrases:
			line = line + ','
			if phrase in movie.reasons:
				line = line + '1'
			else:
				line = line + '0'

		if m_id%2 == 0:	
			outv.write(line+'\n')
		else:
			outt.write(line+'\n')
	
		m_id += 1 	# increment


		'''
		out.write(movie.name + '\n')
		out.write(movie.year + ', ')
		out.write(movie.rating + '\n')
		out.write(movie.lines + '\n')
		out.write('\n   --- \n\n')
		'''	

	print('done\n')




# function from stackoverflow
# removes text within ANY parentheses 
def a(test_str):
    ret = ''
    skip1c = 0
    skip2c = 0
    for i in test_str:
        if i == '[':
            skip1c += 1
        elif i == '(':
            skip2c += 1
        elif i == ']' and skip1c > 0:
            skip1c -= 1
        elif i == ')'and skip2c > 0:
            skip2c -= 1
        elif skip1c == 0 and skip2c == 0:
            ret += i
    return ret


# n00b main call
main()