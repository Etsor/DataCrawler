import logging
from lxml import etree

import src.config.log_config

def validate_xml(xml_file: str, xsd_file: str) -> bool:
    try:
        with open(xsd_file, "rb") as xsd_f:
            schema_root = etree.XML(xsd_f.read())
        
        schema = etree.XMLSchema(schema_root)

        with open(xml_file, "rb") as xml_f:
            try:
                xml_doc = etree.parse(xml_f)
            except etree.XMLSyntaxError as e:
                logging.error(f"XML syntax error: {e}")

        if schema.validate(xml_doc):
            logging.info("XML is valid")
            return True
        else:
            logging.error("XML validation failed:")
            logging.error(schema.error_log)
            return False
    
    except FileNotFoundError as e:
        logging.error(f"File not found: {e}")
        raise
    
    except Exception as e:
        logging.error(f"Validation error: {e}")
        raise
