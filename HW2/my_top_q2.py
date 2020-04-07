# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 07:35:36 2019

@author: pathouli
"""

from crawler import crawler

my_path = 'C:/Users/Timothy/Google Drive/TC Stuff/Analytics/GR 5067 - Natural Language Processing in Social Sciences/HW2/files_q1'

searches = ["sceptile", "virizion", "power law", "lists in r"]

for search in searches:

    the_query = search
    num_docs = 10
    
    my_func = crawler()
    
    my_func.write_crawl_results(my_path, the_query, num_docs)