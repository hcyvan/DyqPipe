workflow DyqPipe {
  Map[String, Map[String, File]] samples
  scatter (sample in samples) {
    call methyCall {
      input:
        bs=sample.right["bs"],
        oxbs=sample.right["oxbs"],
        sample=sample.left,
    }
  }
}

task methyCall {
  File bs
  File oxbs
  String sample
  command {
    dyq_task_mlml.py  --bs-seq ${bs} --oxbs-seq ${oxbs} -o ${sample}.call.bed
    echo aaa > aaa.call.bed
  }
#  output { File out = "${sample}.call.bed" }
}
