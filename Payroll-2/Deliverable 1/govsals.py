import requests
import urllib.request
import time
from bs4 import BeautifulSoup as bs
import csv

def scrape_data(url, output):
	response = requests.get(url, timeout=10)
	soup = bs(response.content, 'html.parser')

	table = soup.find('table')
	rows = table.select('tbody > tr')

	header = [th.text.rstrip() for th in rows[0].find_all('th')]

	with open(output, 'a') as csv_file:
		writer = csv.writer(csv_file)
		writer.writerow(header)
		for row in rows[1:]:
			data = [th.text.rstrip() for th in row.find_all('td')]
			writer.writerow(data[1:])

	#print(rows)


#for i in range(1,132):
#	scrape_data("https://govsalaries.com/salaries/MA/city-of-new-bedford?sort=year-desc&page="+str(i), "new_bedford.csv")
	#scrape_data("https://govsalaries.com/salaries/MA/city-of-lowell?sort=jobTitle-asc&page="+str(i), "lowell.csv")
	#scrape_data("https://govsalaries.com/salaries/MA/city-of-lowell?sort=jobTitle-asc")


# check town CSV files against decert list
# def check_decert(decert_list, town_data):

	# with open(decert_list, 'r') as l1, open(town_data, 'r') as l2, open("compare.csv", "w") as compare:
		# writer = csv.writer(compare)
		# decerts = l1.readlines()
		# # print(decerts)
		# town = l2.readlines()
		# # for x in range(20):
		# # 	print(x)
		# # 	print(town[x])
		# for i in range(len(town)):
			# if i%2==0:
				# position = town[i].split(',')[0]
				# print(position)
				# if position == "Police Officer" and i > 0:
					# name = town[i-1].split(',')[0]
					# for decert in decerts: 
						# decert_name = decert.split(',')[0]
						# if decert_name == name:
							# data = town[i-1]+town[i]+decert
							# print(data)
							# writer.writerow(data)

def check_decert(decert_list, town_data):

	with open(decert_list, 'r') as l1, open(town_data, 'r') as l2, open("compare.csv", "w") as compare:
		writer = csv.writer(compare)
		decerts = l1.readlines()
		town = l2.readlines()
		for x in town:
			a = x.split(',')[0]
			for y in decerts: 
				b = y.split(',')[0]
				if a == b:
					data = y+x
					print(data)
					writer.writerow([data])

check_decert("USA_Today_Police_Decertifications_List.csv", "quincy.csv")
