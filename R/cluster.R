##################################
### Cluster and PCA by Methylation Ratio
##########################################################################
suppressPackageStartupMessages(library(FactoMineR))
suppressPackageStartupMessages(library(factoextra))
suppressPackageStartupMessages(library(RColorBrewer))
suppressPackageStartupMessages(library(ape))
suppressPackageStartupMessages(library(dendextend))


ptPCA_dend <- function(A,B,bedfile)
{
  
input_dir = A
outdir = B

group_type <- read.table(paste0(input_dir,"\\main_info.txt"),sep="\t",header = TRUE)

mcbed <- read.csv(paste0(input_dir,bedfile),sep="\t",header = TRUE)
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

pdf(paste0(outdir,"dendrogram.pdf"), width=6, height=6)
plot(dend)
colored_bars(stcol,dend,rowLabels="")
dev.off()


########################################################################

res.pca <- PCA(t(((as.matrix(data)))), graph = FALSE)
pdf(paste0(outdir,"all.sample.pca.pdf"),width = 6,height = 6)
 fviz_pca_ind(res.pca,repel = TRUE,
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
dev.off()
}


