import pandas

#phosphosite table that contains all known phosphosites (without the kinases known for phosphorylating them)
phos=pandas.read_csv("Phosphosite_FINAL.csv")

phos=phos.fillna("UNAVAILABLE")

#rename columns to match the overlapping columns with the substrate table below
phos.rename(columns={'MOD_RSD': 'MODRES', 'PROTEIN':'TARGET', 'ACC_ID':'SUBSTRATE_ACC_ID'}, inplace=True)


#some protein names were automatically converted to dates in excel 
for x in phos["TARGET"]:
    if x=="Oct-01":
       
        x="Oct1"
    elif x =="Oct-04":
        x="Oct4"
    elif x =="Oct-07":
        x="Oct7"
    else:
        x=x

#table containing all phosphosites with known kinases, along with the kinases responsible for thier phosphorylation. 
sub=pandas.read_csv("substrate_info_final.csv")

#drop empty columns
sub = sub.drop(sub.columns[[6, 7, 8, 9]], axis=1)

#replace empty cells with the string 'UNAVAILABLE'
sub = sub.fillna ("UNAVAILABLE")

#rename columns to match the overlapping columns with the phosphosite table above
sub.rename(columns={'SUBSTRATE_MOD_RES': 'MODRES', 'SUBSTRATE':'TARGET' }, inplace=True)


#cant just match on substrate acession number or modified residue, because one substrate can have multiple kinases that target it.

#join on neighbour seq, modres and substrate accession
kinsub = pandas.merge(phos, sub, how='inner', on = ['SITE_+/-7_AA', 'MODRES','SUBSTRATE_ACC_ID'])

#drop unwanted columns
kinsub = kinsub.drop(kinsub.columns[[1,5]], axis=1)

#rename column
kinsub.rename(columns={'TARGET_y': 'SUBSTRATE'}, inplace=True)

#reorder columns for convenience 
kinsub =kinsub[["SUBSTRATE_ACC_ID" , "GENE" , "SUBSTRATE", "MODRES" , "SITE_+/-7_AA", "HU_CHR_LOC", "KINASE", "KIN_ACC_ID"]]


#create csv file 
kinsub.to_csv('kinsub9', sep=",")
