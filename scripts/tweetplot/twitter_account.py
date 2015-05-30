"""
Created on May 21, 2015

@author: Jean-Sebastien Dery
"""

import tweepy
import ConfigParser
import os.path

class TwitterAuthParams(object):
    """
    Container for the Twitter authentication parameters.
    """
    
    __CONFIG_SECTION_NAME = "TweetPlot.Auth"
    __CONSUMER_KEY_VAR_NAME = "consumer_key"
    __CONSUMER_SECRET_VAR_NAME = "consumer_secret"
    __ACCESS_TOKEN_KEY_VAR_NAME = "access_token_key"
    __ACCESS_TOKEN_SECRET_VAR_NAME = "access_token_secret"
    
    def __init__(self, config_file_name):
        """
        Creates a new instance of TwitterAuthParams.
        
        Args:
            config_file_name (str): The name of the config file containing the auth parameters.
        """
        
        self.__getAuthParamsFromConfig(config_file_name=config_file_name)
        
        if self.__areAuthParamsMissing():
            raise ValueError("At least one authentication parameter from the config file is missing.", self.__CONSUMER_KEY_VAR_NAME+"="+self._consumer_key, self.__CONSUMER_SECRET_VAR_NAME+"="+self._consumer_secret, self.__ACCESS_TOKEN_KEY_VAR_NAME+"="+self._access_token_key, self.__ACCESS_TOKEN_SECRET_VAR_NAME+"="+self._access_token_secret)
        
    def __getAuthParamsFromConfig(self, config_file_name):
        """
        Reads from the specified config file name the Twitter authentication parameters.
        
        Params:
            config_file_name (str): The name of the config file containing the auth parameters.
        """
        self._configFile = ConfigParser.ConfigParser()
        
        if (not os.path.isfile(config_file_name)):
            raise ValueError("The authentication config file cannot be found.", "Name of config = "+self._CONFIG_FILE_NAME)
        
        self._configFile.read(config_file_name)
        
        self._consumer_key = self._configFile.get(self.__CONFIG_SECTION_NAME, self.__CONSUMER_KEY_VAR_NAME)
        self._consumer_secret = self._configFile.get(self.__CONFIG_SECTION_NAME, self.__CONSUMER_SECRET_VAR_NAME)
        self._access_token_key = self._configFile.get(self.__CONFIG_SECTION_NAME, self.__ACCESS_TOKEN_KEY_VAR_NAME)
        self._access_token_secret = self._configFile.get(self.__CONFIG_SECTION_NAME, self.__ACCESS_TOKEN_SECRET_VAR_NAME)
    
    def __areAuthParamsMissing(self):
        """
        Validates if any parameter is missing.
        
        Returns:
            True if there is at least one parameter missing, and False otherwise.
        """
        if (not self._consumer_key) or (not self._consumer_secret) or (not self._access_token_key) or (not self._access_token_secret):
            return True
        else:
            return False
        
    def getConsumerKey(self):
        """
        Returns the Consumer Key value.
        """
        return self._consumer_key
    
    def getConsumerSecret(self):
        """
        Returns the Consumer Secret value.
        """
        return self._consumer_secret
    
    def getAccessTokenKey(self):
        """
        Returns the Access Token Key value.
        """
        return self._access_token_key
    
    def getAccessTokenSecret(self):
        """
        Returns the Access Token Secret value.
        """
        return self._access_token_secret

class TwitterAccount(object):
    '''
    classdocs
    '''
    
    def __init__(self, twitter_auth_params):
        '''
        Constructor
        '''        
        auth = tweepy.OAuthHandler(twitter_auth_params.getConsumerKey(), twitter_auth_params.getConsumerSecret())
        auth.secure = True
        auth.set_access_token(twitter_auth_params.getAccessTokenKey(), twitter_auth_params.getAccessTokenSecret())
        self._twitterApi = tweepy.API(auth)
    
    def getAuthenticatedUserId(self):
        return self._twitterApi.me().id
        
    def getListOfFriendsFromId(self, user_id):
        friends_ids_list = []
        
        for friend_id in tweepy.Cursor(self._twitterApi.friends_ids, user_id=user_id, monitor_rate_limit=True, wait_on_rate_limit=True).items():
            print("Adding '"+str(friend_id)+"' to the list of friends")
            friends_ids_list.append(friend_id)
            
        return friends_ids_list