import pytest
from unittest.mock import patch
from src.writer.exporter import save_to_xml
import src.config.log_config

@pytest.fixture
def valid_products():
    return [
        {
            "title": "Test Product",
            "category": "Test Category",
            "price": "12.34",
            "availability": "In Stock",
            "description": "Test Description"
        }
    ]

@pytest.fixture
def schema_location():
    return "products.xsd"

@pytest.fixture
def output_file():
    return "test/products.xml"

def test_save_to_xml_success(valid_products, schema_location, output_file):
    with patch('xml.etree.ElementTree.ElementTree.write') as mock_write, \
        patch('logging.info') as mock_logging:
        
        save_to_xml(valid_products, schema_location, output_file)
        
        mock_write.assert_called_once()
        mock_logging.assert_called_once_with(f"saved to {output_file}")

def test_save_to_xml_empty_products(schema_location, output_file):
    with pytest.raises(ValueError) as exc_info:
        save_to_xml([], schema_location, output_file)
    
    assert str(exc_info.value) == "Product list cannot be empty"

def test_save_to_xml_io_error(valid_products, schema_location, output_file):
    with patch('xml.etree.ElementTree.ElementTree.write') as mock_write:
        mock_write.side_effect = Exception("Test error")
        
        with pytest.raises(IOError) as exc_info:
            save_to_xml(valid_products, schema_location, output_file)
        
        assert "Error creating file: Test error" in str(exc_info.value)