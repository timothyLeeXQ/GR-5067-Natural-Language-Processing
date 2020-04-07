# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 07:35:36 2019

@author: pathouli
"""

from crawler1 import crawler1

searches = ["sceptile", "virizion", "power law", "lists in r"]
results = []

for search in searches: 
    the_query = search
    num_docs = 10

    my_func = crawler1()

    search_results = my_func.write_crawl_results(the_query, num_docs)
    print(search_results)
    results.append(search_results)