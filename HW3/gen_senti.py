# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 12:54:21 2019

@author: Timothy
"""

def gen_senti(text):
    
    #Imports
    import os
    from nltk.tokenize import word_tokenize
    
    #Set working directory to read in files
    original_directory = os.getcwd()
    word_list_directory = 'C:/Users/Timothy/Google Drive/TC Stuff/Analytics/GR 5067 - Natural Language Processing in Social Sciences/HW3'
    os.chdir(word_list_directory)
    
    #Read in files and store them as objects
    #Positive words
    pos_words_file = open("positive-words.txt", "r")
    pos_words_file = pos_words_file.read()
        #Negative words
    neg_words_file = open("negative-words.txt", "r")
    neg_words_file = neg_words_file.read()
    
    
    # Tokenize the text files to get a list of individual words
    pw = word_tokenize(pos_words_file)
    nw = word_tokenize(neg_words_file)
    
    #Go back to the original WD
    os.chdir(original_directory)
    
    
    #Define sentiment counter and total counted words
    sent_counter = 0
    total_counter = 0
    
    #Force input text to lower case
    text.lower()
    
    #Tokenise the text input
    text_token = word_tokenize(text)
    for word in text_token:
        if word in pw:
            sent_counter += 1
            total_counter += 1
        elif word in nw:
            sent_counter -= 1
            total_counter += 1
        else:
            continue
    
    #Normalise the score based on the total number of words in the list
    S = sent_counter / total_counter
    
    return(S)
    
x = gen_senti("The darkest hour is among us in this time of gloom, however, we will prevail!")

