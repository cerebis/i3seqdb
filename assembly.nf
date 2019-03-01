#!/usr/bin/env nextflow


params.out_dir = 'out'


/**
 * Get the read sets to assemble from a CSV run_table
 **/
read_files = Channel.fromPath(params.run_table)
    .splitCsv(header: true, sep: ',', strip: true)
    .map{[it['sample_name'],  file(it['r1_filename']),
          file(it['r2_filename'])]}


process assemble {
   conda 'bioconda::shovill samtools=1.8'
  //***** On March 1, 2019, shovill has problems reading the samtools that coming with it.**/
  //*** So, samtools 1.8 is used instead **/
  
   cpus 5
   memory '30 GB'
   publishDir params.out_dir, mode: 'copy'

   input:
   set sample_name, r1, r2 from read_files

   output:
   file("${sample_name}.contigs.fa")
   file("${sample_name}.contigs.gfa")
   file("${sample_name}.shovill.log") into shovill_log_ch

   script:
   """
   //**On March 1, 2019, the script will not work if the file doesn't exist. **/
   //** Fix this by removing the samples from the run_table. **/
  
   filesize=\$(stat -c%s "${r1}")
   if(( filesize > 5000000 )); then
	   shovill --cpus 4 --outdir `pwd`/asm --R1 ${r1} --R2 ${r2} --trim
	   cp asm/contigs.fa ${sample_name}.contigs.fa
	   cp asm/contigs.gfa ${sample_name}.contigs.gfa
	   cp asm/shovill.log ${sample_name}.shovill.log
   else
	   touch ${sample_name}.contigs.fa ${sample_name}.contigs.gfa ${sample_name}.shovill.log
   fi
   """
}

/**grabbing the information from shovill_log**/

process grab_info{

	input:
	file shovill_log from shovill_log_ch

	output:
	stdout result

	"""
	#!/usr/bin/env python

	import ntpath
	import sys
	import os

	genome_size=5000000

	input_file="$shovill_log"
	filename=ntpath.basename(input_file)
	sample_name, type, tail=filename.split(".")
	with open(input_file,'r') as f:
		lines = f.readlines()
		for i in range(0,len(lines)):
			line=lines[i]
			if 'It contains' in line:
				num_contigs=int(line.split()[3])
			if 'Assembly is' in line:
				assembly_size=[int(s) for s in line.split() if s.isdigit()][0]
			if 'Input Read Pairs' in line:
				raw_reads=int(line.split()[4])
			if 'Read stats: total_bp =' in line:
				raw_nt=int(line.split()[5])
			if 'Finish error correction' in line:
				next_line=lines[i+1]
				EC_reads=int(next_line.split()[2])
				percentage_reads_EC=float(EC_reads/raw_reads)
			if 'This is shovill' in line:
				version=line.split()[4]
	percentage_reads_EC=float(EC_reads)/(raw_reads*2)*100
	coverage=percentage_reads_EC*(assembly_size/raw_nt)
	print(sample_name,num_contigs, assembly_size, raw_nt, raw_reads, EC_reads, "%.2f" %percentage_reads_EC, version)
	"""
}

/*** KA: I want to put the data from the grab_info into one file.
*But I don't know how.
**/

result.subscribe{
	println "sample_name,num_contigs, assembly_size, raw_nt, raw_reads, EC_reads, percentage_reads_EC, version"
	println it.trim()
}
