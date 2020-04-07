#Imports

#re
import re

#Import Pandas and Numpy
import numpy as np
import pandas as pd

#Web crawler
from crawler import crawler

#nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer 

#Gensim
import gensim
import gensim.corpora as corpora
import gensim.models.ldamodel as lda
from gensim.models import CoherenceModel

# Plotting tools
import pyLDAvis
import pyLDAvis.gensim
import matplotlib.pyplot as plt

#################
#DATA RETRIEVAL

#Get articles in

#Create crawler object
web_crawl = crawler()

# Define Google Search query and number of searches
google_query = ['site:longreads.com america -tag']
num_search = 1

#Call the crawler
#Store the df that is returned in a pandas dataframe
data = web_crawl.write_crawl_results(google_query, num_search)


#Col 1 - basic - Cleaned, but otherwise untouched body of text
#Col 2 - label - Query for the search query


#################
#PRE-PROCESSING - Article

def pre_processing(article):
    #Force everything to lower case
    article_lower = article.lower()
    
    ##Remove non-words
    article_clean = re.sub(r"[^\w\s\d]+", " ", article_lower)
    
    #Tokenise the article
    article_tokenise = word_tokenize(article_clean)
    
    ##Remove stopwords
    #Create a stopwords object
    stop_words = list(stopwords.words("english"))
    
    #Extending the stopwords list with "u" - somehow this even showed up in the LDA
    #I think it comes from U.S. being separated to "u" and "s"
    #Longreads and wordpress are the names of the website and blog that put out the article and
    #add no meaning
    stop_words.extend(['u', 'longreads', 'wordpress']) #Why didn't this get rid of the u?
    
    #Keep only words not in the stopwords list
    article_sans_stopwords = [each_word for each_word in article_tokenise if each_word not in stop_words]
    
    ##Lemmatise
    #Create lemmatise object
    lemmatiser = WordNetLemmatizer()
    
    #Lemmatise~~ - should try to deal with this keeping only nouns, adjectives, verbs, and adverbs?
    article_lemmatised = [lemmatiser.lemmatize(word) for word in article_sans_stopwords]
    
    #Return lemmatised article
    #return article_lower, article_clean, article_tokenise, article_sans_stopwords, article_lemmatised
    return article_lemmatised

#################
#PRE-PROCESSING - Sentences
def sentence_processing(article):
    #Sentence tokenisation
    sentences = sent_tokenize(article)
    
    #Get clean, lemmatised sentences without stopwords
    sentences_lemmatised = [pre_processing(sentence) for sentence in sentences]
    
    #Return lemmatised sentence list
    return sentences_lemmatised

#################
#COUNTING - Sentences

def sent_tfidf(article_lemmatised_sentences):
    #Import sklearn
    from sklearn.feature_extraction.text import TfidfVectorizer
    
    # Create the TFIDF Object
    tfidf_vectoriser = TfidfVectorizer()
    
    #Join sentences for the vectoriser
    sentence_list = [" ".join(sentence) for sentence in article_lemmatised_sentences]
    
    # Fit sentences to the TFIDF vectoriser
    senteces_TFIDFed = tfidf_vectoriser.fit_transform(sentence_list)
    
    # Put the TFIDF vectorised data into a pandas dataframe
    sent_df = pd.DataFrame(senteces_TFIDFed.toarray())
    
    # Rename the columns to the words in the sentences
    sent_df.columns = tfidf_vectoriser.get_feature_names()
    
    return sent_df

#################
#Sentence Word Frequencies

#2nd article    
text = data["basic"][0]

#Lemmatise sentences
sent_lemmatised = sentence_processing(text)

#TFIDF our sentences to see which has the important words
#tfidf_article_by_sent = sent_tfidf(sent_lemmatised)

#Make bigram model
#Set the thresholds low - this seems to be necessary to get sensible bigrams like
# kathleen_alcott and America_Hard (name of the book is America is Hard to Find)
bigram = gensim.models.Phrases(sent_lemmatised,
                               min_count=1,
                               threshold=1
                               )

bigram_model = gensim.models.phrases.Phraser(bigram)
#bigram_model[sent_lemmatised[0]]
bigram_sents = [bigram_model[sent] for sent in sent_lemmatised]

#################
#LDA

#Create LDA dictionary and corpus
dictionary = corpora.Dictionary(bigram_sents)
corpus = [dictionary.doc2bow(text) for text in bigram_sents]
#Btw the lists are still sentences, and the tuples are word id, and the count (within the sentence)


#Create model
lda_model = lda.LdaModel(corpus,
                         id2word = dictionary,
                         num_topics = 10
                         )
topics = lda_model.print_topics(num_words = 10)

for topics in topics:
    print(topics)


# Topic coherence
# Read the explanations from https://datascienceplus.com/evaluation-of-topic-modeling-topic-coherence/
# and https://rare-technologies.com/what-is-topic-coherence/
#But don't completely get it. What's important though, is that topic coherence gives us a quantitative measure
# of topic extraction quality from our LDA model.


#THIS DOESN'T WORK FOR SOME REASON ):
coherence_model_lda = CoherenceModel(model = lda_model,
                                     texts = bigram_sents,
                                     dictionary = dictionary,
                                     coherence='c_v'
                                     )
coherence_lda = coherence_model_lda.get_coherence()





pyLDAvis.enable_notebook()
vis = pyLDAvis.gensim.prepare(lda_model, corpus, dictionary)
vis







