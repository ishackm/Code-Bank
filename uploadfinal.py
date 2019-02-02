import os
from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
import pandas
import urllib3
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.plotting import _converter


UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/csv/'
ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__, static_url_path="/static")
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploader', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            print('Please upload a csv file')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            print('No file selected')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file)
            process_file('output_test.png', file )
            return redirect(url_for('uploaded_file', filename=filename))
    return render_template('upload2.html')


def process_file(path, filename):

    info=pandas.read_csv(filename, sep="\t")
    #tsv file, read as table, default is tab separated so no need for sep="\t"

    info=info.dropna(axis=1, how='all')
    #drop all columns were all elements are "NaNs"- when table was exported, some columns contained all NaNs

    info=info.dropna()
    #drop all rows that have at least one "NaN" (empty cell)
    #(eg. AFF1(S245): some phosphosites have no control means, although they have az20 means)

    info.columns = info.columns.str.strip().str.lower().str.replace('(', '').str.replace(')', '') #.str.replace('-', '_')
    #remove all white space, make all strings lower case, remove brackets

    info2= info[info["az20_p-value"] < 0.05]
    #dataframe containing data only for when the p-value is less than 0.05(threshold)

    info2 # -2009

    info3=info2[~info2['substrate'].str.contains("None")]
    #new dataframe where substrate column does not contain elements with the substring ("None"). This removes all substrates with no reported phosphosite in tbhe dataset
    #invert (~) operator acts like a 'not' for boolean data

    info3
    #only contains substrates with phosphosites - 1865

    #Making sure all proteins in the dataframe are kinases

    #retrieve all known human protein kinases from the source: https://www.uniprot.org/docs/pkinfam.txt (text format)
    uniprot_kinases=pandas.read_csv("https://www.uniprot.org/docs/pkinfam.txt", sep="\t", names=["Column1"],skiprows=74, skip_blank_lines=True )
    uniprot_kinases=uniprot_kinases[uniprot_kinases.Column1.str.contains("_")]
    uniprot_kinases=pandas.DataFrame(uniprot_kinases.Column1.str.split("\)  ",1).tolist(),columns=["human","mouse"])

    #get rid of mouse column
    uniprot_kinases=uniprot_kinases.drop(["mouse"],axis=1)

    #get rid of accession numbers
    uniprot_kinases["human"]=uniprot_kinases["human"].str.slice_replace (-12,-1, "")
    uniprot_kinases=pandas.DataFrame(uniprot_kinases.human.str.split(" ",1).tolist(), columns=["Kinase","Kinase_ID"])
    uniprot_kinases=uniprot_kinases[uniprot_kinases["Kinase_ID"].str.contains("HUMAN")]
    uniprot_kinases["Kinase_ID"]=uniprot_kinases["Kinase_ID"].str.strip()
    uniprot_kinases=uniprot_kinases.append({"Kinase" : "B1_VACCW", "Kinase_ID" : "B1_VACCW"}, ignore_index=True)

    #convert the data frame into a dictionary
    pkinfam_dict = dict(zip(uniprot_kinases.Kinase, uniprot_kinases.Kinase_ID))
    protein_list=pkinfam_dict.values()
    protein_list=list(protein_list)

    #list containing all known kinases (identified by their uniprot names)
    protein_list

    #data frame containing all known kinases and their alternative protein and **GENE NAMES?**  or just protein names?
    protein_alt_names=pandas.read_csv("Protein_alt_names.csv", header=None)
    protein_alt_names

    #Create a dictionary with kinase uniprot names as keys and all alternative names as values

    kinase=open("kinase_info_final.csv","r")
    line=kinase.readline()
    alt_names={}

    while line != "":
        line=kinase.readline()
        line=line.split(",")
        if len(line)<2:
            break
        elif line[2] not in alt_names:
            alt_names[line[2]]=[]
            genenames=line[3].split()
            for y in genenames:
                if y not in alt_names[line[2]]:
                    alt_names[line[2]].append(y)
            line2=line[-1].split("(")
            del line2[0]
            for y in line2:
                y2=y.replace(")","")
                y3=y2.replace("\n","")
                while True:
                    if y3[-1]==" ":
                        y3=y3[:-1]
                    else:
                        break
                if y3 not in alt_names[line[2]]:
                    alt_names[line[2]].append(y3)


    for x in alt_names:
        if x=='':
            del alt_names[x]
    kinase.close()


    newfile=open("Protein_alt_names.csv","w+")
    for x in alt_names:
        for y in alt_names[x]:
            newfile.write(x+","+y+"\n")
    newfile.close()

    #concatenate all values of the dictionary into one big list so the list contains all alternative PROTEIN AND GENE names for all known human kinases
    alt_names_list=[value for values in alt_names.values() for value in values]
    print (alt_names_list)

    info3[['kinase','position']] = info3['substrate'].str.split('(',expand=True)
    #split the substrate name from the phosphosite position into separate columns
    #to easily compare the substrate name with the list of kinases

    info4 = info3[info3['kinase'].isin(alt_names_list) | info3['kinase'].isin(protein_list)]
    #checks if substrate name is in the list of all alternative kinase names, OR the list of kinase uniprot names

    info4.to_csv("az_filtered.csv", sep=",")


    substrate = info4['substrate']
    fold_change = info4['az20_fold_change']
    plt.scatter(substrate, fold_change, edgecolors='b')
    plt.xlabel('Substrate')
    plt.ylabel('Fold Change')
    plt.title('Scatter Plot')
    plt.savefig(path)


    # info5 = info4.sort_values(by=['az20_fold_change'], ascending=False)
    # info5

    # info6 = info5.drop(info5.index[20:],axis=0)
    # info6


    # #Top 20 Fold Change graph

    # df = pandas.DataFrame({"substrate":info6["substrate"], 'fold_change': info6["az20_fold_change"]})
    # plt.rcParams["figure.figsize"] =(15,8)
    # plt.rcParams.update({'font.size': 15})
    # ax = df.plot.bar(rot=0)
    # ax.tick_params(labelsize=6)
    # ax.set_xticklabels(lables, rotation=0)
    # ax.set_title("Top 20 Fold Change", fontsize=25)
    # #ax.autoscale(tight=True)
    # plt.xticks(rotation=90)
    # plt.xticks(fontsize=10)
    # plt.yticks(fontsize=12)
    # plt.xlabel('Substrate', fontsize=18)
    # plt.ylabel('Fold Change', fontsize=15)



    # #Control mean vs Inhibitor treated mean graph"

    # lables=info6["substrate"]

    # df = pandas.DataFrame({'control': info6["control_mean"],'treatment': info6["az20_mean"]})

    # plt.rcParams["figure.figsize"] =(15,8)

    # plt.rcParams.update({'font.size': 15})

    # ax = df.plot.bar(rot=0)

    # ax.tick_params(labelsize=6)

    # ax.set_title("Control mean vs Inhibitor treated mean", fontsize=2)

    # ax.set_xticklabels(lables, rotation=0)

    # ax.autoscale(tight=True)

    # plt.xticks(rotation=90)

    # plt.xticks(fontsize=8)

    # plt.yticks(fontsize=12)

    # plt.xlabel('Substrate', fontsize=18)

    # plt.ylabel('Mean phosphopeptide MS1 peak area', fontsize=15)

    # ax.set_title("Top 20 Control mean vs Treated with Inhibitor mean", fontsize=25)
