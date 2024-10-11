"""
Allows you to get approximate position of device via ip
Based on https://ip-api.com
"""

from requests import get, Timeout, ConnectionError
from LocationIP.exceptions import InvalidIP
import re


class LocationInfo:
    """
    Class to represent response object get from https://ip-api.com/json
    """
    api_url = 'http://ip-api.com/json/%s'

    def __init__(self,
                 country: str = None,
                 countryCode: str = None,
                 region: str = None,
                 regionName: str = None,
                 city: str = None,
                 zip: str = None,
                 lat: str = None,
                 lon: str = None,
                 timezone: str = None,
                 isp: str = None,
                 org: str = None,
                 as_: str = None,
                 query: str = None,
                 status: str = None
                 ):
            """
            Default constructor for LocationInfo
            :param country:
            :param countryCode:
            :param region:
            :param regionName:
            :param city:
            :param zip:
            :param lat:
            :param lon:
            :param timezone:
            :param isp:
            :param org:
            :param as_:
            :param query:
            :param status:
            """
            self.country = country
            self.country_code = countryCode
            self.region = region
            self.region_name = regionName
            self.city = city
            self.zip = zip
            self.lat = lat
            self.lon = lon
            self.timezone = timezone
            self.isp = isp
            self.org = org
            self.as_ = as_
            self.query = query
            self.status = status

    def __init__(self, ip: str):
        """
        Returns an object of LocationInfo getting data via provided IP address
        :param ip:
        :return:
        """
        pattern_ipv4 = '((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])'
        pattern_ipv6 = ('('
                        '([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|'
                        '([0-9a-fA-F]{1,4}:){1,7}:|'
                        '([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|'
                        '([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|'
                        '([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|'
                        '([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|'
                        '([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|'
                        '[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|'
                        ':((:[0-9a-fA-F]{1,4}){1,7}|:)|'
                        'fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|'
                        '::(ffff(:0{1,4}){0,1}:){0,1}'
                        '((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}'
                        '(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|'
                        '([0-9a-fA-F]{1,4}:){1,4}:'
                        '((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}'
                        '(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])'
                        ')')

        if not re.fullmatch(pattern=pattern_ipv4, string=ip) and not re.fullmatch(pattern=pattern_ipv6, string=ip):
            raise InvalidIP(f'"{ip}" is not a valid IP address')

        attempts = 0

        try:
            response = get(LocationInfo.api_url % ip, timeout=10)
        except ConnectionError as err:
            print(err)
        except Timeout as err:
            if attempts < 3:
                response = get(LocationInfo.api_url % ip, timeout=10)
            else:
                print(err)
        else:
            location_info = response.json()
            self.country = location_info['country']
            self.country_code = location_info['countryCode']
            self.region = location_info['region']
            self.region_name = location_info['regionName']
            self.city = location_info['city']
            self.zip = location_info['zip']
            self.lat = location_info['lat']
            self.lon = location_info['lon']
            self.timezone = location_info['timezone']
            self.isp = location_info['isp']
            self.org = location_info['org']
            self.as_ = location_info['as']
            self.query = location_info['query']
            self.status = location_info['status']

    def __dict__(self):
        """
        Returns dict() representation of object attributes
        :return:
        """
        return {
            'country': self.country,
            'countryCode': self.country_code,
            'region': self.region,
            'regionName': self.region_name,
            'city': self.city,
            'zip': self.zip,
            'lat': self.lat,
            'lon': self.lon,
            'timezone': self.timezone,
            'isp': self.isp,
            'as': self.as_,
            'query': self.query,
            'status': self.status
        }

    def __iter__(self):
        """
        Allows iteration over object attributes
        :return:
        """
        return iter(self.__dict__().values())


