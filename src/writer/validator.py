import src.config.log_config as log_config
import logging
from lxml import etree

def validate_xml(xml_file: str, xsd_file: str) -> bool:
    with open(xsd_file, "rb") as xsd_f:
        schema_root = etree.XML(xsd_f.read())
    
    schema = etree.XMLSchema(schema_root)

    with open(xml_file, "rb") as xml_f:
        xml_doc = etree.parse(xml_f)

    if schema.validate(xml_doc):
        logging.info("XML is valid")
        return True
    else:
        logging.error("XML validation failed:")
        logging.error(schema.error_log)
        return False
