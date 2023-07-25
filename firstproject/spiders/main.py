from fastapi import FastAPI
from pydantic import BaseModel
import subprocess
from cancer import pubMed_spider
import scrapy
from scrapy.crawler import CrawlerProcess
from fastapi import FastAPI, HTTPException, Form


app = FastAPI()

        # Exécuter la commande scrapy runspider en tant que sous-processus
        # spider_path = "C:/Users/hp/Downloads/output.json/firstproject/firstproject/spiders/cancer.py"
        # subprocess.run(["scrapy", "runspider", spider_path])
@app.post("/scrape/")
async def scrape_website(term: str = Form(...)):
    try:
        if not term:
            raise HTTPException(status_code=400, detail="Research term cannot be empty!")

        # Create a scrapy crawler and pass the pubMed_spider class
        process = CrawlerProcess(settings={
            "USER_AGENT": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
            "FEEDS": {
                "output.json": {"format": "json"},
            },
        })
        
        # Update the term in the pubMed_spider class
        pubMed_spider.term = term
        process.crawl(pubMed_spider)
        process.start()

        return {"message": "Scraping successful!"}
    except Exception as e:
        return {"message": "Scraping failed!"}

