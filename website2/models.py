# models.py

from db import db


class Alt_names(db.Model):
    __tablename__ = "Alt_names"

    Kinase_name = db.Column(db.String, primary_key=True)
    Protein_name = db.Column(db.String)
    UniqueID = db.Column(db.Integer)

    def __repr__(self):
        return "<Alt_names: {}>".format(self.name)


class Inhibitor(db.Model):

    __tablename__ = "Inhibitor"

    Inhibitor_ID = db.Column(db.Integer, primary_key=True)
    Inhibitor_name = db.Column(db.String)
    Chemical_structure = db.Column(db.String)
    Chemical_diagram = db.Column(db.BLOB)

    def __repr__(self):
        return "<Inhibitor: {}>".format(self.name)

class Kinase(db.Model):

    __tablename__ = "Kinase"

    Kinase_name = db.Column(db.Integer, primary_key=True)
    Accession_number = db.Column(db.Integer)
    Gene_symbol = db.Column(db.String)
    Gene_family = db.Column(db.String)
    Cell_location = db.Column(db.String)
    Genome_location = db.Column(db.String)
    Protein_longname = db.Column(db.String)

    def __repr__(self):
        return "<Kinase: {}>".format(self.name)


class Kinase_Inhibitor(db.Model):

    __tablename__ = "Kinase_Inhibitor"

    UniqueID = db.Column(db.Integer, primary_key=True)
    Inhibitor_ID = db.Column(db.Integer)
    Protein_name = db.Column(db.String)

    def __repr__(self):
        return "<Kinase_Inhibitor: {}>".format(self.name)

class Substrate(db.Model):

    __tablename__ = "Substrate"

    Substrate_accession = db.Column(db.Integer, primary_key=True)
    Substrate_name = db.Column(db.String)
    Substrate_gene_name = db.Column(db.String)

    def __repr__(self):
        return "<Substrate: {}>".format(self.name)

class Substrate_phosphosite(db.Model):

    __tablename__ = "Substrate_phosphosite"

    Substrate_kinase_ID = db.Column(db.Integer, primary_key=True)
    Substrate_name = db.Column(db.String)
    Modified_residue = db.Column(db.String)
    Neighbour_sequence = db.Column(db.String)

    def __repr__(self):
        return "<Substrate_phosphosite: {}>".format(self.name)

class Substrate_site_Kinase(db.Model):

    __tablename__ = "Substrate_site_Kinase"

    Substrate_kinase_ID = db.Column(db.Integer, primary_key=True)
    UniqueID = db.Column(db.Integer)
    Kinase_name = db.Column(db.String)

    def __repr__(self):
        return "<Substrate_site_Kinase: {}>".format(self.name)
