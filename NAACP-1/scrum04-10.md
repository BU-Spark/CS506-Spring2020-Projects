04/10 
1. What work has the team done toward the project this week?

    We tried to label sub-neighborhoods to news articles scarped from news-websites. By linking the articles to sub-neighborhood through census tract number, we can know whether this news report is about a black community based on the population distributions we have collected before. 

2. Is the team having any issues?
	
    The way that we tried to figure out is to use regular expression to find a street name the article mentioned. Then, use pass the street name to US Census Geocoder and get the census track number it return. With that number we can check whether it is a black neighborhood. However, not every article specifically mention a street address.

3. What work does the team plan to do next week?
	
    Figure out a better way to group the news articles and start to do some sentimental analysis on the preprocessed data.
