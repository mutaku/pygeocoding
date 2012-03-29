import urllib2
import urllib
import json    

class LookUpError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class LookUp():
    def __init__(self, output="json", address=None, latlg=None, bounds=None, region=None, language=None, sensor=False):
        self.output = output.lower()
        self.address = address
        self.latlg = latlg
        self.bounds = bounds
        self.region = region
        self.language = language
        self.sensor = sensor
        
        output_types = ['json', 'xml']
        if self.output not in output_types:
            raise LookUpError('Output type not %s' % (' or '.join(output_types)))
        
        if self.address and self.latlg:
            raise LookUpError('Supplied both forward and reverse lookup. Need one or the either.')
    
    def __call__(self, **kwargs):
        kwargs['output'] = self.output
        kwargs['sensor'] = self.sensor
        
        if self.address:
            kwargs['address'] = self.address
        
        if self.latlg:
            kwargs['latlg'] = self.latlg
        
        if self.bounds:
            kwargs['bounds'] = self.bounds
        
        if self.region:
            kwargs['region'] = self.region
            
        if self.language:
            kwargs['language'] = self.language

        params = kwargs.keys()
        
        req_string = "&".join("%s=%s" % (k, urllib.quote_plus(params[k])) for k in params.keys())
        req_string = "?".join((self.output, req_string))
        base_url = "http://maps.googleapis.com/maps/api/geocode/"
        full_url = "".join((base_url, req_string))
        
        req = urllib2.Request(full_url)
        result = urllib2.urlopen(req)
        
        # now we use either json.loads or xml minidom parser depending on output
        # check for status ZERO_RESULTS or OK and either return result or error
        
