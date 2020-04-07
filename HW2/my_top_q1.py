# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 07:35:36 2019

@author: pathouli
"""

from crawler import crawler

my_path = 'C:/Users/Timothy/Google Drive/TC Stuff/Analytics/GR 5067 - Natural Language Processing in Social Sciences/HW2/files_q1'
the_query = 'qmss columbia'
num_docs = 50

my_func = crawler()

my_func.write_crawl_results(my_path, the_query, num_docs)