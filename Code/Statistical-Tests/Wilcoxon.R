library(effsize)


raw<-read.csv("../Data/Wilcoxon/raw.csv",header=TRUE)
abstracted<-read.csv("../Data/Wilcoxon/abstracted.csv",header=TRUE)

res=list(Dataset=c(),Wilcoxon.p=c())

########### COMMENT when running the Wilcoxon test for the ROUGE-LCS score ###########


# res$Dataset=c(res$Dataset,as.character("../Data/Wilcoxon/raw.csv"))
# res$Wilcoxon.p=c(res$Wilcoxon.p, wilcox.test(raw$B4_T5,raw$B4_NGRAM,alternative="two.side",paired=TRUE)$p.value)


# res$Dataset=c(res$Dataset,as.character("../Data/Wilcoxon/abstracted.csv"))
# res$Wilcoxon.p=c(res$Wilcoxon.p, wilcox.test(abstracted$B4_T5,abstracted$B4_NGRAM,alternative="two.side",paired=TRUE)$p.value)

# cliff.delta(abstracted$B4_T5,abstracted$B4_NGRAM)
# cliff.delta(raw$B4_T5,raw$B4_NGRAM)

########### COMMENT when running the Wilcoxon test for the BLEU-4 score ###########
res$Dataset=c(res$Dataset,as.character("../Data/Wilcoxon/raw.csv"))
res$Wilcoxon.p=c(res$Wilcoxon.p, wilcox.test(raw$ROUGE_T5,raw$ROUGE_NGRAM,alternative="two.side",paired=TRUE)$p.value)

res$Dataset=c(res$Dataset,as.character("../Data/Wilcoxon/abstracted.csv"))
res$Wilcoxon.p=c(res$Wilcoxon.p, wilcox.test(abstracted$ROUGE_T5,abstracted$ROUGE_NGRAM,alternative="two.side",paired=TRUE)$p.value)

cliff.delta(abstracted$ROUGE_T5,abstracted$ROUGE_NGRAM)
cliff.delta(raw$ROUGE_T5,raw$ROUGE_NGRAM)


res=data.frame(res)
res$Wilcoxon.p=p.adjust(res$Wilcoxon.p,method="holm")
print(res)





