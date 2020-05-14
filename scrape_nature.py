#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 14 14:57:18 2020

@author: ivan.sheng
"""

from urllib.request import Request, urlopen # requests library, sends the HTTP request to the site's server to return the HTML page source
from bs4 import BeautifulSoup # library to parse HTML documents
import re # regex, a way to search for patterns in strings
import pandas as pd # data wrangling and manipulation
import os

path = 'C:/Users/ivan.sheng/Downloads/'
os.chdir(path)

def pagination(): # the army forums site adds "index + number" to its URLs to denote pages 2, 3, 4 etc of the forum
    url_list = [] # list to contain all the page number'd URLs
    for i in range(1, 6, 1):
        url = "https://sustainabilitycommunity.nature.com/channels/1385?page=" + str(i) + ".html" # the URL "recipe" for the site
        url_list.append(url)  # put all the URLs into the list bucket above
    return url_list # the product of this function is url_list, that means wherever we see "pagination()" in the code, it run "pagination()" and returns the url_list object

def getDates(pageURL): # fix this cuz right now the article has too many dates - run it on the page instead of the article
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(pageURL,headers=hdr)
    html = urlopen(req) # urllib requests library opens each forum post URL and assigns it to variable "html"
    bs = BeautifulSoup(html, 'html.parser') # BeautifulSoup parses the HTML content using "html.parser"
    date = bs.find('div', class_='meta__date') # BeautifulSoup finds all the "a" tags that contain "href links"
    dates.append(date.text) # then add it to the list of pages we want to scrape

def getLinks(pageURL): # this is the function to get all the forum post links off of each page
    pages = [] # container to hold the forum post page URLs
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(pageURL,headers=hdr)
    html = urlopen(req) # urllib requests library opens each forum post URL and assigns it to variable "html"
    bs = BeautifulSoup(html, 'html.parser') # BeautifulSoup parses the HTML content using "html.parser"
    for link in bs.find_all('a', class_='content-card__poster', href=re.compile('1385')):
        if 'href' in link.attrs: # just a check to ensure the href link is within the tag
            if link.attrs['href'] not in pages: # if this particular link isn't already in the pages list (we already got it)
                pages.append('https://sustainabilitycommunity.nature.com' + link.attrs['href']) # then add it to the list of pages we want to scrape
    return pages # the product of this function is "pages," the list of content-bearing forum links we want to travel to and scrape (as opposed to home page etc)

def scrape(url): # this is the scraping part
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(url,headers=hdr)
    html = urlopen(req) # go to the URL specified in the for loop below in "main"
    bs = BeautifulSoup(html, 'html.parser') # BeautifulSoup parses the HTML
    for idx, post in enumerate(bs.find_all('div', class_='article__content')):
   # for idx, post in enumerate(bs.find_all('p', class_='p1')): # for all the div tags BeautifulSoup finds with "content" class
        item = {'post': post.text} # make a dictionary called item, with "post" as the key and the post text as the values
        results.append(item) # append the dictionary to the results list

## main

results = [] # this is the list of dictionaries of forum content that we will gather through scraping
dates = []
for url in pagination(): # for each forum page number (runs the pagination function above)
    for page in (getLinks(url)): # for each forum post link that we get by running getLinks on each forum page number link
        print(page)
        try: 
            scrape(page) # scrape all the comments from that page
            getDates(page)
        except:
            item = {'post': 'ERROR 404'} 
            results.append(item)

df_sustain = pd.DataFrame(results) # put the results list of post content dictionaries into a pandas dataframe
dates = pd.DataFrame(dates, columns = ['Date'])
combine_sustain = pd.concat([df_sustain, dates], axis=1)
out = pd.ExcelWriter('sustain_results.xlsx')
combine_sustain.to_excel(out,'Data')
out.save()
