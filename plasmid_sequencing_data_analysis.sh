#!/bin/bash

# Author: Kay Anantanawat

##################
# Set PBS Commands 
# PBS commands must come at the top of this script, before any other commands.
#################

# Set the resource requirements; 1 CPU, 5 GB memory and 5 minutes wall time.
#PBS -N plasmid_variant_calling
#PBS -l ncpus=2
#PBS -l mem=10GB
#PBS -l walltime=2:00:00

# There are several queues e.g. workq, smallq and others
#PBS -q workq

# Send email on abort, begin and end. 
# CHANGE 999777 to your staff or student number!
#PBS -m abe 
#PBS -M 140837@uts.edu.au

###################################
# What does this workflow do?
# This workflow is needed when Bondi Biowork given us a sequence of the template they try to sequence, and want to see the alignment. Therefore, we do the aligner. 
##1. Trim the adapters using trimmomatics
###################################



###################################
# Setup any input files for the run
###################################
#GENERAL
PROJECT_NAME="Apr21_OO_T"
DATA="/shared/homes/s1/NGS_data/data_2021/Apr21_OO_T"
TAB="/shared/homes/s1/NGS_data/data_2021/Apr21_OO_T/bondi_unicycler.tab"

## unicycler
FASTQ="/shared/homes/s1/NGS_data/data_2021/Apr21_OO_T/fastq"
ADAPTER="/shared/homes/140837/ref/illumina_adapter.fa"
TRIM="/shared/homes/s1/NGS_data/data_2021/Apr21_OO_T/trim"
ASS="/shared/homes/s1/NGS_data/data_2021/Apr21_OO_T/assembly"

## snippy 
REF="/shared/homes/s1/NGS_data/data_2021/Apr21_OO_T/ref"

##Final folder for sending to people
MASTER="/shared/homes/s1/NGS_data/data_2021/Apr21_OO_T/Apr21_OO_T/"
DEN="/shared/homes/s1/NGS_data/data_2021/Apr21_OO_T/Apr21_OO_T/de_novo_assembly"
VAR="/shared/homes/s1/NGS_data/data_2021/Apr21_OO_T/Apr21_OO_T/variant_calling"
CORRECT_NAME="/shared/homes/s1/NGS_data/data_2021/Apr21_OO_T/Apr21_OO_T/fastq"

############3
# Start the Job
###############

cd ${DATA}

source activate unicycler

mkdir ${TRIM}
mkdir ${ASS}
mkdir ${MASTER}
mkdir ${DEN}

mkdir ${VAR}
mkdir ${CORRECT_NAME}

##Read tab files

while read sample_name reference R1 R2
do
        [ "$sample_name" == "sample_name" ] && continue
### unicycler ###
	trimmomatic PE -phred33 ${FASTQ}/$R1 ${FASTQ}/$R2 ${TRIM}/$sample_name.R1_pair.fastq.gz ${TRIM}/$sample_name.R1_unpair.fastq.gz ${TRIM}/$sample_name.R2_pair.fastq.gz ${TRIM}/$sample_name.R2_unpair.fastq.gz ILLUMINACLIP:${ADAPTER}:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36
	unicycler -1 ${TRIM}/$sample_name.R1_pair.fastq.gz -2 ${TRIM}/$sample_name.R2_pair.fastq.gz -o ${ASS}/$sample_name
        cp ${ASS}/$sample_name/assembly.fasta ${DEN}/$sample_name.assembly.fasta
        cp ${ASS}/$sample_name/assembly.gfa ${DEN}/$sample_name.assembly.gfa
        cp ${FASTQ}/$R1 ${CORRECT_NAME}/$sample_name.R1.fastq.gz
        cp ${FASTQ}/$R2 ${CORRECT_NAME}/$sample_name.R2.fastq.gz
### Snippy ###
	singularity exec ~/software1/snippy.sif snippy --outdir $sample_name --ref ${REF}/$reference --R1 ${FASTQ}/$R1 --R2 ${FASTQ}/$R2
	cp $sample_name/snps.consensus.fa  $sample_name.snps.consensus.fa
	cp $sample_name/snps.tab  $sample_name.snps.tab

done < ${TAB}

for i in *snps.tab; do echo sample_name: "$i"; cat "$i";echo; done |cut -f 1,2,3,4,5,6 |sed 's/.snps.tab//g'| sed 's/CHROM/Chromosome/g' |sed 's/POS/Position/g' | sed 's/TYPE/Type/g'|sed 's/REF/Reference allele/g'|sed 's/ALT/Alternative allele/g'|sed 's/EVIDENCE/# Reads observed for each allele/g' >> summary_snps_in_all_sample.txt

mv *.snps.* ${VAR}

mv summary_snps_in_all_sample.txt ${VAR}

cp -r ${TRIM} ${MASTER}/

tar -zcvf ${PROJECT_NAME}.tar.gz ${MASTER}
