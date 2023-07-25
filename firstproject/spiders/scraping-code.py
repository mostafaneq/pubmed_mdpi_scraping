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

basedir = os.path.dirname(os.path.realpath('__file__'))
#mRNA
class pubMed_spider(scrapy.Spider):
 name = "cancer"
 allowed_domains = ["pubmed.ncbi.nlm.nih.gov"]
 i = "2020"
 j = "2023"
 term = "endometriose"
 start_urls = [f"https://pubmed.ncbi.nlm.nih.gov/?term={term}&filter=years.{i}-{j}"]

 def parse(self, response):
   driver = webdriver.Chrome(executable_path="/Users/hp/Desktop/driver/chromedriver.exe")
   driver1 = uc.Chrome(executable_path="/Users/hp/Desktop/driver/chromedriver.exe") 
   driver.get(self.start_urls[0])
   all_results={}
 # Get the total number of pages
   nbr = driver.find_element_by_xpath("//*[@id='bottom-page-number-input']")
   nbr_page = int(nbr.get_attribute("max"))
   article_dict = {}
   def scrap(nbr):
    global hogrefe
    global CURRENT
    for page_num in range(nbr, nbr+1):
     page_url = self.start_urls[0] + f"&page={page_num}"
     driver.get(page_url)
     articles = driver.find_elements(By.TAG_NAME, 'article')
     nbr_art=len(articles)
     for i in range(1,2):   
      driver.get(page_url)
      initial_XPATH=f"/html/body/main/div[9]/div[2]/section[1]/div[1]/div/article["+ str(i) +"]/div[2]/div[1]/a"                                                            
      WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, initial_XPATH))).click()
      sleep(2)
      wait = WebDriverWait(driver, 15)
      element0 = wait.until(EC.presence_of_element_located((By.TAG_NAME,"h1")))
      title_1= element0.text

      element1 = wait.until(EC.presence_of_element_located((By.CLASS_NAME,"authors-list")))
      authors_1= element1.text

      CURRENT=driver.current_url
      article_dict = {}
      link=""
      title=""
      try :
        sleep(5)
        try:
          img_element = driver.find_element_by_xpath("/html/body/div[5]/aside/div/div[1]/div[1]/div/a")
        except:
          img_element = driver.find_element_by_xpath("/html/body/div[5]/aside/div/div[1]/div[1]/div/a") 
        link = img_element.get_attribute('href')
        title = img_element.get_attribute('title')
        if "GN1 Sistemas e Publicacoe" in title:
           img_element2 = driver.find_element_by_xpath("/html/body/div[5]/aside/div/div[1]/div[1]/div/a[2]")
           link = img_element2.get_attribute('href')
           driver.get(link)  
        elif "hogrefe" in link :
           hogrefe =driver.find_element(By.CLASS_NAME,"authors-list") 
           author=hogrefe.text    
        try:
           driver.get(link)
        except:
           driver.get(link)     
        current_url=driver.current_url
        sleep(6)
        if "jogc" in current_url:
          driver1.get(link)
          try:     
            wait = WebDriverWait(driver1, 10)
            try:
             WebDriverWait(driver1, 10).until(EC.visibility_of_element_located((By.ID, "onetrust-accept-btn-handler"))).click() 
            except:
               pass                                        
            element0 = wait.until(EC.presence_of_element_located((By.TAG_NAME,"h1")))
            titre= element0.text
            article_dict['titre'] = titre
            element1 = wait.until(EC.presence_of_element_located((By.CLASS_NAME,"inline-it")))
            date = element1.text.split("DOI")[0].strip()
            article_dict['DATE_PUBLICATION'] = date
            content_divs = driver1.find_elements(By.CLASS_NAME, "section-paragraph")
            Content_texts=[]
            for div in content_divs:
               Content_texts.append(div.text)
            Content_text=list(set(Content_texts))
            article_dict['content'] = Content_text
            author_names=[]
            authors = driver1.find_elements_by_xpath('//a[contains(@class, "loa__item__name")]')
            for author in authors:
               author_names.append(author.text)
            article_dict['authors'] = author_names
            if f"data{i}" in all_results:
               all_results[f"data{i}"].update(article_dict)
            else:
               all_results[f"data{i}"] = article_dict
            json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
            driver.get(page_url)
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
            element0 = wait.until(EC.presence_of_element_located((By.TAG_NAME,"h1")))
            titre= element0.text
            article_dict['titre'] = titre
            element1 = wait.until(EC.presence_of_element_located((By.CLASS_NAME,"inline-it")))
            date = element1.text.split("DOI")[0].strip()
            article_dict['DATE_PUBLICATION'] = date
            content_divs = driver1.find_elements(By.CLASS_NAME, "section-paragraph")
            Content_texts=[]
            for div in content_divs:
               Content_texts.append(div.text)
            Content_text=list(set(Content_texts))
            article_dict['content'] = Content_text
            author_names=[]
            authors = driver1.find_elements_by_xpath('//a[contains(@class, "loa__item__name")]')
            for author in authors:
               author_names.append(author.text)
            article_dict['authors'] = author_names
            if f"data{i}" in all_results:
                all_results[f"data{i}"].update(article_dict)
            else:
                all_results[f"data{i}"] = article_dict
            json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
            driver.get(page_url)
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
            element0 = wait.until(EC.presence_of_element_located((By.TAG_NAME,"h1")))
            titre= element0.text
            article_dict['titre'] = titre
            element1 = wait.until(EC.presence_of_element_located((By.CLASS_NAME,"inline-it")))
            date = element1.text.split("DOI")[0].strip()
            article_dict['DATE_PUBLICATION'] = date
            content_divs = driver1.find_elements(By.CLASS_NAME, "section-paragraph")
            Content_texts=[]
            for div in content_divs:
               Content_texts.append(div.text)
            Content_text=list(set(Content_texts))
            article_dict['content'] = Content_text
            author_names=[]
            authors = driver1.find_elements_by_xpath('//a[contains(@class, "loa__item__name")]')
            for author in authors:
               author_names.append(author.text)
            article_dict['authors'] = author_names
            if f"data{i}" in all_results:
                all_results[f"data{i}"].update(article_dict)
            else:
                all_results[f"data{i}"] = article_dict
            json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
            driver.get(page_url)
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
           element0 = wait.until(EC.presence_of_element_located((By.TAG_NAME,"h1")))
           titre= element0.text
           article_dict['titre'] = titre
           element1 = wait.until(EC.presence_of_element_located((By.CLASS_NAME,"inline-it")))
           date = element1.text.split("DOI")[0].strip()
           article_dict['DATE_PUBLICATION'] = date
           content_divs = driver1.find_elements(By.CLASS_NAME, "section-paragraph")
           Content_texts=[]
           for div in content_divs:
               Content_texts.append(div.text)
           article_dict['content'] = Content_texts
           author_names=[]
           authors = driver1.find_elements_by_xpath('//a[contains(@class, "loa__item__name article-header__info__ctrl loa__item__email")]')
           for author in authors:
               author_names.append(author.text)
           article_dict['authors'] = author_names
           if f"data{i}" in all_results:
                all_results[f"data{i}"].update(article_dict)
           else:
                all_results[f"data{i}"] = article_dict
           json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
           driver.get(page_url)
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
           element0 = wait.until(EC.presence_of_element_located((By.TAG_NAME,"h1")))
           titre= element0.text
           article_dict['titre'] = titre
           element1 = wait.until(EC.presence_of_element_located((By.CLASS_NAME,"inline-it")))
           date = element1.text.split("DOI")[0].strip()
           article_dict['DATE_PUBLICATION'] = date
           content_divs = driver1.find_elements(By.CLASS_NAME, "section-paragraph")
           Content_texts=[]
           for div in content_divs:
               Content_texts.append(div.text)
           article_dict['content'] = Content_texts
           author_names=[]
           authors = driver1.find_elements_by_xpath('//a[contains(@class, "loa__item__name article-header__info__ctrl loa__item__email")]')
           for author in authors:
               author_names.append(author.text)
           article_dict['authors'] = author_names
           if f"data{i}" in all_results:
                all_results[f"data{i}"].update(article_dict)
           else:
                all_results[f"data{i}"] = article_dict
           json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
           driver.get(page_url)
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
           element0 = wait.until(EC.presence_of_element_located((By.TAG_NAME,"h1")))
           titre= element0.text
           article_dict['titre'] = titre
           element1 = wait.until(EC.presence_of_element_located((By.CLASS_NAME,"inline-it")))
           date = element1.text.split("DOI")[0].strip()
           article_dict['DATE_PUBLICATION'] = date
           content_divs = driver1.find_elements(By.TAG_NAME, "section")
           Content_texts=[]
           for div in content_divs:
               Content_texts.append(div.text)
           article_dict['content'] = Content_texts
           author_names=[]
           authors = driver1.find_elements_by_xpath('/html/body/div[3]/div/div[2]/div/div/div/main/article/div[1]/div/div[3]/div[2]/ul')
           author_names.append(author.text)
           article_dict['authors'] = author_names
           if f"data{i}" in all_results:
                all_results[f"data{i}"].update(article_dict)
           else:
                all_results[f"data{i}"] = article_dict
           json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
           driver.get(page_url)
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
           element0 = wait.until(EC.presence_of_element_located((By.TAG_NAME,"h1")))
           titre= element0.text
           article_dict['titre'] = titre
           element1 = wait.until(EC.presence_of_element_located((By.CLASS_NAME,"inline-it")))
           date = element1.text.split("DOI")[0].strip()
           article_dict['DATE_PUBLICATION'] = date
           content_divs = driver1.find_elements(By.TAG_NAME, "section")
           Content_texts=[]
           for div in content_divs:
               Content_texts.append(div.text)
           article_dict['content'] = Content_texts
           author_names=[]
           authors = driver1.find_elements_by_xpath('/html/body/div[3]/div/div[2]/div/div/div/main/article/div[1]/div/div[3]/div[2]/ul')
           author_names.append(author.text)
           article_dict['authors'] = author_names
           if f"data{i}" in all_results:
                all_results[f"data{i}"].update(article_dict)
           else:
                all_results[f"data{i}"] = article_dict
           json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
           driver.get(page_url)
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
           element0 = wait.until(EC.presence_of_element_located((By.TAG_NAME,"h1")))
           titre= element0.text
           article_dict['titre'] = titre
           element2 = wait.until(EC.presence_of_element_located((By.XPATH,"article-header__publish-date__value")))
           date= element2.text
           article_dict['DATE_PUBLICATION'] = date
           content_divs = driver1.find_elements(By.TAG_NAME, "section-paragraph")
           Content_texts=[]
           for div in content_divs:
               Content_texts.append(div.text)
           article_dict['content'] = Content_texts
           author_names=[]
           authors = driver1.find_elements_by_xpath('/html/body/div[3]/div/div[1]/div/div/div/main/article/div[1]/div/div[3]/div[2]/ul')
           author_names.append(author.text)
           article_dict['authors'] = author_names
           if f"data{i}" in all_results:
                all_results[f"data{i}"].update(article_dict)
           else:
                all_results[f"data{i}"] = article_dict
           json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
           driver.get(page_url)
          except:
            
             pass
        elif "sciencedirect.com" in current_url:
          sleep(8) 
          try:   
            wait = WebDriverWait(driver, 5)
            element0 = wait.until(EC.presence_of_element_located((By.CLASS_NAME,"title-text")))
            titre= element0.text
            article_dict['titre'] = titre
            try:
             element1 = wait.until(EC.presence_of_element_located((By.CLASS_NAME,"text-xs")))
             date = element1.text.split(', ')[1:3]  # Extract the second and third substrings
             date = ", ".join(date)
             article_dict['DATE_PUBLICATION'] = date
             elements = driver.find_element_by_class_name("author-group")
             authors = elements.text 
             article_dict['authors'] = authors
            except:
              pass
            Content_texts=[]
            p_tags = driver.find_elements_by_tag_name("p")
            for tag in p_tags:
               if tag.text.strip() != "":
                  Content_texts.append(tag.text)
            article_dict['content'] = Content_texts
            if f"data{i}" in all_results:
                  all_results[f"data{i}"].update(article_dict)
            else:
                 all_results[f"data{i}"] = article_dict
            json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
          except:
            
             pass

        elif "mdpi" in current_url:
          sleep(5)
          try:
           wait = WebDriverWait(driver, 5)
           element0 = wait.until(EC.presence_of_element_located((By.TAG_NAME,"h1")))
           titre= element0.text
           article_dict['titre'] = titre
          
           elements = driver.find_element_by_xpath("//*[@id='abstract']/div[2]/article/div/div[2]")
           authors = elements.text 
           article_dict['authors'] = authors
           p_tags = driver.find_elements_by_class_name("html-p")
           content=[]
           for tag in p_tags:
             if tag.text.strip() != "":
               content.append(tag.text)
           article_dict['content'] = content
           element2 = wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='abstract']/div[2]/article/div/div[7]/span[4]")))
           date= element2.text
           article_dict['DATE_PUBLICATION'] = date
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
            element0 = wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/div[2]/div[3]/main/article/div[1]/header/h1")))
            titre= element0.text
            article_dict['titre'] = titre
            element2 = wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='main-content']/main/article/div[1]/header/ul[1]/li/a/time")))
            date= element2.text
            article_dict['DATE_PUBLICATION'] = date
            element1 = wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='main-content']/main/article/div[1]/header/ul[2]")))
            authors= element1.text
            article_dict['authors'] = authors
            p_tags = driver1.find_elements_by_tag_name("p")
            content=[]
            for tag in p_tags:
             if tag.text.strip() != "":
               content.append(tag.text)
            article_dict['content'] = content
            if f"data{i}" in all_results:
               all_results[f"data{i}"].update(article_dict)
            else:
               all_results[f"data{i}"] = article_dict
            json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
            driver.get(page_url)
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
           classe_title="citation__title"
           ID_authors="accordion-tabbed"
           wait = WebDriverWait(driver1, 5)
           element0 = wait.until(EC.presence_of_element_located((By.CLASS_NAME,classe_title)))
           titre= element0.text
           article_dict['titre'] = titre
           element2 = wait.until(EC.presence_of_element_located((By.CLASS_NAME,"epub-date")))
           date= element2.text
           article_dict['DATE_PUBLICATION'] = date
           element1 = wait.until(EC.presence_of_element_located((By.CLASS_NAME,ID_authors)))
           authors= element1.text
           article_dict['authors'] = authors
           p_tags = driver1.find_elements_by_tag_name('p')
           content=[]
           for tag in p_tags:
             if tag.text.strip() != "":
               content.append(tag.text)
           article_dict['content'] = content
           if f"data{i}" in all_results:
               all_results[f"data{i}"].update(article_dict)
           else:
               all_results[f"data{i}"] = article_dict
           json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
           driver.get(page_url)
          except:
            
             pass


        elif "thieme" in link:
          try:
            sleep(10)
            try:
             WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.ID, "onetrust-accept-btn-handler"))).click()
            except:
               pass
            try:
             WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[3]/div[1]/div[2]/article/ul/li[2]/a"))).click()
            except:
             current=driver.current_url
             if "/login.html" in current:
               driver.get(link)
               p_tags = driver.find_elements_by_tag_name('p')
               content=[]
               for tag in p_tags:
                 if tag.text.strip() != "":
                  content.append(tag.text)
               article_dict['content'] = content
             else:
                pass
            wait = WebDriverWait(driver, 15)
            element0 = wait.until(EC.presence_of_element_located((By.TAG_NAME,"h1")))
            titre= element0.text
            article_dict['titre'] = titre
            try:
             element2 = wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/div[3]/div[1]/div[2]/article/div[5]/section[1]/p[2]")))
             date= element2.text  
             if "Article published online" in date:
              article_dict['DATE_PUBLICATION'] = date
             if "Article published online" not in date:
               element2 = wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/div[3]/div[1]/div[2]/article/div[5]/section[1]/p[10]")))
               date= element2.text  
               article_dict['DATE_PUBLICATION'] = date
             else:
               element2 = wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/div[3]/div[1]/div[2]/article/div[5]/section[1]/p[11]")))
               date= element2.text  
               article_dict['DATE_PUBLICATION'] = date
            except:
               element2 = wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/div[3]/div[1]/div[2]/article/div[6]/section[2]/p[30]")))
               date= element2.text  
               article_dict['DATE_PUBLICATION'] = date
            element1 = wait.until(EC.presence_of_element_located((By.ID,"authorlist")))
            authors= element1.text
            article_dict['authors'] = authors
            p_tags = driver.find_elements_by_tag_name('p')
            content=[]
            for tag in p_tags:
             if tag.text.strip() != "":
               content.append(tag.text)
            article_dict['content'] = content
            if f"data{i}" in all_results:
               all_results[f"data{i}"].update(article_dict)
            else:
              all_results[f"data{i}"] = article_dict
            json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
          except:
            
             pass

        elif "hogrefe" in link:
          try: 
           try:
              WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.ID, "onetrust-reject-all-handler"))).click()
           except:
              pass
           article_dict['authors'] = hogrefe.text
           print(article_dict['authors'])
           wait = WebDriverWait(driver, 15)
           element0 = wait.until(EC.presence_of_element_located((By.TAG_NAME,"h1")))
           titre= element0.text
           article_dict['titre'] = titre
           print(article_dict['titre'])
           element2 = wait.until(EC.presence_of_element_located((By.CLASS_NAME,"epub-section__date")))
           date= element2.text
           article_dict['DATE_PUBLICATION'] = date
           p_tags = driver.find_elements_by_tag_name("p")
           article_dict['content'] = [tag.get_attribute("outerHTML") for tag in p_tags if tag.text.strip() != ""]
           print(article_dict['content'])
           if f"data{i}" in all_results:
               all_results[f"data{i}"].update(article_dict)
           else:
              all_results[f"data{i}"] = article_dict
           json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
          except:
            
             pass
          
        elif "tidsskriftet" in link:
          try:
           wait = WebDriverWait(driver, 15)
           element0 = wait.until(EC.presence_of_element_located((By.TAG_NAME,"h1")))
           titre= element0.text
           article_dict['titre'] = titre
           element2 = wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/div[1]/div/main/div/div/div/div[2]/article/div/div/div[2]/div[3]/div/div[2]/div[1]")))
           date= element2.text
           article_dict['DATE_PUBLICATION'] = date
           p_tags = driver.find_elements_by_tag_name("p")
           content=[]
           for tag in p_tags:
             if tag.text.strip() != "":
               content.append(tag.text)
           article_dict['content'] = content
           author = driver.find_element_by_xpath("/html/body/div[1]/div/main/div/div/div/div[2]/article/div/div/div[2]/div[2]/div[1]/div[1]/div/div")         
           article_dict['authors'] = author.text
           if f"data{i}" in all_results:
               all_results[f"data{i}"].update(article_dict)
           else:
              all_results[f"data{i}"] = article_dict
           json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
          except:
            
             pass
        elif "edpsciences" in link:
          try:
           wait = WebDriverWait(driver, 15)
           element0 = wait.until(EC.presence_of_element_located((By.CLASS_NAME,"title")))
           titre= element0.text
           article_dict['titre'] = titre
           element2 = wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/div[3]/div[1]/main/div/div[2]/div/div[2]/div/div[2]/table/tbody/tr[7]/td[2]")))
           date= element2.text
           article_dict['DATE_PUBLICATION'] = date
           element1 = wait.until(EC.presence_of_element_located((By.CLASS_NAME,"article-authors")))
           authors= element1.text
           article_dict['authors'] = authors
           p_tags = driver.find_elements_by_tag_name("p")
           content=[]
           for tag in p_tags:
             if tag.text.strip() != "":
               content.append(tag.text)
           article_dict['content'] = content
           if f"data{i}" in all_results:
               all_results[f"data{i}"].update(article_dict)
           else:
              all_results[f"data{i}"] = article_dict
           json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
          except:
            
             pass
        elif "panafrican-med-journal.com" in current_url:
          try:
           wait = WebDriverWait(driver, 15)
           element0 = wait.until(EC.presence_of_element_located((By.TAG_NAME,"h1")))
           titre= element0.text
           article_dict['titre'] = titre
           element2 = wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/main/section[1]/div/div/div/div[1]/div/p[2]/i")))
           date= element2.text
           article_dict['DATE_PUBLICATION'] = date
           element1 = wait.until(EC.presence_of_element_located((By.CLASS_NAME,"AuthorListParagraph")))
           authors= element1.text
           article_dict['authors'] = authors
           p_tags = driver.find_elements_by_tag_name("p")
           content=[]
           for tag in p_tags:
             if tag.text.strip() != "":
               content.append(tag.text)
           article_dict['content'] = content
           if f"data{i}" in all_results:
               all_results[f"data{i}"].update(article_dict)
           else:
              all_results[f"data{i}"] = article_dict
           json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
          except:
           
             pass
         
        elif "rev-mal-respir.com" in current_url:
          try:
           wait = WebDriverWait(driver, 15)
           element0 = wait.until(EC.presence_of_element_located((By.TAG_NAME,"h1")))
           titre= element0.text
           article_dict['titre'] = titre
           element2 = wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/div[7]/div/article/div[1]/header/h1/span")))
           date= element2.text
           article_dict['DATE_PUBLICATION'] = date
           element1 = wait.until(EC.presence_of_element_located((By.CLASS_NAME,"textenormalSmallLeft")))
           authors= element1.text
           article_dict['authors'] = authors
           p_tags = driver.find_elements_by_tag_name("p")
           content=[]
           for tag in p_tags:
             if tag.text.strip() != "":
               content.append(tag.text)
           article_dict['content'] = content
           if f"data{i}" in all_results:
               all_results[f"data{i}"].update(article_dict)
           else:
              all_results[f"data{i}"] = article_dict
           json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
          except:
            
             pass
         
        elif "degruyter.com" in current_url:
          try:
           wait = WebDriverWait(driver, 15)
           element0 = wait.until(EC.presence_of_element_located((By.TAG_NAME,"h1")))
           titre= element0.text
           article_dict['titre'] = titre
           element2 = wait.until(EC.presence_of_element_located((By.CLASS_NAME,"publicationDate")))
           date= element2.text
           article_dict['DATE_PUBLICATION'] = date
           element1 = wait.until(EC.presence_of_element_located((By.CLASS_NAME,"metadataAndContributorsFont")))
           authors= element1.text
           article_dict['authors'] = authors
           p_tags = driver.find_elements_by_tag_name("p")
           content=[]
           for tag in p_tags:
             if tag.text.strip() != "":
               content.append(tag.text)
           article_dict['content'] = content
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
           element0 = wait.until(EC.presence_of_element_located((By.TAG_NAME,"h1")))
           titre= element0.text
           article_dict['titre'] = titre
           element2 = wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='content']/main/article/div[2]/header/ul[1]/li[3]/a/time")))
           date= element2.text
           article_dict['DATE_PUBLICATION'] = date
           element1 = wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='content']/main/article/div[2]/header/ul[2]")))
           authors= element1.text
           article_dict['authors'] = authors
           p_tags = driver1.find_elements_by_tag_name("p")
           content=[]
           for tag in p_tags:
             if tag.text.strip() != "":
               content.append(tag.text)
           article_dict['content'] = content
           if f"data{i}" in all_results:
               all_results[f"data{i}"].update(article_dict)
           else:
              all_results[f"data{i}"] = article_dict
           json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
           driver.get(page_url)
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
           element0 = wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/div[3]/div/div[3]/main/article/header/div/h1")))
           titre= element0.text
           article_dict['titre'] = titre
           element2 = wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/div[3]/div/div[3]/main/article/header/div/div[1]/div[1]/div[4]")))
           date= element2.text
           article_dict['DATE_PUBLICATION'] = date
           element1 = wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/div[3]/div/div[3]/main/article/header/div/div[2]/span/span")))
           authors= element1.text
           article_dict['authors'] = authors
           content = wait.until(EC.presence_of_elements_located((By.TAG_NAME,"section")))
           Content=[]
           for tag in content:
             if tag.text.strip() != "":
               Content.append(tag.text)
           article_dict['content'] = Content
           if f"data{i}" in all_results:
               all_results[f"data{i}"].update(article_dict)
           else:
              all_results[f"data{i}"] = article_dict
           json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')  
           driver.get(page_url)
          except:
            
             pass

        elif "tandfonline.com" in current_url:
          try:
           driver1.get(current_url)
           wait = WebDriverWait(driver1, 15)
           element0 = wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/div[2]/div/div[3]/div/div/div/div/div/div[2]/div/div/div/div/div[2]/div/div[1]/div/div/h1/span")))
           titre= element0.text
           article_dict['titre'] = titre
           element2 = wait.until(EC.presence_of_element_located((By.CLASS_NAME,"itemPageRangeHistory")))
           date= element2.text
           article_dict['DATE_PUBLICATION'] = date
           element1 = wait.until(EC.presence_of_element_located((By.CLASS_NAME,"literatumAuthors")))
           authors= element1.text
           article_dict['authors'] = authors
           p_tags = driver1.find_elements_by_tag_name("p")
           content=[]
           for tag in p_tags:
             if tag.text.strip() != "":
               content.append(tag.text)
           article_dict['content'] = content
           if f"data{i}" in all_results:
               all_results[f"data{i}"].update(article_dict)
           else:
              all_results[f"data{i}"] = article_dict
           json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
           driver.get(page_url)
          except:
            
             pass

        elif "amegroups.com" in current_url:
          try:
           wait = WebDriverWait(driver, 5)
           element0 = wait.until(EC.presence_of_element_located((By.TAG_NAME,"h1")))
           titre= element0.text
           article_dict['titre'] = titre                                    
           element2 = wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/div[1]/div/div/div[2]/div[1]/article/header/div[2]/p[4]")))
           date= element2.text
           article_dict['DATE_PUBLICATION'] = date
           element1 = wait.until(EC.presence_of_element_located((By.CLASS_NAME,"authors")))
           authors= element1.text
           article_dict['authors'] = authors
           p_tags = driver.find_elements_by_tag_name("p")
           content=[]
           for tag in p_tags:
             if tag.text.strip() != "":
               content.append(tag.text)
           article_dict['content'] = content
           if f"data{i}" in all_results:
               all_results[f"data{i}"].update(article_dict)
           else:
              all_results[f"data{i}"] = article_dict
           json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
          except:
           
             pass

        elif "frontiersin.org" in current_url:
          try:
           wait = WebDriverWait(driver, 5)
           element0 = wait.until(EC.presence_of_element_located((By.TAG_NAME,"h1")))
           titre= element0.text
           article_dict['titre'] = titre
           element2 = wait.until(EC.presence_of_element_located((By.CLASS_NAME,"header-bar-three")))
           date= element2.text
           article_dict['DATE_PUBLICATION'] = date
           element1 = wait.until(EC.presence_of_element_located((By.CLASS_NAME,"authors")))
           authors= element1.text
           article_dict['authors'] = authors
           p_tags = driver.find_elements_by_tag_name("p")
           content=[]
           for tag in p_tags:
             if tag.text.strip() != "":
               content.append(tag.text)
           article_dict['content'] = content
           if f"data{i}" in all_results:
               all_results[f"data{i}"].update(article_dict)
           else:
              all_results[f"data{i}"] = article_dict
           json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
          except:
            
             pass

        elif "bmj.com" in current_url:
          try:
           wait = WebDriverWait(driver, 5)
           element0 = wait.until(EC.presence_of_element_located((By.CLASS_NAME,"highwire-cite-title")))
           titre= element0.text
           article_dict['titre'] = titre
           authors = driver.find_elements_by_xpath('//ol[contains(@id, "contrib-group-1")]')
           Authors=[]
           for author in authors:
              Authors.append(author.text)
           article_dict['authors'] = Authors
           p_tags = driver.find_elements_by_tag_name("p")
           content=[]
           for tag in p_tags:
             if tag.text.strip() != "":
               content.append(tag.text)
           article_dict['content'] = content
           if f"data{i}" in all_results:
               all_results[f"data{i}"].update(article_dict)
           else:
              all_results[f"data{i}"] = article_dict
           json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
          except:
            
             pass

        elif "biomedcentral.com" in current_url:
          sleep(6)
          try: 
           wait = WebDriverWait(driver, 5)
           element0 = wait.until(EC.presence_of_element_located((By.CLASS_NAME,"c-article-title")))
           titre= element0.text
           article_dict['titre'] = titre
           element2 = wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='main-content']/main/article/div[1]/ul[1]/li[3]/a/time")))
           date= element2.text
           article_dict['DATE_PUBLICATION'] = date
           authors = driver.find_element_by_xpath('//*[@id="main-content"]/main/article/div[1]/ul[2]')
           article_dict['authors'] = authors.text
           p_tags = driver.find_elements_by_tag_name("p")
           content=[]
           for tag in p_tags:
             if tag.text.strip() != "":
               content.append(tag.text)
           article_dict['content'] = content
           if f"data{i}" in all_results:
               all_results[f"data{i}"].update(article_dict)
           else:
              all_results[f"data{i}"] = article_dict
           json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
          except:
            
             pass
         
        elif "karger.com" in current_url:
          try:
           wait = WebDriverWait(driver, 5)
           WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.ID, "cmpbntyestxt"))).click()
           element0 = wait.until(EC.presence_of_element_located((By.TAG_NAME,"h1")))
           titre= element0.text
           article_dict['titre'] = titre
           element2 = wait.until(EC.presence_of_element_located((By.CLASS_NAME,"article-date")))
           date= element2.text
           article_dict['DATE_PUBLICATION'] = date
           element1 = wait.until(EC.presence_of_element_located((By.CLASS_NAME,"wi-authors")))
           authors= element1.text
           article_dict['authors'] = authors
           p_tags = driver.find_elements_by_tag_name("p")
           content=[]
           for tag in p_tags:
             if tag.text.strip() != "":
               content.append(tag.text)
           article_dict['content'] = content
           if f"data{i}" in all_results:
               all_results[f"data{i}"].update(article_dict)
           else:
              all_results[f"data{i}"] = article_dict
           json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
          except:
            
             pass

        elif "uliege.be" in current_url:
          try:
           wait = WebDriverWait(driver, 5)
           element0 = wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/section/div/div/div/div/ul/li/a/div/div[2]")))
           titre= element0.text
           article_dict['titre'] = titre
           element1 = wait.until(EC.presence_of_element_located((By.CLASS_NAME,"text-center")))
           authors= element1.text
           article_dict['authors'] = authors
           p_tags = driver.find_elements_by_tag_name("p")
           content=[]
           for tag in p_tags:
             if tag.text.strip() != "":
               content.append(tag.text)
           article_dict['content'] = content
           if f"data{i}" in all_results:
               all_results[f"data{i}"].update(article_dict)
           else:
              all_results[f"data{i}"] = article_dict
           json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
          except:
            
             pass
        
        elif "nih.gov" in current_url:
          try:
           wait = WebDriverWait(driver, 5)
           element0 = wait.until(EC.presence_of_element_located((By.TAG_NAME,"h1")))
           titre= element0.text
           article_dict['titre'] = titre
           element2 = wait.until(EC.presence_of_element_located((By.CLASS_NAME,"fm-vol-iss-date")))
           date= element2.text
           article_dict['DATE_PUBLICATION'] = date
           element1 = wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/main/article/section[3]/div/div[1]/div[1]/div[2]/div[1]")))
           authors= element1.text
           article_dict['authors'] = authors
           p_tags = driver.find_elements_by_tag_name("p")
           content=[]
           for tag in p_tags:
             if tag.text.strip() != "":
               content.append(tag.text)
           article_dict['content'] = content
           if f"data{i}" in all_results:
               all_results[f"data{i}"].update(article_dict)
           else:
              all_results[f"data{i}"] = article_dict
           json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
          except:
            
             pass
        elif "lww" in current_url:
          try:     
            wait = WebDriverWait(driver, 10)
            try:
             WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "onetrust-reject-all-handler"))).click() 
            except:
               pass                                        
            element0 = wait.until(EC.presence_of_element_located((By.TAG_NAME,"h1")))
            titre= element0.text
            article_dict['titre'] = titre
            element1 = wait.until(EC.presence_of_element_located((By.ID,"ej-journal-date-volume-issue-pg")))
            date = element1.text
            article_dict['DATE_PUBLICATION'] = date
            content_divs = driver.find_elements(By.TAG_NAME, "p")
            Content_texts=[]
            for div in content_divs:
               Content_texts.append(div.text)
            Content_text=list(set(Content_texts))
            article_dict['content'] = Content_text
            author_names=[]
            authors = driver.find_element_by_id("P7")
            article_dict['authors'] = authors.text
            if f"data{i}" in all_results:
                all_results[f"data{i}"].update(article_dict)
            else:
                all_results[f"data{i}"] = article_dict
            json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
          except:
            
             pass
        elif "europeanreview" in current_url:
          try:     
            wait = WebDriverWait(driver, 10)                                        
            element0 = wait.until(EC.presence_of_element_located((By.TAG_NAME,"h1")))
            titre= element0.text
            article_dict['titre'] = titre
            content_divs = driver.find_elements(By.TAG_NAME, "p")
            Content_texts=[]
            for div in content_divs:
               Content_texts.append(div.text)
            Content_text=list(set(Content_texts))
            article_dict['content'] = Content_text
            author_names=[]
            authors = driver.find_element_by_id("article-heading-info")
            article_dict['authors'] = authors.text
            if f"data{i}" in all_results:
                all_results[f"data{i}"].update(article_dict)
            else:
                all_results[f"data{i}"] = article_dict
            json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
          except:
            
             pass
        elif "bioscientifica" in current_url:
          try:     
            wait = WebDriverWait(driver, 10)                                        
            element0 = wait.until(EC.presence_of_element_located((By.TAG_NAME,"h1")))
            titre= element0.text
            article_dict['titre'] = titre
            element1 = wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/div[2]/div[2]/div[2]/div/div[1]/div/div[1]/div/div[1]/div/div/div/div[2]/div/div/div/div/div[1]/div/div[1]/div/div/div[5]/div/div/div/div[2]/dl[2]")))
            date = element1.text
            article_dict['DATE_PUBLICATION'] = date
            content_divs = driver.find_elements(By.TAG_NAME, "p")
            Content_texts=[]
            for div in content_divs:
               Content_texts.append(div.text)
            Content_text=list(set(Content_texts))
            article_dict['content'] = Content_text
            author_names=[]
            authors = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div/div[1]/div/div[1]/div/div[1]/div/div/div/div[2]/div/div/div/div/div[1]/div/div[1]/div/div/div[2]/div/div/div/div")
            article_dict['authors'] = authors.text
            if f"data{i}" in all_results:
                all_results[f"data{i}"].update(article_dict)
            else:
                all_results[f"data{i}"] = article_dict
            json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
          except:
            
             pass
        elif "futuremedicine" in current_url:
          try:     
            wait = WebDriverWait(driver, 10)                                        
            element0 = wait.until(EC.presence_of_element_located((By.TAG_NAME,"h1")))
            titre= element0.text
            article_dict['titre'] = titre
            element1 = wait.until(EC.presence_of_element_located((By.CLASS_NAME,"epub-section__item")))
            date = element1.text
            article_dict['DATE_PUBLICATION'] = date
            content_divs = driver.find_elements(By.TAG_NAME, "p")
            Content_texts=[]
            for div in content_divs:
               Content_texts.append(div.text)
            Content_text=list(set(Content_texts))
            article_dict['content'] = Content_text
            author_names=[]
            authors = driver.find_element_by_class_name("accordion")
            article_dict['authors'] = authors.text
            if f"data{i}" in all_results:
                all_results[f"data{i}"].update(article_dict)
            else:
                all_results[f"data{i}"] = article_dict
            json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
          except:
            
             pass
        elif "liebertpub" in current_url:
          try:     
            wait = WebDriverWait(driver, 10)                                        
            element0 = wait.until(EC.presence_of_element_located((By.TAG_NAME,"h1")))
            titre= element0.text
            article_dict['titre'] = titre
            element1 = wait.until(EC.presence_of_element_located((By.CLASS_NAME,"epub-section__item")))
            date = element1.text
            article_dict['DATE_PUBLICATION'] = date
            content_divs = driver.find_elements(By.TAG_NAME, "p")
            Content_texts=[]
            for div in content_divs:
               Content_texts.append(div.text)
            Content_text=list(set(Content_texts))
            article_dict['content'] = Content_text
            author_names=[]
            authors = driver.find_element_by_id("sb-1")
            article_dict['authors'] = authors.text
            if f"data{i}" in all_results:
                all_results[f"data{i}"].update(article_dict)
            else:
                all_results[f"data{i}"] = article_dict
            json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
          except:
            
             pass
        elif "spandidos-publications" in current_url:
          try:     
            wait = WebDriverWait(driver, 10)                                        
            element0 = wait.until(EC.presence_of_element_located((By.TAG_NAME,"h1")))
            titre= element0.text
            article_dict['titre'] = titre
            element1 = wait.until(EC.presence_of_element_located((By.ID,"publishedOn")))
            date = element1.text
            article_dict['DATE_PUBLICATION'] = date
            content_divs = driver.find_elements(By.TAG_NAME, "p")
            content=driver.find_element(By.ID, "articleAbstract")
            Content_texts=[]
            Content_texts.append(content.text)
            for div in content_divs:
               Content_texts.append(div.text)
            Content_text=list(set(Content_texts))
            article_dict['content'] = Content_text
            author_names=[]
            authors = driver.find_element_by_id("authorshipNames")
            article_dict['authors'] = authors.text
            if f"data{i}" in all_results:
                all_results[f"data{i}"].update(article_dict)
            else:
                all_results[f"data{i}"] = article_dict
            json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
          except:
            
             pass
        elif "jamanetwork" in current_url:
          try:     
            wait = WebDriverWait(driver, 10)                                        
            element0 = wait.until(EC.presence_of_element_located((By.CLASS_NAME,"meta-article-title ")))
            titre= element0.text
            article_dict['titre'] = titre
            element1 = wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/form/section[2]/div[3]/div/div[2]/div/div[5]/div[3]")))
            date = element1.text
            article_dict['DATE_PUBLICATION'] = date
            content_divs = driver.find_elements(By.TAG_NAME, "p")
            Content_texts=[]
            for div in content_divs:
               Content_texts.append(div.text)
            Content_text=list(set(Content_texts))
            article_dict['content'] = Content_text
            author_names=[]
            authors = driver.find_element_by_class_name("meta-authors")
            article_dict['authors'] = authors.text
            if f"data{i}" in all_results:
                all_results[f"data{i}"].update(article_dict)
            else:
                all_results[f"data{i}"] = article_dict
            json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
          except:
            
             pass
        elif "scielo" in current_url:
          try:     
            wait = WebDriverWait(driver, 10)                                        
            element0 = wait.until(EC.presence_of_element_located((By.TAG_NAME,"h1")))
            titre= element0.text
            article_dict['titre'] = titre
            element1 = wait.until(EC.presence_of_element_located((By.CLASS_NAME,"articleTimeline")))
            date = element1.text
            article_dict['DATE_PUBLICATION'] = date
            content_divs = driver.find_elements(By.TAG_NAME, "p")
            Content_texts=[]
            for div in content_divs:
               Content_texts.append(div.text)
            Content_text=list(set(Content_texts))
            article_dict['content'] = Content_text
            author_names=[]
            authors = driver.find_element_by_class_name("contribGroup")
            article_dict['authors'] = authors.text
            if f"data{i}" in all_results:
                all_results[f"data{i}"].update(article_dict)
            else:
                all_results[f"data{i}"] = article_dict
            json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
          except:
            
             pass
        elif "medsci" in current_url:
          try:     
            wait = WebDriverWait(driver, 10)                                        
            element0 = wait.until(EC.presence_of_element_located((By.TAG_NAME,"h1")))
            titre= element0.text
            article_dict['titre'] = titre
            element1 = wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/div/div/div[3]/div[2]/p[71]/span")))
            date = element1.text
            article_dict['DATE_PUBLICATION'] = date
            content_divs = driver.find_elements(By.TAG_NAME, "p")
            Content_texts=[]
            for div in content_divs:
               Content_texts.append(div.text)
            Content_text=list(set(Content_texts))
            article_dict['content'] = Content_text
            author_names=[]
            authors = driver.find_element_by_class_name("author")
            article_dict['authors'] = authors.text
            if f"data{i}" in all_results:
                all_results[f"data{i}"].update(article_dict)
            else:
                all_results[f"data{i}"] = article_dict
            json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
          except:
            
             pass
        elif "dovepress" in current_url:
          try:     
            wait = WebDriverWait(driver, 10)                                        
            element0 = wait.until(EC.presence_of_element_located((By.TAG_NAME,"h1")))
            titre= element0.text
            article_dict['titre'] = titre
            element1 = wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/div[2]/div[4]/div/div/div[2]/div/div/div[4]/div/div[1]/div/p[4]")))
            date = element1.text
            article_dict['DATE_PUBLICATION'] = date
            content_divs = driver.find_elements(By.TAG_NAME, "p")
            Content_texts=[]
            for div in content_divs:
               Content_texts.append(div.text)
            Content_text=list(set(Content_texts))
            article_dict['content'] = Content_text
            author_names=[]
            authors = driver.find_element_by_xpath("/html/body/div[2]/div[4]/div/div/div[2]/div/div/div[4]/div/div[1]/div/p[1]")
            article_dict['authors'] = authors.text
            if f"data{i}" in all_results:
                all_results[f"data{i}"].update(article_dict)
            else:
                all_results[f"data{i}"] = article_dict
            json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
          except:
            
             pass
        elif "ecerm" in current_url:
          try: 
            wait = WebDriverWait(driver, 10)                                        
            element0 = wait.until(EC.presence_of_element_located((By.TAG_NAME,"h3")))
            titre= element0.text
            article_dict['titre'] = titre
            sleep(2)
            element1 = wait.until(EC.presence_of_element_located((By.CLASS_NAME,"metadata-group")))
            date = element1.text
            article_dict['DATE_PUBLICATION'] = date
            content_divs = driver.find_element(By.CLASS_NAME, "section")
            text1=driver.find_element(By.CLASS_NAME, "body")
            Content_texts=[]
            Content_texts.append(content_divs.text)
            Content_texts.append(text1.text)
            Content_text=list(set(Content_texts))
            article_dict['content'] = Content_text
            author_names=[]
            authors = driver.find_elements_by_xpath("/html/body/div[3]/div[2]/div[1]/div/div[1]/div[3]/div/div[7]")
            article_dict['authors'] = authors.text
            if f"data{i}" in all_results:
                all_results[f"data{i}"].update(article_dict)
            else:
                all_results[f"data{i}"] = article_dict
            json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
          except:
            
             pass
        elif "eurekaselect" in current_url:
          try:     
            wait = WebDriverWait(driver, 10)                                        
            element0 = wait.until(EC.presence_of_element_located((By.TAG_NAME,"h1")))
            titre= element0.text
            article_dict['titre'] = titre
            element1 = wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/section/div/div/div[2]/div/div/p[2]")))
            date = element1.text
            article_dict['DATE_PUBLICATION'] = date
            content_divs = driver.find_elements(By.CLASS_NAME, "card-body")
            Content_texts=[]
            for div in content_divs:
               Content_texts.append(div.text)
            Content_text=list(set(Content_texts))
            article_dict['content'] = Content_text
            author_names=[]
            authors = driver.find_element_by_class_name("l-h-3")
            article_dict['authors'] = authors.text
            if f"data{i}" in all_results:
                all_results[f"data{i}"].update(article_dict)
            else:
                all_results[f"data{i}"] = article_dict
            json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
          except:
            
             pass
        elif "jcancer" in current_url:
          try:     
            wait = WebDriverWait(driver, 10)                                        
            element0 = wait.until(EC.presence_of_element_located((By.TAG_NAME,"h1")))
            titre= element0.text
            article_dict['titre'] = titre
            element1 = wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/div/div/div[3]/div[2]/p[189]/span")))
            date = element1.text
            article_dict['DATE_PUBLICATION'] = date
            content_divs = driver.find_elements(By.TAG_NAME, "p")
            Content_texts=[]
            for div in content_divs:
               Content_texts.append(div.text)
            Content_text=list(set(Content_texts))
            article_dict['content'] = Content_text
            author_names=[]
            authors = driver.find_element_by_class_name("author")
            article_dict['authors'] = authors.text
            if f"data{i}" in all_results:
                all_results[f"data{i}"].update(article_dict)
            else:
                all_results[f"data{i}"] = article_dict
            json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
          except:
            
             pass
        elif "hindawi" in current_url:
          try:     
            wait = WebDriverWait(driver, 10)                                        
            element0 = wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/div[2]/section/main/div[2]/div[2]/div/div[1]/h1")))
            titre= element0.text
            article_dict['titre'] = titre
            element1 = wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/div[2]/section/main/div[2]/div[2]/div/div[1]/div[6]/div[3]/span")))
            date = element1.text
            article_dict['DATE_PUBLICATION'] = date
            content_divs = driver.find_element(By.CLASS_NAME, "xml-content")
            article_dict['content'] = content_divs.text
            author_names=[]
            authors = driver.find_element_by_class_name("articleHeader__authors")
            article_dict['authors'] = authors.text
            if f"data{i}" in all_results:
                all_results[f"data{i}"].update(article_dict)
            else:
                all_results[f"data{i}"] = article_dict
            json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
          except:
            
             pass
        elif "viamedica" in current_url:
          try:     
            wait = WebDriverWait(driver, 10)                                        
            element0 = wait.until(EC.presence_of_element_located((By.CLASS_NAME,"articleTitle")))
            titre= element0.text
            article_dict['titre'] = titre
            element1 = wait.until(EC.presence_of_element_located((By.CLASS_NAME,"publishedDate")))
            date = element1.text
            article_dict['DATE_PUBLICATION'] = date
            content_divs = driver.find_elements(By.TAG_NAME, "p")
            Content_texts=[]
            for div in content_divs:
               Content_texts.append(div.text)
            Content_text=list(set(Content_texts))
            article_dict['content'] = Content_text
            author_names=[]
            authors = driver.find_element_by_class_name("Autors")
            article_dict['authors'] = authors.text
            if f"data{i}" in all_results:
                all_results[f"data{i}"].update(article_dict)
            else:
                all_results[f"data{i}"] = article_dict
            json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
          except:
            
             pass
        elif "ojs.ptbioch.edu.pl" in current_url:
          try:     
            wait = WebDriverWait(driver, 10)                                        
            element0 = wait.until(EC.presence_of_element_located((By.TAG_NAME,"h1")))
            titre= element0.text
            article_dict['titre'] = titre
            element1 = wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/div[2]/div[1]/div[1]/div/article/div/div[2]/div[3]")))
            date = element1.text
            article_dict['DATE_PUBLICATION'] = date
            content_divs = driver.find_elements(By.TAG_NAME, "p")
            Content_texts=[]
            for div in content_divs:
               Content_texts.append(div.text)
            Content_text=list(set(Content_texts))
            article_dict['content'] = Content_text
            author_names=[]
            authors = driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[1]/div/article/div/div[1]/ul")
            article_dict['authors'] = authors.text
            if f"data{i}" in all_results:
                all_results[f"data{i}"].update(article_dict)
            else:
                all_results[f"data{i}"] = article_dict
            json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
          except:
            
             pass
        elif "journals.plos.org" in current_url:
          try:     
            wait = WebDriverWait(driver, 10)
            try:
             WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "_19RPUZBjdy2iuONl+jvOiQ=="))).click() 
            except:
               pass                                        
            element0 = wait.until(EC.presence_of_element_located((By.TAG_NAME,"h1")))
            titre= element0.text
            article_dict['titre'] = titre
            element1 = wait.until(EC.presence_of_element_located((By.ID,"artPubDate")))
            date = element1.text
            article_dict['DATE_PUBLICATION'] = date
            content_divs = driver.find_elements(By.TAG_NAME, "p")
            Content_texts=[]
            for div in content_divs:
               Content_texts.append(div.text)
            Content_text=list(set(Content_texts))
            article_dict['content'] = Content_text
            author_names=[]
            authors = driver.find_element_by_id("author-list")
            article_dict['authors'] = authors.text
            if f"data{i}" in all_results:
                all_results[f"data{i}"].update(article_dict)
            else:
                all_results[f"data{i}"] = article_dict
            json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
          except:
            
             pass
        elif "aging-us" in current_url:
          try:     
            wait = WebDriverWait(driver, 10)                                       
            element0 = wait.until(EC.presence_of_element_located((By.TAG_NAME,"h1")))
            titre= element0.text
            article_dict['titre'] = titre
            element1 = wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/div[1]/div[2]/div/div[2]/div[1]/h4[2]/span[3]")))
            date = element1.text
            article_dict['DATE_PUBLICATION'] = date
            content_divs = driver.find_elements(By.TAG_NAME, "p")
            Content_texts=[]
            for div in content_divs:
               Content_texts.append(div.text)
            Content_text=list(set(Content_texts))
            article_dict['content'] = Content_text
            author_names=[]
            authors = driver.find_element_by_class_name("authors")
            article_dict['authors'] = authors.text
            if f"data{i}" in all_results:
                all_results[f"data{i}"].update(article_dict)
            else:
                all_results[f"data{i}"] = article_dict
            json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
          except:
            
             pass
        elif "academic.oup" in current_url:
          try:     
            wait = WebDriverWait(driver, 10)                                       
            element0 = wait.until(EC.presence_of_element_located((By.TAG_NAME,"h1")))
            titre= element0.text
            article_dict['titre'] = titre
            element1 = wait.until(EC.presence_of_element_located((By.CLASS_NAME,"citation-date")))
            date = element1.text
            article_dict['DATE_PUBLICATION'] = date
            content_divs = driver.find_elements(By.TAG_NAME, "p")
            Content_texts=[]
            for div in content_divs:
               Content_texts.append(div.text)
            Content_text=list(set(Content_texts))
            article_dict['content'] = Content_text
            author_names=[]
            authors = driver.find_element_by_class_name("al-authors-list")
            article_dict['authors'] = authors.text
            if f"data{i}" in all_results:
                all_results[f"data{i}"].update(article_dict)
            else:
                all_results[f"data{i}"] = article_dict
            json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
          except:
            
             pass
        elif "futuremedicine" in current_url:
          try:     
            wait = WebDriverWait(driver, 10)                                       
            element0 = wait.until(EC.presence_of_element_located((By.TAG_NAME,"h1")))
            titre= element0.text
            article_dict['titre'] = titre
            element1 = wait.until(EC.presence_of_element_located((By.CLASS_NAME,"epub-section__item")))
            date = element1.text
            article_dict['DATE_PUBLICATION'] = date
            content_divs = driver.find_elements(By.TAG_NAME, "p")
            Content_texts=[]
            for div in content_divs:
               Content_texts.append(div.text)
            Content_text=list(set(Content_texts))
            article_dict['content'] = Content_text
            author_names=[]
            authors = driver.find_elements_by_id("sb-1")
            article_dict['authors'] = authors.text
            if f"data{i}" in all_results:
                all_results[f"data{i}"].update(article_dict)
            else:
                all_results[f"data{i}"] = article_dict
            json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
          except:
            
             pass
        elif "ias.ac.in" in link:
          try: 
           driver.get(CURRENT)
           wait = WebDriverWait(driver, 15)
           element0 = wait.until(EC.presence_of_element_located((By.TAG_NAME,"h1")))
           title= element0.text
           article_dict['titre'] = title

           element2 = wait.until(EC.presence_of_element_located((By.CLASS_NAME,"cit")))
           date= element2.text
           article_dict['DATE_PUBLICATION'] = date

           element1 = wait.until(EC.presence_of_element_located((By.XPATH,'//div[contains(@class, "authors-list")]')))
           authors= element1.text
           article_dict['authors'] = authors
           try:
             p_tags = driver.find_elements_by_tag_name("p")
             content = []
             for tag in p_tags:
               if tag.text.strip() != "":
                content.append(tag.text)
             article_dict['content'] = content
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
          try:
           sleep(7)
           wait = WebDriverWait(driver, 15)
        
           element0 = wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='vmMainPage']/table/tbody/tr[2]/td")))
           title= element0.text
           article_dict['titre'] = title

           element2 = wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='vmMainPage']/table/tbody/tr[8]/td[2]/b")))
           date= element2.text
           article_dict['DATE_PUBLICATION'] = date

           element1 = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="vmMainPage"]/table/tbody/tr[3]/td')))
           authors= element1.text
           article_dict['authors'] = authors
           try:
             p_tags = driver.find_element_by_xpath("//*[@id='vmMainPage']/table/tbody/tr[5]/td")
             article_dict['content'] = p_tags.text
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
          try:
           wait = WebDriverWait(driver, 15)
           element0 = wait.until(EC.presence_of_element_located((By.TAG_NAME,"h1")))
           title= element0.text
           article_dict['titre'] = title

           element2 = wait.until(EC.presence_of_element_located((By.CLASS_NAME,"history-list")))
           date= element2.text
           article_dict['DATE_PUBLICATION'] = date

           element1 = wait.until(EC.presence_of_element_located((By.CLASS_NAME,'highwire-citation-authors')))
           authors= element1.text
           article_dict['authors'] = authors
           try:
             p_tags = driver.find_elements_by_tag_name("p")
             content = []
             for tag in p_tags:
               if tag.text.strip() != "":
                content.append(tag.text)
             article_dict['content'] = content
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
          try:
           wait = WebDriverWait(driver, 15)
           element0 = wait.until(EC.presence_of_element_located((By.TAG_NAME,"h1")))
           title= element0.text
           article_dict['titre'] = title

           element2 = wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/div/div/div[3]/div[2]/p[118]/span")))
           date= element2.text
           article_dict['DATE_PUBLICATION'] = date

           element1 = wait.until(EC.presence_of_element_located((By.CLASS_NAME,'author')))
           authors= element1.text
           article_dict['authors'] = authors
           try:
             p_tags = driver.find_elements_by_tag_name("p")
             content = []
             for tag in p_tags:
               if tag.text.strip() != "":
                content.append(tag.text)
             article_dict['content'] = content
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
          try:
           wait = WebDriverWait(driver, 15)
           element0 = wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/div[4]/div[1]/div/header/h1")))
           title= element0.text
           article_dict['titre'] = title

           element2 = wait.until(EC.presence_of_element_located((By.CLASS_NAME,"history-date")))
           date= element2.text
           article_dict['DATE_PUBLICATION'] = date

           element1 = wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/div[4]/div[1]/div/header/div[1]/p[2]')))
           authors= element1.text
           article_dict['authors'] = authors
           try:
             p_tags = driver.find_elements_by_tag_name("p")
             content = []
             for tag in p_tags:
               if tag.text.strip() != "":
                content.append(tag.text)
             article_dict['content'] = content
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
          try:
           wait = WebDriverWait(driver, 15)
           element0 = wait.until(EC.presence_of_element_located((By.TAG_NAME,"h1")))
           title= element0.text
           article_dict['titre'] = title

           element2 = wait.until(EC.presence_of_element_located((By.CLASS_NAME,"epub-section")))
           date= element2.text
           article_dict['DATE_PUBLICATION'] = date

           element1 = wait.until(EC.presence_of_element_located((By.ID,'sb-1')))
           authors= element1.text
           article_dict['authors'] = authors
           try:
             p_tags = driver.find_elements_by_tag_name("p")
             content = []
             for tag in p_tags:
               if tag.text.strip() != "":
                content.append(tag.text)
             article_dict['content'] = content
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
          try:
           wait = WebDriverWait(driver, 15)
           element0 = wait.until(EC.presence_of_element_located((By.TAG_NAME,"h2")))
           title= element0.text
           article_dict['titre'] = title

           element2 = wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/main/div/div[2]/div/div[2]/section[1]/div/div[2]/div/div/div[2]/dl/div[5]")))
           date= element2.text
           article_dict['DATE_PUBLICATION'] = date

           element1 = wait.until(EC.presence_of_element_located((By.CLASS_NAME,'article__authors')))
           authors= element1.text
           article_dict['authors'] = authors
           try:
             p_tags = driver.find_elements_by_tag_name("p")
             content = []
             for tag in p_tags:
               if tag.text.strip() != "":
                content.append(tag.text)
             article_dict['content'] = content
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
          try:
           wait = WebDriverWait(driver, 15)
           element0 = wait.until(EC.presence_of_element_located((By.TAG_NAME,"h1")))
           title= element0.text
           article_dict['titre'] = title

           element2 = wait.until(EC.presence_of_element_located((By.CLASS_NAME,"ii-pub-date")))
           date= element2.text
           article_dict['DATE_PUBLICATION'] = date

           element1 = wait.until(EC.presence_of_element_located((By.CLASS_NAME,'al-authors-list')))
           authors= element1.text
           article_dict['authors'] = authors
           try:
             p_tags = driver.find_elements_by_tag_name("p")
             content = []
             for tag in p_tags:
               if tag.text.strip() != "":
                content.append(tag.text)
             article_dict['content'] = content
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
          try:
           wait = WebDriverWait(driver, 15)
           element0 = wait.until(EC.presence_of_element_located((By.TAG_NAME,"h1")))
           title= element0.text
           article_dict['titre'] = title

           element2 = wait.until(EC.presence_of_element_located((By.CLASS_NAME,"core-date-published")))
           date= element2.text
           article_dict['DATE_PUBLICATION'] = date

           element1 = wait.until(EC.presence_of_element_located((By.CLASS_NAME,'authors')))
           authors= element1.text
           article_dict['authors'] = authors
           try:
             p_tags = driver.find_elements_by_class_name("core-container")
             content = []
             for tag in p_tags:
               if tag.text.strip() != "":
                content.append(tag.text)
             article_dict['content'] = content
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
          try:
           wait = WebDriverWait(driver, 15)
           element0 = wait.until(EC.presence_of_element_located((By.TAG_NAME,"h1")))
           title= element0.text
           article_dict['titre'] = title

           element2 = wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/div[4]/main/div/div/div[2]/div[9]/p[4]")))
           date= element2.text
           article_dict['DATE_PUBLICATION'] = date

           element1 = wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/div[4]/main/div/div/div[2]/div[3]/div/div[2]')))
           authors= element1.text
           article_dict['authors'] = authors
           try:
             p_tags = driver.find_element_by_class_name("tab-content")
             article_dict['content'] =p_tags.text
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
          try:
           wait = WebDriverWait(driver, 15)
           element0 = wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/div[3]/div/div[1]/div[2]/div/div[1]/div[1]/div[2]")))
           title= element0.text
           article_dict['titre'] = title

           element2 = wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/div[3]/div/div[1]/div[2]/div/div[1]/div[1]/div[8]")))
           date= element2.text
           article_dict['DATE_PUBLICATION'] = date

           element1 = wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/div[3]/div/div[1]/div[2]/div/div[1]/div[1]/div[4]')))
           authors= element1.text
           article_dict['authors'] = authors
           try:
             p_tags = driver.find_elements_by_class_name("section")
             content = []
             seen_text = set() # keep track of unique texts
             for tag in p_tags:
              text = tag.text.strip()
              if text != "" and text not in seen_text: # check if text is not empty and not already seen
                content.append(text)
                seen_text.add(text)
             article_dict['content'] = text
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
          try:
           wait = WebDriverWait(driver, 15)
           element0 = wait.until(EC.presence_of_element_located((By.TAG_NAME,"h1")))
           title= element0.text
           article_dict['titre'] = title
           try:
            element2 = wait.until(EC.presence_of_element_located((By.TAG_NAME,"h6")))
            date= element2.text
            article_dict['DATE_PUBLICATION'] = date

            element1 = wait.until(EC.presence_of_element_located((By.CLASS_NAME,'/html/body/div[4]/div/section/div/div[1]/div/div/ul[1]')))
            authors= element1.text
            article_dict['authors'] = authors
           except:
             pass
           try:
             p_tags = driver.find_element_by_class_name("padding_abstract justify ltr")
             article_dict['content'] = p_tags.text
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
          try:
           wait = WebDriverWait(driver, 15)
           element0 = wait.until(EC.presence_of_element_located((By.TAG_NAME,"h1")))
           title= element0.text
           article_dict['titre'] = title

           element2 = wait.until(EC.presence_of_element_located((By.CLASS_NAME,"ii-pub-date")))
           date= element2.text
           article_dict['DATE_PUBLICATION'] = date

           element1 = wait.until(EC.presence_of_element_located((By.CLASS_NAME,'wi-authors')))
           authors= element1.text
           article_dict['authors'] = authors
           try:
             p_tags = driver.find_elements_by_tag_name("p")
             content = []
             for tag in p_tags:
               if tag.text.strip() != "":
                content.append(tag.text)
             article_dict['content'] = content
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
          try:
           wait = WebDriverWait(driver, 15)
           element0 = wait.until(EC.presence_of_element_located((By.TAG_NAME,"h1")))
           title= element0.text
           article_dict['titre'] = title

           element2 = wait.until(EC.presence_of_element_located((By.CLASS_NAME,"epub-section__date")))
           date= element2.text
           article_dict['DATE_PUBLICATION'] = date

           element1 = wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/div[1]/div/main/div[2]/div/div/article/div/div[1]/div/div[2]/div[1]/div[2]')))
           authors= element1.text
           article_dict['authors'] = authors
           try:
             p_tags = driver.find_elements_by_tag_name("p")
             content = []
             for tag in p_tags:
               if tag.text.strip() != "":
                content.append(tag.text)
             article_dict['content'] = content
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
          try:
           wait = WebDriverWait(driver, 15)
           element0 = wait.until(EC.presence_of_element_located((By.TAG_NAME,"h1")))
           title= element0.text
           article_dict['titre'] = title

           element2 = wait.until(EC.presence_of_element_located((By.CLASS_NAME,"cover-details__date")))
           date= element2.text
           article_dict['DATE_PUBLICATION'] = date

           element1 = wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/div[2]/div/main/div[1]/article/div/div[1]/div[1]/div[2]/div[4]')))
           authors= element1.text
           article_dict['authors'] = authors
           try:
             p_tags = driver.find_elements_by_tag_name("p")
             content = []
             for tag in p_tags:
               if tag.text.strip() != "":
                content.append(tag.text)
             article_dict['content'] = content
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
          try:
           wait = WebDriverWait(driver, 15)
           element0 = wait.until(EC.presence_of_element_located((By.TAG_NAME,"h1")))
           title= element0.text
           article_dict['titre'] = title

           element2 = wait.until(EC.presence_of_element_located((By.CLASS_NAME,"pub-date-value")))
           date= element2.text
           article_dict['DATE_PUBLICATION'] = date

           element1 = wait.until(EC.presence_of_element_located((By.CLASS_NAME,"loa")))
           authors= element1.text
           article_dict['authors'] = authors
           try:
             p_tags = driver.find_elements_by_tag_name("p")
             content = []
             for tag in p_tags:
               if tag.text.strip() != "":
                content.append(tag.text)
             article_dict['content'] = content
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
          try:
           wait = WebDriverWait(driver, 15)
           element0 = wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/div[2]/div/div/div[3]/div/div[2]/div/div[2]/div/div[1]")))
           title= element0.text
           article_dict['titre'] = title

           element2 = wait.until(EC.presence_of_element_located((By.CLASS_NAME,"ipubw-p3")))
           date= element2.text
           article_dict['DATE_PUBLICATION'] = date

           element1 = wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/div[2]/div/div/div[3]/div/div[2]/div/div[2]/div/div[2]")))
           authors= element1.text
           article_dict['authors'] = authors
           try:
             p_tags = driver.find_elements_by_tag_name("p")
             content = []
             for tag in p_tags:
               if tag.text.strip() != "":
                content.append(tag.text)
             article_dict['content'] = content
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
          try:
           wait = WebDriverWait(driver, 15)
           element0 = wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/div[6]/div/div/div[1]/div/div[2]/div/div[1]/table[2]/tbody/tr[2]/td/span/left")))
           title= element0.text
           article_dict['titre'] = title

           element2 = wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/div[6]/div/div/div[1]/div/div[2]/div/div[1]/table[1]/tbody/tr[2]/td")))
           date= element2.text
           article_dict['DATE_PUBLICATION'] = date

           element1 = wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/div[6]/div/div/div[1]/div/div[2]/div/div[1]/table[2]/tbody/tr[3]/td")))
           authors= element1.text
           article_dict['authors'] = authors
           try:
             p_tags = driver.find_elements_by_tag_name("p")
             content = []
             for tag in p_tags:
               if tag.text.strip() != "":
                content.append(tag.text)
             article_dict['content'] = content
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
          try:
           wait = WebDriverWait(driver, 15)
           element0 = wait.until(EC.presence_of_element_located((By.TAG_NAME,"h1")))
           title= element0.text
           article_dict['titre'] = title

           element2 = wait.until(EC.presence_of_element_located((By.ID,"publishedOn")))
           date= element2.text
           article_dict['DATE_PUBLICATION'] = date

           element1 = wait.until(EC.presence_of_element_located((By.ID,"authorshipNames")))
           authors= element1.text
           article_dict['authors'] = authors
           try:
             p_tags = driver.find_elements_by_tag_name("p")
             content = []
             for tag in p_tags:
               if tag.text.strip() != "":
                content.append(tag.text)
             article_dict['content'] = content
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
          try:
           wait = WebDriverWait(driver, 15)
           element0 = wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/div[6]/div/div/div[1]/div/div[2]/div/div[1]/table[2]/tbody/tr[2]/td/span/left")))
           title= element0.text
           article_dict['titre'] = title

           element2 = wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/div[6]/div/div/div[1]/div/div[2]/div/div[1]/table[2]/tbody/tr[8]/td")))
           date= element2.text
           article_dict['DATE_PUBLICATION'] = date

           element1 = wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/div[6]/div/div/div[1]/div/div[2]/div/div[1]/table[2]/tbody/tr[3]/td")))
           authors= element1.text
           article_dict['authors'] = authors
           try:
             p_tags = driver.find_elements_by_tag_name("p")
             content = []
             for tag in p_tags:
               if tag.text.strip() != "":
                content.append(tag.text)
             article_dict['content'] = content
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
          try:
           wait = WebDriverWait(driver, 15)
           element0 = wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/div[6]/div/div/div[1]/div/div[2]/div/div[1]/table[2]/tbody/tr[2]/td/span/left")))
           title= element0.text
           article_dict['titre'] = title

           element2 = wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/div[4]/div[1]/div[2]/div[4]/div[1]/section/div/span")))
           date= element2.text
           article_dict['DATE_PUBLICATION'] = date

           element1 = wait.until(EC.presence_of_element_located((By.CLASS_NAME,"authors")))
           authors= element1.text
           article_dict['authors'] = authors
           try:
             p_tags = driver.find_elements_by_tag_name("p")
             content = []
             for tag in p_tags:
               if tag.text.strip() != "":
                content.append(tag.text)
             article_dict['content'] = content
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
          try:
           wait = WebDriverWait(driver, 15)
           element0 = wait.until(EC.presence_of_element_located((By.TAG_NAME,"h1")))
           title= element0.text
           article_dict['titre'] = title

           element2 = wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/main/div/div/div/div[1]/div[1]/div[1]/p[1]")))
           date= element2.text
           article_dict['DATE_PUBLICATION'] = date

           element1 = wait.until(EC.presence_of_elements_located((By.TAG_NAME,"i")))
           authors= element1.text
           article_dict['authors'] = authors
           try:
             p_tags = driver.find_elements_by_tag_name("p")
             content = []
             for tag in p_tags:
               if tag.text.strip() != "":
                content.append(tag.text)
             article_dict['content'] = content
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
          try:
           wait = WebDriverWait(driver, 15)
           try:
            element0 = wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/table[2]/tbody/tr/td[2]/div/div/p[1]/font/b")))
            title= element0.text
            article_dict['titre'] = title

            element1 = wait.until(EC.presence_of_elements_located((By.XPATH,"/html/body/table[2]/tbody/tr/td[2]/div/div/p[2]/font")))
            authors= element1.text
            article_dict['authors'] = authors
           except:
             pass
           try:
             p_tags = driver.find_elements_by_tag_name("p")
             content = []
             for tag in p_tags:
               if tag.text.strip() != "":
                content.append(tag.text)
             article_dict['content'] = content
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
           wait = WebDriverWait(driver, 15)
           element0 = wait.until(EC.presence_of_element_located((By.TAG_NAME,"h1")))
           title= element0.text
           article_dict['titre'] = title

           element2 = wait.until(EC.presence_of_element_located((By.CLASS_NAME,"epub-date")))
           date= element2.text
           article_dict['DATE_PUBLICATION'] = date

           element1 = wait.until(EC.presence_of_elements_located((By.ID,"sb-1")))
           authors= element1.text
           article_dict['authors'] = authors
           try:
             p_tags = driver.find_elements_by_tag_name("p")
             content = []
             for tag in p_tags:
               if tag.text.strip() != "":
                content.append(tag.text)
             article_dict['content'] = content
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
           wait = WebDriverWait(driver, 15)
           element0 = wait.until(EC.presence_of_element_located((By.TAG_NAME,"h1")))
           title= element0.text
           article_dict['titre'] = title
           try:
            element2 = wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='xplMainContentLandmark']/div/xpl-document-details/div/div[1]/div/div[2]/section/div[2]/xpl-document-abstract/section/div[2]/div[3]/div[1]/div[2]/strong")))
            date= element2.text
            article_dict['DATE_PUBLICATION'] = date

            element1 = wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='indexTerms-container-1683729612923-0']")))
            authors= element1.text
            article_dict['authors'] = authors
           except:
             pass
           try:
             p_tags = driver.find_element_by_xpath("//*[@id='xplMainContentLandmark']/div/xpl-document-details/div/div[1]/div/div[2]/section/div[2]/div/xpl-document-abstract/section/div[2]/div[1]/div/div/div")
             article_dict['content'] = p_tags.text
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
          try:
           wait = WebDriverWait(driver, 15)
           element0 = wait.until(EC.presence_of_element_located((By.TAG_NAME,"h1")))
           title= element0.text
           article_dict['titre'] = title

           element2 = wait.until(EC.presence_of_element_located((By.CLASS_NAME,"received")))
           date= element2.text
           article_dict['DATE_PUBLICATION'] = date

           element1 = wait.until(EC.presence_of_elements_located((By.CLASS_NAME,"Authors")))
           authors= element1.text
           article_dict['authors'] = authors
           try:
             p_tags = driver.find_elements_by_tag_name("p")
             content = []
             for tag in p_tags:
               if tag.text.strip() != "":
                content.append(tag.text)
             article_dict['content'] = content
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
          try:
           wait = WebDriverWait(driver, 15)
           element0 = wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/table/tbody/tr/td[2]/div[1]/b/p")))
           title= element0.text
           article_dict['titre'] = title

           element2 = wait.until(EC.presence_of_element_located((By.CLASS_NAME,"received")))
           date= element2.text
           article_dict['DATE_PUBLICATION'] = date

           element1 = wait.until(EC.presence_of_elements_located((By.XPATH,"/html/body/table/tbody/tr/td[2]/div[1]/p")))
           authors= element1.text
           article_dict['authors'] = authors
           try:
             p_tags = driver.find_elements_by_tag_name("p")
             content = []
             for tag in p_tags:
               if tag.text.strip() != "":
                content.append(tag.text)
             article_dict['content'] = content
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
          try:
           wait = WebDriverWait(driver, 15)
           element0 = wait.until(EC.presence_of_element_located((By.TAG_NAME,"h1")))
           title= element0.text
           article_dict['titre'] = title

           element2 = wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/div[2]/div[1]/div[1]/div/article/div/div[2]/div[4]/section/div/span")))
           date= element2.text
           article_dict['DATE_PUBLICATION'] = date

           element1 = wait.until(EC.presence_of_elements_located((By.CLASS_NAME,"authors")))
           authors= element1.text
           article_dict['authors'] = authors
           try:
             p_tags = driver.find_elements_by_tag_name("p")
             content = []
             for tag in p_tags:
               if tag.text.strip() != "":
                content.append(tag.text)
             article_dict['content'] = content
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
          try:
           wait = WebDriverWait(driver, 15)
           element0 = wait.until(EC.presence_of_element_located((By.TAG_NAME,"h1")))
           title= element0.text
           article_dict['titre'] = title

           element2 = wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/div[3]/div/main/article/div/div[2]/div/div/div[4]/div/section[2]/div/div")))
           date= element2.text
           article_dict['DATE_PUBLICATION'] = date

           element1 = wait.until(EC.presence_of_elements_located((By.ID,"sb-1")))
           authors= element1.text
           article_dict['authors'] = authors
           try:
             p_tags = driver.find_elements_by_tag_name("p")
             content = []
             for tag in p_tags:
               if tag.text.strip() != "":
                content.append(tag.text)
             article_dict['content'] = content
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
          try:
           wait = WebDriverWait(driver, 15)
           element0 = wait.until(EC.presence_of_element_located((By.TAG_NAME,"h3")))
           title= element0.text
           article_dict['titre'] = title

           element2 = wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/div[5]/table/tbody/tr/td[1]/div/div[1]/div[3]/div/div[2]/div/p")))
           date= element2.text
           article_dict['DATE_PUBLICATION'] = date

           element1 = wait.until(EC.presence_of_elements_located((By.XPATH,"/html/body/div[5]/table/tbody/tr/td[1]/div/div[1]/div[3]/div/div[8]")))
           authors= element1.text
           article_dict['authors'] = authors
           try:
             p_tags = driver.find_elements_by_id("article-body")
             article_dict['content'] = p_tags.text
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
          try:
           wait = WebDriverWait(driver, 15)
           element0 = wait.until(EC.presence_of_element_located((By.TAG_NAME,"h1")))
           title= element0.text
           article_dict['titre'] = title

           element2 = wait.until(EC.presence_of_element_located((By.CLASS_NAME,"ii-pub-date")))
           date= element2.text
           article_dict['DATE_PUBLICATION'] = date

           element1 = wait.until(EC.presence_of_elements_located((By.CLASS_NAME,"al-authors-list")))
           authors= element1.text
           article_dict['authors'] = authors
           try:
             p_tags = driver.find_elements_by_tag_name("p")
             content = []
             for tag in p_tags:
               if tag.text.strip() != "":
                content.append(tag.text)
             article_dict['content'] = content
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
          try:
           wait = WebDriverWait(driver, 15)
           element0 = wait.until(EC.presence_of_element_located((By.CLASS_NAME,"global-article-title")))
           title= element0.text
           article_dict['titre'] = title

           element2 = wait.until(EC.presence_of_element_located((By.CLASS_NAME,"ii-pub-date")))
           date= element2.text
           article_dict['DATE_PUBLICATION'] = date

           element1 = wait.until(EC.presence_of_elements_located((By.CLASS_NAME,"global-authors-name-tags")))
           authors= element1.text
           article_dict['authors'] = authors
           try:
             p_tags = driver.find_elements_by_tag_name("p")
             content = []
             for tag in p_tags:
               if tag.text.strip() != "":
                content.append(tag.text)
             article_dict['content'] = content
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
          try:
           wait = WebDriverWait(driver, 15)
           element0 = wait.until(EC.presence_of_element_located((By.TAG_NAME,"h1")))
           title= element0.text
           article_dict['titre'] = title

           element2 = wait.until(EC.presence_of_element_located((By.CLASS_NAME,"toplinks")))
           date= element2.text
           article_dict['DATE_PUBLICATION'] = date

           element1 = wait.until(EC.presence_of_elements_located((By.CLASS_NAME,"writers_list")))
           authors= element1.text
           article_dict['authors'] = authors
           try:
             p_tags = driver.find_elements_by_tag_name("p")
             content = []
             for tag in p_tags:
               if tag.text.strip() != "":
                content.append(tag.text)
             article_dict['content'] = content
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
          try:
           wait = WebDriverWait(driver, 15)
           element0 = wait.until(EC.presence_of_element_located((By.TAG_NAME,"h1")))
           title= element0.text
           article_dict['titre'] = title

           element2 = wait.until(EC.presence_of_element_located((By.CLASS_NAME,"Date")))
           date= element2.text
           article_dict['DATE_PUBLICATION'] = date

           element1 = wait.until(EC.presence_of_elements_located((By.CLASS_NAME,"Authors")))
           authors= element1.text
           article_dict['authors'] = authors
           try:
             p_tags = driver.find_elements_by_tag_name("p")
             content = []
             for tag in p_tags:
               if tag.text.strip() != "":
                content.append(tag.text)
             article_dict['content'] = content
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
          try:
           wait = WebDriverWait(driver, 15)
           element0 = wait.until(EC.presence_of_element_located((By.TAG_NAME,"h1")))
           title= element0.text
           article_dict['titre'] = title

           element2 = wait.until(EC.presence_of_element_located((By.CLASS_NAME,"article-meta-value")))
           date= element2.text
           article_dict['DATE_PUBLICATION'] = date

           element1 = wait.until(EC.presence_of_elements_located((By.CLASS_NAME,"article-authors")))
           authors= element1.text
           article_dict['authors'] = authors
           try:
             p_tags = driver.find_elements_by_tag_name("p")
             content = []
             for tag in p_tags:
               if tag.text.strip() != "":
                content.append(tag.text)
             article_dict['content'] = content
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
          try:
           wait = WebDriverWait(driver, 15)
           element0 = wait.until(EC.presence_of_element_located((By.TAG_NAME,"h3")))
           title= element0.text
           article_dict['titre'] = title

           element2 = wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/div[3]/div[2]/div[1]/div/div[1]/div[3]/div/div[9]/div[2]/span[3]")))
           date= element2.text
           article_dict['DATE_PUBLICATION'] = date

           element1 = wait.until(EC.presence_of_elements_located((By.TAG_NAME,"/html/body/div[3]/div[2]/div[1]/div/div[1]/div[3]/div/div[7]")))
           authors= element1.text
           article_dict['authors'] = authors
           try:
             p_tags = driver.find_elements_by_class_name("section")
             content = []
             for tag in p_tags:
               if tag.text.strip() != "":
                content.append(tag.text)
             article_dict['content'] = content
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
          try:
           wait = WebDriverWait(driver, 15)
           element0 = wait.until(EC.presence_of_element_located((By.TAG_NAME,"h1")))
           title= element0.text
           article_dict['titre'] = title

           element2 = wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/div[2]/div[2]/div[2]/div/div[1]/div/div[1]/div/div[1]/div/div/div/div[2]/div/div/div/div/div[1]/div/div[1]/div/div/div[5]/div/div/div/div[2]/dl[2]")))
           date= element2.text
           article_dict['DATE_PUBLICATION'] = date

           element1 = wait.until(EC.presence_of_elements_located((By.CLASSE_NAME,"contributor-line text-subheading")))
           authors= element1.text
           article_dict['authors'] = authors
           try:
             p_tags = driver.find_elements_by_class_name("p")
             content = []
             for tag in p_tags:
               if tag.text.strip() != "":
                content.append(tag.text)
             article_dict['content'] = content
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
          try:
           wait = WebDriverWait(driver, 15)
           element0 = wait.until(EC.presence_of_element_located((By.TAG_NAME,"h1")))
           title= element0.text
           article_dict['titre'] = title

           element2 = wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div/div[2]/div[2]/button/div/div[1]/div/p")))
           date= element2.text
           article_dict['DATE_PUBLICATION'] = date

           element1 = wait.until(EC.presence_of_elements_located((By.XPATH,"/html/body/div[1]/div/div[2]/div/div/div/div/div[1]/div/div/div[3]/div/button/div/div[1]")))
           authors= element1.text
           article_dict['authors'] = authors
           try:
             p_tags = driver.find_elements_by_class_name("p")
             content = []
             for tag in p_tags:
               if tag.text.strip() != "":
                content.append(tag.text)
             article_dict['content'] = content
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
          try:
           wait = WebDriverWait(driver, 15)
           try:
             WebDriverWait(driver1, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div[1]/div/div/div[2]/a[1]"))).click() 
           except:
               pass 
           element0 = wait.until(EC.presence_of_element_located((By.CLASS_NAME,"articleTitle")))
           title= element0.text
           article_dict['titre'] = title

           element2 = wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/div[1]/div[5]/div/div/div[1]/div[6]/div[5]/div[6]")))
           date= element2.text
           article_dict['DATE_PUBLICATION'] = date

           element1 = wait.until(EC.presence_of_elements_located((By.CLASSE_NAME,"magAbstractAuthors")))
           authors= element1.text
           article_dict['authors'] = authors
           try:
             p_tags = driver.find_elements_by_class_name("section")
             content = []
             for tag in p_tags:
               if tag.text.strip() != "":
                content.append(tag.text)
             article_dict['content'] = content
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
           wait = WebDriverWait(driver1, 15)
           try:
             WebDriverWait(driver1, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='myTab']/li[2]/a"))).click() 
           except:
               pass 
           element0 = wait.until(EC.presence_of_element_located((By.TAG_NAME,"h1")))
           title= element0.text
           article_dict['titre'] = title

           element2 = wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/div[3]/div/div/div[1]/div[2]/div[2]/ul[3]/li[1]/span[3]")))
           date= element2.text
           article_dict['DATE_PUBLICATION'] = date

           element1 = wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/div[3]/div/div/div[1]/div[2]/div[2]/ul[1]")))
           authors= element1.text
           article_dict['authors'] = authors
           try:
             p_tags = driver1.find_element_by_xpath("//*[@id='myTabContent']")
             article_dict['content'] = p_tags.text
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
          try:
           resultat=diffbot(current_url)
           article_dict['authors'] = authors_1
           article_dict['content']=resultat['content']
           article_dict['titre'] = title_1
           article_dict['DATE_PUBLICATION'] = resultat['DATE_PUBLICATION']
           if f"data{i}" in all_results:
              all_results[f"data{i}"].update(article_dict)
           else:
              all_results[f"data{i}"] = article_dict
              json_data2 =json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
          except:
            pass

      except: 
        current_url1=driver.current_url
        driver.get(current_url1)
        wait = WebDriverWait(driver, 15)
        element0 = wait.until(EC.presence_of_element_located((By.TAG_NAME,"h1")))
        title= element0.text
        article_dict['titre'] = title

        element2 = wait.until(EC.presence_of_element_located((By.CLASS_NAME,"cit")))
        date= element2.text
        article_dict['DATE_PUBLICATION'] = date

        element1 = wait.until(EC.presence_of_element_located((By.XPATH,'//span[contains(@class, "authors-list-item ")]')))
        authors= element1.text
        article_dict['authors'] = authors
        try:
          p_tags = driver.find_elements_by_tag_name("p")
          content = []
          for tag in p_tags:
           if tag.text.strip() != "":
             content.append(tag.text)
           article_dict['content'] = content
          if f"data{i}" in all_results:
            all_results[f"data{i}"].update(article_dict)
          else:
            all_results[f"data{i}"] = article_dict
          json_data2 =json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
        except:
          pass

     if f"data{i}" in all_results:
        all_results[f"data{i}"].update(article_dict)
     else:
        all_results[f"data{i}"] = article_dict
     json_data2 = json.dumps(all_results, indent=4, ensure_ascii=False).encode('utf-8')
    return json_data2
   data_list = []
   last_successful_iteration = 0

   for i in range(2,3):
        try:
            data = scrap(i)
            with open(f'breast_cancer{i}.json', 'wb') as f:
                f.write(data)
            data_list.append(data)
            last_successful_iteration = i
        except Exception as e:
            print(f"Une erreur est survenue lors de l'itération {i}: {e}. Retrying from iteration {last_successful_iteration+1}...")
            i = last_successful_iteration+1 # Reprise de l'itération depuis la dernière itération réussie
            print(i)
            data = scrap(i+1)
            with open(f'breast_cancer{i+1}.json', 'wb') as f:
                f.write(data)
            data_list.append(data)
            continue


           
  

