'''
Created on May 21, 2015

@author: jsdery
'''

from tweetscan.twitter_account import TwitterAccount 
import logging

if __name__ == '__main__':
    
    TWITTER_RATE_LIMIT_ERROR_CODE = 88
    FOLLOWERS_NUMBER_LIMIT = 50
    
    logging.info("About to authenticate with Twitter and get the neighbors of your vertex in the 'friends' graph.")
    
    try:
        twitter_account = TwitterAccount()
        auth_user_id = twitter_account.getAuthenticatedUserId()
        neighbors_list = twitter_account.getListOfFriendsFromId(user_id=auth_user_id)
    
        print("There are '"+str(len(neighbors_list))+"' direct neighbors that were collected from user ID '"+str(auth_user_id)+"'.")
        print("Creating the adjacency list of the graph")
        
        for neighbor_id in neighbors_list:
            print("Current neighbor_id ID '"+str(neighbor_id)+"'")
            
            neighbors_of_neighbor = twitter_account.getListOfFriendsFromId(user_id=neighbor_id)
            
            print("There are '"+str(len(neighbors_of_neighbor))+"' neighbors of neighbors that were added to the adjacency list.")
    except Exception as exception:
        # TODO: Will potentially need to handle different types of exceptions.
        print(exception.args)
        