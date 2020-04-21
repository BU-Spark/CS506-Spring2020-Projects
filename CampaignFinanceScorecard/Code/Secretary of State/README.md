# CampaignFinanceScorecard
Project repository for CS506 - Campaign Finance Scorecard

# Instructions
The code was written using Jupyter Notebook, which makes it really easy to play around with the data.

Run 'jupyter notebook' command from the Secretary of State directory to view the code files

# Explanation

saved_links.pkl - The file that contains the defunct links to the main page of individual companies. These links are used by the link\_downloader.ipynb file to get the links to the actual companies

link_downloader.ipynb - Use this to get the links of all companies

pdf_downloader.ipynb - Once you have the links to companies, use this to download the Annual Report PDF's for all the companies

pdf_analyzer.ipynb - Once the PDF's are downloaded, use this to extract text data from them.
