from requests import get, Timeout, ConnectionError
from json import loads


class LocationInfo:
    api_url = 'http://ip-api.com/json/%s'

    def __init__(self,
                 country: str,
                 country_ode: str,
                 region: str,
                 region_name: str,
                 city: str,
                 zip_code: int,
                 lat: float,
                 lon: float,
                 timezone: str,
                 isp: str,
                 org: str,
                 as_: str,
                 query: str
                 ):


    @staticmethod
    def get(ip: int):
        try:
            response = get(LocationInfo.api_url, timeout=10)
        except ConnectionError:
            pass
        except Timeout:
            pass
