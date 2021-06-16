install.packages("writerxl")
library("writexl")
library("tidyverse")
setwd("C:/Users/16192/OneDrive/")
library(readxl)

#Sampling the suspended rules

#generate random unique numbers
#sample 5% for each President

df <- read_excel("Raw_Rules.xlsx")
sum(df$president_id == "george-w-bush") #953 so 48
sum(df$president_id == "barack-obama") #881 so 45
sum(df$president_id == "donald-trump") #727 so 37
sum(df$president_id == "joe-biden") #814 so 41

which(df$president_id == "george-w-bush") #1 to 953
which(df$president_id == "barack-obama") #954 to 1834
which(df$president_id == "donald-trump") #1835 to 2561
which(df$president_id == "joe-biden") #2562 to 3375

#sample will contain 171 rules

set.seed(3555)
rand1 <- sample(x = 1:953, size = 48, replace = FALSE)
rand1 <- data.frame(rand1)
colnames(rand1) <- c("rand")
set.seed(3555)
rand2 <- sample(x = 954:1834, size = 45, replace = FALSE)
rand2 <- data.frame(rand2)
colnames(rand2) <- c("rand")
set.seed(3555)
rand3 <- sample(x = 1835:2561, size = 37, replace = FALSE)
rand3 <- data.frame(rand3)
colnames(rand3) <- c("rand")
set.seed(3555)
rand4 <- sample(x = 2562:3375, size = 41, replace = FALSE)
rand4 <- data.frame(rand4)
colnames(rand4) <- c("rand")

rand <- rbind(rand1, rand2, rand3, rand4)

#subset suspended rules to sample
sample <- df[rand$rand,]

#export sample


write_xlsx(sample, "Sample_Raw_Rules.xlsx")
