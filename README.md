# Massachusetts State Surplus Land Project

Goal: Find the most profitable state owned land in the state of Massachusetts in order to raise funds to build affordable housing in affordable-housing deprived areas. 

## Task 1: Standardize all government agency names

### Method A: Use string-matching to classify variations of agency names to standardized agency name

Our dataset contains several government agencies that own land in the state of Massachusetts, each of which is classified by an arbitrary number of names. In order to standardize each agency to a single name, I will first generate a list of common names for each agency. Then, for each company, I will iterate through each tuple in the dataset exactly once and attempt to compare the recorded name to the generated common names. If there is a similarity between at least one generated name and the common name above some threshold, the recorded name will be modified to the accepted standardized name. 
