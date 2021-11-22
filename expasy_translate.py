# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import csv, sys, getopt, requests


inputfile = ''
outputfile = ''
try:
   opts, args = getopt.getopt(sys.argv[1:],"hi:o:",["ifile=","ofile="])
except getopt.GetoptError:
   print('expasy_translate.py -i <inputfile> -o <outputfile>')
   sys.exit(2)
for opt, arg in opts:
   if opt == '-h':
      print('expasy_translate.py -i <inputfile> -o <outputfile>')
      sys.exit()
   elif opt in ("-i", "--ifile"):
      inputfile = arg
   elif opt in ("-o", "--ofile"):
      outputfile = arg
   else:
      sys.exit(2)
     
      
dnaList = []

with open(inputfile) as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        dnaList.append(row[0])


protList = []

for DNAseq in dnaList:
    response = requests.post("https://web.expasy.org/cgi-bin/translate/dna2aa.cgi", data={"dna_sequence":DNAseq, "output_format":"fasta"})
    resp_list = response.text.splitlines()
    keep = 0
    protStr=""
    for str_prot in resp_list:
        if str_prot.find("5'3' Frame 2") > 0:
            keep=0
        if keep==1:
            protStr += str_prot
        if str_prot.find("5'3' Frame 1") > 0:
            keep=1
    protList.append(protStr)


with open(outputfile,'w') as csvOutput:
    for protRow in protList:
        csvOutput.write(protRow)
        csvOutput.write("\n")
        
csvOutput.close()