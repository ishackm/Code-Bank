import pandas

import urllib3

#retrieve all known human protein kinases from the source: https://www.uniprot.org/docs/pkinfam.txt (text format)
uniprot_kinases=pandas.read_csv("https://www.uniprot.org/docs/pkinfam.txt", sep="\t", names=["Column1"],skiprows=74, skip_blank_lines=True )
uniprot_kinases=uniprot_kinases[uniprot_kinases.Column1.str.contains("_")]
uniprot_kinases=pandas.DataFrame(uniprot_kinases.Column1.str.split("\)  ",1).tolist(),columns=["human","mouse"])

#get rid of mouse column
uniprot_kinases=uniprot_kinases.drop(["mouse"],axis=1)

#get rid of accession numbers
uniprot_kinases["human"]=uniprot_kinases["human"].str.slice_replace (-12,-1, "")
uniprot_kinases=pandas.DataFrame(uniprot_kinases.human.str.split(" ",1).tolist(), columns=["Kinase","Kinase_ID"])
uniprot_kinases=uniprot_kinases[uniprot_kinases["Kinase_ID"].str.contains("HUMAN")]
uniprot_kinases["Kinase_ID"]=uniprot_kinases["Kinase_ID"].str.strip()
uniprot_kinases=uniprot_kinases.append({"Kinase" : "B1_VACCW", "Kinase_ID" : "B1_VACCW"}, ignore_index=True)

#convert the data frame into a dictionary 
pkinfam_dict = dict(zip(uniprot_kinases.Kinase, uniprot_kinases.Kinase_ID))

#assign all values (kinase names) from the dictionary above to the variable "protein list"
protein_list=pkinfam_dict.values()
protein_list=list(protein_list)
print (protein_list)

raw_data=pandas.DataFrame() #empty pandas dataframe

#create empty lists to append info from Uniprot into to create final data frame

Accession=[] #Entry
Kinase_name=[] #Entry name
Gene_symbol=[] #Gene names
Protein_family=[] #Protein families
Cell_location=[] #Subcellular location [CC]
Protein_longname=[] #Protein names

for protein in protein_list:
    
    try: #error handling, **see below**
        
        #uniprot API column names added to link to parse all required data 
        info=pandas.read_csv("https://www.uniprot.org/uniprot/?query=" + protein +"&sort=score&columns=id,entry%20name,protein%20names,genes(ALTERNATIVE),genes,families,protein,comment(SUBCELLULAR%20LOCATION),%20names&format=tab",sep="\t")
        
        #convert info from uniprot into a pandas dataframe
        info=pandas.DataFrame(info)
        
        #to ensure the index values are not used along the concatenation axis. 
        raw_data=raw_data.append(info,ignore_index=True)
        
        #replace allcempty cells("NaN") with a string to avoid "numpy.dtype('float64')" error
        raw_data=raw_data.fillna("UNAVAILABLE")

        
    #when an empty data or header is encountered, ignore it, to avoid the error:"pandas.io.common.EmptyDataError: No columns to parse from file"
    except pandas.errors.EmptyDataError: 
        continue

#raw_data

#assign accession number for each protein in new data frame        
for acc in raw_data["Entry"]:
    Accession.append(acc)
    
#assign kinase name for each protein in new data frame and add to list        
for kin_name in raw_data["Entry name"]:
    Kinase_name.append(kin_name)

#assign kinase name for each protein in new data frame and add to list
for gene_sym in raw_data["Gene names"]:
    Gene_symbol.append(gene_sym)
    
#assign protein family for each protein in new data frame and add to list   
for pro_fam in raw_data["Protein families"]:
    Protein_family.append(pro_fam)

#assign subcellular location for each protein in new data frame and add to list
for subcell in raw_data["Subcellular location [CC]"]:
    if "SUBCELLULAR LOCATION: " in subcell:
        
        #each entry's location begins with the string "SUBCELLULAR LOCATION:" / indexing to remove that string from the final list/data frame
        subcell=subcell.split("SUBCELLULAR LOCATION: ")[1]
        
    #get rid of the long notes that some location entries contain
    if ("Note=") in subcell:
        subcell=subcell.split("Note=")[0]
    else:
        subcell=subcell
    Cell_location.append(subcell)

#assign protein name for each protein in new data frame and add to list
for proname in raw_data["Protein names"]:
    proname=proname.split("(")[0]
    Protein_longname.append(proname)

        
#new data frame with edited data and new column names        
df=pandas.DataFrame({"Kinase_name": Kinase_name, "Gene_symbol":Gene_symbol, "Gene_family":Protein_family, "Cell_Location":Cell_location, "Protein_longname": Protein_longname, "Accession":Accession})
df

#create csv file 
df.to_csv('all_kinases.csv', sep=",")

#Sites that the kinase phosphorylates:

kinase_target_sites=pandas.read_csv("Kinase_Substrate_Dataset-final-edit.txt",sep="\t")

kinase_target_sites=kinase_target_sites.append(kinase_target_sites,ignore_index=True)

Accession=[]
Gene_symbol=[]
Modified_by=[]
#Position=[]
Modified_residue=[]

for acc in kinase_target_sites["ACCESSION"]:
    Accession.append(acc)

for kinase in kinase_target_sites["KINASE"]:
    Modified_by.append(kinase)
    
for target in kinase_target_sites["SUBSTRATE"]:
    Gene_symbol.append(target)
    
for modres in kinase_target_sites["MOD_RES"]:
    Modified_residue.append(modres)
    




df2=pandas.DataFrame({"Accession": Accession, "Gene_symbol":Gene_symbol, "Modified_by":Modified_by, "Modified_residue":Modified_residue})
df2 
