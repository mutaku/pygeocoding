# pygeocoding #

### Python API wrapper to interact with Google Geocoding for Maps API ###
https://developers.google.com/maps/documentation/geocoding/

The intent is to provide a Pythonistic interface in building your Google 
Maps such as building a Google Map in Django with locations stored in your models.
As noted on the API page:

>Note: the Geocoding API **may only be used in conjunction with a Google map;** geocoding results without displaying them on a map is prohibited. For complete details on allowed usage, consult the Maps API Terms of Service License Restrictions.

Some example usage:

```python
import pygeocoding

# Let's find CERN
pygeocoding.LookUp(address="CERN CH-1211 Genève 23 Switzerland")
{u'status': u'OK', u'results': [{u'geometry': {u'location_type': u'APPROXIMATE', # ... truncated output

# We can also search backwards - let's pipe in the lat/long of the liberty bell (approximately)
# - we'll just see what the first result is
r = pygeocoding.LookUp(latlng="39.9518819802915,-75.1476150197085")
r['result'][0]

```