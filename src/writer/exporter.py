import src.config.log_config as log_config
import logging
import xml.etree.ElementTree as ET
from typing import List, Dict

def save_to_xml(
        products: List[Dict],
        schema_location: str,
        output_file: str):
    
    root = ET.Element("products", {
        "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
        "xsi:noNamespaceSchemaLocation": schema_location
    })

    for product in products:
        product_el = ET.SubElement(root, "product")
        
        ET.SubElement(product_el, "title")\
            .text = product["title"]
        
        ET.SubElement(product_el, "category")\
            .text = product["category"]
        
        ET.SubElement(product_el, "price")\
            .text = product["price"]
        
        ET.SubElement(product_el, "availability")\
            .text = product["availability"]
        
        if product["description"]:
            ET.SubElement(product_el, "description")\
                .text = product["description"]

    tree = ET.ElementTree(root)
    ET.indent(tree, space="\t")
    tree.write(output_file, encoding="utf-8", xml_declaration=True)
    
    logging.info(f"saved to {output_file}")
