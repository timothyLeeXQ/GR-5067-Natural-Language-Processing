# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 13:05:36 2019

@author: pathouli
"""

class crawler_sol(object):

    def my_scraper(self, tmp_url_in):
        from bs4 import BeautifulSoup
        import requests
        import re
        from nltk.corpus import stopwords
        sw = stopwords.words('english')
        #url = 'http://www.qmss.columbia.edu/faculty-and-staff'
        tmp_text = ''
        try:
            content = requests.get(tmp_url_in)
            soup = BeautifulSoup(content.text, 'html.parser')
    
            tmp_text = soup.findAll('p') 
    
            tmp_text = [word.text for word in tmp_text]
            tmp_text = [word for word in tmp_text if word not in sw]
            tmp_text = ' '.join(tmp_text)
            tmp_text = re.sub('\W+', ' ', re.sub('xa0', ' ', tmp_text))
            tmp_text = re.sub(r'\w*\d\w*', '', tmp_text).strip()
        except:
            pass
    
        return tmp_text
    
    def fetch_urls(self, query, cnt):
        #now lets use the following function that returns
        #URLs from an arbitrary regex crawl form google
    
        #pip install pyyaml ua-parser user-agents fake-useragent
        import requests
        from fake_useragent import UserAgent
        from bs4 import BeautifulSoup
        import re 
        ua = UserAgent()
    
        #query = 'fishing'
    
        google_url = "https://www.google.com/search?q=" + query + "&num=" + str(cnt)
        response = requests.get(google_url, {"User-Agent": ua.random})
        soup = BeautifulSoup(response.text, "html.parser")
    
        result_div = soup.find_all('div', attrs = {'class': 'ZINbbc'})
    
        links = []
        titles = []
        descriptions = []
        for r in result_div:
            # Checks if each element is present, else, raise exception
            try:
                link = r.find('a', href = True)
                title = r.find('div', attrs={'class':'vvjwJb'}).get_text()
                description = r.find('div', attrs={'class':'s3v9rd'}).get_text()
    
                # Check to make sure everything is present before appending
                if link != '' and title != '' and description != '': 
                    links.append(link['href'])
                    titles.append(title)
                    descriptions.append(description)
            # Next loop if one element is not present
            except:
                continue  
    
        to_remove = []
        clean_links = []
        for i, l in enumerate(links):
            clean = re.search('\/url\?q\=(.*)\&sa',l)
    
            # Anything that doesn't fit the above pattern will be removed
            if clean is None:
                to_remove.append(i)
                continue
            clean_links.append(clean.group(1))
    
        # Remove the corresponding titles & descriptions
#        for x in to_remove:
#            del titles[x]
#            del descriptions[x]
            
        return clean_links
 
    def fetch_crawl(self, the_path, my_query, the_cnt_in):
        #let use fetch_urls to get URLs then pass to the my_scraper function 
        #import os
        import re
        import pandas as pd
        from nltk.stem import PorterStemmer#, WordNetLemmatizer 
        from nltk import word_tokenize
        
        my_stemmer = PorterStemmer()
        #my_lemma = WordNetLemmatizer()
        
        the_data_tmp = pd.DataFrame()
        for tmp_query in my_query:
            tmp_topic = re.sub('[ ]+', '_', tmp_query)
            the_urls_list = self.fetch_urls(tmp_query, the_cnt_in)
            for tmp_urls in the_urls_list:
                tmp_body = self.my_scraper(tmp_urls)
                if len(tmp_body) != 0:
                    #tmp_body_lemma = [my_lemma.lemmatize(word) for word in word_tokenize(tmp_body)] #my_lemma.lemmatize(word_tokenize(tmp_body))
                    #tmp_body_lemma = ' '.join(tmp_body_lemma)
                    tmp_body_stem = [my_stemmer.stem(word) for word in word_tokenize(tmp_body)]
                    tmp_body_stem = ' '.join(tmp_body_stem)
                    #tmp_body_stem = my_stemmer.stem(tmp_body)
                    
                    the_data_tmp = the_data_tmp.append(
                            {'label': tmp_topic,
                             'body_basic': tmp_body,
                             #'body_lemma': tmp_body_lemma,
                             'body_stem': tmp_body_stem}, ignore_index=True)
        return the_data_tmp

    def write_crawl(self, the_path, my_query, the_cnt_in):
        import re, os

        for tmp_query in my_query:
            print (tmp_query)
            the_urls_list = self.fetch_urls(tmp_query, the_cnt_in)
            
            #the_path = 'C:/Users/pathouli/myStuff/academia/columbia/socialSciences/GR5067/lectures/l6/data/'
            cnt = 0
            for word in the_urls_list:
                try:
                    os.makedirs(the_path + re.sub('[ ]+', '_', tmp_query))
                except:
                    pass
                tmp_txt = self.my_scraper(word)
                if len(tmp_txt) != 0:
                    try:
                        tmp_file = open(the_path + re.sub('[ ]+', '_', tmp_query) + '/' + str(cnt) + '.txt',"w") 
                        tmp_file.write(tmp_txt)
                        tmp_file.close()
                        print (word)
                        cnt += 1
                    except:
                        pass