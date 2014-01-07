import urllib2
import urllib
import json
from xml.dom import minidom as xml

class LookUpError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class LookUp():
    def __init__(self, method="http", output="json", address=None, latlng=None, bounds=None, region=None, language=None, sensor=False):
        self.method = method.lower()
        self.output = output.lower()
        self.address = address
        self.latlng = latlng
        self.bounds = bounds
        self.region = region
        self.language = language
        self.sensor = sensor

        method_types = ['https', 'http']
        if self.method not in method_types:
            raise LookUpError('Method type not %s' % (' or '.join(method_types)))

        output_types = ['json', 'xml']
        if self.output not in output_types:
            raise LookUpError('Output type not %s' % (' or '.join(output_types)))

        if self.address and self.latlng:
            raise LookUpError('Supplied both forward and reverse lookup. Need one or the either.')

        params = dict()

        if not self.sensor:
            params['sensor'] = 'false'
        else:
            params['sensor'] = 'true'

        if self.address:
            params['address'] = self.address

        if self.latlng:
            params['latlng'] = ",".join(((i.strip()) for i in self.latlng.split(",")))

        if self.bounds:
            params['bounds'] = self.bounds

        if self.region:
            params['region'] = self.region

        if self.language:
            params['language'] = self.language

        req_string = "&".join("%s=%s" % (k, urllib.quote(params[k])) for k in params.keys())
        req_string = "?".join((self.output, req_string))
        base_url = "".join((self.method, "://maps.googleapis.com/maps/api/geocode/"))
        full_url = "".join((base_url, req_string))

        try:
            req = urllib2.Request(full_url)
            req_result = urllib2.urlopen(req).read()
        except urllib2.URLError, e:
            raise LookUpError('IOError error: %s' % e)
        except urllib2.HTTPError, e:
            raise LookUpError('HTTP error: %s ' % e)

        if output == 'xml':
            result = xml.parseString(req_result)
            status = result.getElementsByTagName('status')[0].childNodes[0].data
        else:

            result = json.loads(req_result)
            status = result['status']

        status_returns = {
            "ZERO_RESULTS" : "indicates that the geocode was successful but returned no results. This may occur if the geocode was passed a non-existent address or a latlng in a remote location.",
            "OVER_QUERY_LIMIT" : "indicates that you are over your quota.",
            "REQUEST_DENIED" : "indicates that your request was denied, generally because of lack of a sensor parameter.",
            "INVALID_REQUEST" : "generally indicates that the query (address or latlng) is missing."
        }
        if status != "OK":
            raise LookUpError(" ".join((status, status_returns[status])))
        else:
            self.result = result

__all__ = ['LookUp', 'LookUpError']
