#!/usr/bin/python3

"""search post function"""

import json
import operator
import requests

def count_words(subreddit, word_list, after=None, counts=None):
    if counts is None:
        counts = {}
    
    if not word_list:
        print_counts(counts)
        return
    
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {"User-Agent": "Mozilla/5.0"}
    params = {"after": after} if after else {}
    
    response = requests.get(url, headers=headers, params=params, allow_redirects=False)
    if response.status_code != 200:
        print_counts(counts)
        return
    
    data = response.json()
    children = data["data"]["children"]
    for child in children:
        title = child["data"]["title"].lower()
        count_keywords(title, word_list, counts)
    
    after = data["data"]["after"]
    if after:
        count_words(subreddit, word_list, after, counts)
    else:
        print_counts(counts)


def count_keywords(title, word_list, counts):
    words = title.split()
    for word in words:
        word = word.strip('.,!?_')
        if word.lower() in word_list:
            counts[word.lower()] = counts.get(word.lower(), 0) + 1


def print_counts(counts):
    sorted_counts = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
    for word, count in sorted_counts:
        print(f"{word}: {count}")
