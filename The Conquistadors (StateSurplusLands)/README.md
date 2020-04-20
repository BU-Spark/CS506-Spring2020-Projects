# Massachusetts State Surplus Land Project

Goal: Find the most profitable state owned land in the state of Massachusetts in order to raise funds to build affordable housing in affordable-housing deprived areas. 

## Task 1: Standardize all government agency names

### Method A: Use string-matching to classify variations of agency names to standardized agency name

Our dataset contains several government agencies that own land in the state of Massachusetts, each of which is classified by an arbitrary number of names. In order to standardize each agency to a single name, I will first generate a list of common names for each agency. Then, for each company, I will iterate through each tuple in the dataset exactly once and attempt to compare the recorded name to the generated common names. If there is a similarity between at least one generated name and the common name above some threshold, the recorded name will be modified to the accepted standardized name.


Dataset description (Only the features that are used are listed below):
 
poly_type: type of owner for the property, mainly focus on Fee and Tax
luc_1: Assessors Use Code (Min) , property type classification code (only uses 91_, 92_, and 97_)
luc_2: Assessors Use Code (Max) , property type classification code (only uses 91_, 92_, and 97_)
luc_adj_1: Standard Use Code (Min) , property type classification code (only uses 91_, 92_, and 97_)
luc_adj_2: Standard Use Code (Max) , property type classification code (only uses 91_, 92_, and 97_)
owner_name: Owner Name
owner_addr: Owner Address
owner_city: Owner City
owner_stat: Owner State
owner_zip: Owner Zip Code
std_name: standardize owner name in dataset for addresses with different variations of owner names
FullOwnerAddress: combined value of owner address, owner city and owner state
TransportationOrHousing: separate properties into these 2 categories, 1 for transportation, 0 for housing and -1 for None
