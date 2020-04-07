#Define list
list_of_articles = []

#Append lemmatised sentences to the list
for text in data["basic"]:
    #Lemmatise article
    #lower, clean, tokenised, wo_stopwords, lemmatised = pre_processing(text)
    lemmatised = pre_processing(text)     
    list_of_articles.append(lemmatised)



#################
#BIGRAMS

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