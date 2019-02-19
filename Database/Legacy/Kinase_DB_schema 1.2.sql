CREATE TABLE Kinase (
	Kinase_name VARCHAR(15) NOT NULL,
	Accession_number VARCHAR(10) NOT NULL,
	Gene_symbol VARCHAR(7) NOT NULL,
	Gene_family VARCHAR(30) NOT NULL,
	Cell_location VARCHAR(50) NOT NULL,
	Cell_loc_image VARCHAR(100), --image link expected
	Genome_location VARCHAR(12),
	Protein_longname VARCHAR(50) NOT NULL,
	PRIMARY KEY (Kinase_name)
);

CREATE TABLE Substrate_accession (
	Substrate_name VARCHAR(20) NOT NULL,
	Substrate_accession VARCHAR(10) NOT NULL,
	PRIMARY KEY (Substrate_name)
);

CREATE TABLE Substrate_phosphosite (
	UniqueID INTEGER(7) NOT NULL,
	Substrate_name VARCHAR(20) NOT NULL,
	Modified_residue VARCHAR(7) NOT NULL,
	Neighbour_sequence VARCHAR(20) NOT NULL,
	Kinase_name VARCHAR(15) NOT NULL,
	PRIMARY KEY (UniqueID),
	FOREIGN KEY (Kinase_name) REFERENCES Kinase(Kinase_name),
	FOREIGN KEY (Substrate_name) REFERENCES Substrate_accession(Substrate_name)
);

CREATE TABLE Alt_names (
	Kinase_name VARCHAR(7) NOT NULL,
	Protein_name VARCHAR(15) NOT NULL,
	PRIMARY KEY (Protein_name),
	FOREIGN KEY (Kinase_name) REFERENCES Kinase(Kinase_name)
);

CREATE TABLE Kinase_Inhibitor (
	UniqueID INTEGER(7) NOT NULL,
	Protein_name VARCHAR(15) NOT NULL,
	Inhibitor_ID VARCHAR(5) NOT NULL,
	PRIMARY KEY (UniqueID),
	FOREIGN KEY (Protein_name) REFERENCES Alt_names(Protein_name),
	FOREIGN KEY (Inhibitor_ID) REFERENCES Inhibitor(Inhibitor_ID)
);

CREATE TABLE Inhibitor (
	Inhibitor_name VARCHAR(40) NOT NULL,
	Chemical_structure VARCHAR(20),
	Chemical_diagram VARCHAR(50), --image link expected
	Inhibitor_ID VARCHAR(5) NOT NULL
	PRIMARY KEY (Inhibitor_ID)
);