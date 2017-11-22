#!/usr/bin/env python

## Script to pre-process ASAP dataset (training_set_rel3.tsv) based on the essay IDs

import argparse
import codecs
import sys
import os
import glob
import shutil

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input-file', dest='input_file', required=True, help='Input TSV file')
parser.add_argument('-p', '--prefix', dest='prefix', default='fold', help='folder prefix')
args = parser.parse_args()

def extract_based_on_ids(dataset, id_file):
	lines = []
	with open(id_file) as f:
		for line in f:
			id = line.strip()
			try:
				lines.append(dataset[id])
			except:
				print >> sys.stederr, 'ERROR: Invalid ID %s in %s' % (id, id_file)
	return lines

def create_dataset(lines, output_fname):
	f_write = open(output_fname, 'w')
	f_write.write(dataset['header'])
	for line in lines:
		f_write.write(line.decode('cp1252', 'replace').encode('utf-8'))

def collect_dataset(input_file):
	dataset = dict()
	lcount = 0
	with open(input_file) as f:
		for line in f:
			lcount += 1
			if lcount == 1:
				dataset['header'] = line
				continue
			parts = line.split('\t')
			assert len(parts) >= 6, 'ERROR: ' + line
			dataset[parts[0]] = line
	return dataset


if args.prefix != 'fold':
	for fold_idx in xrange(0, 5):
		fold = "fold_%d" % (fold_idx)
		outdir = "%s_%d" % (args.prefix,fold_idx)
		if not os.path.isdir(outdir):
			os.makedirs(outdir)
		textfiles = fold+"/*.txt"
		for file in glob.glob(textfiles):
		    shutil.copy(file, outdir)

dataset = collect_dataset(args.input_file)

for fold_idx in xrange(0, 5):
	for dataset_type in ['dev', 'test', 'train']:
		lines = extract_based_on_ids(dataset, '%s_%d/%s_ids.txt' % (args.prefix, fold_idx, dataset_type))
		create_dataset(lines, '%s_%d/%s.tsv' % (args.prefix,fold_idx, dataset_type))