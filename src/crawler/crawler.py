import src.config.log_config as log_config
from src.config.tqdm_config import loading
import logging
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from typing import List, Dict
import asyncio
from concurrent.futures import ThreadPoolExecutor


BASE_URL = "https://sandbox.oxylabs.io/products"


def setup_driver() -> webdriver.Chrome:
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--blink-settings=imagesEnabled=false")
    
    return webdriver.Chrome(options=options)


def fetch_page_data(
        driver: webdriver.Chrome, 
        page: int) -> List[Dict]:
    
    url = f"{BASE_URL}?page={page}"
    
    logging.info(f"fetching page {page}: {url}")
    loading()

    driver.get(url)
    time.sleep(1.0)

    all_products = []
    
    cards = driver.find_elements(
        By.CLASS_NAME, "product-card")
    
    if not cards:
        return []

    for card in cards:
        try:
            title = card.find_element(
                By.CLASS_NAME, "title").text.strip()
            
            category = card.find_element(
                By.CLASS_NAME, "category").text.strip()
            
            price = card.find_element(
                By.CLASS_NAME, "price-wrapper").text.strip()\
                        .replace(",", ".").replace(" €", "")
            
            availability = "Unknown"
            
            try:
                availability = card.find_element(
                    By.CLASS_NAME, "in-stock").text.strip()
            except:
                try:
                    availability = card.find_element(
                        By.CLASS_NAME, "out-of-stock").text.strip()
                except:
                    pass

            description = None
            try:
                description = card.find_element(
                    By.CLASS_NAME, "description").text.strip()
            except:
                pass

            all_products.append({
                "title": title,
                "category": category,
                "price": price,
                "availability": availability,
                "description": description
            })
            
        except Exception as e:
            logging.warning(f"skipped broken card: {e}")
    
    return all_products

def fetch_page_data_and_quit(
        driver: webdriver.Chrome,
        page: int) -> List[Dict]:
    
    try:
        return fetch_page_data(driver, page)
    finally:
        driver.quit()  # !!!


async def crawl_all_products(pages_to_crawl: int) -> List[Dict]:
    loop = asyncio.get_event_loop()
    all_products = []

    with ThreadPoolExecutor(max_workers=6) as executor:
        futures = []

        for page in range(1, pages_to_crawl + 1):
            driver = setup_driver()
            future = loop.run_in_executor(executor,
                                        fetch_page_data_and_quit, 
                                        driver, page)
            futures.append(future)

        results = await asyncio.gather(*futures)

        for page_data in results:
            if page_data:
                all_products.extend(page_data)

    return all_products

