# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 12:12:09 2019

@author: pathouli
"""
import tweepy
from textwrap import TextWrapper
from hw4_model import hw4_model
from sklearn.ensemble import RandomForestClassifier

class sniffer(tweepy.StreamListener):

    #MODEL TRAINING
	#Define path	
    training_data_path = 'C:/Users/Timothy/Google Drive/TC Stuff/Analytics/GR 5067 - Natural Language Processing in Social Sciences/HW4/the_data/data/'
			
	#Create model training object
    model = hw4_model()
    
    #call up of function fetch_df
    the_df = model.fetch_df(the_path_in = training_data_path)
    
    #TFIDF
    tfidf_mat, tfidf_df = model.tfidf_function(the_df.body)
    
    #call up PCA function of above and determine optimal component count for a 'small' test size
    my_dim, pca = model.iterate_var(tfidf_df, 0.95)
		
	#Initialise a RandomForestClassifier object
    clf_pca = RandomForestClassifier()
		
	#paramters to exhaustively iterate through
    param_grid = {"max_depth": [10, 50, 100],
					  "n_estimators": [16, 32, 64],
					  "random_state": [1234]
					  }

	#call up grid search to find the best model
	#Wait here we are using my_xform_tfidf, which has not been transformed by PCA?
	#We should be using my_dim, which has been transformed with PCA right?
    gridsearch_model, best, opt_params = model.grid_search_func(param_grid,
																		clf_pca,
																		tfidf_df,
																		the_df.label
																		)
		
	#call up new model and input optimal paramters from above
	#Create new random forest object
    clf_pca = RandomForestClassifier()
					
	#Define the classifier with the optimal paramters
    clf_pca.set_params(**gridsearch_model.best_params_)
		
	#Train the model using our data
	#my_dim - the data
	#the_df.label - the correct answer
    clf_pca.fit(my_dim, the_df.label)
    
    #Define global variables
    global senti_tfidf
    global senti_pca
    global senti_model
    
    #Assign values to global variables
    senti_tfidf = tfidf_mat
    senti_pca = pca
    senti_model = clf_pca
   

    def on_status(self, status):
        try:
            #Create model training object
            model = hw4_model()
            
            status_wrapper = TextWrapper(width=140, initial_indent='', subsequent_indent='')
            my_dict = dict()
            my_dict['body'] = status_wrapper.fill(status.text)
            my_dict['isRetweet'] = status.retweeted
            my_dict['userLanguage'] = status.user.lang
            my_dict['urls'] = status.entities['urls']
            my_dict['place'] = status.place
            my_dict['followerCount'] = status.user.followers_count
            my_dict['screenName'] = status.author.screen_name
            my_dict['friendCount'] = status.user.friends_count
            my_dict['createdAt'] = status.created_at
            my_dict['messageId'] = status.id
            
			#Use the model on our tweet body to get the predicted label and probability
            probability, prediction = model.fetch_prediction(my_dict['body'], senti_tfidf, senti_pca, senti_model)
            my_dict['classified'] = prediction
            my_dict['probability'] = probability      
            
            print("Tweet Body: \n")
            print(my_dict['body'])
            
            print("Tweet Classification: \n")
            print(my_dict['classified'])
            
            print("Classification Probability:")
            print("Democrat: Republican:")
            print(my_dict['probability'])

        except:
            pass

        return my_dict
		
		

		


	
		
		
