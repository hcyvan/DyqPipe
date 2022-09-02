workflow DyqPipe {
    String title
    String description
    String genome
    Map[String, Map[String, File]] samples
    File index
    Map[String, Array[String]] group
    scatter (sample in samples) {
        call methyCall {
            input:
                bs=sample.right["bs"],
                oxbs=sample.right["oxbs"],
                sample=sample.left,
        }
    }
    call generateMatrix5mc {
        input:
            files=methyCall.out,
            idx=index
    }
    call generateMatrix5hmc {
        input:
            files=methyCall.out,
            idx=index
    }

    call findDifferentiallyMethylationCpG as findDmc {
        input:
            matrix=generateMatrix5mc.out,
            controlGroup=group['control'],
            testGroup=group['test'],
            type="dmc"
    }
    call findDifferentiallyMethylationCpG as findDhmc {
        input:
            matrix=generateMatrix5hmc.out,
            controlGroup=group['control'],
            testGroup=group['test'],
            type="dhmc"
    }
    call findDifferentiallyMethylationRegion as findDmr {
        input:
            dmc=findDmc.out,
            type="dmr"
    }
    call findDifferentiallyMethylationRegion as findDhmr {
        input:
            dmc=findDhmc.out,
            type="dhmr"
    }

    call matrixExtractCpG as matrixExtractDhmcRegion5hmc {
        input:
            matrix=generateMatrix5hmc.out,
            bed=findDhmc.out,
            type='5hmc'
    }
    call matrixExtractCpG as matrixExtractDmcRegion5mc {
        input:
            matrix=generateMatrix5mc.out,
            bed=findDmc.out,
            type='5mc'
    }

    call intersectDmcDhmc {
        input:
            dhmc=findDhmc.out,
            dmc=findDmc.out
    }

    call matrixExtractCpG as matrixExtractDmcDhmcRegion5mc {
        input:
            matrix=generateMatrix5mc.out,
            bed=intersectDmcDhmc.out,
            type='5mc'
    }
    call matrixExtractCpG as matrixExtractDmcDhmcRegion5hmc {
        input:
            matrix=generateMatrix5hmc.out,
            bed=intersectDmcDhmc.out,
            type='5hmc'
    }
    call correlationOf5mcAnd5hmc {
        input:
            matrix5mc=matrixExtractDmcDhmcRegion5mc.out,
            matrix5hmc=matrixExtractDmcDhmcRegion5hmc.out,
            controlGroup=group['control'],
            testGroup=group['test'],
    }
    call summary {
        input:
            controlGroup=group['control'],
            testGroup=group['test'],
            matrix5mc=generateMatrix5mc.out,
            matrix5hmc=generateMatrix5hmc.out,
            dmc=findDmc.out,
            dhmc=findDhmc.out,
            dmr=findDmr.out,
            dhmr=findDhmr.out
    }
    call regionEnrichment {
        input:
            genome=genome,
            bed=intersectDmcDhmc.out
    }
    call generateReport {
        input:
            title=title,
            description=description,
            summary=summary.out,
            imgCor5mc5hmcControl=correlationOf5mcAnd5hmc.outControl,
            imgCor5mc5hmcTest=correlationOf5mcAnd5hmc.outTest,
            enrichmentRegionGo=regionEnrichment.outImg
    }
}

task methyCall {
    File bs
    File oxbs
    String sample
    command {
        dyq_task_mlml.py  --bs-seq ${bs} --oxbs-seq ${oxbs} -o ${sample}.ratioBed
    }
    output {
        File out = "${sample}.ratioBed"
    }
}

task generateMatrix5mc {
    Array[File] files
    File idx
    command {
        dyq_generate_matrix.py --column 3 -i ${sep="," files} -c ${idx} -o matrix.5mc.bed
    }
    output {
        File out = "matrix.5mc.bed"
    }
}

task generateMatrix5hmc {
    Array[File] files
    File idx
    command {
        dyq_generate_matrix.py --column 4 -i ${sep="," files} -c ${idx} -o matrix.5hmc.bed
    }
    output {
        File out = "matrix.5hmc.bed"
    }
}

task findDifferentiallyMethylationCpG {
    File matrix
    Array[String] controlGroup
    Array[String] testGroup
    String type
    Float foldChange = 1.2
    Float pValue = 0.05
    String outfile = "${type}.bed"
    command {
        dyq_dmc_finder.py find -i ${matrix} -c ${sep="," controlGroup} -t ${sep="," testGroup} -o ${type}.origin.bed
        dyq_dmc_finder.py filter -i ${type}.origin.bed -p ${pValue} -f ${foldChange} -o ${outfile}
    }
    output {
        File out = "${outfile}"
    }
}

task findDifferentiallyMethylationRegion {
    File dmc
    String type
    Int dist = 200
    String outfile = "${type}.bed"
    command {
        dyq_dmr_finder.py -i ${dmc} -o  ${outfile} -d ${dist}
    }
    output {
        File out = "${outfile}"
    }
}

task matrixExtractCpG {
    File matrix
    File bed
    String type
    String outfile = basename(bed, '.bed') +".${type}.bed"
    command {
        dyq_matrix_extract.py dmc -m ${matrix} -i ${bed} -o ${outfile}
    }
    output {
        File out = "${outfile}"
    }
}

task intersectDmcDhmc {
    File dmc
    File dhmc
    command {
        dyq_intersect.py -a ${dmc} -b ${dhmc} -o dmc.dhmc.inter.all.bed
    }
    output {
        File out = "dmc.dhmc.inter.all.bed"
    }
}

task correlationOf5mcAnd5hmc {
    File matrix5mc
    File matrix5hmc
    Array[String] controlGroup
    Array[String] testGroup
    command {
        dyq_plot.py parser_cpg_cor -g ${sep="," controlGroup} -a ${matrix5mc} -b ${matrix5hmc} -o  cor.5mc.5hmc.control.png
        dyq_plot.py parser_cpg_cor -g ${sep="," testGroup} -a ${matrix5mc} -b ${matrix5hmc} -o  cor.5mc.5hmc.test.png
    }
    output {
        File outControl = "cor.5mc.5hmc.control.png"
        File outTest = "cor.5mc.5hmc.test.png"
    }
}

task summary {
    Array[String] controlGroup
    Array[String] testGroup
    File matrix5mc
    File matrix5hmc
    File dmc
    File dhmc
    File dmr
    File dhmr
    command {
        dyq_summury.py \
        -c ${sep="," controlGroup} -t ${sep="," testGroup} \
        --matrix-5mc ${matrix5mc} --matrix-5hmc ${matrix5hmc} \
        --dmc ${dmc} --dhmc ${dhmc} --dmr ${dmr} --dhmr ${dhmr} \
        -o summary.json
    }
    output {
        File out = "summary.json"
    }
}

task regionEnrichment {
    File bed
    String genome
    String outDir = 'enrichment'
    command {
        dyq_enrichment.py -i ${bed} -g ${genome} -o ${outDir}
    }
    output {
        File out = "${outDir}"
        File outImg = "${outDir}/GO_result.png"
    }
}

task generateReport {
    String title
    String description
    File summary
    File imgCor5mc5hmcControl
    File imgCor5mc5hmcTest
    File enrichmentRegionGo
    String  reportDir = 'report'
    command {
        dyq_generate_report.py \
        -o ${reportDir} \
        --title "${title}" \
        --description "${description}" \
        --summary "${summary}" \
        --img-cor-5mc-5hmc-control ${imgCor5mc5hmcControl} \
        --img-cor-5mc-5hmc-test ${imgCor5mc5hmcTest} \
        --img-enrichment-region-go ${enrichmentRegionGo}
    }
    output {
        File out = "${reportDir}"
    }
}

