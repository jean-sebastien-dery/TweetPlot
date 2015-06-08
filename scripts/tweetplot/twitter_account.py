"""
Created on May 21, 2015

@author: Jean-Sebastien Dery
"""

from tweepy import OAuthHandler
from tweepy import Cursor
from tweepy import API
#from graph_tool import Graph
from graph_tool.all import *
from configparser import ConfigParser
import os.path
from tweepy.error import TweepError


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
        self._configFile = ConfigParser()
        
        if (not os.path.isfile(config_file_name)):
            raise ValueError("The authentication config file cannot be found.", "Name of config = "+self._CONFIG_FILE_NAME)
        
        self._configFile.read(config_file_name)
        
        self._consumer_key = self._configFile.get(TwitterAuthParams.__CONFIG_SECTION_NAME, TwitterAuthParams.__CONSUMER_KEY_VAR_NAME)
        self._consumer_secret = self._configFile.get(TwitterAuthParams.__CONFIG_SECTION_NAME, TwitterAuthParams.__CONSUMER_SECRET_VAR_NAME)
        self._access_token_key = self._configFile.get(TwitterAuthParams.__CONFIG_SECTION_NAME, TwitterAuthParams.__ACCESS_TOKEN_KEY_VAR_NAME)
        self._access_token_secret = self._configFile.get(TwitterAuthParams.__CONFIG_SECTION_NAME, TwitterAuthParams.__ACCESS_TOKEN_SECRET_VAR_NAME)
    
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
    Represents an authenticated Twitter account.
    '''
    
    __MAX_NUMBER_OF_IDS = 100
    __MAX_NUMBER_ERRORS = 100
    
    def __init__(self, twitter_auth_params):
        '''
        Constructor
        '''
        auth = OAuthHandler(twitter_auth_params.getConsumerKey(), twitter_auth_params.getConsumerSecret())
        auth.secure = True
        auth.set_access_token(twitter_auth_params.getAccessTokenKey(), twitter_auth_params.getAccessTokenSecret())
        self.__twitterApi = API(auth)
    
    def getAuthenticatedUserId(self):
        return self.__twitterApi.me().id
        
    def getListOfFriendsFromId(self, user_id):
        friends_ids_list = []
        error_count = 0
        sending_requests = True
        
        while (sending_requests):
            try:
                for friend_id in Cursor(self.__twitterApi.friends_ids, user_id=user_id, monitor_rate_limit=True, wait_on_rate_limit=True).items():
                    friends_ids_list.append(friend_id)
                    
                sending_requests = False
            except (TweepError, ConnectionResetError) as exception:
                print("An error occurred while sending the request to Twitter, trying again...")
                print(exception)
                error_count += 1
                
                if error_count == TwitterAccount.__MAX_NUMBER_ERRORS:
                    print("It's been "+str(TwitterAccount.__MAX_NUMBER_ERRORS)+" times in a row that we were enable to send requests to Twitter. Raising exception.")
                    raise exception

        return friends_ids_list
    
    def convertIdsToScreenName(self, id_list):
        
        if len(id_list) > TwitterAccount.__MAX_NUMBER_OF_IDS:
            raise ValueError("The number of IDs to be converted is more than "+TwitterAccount.__MAX_NUMBER_OF_IDS, "len(list of IDs)="+str(len(id_list)))
        
        print("converted!")

class TwitterGraphCreator(object):
    
    __ORIG_VERTEX_POS = 0
    __DEST_VERTEX_LIST = 1
    __ADJ_LIST_ORIG_DELIMITER = "="
    __ADJ_LIST_DEST_DELIMITER = ","
#     __VERTEX_PROPERTY_TYPE = "string"
#     __VERTEX_PROPERTY_NAME = "screen_name"
    
    def __init__(self, adjacency_list):

        self.__vertex_dict = {}
        self.__friends_graph = Graph()
#         self.__vertices_props = self.__friends_graph.new_edge_property(TwitterGraphCreator.__VERTEX_PROPERTY_TYPE)
        
        for neighbor_list in adjacency_list:
            #print("Adding: "+neighbor_list)
            
            orig_vertex = self.__getOrigVertex(neighbor_list)
            dest_vertex_list = self.__getDestVertexList(neighbor_list)
            
            for dest_vertex in dest_vertex_list:
                self.__addEdge(orig_vertex, dest_vertex)
        
    def __addEdge(self, orig_vertex, dest_vertex):
        #print("Adding from "+orig_vertex+" to "+dest_vertex)
        orig_vertex_inst = self.__getVertexInstance(orig_vertex)
        dest_vertex_inst = self.__getVertexInstance(dest_vertex)
        self.__friends_graph.add_edge(orig_vertex_inst, dest_vertex_inst)
        
    def __getVertexInstance(self, vertex_name):
        vertex_inst = self.__vertex_dict.get(vertex_name)
        if vertex_inst is None:
            vertex_inst = self.__friends_graph.add_vertex()
            self.__vertex_dict[vertex_name] = vertex_inst
#             self.__vertices_props[vertex_inst] = vertex_name
        return vertex_inst
        
    def __getOrigVertex(self, neighbor_list):
        return neighbor_list.split(sep=TwitterGraphCreator.__ADJ_LIST_ORIG_DELIMITER)[TwitterGraphCreator.__ORIG_VERTEX_POS]
    
    def __getDestVertexList(self, neighbor_list):
        dest_vertices = neighbor_list.split(sep=TwitterGraphCreator.__ADJ_LIST_ORIG_DELIMITER)[TwitterGraphCreator.__DEST_VERTEX_LIST]
        return dest_vertices.split(sep=TwitterGraphCreator.__ADJ_LIST_DEST_DELIMITER)
    
    def writeGraphToFile(self, file_name, graph_size):
        graph_draw(g=self.__friends_graph, output = file_name, pos = arf_layout(self.__friends_graph, max_iter=0))
#         self.__friends_graph.vertex_properties[TwitterGraphCreator.__VERTEX_PROPERTY_NAME] = self.__vertices_props
#         graph_draw(self.__friends_graph, vertex_text=self.__friends_graph.vertex_index, vertex_font_size=10, output_size=(graph_size, graph_size), output=file_name)
