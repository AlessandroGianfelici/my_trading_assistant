import re
from datetime import date
from time import sleep

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

linkedin = {'AZM.MI': 'azimutgroup',
            'BMED.MI': 'banca-mediolanum',
            'CRES.MI': 'coima',
            'ENI.MI': 'eni',
            'FCT.MI': 'fincantieri',
            'G.MI': 'generali',
            'IRE.MI': 'iren-gruppo',
            'IG.MI': 'italgas',
            'LDO.MI': 'leonardo_company',
            'PST.MI': 'poste-italiane',
            'SRG.MI': 'snam-s-p-a-',
            'TITR.MI': 'tim',
            'UCG.MI' : 'unicredit',
            'TRN.MI': 'terna',
            'UNI.MI': 'unipol-gruppo',
            'WBD.MI': 'webuildgroup',
            'MT.MI': 'maire-tecnimont'}

class linkedinScraper:
    def __init__(self):
        self.email = 'gianfo90@gmail.com'
        self.password = 'Vitriol_01'
        self.driver = webdriver.Chrome()
    
    @staticmethod
    def jobs_url(company):
        return f"https://www.linkedin.com/company/{linkedin[company]}/jobs/"
    
    def connect(self):
        self.driver.get('https://www.linkedin.com/login')
        sleep(3)
        self.driver.find_element_by_id('username').send_keys(self.email)
        self.driver.find_element_by_id('password').send_keys(self.password)
        self.driver.find_element_by_id('password').send_keys(Keys.RETURN)
        return self.driver
    
    @staticmethod
    def get_employees_number(soup):
        s1 = soup.get_text()
        index = s1.find('"employeeCount":')
        s2 = s1[index+1:]
        n_employee = int(re.search(r'"employeeCount":(.*?),"callToAction"', s2).group(1))
        return n_employee
    
    @staticmethod
    def get_open_jobs(soup):
        s1 = soup.get_text()
        index = s1.find('"employeeCount":')
        s2 = s1[index+1:]
        s3_part = (re.search(r'"total":(.*?),"links"', s2).group(0))
        s3_index = s1.find(s3_part)
        s3 = s1[s3_index+1:]
        n_opening = int(re.search(r'"total":(.*?),"links"', s3).group(1))
        return n_opening
    
    def scrape(self, company_list):
        results = {}
        driver = self.connect()
        for company in company_list:
            print(f"Scraping {company}")
            sleep(5)
            driver.get(self.jobs_url(company))
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            try:
                results[company] = {'open_jobs' : self.get_open_jobs(soup),
                                'tot_employees' : self.get_employees_number(soup)}
                print(f"Scraped {company}: {results[company]['open_jobs']} open jobs over {results[company]['tot_employees']}")
                sleep(5)
            except:
                pass
        return results

if __name__ == '__main__':

    employees_dict = {}
    today = date.today()
    yyyymm = today.year * 100 + today.month
    filename = "open_positions.csv"
    old = pd.read_csv(filename).rename(columns={'Unnamed: 0':'company'}).set_index('company')
    current_month = old.loc[old['YYYYMM'] == yyyymm]
    to_scrape = set(linkedin.keys())-set(current_month.index)
    while len(to_scrape):
        my_scraper = linkedinScraper()
        employees_dict_tmp = my_scraper.scrape(to_scrape)
        employees_dict = employees_dict | employees_dict_tmp
        to_scrape = set(to_scrape)-set(employees_dict.keys())

    results = pd.DataFrame(employees_dict).T
    results['YYYYMM'] = yyyymm
    pd.concat([old, results]).to_csv(filename)