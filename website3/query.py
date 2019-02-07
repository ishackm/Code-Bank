from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
engine=create_engine("sqlite:///final.db")#,echo=True)
Session=sessionmaker(bind=engine)
session=Session()
from sqlalchemy import MetaData, Table
metadata = MetaData()
alt_names=Table('Alt_names', metadata, autoload=True, autoload_with=engine)
inhibitor=Table('Inhibitor',metadata,autoload=True,autoload_with=engine)
kinase=Table('Kinase',metadata,autoload=True,autoload_with=engine)
kinase_inhibitor=Table('Kinase_Inhibitor',metadata,autoload=True,autoload_with=engine)
sub_phos=Table('Substrate_phosphosite',metadata,autoload=True,autoload_with=engine)
substrate_kinase=Table('Substrate_site_Kinase',metadata,autoload=True,autoload_with=engine)
substrate=Table('Substrate',metadata,autoload=True,autoload_with=engine)


search=input("Enter kinase information: ")
search1="%"+search+"%"
searchresult=[]
likequery=session.query(kinase).filter(kinase.c.Kinase_name.like(search1)).all()
if likequery!=[]: #if search found kinases, aka if the search entry was a kinase name
    for x in likequery:
        if x not in searchresult:
            searchresult.append(x[:3])
likequery=session.query(kinase).filter(kinase.c.Accession_number.like(search1)).all()
if likequery!=[]: #if search was an accession number or like an accession number
    for x in likequery:
        if x not in searchresult:
            searchresult.append(x[:3])
likequery=session.query(kinase).filter(kinase.c.Gene_symbol.like(search1)).all()
if likequery!=[]: #if search was a gene symbol or like a gene symbol
    for x in likequery:
        if x not in searchresult:
            searchresult.append(x[:3])

likequery=session.query(alt_names).filter(alt_names.c.Protein_name.like(search1)).all()
if likequery!=[]:
    k_alts=[]
    for x in likequery:
        if x.Kinase_name not in k_alts:
            k_alts.append(x.Kinase_name)
    for x in k_alts:
        likequery=session.query(kinase).filter(kinase.c.Kinase_name.like(x)).all()
        if likequery!=[]: #if search found kinases, aka if the search entry was a kinase name
            for x in likequery:
                if x not in searchresult:
                    searchresult.append(x[:3])

for x in searchresult:
    print(x)
