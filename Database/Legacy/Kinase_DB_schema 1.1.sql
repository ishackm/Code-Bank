CREATE TABLE Kinase (
	Kinase_name VARCHAR(15) NOT NULL,
	Accession_number VARCHAR(10) NOT NULL,
	Gene_symbol VARCHAR(7) NOT NULL,
	Gene_family VARCHAR(30) NOT NULL,
	Cell_location VARCHAR(50) NOT NULL,
	Cell_loc_image VARCHAR(100), --image link expected
	Genome_location VARCHAR(12) NOT NULL,
	Protein_longname VARCHAR(50) NOT NULL,
	PRIMARY KEY (Kinase_name)
);

CREATE TABLE Phosphosite_info (
	Gene_symbol VARCHAR(7) NOT NULL,
	Position_ModRes VARCHAR(5) NOT NULL,
	Modified_by VARCHAR(50),
	Neighbour_sequence VARCHAR(20) NOT NULL, --7 amino acids either side of modified residue
	PRIMARY KEY (Gene_symbol,Position_ModRes),
	FOREIGN KEY (Gene_symbol) REFERENCES Kinase(Gene_symbol) 
);

CREATE TABLE Alt_names (
	Gene_symbol VARCHAR(7) NOT NULL,
	Protein_name VARCHAR(15) NOT NULL,
	PRIMARY KEY (Gene_symbol,Protein_name),
	FOREIGN KEY (Gene_symbol) REFERENCES Kinase(Gene_symbol)
);

CREATE TABLE Kinase_Inhibitor (
	Protein_name VARCHAR(15) NOT NULL,
	Inhibitor_name VARCHAR(40) NOT NULL,
	PRIMARY KEY (Protein_name,Inhibitor_name),
	FOREIGN KEY (Protein_name) REFERENCES Alt_names(Protein_name),
	FOREIGN KEY (Inhibitor_name) REFERENCES Inhibitor(Inhibitor_name)
);

CREATE TABLE Inhibitor (
	Inhibitor_name VARCHAR(40) NOT NULL,
	Chemical_structure VARCHAR(20),
	Chemical_diagram VARCHAR(50), --image link expected
	PRIMARY KEY (Inhibitor_name)
);

INSERT INTO Kinase (Kinase_name,Gene_symbol,Gene_family,Cell_location,Genome_location,Neighbour_sequence,Protein_longname)
	VALUES('MK01_HUMAN','MAPK1','CMGC','<img>1','22q11.22','MAAAAAAGAGPEMVRGQVFDVGPRYTNLSYIGEGAYGMVCSAYDNVNKVRVAIKKISPFE','Mitogen-activated protein kinase 1');

INSERT INTO Alt_names (Gene_symbol,Protein_name)
	VALUES('MAPK1','ERK2');

INSERT INTO Phosphosite_info(Gene_symbol,Position,Modified_residue,Modified_by)
	VALUES('MAPK1',29,'S','SGK1');

INSERT INTO Kinase_Inhibitor (Protein_name,Inhibitor_name)
	VALUES('TTT-3002','ERK2');

INSERT INTO Inhibitor (Inhibitor_name,Chemical_structure,Chemical_diagram)
	VALUES('TTT-3002',NULL,'<img>10');