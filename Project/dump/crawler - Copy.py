# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 13:05:36 2019

@author: pathouli
"""

class crawler(object):

    def my_scraper(self, url):
        from bs4 import BeautifulSoup
        import requests
        import re
        tmp_text = ''
        try:
			#Get content from the URL
            content = requests.get(url)
			
			#Parse content as a html file (which it is)
            soup = BeautifulSoup(content.text, 'html.parser')
			
			#Find stuff between <p>
            tmp_text = soup.findAll('p') 
			
            tmp_text = [word.text for word in tmp_text]
            tmp_text = ' '.join(tmp_text)
			
			#Keep the article itself. Removed line that gets rid of numbers and punctuation.
            tmp_text = re.sub('xa0', ' ', tmp_text)
            #tmp_text = re.sub(r'\w*\d\w*', '', tmp_text).strip()
        except:
            pass
    
        return tmp_text
    
    def fetch_urls(self, query, cnt):
        #now lets use the following function that returns
        #URLs from an arbitrary regex crawl form google
    
        import requests
        from fake_useragent import UserAgent
        from bs4 import BeautifulSoup
        import re 

		#Define user agent object
        ua = UserAgent()
    
		#Make Google URL
        google_url = "https://www.google.com/search?q=" + query + "&num=" + str(cnt)
		
		#Get the structure of the google search result page and parse it
        response = requests.get(google_url, {"User-Agent": ua.random})
        soup = BeautifulSoup(response.text, "html.parser")
    
		#Find our websites
        result_div = soup.find_all('div', attrs = {'class': 'ZINbbc'})
		
		#List objects to store website info
        links = []
        titles = []
        descriptions = []
		
		#For loop to include only search links that are present
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
				
		#List objects of stuff to store clean links and remove bad link titles and descriptions
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
        for x in to_remove:
            del titles[x]
            del descriptions[x]
            
        return clean_links
 
    def write_crawl_results(self, my_query, the_cnt_in):
        #let use fetch_urls to get URLs then pass to the my_scraper function 
        import re
        import pandas as pd
        from nltk.stem import PorterStemmer, WordNetLemmatizer 
        from nltk import word_tokenize
        
        my_stemmer = PorterStemmer()
        my_lemma = WordNetLemmatizer()
        
        the_data_tmp = pd.DataFrame()
        for tmp_query in my_query:
            tmp_topic = re.sub('[ ]+', '_', tmp_query)
            the_urls_list = self.fetch_urls(tmp_query, the_cnt_in)
            for tmp_urls in the_urls_list:
                tmp_body = self.my_scraper(tmp_urls)
                if len(tmp_body) != 0:
                    tmp_body_lemma = [my_lemma.lemmatize(word) for word in word_tokenize(tmp_body)] #my_lemma.lemmatize(word_tokenize(tmp_body))
                    tmp_body_lemma = ' '.join(tmp_body_lemma)
                    tmp_body_stem = [my_stemmer.stem(word) for word in word_tokenize(tmp_body)]
                    tmp_body_stem = ' '.join(tmp_body_stem)
                    #tmp_body_stem = my_stemmer.stem(tmp_body)
                    
                    the_data_tmp = the_data_tmp.append(
                            {'label': tmp_topic,
                             'basic': tmp_body,
                             'lemmatised': tmp_body_lemma,
                             'stemmed': tmp_body_stem}, ignore_index=True)
        return the_data_tmp