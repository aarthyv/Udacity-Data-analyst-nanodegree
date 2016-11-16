library(ggplot2)
library(GGally)
library(dplyr)
library(tidyr)
library(scales)
library(RColorBrewer)
library(reshape2)
library(gridExtra)
library(markdown)
install.packages("gridExtra")

setwd('~/Desktop/P6 assignment')
data <- read.csv('Data3.csv')
str(data)
summary(data)
names(data)


## Some bivariate analysis
P1 <- ggplot(data = data, aes(x = Student.condition.at.home, y = International.Average, group_by(Factors))) +
geom_bar(aes(fill = Factors), stat = 'identity') +
  scale_y_continuous(limits = c(0,600), breaks = seq(0,600,100))+
  xlab("Home conditions") +
  theme(axis.text.x = element_text(angle = 45, hjust =1))+
  ylab("International average reading score")
P2 <- ggplot(data = data, aes(x = Student.condition.at.home, y = United.States, group_by(Factors))) +
  geom_bar(aes(fill = Factors), stat = 'identity') +
  scale_y_continuous(limits = c(0,600), breaks = seq(0,600,100))+
  xlab("Home conditions") +
  theme(axis.text.x = element_text(angle = 45, hjust =1))+
  ylab("United States average reading score")
P3 <- ggplot(data = data, aes(x = Student.condition.at.home, y = Australia, group_by(Factors))) +
  geom_bar(aes(fill = Factors), stat = 'identity') +
  scale_y_continuous(limits = c(0,600), breaks = seq(0,600,100))+
  xlab("Home conditions") +
  theme(axis.text.x = element_text(angle = 45, hjust =1))+
  ylab("Australia average reading score")
P4 <- ggplot(data = data, aes(x = Student.condition.at.home, y = Canada, group_by(Factors))) +
  geom_bar(aes(fill = Factors), stat = 'identity') +
  scale_y_continuous(limits = c(0,600), breaks = seq(0,600,100))+
  xlab("Home conditions") +
  theme(axis.text.x = element_text(angle = 45, hjust =1))+
  ylab("Canada average reading score")
P5 <- ggplot(data = data, aes(x = Student.condition.at.home, y = England, group_by(Factors))) +
  geom_bar(aes(fill = Factors), stat = 'identity') +
  scale_y_continuous(limits = c(0,600), breaks = seq(0,600,100))+
  xlab("Home conditions") +
  theme(axis.text.x = element_text(angle = 45, hjust =1))+
  ylab("England average reading score")
P6 <- ggplot(data = data, aes(x = Student.condition.at.home, y = Singapore, group_by(Factors))) +
  geom_bar(aes(fill = Factors), stat = 'identity') +
  scale_y_continuous(limits = c(0,600), breaks = seq(0,600,100))+
  xlab("Home conditions") +
  theme(axis.text.x = element_text(angle = 45, hjust =1))+
  ylab("Singapore average reading score")
grid.arrange(P1, P2, P3, P4, P5, P6, ncol= 3, top = "Distribution of reading scores in 4th graders across first world countries in 2011 based on student home conditions")


## Overlaying on United states to make comparisons
 ggplot(data = data, aes(x = Student.condition.at.home, y = United.States)) +
  geom_bar(color = "light blue", fill = "light blue", stat = 'identity') +
  geom_line(data = data, colour = "black", aes(x =Student.condition.at.home, y = International.Average, group = 1)) +
  geom_line(data = data, colour = "blue", aes(x =Student.condition.at.home, y = Canada, group = 1)) +
  geom_line(data = data, colour = "brown", aes(x =Student.condition.at.home, y = Australia, group = 1)) +
  geom_line(data = data, colour = "purple", aes(x =Student.condition.at.home, y = England, group = 1)) +
  geom_line(data = data, colour = "red", aes(x =Student.condition.at.home, y = Singapore, group = 1)) +
  scale_y_continuous(limits = c(0,600), breaks = seq(0,600,100))+
  xlab("Home conditions") +
  theme(axis.text.x = element_text(angle = 45, hjust =1))+
  ylab("United States average reading score")
