# Written by Casey Helgeson (Orchid id 0000-0001-5333-9954) to tabulate and plot quantitative response-scale data from an interview study. The code also reads in two other files containing information about each participant to be associated with their interview responses.

# this code uses the plotrix library
# This code was tested and confirmed to work with R version 4.0.3 (2020-10-10), nickname "Bunny-Wunnies Freak Out"

# set working directory to the "inputData" folder.

library(plotrix)
# import files
likert.raw<-read.csv("./response_scale.csv", header=TRUE, sep=",") # the main data file, containing participants' quantitative responses
personnel<-read.csv("./personnel_blinded.csv", header=TRUE, sep=",") # supplementary file, contining info on participants
coauthorship<-read.csv("./coauthorship.csv", header=TRUE, sep=",") # supplementary file, containing coauthorship indices calculated for each participant

# some people gave ranges instead of integers. convert ranges to midpoints
mo.u<-(likert.raw$mo.u.bottom+likert.raw$mo.u.top)/2 # multi-objective, understanding
mo.i<-(likert.raw$mo.i.bottom+likert.raw$mo.i.top)/2 # multi-objective, importance
du.u<-(likert.raw$du.u.bottom+likert.raw$du.u.top)/2 # deep uncertainty, understanding
du.i<-(likert.raw$du.i.bottom+likert.raw$du.i.top)/2 # deep uncertainty, importance
ee.u<-(likert.raw$ee.u.bottom+likert.raw$ee.u.top)/2 # ethical-epistemic, understanding
ee.i<-(likert.raw$ee.i.bottom+likert.raw$ee.i.top)/2 # ethical-epistemic, importance

#du.u<-du.u[which(du.i!="NA")] # activate to exclude participants who provided no importance response
#mo.u<-mo.u[which(mo.i!="NA")] # activate to exclude participants who provided no importance response
#ee.u<-ee.u[which(ee.i!="NA")] # activate to exclude participants who provided no importance response

##################### 
##################### FIGURE 2
# calculate means to be superimposed on histograms
means<-matrix(nrow=2,ncol=3, rev(c(
  mean(mo.u, na.rm=TRUE),
  mean(mo.i, na.rm=TRUE),
  mean(du.u, na.rm=TRUE),
  mean(du.i, na.rm=TRUE),
  mean(ee.u, na.rm=TRUE),
  mean(ee.i, na.rm=TRUE)))
)

## conversion of some responses to midpoints (above) creates data points that don't fit nicely into a histogram
## decompose interval midpoints into weighted integer responses so they can go in the histogram

# multi-objective understanding
multi.u<-table(factor(as.integer(mo.u), levels=1:5))
original.multi.u<-multi.u # make a copy for diagnostic comparison with what the for loop does
multi.u.diff<-mo.u-as.integer(mo.u)
for (i in which(multi.u.diff!=0)){
multi.u[as.integer(mo.u)[i]]<-multi.u[as.integer(mo.u)[i]]-multi.u.diff[i]
multi.u[as.integer(mo.u)[i]+1]<-multi.u[as.integer(mo.u)[i]+1]+multi.u.diff[i]
}

#multi-objective importance
multi.i<-table(factor(as.integer(mo.i), levels=1:5))
original.multi.i<-multi.i # make a copy for diagnostic comparison with what the for loop does
multi.i.diff<-mo.i-as.integer(mo.i)
for (i in which(multi.i.diff!=0)){
  multi.i[as.integer(mo.i)[i]]<-multi.i[as.integer(mo.i)[i]]-multi.i.diff[i]
  multi.i[as.integer(mo.i)[i]+1]<-multi.i[as.integer(mo.i)[i]+1]+multi.i.diff[i]
}

# deep uncertainty understanding
deep.u<-table(factor(as.integer(du.u), levels=1:5))
original.deep.u<-deep.u # make a copy for diagnostic comparison with what the for loop does
deep.u.diff<-du.u-as.integer(du.u)
for (i in which(deep.u.diff!=0)){
  deep.u[as.integer(du.u)[i]]<-deep.u[as.integer(du.u)[i]]-deep.u.diff[i]
  deep.u[as.integer(du.u)[i]+1]<-deep.u[as.integer(du.u)[i]+1]+deep.u.diff[i]
}

# deep uncertainty importance
deep.i<-table(factor(as.integer(du.i), levels=1:5))
original.deep.i<-deep.i # make a copy for diagnostic comparison with what the for loop does
deep.i.diff<-du.i-as.integer(du.i)
for (i in which(deep.i.diff!=0)){
  deep.i[as.integer(du.i)[i]]<-deep.i[as.integer(du.i)[i]]-deep.i.diff[i]
  deep.i[as.integer(du.i)[i]+1]<-deep.i[as.integer(du.i)[i]+1]+deep.i.diff[i]
}

# coupled ee understanding
coupled.u<-table(factor(as.integer(ee.u), levels=1:5))
original.coupled.u<-coupled.u # make a copy for diagnostic comparison with what the for loop does
coupled.u.diff<-ee.u-as.integer(ee.u)
for (i in which(coupled.u.diff!=0)){
  coupled.u[as.integer(ee.u)[i]]<-coupled.u[as.integer(ee.u)[i]]-coupled.u.diff[i]
  coupled.u[as.integer(ee.u)[i]+1]<-coupled.u[as.integer(ee.u)[i]+1]+coupled.u.diff[i]
}

# coupled ee importance
coupled.i<-table(factor(as.integer(ee.i), levels=1:5))
original.coupled.i<-coupled.i # make a copy for diagnostic comparison with what the for loop does
coupled.i.diff<-ee.i-as.integer(ee.i)
for (i in which(coupled.i.diff!=0)){
  coupled.i[as.integer(ee.i)[i]]<-coupled.i[as.integer(ee.i)[i]]-coupled.i.diff[i]
  coupled.i[as.integer(ee.i)[i]+1]<-coupled.i[as.integer(ee.i)[i]+1]+coupled.i.diff[i]
}

##### make plot 
#quartz(height=5, width=4)
pdf("./../outputs/Figure_2.pdf", height=5, width=4)
par(cex=1, xpd=TRUE, mfrow=c(4,1), mar=c(2,5,0.7,0), oma=c(4,4,0,4)) # note to self: "mar" is inner and goes clockwise from bottom; "oma" is outer margins

# legend
plot.new()
legend(-.2,.3, legend=c("level of understanding (self assessed)","importance to achieving research goals"), 
       fill=c("#CAB2D6","white"), border=c("#CAB2D6","black"), bty="n", xpd=TRUE)

# panel a
barplot(multi.u/sum(multi.u), space=0, col="#CAB2D6", border="#CAB2D6", xlim=c(0,6), ylim=c(0,.65), xpd=FALSE, ylab="frequency", names.arg=FALSE, axes=FALSE)
lines(0:5, c(multi.i/sum(multi.i),0), type="s", lwd=2, col="black", xpd=FALSE, xlim=c(.5, 5.5))
points(means[,3]-.5,c(0,0),col=c("black","purple"), lwd=1.4, cex=1.1, pch=c(1,19))
axis(2,at=c(0,.1, .2,.3,.4,.5,.6), labels=c("0","",".2","",".4","",".6"), tick=TRUE)
text(-.15,.51, "multi-objective robust \ndecision analysis", cex=.9, pos=4)
mtext("a", side =3, line=-.35, cex=.88, font=2, at=-1.3)

# panel b
barplot(deep.u/sum(deep.u), space=0, col="#CAB2D6", border="#CAB2D6", xlim=c(0,6), ylim=c(0,.65), xpd=FALSE, ylab="frequency", names.arg=FALSE, axes=FALSE)
lines(0:5, c(deep.i/sum(deep.i),0), type="s", lwd=2, col="black", xlim=c(.5, 5.5), xpd=FALSE)
points(means[,2]-.5,c(0,0),col=c("black","purple"), lwd=1.4, cex=1.1, pch=c(1,19))
axis(2,at=c(0,.1, .2,.3,.4,.5,.6), labels=c("0","",".2","",".4","",".6"), tick=TRUE)
text(-.15,.51, "identify & characterize \ndeep uncertainties", cex=.9, pos=4)
mtext("b", side =3, line=-.35, cex=.88, font=2, at=-1.3)

# panel c
barplot(coupled.u/sum(coupled.u), space=0, col="#CAB2D6", border="#CAB2D6", xlim=c(0,6), ylim=c(0,.65), xpd=TRUE, ylab="frequency", names.arg=FALSE, axes=FALSE)
lines(0:5, c(coupled.i/sum(coupled.i),0), type="s", lwd=2, col="black", xlim=c(.5, 5.5), xpd=FALSE)
points(means[,1]-.5,c(0,0),col=c("black","purple"), lwd=1.4, cex=1.1, pch=c(1,19))
axis(2,at=c(0,.1, .2,.3,.4,.5,.6), labels=c("0","",".2","",".4","",".6"), tick=TRUE)
axis(1,at=c(.5,1.5,2.5,3.5,4.5), labels=c(1,2,3,4,5), tick=FALSE, line=-.7)
text(-.15,.51, "coupled ethical- \nepistemic analysis", cex=.9, pos=4)
mtext("c", side =3, line=-.35, cex=.88, font=2, at=-1.3)

mtext("rating scale: 1=very low, 5=very high", side =1, at=2.47, line=1.6, cex=.7)
dev.off()

####################
#################### FIGURE 3
# code below assumes participants (rows) are in the same order in the three files imported at the top of this script
# participant identifiers are present in each file (column name: code) to verify this

# calculate individuals' mean response across three understanding scores
y<-rowMeans(cbind(mo.u,du.u,ee.u), na.rm=TRUE)

# create subsetting tools
faculty<-likert.raw$fac.post==1
postdocs<-likert.raw$fac.post==2

faculty.mPM<-faculty    #mPM stands for "minus project manager"
PM.id<-which.max(personnel$months)
faculty.mPM[PM.id]<-FALSE 

faculty.mPI<-faculty    #mPI stands for "minus principal investigator"
PI.id<-which.max(coauthorship$department)
faculty.mPI[PI.id]<-FALSE

###### create explanatory variables and save regression results
# 1st explanatory variable (x): funding
x<-personnel$months
lin.funds.fac<-lm(y[faculty]~x[faculty])
lin.funds.fac.mPM<-lm(y[faculty.mPM]~x[faculty.mPM])
lin.funds.post<-lm(y[postdocs]~x[postdocs])

# calculate confidence intervals reported in Table 2 caption
#confint(lin.funds.fac, level=0.90)
confint(lin.funds.fac.mPM, level=0.90)
confint(lin.funds.post, level=0.90)

# 2nd explanatory variable (x2): attendance
x2<-personnel$meetings+personnel$sessions
lin.attend.fac<-lm(y[faculty]~x2[faculty])
lin.attend.post<-lm(y[postdocs]~x2[postdocs])

# calculate confidence intervals reported in Table 2 caption
confint(lin.attend.fac, level=0.90)
confint(lin.attend.post, level=0.90)

# 3rd explanatory variable (x3): co-authorship
x3<-coauthorship$department
lin.coauthor.fac<-lm(y[faculty]~x3[faculty])
lin.coauthor.fac.mPI<-lm(y[faculty.mPI]~x3[faculty.mPI])
lin.coauthor.post<-lm(y[postdocs]~x3[postdocs])

# 3rd explanatory variable (x3): co-authorship # again, now using subjective disciplines categorization
x3.alt<-coauthorship$discipline
lin.coauthor.alt.fac<-lm(y[faculty]~x3.alt[faculty])
lin.coauthor.alt.fac.mPI<-lm(y[faculty.mPI]~x3.alt[faculty.mPI])
lin.coauthor.alt.post<-lm(y[postdocs]~x3.alt[postdocs])

# calculate confidence intervals reported in Table 2 caption
#confint(lin.coauthor.fac, level=0.90)
confint(lin.coauthor.fac.mPI, level=0.90)
confint(lin.coauthor.alt.fac.mPI, level=0.90)
confint(lin.coauthor.post, level=0.90)
confint(lin.coauthor.alt.post, level=0.90)

##### make plot
pdf("./../outputs/Figure_3.pdf", height=5, width=6.4)
par(mfrow=c(2,3), mar=c(4,3.25,3,0), oma=c(1,2,0,2), cex.main=1.1)
overlay<-"olivedrab3" # define the color for the discipline-based coauthorship points in panels c and f

# panel a
plot(x[faculty.mPM],y[faculty.mPM], pch=15, cex=1, main="a. funding (faculty)", xlab="", ylab="", ylim=c(1,5), xlim=c(.5,28.5),
     #xlim=c(0.8,14.6), 
     xaxt="n")
abline(lin.funds.fac.mPM)
points(x[PM.id]-15,y[PM.id], pch=15, col="gray45")

text(x[which.max(personnel$months)]-15.1, y[which.max(personnel$months)]+.27, labels="PM", cex=.9, col="gray45") # add project manager separately
text(19, 1.9, labels="  not included \nin regression", cex=1, col="gray45") # add text to plot
segments(22,2.3, x[PM.id]-15.15,y[PM.id]-.17,  lwd=.8, col="gray45")

axis(1, at=c(0,5,10,15,20,25), labels=c(0,5,10,15,20,40))
axis.break(axis=1, 22.5, style="slash", brw=.036)

title(ylab="mean understanding", line=2.5, cex.lab=1)
title(xlab="funding (months)", line=2.25, cex.lab=1)

# panel b
plot(x2[faculty],y[faculty], pch=15, cex=1, main="b. attendance (faculty)", xlab="", ylab="",yaxt="n", ylim=c(1,5), xlim=c(0,10))
abline(lin.attend.fac)

title(xlab="project events attended (#)", line=2.25, cex.lab=1)

# panel c
plot(x3[faculty.mPI],y[faculty.mPI], pch=15, cex=1, main="c. coauthorship (faculty)", xlab="", ylab="",yaxt="n", ylim=c(1,5), xlim=c(0,26), xaxt="no")
abline(lin.coauthor.fac.mPI)

points(x3.alt[faculty.mPI],y[faculty.mPI], cex=2, main="c. coauthorship (faculty)", xlab="", ylab="",yaxt="n", ylim=c(1,5), col=overlay)
abline(lin.coauthor.alt.fac.mPI, col=overlay)

points(x3[PI.id]-43, y[PI.id], pch=15, col="gray50") # add PI separately
text(x3[PI.id]-43.1, y[PI.id]+.26, labels="PI", cex=.9, col="gray50")
text(19.5, 2.8, labels="  not included \nin regression", cex=1, col="gray50")
segments(23.5,3.3, x3[PI.id]-43.3, y[PI.id]-.17,  lwd=.8, col="gray50")

legend("bottomright", legend=c("department", "discipline"), col=c("black",overlay), pch=c(15,1), pt.cex=c(1,1.6))
title(xlab="coauthorship outside dept./disc.", line=2.25, cex.lab=1)

axis(1, at=c(0,5,10,15,20,25), labels=c(0,5,10,15,20,68))
axis.break(axis=1, 23, style="slash", brw=.036)

# panel d
plot(x[postdocs],y[postdocs], pch=16, cex=1.1, xlab="", ylab="", ylim=c(1,5), xlim=c(.5,28.5), main="d. funding (postdocs)")
abline(lin.funds.post)

title(ylab="mean understanding", line=2.5, cex.lab=1)
title(xlab="funding (months)", line=2.25, cex.lab=1)

# panel e
plot(x2[postdocs],y[postdocs], pch=16, cex=1.1, xlab="", ylab="", yaxt="n", ylim=c(1,5), xlim=c(0,10), main="e. attendance (postdocs)")
abline(lin.attend.post)

title(xlab="project events attended (#)", line=2.25, cex.lab=1)

# panel f
plot(x3[postdocs],y[postdocs], pch=16, cex=1.1, xlab="", ylab="", yaxt="n", ylim=c(1,5), main="f. coauthorship (postdocs)", xlim=c(0,25))
#xlim=c(0,15.2))
abline(lin.coauthor.post)
points(x3.alt[postdocs],y[postdocs], cex=2, xlab="", ylab="", yaxt="n", ylim=c(1,5), main="f. coauthorship (postdocs)", col=overlay)
abline(lin.coauthor.alt.post, col=overlay)

legend("bottomright", legend=c("department", "discipline"), col=c("black",overlay), pch=c(16,1), pt.cex=c(1,1.6))
title(xlab="coauthorship outside dept./disc.", line=2.25, cex.lab=1)
dev.off()

####################
#################### FIGURE SM 1
# plot

pdf("./../outputs/Figure_SM1.pdf", width=8, height=6.5)
par(
  mfrow=c(2,1),  
  mar=c(4,3.25,3,0),
  oma=c(1,2,0,2),
  cex.main=1.1
)

plot(x[faculty],y[faculty], pch=15, cex=1, main="a*.  funding (faculty)", xlab="", ylab="", ylim=c(1,5))
abline(lin.funds.fac.mPM)
abline(lin.funds.fac, lty=2)

text(x[PM.id], y[PM.id]-.4, labels="PM", cex=.9)
title(ylab="mean understanding", line=2.5, cex.lab=1)
title(xlab="funding (months)", line=2.25, cex.lab=1)
legend("bottomright", legend=c("regression without Project Manager", "regression with Project Manager"), col=c("black","black"), lty=c(1,2), box.lty=0)


plot(x3[faculty],y[faculty], pch=15, cex=1, main="c*.  coauthorship (faculty)", xlab="", ylab="", ylim=c(1,5))
abline(lin.coauthor.fac.mPI)
abline(lin.coauthor.fac, lty=2)
points(x3.alt[faculty],y[faculty], cex=2, main="c. coauthorship (faculty)", xlab="", ylab="",yaxt="n", ylim=c(1,5), col=overlay, lwd=1.4)
abline(lin.coauthor.alt.fac.mPI, col=overlay, lwd=1.2)
abline(lin.coauthor.alt.fac, col=overlay, lty=2, lwd=1.3)

text(x3[PI.id], y[PI.id]-.4, labels="PI", cex=.9)  

legend("bottomleft", legend=c("department", "discipline"), col=c("black",overlay), pch=c(15,1), pt.cex=c(1,1.6), inset=c(.24,0), box.lty=0)
legend("bottomright", legend=c("regression without Principal Investigator", "regression with Principal Investigator"), col=c("black","black"), lty=c(1,2), box.lty=0)
title(ylab="mean understanding", line=2.5, cex.lab=1)
title(xlab="index of coauthorship outside department / discipline", line=2.25, cex.lab=1)
dev.off()

