#!/usr/bin/env python
#Writtent by Boliang Dai
#Date: 2015 Jun 16
#Arduino UNO + LM35 required
#Arduino UNO sketch required: sketch_k_control
#Citiation:
#konke_example.py from open API, www.ikonke.com

import requests,json,serial

class Kcontrol(object):
    """An instance is a Kcontrol object that contains the necessary information to make
    HTTP GET and POST requests to the konke server in order to gain control to the
    Kmini WiFi plug.
    
    Instance Attributes:
        username [string]:
            username of KK account
        password [string]:
            password to the username
        client_id [string]:
            assigned client id
        client_secret [string]:
            assigned client secret passward
        callbackurl [string]:
            url used for redirecting
        payload [dic]:
            the dictionary containing keys 'username' and 'password'
        headers [dic]:
            the dictionary containing the headers for HTTP POST request
        kopen [bool]:
            indicates if plug is currently in use
        userinfo [dic]:
            dictionary containing information extracted from the JSON returned from the server
        kid [string]:
            the id of K mini plug registered with the server
    
    """
    
    def __init__(self):
        """Initializer: initiates the necesarry attributes"""
        
        self.username = '18626071267' #change this to your username
        self.password = 'dbl920910' #change this to your password
        self.client_id = 'cv9596ptag945tgp' #change this to your assigned client_id
        self.client_secret = 'F3aCD4W53RWjxd0a' #change this to your client_secret
        self.callbackurl = 'http://www.cornell.edu' #change this to your coperation web url
        self.payload = {'username': self.username, 'password': self.password}
        self.headers = {}
        self.kopen = False
        self.userinfo = {}
        self.kid = ""

    def setup(self):
        """Method to request necessary info to control the WiFi plug from the server"""
        
        username = '18626071267' 
        password = 'dbl920910' 
        client_id = 'cv9596ptag945tgp'
        client_secret = 'F3aCD4W53RWjxd0a'
        callbackurl = 'http://www.cornell.edu'
        payload = {'username': username, 'password': password}
        r = requests.post('http://kk.bigk2.com:8080/KOAuthDemeter/authorize?client_id=%s&response_type=code&redirect_uri=%s' % (self.client_id,self.callbackurl), params=self.payload) 
        
        code = r.url.split("=",1)[1]
        data = {
                   'grant_type': 'authorization_code', 
                   'client_id': self.client_id, 
                   'client_secret': self.client_secret,
                   'code': code, 
                   'redirect_uri': self.callbackurl
         } 
        r = requests.post('http://kk.bigk2.com:8080/KOAuthDemeter/accessToken', data=data)
        token = eval(r.text)
        print 'access_token :',token['access_token']
        print 'refresh_token:',token['refresh_token']
        self.headers = {'Authorization': 'Bearer %s' % token['access_token']}
        r = requests.post('http://kk.bigk2.com:8080/KOAuthDemeter/UserInfo',headers=self.headers)
        self.userinfo = eval(r.text)
        print "userid:", self.userinfo['userid']
        data = {'userid':self.userinfo['userid']}
        print data
        print self.headers
        
        r = requests.post('http://kk.bigk2.com:8080/KOAuthDemeter/User/getKList',headers=self.headers,json=data)
        rawid = r.content.decode('utf-8')
        content = eval(r.text)
        #print content
        
        self.kid = content['datalist'][0]['kid']
        print "kid is " + self.kid
        print "Finished setting up\n"
    
    def control(self):
        """Method to toggle the WiFi plug on and off depending on the temperature read from
        the Arduino UNO board, which is printed through the serial port"""
        
        print "In Control\n"
        ser = serial.Serial('/dev/cu.usbmodem1421',9600)
        print "Checking current state of K mini...\n"
        
        newdata = {'userid':self.userinfo['userid'],'kid':self.kid}
        r = requests.post('http://kk.bigk2.com:8080/KOAuthDemeter/KInfo/getKState',headers=self.headers,json=newdata)
        result = eval(r.text)
        print "Current state: " + result['data'] +"\n"
        
        if self.isOnline():
            if result['data'] == 'close':
                self.kopen = False
            else: 
                self.kopen = True
            
            count = 0 #an int counter
            
            while True:
                text = ser.readline()
                count = count+1
                print "Counter: " + str(count)
                print text[:-2]
                
                if "Cold" in text:
                    if self.kopen:
                        print "Disengaging Kmini"
                        newdata = {'userid':self.userinfo['userid'],'kid':self.kid,'key':'close'}
                        r = requests.post('http://kk.bigk2.com:8080/KOAuthDemeter/KControl/doSwitchK',headers=self.headers,json=newdata)
                        result = eval(r.text)
                        print "Disengaging "+result['des']
                        self.kopen = False
                        print "WiFi Kmini is now disengaged\n"
                    else:
                        print "WiFi Kmini is not engaged\n"
                elif "Hot" in text:
                    if not self.kopen:
                        print "Engaging Kmini"
                        newdata = {'userid':self.userinfo['userid'],'kid':self.kid,'key':'open'}
                        r = requests.post('http://kk.bigk2.com:8080/KOAuthDemeter/KControl/doSwitchK',headers=self.headers,json=newdata)
                        result = eval(r.text)
                        print "Engaging "+result["des"]
                        self.kopen = True
                        print "WiFi Kmini is now engaged\n"
                    else:
                        print "WiFi Kmini is already engaged\n"
                else:
                    print "In buffer zone, maintaining current state\n"
        else:
            print "Kmini is currently offline, please check connection and relaunch"


    def isOnline(self):
        """Method to check if Kmini is online"""
        
        newdata = {'userid':self.userinfo['userid'],'kid':self.kid}
        r = requests.post('http://kk.bigk2.com:8080/KOAuthDemeter/KInfo/getKState',headers=self.headers,json=newdata)
        result = eval(r.text)
        if result['data'] == 'offline':
            return False
        else:
            return True


if __name__ in ('__android__', '__main__'):
    k = Kcontrol()
    k.setup()
    k.control()
