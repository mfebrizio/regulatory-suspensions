install.packages("writerxl")
library("writexl")
library("tidyverse")
setwd("C:/Users/16192/OneDrive/")
library(readxl)
df <- read_excel("dfDelay.xlsx")

#scan the three columns for the keywords
#keywords: effective date, compliance date, delay

df$title <- as.character(df$title)
df$action <- as.character(df$action)
df$dates <- as.character(df$dates)

#alternative method
#https://programmersought.com/article/1682963614/#:~:text=stringr%3A%3Astr_detect%20The%20default,I%20want%20to%20ignore%20it.

#title column
df$titleTF <- 0
df$title1 <- str_detect(df$title, fixed("compliance date", ignore_case=T))
df$title2 <- str_detect(df$title, fixed("effective date", ignore_case=T))
df$title3 <- str_detect(df$title, fixed("delay", ignore_case=T))
df$titleTF[df$title1 == TRUE & df$title3 == TRUE|df$title2 == TRUE & df$title3 == TRUE] <- 1
sum(df$titleTF) #119

#action column

df$actionTF <- 0
df$action1 <- str_detect(df$action, fixed("compliance date", ignore_case=T))
df$action2 <- str_detect(df$action, fixed("effective date", ignore_case=T))
df$action3 <- str_detect(df$action, fixed("delay", ignore_case=T))
df$actionTF[df$action1 == TRUE & df$action3 == TRUE|df$action2 == TRUE & df$action3 == TRUE] <- 1
sum(df$actionTF) #210

#dates column

df$datesTF <- 0
df$dates1 <- str_detect(df$dates, fixed("compliance date", ignore_case=T))
df$dates2 <- str_detect(df$dates, fixed("effective date", ignore_case=T))
df$dates3 <- str_detect(df$dates, fixed("delay", ignore_case=T))
df$datesTF[df$dates1 == TRUE & df$dates3 == TRUE|df$dates2 == TRUE & df$dates3 == TRUE] <- 1
sum(df$datesTF) #214

#create suspension column (= 1 if at least one of three columns = 1)

df$susp <- 0
df$susp[df$titleTF == 1 | df$actionTF == 1 | df$datesTF == 1] <- 1
sum(df$susp) #227

#sum by President

sum(df$susp[df$president_id == "george-w-bush"]) #87
sum(df$susp[df$president_id == "barack-obama"]) #27
sum(df$susp[df$president_id == "donald-trump"]) #70
sum(df$susp[df$president_id == "joe-biden"]) #43

df1 <- df[,-c(21:33)] #delete unnecessary columns
df1 <- df1[df1$susp == 1,] #keep the suspended rules only

#export to .xlsx

write_xlsx(df[,-c(21:33)], "Raw_Rules_Ver2.xlsx")
write_xlsx(df1, "Suspended_Rules_Ver2.xlsx")

#compare the two methods

method1 <- read_excel("Raw_Rules.xlsx")
method2 <- read_excel("Raw_Rules_Ver2.xlsx")

which(method1$susp != method2$susp) #integer = 0, they are the same
which(method1$susp == method2$susp)

#sampling
#generate random unique integers
#generate n random numbers, where n = 50, x = the interval of numbers to choose from, inclusive

rand <- sample(x = 1:3375, size = 40, replace = FALSE)
rand <- data.frame(rand)

#save random numbers

write_xlsx(rand, "Raw_Sample_Random_Numbers.xlsx")

#subset raw rules to sample

raw <- read_excel("Raw_Rules_Ver2.xlsx")
sample <- raw[rand$rand,]

#export sample of raw rules

write_xlsx(sample, "Sample_Raw_Rules.xlsx")

#generate random unique numbers

rand2 <- sample(x = 1:227, size = 40, replace = FALSE)
rand2 <- data.frame(rand2)

#save random numbers

write_xlsx(rand2, "Suspended_Sample_Random_Numbers.xlsx")

#subset raw rules to sample

suspend <- read_excel("Suspended_Rules_Ver2.xlsx")
sample2 <- suspend[rand2$rand2,]

#export sample of raw rules

write_xlsx(sample2, "Sample_Suspended_Rules.xlsx")
