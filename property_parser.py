import requests, xmltodict, csv, datetime


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
        raw_xml = None
        print(err)

    return raw_xml


def parse_xml(xml_file):
    """
    Parse xml for valid properties
    -Contains only properties listed from 2016 [DateListed]
    -Contains only properties that contain `and' in the Description field

    :param xml_file: XML Containing property information
    :return: array of dictionaries of valid properties
    """

    valid_listings = []
    try:
        doc = xmltodict.parse(xml_file)
        # iterate over all properties and stored valid ones into valid_listing
        if isinstance(doc['Listings']['Listing'], list):
            for idx, listing in enumerate(doc['Listings']['Listing']):
                year = listing['ListingDetails']['DateListed'][:4]
                if year == '2016' and 'and' in listing['BasicDetails']['Description']:
                    valid_listings.append(listing)
        else:
            listing = doc['Listings']['Listing']
            year = listing['ListingDetails']['DateListed'][:4]
            if year == '2016' and 'and' in listing['BasicDetails']['Description']:
                valid_listings.append(listing)

    except Exception as err:
        valid_listing = None
        print(err)

    return valid_listings


def create_csv(file_name, properties):
    """
    Create CSV with properties ordered by DateListed
    Required fields:
    -MlsId
    -MlsName
    -DateListed
    -StreetAddress
    -Price
    -Bedrooms
    -Bathrooms
    -Appliances (all sub-nodes comma joined)
    -Rooms (all sub-nodes comma joined)
    -Description (the first 200 characters)

    :param file_name: output CSV file name
    :param properties: filtered properties
    :return: True or False
    """

    properties.sort(key=lambda prop: datetime.datetime.strptime(prop['ListingDetails']['DateListed'][:10], '%Y-%m-%d'))

    with open(file_name, 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL)
        for prop in properties:
            mls_id = prop['ListingDetails']['MlsId']
            mls_name = prop['ListingDetails']['MlsName']
            date_listed = prop['ListingDetails']['DateListed']
            street_address = prop['Location']['StreetAddress']
            price = prop['ListingDetails']['Price']
            bedrooms = prop['BasicDetails']['Bedrooms']
            fullbathrooms = prop['BasicDetails']['FullBathrooms']
            fullbathrooms = int(0 if fullbathrooms is None else fullbathrooms)
            halfbathrooms = prop['BasicDetails']['HalfBathrooms']
            halfbathrooms = .5*int(0 if halfbathrooms is None else halfbathrooms)
            threequarterbathrooms = prop['BasicDetails']['ThreeQuarterBathrooms']
            threequarterbathrooms = .75*int(0 if threequarterbathrooms is None else threequarterbathrooms)
            bathrooms = fullbathrooms + halfbathrooms + threequarterbathrooms

            appliances_exist = prop['RichDetails'].get('Appliances')
            appliances = ''
            if appliances_exist:
                appliances_list = appliances_exist['Appliance']
                if isinstance(appliances_list, list):
                    appliances = ",".join(appliances_exist['Appliance'])
                else:
                    appliances = appliances_exist['Appliance']

            rooms_exist = prop['RichDetails'].get('Rooms')
            rooms = ''
            if rooms_exist:
                appliances_list = rooms_exist['Room']
                if isinstance(appliances_list, list):
                    rooms = ",".join(rooms_exist['Room'])
                else:
                    rooms = rooms_exist['Room']

            description = prop['BasicDetails']['Description'][:200]

            filewriter.writerow([mls_id, mls_name, date_listed, street_address, price, bedrooms, bathrooms, appliances, rooms, description])



def main():
    raw_xml = retreive_xml('http://syndication.enterprise.websiteidx.com/feeds/BoojCodeTest.xml')
    if raw_xml:
        valid_listings = parse_xml(raw_xml)

    if valid_listings:
       create_csv('asada.csv', valid_listings)

if __name__ == "__main__":
    main()