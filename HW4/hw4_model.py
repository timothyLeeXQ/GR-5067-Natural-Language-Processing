# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 08:27:24 2019

@author: pathouli
"""

#############
###IMPORTS###
#############

#nltk stop words
from nltk.corpus import stopwords

#re for regex operations
import re

#OS for directory navigation
import os

#Pandas for dataframes and dataframe operations
import pandas as pd

#Sklearn
#TFIDF
from sklearn.feature_extraction.text import TfidfVectorizer

#PCA
from sklearn.decomposition import PCA

#Gridsearch - searches a 'grid' of models with different combinations of parameters
#Outputs best model
from sklearn.model_selection import GridSearchCV



class hw4_model(object):
    ##############################
    ###CLEANING PORTION OF CODE###
    ##############################
    
    #Function to clean up a string. Accepts a string as the argument var
    #Removes stopwords and non-alphabetical characters
    def clean_up_sw(self, var):
        #Create a stopwords object
        stop_words = set(stopwords.words('english'))
        
        #Remove non alphabetical characters in the string
        tmp = re.sub('[^a-zA-Z]+', ' ', var)
        
        #Split the string into a list of words, then remove all the words that are in stop_words
        tmp = [word for word in tmp.split() if word not in stop_words]
        
        #Rejoin the list into a single string, with words separated by spaces
        tmp = ' '.join(tmp) 
        
        #Return the clean string
        return tmp
    
    
    
    #####################################################################
    ###GETTING DATA PORTION OF CODE (THAT INCORPORATES CLEANING ABOVE)###
    #####################################################################
    
    #Function to walk through a directory, read files, clean and pack cleaned body and label to pandas df
    #Accepts a string - a filepath - as an argument
    def fetch_df(self, the_path_in):
        
        #Get the directories within the specified path and store them in the_dirs
        #In the current case where we pass in the_path, we should get 'neg', and 'pos'
        #as the list elements
        the_dirs = os.listdir(the_path_in)
        
        #Initialise the_df_out. This is the return object. Currently, it is a blank data frame,
        #ready to accept the cleaned body and label from each of the files in the training data
        the_df_out = pd.DataFrame()
        
        #For loop that iterates through each of the folders in the listed directory
        for dir_name in the_dirs:
            #Get the directories within the specified path's subfolders. In this case, we get
            #each of the file names inside the 'neg' and 'pos' folders.
            the_filenames = os.listdir(the_path_in + dir_name)
            
            #For loop that iterates through the first 100 files (remove the [1:100] to get all
            #of them instead.
            for word in the_filenames[0:100]:
                
                #Open the file
                f = open(the_path_in + dir_name + '/' + word, "r", encoding = 'ISO-8859-1')
                
                #Read the file 
                tmp_read = str(f.read())
                
                #Clean the file using the clean_up_sw function defined above, then put it into a temporary
                #data frame under the column body
                tmp = pd.DataFrame([self.clean_up_sw(tmp_read)], columns=['body'])
                
                #Put the directory name ('neg' or 'pos') as another column 'label'
                tmp['label'] = dir_name
                
                #Stick the temporary data frame to the main the_df_out df
                the_df_out = the_df_out.append(tmp, ignore_index = True)
    
                #Close the file         
                f.close()
        
        #Return the_df_out
        return the_df_out
    
    
    ###################
    ###VECTORISATION###
    ###################
    
    #Vectorisation involves turning the individual words into features, with frequencies
    #as weights (either raw counts, or TFIDF, as is used here)
    
    def tfidf_function(self, training_data):
        #Create TFIDF object
        my_vec_tfidf = TfidfVectorizer()
        
        #Transform the text using TFIDF
        my_xform_tfidf = my_vec_tfidf.fit_transform(training_data).toarray()        
        
        #Rename the columns of the array to the words
        col_names = my_vec_tfidf.get_feature_names()
        
        #Convert back into a data frame
        my_xform_tfidf = pd.DataFrame(my_xform_tfidf, columns=col_names) 
    
        #return the df
        return(my_vec_tfidf, my_xform_tfidf)
    
    ##################################
    ###DIMENSION REDUCTION WITH PCA###
    ##################################
    
    
    #Function to determine number of components required to achieve user specified var_target 
    #my_xform_tfidf_in - the vector with words as features and TFIDF weights as values
    #var_target is a specified variance level desired
    #data_slice - the number of documents in my_xform_tfidf_in to be used in the training data
    ##The rest of the data will not be passed into our PCA, since we're saving it to test
    def iterate_var(self, my_xform_tfidf_in, var_target):
        
        #Initialise an object to store the total amount of variance the model is accounting for
        var_fig = 0.0
        #Create a counter of the number of components
        cnt = 1
        
        #Keep runing this loop until the variance explained by the model equals or exceeds the target
        while var_fig <= var_target:
            #Create a PCA object with cnt number of components
            #This starts at 1 (see initialisation of cnt above), and increases by 1 with each iteration
            #of the loop
            pca = PCA(n_components=cnt)
            
            #Transform the data along the components of the PCA - somehow this wasn't needed in 
            #the lecture, but without this line, how does the PCA know how much variance it has
            #accounted for without seeing our data?
            my_dim = pca.fit_transform(my_xform_tfidf_in[0:100])
            
            #Get the amount of variance explained by the model
            var_fig = sum(pca.explained_variance_ratio_)   
            
            #Increase the counter by 1 for the next iteration
            cnt += 1
        
        #Decrease the counter by 1, since it would have needlessly been increased by 1 at the
        #end of the loop, even after hitting our target
        cnt -= 1
        
        #Print the number of components in the final model
        #print (cnt)
        
        #Same as above, but now doing it for the output
        pca = PCA(n_components=cnt)
        my_dim = pca.fit_transform(my_xform_tfidf_in)
        var_fig = sum(pca.explained_variance_ratio_) 
        
        #Print the amount of variance accounted for by the final model
        #print (var_fig)
        
        #Return the PCA object and the data transformed by the PCA
        return my_dim, pca


    #######################################
    ###CLASSIFICATION WITH RANDOM FOREST###
    #######################################
    
    #function for optimal parameters to set for random forest
    #Runs a grid search - given a set of values for different parameters, form a grid of all
    #possible variations in parameters
    #Run a model with each possible permutation, and get us back the best model
    #param_grid - the parameters and the values for each of them to try. A dictionary with 
    ##parameter as key and a list of values as value.
    #the_mode_in - Object with the model used - here the random forest object
    #the_vec_in - the data, with features, instances, and counts
    #the_lab_in - the correct labels of the data
    def grid_search_func(self, param_grid, the_mode_in, the_vec_in, the_lab_in):
        grid_search = GridSearchCV(the_mode_in, param_grid=param_grid, cv=5)
        best_model = grid_search.fit(the_vec_in, the_lab_in)
        max_score = grid_search.best_score_
        best_params = grid_search.best_params_
        
        return best_model, max_score, best_params
    
    #Function to predict input data and output predicted and actual values
    #data_in - the test data
    def fetch_prediction(self, text, tfidf_in, pca_in, model_in):
        
        #Transform each test text using the TFIDF object we fitted with the test data above
        #Each test text will be judged based on the term frequency and inverse document frequencies of all the training text
        tfidf_text = tfidf_in.transform([text]).toarray()
        
        #Transform the vector of the test text, already transformed into a TFIDF vector of words as features,
        #using the PCA object we made earlier. The test text will be transformed to vary along our principal components.
        pca_text = pca_in.transform(tfidf_text)
        
        #Predict the probability of the test text being classified as one of the classes ('neg' or 'pos')
        prob_prediction = model_in.predict_proba(pca_text)[0]
        
        #Predict which class is more likely for our test text
        predicted_val = model_in.predict(pca_text)[0]
            
        #return the predicted probability and predicted value
        return prob_prediction, predicted_val