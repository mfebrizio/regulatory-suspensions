install.packages("writerxl")
library("writexl")
library("tidyverse")
setwd("C:/Users/16192/OneDrive/")
library(readxl)

#Sampling the suspended rules

#generate random unique numbers
#sample 50% for each President

df <- read_excel("Suspended_Rules.xlsx")
sum(df$susp[df$president_id == "george-w-bush"]) #87 so 44
sum(df$susp[df$president_id == "barack-obama"]) #27 so 14
sum(df$susp[df$president_id == "donald-trump"]) #70 so 35
sum(df$susp[df$president_id == "joe-biden"]) #43 so 22

which(df$president_id == "george-w-bush") #1 to 87
which(df$president_id == "barack-obama") #88 to 114
which(df$president_id == "donald-trump") #115 to 184
which(df$president_id == "joe-biden") #185 to 227

#sample will contain 115 rules

set.seed(3555)
rand1 <- sample(x = 1:87, size = 44, replace = FALSE)
rand1 <- data.frame(rand1)
colnames(rand1) <- c("rand")
set.seed(3555)
rand2 <- sample(x = 88:114, size = 14, replace = FALSE)
rand2 <- data.frame(rand2)
colnames(rand2) <- c("rand")
set.seed(3555)
rand3 <- sample(x = 115:184, size = 35, replace = FALSE)
rand3 <- data.frame(rand3)
colnames(rand3) <- c("rand")
set.seed(3555)
rand4 <- sample(x = 185:227, size = 22, replace = FALSE)
rand4 <- data.frame(rand4)
colnames(rand4) <- c("rand")

rand <- rbind(rand1, rand2, rand3, rand4)

#subset suspended rules to sample
sample <- df[rand$rand,]

#export sample

write_xlsx(sample, "Sample_Suspended_Rules.xlsx")
