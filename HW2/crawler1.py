# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 13:05:36 2019

@author: pathouli
"""

class crawler1(object):

    def my_scraper(self, tmp_url_in):
        from bs4 import BeautifulSoup
        import requests
        import re
        #url = 'http://www.qmss.columbia.edu/faculty-and-staff'
        tmp_text = ''
        try:
            content = requests.get(tmp_url_in)
            soup = BeautifulSoup(content.text, 'html.parser')
    
            tmp_text = soup.findAll('p') 
    
            tmp_text = [word.text for word in tmp_text]
            tmp_text = ' '.join(tmp_text)
            tmp_text = re.sub('\W+', ' ', re.sub('xa0', ' ', tmp_text))
            #tmp_text = re.sub('\W+', ' ', tmp_text)
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
        for x in to_remove:
            del titles[x]
            del descriptions[x]
            
        return clean_links
 
    def write_crawl_results(self, my_query, the_cnt_in):
        
        #Import needed libraries
        import pandas as pd
        from nltk.stem import PorterStemmer
        import re
        
        #Create empty data frame
        the_data = pd.DataFrame()
        #Create PorterStemmer object for stemming
        my_stemmer = PorterStemmer()
        #Label to include in data frame column
        the_label = re.sub('[\s]+', '_', my_query)
        
        #Call fetch_urls to get our list of URLs
        the_urls_list = self.fetch_urls(my_query, the_cnt_in)
        
        #For each URL in the list of URLs, get the text, process, and make an entry in our data frame
        for link in the_urls_list:
            #Get the cleaned text by calling my_scraper
            body_basic = self.my_scraper(link)
            
            #If statement to further process only websites with actual text.
            if len(body_basic) != 0:
                try:
                    #Use our PorterStemmer object to stem body_basic, and store the result in body_stem
                    body_stem = [my_stemmer.stem(one_word) for one_word in body_basic.split()]
                    #Create the dictionary to enter into our data frame
                    entry = {'label': the_label,
                             'URL': link,
                            'body_basic': body_basic,
                            'body_stem': body_stem}
                    #Enter our dictionary entry into the data frame
                    the_data = the_data.append(entry, ignore_index = True)
                except:
                    pass
            
        
        return(the_data)
        