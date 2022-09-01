###########################stacked bar charts###################################

suppressPackageStartupMessages(library(optparse))

options <- list(
  
  make_option(c("-a", "--test-C"), type = "double", default = NA, 
              action = "store", help = "Percentage value of C of test"),
  make_option(c("-b", "--test-5hmc"), type = "double", default = NA, 
              action = "store", help = "Percentage value of 5hmc of test"),
  make_option(c("-c", "--test-5mc"), type = "double", default = NA, 
               action = "store", help = "Prcentage value of 5mc of test"),
  make_option(c("-d", "--control-C"), type = "double", default = NA, 
              action = "store", help = "Percentage value of C of control"),
  make_option(c("-e", "--control-5hmc"), type = "double", default = NA, 
               action = "store", help = "Percentage value of 5hmc of control"),
  make_option(c("-f", "--control-5mc"), type = "double", default = NA, 
               action = "store", help = "Percentage value of 5mc of control"),
  make_option(c("-s", "--out-directory"), type = "character", default = NA, 
               action = "store", help = "Path to save results")
  
)
args<-parse_args(OptionParser(option_list=options))


DrawStackedBarChart<-function(a,b,c,d,e,f,g){
  
  suppressPackageStartupMessages(library(ggplot2))
 
#############################create table####################################### 
  group<-c(rep("test",3),rep("control",3))
  condition<-factor(rep(c("C","5hmc","5mc"),2))
  value<-c(0)
  data<-data.frame(group,condition,value)
  data$value<-c(a,b,c,d,e,f)
  print(data)
  
#############################plot stacked bar chart#############################  
  png(filename=g)  
  ggm<-ggplot(data,aes(fill=relevel(condition,"C"),y=value,x=group))+
    geom_bar(width=0.7,position="stack",stat="identity")+
    scale_fill_manual(values=c("#D2D2C7","#03B161","#B55B0B"))+
    ggtitle("Methylation rate between control and test")+
    ylab("% Modification")+theme_classic()+
    theme(
      plot.title = element_text(face="bold",color="black", size=18),
      axis.title.x = element_blank(),
      axis.title.y = element_text(face="bold",color="black", size=18),
      axis.text.x=element_text(face="bold",color="black",size=18),
      axis.text.y=element_text(face="bold",color="black",size=18),
      axis.line=element_line(colour="black",size=1,linetype="solid"),
      legend.title=element_blank(),
      legend.text=element_text(colour="black",size=12,face="bold")
    )
  print(ggm)
  dev.off()
  
}

DrawStackedBarChart(args[['test-C']],
                    args[['test-5hmc']],
                    args[['test-5mc']],
                    args[['control-C']],
                    args[['control-5hmc']],
                    args[['control-5mc']],
                    args[['out-directory']])
