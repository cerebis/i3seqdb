#!/usr/bin/env nextflow


params.out_dir = 'out'


/**
 * Get the read sets to assemble from a CSV run_table
 **/
read_files = Channel.fromPath(params.run_table)
    .splitCsv(header: true, sep: '\t', strip: true)
    .map{[it['sample_name'],  file(it['r1_filename']),
          file(it['r2_filename'])]}


process assemble {
   cpus 5
   memory '30 GB'
   publishDir params.out_dir, mode: 'copy'

   input:
   set sample_name, r1, r2 from read_files

   output:
   file("${sample_name}.contigs.fa")
   file("${sample_name}.contigs.gfa")
   file("${sample_name}.shovill.log")

   script:
   """
   filesize=\$(stat -c%s "${r1}")
   if(( filesize > 5000000 )); then
	   shovill --cpus 4 --outdir `pwd`/asm --R1 ${r1} --R2 ${r2} --trim
	   cp asm/contigs.fa ${sample_name}.contigs.fa
	   cp asm/contigs.gfa ${sample_name}.contigs.gfa
	   cp asm/00-shovill.log ${sample_name}.shovill.log
   else
	   touch ${sample_name}.contigs.fa ${sample_name}.contigs.gfa ${sample_name}.shovill.log
   fi
   """
}
