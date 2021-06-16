install.packages("writerxl")
library("writexl")
library("tidyverse")
setwd("C:/Users/16192/OneDrive/")
library(readxl)

df <- read_excel("Raw_Rules.xlsx")
df <- df[df$susp == 0,] #subset to all the non-suspensions
write_xlsx(df, "Non_Suspended_Rules.xlsx")

#Sampling the non suspended rules

#generate random unique numbers
#sample 5% for each President

sum(df$president_id == "george-w-bush") #866 so 44
sum(df$president_id == "barack-obama") #854 so 43
sum(df$president_id == "donald-trump") #657 so 33
sum(df$president_id == "joe-biden") #771 so 39

which(df$president_id == "george-w-bush") #1 to 866
which(df$president_id == "barack-obama") #867 to 1720
which(df$president_id == "donald-trump") #1721 to 2377
which(df$president_id == "joe-biden") #2378 to 3148

#sample will contain 159 rules

set.seed(3555)
rand1 <- sample(x = 1:866, size = 44, replace = FALSE)
rand1 <- data.frame(rand1)
colnames(rand1) <- c("rand")
set.seed(3555)
rand2 <- sample(x = 867:1720, size = 43, replace = FALSE)
rand2 <- data.frame(rand2)
colnames(rand2) <- c("rand")
set.seed(3555)
rand3 <- sample(x = 1721:2377, size = 33, replace = FALSE)
rand3 <- data.frame(rand3)
colnames(rand3) <- c("rand")
set.seed(3555)
rand4 <- sample(x = 2378:3148, size = 39, replace = FALSE)
rand4 <- data.frame(rand4)
colnames(rand4) <- c("rand")

rand <- rbind(rand1, rand2, rand3, rand4)

#subset suspended rules to sample
sample <- df[rand$rand,]

#export sample


write_xlsx(sample, "Sample_Non_Suspended_Rules.xlsx")
