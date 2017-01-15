'''
Created on 14 Jan 2016

@author: ranganathan.veluswamy
'''
import json
import time

import requests


class sessionObject(object):
    
    def __init__(self, username, password, baseURL):
        self.username = username #API_CREDENTIALS.apiUsername
        self.password = password #API_CREDENTIALS.apiPassword
        self.url = baseURL
        self.headers  = {'Accept':'application/vnd.alertme.zoo-6.0+json',
                         'X-AlertMe-Client':'KG',
                         'Content-Type':'application/json'}

        self.sessionId, self.userId, self.latestSupportedApiVersion, self.statusCode, self.response  = getSessionToken(self.username,self.password, self.url)
        self.headers['X-Omnia-Access-Token'] = self.sessionId
        return

def getSessionToken(username, password, baseURL):
    """ Login and get a session token for the user
        Used by the sessionObject class to get the session token
    """    
    url = baseURL+ '/omnia/auth/sessions'
    payload = json.dumps({'sessions':[ {'username':username,'password':password}]})
    headers = {'Accept':'application/vnd.alertme.zoo-6.0+json',
               'X-AlertMe-Client':'KG',
               'Content-Type':'application/json'}
    
    r = requests.post(url, data=payload, headers=headers)
    #print("respose for the Login")
    #print(r.json)
    if r.status_code!=200:
        print("ERROR in getSessionToken(): ",r.status_code,r.reason,r.url,r.text)
        print(r.text)
        return "", username, "", r.status_code,r.text
    latestSupportedApiVersion = ''
    session = r.json()['sessions'][0]
    userId = session['userId']
    sessionId = session['sessionId']
    username = session['username']
    if 'latestSupportedApiVersion' in session: 
        latestSupportedApiVersion = session['latestSupportedApiVersion']
    return sessionId, userId, latestSupportedApiVersion, r.status_code,r.text


def deleteSessionV6(session):
    """ Logout from session
    """
    url = session.url + '/omnia/auth/sessions/{}'.format(session.sessionId)
    r = requests.delete(url,headers=session.headers)
    if r.status_code!=200:
        print("ERROR in deleteSession(): ",r.status_code,r.reason,r.url,r.text)
        exit()
    return

def getNodesV6(session):
    """
    """
    url = session.url + '/omnia/nodes/'
    r = requests.get(url, headers=session.headers)
    
    if r.status_code!=200:
        print("ERROR in getNodes(): ",r.status_code,r.reason,r.url,r.text)
        exit()
    return r.json() 

def setSmartPlugState(session,nodeId,state):
    """ Set the state of the smart plug
        PUT /omina/nodes/{nodeId}
        Payload = {"nodes":[{"attributes": {"state":{"targetValue":state}]}
        200 = Success
            
    """
    success = False
    payload=json.dumps({"nodes":[{"attributes": {"state":{"targetValue":state}}}]})
    url = session.url + '/omnia/nodes/{}'.format(nodeId)
    r = requests.put(url, headers=session.headers,data=payload)
    if r.status_code==200: success=True
    return r,success

if __name__ == '__main__':
    username = "tester9_v6"
    password = "Password1"
    url = "https://api.internalprod.zoo.alertme.com"
    session = sessionObject(username, password, url)
    respJson = getNodesV6(session)
    model = "SLP2"
    strNode = ""
    for oNode in respJson['nodes']:
        if ('supportsHotWater'  not in oNode['attributes']) and "nodeType" in oNode:
            if '.json' in oNode["nodeType"] and "model" in oNode["attributes"]:
                if "reportedValue" in oNode["attributes"]["model"]:
                    strModel = oNode["attributes"]["model"]["reportedValue"]
                    if model == strModel:
                        strNode= oNode["id"]
                        break
    if not strNode is "":
        setSmartPlugState(session, strNode, "ON")
        for intCntr in range(0,5):
            setSmartPlugState(session, strNode, "OFF")
            time.sleep(1)
            setSmartPlugState(session, strNode, "ON")
            time.sleep(1)
        
    #print(json.dumps(respJson, indent=4, sort_keys=False))
    deleteSessionV6(session)