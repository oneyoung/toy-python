#!/usr/bin/env python3
import urllib.request
import re
import json

urlopen = urllib.request.urlopen


def query_hostip(ip_addr):
    ''' return "country - city"
    example result of hostip.info
    -----------------------------
    Country: UNITED STATES (US)
    City: Aurora, TX

    Latitude: 33.0582
    Longitude: -97.5159
    IP: 12.215.42.19
    -----------------------------
    '''
    url = 'http://api.hostip.info/get_html.php?ip=%s&position=true' % ip_addr

    reg_expr = r"Country: (?P<country>.+)\W+" + \
               r"City: (?P<city>.+)\W+" + \
               r"Latitude: (?P<latitude>.+)\W+" + \
               r"Longitude: (?P<longtitude>.+)\W+" + \
               r"IP: (?P<IP>.+)\W*"
    response = urlopen(url).read().decode()
    m = re.match(reg_expr, response)
    if m:
        result = m.groupdict()
        return "%s - %s" % (result['country'], result['city'])
    else:
        return "Unknown"


def query_ipinfodb(ip_addr):
    ''' example query result:
    {'cityName': 'MOUNTAIN VIEW',
     'countryCode': 'US',
     'countryName': 'UNITED STATES',
     'ipAddress': '8.8.8.8',
     'latitude': '37.3861',
     'longitude': '-122.084',
     'regionName': 'CALIFORNIA',
     'statusCode': 'OK',
     'statusMessage': '',
     'timeZone': '-07:00',
     'zipCode': '94043'}
     '''
    api_key = "e4da25257ba7881f043f5944bc7a3e021ef9c9c73d5e8d3cc976bffb714760cf"
    url = "http://api.ipinfodb.com/v3/ip-city/?key=%s&ip=%s&format=json" % (api_key, ip_addr)

    response = urlopen(url)
    dictdata = json.loads(response.read().decode())
    response.close()
    if dictdata['statusCode'] != 'OK':
        return "Unknown"
    else:
        return "%s - %s" % (dictdata['countryName'], dictdata['cityName'])
        #return "%s - %s" % (dictdata['latitude'], dictdata['longitude'])


def ip_location(ip):
    #return ip_location_hostip(ip)
    return query_ipinfodb(ip)


if __name__ == '__main__':
    import sys
    import socket

    if len(sys.argv) != 2:
        print("Syntax: %s host" % sys.argv[0])
    try:
        ip_addr = socket.gethostbyname(sys.argv[1])
    except:
        print("ERROR: Please give a valid host.")
        exit(-1)
    print("IP:%s \t%s" % (ip_addr, ip_location(ip_addr)))
    exit(0)
