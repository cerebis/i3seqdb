//Updated on 26 Nov 19 by Kay Anantanawat

read_files = Channel.fromPath(params.run_table)
        .splitCsv(header: true, sep: ',', strip: true)
        .map{[it['sample_name'],  file(it['r1_filename']),
        file(it['r2_filename'])]}

process assembly{
        conda '/shared/homes/140837/miniconda3/envs/shovill'

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
            shovill -cpus 4 --outdir ${sample_name} --R1 ${r1} --R2 ${r2}
            cp ${sample_name}/contigs.fa ${sample_name}.contigs.fa
            cp ${sample_name}/contigs.gfa ${sample_name}.contigs.gfa
            cp ${sample_name}/shovill.log ${sample_name}.shovill.log
           else
            touch ${sample_name}.contigs.fa ${sample_name}.contigs.gfa ${sample_name}.shovill.log
           fi
        """
}
