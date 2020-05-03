# Part3: possible customer and their expected prices
 Predict which range of the rent will be accepted by a customer based on a censor dataset.

## Codes:
* cleandata.ipynb (choosing data features that we need)
* rent1.ipynb (single models to predict housing prices)
* rent2.ipynb (combine 2 models for different fields to predict housing prices)


## Pre-request:
* anaconda3
* python 3.7.6
* pandas 1.0.2
* numpy 1.18.1
* scikit-learn 0.22.1
* seaborn 0.10.0
* matplotlib 3.2.0

## Input:
* A CSV file of all data features

## Output:
* Accuracy for each model

## How to run:
### rent1.ipynb
* Open jupyter notebook in anaconda
* Open file cleandata.ipynb
   * we cleanup dataset usa_00011 and we also provides dataset we use for next file which is dataMA.csv
* Now run rent1.ipynb in jupyter notebook 
* Run each Cell in order
* The accuracy result will be print out under each of the model cells. Model including:
	* Logistic Regression
	* SVM
	* Random Forest
	* KNN
	* MLP
	* LinearSVM

### rent2.ipynb
* Open jupyter notebook in anaconda
* Open file cleandata.ipynb
   * we cleanup dataset usa_00011 and we also provides dataset we use for next file which is dataMA.csv
* Now open rent2.ipynb in jupyter notebook 
* Change the variable model1(The model we used for layer1) and model2(The model we used for layer2) for the models we want.
	* 1: Logistic Regression
	* 2: SVM
	* 3: Random Forest
	* 4: KNN
	* 5: MLP
	* 6: LinearSVM
* Run all the cells
* The accuracy result will be print out under each of the model cells.



## Labels:
* Year (YEAR)
   * Include sample in 2016, 2017 and 2018
* State (STATEFIP)
   * We only use data in MA which has state code 25
* City (CITY)
   * Narrow down our city choosing to Boston, Cambridge and Brookline
   * Boston is 0, Brookline is 1, Cambridge is 2
* Mortgage status (MORTGAGE)
   * Indicate whether the person is encumbered by mortgage or loan
   * N/A is 0, No is 1, Yes with mortgage is 3, Yes with contract is 4
* Monthly contract rent (RENT)
   * Reports the amount of household’s monthly contract rent payment
   * N/A is 0000 
* Kitchen or cooking facilities (KITCHEN)
   * Indicates whether the housing unit contained kitchen facilities.
   * N/A is 0, No is 1, Yes is 4
* Refrigerator (FRIDGE)
   * Indicates whether the housing unit provided access to a refrigerator
   * N/A is 0, No is 1, Yes is 2
* Telephone availability (PHONE)
   * Indicates whether residents of the housing unit had telephone access.
   * N/A is 0, No is 1, Yes is 2
* Access to Internet (CINETHH)
   * Indicate whether any member of the household accesses the Internet.
   * N/A is 0, Yes with subscription to internet is 1, Yes without subscription is 2, No is 3
* Number of family member (FAMSIZE)
   * Counts the number of own family members residing with each individual, including the person her/himself.
* Sex (SEX)
   * Male is 1, Female is 2
* Age (AGE)
* Marital status (MARST)
   * Married with spouse present is 1, Married without spouse present is 2, Seperated is 3, Divorced is 4, Widow is 5, Single is 6
* Race (RACE)
   * White is 1, Blace/African American/Negro is 2, American India or Alaska Native is 3, Chinese is 4, Japanese is 5, Other Asian or Pacific Islander is 6, Other race is 7
* Citizenship status (CITIZEN)
   * Reports the citizenship status of respondents, distinguishing between naturalized citizens and non-citizens.
   * N/A is 0, Borned abroad of American parents is 1, Naturalized citizen is 2, Not citizen is 3
* School attendance (SCHOOL)
   * Indicates whether the respondent currently attend school
   * N/A is 0, No is 1, Yes is 2
* Education attainment (EDUC)
   * Indicates respondents' educational attainment, as measured by the highest year of school or degree completed. 
   * N/A is 0, grade 4 or below is 1, grade 5,6,7,8 is 2, grade 9 is 3 …...4 years of college is 10, 5+ years of college is 11
* Grade level attending (GRADEATT)
   * Reports the grade or level of recent schooling for people who attended "regular school or college" 
   * N/A is 0, preschool is 1, Kindergarten is 2, Grade 1-4 is 3, Grade 5-8 is 4, Grade 9-12 is 5, College undergraduate is 6, Graduate or professional school is 7
* Employment status (EMPSTAT)
   * Indicates whether the respondent was a part of the labor force -- working or seeking work -- and, if so, whether the person was currently unemployed. 
   * N/A is 0, Employed is 1, Unemployed is 2, Not in labor force is 3
* Total personal income (INCTOT)
   * Reports each respondent's total pre-tax personal income
* Total family income (FTOTINC)
   * Reports the total pre-tax money income earned by one's family
