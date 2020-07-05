import pandas as pd
from Bio import pairwise2

# Import format_alignment method
from Bio.pairwise2 import format_alignment

data = pd.read_csv("../Results/dave.csv")
x =data["Dave"] 
y =data["Ish"]

for i in range(0,len(data)):
    X=x[i]
    Y=y[i]
    global_align = pairwise2.align.globalms(X, Y, 10, -2, -1, -1)
    score = global_align[0][2]

    


# Define two sequences to be aligned


# Get a list of the global alignments between the two sequences ACGGGT and ACG satisfying the given scoring
# A match score is the score of identical chars, else mismatch score.
# Same open and extend gap penalties for both sequences.

# matches = 10
#mismatch = -2
# gap = -1
# extending = -1
score_list = []
score_list=[]
score_list.append(score)

print(score)
print (score_list)
