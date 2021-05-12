# Written by Casey Helgeson (Orchid id 0000-0001-5333-9954) to transform and plot data generated through qualitative data analysis of interview transcripts. This code reads in a set of .ann files produced by the Brat text annotation tool (one file per transcript). The code also reads in a personnel file with some information about each interviewee in order to subdivide the transcript data according to personnel categories.

# This code doesn't need any special packages.
# This code was tested and confirmed to work with R version 4.0.3 (2020-10-10), nickname "Bunny-Wunnies Freak Out".

# set working directory to the "inputData" folder.

# import personnel data
peeps<-read.csv("./personnel_blinded.csv", header=TRUE, sep=",")

# below are the code labels from our QDA codebook
# to use this with your data, you'll need to replace the "entities" and "attributes" lists below with those used in your Brat coding
entities<-c(
  "motivation", 
  "design", 
  "collaboration", 
  "research", 
  "mentoring", 
  "exposure", 
  "infrastructure", 
  "code")

attributes<-c(
  "uncertainty", 
  "values", 
  "decision", 
  "skill_sets", 
  "disciplines", 
  "new_topic", 
  "stakeholders", 
  "sustained")

# these are longer names for the attribute codes 
# this is used only to draw from for plot labels
attributes.long<-c(
  "treatment of uncertainties", 
  "attention to values", 
  "decision-relevance", 
  "skill_sets", 
  "bridging disciplines", 
  "new_topic", 
  "stakeholders", 
  "sustained")

# read in the .ann files
file.names <- list.files(path="./brat_files", full.names=T)
annotations<-list()
for (i in seq_along(file.names)) {
  annotations[[i]] <- read.table(file.names[i], header=FALSE, fill=TRUE)[,1:3]
}

# make a second list to hold intermediate results of transforming the .ann data
# the code below makes a entities-by-attributes matrix for each transcript, displaying which entities and attributes are present in the transcript and which entities are coded on top of which attributes. This is overkill for present purposes, since we only visualize the attributes data here.
presence<-list()

for(i in 1:29){
  presence[[i]]<-matrix(FALSE,nrow=length(attributes)+1,ncol=length(entities)+1)# +1 is for the "marginals"
  temp.ann<-annotations[[i]]# just to make the following a bit more readable
  
  for(j in which(temp.ann[,2]%in%attributes)){# expression inside which gives row numbers of attribute annotations
    presence[[i]][
      which(temp.ann[j,2]==attributes),
      which(temp.ann[match(temp.ann[j,3],temp.ann[,1]),2]==entities)
      ]<-TRUE
  }
  presence[[i]][9,1:8]<-entities%in%temp.ann[,2] # calculate entity "marginals"
  presence[[i]][1:8,9]<-attributes%in%temp.ann[,2] #calculate attribute "marginals"
}
# now sum across transcripts
sums<-Reduce('+',presence)

### make subsetting tools
faculty<-which(peeps$Role==1 | peeps$Role==2)
postdocs<-which(peeps$Role==3)

### use subsetting tools to count code instances within subsets of the transcripts
facultysums<-Reduce('+', presence[faculty])/length(faculty)
postdocsums<-Reduce('+', presence[postdocs])/length(postdocs)

### bind the results to make plotting easier
compare.faculty.postdocs<-rbind(postdocsums[1:8,9],facultysums[1:8,9])

### load color pallette
paired<-c(	# 12-member paired palette from RColorBrewer
  "#A6CEE3", #blue
  "#1F78B4", #blue 
  "#B2DF8A", #green
  "#33A02C", #green
  "#FB9A99", #red
  "#E31A1C", #red
  
  "#FDBF6F", #orange
  "#FF7F00", #orange
  "#CAB2D6", #purple
  "#6A3D9A", #purple
  "#FFFF99", #brown
  "#B15928"  #brown
)

## makes a two-panel plot showing the fraction of transcripts that contain each entity
## second panel divides faculty versus postdocs (this info came from the personnel file)

order<-c(2,1,3,5) # tool for subsetting from full set of attributes 
pdf("./../outputs/Figure_1.pdf", height=4.48, width=8)
#quartz(height=4.85, width=8) # old height=6
  par(mfrow=c(2,1),mar=c(3.5,11,0,2), oma=c(4,1,1,1), cex=1)# bottom, left, top, right

  barplot(sums[order,9]/29, names.arg=attributes.long[order], horiz=TRUE, xaxt="n",
        col="gray30", border=FALSE, las=2, xlim=c(0,.7), space=0.55)
  axis(1)
  legend("bottomright", legend=c("all interviews (n=29)"), 
       fill="gray30", border="gray30", bty="n",inset=c(-.015,-.03))

  barplot(compare.faculty.postdocs[,order], beside=TRUE, horiz=TRUE, col=paired[1:2], border=FALSE, 
        names.arg=attributes.long[order], las=2, xaxt="n", xlim=c(0,.7))
  title(xlab="frequency", line=2.5)
  axis(1)
  legend("bottomright", legend=c("faculty (n=15)", "postdocs (n=14)"), 
       fill=paired[2:1], border=paired[2:1], bty="n", inset=c(-.015,-.03))

dev.off() #end Figure 1


