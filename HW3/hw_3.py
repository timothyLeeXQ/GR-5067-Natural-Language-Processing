# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 16:49:29 2019

@author: pathouli
"""

from crawler import crawler_sol
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import pandas as pd
from sklearn.model_selection import GridSearchCV

#array that contains what topics to crawl
the_query = ['positive words', 'negative words']
#number of document to crawl per topic
num_docs = 100

#initialize function
my_func = crawler_sol()

#call up crawler function and perform crawl, resultant dataframe contains 3 columns, basic wranged
#data
#the_data = my_func.fetch_crawl(None, the_query, num_docs)

#####
my_vec = CountVectorizer(ngram_range=(1, 3))

#Takes the data and fits it in a count vectorise
my_xform_vec = my_vec.fit_transform(the_data.body_basic).toarray()
col_names = my_vec.get_feature_names()
#count_list = dict(my_xform_vec.sum(axis=0)) #this gets word frequency counts into a dictionary

my_xform_vec = pd.DataFrame(my_xform_vec, columns=col_names)
#####

#####
my_vec_tfidf = TfidfVectorizer()

my_xform_tfidf = my_vec_tfidf.fit_transform(the_data.body_basic).toarray()
col_names = my_vec_tfidf.get_feature_names()

my_xform_tfidf = pd.DataFrame(my_xform_tfidf, columns=col_names)

#####
#
#clf = RandomForestClassifier(n_estimators=100, max_depth=2, random_state=0)
#
#clf.fit(my_xform_tfidf, the_data.label)  
#
#my_sample = ['i hiked in the woods and ran into a bobcat']
#test_text = my_vec_tfidf.transform(my_sample).toarray()
#
#clf.predict(test_text)

#####

from sklearn.decomposition import PCA

#Q2.1
# The iterate_var function finds the least number of components/dimensions needed to capture at least a target portion of the variance
# in the data when applying a Principal Component Analysis (PCA). The target portion of the variance one wants to capture is passed
# as the argument var_target in the function (in the call below, this is 0.95 or 95%).
# The function returns:
    # The PCA object with the number of dimensions needed to produce the model with the target variance
    # The data transformed by this model

# It does this using the following steps
# 1. Set the number of dimensions in the PCA to 1, and initialise a variable of the amount of variance captured as 0.
# 2. While the amount of variance captured is less than the target:
#       run a PCA with the given number of dimensions and transform the data to fit the new model.
# 3.    Sum the variance explained by the principal components from the model.
# 4.    Increase the number of dimensions ino the PCA by 1, and perform steps 2 and 3 again, until the amount of variance
#       captured by the model's principal components exceeds the target.
# 5. Once the number of principal components exceeds the target, return the PCA model and the data transformed by this model
    
def iterate_var(var_target):
    var_fig = 0.0
    cnt = 1
    while var_fig <= var_target:
        pca = PCA(n_components=cnt)
        my_dim = pca.fit_transform(my_xform_tfidf)
        var_fig = sum(pca.explained_variance_ratio_)   
        cnt += 1
    return my_dim, pca

my_dim, pca = iterate_var(0.95)

#Q2.2
# The grid_search function tries to find the optimal parameters for a given model given data, a classifier, and
# and a set of parameters to consider.
#. Given the arguments:
    # param_grid - A dictionary or list of dictionaries with the parameters to try in the grid search
    # the_mode_in - The model/estimator object that is being used for the analysis (below, random forest classifier)
    # the_vec_in - The training data to fit
    # the_lab_in - The classifier labels associated with the training data
# 1. The grid search goes through all the combination of parameters in param_grid for the given classifier 
#       and places them in a grid
# 2. best_model trains models using the training data and labels using all possible model parameter combinations within the grid
# 3. max_score takes the best score of all the training models, while best_params saves the parameters of the model with the
#       best score
# 4. best_model, max_score, and best_params are returned as objects.

def grid_search_func(param_grid, the_mode_in, the_vec_in, the_lab_in):
    grid_search = GridSearchCV(the_mode_in, param_grid=param_grid, cv=5)
    best_model = grid_search.fit(the_vec_in, the_lab_in)
    max_score = grid_search.best_score_
    best_params = grid_search.best_params_

    return best_model, max_score, best_params

param_grid = {"max_depth": [10, 50, 100],
              "n_estimators": [1, 4, 16, 32, 64]}

clf_pca = RandomForestClassifier()
gridsearch_model, best, opt_params = grid_search_func(
        param_grid, clf_pca, my_xform_tfidf, the_data.label)

clf_pca = RandomForestClassifier()
clf_pca.set_params(**gridsearch_model.best_params_)
clf_pca.fit(my_dim, the_data.label)

my_sample = ['The darkest hour is among us in this time of gloom, however, we will prevail!']
test_text = my_vec_tfidf.transform(my_sample).toarray()
test_text_pca = pca.transform(test_text)

the_result = pd.DataFrame(clf_pca.predict_proba(test_text_pca))
the_result.columns = clf_pca.classes_
print (the_result)


#Q2.3: -1 (of all the words, only gloom is present in the word lists, as a negative word)
# By "the function above", I presume the question is referring to Q1, not Q2, since Q2.4 effectively asks for the sentiment score of 
# the Q2 function.
#Q2.4: negative_words  positive_words
#         0.40378         0.59622

#Q2.5: negative_words  positive_words
#        0.611851        0.388149

# Including the trigrams increased the likelihood that the sample text was classified as a negative word (from about 40% to about 60%).
# This could have been because of various reasons.
# 1. Tokenising the words by trigrams may have led to more matches between the tokenised trigrams and searches with the negative words label
# less matches with searches bearing the positive words label, or both, relative to unigram matches with the google search.
# For instance, where the unigram 'hour' may not have influenced matching with either positive or negative labels before, the trigram 'the darkest hour' 
# is likely to have matched with the negative words label.
# 2. The use of trigrams created more features where words in the sample text that are likely to produce a negative words label could exert greater
# influence on the string's classification.
# For instance, where "darkest", likely to produce a negative words label, is counted only once when unigrams are used, it is counted twice
# ('the darkest hour', darkest hour is') when trigrams are counted. It is also counted once more as a unigram and twice as a bigram given the 1,3 
# ngram_range setting.
# 3. The differences in results may also have had less to do with the use of trigrams as opposed to unigrams than random variation in the model building 
# process, since no seed was set during the creation of the classifier models.
# Wide variation in classification results is a likely possibility given that the amount of label training data (from google searches, 50 per label) is very small
# for the number of features that were present in the data (after PCA, there were still more than 100 features).
# This is likely to explain the pattern of results here. While I cannot personally attest to this as I only ran the code above once, copying the output in the
# comments above, others have mentioned getting widely different values for 'the_result' when they ran a repeat analysis, suggesting high model variability that
# likely emerged from insufficient data.