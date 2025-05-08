import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from selenium.common.exceptions import WebDriverException

from src.crawler import crawler

@pytest.fixture
def mock_driver():
    with patch('selenium.webdriver.Chrome') as mock:
        yield mock

def test_setup_driver_failure(mock_driver):
    mock_driver.side_effect = WebDriverException("Chrome not found")
    with pytest.raises(crawler.CrawlerException):
        crawler.setup_driver()

@pytest.mark.asyncio
async def test_crawl_all_products_success():
    mock_data = [{"title": "Test Product", "price": "10.00"}]
    
    with patch('src.crawler.crawler.fetch_page_data_and_quit', 
            return_value=mock_data):
        products = await crawler.crawl_all_products(1)
        assert len(products) == 1
        assert products[0]["title"] == "Test Product"

@pytest.mark.asyncio
async def test_crawl_all_products_invalid_values():
    with pytest.raises(ValueError):
        await crawler.crawl_all_products(0)
    with pytest.raises(ValueError):
        await crawler.crawl_all_products(95)