from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData, Table


def session():
    engine=create_engine("sqlite:///final.db")#,echo=True)
    Session=sessionmaker(bind=engine)
    session=Session()

    metadata = MetaData()
    alt_names=Table('Alt_names', metadata, autoload=True, autoload_with=engine)
    inhibitor=Table('Inhibitor',metadata,autoload=True,autoload_with=engine)
    kinase=Table('Kinase',metadata,autoload=True,autoload_with=engine)
    kinase_inhibitor=Table('Kinase_Inhibitor',metadata,autoload=True,autoload_with=engine)
    sub_phos=Table('Substrate_phosphosite',metadata,autoload=True,autoload_with=engine)
    substrate_kinase=Table('Substrate_site_Kinase',metadata,autoload=True,autoload_with=engine)
    substrate=Table('Substrate',metadata,autoload=True,autoload_with=engine)
