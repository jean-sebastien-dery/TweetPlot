"""
Created on May 21, 2015

@author: Jean-Sebastien Dery
"""

from tweetplot.twitter_account import TwitterAccount
from tweetplot.twitter_account import TwitterAuthParams
import logging

_CONFIG_FILE_NAME = "twitterAuthInformation.ini"

if __name__ == '__main__':
    TWITTER_RATE_LIMIT_ERROR_CODE = 88
    FOLLOWERS_NUMBER_LIMIT = 50

    logging.info("About to authenticate with Twitter and get the neighbors of your vertex in the 'friends' graph.")

    try:
        twitter_auth_params = TwitterAuthParams(_CONFIG_FILE_NAME)
        twitter_account = TwitterAccount(twitter_auth_params)
        auth_user_id = twitter_account.getAuthenticatedUserId()
        neighbors_list = twitter_account.getListOfFriendsFromId(user_id=auth_user_id)

        print("There are '"+str(len(neighbors_list))+"' direct neighbors that were collected from user ID '"+str(auth_user_id)+"'.")
        print("Creating the adjacency list of the graph")
        
        adj_list_file = open('adjacency_list.dat', 'w+')

        for neighbor_id in neighbors_list:
            print("Current neighbor_id ID '"+str(neighbor_id)+"'")

            neighbors_of_neighbor = twitter_account.getListOfFriendsFromId(user_id=neighbor_id)
            
            adjacency_list = str(auth_user_id) + "=" + (",".join(str(neighbor) for neighbor in neighbors_of_neighbor)) + "\n"
            print(adjacency_list)
            adj_list_file.write(adjacency_list)

            print("There are '"+str(len(neighbors_of_neighbor))+"' neighbors of neighbors that were added to the adjacency list.")
    except Exception as exception:
        # TODO: Will potentially need to handle different types of exceptions.
        print("An exception ocured while creating the graph of neighbors.")
        print(exception)
