#Imports

#re
import re

#pandas
import pandas as pd

#Web crawler
from crawler import crawler

#nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

#sklearn
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer



#################
#DATA RETRIEVAL

#Get articles in

#Create crawler object
web_crawl = crawler()

# Define Google Search query and number of searches
google_query = ['site:medium.com life']
num_search = 10

#Call the crawler
#Store the df that is returned in a pandas dataframe
data = web_crawl.write_crawl_results(google_query, num_search)


#Col 1 - basic - Cleaned, but otherwise untouched body of text
#Col 2 - lemmatised - Lemmatised text
#Col 3 - stemmed - Stemmed text
#Col 4 - label - Query for the search query

#################
#PRE-PROCESSING

#Force everything to lower case in new columns of the DF
data["lower"] = data["basic"].map(lambda x: x.lower())
#data["lem_lower"] = data["lemmatised"].map(lambda x: x.lower())
#data["stem_lower"] = data["stemmed"].map(lambda x: x.lower())

#Create a stopwords object
stop_words = list(stopwords.words("english"))


#################
#WORD TOKENISATION

#Get rid of punctuation
data["wo_punct"] = data["lower"].map(lambda x: re.sub("[^\w\s\d]+", " ", x))

#Tokenise
data["words"] = data["wo_punct"].map(lambda x: word_tokenize(x))

#Get rid of stopwords
data["stopless_words"] = data["words"].map(lambda x: [word for word in x if word not in stop_words])

#################
#SENTENCE TOKENISATION

#Create tokeniser column in our data frame
data["sentences"] = data["lower"].map(lambda x: sent_tokenize(x))

#Get rid of punctuation
data["wo_punct_sent"] = data["sentences"].map(lambda x: [re.sub("[^\w\s\d]+", " ", sentence) for sentence in x])

#Get rid of stopwords in sentences, while preserving each sentence in its own list
wo_stopword_sent_entry = []
for article in data["wo_punct_sent"]:
    article_entry = []
    for sentence in article:
        tokenized_sent = word_tokenize(sentence)
        sent_entry = [word for word in tokenized_sent if word not in stop_words]
        article_entry.append(sent_entry)
    wo_stopword_sent_entry.append(article_entry)

data["wo_stopword_sent"] = wo_stopword_sent_entry

#################
#WORD VECTORISATION