import pandas
import urllib3
info=pandas.read_csv("kinase_inhibitor_list_new.csv",encoding="ISO-8859-1")
info
inhibitor=[]
pub_id=[]
chem_formula=[]
info=pandas.read_csv("kinase_inhibitor_list_new.csv",encoding="ISO-8859-1")
for x in info["PubChem CID"]:
    x=str(x)
    x=x.split(".")[0]
    info["PubChem_CID"]= x
    pub_id.append(x)
    
for x in info["Inhibitor"]:
    inhibitor.append(x)
    
for x in info["Brutto"]:
    chem_formula.append(x)
   
info2=pandas.DataFrame({"Inhibitor":inhibitor, "PubChem_id":pub_id,"Chemical formula":chem_formula})
info2
urllist=[]
for x in info2["PubChem_id"]:
    if x!="Unavailable":     
        y="https://pubchem.ncbi.nlm.nih.gov/image/imagefly.cgi?cid="+x+"&width=300&height=300"
        urllist.append(y)
    if x=="Unavailable":        
        y="Unavailable"       
        urllist.append(y)
info2['Chemical_Structure']=urllist        
import pandas as pd
from IPython.core.display import HTML
def path_to_image_html(path):
    return '<img src="'+ path + '" width="60" >'
pd.set_option('display.max_colwidth', -1)
HTML(info2.to_html(escape=False ,formatters=dict(Chemical_Structure= path_to_image_html))
info2.to_csv('Chemical_structures.csv',sep=",",encoding="ISO-8859-1")