# -*- coding: utf-8 -*-
"""
Created on Sat Nov  9 21:41:12 2019

@author: Timothy
"""

import re

#Open the file
open_file = open('psalms.txt', 'r')

#Read the file
all_psalms = open_file.read()

open_file.close()

#Pre-pre-processing
#This deals with the whole string object
#We want to remove some repetitive elements that are common and will skew our analysis, specific to the book of psalms

#Remove "Chief Musician", "stringed instruments", "A Psalm of David."
all_psalms_wo_preface = re.sub("The Book of Psalms|Book I+|Chief Musician|stringed instruments|A .+ of David",
                               " ",
                               all_psalms,
                               flags=re.IGNORECASE)

#Split the large string by Psalm
each_psalm = re.split("Psalm \\d+", all_psalms_wo_preface)