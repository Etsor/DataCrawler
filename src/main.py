import sys

import asyncio

from src.crawler.crawler import crawl_all_products
from src.writer.exporter import save_to_xml
from src.writer.validator import validate_xml

async def main():
    try:
        pages_to_crawl = int(input("Enter number of pages (max: 94)\n"))

        OUTPUT_FILE = "products.xml"
        SCHEMA_PATH = "src/res/schema.xsd"

        products = await crawl_all_products(pages_to_crawl)
        save_to_xml(products, SCHEMA_PATH, OUTPUT_FILE)
        validate_xml(OUTPUT_FILE, SCHEMA_PATH)

    except ValueError as e:
        print(f"Input error: {e}", file=sys.stderr)
        sys.exit(1)
    
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
