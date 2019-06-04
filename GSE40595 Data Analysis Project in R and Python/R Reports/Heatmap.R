
# install.packages("pheatmap", "RColorBrewer", "viridis")
library(pheatmap)
library(RColorBrewer)
library(viridis)


# MOCS vs MOSE
comp1 = read.csv("../Python/Heatmap_Analysis/Comparison Gsets/MOCSvsMOSE_gset.csv", header = TRUE, row.names = 1)


data = comp1[9:45] # select the samples columns


annot = read.csv("../Data/annot_045.csv", header = TRUE, row.names = 1) # sample annotation

metadata<-subset(annot, Group=="MOCS"|Group=="MOSE") # select the sample groups for comparison

rownames(metadata) <- colnames(data) # match the samples in the two datasets


# code for the heatmap


mycols <- brewer.pal(10, "RdBu")


require(pheatmap)
data1 = scale(data)
out <- pheatmap(data1, 
                show_rownames=F, color = mycols,breaks = c(-2,-1.5,-1,-0.5,0,0.5,1,1.5,2,2.5)
                ,main = "MOCS vs MOSE",fontsize = 7, cluster_cols=T, cluster_rows=T, scale="row",cex=1, clustering_distance_rows="euclidean", cex=1,
                clustering_distance_cols="euclidean", clustering_method="complete", border_color=FALSE,
                annotation_col=metadata, xlim=c(-7.7,7))







# MOCS vs MOTEC
comp2 = read.csv("../Python/Heatmap_Analysis/Comparison Gsets/MOCSvsMOTEC_gset.csv", header = TRUE, row.names = 1)


mocs_sample = comp2[9:39]
motec_sample = comp2[46:77]
data2 <- cbind(mocs_sample, motec_sample) 

data2 = scale(data2)


annot = read.csv("../Data/annot_045.csv", header = TRUE, row.names = 1) # sample annotation

metadata2<-subset(annot, Group=="MOCS"|Group=="MOTEC") # select the sample groups for comparison


rownames(metadata2) <- colnames(data2) # match the samples in the two datasets

mycols <- brewer.pal(10, "RdBu")


# code for the heatmap
#data2 = scale(data2)
require(pheatmap)
out <- pheatmap(data2, 
                show_rownames=F, color = mycols,breaks = c(-2,-1.5,-1,-0.5,0,0.5,1,1.5,2,2.5)
                ,main = "MOCS vs MOTEC",fontsize = 6,
                cluster_cols=T, cluster_rows=T, scale="row",cex=1, clustering_distance_rows="euclidean", cex=1,
                clustering_distance_cols="euclidean", clustering_method="complete", border_color=FALSE,
                annotation_col=metadata2, xlim=c(-7.7,7))


# MOTEC vs MOSE
comp3 = read.csv("../Python/Heatmap_Analysis/Comparison Gsets/MOSEvsMOTEC_gset.csv  ", header = TRUE, row.names = 1)


data3 = comp3[40:77] # select the sample columns


annot = read.csv("../Data/annot_045.csv", header = TRUE, row.names = 1) # sample annotation

metadata3<-subset(annot, Group=="MOTEC"|Group=="MOSE") # select the sample groups for comparison

rownames(metadata3) <- colnames(data3) # match the samples in the two datasets


mycols <- brewer.pal(10, "RdBu")

data3 = scale(data3)

# code for the heatmap

require(pheatmap)
out <- pheatmap(data3, 
                show_rownames=F,main = "MOTEC vs MOSE",fontsize = 7,
                cluster_cols=T, cluster_rows=T, scale="row",cex=1, clustering_distance_rows="euclidean", cex=1,
                clustering_distance_cols="euclidean", clustering_method="complete", border_color=FALSE,
                annotation_col=metadata3,color = mycols,breaks = c(-2,-1.5,-1,-0.5,0,0.5,1,1.5,2,2.5), xlim=c(-7.7,7))


