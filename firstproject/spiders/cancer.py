import scrapy
import os
from time import sleep
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import json
import undetected_chromedriver as uc
from seleniumwire import webdriver
from selenium_stealth import stealth
from fastapi import FastAPI
import pyperclip
import re 
from selenium.webdriver.common.action_chains import ActionChains
import datefinder

basedir = os.path.dirname(os.path.realpath('__file__'))
#mRNA
class pubMed_spider(scrapy.Spider):
 name = "cancer"
 allowed_domains = ["pubmed.ncbi.nlm.nih.gov"]
 i = "2020"
 j = "2023"
 term = "ovarian cancer AND (lncRNA OR microRNA OR miRNA OR mRNA OR Non-Coding RNA)"
 start_urls = [f"https://pubmed.ncbi.nlm.nih.gov/?term={term}&filter=years.{i}-{j}"]

 def parse(self, response):
   chrome_options = Options()
   chrome_options.add_argument("--headless")
   #driver = webdriver.Chrome(executable_path="/Users/hp/Desktop/driver/chromedriver.exe", options=chrome_options)
   driver1 = uc.Chrome(executable_path="/Users/hp/Desktop/driver/chromedriver.exe")
   driver1.get(self.start_urls[0])
   all_results={}
 # Get the total number of pages
   nbr = driver1.find_element_by_xpath("//*[@id='bottom-page-number-input']")
   nbr_page = int(nbr.get_attribute("max"))
   article_dict = {}
   def scrap(nbr):
    global hogrefe
    global CURRENT
    global citation_1
    global abstract


    import re
    import datefinder

    def extract_date_from_text(text):
     matches = datefinder.find_dates(text)
     for match in matches:
        formatted_date = match.strftime("%Y-%m")
        return formatted_date
     return None

    def extract_date_and_year(text):
     pattern_epub = r"Epub (\d{4} [A-Za-z]{3} \d{1,2})"
     pattern_print = r"Print (\d{4} [A-Za-z]{3} \d{1,2})"
     pattern_date = r"\d{4} [A-Za-z]{3} \d{1,2}"

     match_epub = re.search(pattern_epub, text)
     if match_epub:
        date = match_epub.group(1)
        formatted_date = date.split()[0] + "-" + date.split()[1]
        return formatted_date

     match_print = re.search(pattern_print, text)
     if match_print:
        date = match_print.group(1)
        formatted_date = date.split()[0] + "-" + date.split()[1]
        return formatted_date

     match_date = re.search(pattern_date, text)
     if match_date:
        date = match_date.group(0)
        formatted_date = date.split()[0] + "-" + date.split()[1]
        return formatted_date
     else:
        return extract_date_from_text(text)
     return None

    def remove_repeated_words(text):
     words = text.split()
     unique_words = []
     for word in words:
        if word not in unique_words:
            unique_words.append(word)
     return ' '.join(unique_words)

    
    for page_num in range(nbr, nbr+1):
     page_url = self.start_urls[0] + f"&page={page_num}"
     driver1.get(page_url)
     articles = driver1.find_elements(By.TAG_NAME, 'article')
     nbr_art=len(articles)
     for i in range(1,2):   
      driver1.get(page_url)
      initial_XPATH=f"/html/body/main/div[9]/div[2]/section[1]/div[1]/div/article["+ str(i) +"]/div[2]/div[1]/a"                                                            
      WebDriverWait(driver1, 10).until(EC.visibility_of_element_located((By.XPATH, initial_XPATH))).click()
      sleep(2)
      abs = driver1.find_elements(By.TAG_NAME, "p")
      text = []
      for div in abs:
          text.append(div.text)
      abstract = list(set(text))
      wait = WebDriverWait(driver1, 15)
      driver1.execute_script("window.scrollBy(0, 200);")
      try:
       citation_button = driver1.find_element(By.XPATH,'//*[@id="article-page"]/aside/div/div[2]/div/button[1]')
       actions = ActionChains(driver1)
       actions.move_to_element(citation_button).click().perform() 
      except:
         citation_button = driver1.find_element(By.XPATH,'/html/body/div[5]/aside/div/div[1]/div/button[1]')
         actions = ActionChains(driver1)
         actions.move_to_element(citation_button).click().perform() 
      try:  
       copy_button = WebDriverWait(driver1, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='article-page']/div[2]/div/div[2]/div[2]/button")))    
       copy_button.click()
      except:
        copy_button = WebDriverWait(driver1, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div[1]/div/div[2]/div[2]/button")))    
        copy_button.click()
      citation_1= pyperclip.paste()
      date_year_extracted = extract_date_and_year(citation_1)
      match_authors = re.search(r"^([^\.]+)\.", citation_1)
      authors = match_authors.group(1).strip() if match_authors else ""
      sentences = citation_1.split('. ')
      if len(sentences) >= 2:
       titre = sentences[1]
      else:
        print("Aucun titre trouvé.")
      match_pmid = re.search(r"PMID: (\d+)", citation_1)
      pmid = match_pmid.group(1) if match_pmid else ""

      CURRENT=driver1.current_url
      article_dict = {}
      link=""
      title=""
      try :
        sleep(5)
        try:
          img_element = driver1.find_element_by_xpath("/html/body/div[5]/aside/div/div[1]/div[1]/div/a")
        except:
          img_element = driver1.find_element_by_xpath("/html/body/div[5]/aside/div/div[1]/div[1]/div/a") 
        link = img_element.get_attribute('href')
        title = img_element.get_attribute('title')
        if "GN1 Sistemas e Publicacoe" in title:
           img_element2 = driver1.find_element_by_xpath("/html/body/div[5]/aside/div/div[1]/div[1]/div/a[2]")
           link = img_element2.get_attribute('href')
           driver.get(link)  
        elif "hogrefe" in link :
           hogrefe =driver1.find_element(By.CLASS_NAME,"authors-list") 
           author=hogrefe.text    
        try:
           driver1.get(link)
        except:
           driver1.get(link)     
        current_url=driver1.current_url
        sleep(6)
        if "jogc" in current_url:
          driver1.get(link)
          try:     
            wait = WebDriverWait(driver1, 10)
            try:
             WebDriverWait(driver1, 10).until(EC.visibility_of_element_located((By.ID, "onetrust-accept-btn-handler"))).click() 
            except:
               pass                                        
            article_dict['titre'] = titre
            article_dict['authors'] = authors
            article_dict['PMID'] = pmid
            content_divs = driver1.find_elements(By.CLASS_NAME, "section-paragraph")
            Content_texts=[]
            for div in content_divs:
               Content_texts.append(div.text)
            Content_text=list(set(Content_texts))
            article_dict['content'] = Content_text
            article_dict['abstract'] = abstract
            article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
            article_dict['News_paper'] = "jogc"
            article_dict['Query'] = self.term
            if f"data{i}" in all_results:
               all_results[f"data{i}"].update(article_dict)
            else:
               all_results[f"data{i}"] = article_dict
            json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
            driver1.get(page_url)
          except:
            
             pass
        elif "ajog" in current_url:
          driver1.get(link)
          try:     
            wait = WebDriverWait(driver1, 10)
            try:
             WebDriverWait(driver1, 10).until(EC.visibility_of_element_located((By.ID, "onetrust-accept-btn-handler"))).click() 
            except:
               pass                                        
            article_dict['titre'] = titre
            article_dict['authors'] = authors
            article_dict['PMID'] = pmid
            content_divs = driver1.find_elements(By.CLASS_NAME, "section-paragraph")
            Content_texts=[]
            for div in content_divs:
               Content_texts.append(div.text)
            Content_text=list(set(Content_texts))
            article_dict['content'] = Content_text
            article_dict['abstract'] = abstract
            article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
            article_dict['News_paper'] = "ajog"
            article_dict['Query'] = self.term
            if f"data{i}" in all_results:
                all_results[f"data{i}"].update(article_dict)
            else:
                all_results[f"data{i}"] = article_dict
            json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
            driver1.get(page_url)
          except:
            
             pass
        elif "fertstertscience.org" in current_url:
          driver1.get(link)
          try:     
            wait = WebDriverWait(driver1, 10)
            try:
             WebDriverWait(driver1, 10).until(EC.visibility_of_element_located((By.ID, "onetrust-accept-btn-handler"))).click() 
            except:
               pass                                        
            article_dict['titre'] = titre
            article_dict['authors'] = authors
            article_dict['PMID'] = pmid
            content_divs = driver1.find_elements(By.CLASS_NAME, "section-paragraph")
            Content_texts=[]
            for div in content_divs:
               Content_texts.append(div.text)
            Content_text=list(set(Content_texts))
            article_dict['content'] = Content_text
            article_dict['abstract'] = abstract
            article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
            article_dict['News_paper'] = "fertstertscience"
            article_dict['Query'] = self.term
            if f"data{i}" in all_results:
                all_results[f"data{i}"].update(article_dict)
            else:
                all_results[f"data{i}"] = article_dict
            json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
            driver1.get(page_url)
          except:
            
             pass
        elif "jmig" in current_url:
          driver1.get(link)
          try:
           wait = WebDriverWait(driver1, 10)
           try:
             WebDriverWait(driver1, 10).until(EC.visibility_of_element_located((By.ID, "onetrust-accept-btn-handler"))).click() 
           except:
               pass                                        
           article_dict['titre'] = titre
           article_dict['authors'] = authors
           article_dict['PMID'] = pmid
           content_divs = driver1.find_elements(By.CLASS_NAME, "section-paragraph")
           Content_texts=[]
           for div in content_divs:
               Content_texts.append(div.text)
           article_dict['content'] = Content_texts
           article_dict['abstract'] = abstract
           article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
           article_dict['News_paper'] = "jmig"
           article_dict['Query'] = self.term
           if f"data{i}" in all_results:
                all_results[f"data{i}"].update(article_dict)
           else:
                all_results[f"data{i}"] = article_dict
           json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
           driver1.get(page_url)
          except:
            
             pass
        elif "ejradiology" in current_url:
          driver1.get(link)
          try:
           wait = WebDriverWait(driver1, 10)
           try:
             WebDriverWait(driver1, 10).until(EC.visibility_of_element_located((By.ID, "onetrust-accept-btn-handler"))).click() 
           except:
               pass                                        
           article_dict['titre'] = titre
           article_dict['authors'] = authors
           article_dict['PMID'] = pmid
           content_divs = driver1.find_elements(By.CLASS_NAME, "section-paragraph")
           Content_texts=[]
           for div in content_divs:
               Content_texts.append(div.text)
           article_dict['content'] = Content_texts
           article_dict['abstract'] = abstract
           article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
           article_dict['News_paper'] = "ejradiology"
           article_dict['Query'] = self.term
           if f"data{i}" in all_results:
                all_results[f"data{i}"].update(article_dict)
           else:
                all_results[f"data{i}"] = article_dict
           json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
           driver1.get(page_url)
          except:
            
             pass
        elif "ejog.org" in current_url:
          driver1.get(link)
          try:
           wait = WebDriverWait(driver1, 10)
           try:
             WebDriverWait(driver1, 10).until(EC.visibility_of_element_located((By.ID, "onetrust-accept-btn-handler"))).click() 
           except:
               pass                                        
           article_dict['titre'] = titre
           article_dict['authors'] = authors
           article_dict['PMID'] = pmid
           content_divs = driver1.find_elements(By.TAG_NAME, "section")
           Content_texts=[]
           for div in content_divs:
               Content_texts.append(div.text)
           article_dict['content'] = Content_texts
           article_dict['abstract'] = abstract
           article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
           article_dict['News_paper'] = "ejog"
           article_dict['Query'] = self.term
           if f"data{i}" in all_results:
                all_results[f"data{i}"].update(article_dict)
           else:
                all_results[f"data{i}"] = article_dict
           json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
           driver1.get(page_url)
          except:
            
             pass
        elif "cell" in current_url:
          driver1.get(link)
          try:
           wait = WebDriverWait(driver1, 10)
           try:
             WebDriverWait(driver1, 10).until(EC.visibility_of_element_located((By.ID, "onetrust-accept-btn-handler"))).click() 
           except:
               pass                                        
           article_dict['titre'] = titre
           article_dict['authors'] = authors
           article_dict['PMID'] = pmid
           content_divs = driver1.find_elements(By.TAG_NAME, "section")
           Content_texts=[]
           for div in content_divs:
               Content_texts.append(div.text)
           article_dict['content'] = Content_texts
           article_dict['abstract'] = abstract
           article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
           article_dict['News_paper'] = "cell"
           article_dict['Query'] = self.term
           if f"data{i}" in all_results:
                all_results[f"data{i}"].update(article_dict)
           else:
                all_results[f"data{i}"] = article_dict
           json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
           driver1.get(page_url)
          except:
            
             pass
        elif "rbmojournal.com" in current_url:
          driver1.get(link)
          try:
           wait = WebDriverWait(driver1, 10)
           try:
             WebDriverWait(driver1, 10).until(EC.visibility_of_element_located((By.ID, "onetrust-accept-btn-handler"))).click() 
           except:
               pass                                        
           article_dict['titre'] = titre
           article_dict['authors'] = authors
           article_dict['PMID'] = pmid
           content_divs = driver1.find_elements(By.TAG_NAME, "section")
           Content_texts=[]
           for div in content_divs:
               Content_texts.append(div.text)
           article_dict['content'] = Content_texts
           article_dict['abstract'] = abstract
           article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
           article_dict['News_paper'] = "rbmojournal"
           article_dict['Query'] = self.term
           if f"data{i}" in all_results:
                all_results[f"data{i}"].update(article_dict)
           else:
                all_results[f"data{i}"] = article_dict
           json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
           driver1.get(page_url)
          except:
            
             pass
        elif "sciencedirect.com" in current_url:
          driver1.get(link)
          sleep(8) 
          try:   
            wait = WebDriverWait(driver1, 5)
            article_dict['titre'] = titre
            article_dict['authors'] = authors
            article_dict['PMID'] = pmid
            Content_texts=[]
            p_tags = driver1.find_elements_by_tag_name("p")
            for tag in p_tags:
               if tag.text.strip() != "":
                  Content_texts.append(tag.text)
            article_dict['content'] = Content_texts
            article_dict['abstract'] = abstract
            article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
            article_dict['News_paper'] = "sciencedirect"
            article_dict['Query'] = self.term
            if f"data{i}" in all_results:
                  all_results[f"data{i}"].update(article_dict)
            else:
                 all_results[f"data{i}"] = article_dict
            json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
          except:
            
             pass

        elif "mdpi" in current_url:
          driver1.get(link)
          sleep(5)
          try:
           wait = WebDriverWait(driver1, 5)
           article_dict['titre'] = titre
           article_dict['authors'] = authors
           article_dict['PMID'] = pmid
           p_tags = driver1.find_elements_by_class_name("html-p")
           content=[]
           for tag in p_tags:
             if tag.text.strip() != "":
               content.append(tag.text)
           article_dict['content'] = content
           article_dict['abstract'] = abstract
           article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
           article_dict['News_paper'] = "mdpi"
           article_dict['Query'] = self.term
           if f"data{i}" in all_results:
                all_results[f"data{i}"].update(article_dict)
           else:
                all_results[f"data{i}"] = article_dict
           json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
          except:
            
             pass

        elif "springermedizin" in current_url:
           pass
            
        elif "link.springer.com" in current_url :
           driver1.get(link)
           sleep(6)
           try:
            print('oui')
            wait = WebDriverWait(driver1, 5)
            article_dict['titre'] = titre
            article_dict['authors'] = authors
            article_dict['PMID'] = pmid
            p_tags = driver1.find_elements_by_tag_name("p")
            content=[]
            for tag in p_tags:
             if tag.text.strip() != "":
               content.append(tag.text)
            article_dict['content'] = content
            article_dict['abstract'] = abstract
            try:
             article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
            except:
              try:
               element=driver1.find_element_by_xpath("/html/body/div[2]/div[3]/main/article/header/div/ul[2]/li[2]/a/time")
               article_dict['DATE_PUBLICATION'] =  remove_repeated_words(extract_date_and_year(element.text))
              except:
                article_dict['DATE_PUBLICATION'] = ""
            article_dict['News_paper'] = "springer"
            article_dict['Query'] = self.term
            if f"data{i}" in all_results:
               all_results[f"data{i}"].update(article_dict)
            else:
               all_results[f"data{i}"] = article_dict
            json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
            driver1.get(page_url)
           except:
              print('non')
              pass
           
        elif "onlinelibrary.wiley.com" in current_url:
          stealth(driver,
                 languages=["en-US", "en"],
                 vendor="Google Inc.",
                 platform="Win32",
                 webgl_vendor="Intel Inc.",
                 renderer="Intel Iris OpenGL Engine",
                 fix_hairline=True,
          )
          driver1.get(link)
          try:
           wait = WebDriverWait(driver1, 5)
           article_dict['titre'] = titre
           article_dict['authors'] = authors
           article_dict['PMID'] = pmid
           p_tags = driver1.find_elements_by_tag_name('p')
           content=[]
           for tag in p_tags:
             if tag.text.strip() != "":
               content.append(tag.text)
           article_dict['content'] = content
           article_dict['abstract'] = abstract
           article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
           article_dict['News_paper'] = "wiley"
           article_dict['Query'] = self.term
           if f"data{i}" in all_results:
               all_results[f"data{i}"].update(article_dict)
           else:
               all_results[f"data{i}"] = article_dict
           json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
           driver1.get(page_url)
          except:
            
             pass


        elif "thieme" in link:
          driver1.get(link)
          try:
            sleep(10)
            try:
             WebDriverWait(driver1, 15).until(EC.visibility_of_element_located((By.ID, "onetrust-accept-btn-handler"))).click()
            except:
               pass
            try:
             WebDriverWait(driver1, 30).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[3]/div[1]/div[2]/article/ul/li[2]/a"))).click()
            except:
             current=driver.current_url
             if "/login.html" in current:
               driver1.get(link)
               p_tags = driver1.find_elements_by_tag_name('p')
               content=[]
               for tag in p_tags:
                 if tag.text.strip() != "":
                  content.append(tag.text)
               article_dict['content'] = content
             else:
                pass
            wait = WebDriverWait(driver1, 15)
            article_dict['titre'] = titre
            article_dict['authors'] = authors
            article_dict['PMID'] = pmid
            p_tags = driver1.find_elements_by_tag_name('p')
            content=[]
            for tag in p_tags:
             if tag.text.strip() != "":
               content.append(tag.text)
            article_dict['content'] = content
            article_dict['abstract'] = abstract
            article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
            article_dict['News_paper'] = "thieme"
            article_dict['Query'] = self.term
            if f"data{i}" in all_results:
               all_results[f"data{i}"].update(article_dict)
            else:
              all_results[f"data{i}"] = article_dict
            json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
          except:
            
             pass

        elif "hogrefe" in link:
          driver1.get(link)
          try: 
           try:
              WebDriverWait(driver1, 15).until(EC.visibility_of_element_located((By.ID, "onetrust-reject-all-handler"))).click()
           except:
              pass
           article_dict['titre'] = titre
           article_dict['authors'] = authors
           article_dict['PMID'] = pmid
           p_tags = driver1.find_elements_by_tag_name("p")
           content=[]
           for tag in p_tags:
             if tag.text.strip() != "":
               content.append(tag.text)
           article_dict['content'] = content
           article_dict['abstract'] = abstract
           try:
             article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
           except:
             element= driver1.find_element_by_class_name('epub-section__date')
             article_dict['DATE_PUBLICATION'] = element.text
           article_dict['News_paper'] = "hogrefe"
           article_dict['Query'] = self.term
           if f"data{i}" in all_results:
               all_results[f"data{i}"].update(article_dict)
           else:
              all_results[f"data{i}"] = article_dict
           json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
          except:
             pass
          
        elif "tidsskriftet" in link:
          driver1.get(link)
          try:
           wait = WebDriverWait(driver1, 15)
           article_dict['titre'] = titre
           article_dict['authors'] = authors
           article_dict['PMID'] = pmid
           p_tags = driver1.find_elements_by_tag_name("p")
           content=[]
           for tag in p_tags:
             if tag.text.strip() != "":
               content.append(tag.text)
           article_dict['content'] = content
           article_dict['abstract'] = abstract
           article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
           article_dict['News_paper'] = "tidsskriftet"
           article_dict['Query'] = self.term
           if f"data{i}" in all_results:
               all_results[f"data{i}"].update(article_dict)
           else:
              all_results[f"data{i}"] = article_dict
           json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
          except:
            
             pass
        elif "edpsciences" in link:
          driver1.get(link)
          try:
           wait = WebDriverWait(driver1, 15)
           article_dict['titre'] = titre
           article_dict['authors'] = authors
           article_dict['PMID'] = pmid
           p_tags = driver1.find_elements_by_tag_name("p")
           content=[]
           for tag in p_tags:
             if tag.text.strip() != "":
               content.append(tag.text)
           article_dict['content'] = content
           article_dict['abstract'] = abstract
           article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
           article_dict['News_paper'] = "edpsciences"
           article_dict['Query'] = self.term
           if f"data{i}" in all_results:
               all_results[f"data{i}"].update(article_dict)
           else:
              all_results[f"data{i}"] = article_dict
           json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
          except:
            
             pass
        elif "panafrican-med-journal.com" in current_url:
          driver1.get(link)
          try:
           wait = WebDriverWait(driver1, 15)
           article_dict['titre'] = titre
           article_dict['authors'] = authors
           article_dict['PMID'] = pmid
           p_tags = driver1.find_elements_by_tag_name("p")
           content=[]
           for tag in p_tags:
             if tag.text.strip() != "":
               content.append(tag.text)
           article_dict['content'] = content
           article_dict['abstract'] = abstract
           article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
           article_dict['News_paper'] =  "panafrican-med-journal"
           article_dict['Query'] = self.term
           if f"data{i}" in all_results:
               all_results[f"data{i}"].update(article_dict)
           else:
              all_results[f"data{i}"] = article_dict
           json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
          except:
           
             pass
         
        elif "rev-mal-respir.com" in current_url:
          driver1.get(link)
          try:
           wait = WebDriverWait(driver1, 15)
           article_dict['titre'] = titre
           article_dict['authors'] = authors
           article_dict['PMID'] = pmid
           p_tags = driver1.find_elements_by_tag_name("p")
           content=[]
           for tag in p_tags:
             if tag.text.strip() != "":
               content.append(tag.text)
           article_dict['content'] = content
           article_dict['abstract'] = abstract
           article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
           article_dict['News_paper'] = "rev-mal-respir"
           article_dict['Query'] = self.term
           if f"data{i}" in all_results:
               all_results[f"data{i}"].update(article_dict)
           else:
              all_results[f"data{i}"] = article_dict
           json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
          except:
            
             pass
         
        elif "degruyter.com" in current_url:
          driver1.get(link)
          try:
           wait = WebDriverWait(driver1, 15)
           article_dict['titre'] = titre
           article_dict['authors'] = authors
           article_dict['PMID'] = pmid
           p_tags = driver1.find_elements_by_tag_name("p")
           content=[]
           for tag in p_tags:
             if tag.text.strip() != "":
               content.append(tag.text)
           article_dict['content'] = content
           article_dict['abstract'] = abstract
           article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
           article_dict['News_paper'] = "degruyter"
           article_dict['Query'] = self.term
           if f"data{i}" in all_results:
               all_results[f"data{i}"].update(article_dict)
           else:
              all_results[f"data{i}"] = article_dict
           json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
          except:
            
             pass

        elif "nature.com" in current_url:
          driver1.get(link)
          try:
           wait = WebDriverWait(driver1, 15)
           article_dict['titre'] = titre
           article_dict['authors'] = authors
           article_dict['PMID'] = pmid
           p_tags = driver1.find_elements_by_tag_name("p")
           content=[]
           for tag in p_tags:
             if tag.text.strip() != "":
               content.append(tag.text)
           article_dict['content'] = content
           article_dict['abstract'] = abstract
           article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
           article_dict['News_paper'] = "nature"
           article_dict['Query'] = self.term
           if f"data{i}" in all_results:
               all_results[f"data{i}"].update(article_dict)
           else:
              all_results[f"data{i}"] = article_dict
           json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
           driver1.get(page_url)
          except:
            
             pass

        elif "journals.sagepub.com" in current_url:
          driver1.get(link)
          try:
           try:
              WebDriverWait(driver1, 15).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='qc-cmp2-ui']/div[2]/div/button[3]"))).click()
           except:
              pass
           wait = WebDriverWait(driver1, 15)
           article_dict['titre'] = titre
           article_dict['authors'] = authors
           article_dict['PMID'] = pmid
           content = wait.until(EC.presence_of_elements_located((By.TAG_NAME,"section")))
           Content=[]
           for tag in content:
             if tag.text.strip() != "":
               Content.append(tag.text)
           article_dict['content'] = Content
           article_dict['abstract'] = abstract
           article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
           article_dict['News_paper'] =  "journals.sagepub"
           article_dict['Query'] = self.term
           if f"data{i}" in all_results:
               all_results[f"data{i}"].update(article_dict)
           else:
              all_results[f"data{i}"] = article_dict
           json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')  
           driver1.get(page_url)
          except:
            
             pass

        elif "tandfonline.com" in current_url:
          try:
           driver1.get(current_url)
           wait = WebDriverWait(driver1, 15)
           article_dict['titre'] = titre
           article_dict['authors'] = authors
           article_dict['PMID'] = pmid
           p_tags = driver1.find_elements_by_tag_name("p")
           content=[]
           for tag in p_tags:
             if tag.text.strip() != "":
               content.append(tag.text)
           article_dict['content'] = content
           article_dict['abstract'] = abstract
           article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
           article_dict['News_paper'] = "tandfonline"
           article_dict['Query'] = self.term
           if f"data{i}" in all_results:
               all_results[f"data{i}"].update(article_dict)
           else:
              all_results[f"data{i}"] = article_dict
           json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
           driver1.get(page_url)
          except:
            
             pass

        elif "amegroups.com" in current_url:
          driver1.get(link)
          try:
           wait = WebDriverWait(driver1, 5)
           article_dict['titre'] = titre
           article_dict['authors'] = authors
           article_dict['PMID'] = pmid
           p_tags = driver1.find_elements_by_tag_name("p")
           content=[]
           for tag in p_tags:
             if tag.text.strip() != "":
               content.append(tag.text)
           article_dict['content'] = content
           article_dict['abstract'] = abstract
           article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
           article_dict['News_paper'] = "amegroups"
           article_dict['Query'] = self.term
           if f"data{i}" in all_results:
               all_results[f"data{i}"].update(article_dict)
           else:
              all_results[f"data{i}"] = article_dict
           json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
          except:
           
             pass

        elif "frontiersin.org" in current_url:
          driver1.get(link)
          try:
           wait = WebDriverWait(driver1, 5)
           article_dict['titre'] = titre
           article_dict['authors'] = authors
           article_dict['PMID'] = pmid
           p_tags = driver1.find_elements_by_tag_name("p")
           content=[]
           for tag in p_tags:
             if tag.text.strip() != "":
               content.append(tag.text)
           article_dict['content'] = content
           article_dict['abstract'] = abstract
           article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
           article_dict['News_paper'] = "frontiersin"
           article_dict['Query'] = self.term
           if f"data{i}" in all_results:
               all_results[f"data{i}"].update(article_dict)
           else:
              all_results[f"data{i}"] = article_dict
           json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
          except:
            
             pass

        elif "bmj.com" in current_url:
          driver1.get(link)
          try:
           wait = WebDriverWait(driver1, 5)
           article_dict['titre'] = titre
           article_dict['authors'] = authors
           article_dict['PMID'] = pmid
           p_tags = driver1.find_elements_by_tag_name("p")
           content=[]
           for tag in p_tags:
             if tag.text.strip() != "":
               content.append(tag.text)
           article_dict['content'] = content
           article_dict['abstract'] = abstract
           article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
           article_dict['News_paper'] = "bmj"
           article_dict['Query'] = self.term
           if f"data{i}" in all_results:
               all_results[f"data{i}"].update(article_dict)
           else:
              all_results[f"data{i}"] = article_dict
           json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
          except:
             pass

        elif "biomedcentral.com" in current_url:
          driver1.get(link)
          sleep(6)
          try: 
           wait = WebDriverWait(driver1, 5)
           article_dict['titre'] = titre
           article_dict['authors'] = authors
           article_dict['PMID'] = pmid
           p_tags = driver1.find_elements_by_tag_name("p")
           content=[]
           for tag in p_tags:
             if tag.text.strip() != "":
               content.append(tag.text)
           article_dict['content'] = content
           article_dict['abstract'] = abstract
           article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
           article_dict['News_paper'] = "biomedcentral"
           article_dict['Query'] = self.term
           if f"data{i}" in all_results:
               all_results[f"data{i}"].update(article_dict)
           else:
              all_results[f"data{i}"] = article_dict
           json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
          except:
            
             pass
         
        elif "karger.com" in current_url:
          driver1.get(link)
          try:
           wait = WebDriverWait(driver1, 5)
           WebDriverWait(driver1, 15).until(EC.visibility_of_element_located((By.ID, "cmpbntyestxt"))).click()
           article_dict['titre'] = titre
           article_dict['authors'] = authors
           article_dict['PMID'] = pmid
           p_tags = driver1.find_elements_by_tag_name("p")
           content=[]
           for tag in p_tags:
             if tag.text.strip() != "":
               content.append(tag.text)
           article_dict['content'] = content
           article_dict['abstract'] = abstract
           article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
           article_dict['News_paper'] = "karger"
           article_dict['Query'] = self.term
           if f"data{i}" in all_results:
               all_results[f"data{i}"].update(article_dict)
           else:
              all_results[f"data{i}"] = article_dict
           json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
          except:
            
             pass

        elif "uliege.be" in current_url:
          driver1.get(link)
          try:
           wait = WebDriverWait(driver1, 5)
           article_dict['titre'] = titre
           article_dict['authors'] = authors
           article_dict['PMID'] = pmid
           p_tags = driver1.find_elements_by_tag_name("p")
           content=[]
           for tag in p_tags:
             if tag.text.strip() != "":
               content.append(tag.text)
           article_dict['content'] = content
           article_dict['abstract'] = abstract
           article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
           article_dict['News_paper'] = "uliege"
           article_dict['Query'] = self.term
           if f"data{i}" in all_results:
               all_results[f"data{i}"].update(article_dict)
           else:
              all_results[f"data{i}"] = article_dict
           json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
          except:
            
             pass
        
        elif "nih.gov" in current_url:
          driver1.get(link)
          try:
           wait = WebDriverWait(driver1, 5)
           article_dict['titre'] = titre
           article_dict['authors'] = authors
           article_dict['PMID'] = pmid
           p_tags = driver1.find_elements_by_tag_name("p")
           content=[]
           for tag in p_tags:
             if tag.text.strip() != "":
               content.append(tag.text)
           article_dict['content'] = content
           article_dict['abstract'] = abstract
           article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
           article_dict['News_paper'] = "nih"
           article_dict['Query'] = self.term
           if f"data{i}" in all_results:
               all_results[f"data{i}"].update(article_dict)
           else:
              all_results[f"data{i}"] = article_dict
           json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
          except:
            
             pass
        elif "lww" in current_url:
          driver1.get(link)
          try:     
            wait = WebDriverWait(driver1, 10)
            try:
             WebDriverWait(driver1, 10).until(EC.visibility_of_element_located((By.ID, "onetrust-reject-all-handler"))).click() 
            except:
               pass                                        
            article_dict['titre'] = titre
            article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
            article_dict['authors'] = authors
            article_dict['PMID'] = pmid
            content_divs = driver1.find_elements(By.TAG_NAME, "p")
            Content_texts=[]
            for div in content_divs:
               Content_texts.append(div.text)
            Content_text=list(set(Content_texts))
            article_dict['content'] = Content_text
            article_dict['abstract'] = abstract
            article_dict['News_paper'] = "lww"
            article_dict['Query'] = self.term
            if f"data{i}" in all_results:
                all_results[f"data{i}"].update(article_dict)
            else:
                all_results[f"data{i}"] = article_dict
            json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
          except:
            
             pass
        elif "europeanreview" in current_url:
          driver1.get(link)
          try:     
            wait = WebDriverWait(driver1, 10)                                        
            article_dict['titre'] = titre
            article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
            article_dict['authors'] = authors
            article_dict['PMID'] = pmid
            content_divs = driver1.find_elements(By.TAG_NAME, "p")
            Content_texts=[]
            for div in content_divs:
               Content_texts.append(div.text)
            Content_text=list(set(Content_texts))
            article_dict['content'] = Content_text
            article_dict['abstract'] = abstract
            article_dict['News_paper'] = "europeanreview"
            article_dict['Query'] = self.term
            if f"data{i}" in all_results:
                all_results[f"data{i}"].update(article_dict)
            else:
                all_results[f"data{i}"] = article_dict
            json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
          except:
            
             pass
        elif "bioscientifica" in current_url:
          driver1.get(link)
          try:     
            wait = WebDriverWait(driver1, 10)                                        
            article_dict['titre'] = titre
            article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
            article_dict['authors'] = authors
            article_dict['PMID'] = pmid
            content_divs = driver1.find_elements(By.TAG_NAME, "p")
            Content_texts=[]
            for div in content_divs:
               Content_texts.append(div.text)
            Content_text=list(set(Content_texts))
            article_dict['content'] = Content_text
            article_dict['abstract'] = abstract
            article_dict['News_paper'] = "bioscientifica"
            article_dict['Query'] = self.term
            if f"data{i}" in all_results:
                all_results[f"data{i}"].update(article_dict)
            else:
                all_results[f"data{i}"] = article_dict
            json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
          except:
            
             pass
        elif "futuremedicine" in current_url:
          try:     
            wait = WebDriverWait(driver1, 10)                                        
            article_dict['titre'] = titre
            article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
            article_dict['authors'] = authors
            article_dict['PMID'] = pmid
            content_divs = driver1.find_elements(By.TAG_NAME, "p")
            Content_texts=[]
            for div in content_divs:
               Content_texts.append(div.text)
            Content_text=list(set(Content_texts))
            article_dict['content'] = Content_text
            article_dict['abstract'] = abstract
            article_dict['News_paper'] = "futuremedicine"
            article_dict['Query'] = self.term
            if f"data{i}" in all_results:
                all_results[f"data{i}"].update(article_dict)
            else:
                all_results[f"data{i}"] = article_dict
            json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
          except:
            
             pass
        elif "liebertpub" in current_url:
          driver1.get(link)
          try:     
            wait = WebDriverWait(driver1, 10)                                        
            article_dict['titre'] = titre
            article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
            article_dict['authors'] = authors
            article_dict['PMID'] = pmid
            content_divs = driver1.find_elements(By.TAG_NAME, "p")
            Content_texts=[]
            for div in content_divs:
               Content_texts.append(div.text)
            Content_text=list(set(Content_texts))
            article_dict['content'] = Content_text
            article_dict['abstract'] = abstract
            article_dict['News_paper'] =  "liebertpub"
            article_dict['Query'] = self.term
            if f"data{i}" in all_results:
                all_results[f"data{i}"].update(article_dict)
            else:
                all_results[f"data{i}"] = article_dict
            json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
          except:
            
             pass
        elif "spandidos-publications" in current_url:
          driver1.get(current_url)
          try:     
            wait = WebDriverWait(driver1, 10)                                        
            article_dict['titre'] = titre
            article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
            article_dict['authors'] = authors
            article_dict['PMID'] = pmid
            content_divs = driver1.find_elements(By.TAG_NAME, "p")
            content=driver1.find_element(By.ID, "articleAbstract")
            Content_texts=[]
            Content_texts.append(content.text)
            for div in content_divs:
               Content_texts.append(div.text)
            Content_text=list(set(Content_texts))
            article_dict['content'] = Content_text
            article_dict['abstract'] = abstract
            article_dict['News_paper'] =  "spandidos-publications"
            article_dict['Query'] = self.term
            if f"data{i}" in all_results:
                all_results[f"data{i}"].update(article_dict)
            else:
                all_results[f"data{i}"] = article_dict
            json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
          except:
            
             pass
        elif "jamanetwork" in current_url:
          driver1.get(link)
          try:     
            wait = WebDriverWait(driver1, 10)                                        
            article_dict['titre'] = titre
            article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
            article_dict['authors'] = authors
            article_dict['PMID'] = pmid
            content_divs = driver1.find_elements(By.TAG_NAME, "p")
            Content_texts=[]
            for div in content_divs:
               Content_texts.append(div.text)
            Content_text=list(set(Content_texts))
            article_dict['content'] = Content_text
            article_dict['abstract'] = abstract
            article_dict['News_paper'] = "jamanetwork"
            article_dict['Query'] = self.term
            if f"data{i}" in all_results:
                all_results[f"data{i}"].update(article_dict)
            else:
                all_results[f"data{i}"] = article_dict
            json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
          except:
            
             pass
        elif "scielo" in current_url:
          driver1.get(link)
          try:     
            wait = WebDriverWait(driver1, 10)                                        
            article_dict['titre'] = titre
            article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
            article_dict['authors'] = authors
            article_dict['PMID'] = pmid
            content_divs = driver1.find_elements(By.TAG_NAME, "p")
            Content_texts=[]
            for div in content_divs:
               Content_texts.append(div.text)
            Content_text=list(set(Content_texts))
            article_dict['content'] = Content_text
            article_dict['abstract'] = abstract
            article_dict['News_paper'] = "scielo" 
            article_dict['Query'] = self.term
            if f"data{i}" in all_results:
                all_results[f"data{i}"].update(article_dict)
            else:
                all_results[f"data{i}"] = article_dict
            json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
          except:
            
             pass
        elif "medsci" in current_url:
          driver1.get(link)
          try:     
            wait = WebDriverWait(driver1, 10)                                        
            article_dict['titre'] = titre
            article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
            article_dict['authors'] = authors
            article_dict['PMID'] = pmid
            content_divs = driver1.find_elements(By.TAG_NAME, "p")
            Content_texts=[]
            for div in content_divs:
               Content_texts.append(div.text)
            Content_text=list(set(Content_texts))
            article_dict['content'] = Content_text
            article_dict['abstract'] = abstract
            article_dict['News_paper'] = "medsci"
            article_dict['Query'] = self.term
            if f"data{i}" in all_results:
                all_results[f"data{i}"].update(article_dict)
            else:
                all_results[f"data{i}"] = article_dict
            json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
          except:
            
             pass
        elif "dovepress" in current_url:
          driver1.get(link)
          try:     
            wait = WebDriverWait(driver1, 10)                                        
            article_dict['titre'] = titre
            article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
            article_dict['authors'] = authors
            article_dict['PMID'] = pmid
            content_divs = driver1.find_elements(By.TAG_NAME, "p")
            Content_texts=[]
            for div in content_divs:
               Content_texts.append(div.text)
            Content_text=list(set(Content_texts))
            article_dict['content'] = Content_text
            article_dict['abstract'] = abstract
            article_dict['News_paper'] = "dovepress" 
            article_dict['Query'] = self.term
            if f"data{i}" in all_results:
                all_results[f"data{i}"].update(article_dict)
            else:
                all_results[f"data{i}"] = article_dict
            json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
          except:
            
             pass
        elif "ecerm" in current_url:
          driver1.get(link)
          try: 
            wait = WebDriverWait(driver1, 10)                                        
            article_dict['titre'] = titre
            article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
            article_dict['authors'] = authors
            article_dict['PMID'] = pmid
            content_divs = driver1.find_element(By.CLASS_NAME, "section")
            text1=driver1.find_element(By.CLASS_NAME, "body")
            Content_texts=[]
            Content_texts.append(content_divs.text)
            Content_texts.append(text1.text)
            Content_text=list(set(Content_texts))
            article_dict['content'] = Content_text
            article_dict['abstract'] = abstract
            article_dict['News_paper'] =  "ecerm"
            article_dict['Query'] = self.term
            if f"data{i}" in all_results:
                all_results[f"data{i}"].update(article_dict)
            else:
                all_results[f"data{i}"] = article_dict
            json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
          except:
            
             pass
        elif "eurekaselect" in current_url:
          driver1.get(link)
          try:     
            wait = WebDriverWait(driver1, 10)                                        
            article_dict['titre'] = titre
            try:
             article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
            except:
              element=driver1.find_elements(By.XPATH,"/html/body/section/div/div/div[2]/div/div/p[2]")
              article_dict['DATE_PUBLICATION'] =remove_repeated_words(extract_date_and_year(element.text))
            article_dict['authors'] = authors
            article_dict['PMID'] = pmid
            content_divs = driver1.find_elements(By.CLASS_NAME, "card-body")
            Content_texts=[]
            for div in content_divs:
               Content_texts.append(div.text)
            Content_text=list(set(Content_texts))
            article_dict['content'] = Content_text
            article_dict['abstract'] = abstract
            article_dict['News_paper'] = "eurekaselect"
            article_dict['Query'] = self.term
            if f"data{i}" in all_results:
                all_results[f"data{i}"].update(article_dict)
            else:
                all_results[f"data{i}"] = article_dict
            json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
          except:
            
             pass
        elif "jcancer" in current_url:
          driver1.get(link)
          try:     
            wait = WebDriverWait(driver1, 10)                                        
            article_dict['titre'] = titre
            article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
            article_dict['authors'] = authors
            article_dict['PMID'] = pmid
            content_divs = driver1.find_elements(By.TAG_NAME, "p")
            Content_texts=[]
            for div in content_divs:
               Content_texts.append(div.text)
            Content_text=list(set(Content_texts))
            article_dict['content'] = Content_text
            article_dict['abstract'] = abstract
            article_dict['News_paper'] = "jcancer"
            article_dict['Query'] = self.term
            if f"data{i}" in all_results:
                all_results[f"data{i}"].update(article_dict)
            else:
                all_results[f"data{i}"] = article_dict
            json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
          except:
            
             pass
        elif "hindawi" in current_url:
          driver1.get(link)
          try:     
            wait = WebDriverWait(driver1, 10)                                        
            article_dict['titre'] = titre
            article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
            article_dict['authors'] = authors
            article_dict['PMID'] = pmid
            content_divs = driver1.find_element(By.CLASS_NAME, "xml-content")
            article_dict['content'] = content_divs.text
            article_dict['abstract'] = abstract
            article_dict['News_paper'] = "hindawi"
            article_dict['Query'] = self.term
            if f"data{i}" in all_results:
                all_results[f"data{i}"].update(article_dict)
            else:
                all_results[f"data{i}"] = article_dict
            json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
          except:
            
             pass
        elif "viamedica" in current_url:
          driver1.get(link)
          try:     
            wait = WebDriverWait(driver1, 10)                                        
            wait = WebDriverWait(driver1, 10)                                        
            article_dict['titre'] = titre
            article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
            article_dict['authors'] = authors
            article_dict['PMID'] = pmid
            content_divs = driver1.find_elements(By.TAG_NAME, "p")
            Content_texts=[]
            for div in content_divs:
               Content_texts.append(div.text)
            Content_text=list(set(Content_texts))
            article_dict['content'] = Content_text
            article_dict['abstract'] = abstract
            article_dict['News_paper'] = "viamedica"
            article_dict['Query'] = self.term
            if f"data{i}" in all_results:
                all_results[f"data{i}"].update(article_dict)
            else:
                all_results[f"data{i}"] = article_dict
            json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
          except:
            
             pass
        elif "ojs.ptbioch.edu.pl" in current_url:
          driver1.get(link)
          try:     
            wait = WebDriverWait(driver1, 10)                                        
            article_dict['titre'] = titre
            article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
            article_dict['authors'] = authors
            article_dict['PMID'] = pmid
            content_divs = driver1.find_elements(By.TAG_NAME, "p")
            Content_texts=[]
            for div in content_divs:
               Content_texts.append(div.text)
            Content_text=list(set(Content_texts))
            article_dict['content'] = Content_text
            article_dict['abstract'] = abstract
            article_dict['News_paper'] = "ojs.ptbioch.edu.pl" 
            article_dict['Query'] = self.term
            if f"data{i}" in all_results:
                all_results[f"data{i}"].update(article_dict)
            else:
                all_results[f"data{i}"] = article_dict
            json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
          except:
            
             pass
        elif "journals.plos.org" in current_url:
          driver1.get(link)
          try:     
            wait = WebDriverWait(driver1, 10)
            try:
             WebDriverWait(driver1, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "_19RPUZBjdy2iuONl+jvOiQ=="))).click() 
            except:
               pass                                        
            article_dict['titre'] = titre
            article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
            article_dict['authors'] = authors
            article_dict['PMID'] = pmid
            content_divs = driver1.find_elements(By.TAG_NAME, "p")
            Content_texts=[]
            for div in content_divs:
               Content_texts.append(div.text)
            Content_text=list(set(Content_texts))
            article_dict['content'] = Content_text
            article_dict['abstract'] = abstract
            article_dict['News_paper'] = "journals.plos"
            article_dict['Query'] = self.term
            if f"data{i}" in all_results:
                all_results[f"data{i}"].update(article_dict)
            else:
                all_results[f"data{i}"] = article_dict
            json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
          except:
            
             pass
        elif "aging-us" in current_url:
          driver1.get(link)
          try:     
            wait = WebDriverWait(driver1, 10)                                       
            article_dict['titre'] = titre
            article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
            article_dict['authors'] = authors
            article_dict['PMID'] = pmid
            content_divs = driver1.find_elements(By.TAG_NAME, "p")
            Content_texts=[]
            for div in content_divs:
               Content_texts.append(div.text)
            Content_text=list(set(Content_texts))
            article_dict['content'] = Content_text
            article_dict['abstract'] = abstract
            article_dict['News_paper'] = "aging-us"
            article_dict['Query'] = self.term
            if f"data{i}" in all_results:
                all_results[f"data{i}"].update(article_dict)
            else:
                all_results[f"data{i}"] = article_dict
            json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
          except:
            
             pass
        elif "academic.oup" in current_url:
          driver1.get(link)
          try:     
            wait = WebDriverWait(driver1, 10)                                       
            article_dict['titre'] = titre
            article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
            article_dict['authors'] = authors
            article_dict['PMID'] = pmid
            content_divs = driver1.find_elements(By.TAG_NAME, "p")
            Content_texts=[]
            for div in content_divs:
               Content_texts.append(div.text)
            Content_text=list(set(Content_texts))
            article_dict['content'] = Content_text
            article_dict['abstract'] = abstract
            article_dict['News_paper'] = "academic.oup"
            article_dict['Query'] = self.term
            if f"data{i}" in all_results:
                all_results[f"data{i}"].update(article_dict)
            else:
                all_results[f"data{i}"] = article_dict
            json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
          except:
            
             pass
        elif "futuremedicine" in current_url:
          driver1.get(link)
          try:     
            wait = WebDriverWait(driver1, 10)                                       
            article_dict['titre'] = titre
            article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
            article_dict['authors'] = authors
            article_dict['PMID'] = pmid
            content_divs = driver1.find_elements(By.TAG_NAME, "p")
            Content_texts=[]
            for div in content_divs:
               Content_texts.append(div.text)
            Content_text=list(set(Content_texts))
            article_dict['content'] = Content_text
            article_dict['abstract'] = abstract
            article_dict['News_paper'] = "futuremedicine"
            article_dict['Query'] = self.term
            if f"data{i}" in all_results:
                all_results[f"data{i}"].update(article_dict)
            else:
                all_results[f"data{i}"] = article_dict
            json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
          except:
            
             pass
        elif "ias.ac.in" in link:
          try: 
           driver1.get(CURRENT)
           wait = WebDriverWait(driver1, 15)
           article_dict['titre'] = titre
           article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
           article_dict['authors'] = authors
           article_dict['PMID'] = pmid
           try:
             p_tags = driver1.find_elements_by_tag_name("p")
             content = []
             for tag in p_tags:
               if tag.text.strip() != "":
                content.append(tag.text)
             article_dict['content'] = content
             article_dict['abstract'] = abstract
             article_dict['News_paper'] = "ias.ac.in"
             article_dict['Query'] = self.term
             if f"data{i}" in all_results:
              all_results[f"data{i}"].update(article_dict)
             else:
              all_results[f"data{i}"] = article_dict
             json_data2 =json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
           except:
             pass
          except:
           
             pass
        elif "elis.sk" in current_url:
          driver1.get(link)
          try:
           sleep(7)
           wait = WebDriverWait(driver1, 15)
           article_dict['titre'] = titre
           article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
           article_dict['authors'] = authors
           article_dict['PMID'] = pmid
           try:
             p_tags = driver1.find_element_by_xpath("//*[@id='vmMainPage']/table/tbody/tr[5]/td")
             article_dict['content'] = p_tags.text
             article_dict['abstract'] = abstract
             article_dict['News_paper'] = "elis.sk"
             article_dict['Query'] = self.term
             if f"data{i}" in all_results:
              all_results[f"data{i}"].update(article_dict)
             else:
              all_results[f"data{i}"] = article_dict
             json_data2 =json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
           except:
             pass
          except:
            
             pass
           
        elif "iv.iiarjournals" in current_url:
          driver1.get(link)
          try:
           wait = WebDriverWait(driver1, 15)
           article_dict['titre'] = titre
           article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
           article_dict['authors'] = authors
           article_dict['PMID'] = pmid
           try:
             p_tags = driver1.find_elements_by_tag_name("p")
             content = []
             for tag in p_tags:
               if tag.text.strip() != "":
                content.append(tag.text)
             article_dict['content'] = content
             article_dict['abstract'] = abstract
             article_dict['News_paper'] = "iv.iiarjournals"
             article_dict['Query'] = self.term
             if f"data{i}" in all_results:
              all_results[f"data{i}"].update(article_dict)
             else:
              all_results[f"data{i}"] = article_dict
             json_data2 =json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
           except:
             pass
          except:
            
             pass
        elif "thno" in current_url:
          driver1.get(link)
          try:
           wait = WebDriverWait(driver1, 15)
           article_dict['titre'] = titre
           article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
           article_dict['authors'] = authors
           article_dict['PMID'] = pmid
           try:
             p_tags = driver1.find_elements_by_tag_name("p")
             content = []
             for tag in p_tags:
               if tag.text.strip() != "":
                content.append(tag.text)
             article_dict['content'] = content
             article_dict['abstract'] = abstract
             article_dict['News_paper'] = "thno"
             article_dict['Query'] = self.term
             if f"data{i}" in all_results:
              all_results[f"data{i}"].update(article_dict)
             else:
              all_results[f"data{i}"] = article_dict
             json_data2 =json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
           except:
             pass
          except:
            
             pass
        elif "iospress" in current_url:
          driver1.get(link)
          try:
           wait = WebDriverWait(driver1, 15)
           article_dict['titre'] = titre
           article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
           article_dict['authors'] = authors
           article_dict['PMID'] = pmid
           try:
             p_tags = driver1.find_elements_by_tag_name("p")
             content = []
             for tag in p_tags:
               if tag.text.strip() != "":
                content.append(tag.text)
             article_dict['content'] = content
             article_dict['abstract'] = abstract
             article_dict['News_paper'] = "iospress"
             article_dict['Query'] = self.term
             if f"data{i}" in all_results:
              all_results[f"data{i}"].update(article_dict)
             else:
              all_results[f"data{i}"] = article_dict
             json_data2 =json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
           except:
             pass
          except:
            
             pass
        elif "liebertpub" in current_url:
          driver1.get(link)
          try:
           wait = WebDriverWait(driver1, 15)
           article_dict['titre'] = titre
           article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
           article_dict['authors'] = authors
           article_dict['PMID'] = pmid
           try:
             p_tags = driver1.find_elements_by_tag_name("p")
             content = []
             for tag in p_tags:
               if tag.text.strip() != "":
                content.append(tag.text)
             article_dict['content'] = content
             article_dict['abstract'] = abstract
             article_dict['News_paper'] = "liebertpub"
             article_dict['Query'] = self.term
             if f"data{i}" in all_results:
              all_results[f"data{i}"].update(article_dict)
             else:
              all_results[f"data{i}"] = article_dict
             json_data2 =json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
           except:
             pass
          except:
            
             pass
        elif "pubs.rsc" in current_url:
          driver1.get(link)
          try:
           wait = WebDriverWait(driver1, 15)
           article_dict['titre'] = titre
           article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
           article_dict['authors'] = authors
           article_dict['PMID'] = pmid
           try:
             p_tags = driver1.find_elements_by_tag_name("p")
             content = []
             for tag in p_tags:
               if tag.text.strip() != "":
                content.append(tag.text)
             article_dict['content'] = content
             article_dict['abstract'] = abstract
             article_dict['News_paper'] = "pubs.rsc"
             article_dict['Query'] = self.term
             if f"data{i}" in all_results:
              all_results[f"data{i}"].update(article_dict)
             else:
              all_results[f"data{i}"] = article_dict
             json_data2 =json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
           except:
             pass
          except:
           
             pass
        elif "aacrjournals" in current_url:
          driver1.get(link)
          try:
           wait = WebDriverWait(driver1, 15)
           article_dict['titre'] = titre
           article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
           article_dict['authors'] = authors
           article_dict['PMID'] = pmid
           try:
             p_tags = driver1.find_elements_by_tag_name("p")
             content = []
             for tag in p_tags:
               if tag.text.strip() != "":
                content.append(tag.text)
             article_dict['content'] = content
             article_dict['abstract'] = abstract
             article_dict['News_paper'] = "aacrjournals" 
             article_dict['Query'] = self.term
             if f"data{i}" in all_results:
              all_results[f"data{i}"].update(article_dict)
             else:
              all_results[f"data{i}"] = article_dict
             json_data2 =json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
           except:
             pass
          except:
            
             pass
        elif "science" in current_url:
          driver1.get(link)
          try:
           wait = WebDriverWait(driver1, 15)
           article_dict['titre'] = titre
           article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
           article_dict['authors'] = authors
           article_dict['PMID'] = pmid
           try:
             p_tags = driver1.find_elements_by_class_name("core-container")
             content = []
             for tag in p_tags:
               if tag.text.strip() != "":
                content.append(tag.text)
             article_dict['content'] = content
             article_dict['abstract'] = abstract
             article_dict['News_paper'] = "science"
             article_dict['Query'] = self.term
             if f"data{i}" in all_results:
              all_results[f"data{i}"].update(article_dict)
             else:
              all_results[f"data{i}"] = article_dict
             json_data2 =json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
           except:
             pass
          except:
            
             pass
        elif "ingentaconnect" in current_url:
          driver1.get(link)
          try:
           wait = WebDriverWait(driver1, 15)
           article_dict['titre'] = titre
           article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
           article_dict['authors'] = authors
           article_dict['PMID'] = pmid
           try:
             p_tags = driver1.find_element_by_class_name("tab-content")
             article_dict['content'] =p_tags.text
             article_dict['abstract'] = abstract
             article_dict['News_paper'] = "ingentaconnect"
             article_dict['Query'] = self.term
             if f"data{i}" in all_results:
              all_results[f"data{i}"].update(article_dict)
             else:
              all_results[f"data{i}"] = article_dict
             json_data2 =json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
           except:
             pass
          except:
            
             pass
        elif "bmbreports" in current_url:
          driver1.get(link)
          try:
           wait = WebDriverWait(driver1, 15)
           article_dict['titre'] = titre
           article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
           article_dict['authors'] = authors
           article_dict['PMID'] = pmid
           try:
             p_tags = driver1.find_elements_by_class_name("section")
             content = []
             seen_text = set() # keep track of unique texts
             for tag in p_tags:
              text = tag.text.strip()
              if text != "" and text not in seen_text: # check if text is not empty and not already seen
                content.append(text)
                seen_text.add(text)
             article_dict['content'] = text
             article_dict['abstract'] = abstract
             article_dict['News_paper'] = "bmbreports"
             article_dict['Query'] = self.term
             if f"data{i}" in all_results:
              all_results[f"data{i}"].update(article_dict)
             else:
              all_results[f"data{i}"] = article_dict
             json_data2 =json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
           except:
             pass
          except:
            
             pass
        elif "journal.waocp" in current_url:
          driver1.get(link)
          try:
           wait = WebDriverWait(driver1, 15)
           article_dict['titre'] = titre
           article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
           article_dict['authors'] = authors
           article_dict['PMID'] = pmid
           try:
             p_tags = driver1.find_element_by_class_name("padding_abstract justify ltr")
             article_dict['content'] = p_tags.text
             article_dict['abstract'] = abstract
             article_dict['News_paper'] = "journal.waocp"
             article_dict['Query'] = self.term
             if f"data{i}" in all_results:
              all_results[f"data{i}"].update(article_dict)
             else:
              all_results[f"data{i}"] = article_dict
             json_data2 =json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
           except:
             pass
          except:
            
             pass
        elif "portlandpress" in current_url:
          driver1.get(link)
          try:
           wait = WebDriverWait(driver1, 15)
           article_dict['titre'] = titre
           article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
           article_dict['authors'] = authors
           article_dict['PMID'] = pmid
           try:
             p_tags = driver1.find_elements_by_tag_name("p")
             content = []
             for tag in p_tags:
               if tag.text.strip() != "":
                content.append(tag.text)
             article_dict['content'] = content
             article_dict['abstract'] = abstract
             article_dict['News_paper'] = "portlandpress"
             article_dict['Query'] = self.term
             if f"data{i}" in all_results:
              all_results[f"data{i}"].update(article_dict)
             else:
              all_results[f"data{i}"] = article_dict
             json_data2 =json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
           except:
             pass
          except:
            
             pass
        elif "royalsocietypublishing" in current_url:
          driver1.get(link)
          try:
           wait = WebDriverWait(driver1, 15)
           article_dict['titre'] = titre
           article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
           article_dict['authors'] = authors
           article_dict['PMID'] = pmid
           try:
             p_tags = driver1.find_elements_by_tag_name("p")
             content = []
             for tag in p_tags:
               if tag.text.strip() != "":
                content.append(tag.text)
             article_dict['content'] = content
             article_dict['abstract'] = abstract
             article_dict['News_paper'] = "royalsocietypublishing"
             article_dict['Query'] = self.term
             if f"data{i}" in all_results:
              all_results[f"data{i}"].update(article_dict)
             else:
              all_results[f"data{i}"] = article_dict
             json_data2 =json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
           except:
             pass
          except:
            
             pass
        elif "embopress" in current_url:
          driver1.get(link)
          try:
           wait = WebDriverWait(driver1, 15)
           article_dict['titre'] = titre
           article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
           article_dict['authors'] = authors
           article_dict['PMID'] = pmid
           try:
             p_tags = driver1.find_elements_by_tag_name("p")
             content = []
             for tag in p_tags:
               if tag.text.strip() != "":
                content.append(tag.text)
             article_dict['content'] = content
             article_dict['abstract'] = abstract
             article_dict['News_paper'] = "embopress"
             article_dict['Query'] = self.term 
             if f"data{i}" in all_results:
              all_results[f"data{i}"].update(article_dict)
             else:
              all_results[f"data{i}"] = article_dict
             json_data2 =json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
           except:
             pass
          except:
            
             pass
        elif "pubs.acs" in current_url:
          driver1.get(link)
          try:
           wait = WebDriverWait(driver1, 15)
           article_dict['titre'] = titre
           article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
           article_dict['authors'] = authors
           article_dict['PMID'] = pmid
           try:
             p_tags = driver1.find_elements_by_tag_name("p")
             content = []
             for tag in p_tags:
               if tag.text.strip() != "":
                content.append(tag.text)
             article_dict['content'] = content
             article_dict['abstract'] = abstract
             article_dict['News_paper'] = "pubs.acs"
             article_dict['Query'] = self.term
             if f"data{i}" in all_results:
              all_results[f"data{i}"].update(article_dict)
             else:
              all_results[f"data{i}"] = article_dict
             json_data2 =json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
           except:
             pass
          except:
            
             pass
        elif "imrpress" in current_url:
          driver1.get(link)
          try:
           wait = WebDriverWait(driver1, 15)
           article_dict['titre'] = titre
           article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
           article_dict['authors'] = authors
           article_dict['PMID'] = pmid
           try:
             p_tags = driver1.find_elements_by_tag_name("p")
             content = []
             for tag in p_tags:
               if tag.text.strip() != "":
                content.append(tag.text)
             article_dict['content'] = content
             article_dict['abstract'] = abstract
             article_dict['News_paper'] = "imrpress"
             article_dict['Query'] = self.term
             if f"data{i}" in all_results:
              all_results[f"data{i}"].update(article_dict)
             else:
              all_results[f"data{i}"] = article_dict
             json_data2 =json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
           except:
             pass
          except:
            
             pass
        elif "ejgo" in current_url:
          driver1.get(link)
          try:
           wait = WebDriverWait(driver1, 15)
           article_dict['titre'] = titre
           article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
           article_dict['authors'] = authors
           article_dict['PMID'] = pmid
           try:
             p_tags = driver1.find_elements_by_tag_name("p")
             content = []
             for tag in p_tags:
               if tag.text.strip() != "":
                content.append(tag.text)
             article_dict['content'] = content
             article_dict['abstract'] = abstract
             article_dict['News_paper'] = "ejgo"
             article_dict['Query'] = self.term
             if f"data{i}" in all_results:
              all_results[f"data{i}"].update(article_dict)
             else:
              all_results[f"data{i}"] = article_dict
             json_data2 =json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
           except:
             pass
          except:
            
             pass
        elif "spandidos-publications" in current_url:
          driver1.get(link)
          try:
           wait = WebDriverWait(driver1, 15)
           article_dict['titre'] = titre
           article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
           article_dict['authors'] = authors
           article_dict['PMID'] = pmid
           try:
             p_tags = driver1.find_elements_by_tag_name("p")
             content = []
             for tag in p_tags:
               if tag.text.strip() != "":
                content.append(tag.text)
             article_dict['content'] = content
             article_dict['abstract'] = abstract
             article_dict['News_paper'] = "spandidos-publications"
             article_dict['Query'] = self.term
             if f"data{i}" in all_results:
              all_results[f"data{i}"].update(article_dict)
             else:
              all_results[f"data{i}"] = article_dict
             json_data2 =json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
           except:
             pass
          except:
            
             pass
        elif "eymj" in current_url:
          driver1.get(link)
          try:
           wait = WebDriverWait(driver1, 15)
           article_dict['titre'] = titre
           article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
           article_dict['authors'] = authors
           article_dict['PMID'] = pmid
           try:
             p_tags = driver1.find_elements_by_tag_name("p")
             content = []
             for tag in p_tags:
               if tag.text.strip() != "":
                content.append(tag.text)
             article_dict['content'] = content
             article_dict['abstract'] = abstract
             article_dict['News_paper'] = "eymj"
             article_dict['Query'] = self.term
             if f"data{i}" in all_results:
              all_results[f"data{i}"].update(article_dict)
             else:
              all_results[f"data{i}"] = article_dict
             json_data2 =json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
           except:
             pass
          except:
            
             pass
        elif "ejh" in current_url:
          driver1.get(link)
          try:
           wait = WebDriverWait(driver1, 15)
           article_dict['titre'] = titre
           article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
           article_dict['authors'] = authors
           article_dict['PMID'] = pmid
           try:
             p_tags = driver1.find_elements_by_tag_name("p")
             content = []
             for tag in p_tags:
               if tag.text.strip() != "":
                content.append(tag.text)
             article_dict['content'] = content
             article_dict['abstract'] = abstract
             article_dict['News_paper'] = "ejh"
             article_dict['Query'] = self.term
             if f"data{i}" in all_results:
              all_results[f"data{i}"].update(article_dict)
             else:
              all_results[f"data{i}"] = article_dict
             json_data2 =json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
           except:
             pass
          except:
            
             pass
        elif "medscimonit" in current_url:
          driver1.get(link)
          try:
           wait = WebDriverWait(driver1, 15)
           article_dict['titre'] = titre
           article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
           article_dict['authors'] = authors
           article_dict['PMID'] = pmid
           try:
             p_tags = driver1.find_elements_by_tag_name("p")
             content = []
             for tag in p_tags:
               if tag.text.strip() != "":
                content.append(tag.text)
             article_dict['content'] = content
             article_dict['abstract'] = abstract
             article_dict['News_paper'] = "medscimonit"
             article_dict['Query'] = self.term
             if f"data{i}" in all_results:
              all_results[f"data{i}"].update(article_dict)
             else:
              all_results[f"data{i}"] = article_dict
             json_data2 =json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
           except:
             pass
          except:
            
             pass
        elif "hh.um" in current_url:
          driver1.get(link)
          try:
           wait = WebDriverWait(driver1, 15)
           try:
            article_dict['titre'] = titre
            article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
            article_dict['authors'] = authors
            article_dict['PMID'] = pmid
           except:
             pass
           try:
             p_tags = driver1.find_elements_by_tag_name("p")
             content = []
             for tag in p_tags:
               if tag.text.strip() != "":
                content.append(tag.text)
             article_dict['content'] = content
             article_dict['abstract'] = abstract
             article_dict['News_paper'] = "hh.um"
             article_dict['Query'] = self.term
             if f"data{i}" in all_results:
              all_results[f"data{i}"].update(article_dict)
             else:
              all_results[f"data{i}"] = article_dict
             json_data2 =json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
           except:
             pass
          except:
            
             pass
        elif "physoc.onlinelibrary.wiley" in current_url:
          driver1.get(link)
          try:
           wait = WebDriverWait(driver1, 15)
           article_dict['titre'] = titre
           article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
           article_dict['authors'] = authors
           article_dict['PMID'] = pmid
           try:
             p_tags = driver1.find_elements_by_tag_name("p")
             content = []
             for tag in p_tags:
               if tag.text.strip() != "":
                content.append(tag.text)
             article_dict['content'] = content
             article_dict['abstract'] = abstract
             article_dict['News_paper'] = "physoc.onlinelibrary.wiley"
             article_dict['Query'] = self.term
             if f"data{i}" in all_results:
              all_results[f"data{i}"].update(article_dict)
             else:
              all_results[f"data{i}"] = article_dict
             json_data2 =json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
             driver.get(page_url)
           except:
             pass
          except:
            
             pass
        elif "ieeexplore.ieee" in current_url:
          driver1.get(link)
          try:
           wait = WebDriverWait(driver1, 15)
           article_dict['titre'] = titre
           article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
           article_dict['authors'] = authors
           article_dict['PMID'] = pmid
           try:
             p_tags = driver1.find_element_by_xpath("//*[@id='xplMainContentLandmark']/div/xpl-document-details/div/div[1]/div/div[2]/section/div[2]/div/xpl-document-abstract/section/div[2]/div[1]/div/div/div")
             article_dict['content'] = p_tags.text
             article_dict['abstract'] = abstract
             article_dict['News_paper'] = "ieeexplore.ieee"
             article_dict['Query'] = self.term
             if f"data{i}" in all_results:
              all_results[f"data{i}"].update(article_dict)
             else:
              all_results[f"data{i}"] = article_dict
             json_data2 =json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
             driver.get(page_url)
           except:
             pass
          except:
            
             pass
        elif "sciengine" in current_url:
          driver1.get(link)
          try:
           wait = WebDriverWait(driver1, 15)
           article_dict['titre'] = titre
           article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
           article_dict['authors'] = authors
           article_dict['PMID'] = pmid
           try:
             p_tags = driver1.find_elements_by_tag_name("p")
             content = []
             for tag in p_tags:
               if tag.text.strip() != "":
                content.append(tag.text)
             article_dict['content'] = content
             article_dict['abstract'] = abstract
             article_dict['News_paper'] = "sciengine"
             article_dict['Query'] = self.term
             if f"data{i}" in all_results:
              all_results[f"data{i}"].update(article_dict)
             else:
              all_results[f"data{i}"] = article_dict
             json_data2 =json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
           except:
             pass
          except:
            
             pass
        elif "molecbio" in current_url:
          driver1.get(link)
          try:
           wait = WebDriverWait(driver1, 15)
           article_dict['titre'] = titre
           article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
           article_dict['authors'] = authors
           article_dict['PMID'] = pmid
           try:
             p_tags = driver1.find_elements_by_tag_name("p")
             content = []
             for tag in p_tags:
               if tag.text.strip() != "":
                content.append(tag.text)
             article_dict['content'] = content
             article_dict['abstract'] = abstract
             article_dict['News_paper'] = "molecbio" 
             article_dict['Query'] = self.term
             if f"data{i}" in all_results:
              all_results[f"data{i}"].update(article_dict)
             else:
              all_results[f"data{i}"] = article_dict
             json_data2 =json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
           except:
             pass
          except:
            
             pass
        elif "bjbms" in current_url:
          driver1.get(link)
          try:
           wait = WebDriverWait(driver1, 15)
           article_dict['titre'] = titre
           article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
           article_dict['authors'] = authors
           article_dict['PMID'] = pmid
           try:
             p_tags = driver1.find_elements_by_tag_name("p")
             content = []
             for tag in p_tags:
               if tag.text.strip() != "":
                content.append(tag.text)
             article_dict['content'] = content
             article_dict['abstract'] = abstract
             article_dict['News_paper'] = "bjbms"
             article_dict['Query'] = self.term
             if f"data{i}" in all_results:
              all_results[f"data{i}"].update(article_dict)
             else:
              all_results[f"data{i}"] = article_dict
             json_data2 =json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
           except:
             pass
          except:
            
             pass
        elif "worldscientific" in current_url:
          driver1.get(link)
          try:
           wait = WebDriverWait(driver1, 15)
           article_dict['titre'] = titre
           article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
           article_dict['authors'] = authors
           article_dict['PMID'] = pmid
           try:
             p_tags = driver1.find_elements_by_tag_name("p")
             content = []
             for tag in p_tags:
               if tag.text.strip() != "":
                content.append(tag.text)
             article_dict['content'] = content
             article_dict['abstract'] = abstract
             article_dict['News_paper'] = "worldscientific"
             article_dict['Query'] = self.term
             if f"data{i}" in all_results:
              all_results[f"data{i}"].update(article_dict)
             else:
              all_results[f"data{i}"] = article_dict
             json_data2 =json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
           except:
             pass
          except:
           
             pass
        elif "e-crt" in current_url:
          driver1.get(link)
          try:
           wait = WebDriverWait(driver1, 15)
           article_dict['titre'] = titre
           article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
           article_dict['authors'] = authors
           article_dict['PMID'] = pmid
           try:
             p_tags = driver1.find_elements_by_id("article-body")
             article_dict['content'] = p_tags.text
             article_dict['abstract'] = abstract
             article_dict['News_paper'] = "e-crt"
             article_dict['Query'] = self.term
             if f"data{i}" in all_results:
              all_results[f"data{i}"].update(article_dict)
             else:
              all_results[f"data{i}"] = article_dict
             json_data2 =json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
           except:
             pass
          except:
            
             pass
        elif "journals.aai" in current_url:
          driver1.get(link)
          try:
           wait = WebDriverWait(driver1, 15)
           article_dict['titre'] = titre
           article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
           article_dict['authors'] = authors
           article_dict['PMID'] = pmid
           try:
             p_tags = driver1.find_elements_by_tag_name("p")
             content = []
             for tag in p_tags:
               if tag.text.strip() != "":
                content.append(tag.text)
             article_dict['content'] = content
             article_dict['abstract'] = abstract
             article_dict['News_paper'] = "journals.aai"
             article_dict['Query'] = self.term
             if f"data{i}" in all_results:
              all_results[f"data{i}"].update(article_dict)
             else:
              all_results[f"data{i}"] = article_dict
             json_data2 =json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
           except:
             pass
          except:
            
             pass
        elif "jstage.jst.go" in current_url:
          driver1.get(link)
          try:
           wait = WebDriverWait(driver1, 15)
           article_dict['titre'] = titre
           article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
           article_dict['authors'] = authors
           article_dict['PMID'] = pmid
           try:
             p_tags = driver1.find_elements_by_tag_name("p")
             content = []
             for tag in p_tags:
               if tag.text.strip() != "":
                content.append(tag.text)
             article_dict['content'] = content
             article_dict['abstract'] = abstract
             article_dict['News_paper'] = "jstage.jst.go"
             article_dict['Query'] = self.term
             if f"data{i}" in all_results:
              all_results[f"data{i}"].update(article_dict)
             else:
              all_results[f"data{i}"] = article_dict
             json_data2 =json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
           except:
             pass
          except:
            
             pass
        elif "exp-oncology" in current_url:
          driver1.get(link)
          try:
           wait = WebDriverWait(driver1, 15)
           article_dict['titre'] = titre
           article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
           article_dict['authors'] = authors
           article_dict['PMID'] = pmid
           try:
             p_tags = driver1.find_elements_by_tag_name("p")
             content = []
             for tag in p_tags:
               if tag.text.strip() != "":
                content.append(tag.text)
             article_dict['content'] = content
             article_dict['abstract'] = abstract
             article_dict['News_paper'] = "exp-oncology"
             article_dict['Query'] = self.term
             if f"data{i}" in all_results:
              all_results[f"data{i}"].update(article_dict)
             else:
              all_results[f"data{i}"] = article_dict
             json_data2 =json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
           except:
             pass
          except:
            
             pass
        elif "oncotarget" in current_url:
          driver1.get(link)
          try:
           wait = WebDriverWait(driver1, 15)
           article_dict['titre'] = titre
           article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
           article_dict['authors'] = authors
           article_dict['PMID'] = pmid
           try:
             p_tags = driver1.find_elements_by_tag_name("p")
             content = []
             for tag in p_tags:
               if tag.text.strip() != "":
                content.append(tag.text)
             article_dict['content'] = content
             article_dict['abstract'] = abstract
             article_dict['News_paper'] = "oncotarget"
             article_dict['Query'] = self.term
             if f"data{i}" in all_results:
              all_results[f"data{i}"].update(article_dict)
             else:
              all_results[f"data{i}"] = article_dict
             json_data2 =json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
           except:
             pass
          except:
            
             pass
        elif "peerj" in current_url:
          driver1.get(link)
          try:
           wait = WebDriverWait(driver1, 15)
           article_dict['titre'] = titre
           article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
           article_dict['authors'] = authors
           article_dict['PMID'] = pmid
           try:
             p_tags = driver1.find_elements_by_tag_name("p")
             content = []
             for tag in p_tags:
               if tag.text.strip() != "":
                content.append(tag.text)
             article_dict['content'] = content
             article_dict['abstract'] = abstract
             article_dict['News_paper'] = "peerj"
             article_dict['Query'] = self.term
             if f"data{i}" in all_results:
              all_results[f"data{i}"].update(article_dict)
             else:
              all_results[f"data{i}"] = article_dict
             json_data2 =json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
           except:
             pass
          except:
            
             pass
        elif "genominfo" in current_url:
          driver1.get(link)
          try:
           wait = WebDriverWait(driver1, 15)
           article_dict['titre'] = titre
           article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
           article_dict['authors'] = authors
           article_dict['PMID'] = pmid
           try:
             p_tags = driver1.find_elements_by_class_name("section")
             content = []
             for tag in p_tags:
               if tag.text.strip() != "":
                content.append(tag.text)
             article_dict['content'] = content
             article_dict['abstract'] = abstract
             article_dict['News_paper'] = "genominfo"
             article_dict['Query'] = self.term
             if f"data{i}" in all_results:
              all_results[f"data{i}"].update(article_dict)
             else:
              all_results[f"data{i}"] = article_dict
             json_data2 =json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
           except:
             pass
          except:
            
             pass
        elif "erc.bioscientifica" in current_url:
          driver1.get(link)
          try:
           wait = WebDriverWait(driver1, 15)
           article_dict['titre'] = titre
           article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
           article_dict['authors'] = authors
           article_dict['PMID'] = pmid
           try:
             p_tags = driver1.find_elements_by_class_name("p")
             content = []
             for tag in p_tags:
               if tag.text.strip() != "":
                content.append(tag.text)
             article_dict['content'] = content
             article_dict['abstract'] = abstract
             article_dict['News_paper'] = "erc.bioscientifica"
             article_dict['Query'] = self.term
             if f"data{i}" in all_results:
              all_results[f"data{i}"].update(article_dict)
             else:
              all_results[f"data{i}"] = article_dict
             json_data2 =json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
           except:
             pass
          except:
            
             pass
        elif "researchsquare" in current_url:
          driver1.get(link)
          try:
           wait = WebDriverWait(driver1, 15)
           article_dict['titre'] = titre
           article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
           article_dict['authors'] = authors
           article_dict['PMID'] = pmid
           try:
             p_tags = driver1.find_elements_by_class_name("p")
             content = []
             for tag in p_tags:
               if tag.text.strip() != "":
                content.append(tag.text)
             article_dict['content'] = content
             article_dict['abstract'] = abstract
             article_dict['News_paper'] = "researchsquare"
             article_dict['Query'] = self.term
             if f"data{i}" in all_results:
              all_results[f"data{i}"].update(article_dict)
             else:
              all_results[f"data{i}"] = article_dict
             json_data2 =json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
           except:
             pass
          except:
            
             pass
        elif "archivesofmedicalscience" in current_url:
          driver1.get(link)
          try:
           wait = WebDriverWait(driver1, 15)
           article_dict['titre'] = titre
           article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
           article_dict['authors'] = authors
           article_dict['PMID'] = pmid
           try:
             p_tags = driver1.find_elements_by_class_name("section")
             content = []
             for tag in p_tags:
               if tag.text.strip() != "":
                content.append(tag.text)
             article_dict['content'] = content
             article_dict['abstract'] = abstract
             article_dict['News_paper'] = "archivesofmedicalscience"
             article_dict['Query'] = self.term
             if f"data{i}" in all_results:
              all_results[f"data{i}"].update(article_dict)
             else:
              all_results[f"data{i}"] = article_dict
             json_data2 =json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
           except:
             pass
          except:
            
             pass
        elif "aimspress.com" in current_url:
          driver1.get(link)
          sleep(6)
          try:
           article_dict['titre'] = titre
           article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
           article_dict['authors'] = authors
           article_dict['PMID'] = pmid
           try:
             p_tags = driver1.find_element_by_xpath("//*[@id='myTabContent']")
             article_dict['content'] = p_tags.text
             article_dict['abstract'] = abstract
             article_dict['News_paper'] = "aimspress.com"
             article_dict['Query'] = self.term
             if f"data{i}" in all_results:
              all_results[f"data{i}"].update(article_dict)
             else:
              all_results[f"data{i}"] = article_dict
             json_data2 =json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
           except:
             pass
           driver.get(page_url)
          except:
            
             pass
        else:
          print('else')
          link_else=driver1.current_url
          driver1.get(link_else)
          from urllib.parse import urlparse
          def extract_website_name(url):
            parsed_url = urlparse(url)
            website_name = parsed_url.netloc
            return website_name
          website_name = extract_website_name(link_else)
          website_name = website_name .split('.')[1]
          try:
           article_dict['titre'] = titre
           try:
            article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
           except:
             article_dict['DATE_PUBLICATION'] = ""
           article_dict['authors'] = authors
           article_dict['PMID'] = pmid
           try:
            driver1.get(link)
            p_tags = driver1.find_elements_by_tag_name("p")
            content = []
            for tag in p_tags:
               if tag.text.strip() != "":
                content.append(tag.text)
            article_dict['content'] = content
           except:
            driver1.get(link)
            p_tags = driver1.find_elements_by_tag_name("section")
            content = []
            for tag in p_tags:
               if tag.text.strip() != "":
                content.append(tag.text)
            article_dict['content'] = content
           article_dict['abstract'] = abstract
           article_dict['News_paper'] = website_name
           article_dict['Query'] = self.term
           if f"data{i}" in all_results:
              all_results[f"data{i}"].update(article_dict)
           else:
              all_results[f"data{i}"] = article_dict
              json_data2 =json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
          except:
            pass

      except: 
        current_url1=driver1.current_url
        driver1.get(current_url1)
        wait = WebDriverWait(driver1, 15)
        article_dict['titre'] = titre
        try:
         article_dict['DATE_PUBLICATION'] = remove_repeated_words(date_year_extracted)
        except:
          article_dict['DATE_PUBLICATION'] = ""
        article_dict['authors'] = authors
        article_dict['PMID'] = pmid
        article_dict['content'] = abstract
        article_dict['News_paper'] ="PubMed_abstract"
        article_dict['Query'] = self.term
        if f"data{i}" in all_results:
            all_results[f"data{i}"].update(article_dict)
        else:
            all_results[f"data{i}"] = article_dict
        json_data2 =json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')

     if f"data{i}" in all_results:
        all_results[f"data{i}"].update(article_dict)
     else:
        all_results[f"data{i}"] = article_dict
     json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
    return json_data2
   data_list = []
   last_successful_iteration = 0

   for i in range(1,2):
        try:
            data = scrap(i)
            with open(f'C:\\Users\\hp\\Downloads\\output.json\\projet\\ovarian{i}.json', 'wb') as f:
                f.write(data)
            data_list.append(data)
            last_successful_iteration = i
        except Exception as e:
            print(f"Une erreur est survenue lors de l'itération {i}: {e}. Retrying from iteration {last_successful_iteration+1}...")
            i = last_successful_iteration+1 # Reprise de l'itération depuis la dernière itération réussie
            print(i)
            continue
        sleep(5)
        import unicodedata
        with open(f"C:\\Users\\hp\\Downloads\\output.json\\projet\\ovarian{i}.json","r", encoding='utf-8') as f:
                 data = json.load(f)
        for key, record in data.items():
              if record['content']:
                 del record['abstract']
              else:
                 record['content']=record['abstract']
                 del record['abstract']

        for key, record in data.items():
                date = record['DATE_PUBLICATION']
                if len(date) == 7 and date[4] == '-':
                   year = date[:4]
                   month = date[5:]
                   month_mapping = {
                      '01': 'Jan',
                      '02': 'Feb',
                      '03': 'Mar',
                      '04': 'Apr',
                      '05': 'May',
                      '06': 'Jun',
                      '07': 'Jul',
                      '08': 'Aug',
                      '09': 'Sep',
                      '10': 'Oct',
                      '11': 'Nov',
                      '12': 'Dec'}
                   record['DATE_PUBLICATION'] = f"{year}-{month_mapping[month]}"
        for key, record in data.items():
            authors = record["authors"]
            for author in authors:
                 name = unicodedata.name(author)
            authors_list = authors.split(",")
            record["authors"] = authors_list
        with open(f"C:\\Users\\hp\\Downloads\\output.json\\projet\\ovarian{i}.json", 'w') as file:
            json.dump(data, file, indent=4)
        sleep(5)
        with open(f'C:\\Users\\hp\\Downloads\\output.json\\projet\\ovarian{i}.json','r', encoding='utf-8') as file:
            data = json.load(file)
        updated_data = []
        for key, value in data.items():
          updated_data.append(value)
        with open(f'C:\\Users\\hp\\Downloads\\output.json\\projet\\ovarian{i}.json', 'w') as file:
            json.dump(updated_data, file, indent=4)

           
  

