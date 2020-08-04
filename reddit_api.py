# -*- coding: utf-8 -*-
"""
Created on Fri Dec 21 00:05:33 2018

@author: ivan.sheng
"""

#! python3
import praw
import pandas as pd
import datetime
import os
import pickle
#from praw.models import MoreComments

path = 'C:/Users/ivan.sheng/Downloads/' #path for export
os.chdir(path)

reddit = praw.Reddit(client_id='VaUjLSLZnGKnsQ',
                     client_secret='VGonfWF3BKVr0g3IzyYFXvTzDdA',
                     user_agent='reddit-explorer',
                     username='PM_ME_COSPLAY_BUTT', #fill in username
                     password='devil1202') #fill in password

def get_submission_date(submission):
    time = submission.created
    return datetime.date.fromtimestamp(time)

subs = ['Thritis']
#keywords = ['arthritis']


#keywords = ['Diet',
#            'Gluten-free',
#            'Digestive suppliment',
#            'Fiber',
#            'Digestive enzymes',
#            'probiotics',
#            'Kefir',
#            'Castor Oil',
#            'Prunes',
#            'Magnesium citrate',
#            'FODMAP',
#            'Senna Tea',
#            'Apple Cider Vinegar',
#            'Peppermint Tea',
#
#            "IBS",
#            "IBD",
#            "Crohn's disease",
#            "coeliac ",
#            "Leaky Gut ",
#            "Eating Disorder",
#            
#            "indigestion",
#            "nausea",
#            "belly cramps",
#            "belly pain",
#            "bloating",
#            "distention",
#            "flatulence",
#            "bleching",
#            "gasy",
#            "constipation",
#            "hard stools",
#            "Irregular bowel movements ",
#            "vomit",
#            "Hemorrhoids",
#            "Blood in stool ",
#            "trouble sleeping",
#            "back pain",
#            "loss of appetite",
#            "fatigue",
#            "dizziness",
#            "anxiety"]

topics_dict = { "title":[], \
                "score":[], \
                "id":[], \
                "url":[], \
                "comms_num": [], \
                "created": [], \
                "body":[], \
                "sub":[], \
                "date": []}

count =0
for s in subs:
    subreddit = reddit.subreddit(s)
    for submission in subreddit.top('all',limit=1000):
        if submission.selftext == '':
            continue
        else:
            topics_dict["title"].append(submission.title)
            topics_dict["score"].append(submission.score)
            topics_dict["id"].append(submission.id)
            topics_dict["url"].append(submission.url)
            topics_dict["comms_num"].append(submission.num_comments)
            topics_dict["created"].append(submission.created)
            topics_dict["body"].append(submission.selftext)
            topics_dict["sub"].append(submission.subreddit.display_name)
            topics_dict["date"].append(get_submission_date(submission))
                
#count =0
#for s in subs:
#    subreddit = reddit.subreddit(s)
#    print(s)
#    for word in keywords:
#        print(word)
#        for submission in subreddit.search(word, limit = None):
#            if submission.selftext == '':
#                continue
#            else:
#                topics_dict["title"].append(submission.title)
#                topics_dict["score"].append(submission.score)
#                topics_dict["id"].append(submission.id)
#                topics_dict["url"].append(submission.url)
#                topics_dict["comms_num"].append(submission.num_comments)
#                topics_dict["created"].append(submission.created)
#                topics_dict["body"].append(submission.selftext)
#                topics_dict["sub"].append(submission.subreddit.display_name)
#                topics_dict["date"].append(get_submission_date(submission))
#                topics_dict["keyword"].append(word)

topics_data = pd.DataFrame(topics_dict)
topics_data.drop_duplicates(subset = ['title'], keep='first', inplace=True)
pickle.dump( topics_data, open( "topical.p", "wb" ))
#topics_data.to_csv('smallbiz-pub.csv', index=False)

##comments too
#comments_dict = { "title":[], \
#                "score":[], \
#                "id":[], "url":[], \
#                "comms_num": [], \
#                "created": [], \
#                "body":[], \
#                "comment":[], \
#                "sub":[], \
#                "date": []}
#                
#count =0
#for s in subs:
#    subreddit = reddit.subreddit(s)
#    print(s)
#    for word in keywords:
#        print(word)
#        for submission in subreddit.search(word,limit=100):
#            submission.comments.replace_more(limit=1)
#            for comment in submission.comments:
#                comments_dict["title"].append(submission.title)
#                comments_dict["score"].append(submission.score)
#                comments_dict["id"].append(submission.id)
#                comments_dict["url"].append(submission.url)
#                comments_dict["comms_num"].append(submission.num_comments)
#                comments_dict["created"].append(submission.created)
#                comments_dict["body"].append(submission.selftext)
#                comments_dict["comment"].append(comment.body)
#                comments_dict["sub"].append(submission.subreddit.display_name)
#                comments_dict["date"].append(get_submission_date(submission))

##
# =============================================================================
# 
# df = pd.DataFrame(pd.read_excel(r'C:\Users\ivan.sheng\Downloads\ibuprofen-askDocs.xlsx'))
# keywords = df.Terms.tolist()
# 

#for submission in reddit.subreddit('askDocs').search(keywords):
#    date = get_submission_date(submission)
#    title = submission.title
#    text = submission.selftext
#    sub = submission.subreddit.display_name
#    sub_author = submission.author
#    url = submission.url
#    submission.comments.replace_more(limit=None)
#    for comment in submission.comments.list():
#        comment_body = comment.body
#        comment_author = comment.author
#        data = {"keyword": i,
#                "submission_url": url,
#                "date": date,
#                "title": title,
#                "submission_text": text,
#                "submission_author": sub_author,
#                "comment": comment_body,
#                "comment_author": comment_author,
#                "subreddit": sub}
#    results.append(data)

# df = pd.DataFrame(results)
# df.to_csv('askdoc.csv', index=False)
# print(df.head())
# 
# 
# =============================================================================