from property_parser import retreive_xml, parse_xml, create_csv
import os.path
from xml.etree.ElementTree import parse

def test_retreive_xml():
    """
    Test good and bad links or none existent xml

    """


    x = retreive_xml('https://www.amazon.com/walterwhiteiscool')
    assert x is None

    x = retreive_xml('http://syndication.enterprise.websiteidx.com/feeds/BoojCodeTest.xml')
    assert x is not None


def make_test_xml():
    """
    Used to make valid or invalid XMLs
    """

    tree = parse('xml_template.xml')
    root = tree.getroot()
    test_dict = {}
    test_dict['MlsId'] = '2393364202'
    test_dict['MlsName'] = 'La Rumba'
    test_dict['DateListed'] = '2016-09-07 00:00:00'
    test_dict['StreetAddress'] = '4 Asada St'
    test_dict['Price'] = '2.00'
    test_dict['Bedrooms'] = '0'
    test_dict['FullBathrooms'] = '0'
    test_dict['HalfBathrooms'] = '3'
    test_dict['ThreeQuarterBathrooms'] = '12'
    test_dict['Description'] = '2'*200 + 'and'

    for mls_id in root.iter('MlsId'):
        mls_id.text = test_dict['MlsId']

    for mls_name in root.iter('MlsName'):
        mls_name.text = test_dict['MlsName']

    for date_listed in root.iter('DateListed'):
        date_listed.text = test_dict['DateListed']

    for street_address in root.iter('StreetAddress'):
        street_address.text = test_dict['StreetAddress']

    for price in root.iter('Price'):
        price.text = test_dict['Price']

    for bedrooms in root.iter('Bedrooms'):
        bedrooms.text = test_dict['Bedrooms']

    for full_bathrooms in root.iter('FullBathrooms'):
        full_bathrooms.text = test_dict['FullBathrooms']

    for half_bathrooms in root.iter('HalfBathrooms'):
        half_bathrooms.text = test_dict['HalfBathrooms']

    for three_quarter_bathrooms in root.iter('ThreeQuarterBathrooms'):
        three_quarter_bathrooms.text = test_dict['ThreeQuarterBathrooms']

    for description in root.iter('Description'):
        description.text = test_dict['Description']


    tree.write('xml_template.xml')
    return test_dict


def test_parse_xml():
    """
    Test for valid or invalid listings
    """
    test_dict = make_test_xml()
    with open('xml_template.xml') as file:
        valid_listings = parse_xml(file.read())
        assert valid_listings == []




def test_create_csv():
    """
    Test iF CSV got created

    """
    test_dict = make_test_xml()
    file_name = 'test.csv'
    with open('xml_template.xml') as file:
        valid_listings = parse_xml(file.read())
        if valid_listings:
            create_csv(file_name, valid_listings)
            assert os.path.isfile(file_name)




def main():
    #test_retreive_xml()

    #test_parse_xml()

    test_create_csv()


if __name__ == "__main__":
    main()
