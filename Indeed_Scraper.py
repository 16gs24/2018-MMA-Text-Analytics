from bs4 import BeautifulSoup as Soup
import re, pandas as pd
from selenium import webdriver
import sys, os
import feather
import json

class IndeedJobs:

#initialize our class
	def __init__(self, query, city, numOfPages,):
		self.numOfPages = numOfPages
		self.query = query
		self.city= city
		
		self.indeed_url = "https://www.indeed.ca"		
		self.driver = webdriver.Chrome(os.getcwd() + "/chromedriver.exe")
		
		self.urls = []
		self.postings = []

#grab the text we need. enter the link indeed gives, grab text, return
	def __PopulatePostingForURL(self, url):
		try:
			soup = self.__PopulateSoupObj(url)
			
			for script in soup(["script", "style"]):
				script.extract()
			text = soup.get_text()
			#text = re.sub("[^a-zA-Z.+3#&]", " ", text)
			text = text.lower()
			return text
		except:
			return "NA"

#get our base URL. navigate to it. Loop through the non-sponsored jobs
#pull title, job tag, company then navigate to website to get text
#store it in a dictionary and append to list
	def __Populate(self):
		
		for i in range(self.numOfPages):
			append_num = (i + 1) * 10
			base_url = '{}/jobs?q={}&I={}&start={}'.format(
					self.indeed_url,self.query,self.city,append_num)
			soup = self.__PopulateSoupObj(base_url)
			
			current_page_postings = soup.find_all('div', {'data-tn-component': 'organicJob'})
			print('loading page', i+1,'of jobs for {}'.format(self.query))
			
			for posting in current_page_postings:
				titles=posting.find('a', {'data-tn-element':'jobTitle'}).text
				job_tag = self.indeed_url+posting.a.get('href')
				company = posting.find('span', {'class':'company'}).text
				text = self.__PopulatePostingForURL(job_tag)
				
				tempdict = {'title' : titles,'url' : job_tag,
			'company' : company, 'text' : text}
				
				self.postings.append(tempdict)

		return self.urls

#parse with soup
	def __PopulateSoupObj(self, url):
		self.driver.get(url)
		html = self.driver.page_source
		soup = Soup(html, 'html.parser')
		return soup

#run will call Populate which scrapes and creates our data, then saves it.
	def run(self):
		self.__Populate()

#write to feather to pass to R
		dataframe = pd.DataFrame.from_dict(self.postings)
		filename = '{}.feather'.format(self.query)
		feather.write_dataframe(dataframe, 'data/feather/' + filename)

#write to JSON to view data
		filename = '{}.json'.format(self.query)
		with open('data/json/'+ filename, 'x') as fp:
			json.dump(self.postings, fp)

#initialize terms and run searches
searches = ["analytics",
			"data analyst",
			"data scientist",
			"analytics strategy",
			"data insights",
			"marketing analytics",
			"analytics reporting",
			"machine learning",
			"business intelligence"]
				 
def searchnet(searchlist,numPages):
	for search in searchlist:
		indeed = IndeedJobs(search, "Toronto+ON", numPages)
		indeed.run()
		
searchnet(searches,10)
		
		








