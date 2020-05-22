import re
import timeit
from time import sleep

import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


class spider104:
    def __init__(self, keyword, area):
        """Create an object with keyword=job title, area=city name"""
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
        self.keyword = keyword
        self.area = area
        
    def openBrowser(self):
        """Since I only seek jobs in these three cities (新竹縣市、台北市、新北市) in Taiwan, so other cities are not
        available """
        driver = self.driver
        
        areadict = {'台北市':'6001001000','新北市':'6001002000','新竹縣市':'6001006000'}
        my_params = {'ro':'1', # limit to only full-time job. 
             'keyword':self.keyword, 
             'area': areadict[self.area], 
             'isnew':'30', 
             'mode':'l'} # list mode 

        headers = {
            "-----"}
        # type your computer headers

        url = requests.get('https://www.104.com.tw/jobs/search/?' , my_params, headers = headers).url
    
        
        driver.get(url)
    
    def scrollDown(self):
        """scroll down to page 15. After p.15 you need to press button 'next to 
        enter the next page'"""
        driver = self.driver
        
        sleep(0.5)
        for i in range(20): 
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            sleep(0.6)
    
    def clickNextPage(self):
        """click the button until there is no btn"""
        driver = self.driver
        
        nextp = 1
        count = 0
        while nextp != 0:    
            try:
                driver.find_elements_by_class_name('js-more-page')[count].click()
                driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                sleep(0.6)
                count +=1

            except:
                nextp = 0
                
    
    def getAllLinks(self):
        """get all links loaded in the page"""
        driver = self.driver
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        List = soup.findAll('a',{'class':'js-job-link'})
        return (List)
    
    def scrapeData(self,jobDataFrame):
        """Take one pandas dataframe as an input to save data into that dataframe
        the columns are ['title','company','jobDscrp','jobType','salary','location','startTime','workExp','edu',
        'fieldofStudy','language','tool','skills','others']"""
        driver = self.driver
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        jobDetails = soup.findAll('div',{'class':'job-description-table__data'})
        requirements = soup.findAll('div',{'class':'job-requirement-table__data'})

        df = pd.DataFrame(data= [{
            'title':soup.h1.attrs['title'],
            'company':soup.find('a',{'class':'mr-6'}).attrs['title'],
            'jobDscrp':soup.find('p',{'class':'text-break'}).text.replace('\r','').replace('\n',' '),
            'jobType':jobDetails[0].text.strip(),
            'salary':jobDetails[1].text.strip(),
            'location':jobDetails[3].text.strip(),
            'startTime':jobDetails[-2].text.strip(),
            'workExp':requirements[1].text.strip(),
            'edu':requirements[2].text.strip(),
            'fieldofStudy':requirements[3].text.strip(),
            'language':requirements[4].text.strip(),
            'tool':requirements[5].text.strip(),
            'skills':requirements[6].text.strip(),
            'others':requirements[-1].text.strip()}],
            columns = ['title','company','jobDscrp','jobType','salary','location','startTime','workExp','edu',
                       'fieldofStudy','language','tool','skills','others'],
            )
        
        jobDataFrame = jobDataFrame.append(df, ignore_index=True)
        return(jobDataFrame)
    
    def closeBrowser(self):
        """close the browser"""
        driver = self.driver
        driver.close()
        
        
    def goToPage(self, link):
        """go to certain page. for testing purpose only"""
        driver = self.driver
        driver.get(link)