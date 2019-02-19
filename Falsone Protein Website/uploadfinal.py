import os
from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
import pandas
import urllib3
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.plotting import _converter
from pylab import rcParams
from matplotlib.pyplot import figure
import matplotlib.patches as mpatches
import sys
#connecting to database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData, Table
import math
import six
from scipy.stats import norm
from flask import abort



def process_file(path, filename):

    info=pandas.read_csv(filename, sep="\t")
    #tsv file, read as table, default is tab separated so no need for sep="\t"


    info=info.dropna(axis=1, how='all')
    #drop all columns were all elements are "NaNs"- when table was exported, some columns contained all NaNs

    pandas.set_option("use_inf_as_na",True)

    info=info.dropna()
    #drop all rows that have at least one "NaN" (empty cell)
    #(eg. AFF1(S245): some phosphosites have no control means, although they have az20 means)

    info.columns = info.columns.str.strip().str.lower().str.replace('(', '').str.replace(')', '') #.str.replace('-', '_')
    #remove all white space, make all strings lower case, remove brackets

    
    #rename column names to make them fit the same format for different uploaded files. (fixed set of column names for every file)
    for x in info.columns.values:
        if "fold" in x:
            a="fold_change"
            info.columns = info.columns.str.replace(x,a)
        if "value" in x:
            b="p-value"
            info.columns = info.columns.str.replace(x,b)
        if "ctrlcv" in x:
            c="ctrlcv"
            info.columns = info.columns.str.replace(x,c)
        if "treatcv" in x:
            d="treatcv"
            info.columns = info.columns.str.replace(x,d)
        if "mean" in x and "control" not in x:
            e="treatment_mean"
            info.columns = info.columns.str.replace(x,e)

        else:
            continue

    #list of the column names in the dataframe and use "set" to remove any duplicates from the list. 
    #Then, if the length of that "unique" list is not the same as the length of the list of column names in the dataset, there are too many inhibitors, so abort. 
    if len(set(info.columns.tolist()))!= len(info.columns):
        abort(403, "ERROR: file contains more than one inhibitor. Please ensure your dataset contains data for one inhibitor only.")




    info=info[~info['substrate'].str.contains("None")] 
    #removes all substrates with no reported phosphosite in the dataset (invert (~) operator acts like a 'not' for boolean data)

    info=info[~info['substrate'].str.contains("\(M")] 
    #remove all methionines -regex

    info['log2_fold_change'] = np.log2(info['fold_change'])
    #log 2 of fold change 

    info['-log10(pvalue)'] = np.log10(info['p-value'])
    info.loc[:, '-log10(pvalue)'] = info['-log10(pvalue)'] * -1
    #-log10 of pvalue 

    info=info.dropna()

    #get log2 of the fold change and -log10 of pvalue and make volcanoe plot

    

    #VOLCANO PLOT

    colours = np.where((info["log2_fold_change"]<-1.5) & (info["-log10(pvalue)"]>1.301) | (info["log2_fold_change"]>1.5) & (info["-log10(pvalue)"]>1.301)  ,'#D74A31', '#297575')

    # colour code for all points where log 2 fold change is greater than 1 (upregulated) AND pvalue is less than 0.05 OR 
    # fold change is less than -1 AND p value is less than 0.05 

    # threshold for p value is 0.05 -> -log10 of 0.05 is 1.301 -> anything above 1.301 is significant

    # threshold for log2 fold change is over 1 and under -1. 

    info.plot.scatter(x='log2_fold_change', y='-log10(pvalue)', c=colours) #assign x and y axis and colours of points

    rcParams['figure.figsize'] = 18, 10 #figure size

    plt.suptitle('Phosphoproteome', fontsize=20) #title

    plt.xlabel("Log2 fold change", fontsize=15) #font size of x axis label

    plt.ylabel("-Log10 p-value", fontsize=15) #font size of y axis label

    plt.xticks(fontsize=12) #font size of x ticks

    plt.yticks(fontsize=12) #font size of y ticks

    red_dots = mpatches.Patch(color='#D74A31', label='Significantly Upregulated or Downregulated')
    grey_dots=mpatches.Patch(color='#297575', label='Non-Significantly Upregulated or Downregulated')
    patches=[red_dots,grey_dots]
    plt.legend(handles=patches)


    #VOLCANO PLOT SAVE IMAGE

    save_results_to = 'static/pp/'
    plt.savefig(save_results_to + 'volcano_ipa.svg', bbox_inches="tight")





    #PREPARING DATAFRAMES FOR GRAPHS BELOW 

    info_=info[info["p-value"] <= 0.05]
    #dataframe containing data only for when the p-value is less than or equal to 0.05(threshold)
    info2=info_.sort_values(by=['log2_fold_change'],ascending=False) #sort values - largest to smallest
    info3=info_.sort_values(by=['log2_fold_change'],ascending=True) #sort values - smallest to largest
    info4 = info2.drop(info2.index[40:],axis=0) #take top 40 of largest values of logFC
    info5 = info3.drop(info3.index[40:],axis=0) #take top 40 of smallest (most negative) values of logFC



    #TOP 40 POSITIVE FOLD CHANGE GRAPH

    #Preparation for graph
    plt.rcParams["figure.figsize"] =(15,8)
    info2=info.sort_values(by=['log2_fold_change'],ascending=False) #sort values - largest to smallest
    info3=info.sort_values(by=['log2_fold_change'],ascending=True) #sort values - smallest to largest
    info4 = info2.drop(info2.index[40:],axis=0) #take top 40 of largest values of logFC
    info5 = info3.drop(info3.index[40:],axis=0) #take top 40 of smallest (most negative) values of logFC
    

    #Plot graph
    labels1=info4["substrate"]
    df = pandas.DataFrame({"substrate":info4["substrate"], 'LogFC': info4["log2_fold_change"]})
    plt.rcParams.update({'font.size': 15})
    ax = df.plot.bar(rot=0, color="#0992A4") 
    ax.tick_params(labelsize=6)
    ax.set_xticklabels(labels1, rotation=45)
    ax.set_title("Top 40 (+ve) Log2 Fold Change", fontsize=25)
    #ax.autoscale(tight=True)
    plt.xticks(rotation=90) 
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=12)
    plt.xlabel('Substrate', fontsize=18)
    plt.ylabel('Log2(FC)', fontsize=18)

    #TOP 40 POSITIVE SAVE IMAGE

    save_results_to = 'static/pp/'
    plt.savefig(save_results_to + 'positive_fold_change_ipa.svg', bbox_inches="tight")




    #BOTTOM 40 FOLD CHANGE GRAPH

    labels2=info5["substrate"]
    df = pandas.DataFrame({"substrate":info5["substrate"], 'LogFC': info5["log2_fold_change"]})
    plt.rcParams.update({'font.size': 15})
    ax = df.plot.bar(rot=0, color= "#18C08F") 
    ax.tick_params(labelsize=6)
    ax.set_xticklabels(labels2, rotation=45)
    plt.suptitle("Top 40 (-ve) Log2 Fold Change", fontsize=25)
    #ax.autoscale(tight=True)
    plt.xticks(rotation=90) 
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=12)
    plt.xlabel('Substrate', fontsize=18)
    plt.ylabel('Log2(FC)', fontsize=18)

    #bottom 40 graph save image
    save_results_to = 'static/pp/'
    plt.savefig(save_results_to + 'negative_fold_change_ipa.svg', bbox_inches="tight")




    #CALL DATABASE

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




    #MATCHING KINASES BASED ON GENE NAME AND PROTEIN NAME IN OUR DB)

    kinasedat={}
    for kn in info.substrate:
        kinlist=[]
        kn=kn.split("(")
        kn[1]=kn[1][:-1]
        subs=kn[0]
        modres=kn[1]
        try:
            kname=session.query(sub_phos).filter(sub_phos.c.Modified_residue==modres,sub_phos.c.Substrate_name==subs).one()
            kin=session.query(substrate_kinase).filter(substrate_kinase.c.Substrate_kinase_ID==kname.Substrate_kinase_ID).all()
            for x in kin:
                if x.Kinase_name not in kinlist:
                    kinlist.append(x.Kinase_name)
            kinasedat[subs+"("+modres+")"]=kinlist
        except:
                try:
                    sname=session.query(substrate).filter(substrate.c.Substrate_gene_name==subs).one()
                    kname=session.query(sub_phos).filter(sub_phos.c.Modified_residue==modres,sub_phos.c.Substrate_name==sname.Substrate_name).one()
                    kin=session.query(substrate_kinase).filter(substrate_kinase.c.Substrate_kinase_ID==kname.Substrate_kinase_ID).all()
                    for x in kin:
                        if x.Kinase_name not in kinlist:
                            kinlist.append(x.Kinase_name)
                    kinasedat[subs+"("+modres+")"]=kinlist
                except:
                    pass


    #SPLITTING KINASES IN DATAFRAME

    kinaselist_df=pandas.DataFrame(list(kinasedat.items()),columns=['substrate','Kinase']) 
    kinaselist_df

    merged_info=pandas.merge(info,kinaselist_df, how="inner", on =["substrate"])
    merged_info

    #SPLITTING KINASES IN DF 

    newDF=pandas.DataFrame(columns=["substrate","control_mean","treatment_mean","fold_change","p-value","ctrlcv","treatcv","log2_fold_change","-log10(pvalue)","Kinase"])
    count=0
    for (i,row) in merged_info.iterrows():
        for kin in row['Kinase']:
            newDF.loc[count]=row
            newDF.loc[count,'Kinase']=kin
            count+=1
    newDF



    #KSEA EQUATION PREPARATION

    #p - mean log2 fold change of ALL phosphosites in dataset
    mean_log2_fold_change=newDF.loc[:,"log2_fold_change"].mean()
    p=mean_log2_fold_change
    p


    #sigma - standard deviation of log2 fold change across ALL phosphosites in dataset
    sd_log2_fold_change=newDF.loc[:,"log2_fold_change"].std()
    sigma=sd_log2_fold_change
    sigma

    #s - mean of log2 fold change of all substrates of the kinase in question
    s_df=pandas.DataFrame({"Kinase":newDF["Kinase"],"log2FC":newDF["log2_fold_change"]})
    newdic={}
    for x in s_df.values:
        if x[0] not in newdic:
            newdic[x[0]]=x[1]
        elif x[0] in newdic:
            newdic[x[0]]+=x[1]


    #m - total number of phosphosites that map to that kinase (total number of times kinase shows in df as a match)
    m=newDF.groupby('Kinase').size()
    m=m.to_dict()


    s_dictvalues={k:newdic[k]/m[k] for k in newdic.keys() & m}




    #CARRYING OUT THE KSEA EQUATION (to find Z-SCORES for each kinase)

    n=math.sqrt(4)
    z=(5-6)*n/(sigma)
    zscore={}
    for x in s_dictvalues.keys():
        if x in m.keys():
            n=math.sqrt(int(m[x]))
            z=(s_dictvalues[x]-p)*n/(sigma)
            zscore[x]=z


    #new data frame with the kinase and its relative score   
    zscore_df=pandas.DataFrame(list(zscore.items()),columns=['Kinase','Relative Activity']) 


    #Z SCORE P VALUES (use function in Scipy Library for python to finf p values for z scores)

    zscorepvalue=[]
    kinasename=[]
    
    for x in zscore_df["Relative Activity"]:
        p_value_mean=norm.sf(abs(x))
        zscorepvalue.append(p_value_mean)
        kinasename.append(zscore_df["Kinase"])

        #fixed values to 3 decimal places 
        
    #add p value column to z score data frame
    zscore_df["p-value"]=zscorepvalue

    zscore_df['p-value']= round(zscore_df['p-value'],3)
    zscore_df['Relative Activity']= round(zscore_df['Relative Activity'],3)
    
    


    #DATAFRAME FOR TOP UP OR DOWNREGULATED KINASES

    zscore2_df=zscore_df.sort_values(by=['Relative Activity'],ascending=False) #sort values - largest to smallest
    zscore3_df=zscore_df.sort_values(by=['Relative Activity'],ascending=True) #sort values - smallest to largest
    zscore4_df=zscore2_df.drop(zscore2_df.index[40:],axis=0) #take top 40 of largest values of relative kinase activity
    zscore5_df=zscore3_df.drop(zscore3_df.index[40:],axis=0) #take top 40 of smallest (most negative) values of relative kinase activity


    #UPREGULATED KINASES

    ax=zscore4_df[["Kinase", "Relative Activity"]].plot(kind='bar', color=[np.where(zscore4_df["p-value"]>0.05, '#EE2E13', '#25BD3A')])
    #colour significant z scores in green, non signoficant in red 

    plt.xticks(rotation=90)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=12)
    plt.rcParams["figure.figsize"] =(15,8)
    plt.rcParams.update({'font.size': 15})


    ax.tick_params(labelsize=10)
    ax.set_xticklabels(zscore4_df["Kinase"], rotation=45)
    ax.set_title("Top 40 Upregulated Kinases' Relative Activity", fontsize=25)
    plt.xlabel('Kinases', fontsize=18)
    plt.ylabel('Relative Kinase Activity (Z-score)', fontsize=18)

    #legend for graph
    green_bars_upreg = mpatches.Patch(color='#25BD3A', label='Significantly Upregulated')
    red_bars_upreg = mpatches.Patch(color='#EE2E13', label='Non-Significantly Upregulated')
    patches=[green_bars_upreg,red_bars_upreg]
    plt.legend(handles=patches)
    
    #SAVE IMAGE FOR UPREGULATED KINASES
    save_results_to = 'static/pp/'
    plt.savefig(save_results_to + 'upreg_zscore_ipa.svg', bbox_inches="tight")
    


    #DOWNREGULATED KINASES

    ax=zscore5_df[["Kinase", "Relative Activity"]].plot(kind='bar', color=[np.where(zscore5_df["p-value"]>0.05, '#EE2E13', '#25BD3A')])
    #significant z scores in green, non significant in red. 

    plt.xticks(rotation=90)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=12)
    plt.rcParams["figure.figsize"] =(15,8)
    plt.rcParams.update({'font.size': 15})


    ax.tick_params(labelsize=10)
    ax.set_xticklabels(zscore5_df["Kinase"], rotation=45)
    ax.set_title("Top 40 Downregulated Kinases' Relative Activity", fontsize=25)
    plt.xlabel('Kinases', fontsize=18)
    plt.ylabel('Relative Kinase Activity (Z-score)', fontsize=18)

    #legend for graph
    green_bars_downreg = mpatches.Patch(color='#25BD3A', label='Significantly Downregulated')
    red_bars_downreg = mpatches.Patch(color='#EE2E13', label='Non-Significantly Downregulated')
    patches=[green_bars_downreg,red_bars_downreg]
    plt.legend(handles=patches)

    #SAVE IMAGE FOR DOWNREGULATED KINASES
    save_results_to = 'static/pp/'
    plt.savefig(save_results_to + 'downreg_zscore_ipa.svg', bbox_inches="tight")
    



    #Z SCORE TABLE 

    def render_mpl_table(data, col_width=10.0, row_height=0.625, font_size=14,
                         header_color='#0489B1', row_colors=['#f1f1f2', 'w'], edge_color='w',
                         bbox=[0, 0, 1, 1], header_columns=0,
                         ax=None, **kwargs):
        if ax is None:
            size = (np.array(data.shape[::-1]) + np.array([0, 1])) * np.array([col_width, row_height])
            fig, ax = plt.subplots(figsize=size)
            ax.axis('off')

        mpl_table = ax.table(cellText=data.values, bbox=bbox, colLabels=data.columns, **kwargs)

        mpl_table.auto_set_font_size(False)
        mpl_table.set_fontsize(font_size)

        for k, cell in  six.iteritems(mpl_table._cells):
            cell.set_edgecolor(edge_color)
            if k[0] == 0 or k[1] < header_columns:
                cell.set_text_props(weight='bold', color='w')
                cell.set_facecolor(header_color)
            else:
                cell.set_facecolor(row_colors[k[0]%len(row_colors) ])
        return ax

    render_mpl_table(zscore_df, header_columns=1, col_width=5.0)
    #col_width changes column width

    #SAVE Z SCORE TABLE
    save_results_to = 'static/pp/'
    plt.savefig(save_results_to + 'score_table_ipa.svg', bbox_inches="tight")







