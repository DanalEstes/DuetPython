# Python Script that returns axis coordinates of a Duet RepRap based  printer
# Works with RRF2 or RRF3
#
# Copyright (C) 2020 Danal Estes all rights reserved.
# Released under The MIT License. Full text available via https://opensource.org/licenses/MIT
#
# Requires Python3 

import requests
import json
import sys

endpoint2='/rr_status?type=1'   # RRF2 request
endpoint3='/machine/status'     # RRF3 request
endpointA=endpoint2             # Active

def getCoords(base_url):
    global endpointA
    if (endpointA == endpoint2):
        try:
            r = requests.get(f'{base_url}{endpointA}')
            j=json.loads(r.text)
            jc=j['coords']['xyz']
            ret=json.loads('{}')
            for i in range(0,len(jc)):
                ret[ 'xyz'[i] ] = jc[i] 
            return(ret)
        except:
            endpointA = endpoint3
    if (endpointA == endpoint3):    
        try:
            r = requests.get(f'{base_url}{endpointA}')
            j=json.loads(r.text)
            ja=j['result']['move']['axes']
            jd=j['result']['move']['drives']
            ad=json.loads('{}')
            for i in range(0,len(ja)):
                ad[ ja[i]['letter'] ] = ja[i]['drives'][0]
            ret=json.loads('{}')
            for i in range(0,len(ja)):
                ret[ ja[i]['letter'] ] = jd[i]['position']
            return(ret)
        except:
            print(base_url," does not appear to be a RRF2 or RRF3 printer", file=sys.stderr)
            raise
# Test cases
print(getCoords('http://192.168.7.100'))            
print(getCoords('http://127.0.0.1'))            
print(getCoords('http://192.168.7.101')) 

    

