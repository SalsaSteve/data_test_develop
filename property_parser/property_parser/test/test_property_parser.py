from property_parser import property_parser


def test_retreive_xml():

    x = property_parser.retreive_xml('https://www.amazon.com/walterwhiteiscool')
    assert x is None

    x = property_parser.retreive_xml('http://syndication.enterprise.websiteidx.com/feeds/BoojCodeTest.xml')
    assert x is not None