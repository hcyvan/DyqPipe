##################################
### Cluster and PCA by Methylation Ratio
##########################################################################

suppressPackageStartupMessages(library(optparse))

options <- list(
  
  make_option(c("-i", "--input-dir"), type = "character", default = NA, 
              action = "store", help = "directory of main_info.txt"),
  make_option(c("-o", "--out-dir"), type = "character", default = NA, 
              action = "store", help = "directory of results"),
  make_option(c("-b", "--bed-file"), type = "character", default = NA, 
              action = "store", help = "name of a bedfile")
  
)
args<-parse_args(OptionParser(option_list=options))



ptPCA_dend <- function(A,B,bedfile){
  
  suppressPackageStartupMessages(library(FactoMineR))
  suppressPackageStartupMessages(library(factoextra))
  suppressPackageStartupMessages(library(RColorBrewer))
  suppressPackageStartupMessages(library(ape))
  suppressPackageStartupMessages(library(dendextend))
  
  input_dir = A
  outdir = B
  
  group_type <- read.table(paste(input_dir,"\\main_info.txt",sep=""),sep="\t",header = TRUE)
  
  mcbed <- read.csv(paste(paste(input_dir,"\\",sep=""),bedfile,sep=""),sep="\t",header = TRUE)
  #stcol=brewer.pal(8,da)[1:length(unique(group_type$Group))]
  #names(stcol) <- unique(group_type$Group)
  
  cols <- colorspace::rainbow_hcl(length(unique(group_type$Group)), c = 70, l  = 50)
  stcol <- cols[factor(group_type$Group)]
  names(stcol) <- group_type$Group
  
  #for (i in 1:length(stcol)){
  #  group_type$color[group_type$Group==names(stcol)[i]] <- stcol[i]
  #}
  
  
  colnames(mcbed)
  data<-mcbed[,match(group_type$Sample,colnames(mcbed))]
  
  dist_mm<-dist(t(data))
  hclust_avg <- hclust(dist_mm)
  dend <- as.dendrogram(hclust_avg)
  #labels_colors(dend) <- group_type$color[order.dendrogram(dend)]
  
  pdf(paste(outdir,"\\dendrogram.pdf",sep=""), width=6, height=6)
  plot(dend)
  colored_bars(stcol,dend,rowLabels="")
  dev.off()
  
  
  ########################################################################
  
  res.pca <- PCA(t(((as.matrix(data)))), graph = FALSE)
  pdf(paste(outdir,"\\all.sample.pca.pdf",sep=""),width=6,height=6)
  pt<-fviz_pca_ind(res.pca,repel = TRUE,
               col.ind=group_type$Group,palette=stcol,
               addEllipses=TRUE,
               ellipse.alpha = 0.01,
               pointsize =1.5,
               col.var="black",
               axes=c(1,2),
               pointshape = 19)+
    theme_classic()+
    theme(plot.title = element_blank(),axis.text=element_text(size=20,colour="black"),
          axis.title=element_text(size=20))
  print(pt)
  dev.off()
  
}


ptPCA_dend(args[['input-dir']],args[['out-dir']],args[['bed-file']])


