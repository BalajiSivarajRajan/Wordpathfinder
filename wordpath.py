https://codereview.stackexchange.com/questions/107823/algorithm-to-transform-one-word-to-another-through-valid-words
import argparse, sys
from collections import defaultdict, namedtuple
from heapq import heappush, heappop

	#Return a word path - a list of words each of which differs from
	#the last by one letter by linking start and end, using the given
	#collection of words.


def readfile (filename):
	# to read the file and load to list
    try:
         with open (filename) as file:
             line = file.read()
             data = line.splitlines()
             return data
    except IOError:
         print "file not found: " +  filename
         sys.exit()
    except:
         print "unexpected error"
         sys.exit()

def word_ladder(words, start, end):
		#Identify the neighbourhood of each word. 
		#A* algorithm is used to path finding for the nodes
		#see https://en.wikipedia.org/wiki/A*_search_algorithm
		
    try:
		placeholder = object()
		matches = defaultdict(list)
		neighbours = defaultdict(list)
		for word in words:
			for i in range(len(word)):
				pattern = tuple(placeholder if i == j else for j, c in enumerate(word))
				m = matches[pattern]
				m.append(word)
				neighbours[word].append(m)

		# Admissible estimate of the steps to get from word to end.
		def h_score(word):
			return sum(a != b for a, b in zip(word, end))

		# Closed set: of words visited in the search.
		closed_set = set()

		# Open set: search nodes that have been found but not yet
		# processed. Accompanied by a min-heap of 4-tuples (f-score,
		# g-score, word, previous-node) so that we can efficiently find
		# the node with the smallest f-score.
		Node = namedtuple('Node', 'f g word previous')
		open_set = set([start])
		open_heap = [Node(h_score(start), 0, start, None)]
		while open_heap:
			node = heappop(open_heap)
			if node.word == end:
				result = []
				while node:
					result.append(node.word)
					node = node.previous
				return result[::-1]
			open_set.remove(node.word)
			closed_set.add(node.word)
			g = node.g + 1
			for neighbourhood in neighbours[node.word]:
				for w in neighbourhood:
					if w not in closed_set and w not in open_set:
						next_node = Node(h_score(w) + g, g, w, node)
						heappush(open_heap, next_node)
						open_set.add(w)

		return 'no possible path for the given input '
		
    except:
		print "error in path finder...."


def main():
    try:
		parser = argparse.ArgumentParser()
		parser.add_argument("-d", "--dict", required=True)
		parser.add_argument("-s", "--start", required=True)
		parser.add_argument("-e", "--end", required=True)
		args = vars(parser.parse_args())
		res = word_ladder (readfile (args['dict']), args['start'], args['end'] )
		print res
	except PathNotFound:
		print "No path found"
		sys.exit()
    except:
		print "unnexpected error ...."
		sys.exit()

if __name__ == '__main__':
    main()

