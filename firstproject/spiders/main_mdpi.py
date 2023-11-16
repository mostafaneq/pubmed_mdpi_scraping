import os
import re
import json
from time import sleep
from datetime import datetime
import logging
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from selenium.webdriver.common.action_chains import ActionChains
import unicodedata
import datefinder
from fastapi import FastAPI, HTTPException

app = FastAPI()

class MDPIScraper:
    def __init__(self, driver_path="/Users/hp/Downloads/chromedriver"):
        self.driver_path = driver_path
        self.chrome_options = Options()
        self.chrome_options.add_argument('--window-size=1920x1080')
        self.chrome_options.add_argument('--disable-gpu')
        self.chrome_options.add_argument('--disable-extensions')
        self.chrome_options.add_argument('--proxy-server="direct://"')
        self.chrome_options.add_argument('--proxy-bypass-list=*')
        self.chrome_options.add_argument('--start-maximized')
        self.driver = None

    def start_driver(self):
        #self.chrome_options.add_argument('--headless')
        self.driver = uc.Chrome(executable_path=self.driver_path, options=self.chrome_options)

    def stop_driver(self):
        if self.driver:
            self.driver.quit()

    def scrape_page(self, page_url, term, i, j,k):
        if not self.driver:
            raise Exception("Driver not initialized. Call start_driver() first.")
        
        self.driver.get(page_url)
        sleep(5)
        try:
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="CybotCookiebotDialogBodyButtonDecline"]'))).click()
        except:
            pass
        
        articles = self.driver.find_elements(By.CLASS_NAME, 'title-link')
        nbr_art=len(articles)
        article_page_info_element = self.driver.find_element(By.XPATH, '//*[@id="exportArticles"]/div/div[3]/div/div[2]/div[1]')

        info_text = article_page_info_element.text
        print(info_text)
        pattern = r'Displaying article (\d+)-(\d+) on page (\d+) of (\d+).'

        match = re.search(pattern, info_text)

        if match:
           total_pages = int(match.group(4))
    
        page_results = {}
        if k==0: 
         for i in range(1,nbr_art+1):
            article_dict = {}

            self.driver.get(page_url)
            sleep(3)           
            initial_XPATH = f"/html/body/div[9]/section/div/div/div[2]/div[2]/div/div/form/div/div[2]/div[{str(i)}]/div/a[1]"
            element =self.driver.find_element(By.XPATH,initial_XPATH)
            lk=element.get_attribute('href')
            self.driver.get(lk)

            try:
                        try:
                           WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="CybotCookiebotDialogBodyButtonDecline"]'))).click()
                        except:
                             pass
                        wait = WebDriverWait(self.driver, 5)
                        try:
                            titre = self.driver.find_element(By.XPATH, '//*[@id="abstract"]/div[2]/article/div/h1')
                            article_dict['titre'] = titre.text
                        except:
                            logging.error('ftitre')

                        try:
                            sleep(3)
                            authors_element = self.driver.find_element(By.XPATH, '//*[@id="abstract"]/div[2]/article/div/div[2]')
                            authors_string = authors_element.text
                            author_info = re.split(r'\d,*ORCID|and', authors_string)
                            names = []
                            for part in author_info:
                                part = part.strip()
                                if part:
                                    names.extend(re.findall(r'[A-Z][a-zA-Z]* [A-Z][a-zA-Z]*', part))
                            article_dict['authors'] = names
                        except:
                            logging.error('authors')
                            pass

                        try:
                            p_tags = self.driver.find_elements(By.CLASS_NAME, "html-p")
                            content = []
                            for tag in p_tags:
                                if tag.text.strip() != "":
                                    content.append(tag.text)
                            article_dict['content'] = content
                        except:
                            logging.error('hna 3awtani')
                            pass

                        try:
                            from datetime import datetime
                            sleep(2)
                            date_element = self.driver.find_element(By.XPATH, '//*[@id="abstract"]/div[2]/article/div/div[7]/span[4]')
                            input_date_str = date_element.text
                            input_date_str = input_date_str.replace("Published: ", "")
                            date = datetime.strptime(input_date_str, "%d %B %Y")
                            output_date_str = date.strftime("%Y-%b")
                            article_dict['DATE_PUBLICATION'] = output_date_str
                            article_dict['Query'] = term
                            journal=self.driver.find_element(By.XPATH,'//*[@id="abstract"]/div[2]/article/div/div[6]/em[1]')
                            article_dict['journal'] = journal.text
                            type_art=self.driver.find_element(By.XPATH,'//*[@id="abstract"]/div[2]/article/div/div[1]/span[2]')
                            article_dict['article_type'] = type_art.text
                        except:
                            logging.error('date')
            except:
                    logging.error('Error occurred while scraping')

            page_results[f"data{i}"] = article_dict
         return page_results
        else:
            return total_pages

#,'Non-Coding RNA','lncRNA','mRNA','microRNA'
def scrap(search_term):
    sous_term = [ 'miRNA','microRNA']  # Modify the list of terms as needed
    for s_term in sous_term:
        term = f"{search_term} AND {s_term}"
        year_from = "2020"
        year_to = "2023"

        # Initialize Selenium scraper
        scraper = MDPIScraper()
        scraper.start_driver()

        data_list = []
        last_successful_iteration = 0

        #+' '+ words[1]endometriosis AND lncRNA
        words = term.split()
        if search_term=='endometriosis':
          first_word = words[0]
          if s_term=='Non-Coding RNA':
            third_word = 'Non-Coding RNA'
            print(third_word)
          else:
           third_word = words[2]
           print(third_word)
        elif search_term=='Amyotrophic Lateral Sclerosis':
            first_word = words[0]+" "+ words[1]+" "+words[2]
            if s_term=='Non-Coding RNA':
             third_word = words[4]+" "+words[5]
             print(third_word)
            else:
             third_word = words[4]
             print(third_word)
        else:
           first_word = words[0]+" "+ words[1]
           if s_term=='Non-Coding RNA':
             third_word = words[3]+" "+words[4]
             print(third_word)
           else:
             third_word = words[3]
             print(third_word)

        nbr_page = scraper.scrape_page(
            f"https://www.mdpi.com/search?sort=pubdate&page_count=10&advanced=(@(title){first_word}@(title){third_word})&year_from={year_from}&year_to={year_to}&featured=&subjects=&journals=&article_types=&countries=",
            term,
            year_from,
            year_to,1
        )

        nbr_page = int(nbr_page)
        print(nbr_page)
        # Create a dictionary to store all the data
        all_data = {}

        for i in range(1, nbr_page+1):
            try:
                page_url = f"https://www.mdpi.com/search?sort=pubdate&page_no={i}&page_count=10&advanced=(@(title){first_word}@(title){third_word})&year_from={year_from}&year_to={year_to}&featured=&subjects=&journals=&article_types=&countries="
                data= scraper.scrape_page(page_url, term, year_from, year_to,0)

                if isinstance(data, dict):
                   data_list.append(data)


                if third_word == 'mRNA':
                    file_path = f'{first_word} AND mRNA{i}.json'
                elif third_word == 'lncRNA':
                    file_path = f'{first_word} AND lncRNA{i}.json'
                elif third_word == 'miRNA':
                    file_path = f'{first_word} AND miRNA{i}.json'
                elif third_word == 'microRNA':
                    file_path = f'{first_word} AND microRNA{i}.json'
                else:
                    file_path = f'{first_word} AND non-coding RNA{i}.json'
        
                with open(file_path, 'w', encoding='utf-8') as f:
                   json.dump(data, f, indent=4, ensure_ascii=False)
                sleep(2)
                with open(file_path,'r', encoding='utf-8') as file:
                   data = json.load(file)
                updated_data = []
                for key, value in data.items():
                  updated_data.append(value)
                with open(file_path, 'w') as file:
                  json.dump(updated_data, file, indent=4)
                last_successful_iteration = i
                
                with open(file_path , 'r', encoding='utf-8') as fichier:
                  donnees = json.load(fichier)
                donnees_sans_cles = {}

                for cle, valeur in donnees.items():
                   donnees_sans_cles.update(valeur)


                with open(file_path, 'w', encoding='utf-8') as fichier_sortie:
                  json.dump(donnees, fichier_sortie, indent=4)
            except Exception as e:
                print(f"An error occurred during iteration {i}: {e}. Retrying from iteration {last_successful_iteration + 1}...")
        try:
               directory_path = 'firstproject\\spiders'
               json_files = [f for f in os.listdir(directory_path) if f.startswith(search_term) and f.endswith('.json')]

               all_data = {}

               for json_file in json_files:
                 file_path = os.path.join(directory_path, json_file)
                 with open(file_path, 'r', encoding='utf-8') as file:
                     try:
                       data_list = json.load(file)
                       if isinstance(data_list, list) and len(data_list) == 1:
                         data = data_list[0]
                         if isinstance(data, dict):
                           all_data.update(data)
                         else:
                           print(f"Invalid data format in {json_file}")
                           print(f"Content: {data}")
                       else:
                           print(f"Invalid data format in {json_file}")
                           print(f"Content: {data_list}")
                     except json.JSONDecodeError as json_error:
                           print(f"Error decoding JSON in {json_file}: {json_error}")

               output_file_path = f'{search_term}.json'

               with open(output_file_path, 'w', encoding='utf-8') as output_file:
                   json.dump(all_data, output_file, indent=4, ensure_ascii=False)

               os.remove(file_path)
        except Exception as e:
                print(f"An error occurred in concat_del_json: {str(e)}")

        scraper.stop_driver()



def scrape_mdpi_data(search_term):
    # Initialize the scraper
    try:
        # Call the main scraping function
        scrap(search_term)
    except Exception as e:
        # Handle exceptions if needed
        raise HTTPException(status_code=500, detail=f"An error occurred during scraping: {str(e)}")
    # Return a success message
    return {"message": f"Scraping completed for search term: {search_term}"}

@app.post("/scrape-mdpi/")
async def scrape_mdpi_endpoint(search_term: str):
    # Validate the search term
    if not search_term:
        raise HTTPException(status_code=400, detail="Search term is required")

    # Call the scraping function
    scrape_mdpi_data(search_term)

if __name__ == "__main__":
    import uvicorn

    # Run the FastAPI application
    uvicorn.run(app, host="127.0.0.1", port=8000)
