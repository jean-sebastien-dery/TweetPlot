"""
Created on May 21, 2015

@author: Jean-Sebastien Dery
"""

from tweetplot.twitter_account import TwitterAccount
from tweetplot.twitter_account import TwitterAuthParams
from tweetplot.twitter_account import TwitterGraphCreator
import logging
import traceback
import time

_CONFIG_FILE_NAME = "twitterAuthInformation.ini"

if __name__ == '__main__':
    TWITTER_RATE_LIMIT_ERROR_CODE = 88
    FOLLOWERS_NUMBER_LIMIT = 50

    logging.info("About to authenticate with Twitter and get the neighbors of your vertex in the 'friends' graph.")

    try:
        
#         list1 = "js=nadim,valentine,benj,bryan,steph,nicolas,antoine,anne-marie,croquette"
#         list2 = "nadim=valentine"
#         list3 = "valentine=nadim,js"
#         list4 = "steph=js,max,bryan"
#         list5 = "bryan=js,steph,valentine,nadim,benj"
#         list6 = "vincent=nicolas,antoine,anne-marie,croquette,js"
#         list7 = "nicolas=antoine,anne-marie,croquette,js,vincent"
#          
#         adjacency_list = [list1,list2,list3]
         
        
        twitter_auth_params = TwitterAuthParams(_CONFIG_FILE_NAME)
        twitter_account = TwitterAccount(twitter_auth_params)
        auth_user_id = twitter_account.getAuthenticatedUserId()
        neighbors_list = twitter_account.getListOfFriendsFromId(user_id=auth_user_id)
   
        print("There are '"+str(len(neighbors_list))+"' direct neighbors that were collected from user ID '"+str(auth_user_id)+"'.")
        print("Creating the adjacency list of the graph")
           
        time_milli = int(round(time.time() * 1000))
        adj_list_file = open("neighbor_list."+str(time_milli)+".dat", 'a')
        adjacency_list = []
   
        for neighbor_id in neighbors_list:
            print("Current neighbor_id ID '"+str(neighbor_id)+"'")
   
            neighbors_of_neighbor = twitter_account.getListOfFriendsFromId(user_id=neighbor_id)
               
            neighbor_list = str(auth_user_id) + "=" + (",".join(str(neighbor) for neighbor in neighbors_of_neighbor)) + "\n"
            print(neighbor_list)
            adjacency_list.append(neighbor_list)
            adj_list_file.write(neighbor_list)
   
            print("There are '"+str(len(neighbors_of_neighbor))+"' neighbors of neighbors that were added to the adjacency list.")

#         adjacency_list = []
#         file = open("neighbor_list.1433525485504.dat", "r")
#         for neighbor_list in file:
#             adjacency_list.append(neighbor_list)
#         file.close()
#         
#         print("There are "+str(len(adjacency_list))+" direct neighbors that will be added to the graph.")
#             
#         graph_creator = TwitterGraphCreator(adjacency_list)
#         graph_creator.writeGraphToFile(file_name="neighbor_graph.pdf", graph_size=100000)
        
    except Exception as exception:
        # TODO: Will potentially need to handle different types of exceptions.
        print("An exception ocured while creating the graph of neighbors.")
        print(exception)
        print(traceback.format_exc())
