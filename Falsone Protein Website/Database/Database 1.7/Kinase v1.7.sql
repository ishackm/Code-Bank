CREATE TABLE Kinase (
	Kinase_name VARCHAR(15) NOT NULL,
	Accession_number VARCHAR(10) NOT NULL,
	Gene_symbol VARCHAR(7) NOT NULL,
	Gene_family VARCHAR(30) NOT NULL,
	Cell_location VARCHAR(50) NOT NULL,
	Genome_location VARCHAR(12),
	Protein_longname VARCHAR(50) NOT NULL,
	PRIMARY KEY (Kinase_name)
);

CREATE TABLE Substrate_site_Kinase (
	Substrate_kinase_ID INTEGER(5) NOT NULL,
	UniqueID INTEGER(5) NOT NULL,
	Kinase_name VARCHAR(10) NOT NULL,
	PRIMARY KEY (UniqueID),
	FOREIGN KEY (Substrate_kinase_ID) REFERENCES Substrate_phosphosite(Substrate_kinase_ID),
	FOREIGN KEY (Kinase_name) REFERENCES Alt_names(Protein_name)
);

CREATE TABLE Substrate_phosphosite (
	Substrate_kinase_ID INTEGER(7) NOT NULL,
	Substrate_name VARCHAR(20) NOT NULL,
	Modified_residue VARCHAR(7) NOT NULL,
	Neighbour_sequence VARCHAR(20) NOT NULL,
	PRIMARY KEY (Substrate_kinase_ID),
	FOREIGN KEY (Substrate_name) REFERENCES Substrate(Substrate_name)
);

CREATE TABLE Substrate (
	Substrate_accession VARCHAR(8) NOT NULL,
	Substrate_name VARCHAR(20) NOT NULL,
	Substrate_gene_name VARCHAR(15) NOT NULL,
	PRIMARY KEY (Substrate_name)
);

CREATE TABLE Alt_names (
	Kinase_name VARCHAR(7) NOT NULL,
	Protein_name VARCHAR(15) NOT NULL UNIQUE,
	UniqueID INTEGER(3) NOT NULL,
	PRIMARY KEY (UniqueID),
	FOREIGN KEY (Kinase_name) REFERENCES Kinase(Kinase_name)
);

CREATE TABLE Kinase_Inhibitor (
	UniqueID INTEGER(7) NOT NULL,
	Inhibitor_ID VARCHAR(5) NOT NULL,
	Protein_name VARCHAR(15) NOT NULL,
	PRIMARY KEY (UniqueID),
	FOREIGN KEY (Inhibitor_ID) REFERENCES Inhibitor(Inhibitor_ID),
	FOREIGN KEY (Protein_name) REFERENCES Alt_names(Protein_name)
);

CREATE TABLE Inhibitor (
	Inhibitor_ID VARCHAR(5) NOT NULL,
	Inhibitor_name VARCHAR(40) NOT NULL,
	Chemical_structure VARCHAR(20),
	Chemical_diagram VARCHAR(50), 
	PRIMARY KEY (Inhibitor_ID)
);