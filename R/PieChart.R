suppressPackageStartupMessages(library(optparse))

option_list <- list(
  make_option(c("-i", "--bedfile"), type = "character", default = NA, 
              action = "store", help = "Path to a bed file"),
  make_option(c("-o", "--outdir"), type = "character", default = NA, 
              action = "store", help = "Path to save results")
)
args<-parse_args(OptionParser(option_list=option_list))



DrawAnnoPieChart<-function(bedfile, outdir){
  
  suppressPackageStartupMessages(library(ChIPseeker))
  suppressPackageStartupMessages(library(ggplot2))
  suppressPackageStartupMessages(library(gplots))
  
  atac.bed<-read.table(bedfile,header = T,sep="\t",stringsAsFactors = F,quote="")
  atac.bed<-atac.bed[,c(1:3)]
  peak.bed <- GRanges(atac.bed)
  
  
  options(ChIPseeker.ignore_1st_exon = T)
  options(ChIPseeker.ignore_1st_intron = T)
  options(ChIPseeker.ignore_downstream = T)
  options(ChIPseeker.ignore_promoter_subcategory = T)
  
  anno<-annotatePeak(peak.bed,tssRegion=c(-5000, 3000),TxDb=txdb)
  
  
  pdf(outdir, width=5, height=3)
  plotAnnoPie(anno)
  dev.off()
  
}

DrawAnnoPieChart(args$bedfile, args$outdir)






