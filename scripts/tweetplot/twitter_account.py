'''
Created on May 21, 2015

@author: jsdery
'''

import tweepy
import ConfigParser
import os.path

class TwitterAccount(object):
    '''
    classdocs
    '''
    
    _CONFIG_FILE_NAME = "twitterAuthInformation.ini"
    _CONFIG_SECTION_NAME = "TwitterScan.Auth"
    _CONSUMER_KEY_VAR_NAME = "consumer_key"
    _CONSUMER_SECRET_VAR_NAME = "consumer_secret"
    _ACCESS_TOKEN_KEY_VAR_NAME = "access_token_key"
    _ACCESS_TOKEN_SECRET_VAR_NAME = "access_token_secret"

    def __init__(self):
        '''
        Constructor
        '''        
        
        self._getAuthParamsFromConfig()
        
        if self._areAuthParamsMissing():
            auth = tweepy.OAuthHandler(self._consumer_key, self._consumer_secret)
            auth.secure = True
            auth.set_access_token(self._access_token_key, self._access_token_secret)
            self._twitterApi = tweepy.API(auth)
        else:
            raise ValueError("At least one authentication parameter from the config file is missing.", self._CONSUMER_KEY_VAR_NAME+"="+self._consumer_key, self._CONSUMER_SECRET_VAR_NAME+"="+self._consumer_secret, self._ACCESS_TOKEN_KEY_VAR_NAME+"="+self._access_token_key, self._ACCESS_TOKEN_SECRET_VAR_NAME+"="+self._access_token_secret)
        
    def _getAuthParamsFromConfig(self):
        self._configFile = ConfigParser.ConfigParser()
        
        if (not os.path.isfile(self._CONFIG_FILE_NAME)):
            raise ValueError("The authentication config file cannot be found.", "Name of config = "+self._CONFIG_FILE_NAME)
        
        self._configFile.read(self._CONFIG_FILE_NAME)
        
        self._consumer_key = self._configFile.get(self._CONFIG_SECTION_NAME, self._CONSUMER_KEY_VAR_NAME)
        self._consumer_secret = self._configFile.get(self._CONFIG_SECTION_NAME, self._CONSUMER_SECRET_VAR_NAME)
        self._access_token_key = self._configFile.get(self._CONFIG_SECTION_NAME, self._ACCESS_TOKEN_KEY_VAR_NAME)
        self._access_token_secret = self._configFile.get(self._CONFIG_SECTION_NAME, self._ACCESS_TOKEN_SECRET_VAR_NAME)
        return;
    
    def _areAuthParamsMissing(self):
        if (not self._consumer_key) or (not self._consumer_secret) or (not self._access_token_key) or (not self._access_token_secret):
            return False
        else:
            return True
    
    def getAuthenticatedUserId(self):
        return self._twitterApi.me().id
        
    def getListOfFriendsFromId(self, user_id):
        friends_ids_list = []
        
        for friend_id in tweepy.Cursor(self._twitterApi.friends_ids, user_id=user_id, monitor_rate_limit=True, wait_on_rate_limit=True).items():
            print("Adding '"+str(friend_id)+"' to the list of friends")
            friends_ids_list.append(friend_id)
            
        return friends_ids_list