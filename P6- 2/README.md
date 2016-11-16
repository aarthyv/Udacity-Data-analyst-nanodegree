##Data visualization of reading scores for 4th graders in countries with English as first language, 2011
### by Aarthy Vallur towards fulfillment of P6

This Data visualization shows the average reading proficiency scores for 4th graders in 5 countries where English is taught as the first language along with the international average for 2011. The data was obtained from the NCES and is part of the Progress in International Reading Literacy Study (PIRLS) data at <http://nces.ed.gov/surveys/pirls/idepirls/> 

##Design

###Preliminary exploration of data using Excel and R

I chose the data because I am interested in how reading contributes to educational achievement evaluation at many levels. The original data set consists of reading scores for over 60 countries with many categories. I chose to compare reading scores in the presence and absence of amenities and facilities outside school, such as room, desk, table and internet, since these are variables that were objectively accounted for. I also chose advanced countries that teach english as the first language, such as US, Canada, England, Australia and Singapore to be able to compare without interference from factors such as language and economic differences on the students. I chose to include the international average as a means of comparison. I chose my parameters in [PIRLS] (http://nces.ed.gov/surveys/pirls/idepirls/) and downloaded a series of data files. I then chose the conditions I wanted, namely, having or not having desk and table; having or not having either both or one of room and internet duration of study from 30 minutes- >2 hours and assembled my datafile,```Data3.csv```.  When I explored the initial dataset using R, I found that bivariate analysis allowed to visualize the average reading scores in the presence or absence of a particular factor, such as desk, table, room or internet. A series of facet wrapped bivariate graphs revealed subtle differences among the countries.
I then realized that my takeaway from the visualization needs to be

1. Does having or not having a factor affect reading scores? Clearly, scores drop when students don t have desks or tables, with the largest drop seem when they don’t have room and internet.
2. How to countries compare between each other and the international average on any given factor?
Towards that end, I realized I needed a visualization that will allow easy comparisons between points and countries and any trends.  So I then created a bar graph for the United states and overlaid other countries as lines. This created a good but confusing visual, since the y-axis scale was spread out clustering all the lines. Though this gave me a template to compare, it was not clear.
Also, looking at the data and the graphs, I realized that the duration of study was a personal factor that did not fit with the others, that were external, whose presence or absence can be objectively noted . So I removed it and wrangled the data to create ```Data4.csv```  as the final datafile with 3 columns- Categories, comprising countries, Reading scores and Factors. With this I created an initial line plot with a zoomed in y- axis for better discernment of trends using dimple.js in ```index_1.html```.  The line plots looked clean and easy to visualize. I then solicited feedback from 3 viewers:
###Feedback 1:
I really like the line plots, since they are simple and distinct due to the colors used. It is easy to see that all countries are above international average and that, the factors are clearly similar in these countries. The data is interesting and a clear trend of dropping reading scores when an amenity is not present, especially for internet is visible. But the zoomed scale irks me a bit- are these differences even significant? I would like to see only lines I choose, so counties can be compared in any way the viewer chooses. This will make the data more visually informative.
###Feedback 2:
I like the dataset in that the colors and bubbles are distinct and there are not too many categories in the graph. I like the pointer and how it aligns all the points. But, the factors- desk and table , room and internet are misleading to me- does having desk or table mean the student also has a room? Or doe sit mean that a student with a room also has a desk? What is the overlap among these factors. nevertheless, clearly, internet is a factor in reading scores- without which there is a very visible drop. This seems to be more drastic for some countries like Singapore and Australia than others. A bit of interactivity will make this a very satisfactory visualization.
###Feedback 3:
Simple and clear visualization, but the data seems more complex. Are these strictly home amenities? Do the students have access to desk or internet elsewhere like a library? That is not clear. But clearly in the absence of amenities, reading scores drop, more in some cases. Why does Australia see this drop? How is it different from the other countries? Also, were the sample sizes comparable to begin with? Singapore will have less students than the US or Canada, surely. The visualization does justice to the chosen data though. It is easy to understand the major trend. I would like to see bright colors or some way to pop- up the lines.

## Design incorporating feedback:
Taking these feedback into account, I incorporated the following into my updated visualization, ```index_2.html```. It has
1. Interactive legends, which are click -enabled. Clicking filters that category out. This allows for viewer- driven comparisons of any of the categories.
2. Made the chart size smaller and encompassing.
3. Changed chart title to be more descriptive.
Interactive legends really drove home the message of how reading scores drop when certain amenities are absent, especially internet and showed the extent of the drop for each country. Comparisons between 2 or more categories became much easier. 



