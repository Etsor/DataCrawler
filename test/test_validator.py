import pytest
from src.writer.validator import validate_xml

@pytest.fixture
def test_files(tmp_path):
    xml_file = tmp_path / "test.xml"
    xsd_file = tmp_path / "test.xsd"
    return xml_file, xsd_file

def test_validate_xml_success(test_files):
    xml_file, xsd_file = test_files

    xml_file.write_text("<root><item>test</item></root>")
    xsd_file.write_text('''<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
                            <xs:element name="root">
                                <xs:complexType>
                                    <xs:sequence>
                                        <xs:element name="item" type="xs:string"/>
                                    </xs:sequence>
                                </xs:complexType>
                            </xs:element>
                        </xs:schema>''')

    assert validate_xml(str(xml_file), str(xsd_file)) is True

def test_validate_xml_failure(test_files):
    xml_file, xsd_file = test_files
    
    xml_file.write_text("<root><aboba>test</aboba></root>")
    xsd_file.write_text('''<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
                            <xs:element name="root">
                                <xs:complexType>
                                    <xs:sequence>
                                        <xs:element name="item" type="xs:string"/>
                                    </xs:sequence>
                                </xs:complexType>
                            </xs:element>
                        </xs:schema>''')

    assert validate_xml(str(xml_file), str(xsd_file)) is False

def test_validate_missing_files():
    with pytest.raises(FileNotFoundError):
        validate_xml("nonexistent.xml", "schema.xsd")
