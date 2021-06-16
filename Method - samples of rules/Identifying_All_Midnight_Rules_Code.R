#Midnight rules: all from election day until inauguration day
install.packages("writerxl")
library("writexl")
library("tidyverse")
setwd("C:/Users/16192/OneDrive/")
library(readxl)

cb <- read_excel("clinton_bush_midnight_rules.xlsx") #954
bo <- read_excel("bush_obama_midnight_rules.xlsx") #861
ot <- read_excel("obama_trump_midnight_rules.xlsx") #841
tb <- read_excel("trump_biden_midnight_rules.xlsx") #767

midnight <- rbind(cb, bo, ot, tb)

write_xlsx(midnight, "All_Midnight_Rules.xlsx")

#how many midnight rules per President

contain <- TRUE

for (i in 1:length(midnight$document_number))
{
  contain[i] <- "william-j-clinton" %in% midnight$president_id[i]
}

sum(contain, na.rm = FALSE) #954 midnight rules for Clinton

contain <- TRUE

for (i in 1:length(midnight$document_number))
{
  contain[i] <- "george-w-bush" %in% midnight$president_id[i]
}

sum(contain, na.rm = FALSE) #861 midnight rules for Bush

contain <- TRUE

for (i in 1:length(midnight$document_number))
{
  contain[i] <- "barack-obama" %in% midnight$president_id[i]
}

sum(contain, na.rm = FALSE) #841 midnight rule for Obama

contain <- TRUE

for (i in 1:length(midnight$document_number))
{
  contain[i] <- "donald-trump" %in% midnight$president_id[i]
}

sum(contain, na.rm = FALSE) #767 midnight rules for Trump
