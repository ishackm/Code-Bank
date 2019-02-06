# models.py

from db import db


class Alt_names(db.Model):
    __tablename__ = "Alt_names"

    Kinase_name = db.Column(db.String, primary_key=True)
    Protein_name = db.Column(db.String)
    UniqueID = db.Column(db.Integer)

class Inhibitor(db.Model):

    __tablename__ = "Inhibitor"

    Inhibitor_ID = db.Column(db.Integer, primary_key=True)
    Inhibitor_name = db.Column(db.String)
    Chemical_structure = db.Column(db.String)
    Chemical_diagram = db.Column(db.BLOB)



class Kinase(db.Model):

    __tablename__ = "Kinase"

    Kinase_name = db.Column(db.Integer, primary_key=True)
    Accession_number = db.Column(db.Integer)
    Gene_symbol = db.Column(db.String)
    Gene_family = db.Column(db.String)
    Cell_location = db.Column(db.String)
    Genome_location = db.Column(db.String)
    Protein_longname = db.Column(db.String)



class Kinase_Inhibitor(db.Model):

    __tablename__ = "Kinase_Inhibitor"

    UniqueID = db.Column(db.Integer, primary_key=True)
    Inhibitor_ID = db.Column(db.Integer)
    Protein_name = db.Column(db.String)


class Substrate(db.Model):

    __tablename__ = "Substrate"

    Substrate_accession = db.Column(db.Integer, primary_key=True)
    Substrate_name = db.Column(db.String)
    Substrate_gene_name = db.Column(db.String)


class Substrate_phosphosite(db.Model):

    __tablename__ = "Substrate_phosphosite"

    Substrate_kinase_ID = db.Column(db.Integer, primary_key=True)
    Substrate_name = db.Column(db.String)
    Modified_residue = db.Column(db.String)
    Neighbour_sequence = db.Column(db.String)


class Substrate_site_Kinase(db.Model):

    __tablename__ = "Substrate_site_Kinase"

    Substrate_kinase_ID = db.Column(db.Integer, primary_key=True)
    UniqueID = db.Column(db.Integer)
    Kinase_name = db.Column(db.String)
