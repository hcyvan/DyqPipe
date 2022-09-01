suppressPackageStartupMessages(library(optparse))


option_list <- list(
  make_option(c("-i", "--in-file"), type = "character", default = NA, action = "store", help = "The input bed file"),
  make_option(c("-o", "--out-dir"), type = "character", default = NA, action = "store", help = "The output directory"),
  make_option(c("-g", "--genome"), type = "character", default = 'hg38', action = "store", help = "The genome version")
)

opt = parse_args(OptionParser(option_list = option_list, usage = "Change genomic region to realted gene"))


source('./R/base.R')

in.file<-checkOpt(opt, 'in-file', required = TRUE)
out.dir<-checkOpt(opt, 'out-dir', required = TRUE)
genome<-checkOpt(opt, 'genome', required = FALSE)
checkDirAndCreateIfNotExist(out.dir)


suppressPackageStartupMessages(library(GenomicRanges))
suppressPackageStartupMessages(library(ChIPseeker))
suppressPackageStartupMessages(library(clusterProfiler))
suppressPackageStartupMessages(library(org.Hs.eg.db))
suppressPackageStartupMessages(library(ggplot2))




if (genome == 'hg38') {
  suppressPackageStartupMessages(library(TxDb.Hsapiens.UCSC.hg38.knownGene))
  txdb <- TxDb.Hsapiens.UCSC.hg38.knownGene
} else if(genome == 'hg19') {
  suppressPackageStartupMessages(library(TxDb.Hsapiens.UCSC.hg19.knownGene))
  txdb <- TxDb.Hsapiens.UCSC.hg19.knownGene
} else {
  suppressPackageStartupMessages(library(TxDb.Hsapiens.UCSC.hg38.knownGene))
  txdb <- TxDb.Hsapiens.UCSC.hg38.knownGene
}



data<-read.csv(in.file, sep = "\t",header = FALSE)
colnames(data) <- c('chrom','start','end')
region <- GRanges(data)
anno<-annotatePeak(region, tssRegion=c(-1000, 1000), TxDb=txdb,annoDb="org.Hs.eg.db")

gene.df <- bitr(anno@anno$SYMBOL, fromType = "SYMBOL",
               toType = c("ENSEMBL", "ENTREZID"),
               OrgDb = org.Hs.eg.db)


All <- enrichGO(gene          = gene.df$ENTREZID,
                OrgDb         = org.Hs.eg.db,
                ont           = "ALL",
                pAdjustMethod = "BH",
                pvalueCutoff  = 0.01,
                qvalueCutoff  = 0.05,
                readable      = TRUE)

png(file.path(out.dir, 'GO_result.png'), units="in", width=8, height=7, res=300)
barplot(All,showCategory=10,split='ONTOLOGY',font.size=9)+ facet_grid(ONTOLOGY~.,scale="free",space="free_y")
dev.off()


result <- as.data.frame(All@result)
write.csv(result, file=file.path(out.dir, 'GO_result.csv'),quote=FALSE)



