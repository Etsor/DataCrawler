from src.crawler.crawler import crawl_all_products
from src.writer.exporter import save_to_xml
from src.writer.validator import validate_xml
import asyncio

pages_to_crawl = int(input("Введите кол-во страниц (макс: 94)\n"))

OUTPUT_FILE = "products.xml"
SCHEMA_PATH = "src/res/schema.xsd"

async def main():
    if pages_to_crawl >= 95:
        print("Макс. кол-во страниц: 94")
    else:
        products = await crawl_all_products(pages_to_crawl)
        save_to_xml(products, SCHEMA_PATH, OUTPUT_FILE)
        validate_xml(OUTPUT_FILE, SCHEMA_PATH)

if __name__ == "__main__":
    asyncio.run(main())
