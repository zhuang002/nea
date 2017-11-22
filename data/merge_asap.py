import argparse
import codecs
import sys

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input-file', dest='input_file', required=True, help='Input TSV file')
parser.add_argument('-o', '--output-file', dest='output_file', required=True, help='Output TSV file')
parser.add_argument('-m', '--merge-essayset', dest='merge',default='(3,4)', help='Output TSV file')
args = parser.parse_args()	

merges=args.merge[1:-1].split(',')
print("merges=%s" % (merges))
outlines = []
with open(args.input_file) as fi:
	for line in fi:
		parts = line.split('\t')
		if parts[1] in merges:
			parts[1] = merges[0]
		outlines.append('\t'.join(parts))
with open(args.output_file,'w') as fo:
	for line in outlines:
		fo.write(line.decode('cp1252', 'replace').encode('utf-8'))

