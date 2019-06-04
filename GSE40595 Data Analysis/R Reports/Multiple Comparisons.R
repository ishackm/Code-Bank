# Version info: R 3.2.3, Biobase 2.30.0, GEOquery 2.40.0, limma 3.26.8
# R scripts generated  Fri Mar 29 10:38:14 EDT 2019

################################################################
#   Differential expression analysis with limma
library(Biobase)
library(GEOquery)
library(limma)

# load series and platform data from GEO

gset = read.csv("../Data/final_gset.csv", header = TRUE, row.names = 1)

#gset <- getGEO( raed, GSEMatrix =TRUE, AnnotGPL=TRUE)
#if (length(gset) > 1) idx <- grep("GPL570", attr(gset, "names")) else idx <- 1
#gset <- gset[[idx]]

# make proper column names to match toptable 
#fvarLabels(gset) <- make.names(fvarLabels(gset))

# group names for all samples
gsms <- paste0("00000000111111111111111111111111111111122222233333",
               "333333333333333333333333333")
sml <- c()
for (i in 1:nchar(gsms)) { sml[i] <- substr(gsms,i,i) }

# log2 transform
#ex <- exprs(gset)
#qx <- as.numeric(quantile(ex, c(0., 0.25, 0.5, 0.75, 0.99, 1.0), na.rm=T))
#LogC <- (qx[5] > 100) ||
  #(qx[6]-qx[1] > 50 && qx[2] > 0) ||
  #(qx[2] > 0 && qx[2] < 1 && qx[4] > 1 && qx[4] < 2)
#if (LogC) { ex[which(ex <= 0)] <- NaN
#exprs(gset) <- log2(ex) }

# set up the data and proceed with analysis
sml <- paste("G", sml, sep="")    # set group names
fl <- as.factor(sml)
#gset$description <- fl

#G1 vs G0

design<- model.matrix(~0+ fl)
#design <- model.matrix(~ description + 0, gset)
colnames(design) <- levels(fl)
fit <- lmFit(gset, design)
cont.matrix <- makeContrasts(comp1 = G1 - G0, levels = design)

comp1 <- contrasts.fit(fit, cont.matrix[,"comp1"])

comp1 <- eBayes(comp1)

tT <- topTable(comp1, adjust="fdr", sort.by="none", number= 22221)

write.table(tT, file=stdout(), row.names=F, sep="\t")
write.csv(tT, "../Data/Comparisons/Sample Comparisons/G1 - G0.csv")


#G2 vs G0

design<- model.matrix(~0+ fl)
colnames(design) <- levels(fl)
fit <- lmFit(gset, design)
cont.matrix <- makeContrasts(comp2 = G2 - G0, levels = design)

comp2 <- contrasts.fit(fit, cont.matrix[,"comp2"])

comp2 <- eBayes(comp2)


tT <- topTable(comp2, adjust="fdr", sort.by="none", number= 22221)

write.table(tT, file=stdout(), row.names=F, sep="\t")
write.csv(tT, "../Data/Comparisons/Sample Comparisons/G2 - G0.csv")


#G3 vs G0

design<- model.matrix(~0+ fl)
colnames(design) <- levels(fl)
fit <- lmFit(gset, design)
cont.matrix <- makeContrasts(comp3 = G3 - G0, levels = design)

comp3 <- contrasts.fit(fit, cont.matrix[,"comp3"])

comp3 <- eBayes(comp3)


tT <- topTable(comp3, adjust="fdr", sort.by="none", number= 22221)

write.table(tT, file=stdout(), row.names=F, sep="\t")
write.csv(tT, "../Data/Comparisons/Sample Comparisons/G3 - G0.csv")

#G1 vs G3

design<- model.matrix(~0+ fl)
colnames(design) <- levels(fl)
fit <- lmFit(gset, design)
cont.matrix <- makeContrasts(comp4 = G1 - G3, levels = design)

comp4 <- contrasts.fit(fit, cont.matrix[,"comp4"])

comp4 <- eBayes(comp4)


tT <- topTable(comp4, adjust="fdr", sort.by="none", number= 22221)

write.table(tT, file=stdout(), row.names=F, sep="\t")
write.csv(tT, "../Data/Comparisons/Sample Comparisons/G1 - G3.csv")


#G1 vs G2

design<- model.matrix(~0+ fl)
colnames(design) <- levels(fl)
fit <- lmFit(gset, design)
cont.matrix <- makeContrasts(comp5 = G1 - G2, levels = design)

comp5 <- contrasts.fit(fit, cont.matrix[,"comp5"])

comp5 <- eBayes(comp5)


tT <- topTable(comp5, adjust="fdr", sort.by="none", number= 22221)

write.table(tT, file=stdout(), row.names=F, sep="\t")
write.csv(tT, "../Data/Comparisons/Sample Comparisons/G1 - G2.csv")

#G2 vs G3

design<- model.matrix(~0+ fl)
colnames(design) <- levels(fl)
fit <- lmFit(gset, design)
cont.matrix <- makeContrasts(comp6 = G2 - G3, levels = design)

comp6 <- contrasts.fit(fit, cont.matrix[,"comp6"])

comp6 <- eBayes(comp6)


tT <- topTable(comp6, adjust="fdr", sort.by="none", number= 22221)

write.table(tT, file=stdout(), row.names=F, sep="\t")
write.csv(tT, "../Data/Comparisons/Sample Comparisons/G2 - G3.csv")








































