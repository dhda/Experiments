#!/usr/bin/python
import sys

from bitstring import BitArray, ConstBitStream, ReadError
from heapq import heappush, heappop, heapify
from collections import defaultdict


# Algorithm details from http://rosettacode.org/wiki/Huffman_coding#Python
def huff_encode(text):
	freq = defaultdict(int)
	for s in text:
		freq[s] += 1

	tree = [ [f, [s, ""]] for s,f in freq.items() ]
	heapify(tree)

	while len(tree) > 1:
		l = heappop(tree)
		h = heappop(tree)
		
		for n in l[1:]:
			n[1] = '0' + n[1]
		for n in h[1:]:
			n[1] = '1' + n[1]

		heappush(tree, [l[0] + h[0]] + l[1:] + h[1:])

	root = heappop(tree)[1:]
	codes = dict([(s, "0b"+c) for s,c in root])
	
	# Header
	enc = BitArray()
	for s,c in root:
		enc += BitArray(bytes=s)
		enc += BitArray(uint=len(c), length=8)
		enc += BitArray("0b"+c)
	enc.prepend(BitArray(uint=len(root), length=8))
			
	for s in text:
		enc += BitArray(codes[s])

	return enc


def huff_decode(enc_file):
	enc = ConstBitStream(enc_file)
	
	tree = []

	tree_sz = enc.read("uint:8")
	while tree_sz > 0:
		s    = enc.read("bytes:1")
		c_sz = enc.read("uint:8")
		c    = BitArray(enc.read("bits:"+str(c_sz)))
		tree.append([s, c])
		tree_sz -= 1

	tree = sorted(tree, key = lambda v: v[1].len)
	
	text = ""
	while True:
		try:
			found = False
			for s,c in tree:
				if enc.startswith(c, enc.pos):
					print enc[enc.pos:].bin
					code = enc.read("bits:"+str(c.len))
					text += s
					found = True
					break
			if found == False:
				raise ReadError
		except ReadError:
			break
	
	return text


def main():
	if len(sys.argv) < 2:
		printUsage()
		sys.exit(1)

	enc_cmd = "encode"
	dec_cmd = "decode"
	cmd = sys.argv[1]

	if cmd.lower() == enc_cmd[0:len(cmd)]:
		if len(sys.argv) != 4:
			printUsage()
			sys.exit(1)

		with open(sys.argv[2], 'r') as f:
			text = f.read()
			enc = huff_encode(text)

		with open(sys.argv[3], 'wb') as f:
			enc.tofile(f)

	elif cmd.lower() == dec_cmd[0:len(cmd)]:
		if len(sys.argv) != 3:
			printUsage()
			sys.exit(1)

		with open(sys.argv[2], 'rb') as f:
			text = huff_decode(f)
			print text

	else:
		printUsage()


def printUsage():
	print "Usage: huffman encode <in file> <out file>"
	print "       huffman decode <in file>"


if __name__ == "__main__":
	main()
