This README file contains descriptions of the X features of 52 features in the MAPC dataset used in analysis.
Features added as a result of the team's work are also indicated explained below

- POLY_TYP: Indicates type of ownership:  FEE, TAX, ROW, WATER, PRIV_ROW, RAIL_ROW(Boston_poly for City of Boston)- LUC_1: Assesors Code. The minimum property type classification code found on all of the associated assessors records; may include non-standard codes assigned by local staff luc_adj_1Standard Use Code (Min)Standard Use Code (Max)
- LUC_2: Assessors Use Code.The maximum property type classification code found on all ofthe associated assessors records; may include non-standard codes assigned by local staff
- LUC_ADJ_1: Standard Use Code. The minimum property type classification code, after non-standard codes were assigned by MAPC to the best match of standard codes
- LUC_ADJ 2: Standard Use Code.The maximum property type classification code, after non-standard codes were assigned by MAPC to the best match of standard codes
- MUNI: town of land parcel
- OWNER_NAME: name of agency/individual in possession of land parcel
- MAPC_ID: unique ID assigned to each parcel by MassGIS
- BLDG_VALUE: value of building on parcel for condos, generally includes land value
- BLDGV_PSF: building value $ per sq foot
- BLDG_AREA: total area taken up by building construction, may include garages, stairwells, basements, and other     uninhabitable areas.
- SQM_BLDG: parcel area estimated to be covered by a building (sq meters)
- PCT_BLDG: % parcel area estimated to be covered by a building
- numTransitStops (APPENDED): number of transit stops within .5 mi radius of land parcel
- longitude (APPENDED): String value of longitude of land parcel
- latitude (APPENDED): String value of latitude of land parcel
- owner_name_std (APPENDED): standardized owner_name values. Each unique agency should collapse into one spelling
- agency_name (APPENDED): maps each housing/transportation related agency in owner_name_std to an agency from Mass.gov's A-Z agency list

- NOTE: descriptions for all other features in the dataset can be found at https://mapc-org.sharefile.com/share/view/s8eb6a592d18450f9


