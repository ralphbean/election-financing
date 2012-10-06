import urllib

""" Just some scratch work here. """


url = "http://www.monroecounty.gov/swf/php/property/prop_search_2.php"
post_data="info=SWIS%09parcelID%09tax%09num%09street%09zip%09ext%3BSWIS%20Code%09Parcel%20ID%09undefined%09Number%09Brentwood%09Zip%09undefined&siteType=R&searchtype=report&action=prop%5Fsearch"

mystery_payload = [
    'SWIS',
    'parcelID',
    'tax',
    'num',
    'street',
    'zip',
    'ext;SWIS Code',
    'Parcel ID',
    'undefined',
    'Number',
    'Brentwood',
    'Zip',
    'undefined',
]

urllib.quote_plus = urllib.quote
data = urllib.urlencode([
    # Who wrote this thing?  Why tabs?
    ('info', '\t'.join(mystery_payload)),
    ('siteType', 'R'),
    ('searchtype', 'report'),
    ('action', 'prop search'),
])

print data
print post_data
assert(data==post_data)
