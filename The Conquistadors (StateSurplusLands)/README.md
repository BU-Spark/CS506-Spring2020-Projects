# Massachusetts State Surplus Land Project

Goal: Find the most profitable state owned land in the state of Massachusetts in order to raise funds to build affordable housing in affordable-housing deprived areas. 

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
matchAgencyList: 1 if std_name match the MassGovAgencyList names, 0 otherwise
FullOwnerAddress: combined value of owner address, owner city and owner state
TransportationOrHousing: separate properties into these 2 categories, 1 for transportation, 0 for housing and -1 for None
latitude: calculate latitude of owner address using geopy
longitude: calculate longitude of owner address using geopy
point: convert (latitude,longitude)from epsg 4326 to epsg 26986 format
removable: 1 if land is removable due to it is either wetlands, openspace, or conservation area, 0 otherwise

To install the libraries,
pip install -r requirements.txt

To reproduce the datasets:
please follow the steps mentioned in the final report, and also unzip the result folder.