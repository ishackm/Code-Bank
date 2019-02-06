from flask_table import Table, Col

class Results(Table):
    Kinase_name = Col('Kinase_name')
    Protein_name = Col('Protein_name')
    UniqueID = Col('UniqueID')
    
