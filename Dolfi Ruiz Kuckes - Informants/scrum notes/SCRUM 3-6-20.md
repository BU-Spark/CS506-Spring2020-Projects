# Scrum 3-6-20

By Guthrie Kuckes
1. __What my team worked on:__
We scraped all appeals cases from the site masscases.com from 2000-2008 and from 2019, and parsed them into a JSON format extremely similar to the current format of our data. 

We also separated criminal from civil cases in our existing data from last week and observed that this only changed the number of cases with infromants detected by one. 
	
2.  __What work does the team plan to do next week?__
 - We plan to adjust the format of the JSON data to exactly match the format of our previous data 
 - We plan to rerun our analysis of which cases contain informants on the new data
 - We will continue to work on figuring out which cases were overturned, probably beginning by examining the algorithm used by previous teams
 
3. __Is the team having any issues?__
As we were scraping new data, we realized that the data contained in the two separate JSONs left by previous teams, which we thought was homogenous, was not, but actually comes from two different parts of the court system. This complicates our analysis, and we will now have to do a sophisticated duplicate search--we are talking with the client about how to interpret the data and where we should go from here. 

