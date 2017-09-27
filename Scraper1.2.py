from bs4 import BeautifulSoup as Soup
import re, pandas as pd
from selenium import webdriver
import sys, os
import feather

class IndeedJobs:

	def __init__(self, query, city, numOfPages,):
		self.numOfPages = numOfPages
		self.query = query
		self.city= city
		
		self.indeed_url = "https://www.indeed.ca"		
		self.driver = webdriver.Chrome(os.getcwd() + "/chromedriver.exe")
		
		self.urls = []
		self.titles=[]
		self.postings=[]
		self.company=[]
		
	def __PopulatePostingForURL(self, url):
		try:
			soup = self.__PopulateSoupObj(url)
			
			for script in soup(["script", "style"]):
				script.extract()
			text = soup.get_text()
			text = re.sub("[^a-zA-Z.+3#&]", " ", text)
			#text = text.lower().split()
			
			return text
		except:
			return "NA"

	def __Populate(self):
		for i in range(self.numOfPages):
			append_num = (i + 1) * 10
			base_url = '{}/jobs?q={}&I={}&start={}'.format(
					self.indeed_url,self.query,self.city,append_num)
			soup = self.__PopulateSoupObj(base_url)
			
			for link in soup.find_all('h2', {'class': 'jobtitle'}):
				job_title = link.a.get('title')
				job_tag = self.indeed_url+link.a.get('href')
				
				if 'pagead' not in job_tag:
					self.titles.append(job_title)
					self.urls.append(job_tag)
					job_posting = self.__PopulatePostingForURL(job_tag)
					self.postings.append(job_posting)
		#print("Added {} URLs Job Postings...".format(len(self.urls)))
		return self.urls
	
	def __PopulateCompanies(self):
		for i in range(self.numOfPages):
			append_num = (i + 1) * 10
			base_url = '{}/jobs?q={}&I={}&start={}'.format(
					self.indeed_url,self.query,self.city,append_num)
			soup = self.__PopulateSoupObj(base_url)
			
			for company in soup.find_all('span', {'class':'company'}):
				job_company = company.a.text
				print(job_company)
				self.company.append(job_company)

	def __PopulateSoupObj(self, url):
		self.driver.get(url)
		html = self.driver.page_source
		soup = Soup(html, 'html.parser')
		return soup

	def run(self):
		self.__Populate()
		mydict = {'urls':self.urls,
			'titles':self.titles,
			'text':self.postings}
		dataframe = pd.DataFrame(data=mydict)
		filename = 'results_{}_{}.feather'.format(self.query,self.city)
		feather.write_dataframe(dataframe, filename)


indeed = IndeedJobs("analytics", "Toronto+ON", 1)
indeed.run()
