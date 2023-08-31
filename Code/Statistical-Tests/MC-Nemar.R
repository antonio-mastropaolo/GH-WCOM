library(exact2x2)
library(effsize)
library(xtable)

####### UNCOMMENT to run the statistical tests for the several pre-training strategies #######

# res=list(Dataset=c(),McNemar.p=c(),McNemar.OR=c())
# d<-"../Data/MCNemar/PT-Strategies/abstracted-developer.csv"
# t<-read.csv(d)

# m=mcnemar.exact(t$NO_PT,t$ENGLISH_PT)
# res$Dataset=c(res$Dataset,as.character(d))
# res$McNemar.p=c(res$McNemar.p, m$p.value)
# res$McNemar.OR=c(res$McNemar.OR,m$estimate)

# m=mcnemar.exact(t$YAML_PT,t$ENGLISH_PT)
# res$Dataset=c(res$Dataset,as.character(d))
# res$McNemar.p=c(res$McNemar.p, m$p.value)
# res$McNemar.OR=c(res$McNemar.OR,m$estimate)

# m=mcnemar.exact(t$YAML_ENGLISH_PT,t$ENGLISH_PT)
# res$Dataset=c(res$Dataset,as.character(d))
# res$McNemar.p=c(res$McNemar.p, m$p.value)
# res$McNemar.OR=c(res$McNemar.OR,m$estimate)

# m=mcnemar.exact(t$YAML_PT,t$YAML_ENGLISH_PT)
# res$Dataset=c(res$Dataset,as.character(d))
# res$McNemar.p=c(res$McNemar.p, m$p.value)
# res$McNemar.OR=c(res$McNemar.OR,m$estimate)


# res=data.frame(res)
# #p-value adjustment
# res$McNemar.p=p.adjust(res$McNemar.p,method="holm")
# print(res)

####### UNCOMMENT to run the statistical tests which compare GH-WCOM against the baseline (ngram) #######


res=list(Dataset=c(),McNemar.p=c(),McNemar.OR=c())
abstracted<-read.csv("../Data/MCNemar/approach-ngram-abstracted.csv",header=TRUE)
raw<-read.csv("../Data/MCNemar/approach-ngram-raw.csv",header=TRUE)


m=mcnemar.exact(raw$NGRAM,raw$T5)
res$Dataset=c(res$Dataset,as.character("../Data/MCNemar/approach-ngram-abstracted.csv"))
res$McNemar.p=c(res$McNemar.p, m$p.value)
res$McNemar.OR=c(res$McNemar.OR,m$estimate)

m=mcnemar.exact(abstracted$NGRAM,abstracted$T5)
res$Dataset=c(res$Dataset,as.character("../Data/MCNemar/approach-ngram-raw.csv"))
res$McNemar.p=c(res$McNemar.p, m$p.value)
res$McNemar.OR=c(res$McNemar.OR,m$estimate)

res=data.frame(res)
#p-value adjustment
res$McNemar.p=p.adjust(res$McNemar.p,method="holm")
print(res)
