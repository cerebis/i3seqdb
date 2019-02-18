#!/bin/env python

import re
import ntpath
import sys
import os

###input_file='/shared/homes/140837/ref/W_assembly/W_1_B11.shovill.log'

input_directory=sys.argv[1]

dict={}
genome_size=5000000

##dict has the sample_name as key.
##dict[key][0]=number of raw bases
##dict[key][1]=coverage
##dict[key][2]=number of > from fasta file
##dict[key][3]=nt used
print
print("sample_name", "raw_nt", "coverage", "contigs", "nt_used", "estimated_coverage", "corrected_coveraged")


for file in os.listdir(input_directory):
	filename=ntpath.basename(file)
	fullpath=os.path.join(input_directory,file)
	sample_name, type, tail=filename.split(".")
	if sample_name in dict:
		pass
	else:
		dict[sample_name]=[0,1,2,3,4,5]
	if type=='shovill':
		with open(fullpath, 'r') as f:
			#print f
			for line in f.readlines():
				#print line
				if 'Read stats: total_bp =' in line:
					#print(line)
					raw_nt=int(line.split()[5])
#                                       print raw_nt
					coverage=int(raw_nt/genome_size)
					dict[sample_name][0]=raw_nt
					dict[sample_name][1]=coverage
				if 'Estimated sequencing depth:' in line:
#                                       print line
					estimated_coverage=line.split()[4]
					dict[sample_name][4]=estimated_coverage
				if 'Both Surviving:' in line:
#                                       print line
					percentage_read_used=[float(s) for s in re.findall(r'-?\d+\.?\d*',line)][2]
#                                       print percentage_read_used
					nt_used=int(percentage_read_used*raw_nt/100)
					dict[sample_name][3]=nt_used
					dict[sample_name][5]=int((dict[sample_name][1]*percentage_read_used/100))
				if 'It contains' in line:
#                                       print line
					contigs=[int(s) for s in re.findall(r'-?\d+\.?\d*',line)][0]
					dict[sample_name][2]=contigs

for key, value in dict.items():
	print(key, value[0],value[1],value[2],value[3],value[4],value[5])
print

##############################################################################
##############################################################################
##############################################################################
#The columns of the assembly stats file must be as follows:
#
#Contigs             // Number of contigs generated
#Scaffolds           // Number of scaffolds generated
#Assembly size       // Sum of lengths of all scaffolds in assembly; if no scaffolds, sum of all contigs
#Longest Scaffold    // Length of the longest scaffold, if no scaffolds, longest contigs
#N50                 // N50 value for the scaffolds (N50 length is defined as the length for which
#                    //    the collection of all scaffolds of that length or longer contains at
#                    //    least half of the total of the lengths of the scaffolds)
#Raw reads           // Number of raw reads used as input
#EC reads            // Number of reads used for assembly, after quality control and error correction
#% reads passing EC  // Percentage of the raw reads that the EC reads represent
#Raw nt              // Number of nucleotides used as input
#EC nt               // Number of nucleotides after quality control and error correction
#% nt passing EC     // Percentage of the raw nucleotides that the EC nucleotides represent
#Raw cov             // Average depth of sequence coverage provided by the raw data
#Median cov          // Median actual depth of coverage in the assembly
#10th percentile cov // 10th percentile depth of coverage -- 90% of sites have greater coverage
#bases >= Q40        // Number of bases that have a PHRED-scale quality greater or equal to Q40
#Assembler version   // Version used to run the assembly.
###############################################################################
##############################################################################
##############################################################################
##############################################################################
