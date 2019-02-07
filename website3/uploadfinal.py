import os
from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
import pandas
import urllib3
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.plotting import _converter

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

    info=info[~info['substrate'].str.contains("None")]
    #removes all substrates with no reported phosphosite in tbhe dataset (invert (~) operator acts like a 'not' for boolean data)

    info=info[~info['substrate'].str.contains("\(M")]
    #remove all methionines -regex

    info['log2_fold_change'] = np.log2(info['az20_fold_change'])
    #log 2 of fold change

    info['-log10(pvalue)'] = np.log10(info['az20_p-value'])
    info.loc[:, '-log10(pvalue)'] = info['-log10(pvalue)'] * -1
    #-log10 of pvalue

    #info
    #get log2 of the fold change and -log10 of pvalue and make volcanoe plot

    colours = np.where((info["az20_fold_change"]>1) | (info["az20_p-value"]<0.05) ,'red', 'blue')
#colour code for all points where fold change is greater than 1 AND pvalue is less than 0.05 (for RAW data)

    info.plot.scatter(x='log2_fold_change', y='-log10(pvalue)', c=colours)

    save_results_to = 'static/pp/'
    plt.savefig(save_results_to + 'fold_change.svg', dpi = 1500)
