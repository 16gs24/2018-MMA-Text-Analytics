from bs4 import BeautifulSoup as Soup
import re, pandas as pd
from selenium import webdriver
import sys, os
import feather
import json

class IndeedJobs:

	def __init__(self, query, city, numOfPages,):
		self.numOfPages = numOfPages
		self.query = query
		self.city= city
		
		self.indeed_url = "https://www.indeed.ca"		
		self.driver = webdriver.Chrome(os.getcwd() + "/chromedriver.exe")
		
		self.urls=[]
		
	def __PopulatePostingForURL(self, url):
		try:
			soup = self.__PopulateSoupObj(url)
			
			for script in soup(["script", "style"]):
				script.extract()
			text = soup.get_text()
			text = re.sub("[^a-zA-Z.+3#&]", " ", text)
			
			return text
		except:
			return "NA"

	def __Populate(self):
		for i in range(self.numOfPages):
			append_num = (i + 1) * 10
			base_url = '{}/jobs?q={}&I={}&start={}'.format(
					self.indeed_url,self.query,self.city,append_num)
			soup = self.__PopulateSoupObj(base_url)
			
			for posting in soup.find_all('div', {'class': 'row result'}):
				titles=posting.find('a', {'data-tn-element':'jobTitle'}).text
				job_tag = self.indeed_url+posting.a.get('href')
				company=posting.find('span', {'class':'company'}).text
				if 'pagead' not in job_tag:
					print(titles)
					print(job_tag)
					print(company)
				else: print('error')
				
				#job_postings=self.__PopulatePPostingForURL(job_tag)
				#job_tag = self.indeed_url+link.a.get('href')
				
				#if 'pagead' not in job_tag:
					#self.titles.append(job_title)
					#self.urls.append(job_tag)
					#job_posting = self.__PopulatePostingForURL(job_tag)
					#self.postings.append(job_posting)
		return self.urls

	def __PopulateSoupObj(self, url):
		self.driver.get(url)
		html = self.driver.page_source
		soup = Soup(html, 'html.parser')
		return soup

	def run(self):
		#urls=[]
		#titles=[]
		#company=[]
		#job_postings=[]
		
		self.__Populate()
		#mydict = {'company':company,
		#	'titles':titles,
		#	'posting':job_postings,
		#	'urls':urls}
		#print(mydict)
		#dataframe = pd.DataFrame(data=mydict)
		#filename = 'results_{}_{}.feather'.format(self.query,self.city)
		#feather.write_dataframe(dataframe, filename)

		#filename = 'indeed_search3_{}_{}.json'.format(self.query,self.city)
		#with open(filename, 'x') as fp:
			#json.dump(mydict, fp)


indeed = IndeedJobs("analytics", "Toronto+ON", 1)
indeed.run()
