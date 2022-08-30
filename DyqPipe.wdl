workflow DyqPipe {
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

    call findDmc as findDmc5mc {
        input:
            matrix=generateMatrix5mc.out,
            controlGroup=group['control'],
            testGroup=group['test'],
            type="5mc"
    }
    call findDmc as findDmc5hmc {
        input:
            matrix=generateMatrix5hmc.out,
            controlGroup=group['control'],
            testGroup=group['test'],
            type="5hmc"
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


task findDmc {
    File matrix
    Array[String] controlGroup
    Array[String] testGroup
    String type
    Float foldChange = 1.2
    Float pValue = 0.05
    command {
        dyq_dmc_finder.py find -i ${matrix} -c ${sep="," controlGroup} -t ${sep="," testGroup} -o dmc.${type}.bed
        dyq_dmc_finder.py filter -i dmc.${type}.bed -p ${pValue} -f ${foldChange} -o dmc_${foldChange}_${pValue}_${type}.bed
    }
    output {
        File out = "dmc_${foldChange}_${pValue}_${type}.bed"
    }
}
