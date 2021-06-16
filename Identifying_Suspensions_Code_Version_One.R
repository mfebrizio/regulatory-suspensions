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

#title column
#detect if string contains effective date/compliance date AND delay
#documentation: https://stackoverflow.com/questions/10128617/test-if-characters-are-in-a-string
#case sensitive? check case sensitivity for grepl

df$titleTF <- 0

df$title1 <- grepl("effective date", df$title, ignore.case = TRUE) #ignore.case = TRUE means case insensitive

df$title2 <- grepl("compliance date", df$title, ignore.case = TRUE)

df$title3 <- grepl("delay", df$title, ignore.case = TRUE)

df$titleTF[df$title1 == TRUE & df$title3 == TRUE | df$title2 == TRUE & df$title3 == TRUE] <- 1

sum(df$titleTF) #119

#action column

df$actionTF <- 0

df$action1 <- grepl("effective date", df$action, ignore.case = TRUE)

df$action2 <- grepl("compliance date", df$action, ignore.case = TRUE)

df$action3 <- grepl("delay", df$action, ignore.case = TRUE)

df$actionTF[df$action1 == TRUE & df$action3 == TRUE | df$action2 == TRUE & df$action3 == TRUE] <- 1

sum(df$actionTF) #210

#dates column

df$datesTF <- 0

df$dates1 <- grepl("effective date", df$dates, ignore.case = TRUE)

df$dates2 <- grepl("compliance date", df$dates, ignore.case = TRUE)

df$dates3 <- grepl("delay", df$dates, ignore.case = TRUE)

df$datesTF[df$dates1 == TRUE & df$dates3 == TRUE | df$dates2 == TRUE & df$dates3 == TRUE] <- 1

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
write_xlsx(df[,-c(21:33)], "Raw_Rules.xlsx")
write_xlsx(df1, "Suspended_Rules.xlsx")

#alternative method: commentary2

#compare the two columns (first method and second method, which rules are left out?)

which(df$susp != df$susp2) #none
which(df$titleTF != df$titleTF2)