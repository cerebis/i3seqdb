//Analysing Bondi data
//Updated on 27 Nov 19 by Kay Anantanawat

params.out_dir='Nov19_BB'

Channel.fromPath('/shared/homes/140837/ref/illumina_adapter.fa')
	.set{adaptersChannel}

read_files = Channel.fromPath(params.run_table)
	.splitCsv(header: true, sep: ',', strip: true)
	.map{[it['sample_name'],  file(it['r1_filename']),
	file(it['r2_filename'])]}

process trimmomatic{
	container 'quay.io/biocontainers/trimmomatic:0.35--6'
	errorStrategy 'ignore'
        time '30m'
        cpus 5
	memory '30 GB'
		

	input:
        file(adapters) from adaptersChannel
	set sample_name, r1, r2 from read_files

        output:
        set val(sample_name), file('R1.paired.fastq.gz'), file('R2.paired.fastq.gz') into trimmedReadsChannel

	script:

	if((new java.io.File(r1.toString())).length()>5000000){

	"""
	trimmomatic PE -phred33 ${r1} ${r2}\
		R1.paired.fastq.gz \
		R1.unpaired.fastq.gz \
		R2.paired.fastq.gz \
		R2.unpaired.fastq.gz \
		ILLUMINACLIP:${adapters}:2:30:10 \
		LEADING:3 \
		TRAILING:3 \
		SLIDINGWINDOW:4:15 \
		MINLEN:37

	"""

	}else{

	"""
	touch R1.paired.fastq.gz R2.paired.fastq.gz
	"""
	}

}



process assembly{
	container 'quay.io/biocontainers/unicycler:0.4.4--py37h8b12597_2'
	publishDir params.out_dir, mode:'copy'
	errorStrategy 'ignore'
	time '30m'
	cpus 5
	memory '30 GB'
	
	input:	
	set sample, r1, r2 from trimmedReadsChannel

        output:
        file("${sample}.assembly.fasta")

        script:
	if((new java.io.File(r1.toString())).length()>5000000){
        """
	unicycler -1 ${r1} -2 ${r2} -o ${sample}
        cp ${sample}/assembly.fasta ${sample}.assembly.fasta
	cp ${sample}/assembly.gfa ${sample}.assembly.gfa
	cp ${sample}/unicycler.log ${sample}.unicycler.log
	"""
	}else{
	"""
	touch ${sample}.assembly.fasta ${sample}.assembly.gfa ${sample}.unicycler.log
        """       
	}
}


