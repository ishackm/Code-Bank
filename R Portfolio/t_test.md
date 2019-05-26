T test for each row
================
Ishack
27 May 2019

``` r
data = read.csv("original_data.csv") # import the dataset
head(data)
```

    ##   Gene.Symbol        Division          Category QE1_Jo_Exp1_AOCS1
    ## 1         ALB Non-ECM Protein   Non-ECM Protein          37623.12
    ## 2       POSTN  Core matrisome ECM Glycoproteins          29567.72
    ## 3       POSTN  Core matrisome ECM Glycoproteins          29564.63
    ## 4   HIST1H2BB Non-ECM Protein   Non-ECM Protein          26814.03
    ## 5        AHSG Non-ECM Protein   Non-ECM Protein          25752.90
    ## 6         VIM Non-ECM Protein   Non-ECM Protein          24976.30
    ##   QE1_Jo_Exp1_G33 QE1_Jo_Exp1_G164 QE1_Jo_Exp1_G342 QE1_Jo_Exp1_G351
    ## 1       40166.904      352347.5090         924.2543         733.3503
    ## 2       34018.336         212.4495       43512.8320       48251.9929
    ## 3       34018.336         188.1493       43511.1663       48247.2426
    ## 4        4382.611         283.5868        2258.9506         987.5856
    ## 5       18890.483        1833.1177         257.6850         233.0221
    ## 6       40067.900         467.2290       26315.5844       47464.7515
    ##   QE1_Jo_Exp1_G369
    ## 1        1324.5012
    ## 2       37954.5521
    ## 3       37949.7421
    ## 4        2777.5721
    ## 5         479.1749
    ## 6       37981.5538

``` r
data = subset(data,data$Category!="Non-ECM Protein")
genename = data[, 1]
Gene.Symbol = as.data.frame(genename)
```

``` r
data$Division <- data$Category <- data$Gene.Symbol <- NULL

pValues <- apply(data, 1, function(x) t.test(x[2:4],x[5:7])$p.value)
pValues = as.data.frame(pValues)

PvData = data.frame(gene=Gene.Symbol,pValues=pValues)
head(PvData)
```

    ##    genename    pValues
    ## 2     POSTN 0.32416156
    ## 3     POSTN 0.32428628
    ## 19    PRSS1 0.78892014
    ## 28   COL3A1 0.89373457
    ## 40 SERPINH1 0.05691749
    ## 43    PLOD1 0.43697109
