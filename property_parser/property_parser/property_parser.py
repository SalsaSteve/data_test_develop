import requests, xmltodict


def retreive_xml(xml_url):
    """
    Retrieve property xml to be parse into CSV

    :param xml_url: URL to XML
    :return: xml formatted data
    """

    try:
        r = requests.get(xml_url)
        r.raise_for_status()
        raw_xml = r.content
    except Exception as err:
        print(err)
        raw_xml = None

    return raw_xml


def main():
    raw_xml = retreive_xml('http://syndication.enterprise.websiteidx.com/feeds/BoojCodeTest.xml')
    if raw_xml:
        doc = xmltodict.parse(raw_xml)

        for i in doc['Listings']['Listing']:
            print(i)

if __name__ == "__main__":
    main()