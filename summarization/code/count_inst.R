# Written by Casey Helgeson (Orchid id 0000-0001-5333-9954) to calculate some statistics of a set of publications produced by a multi-institution research network. This code counts how many publications each institution coauthored and also how many publications were coauthored across each pair of institutions.

# This code doesn't need any special packages.
# This code was tested and confirmed to work with R version 4.0.3 (2020-10-10), nickname "Bunny-Wunnies Freak Out".

# set working directory to the "inputData" folder.

# This code uses one data file: by.institution.csv. 
# by.institution.csv has one row for each publication and one column for each institution.
# Looking down a column, the "1"s indicate which publicaitons were coauthored by someone from that institution. 
# by.institutions.csv is derived from the pubstats output pubstats2.csv by extracting n columns (n=number of institutions) and replacing column names with pseudonyms

# function "compare" outputs how many pubs feature authors from institutions a and b
compare<-function(a,b){sum(by.institution[a]==TRUE & by.institution[b]==TRUE)}

# read in the data file
by.institution<-read.csv("./by_institution.csv", header=TRUE, sep=",")

# count total pubs coauthored by each institution
m<-ncol(by.institution)   # count how many institutions
totals<-vector(length=m)  # create recepticle for totals
for (k in 1:m){
  totals[k]<-sum(by.institution[k])
}

# now count pubs coauthored across each pair of institutions
rainbows<-matrix(nrow=m,ncol=m) # make recepticle to hold the cross-tabulations
# now fill with counts using the compare function. resulting matrix will be symmetric.
for (i in 1:m){
  for (j in 1:m){
    rainbows[i,j]<-compare(order(totals,decreasing=TRUE)[i],order(totals,decreasing=TRUE)[j])
  }  
}

write.csv(rainbows, "./../outputs/rainbows.csv", row.names = TRUE)



## below is the code for making the annonomized data file "by.institution.csv" from the output "pubstats2" of the python package pubstats:
## pubs<-read.csv("pubstats2_March_2020.csv", header=TRUE, sep=",")
## pubs[is.na(pubs)] = 0    # replace NA with 0
## by.institution<-pubs[,98:105]  # extract columns with institutional authorship data
## colnames(by.institution)<- c("do","re","mi", "fa", "sol", "la", "ti", "du")    # replace institution names with pseudonyms
## write.csv(by.institution,"Path where you'd like to export the DataFrame\\by.institution.csv", row.names = FALSE)


