install.packages("writerxl")
library("writexl")
library("tidyverse")
setwd("C:/Users/16192/OneDrive/")
library(readxl)

#first check: sample with suspensions
df <- read_excel("Sample_Suspended_Rules.xlsx")
which(df$susp != df$actual_susp) #5/115 not matching (4.3% error rate, 95.7% accuracy)
sum(df$susp != df$actual_susp)

#second check: sample with all rules
df <- read_excel("Sample_Raw_Rules.xlsx")
which(df$susp != df$actual_susp) #4/171 not matching (2.3% error rate, 97.7% accuracy)
sum(df$susp != df$actual_susp)

#third check: sample with non-suspensions
df <- read_excel("Sample_Non_Suspended_Rules.xlsx")
which(df$susp != df$actual_susp) #1/159 not matching (0.6% error rate, 99.4% accuracy)
sum(df$susp != df$actual_susp)