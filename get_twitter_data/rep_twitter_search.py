import re
import json

from get_twitter_data.standard_twitter_search import twitter_search

def get_twitter_handles(rep_twitter_file):
    '''
    '''
    reps_twitter_handles = {}
    with open(rep_twitter_file) as input:
        for line in input:
            r = re.search(r"(.+?(?=@))@([\w.]+)", line)
            name, twitter_handle = r.groups()
            if twitter_handle not in reps_twitter_handles:
                reps_twitter_handles[twitter_handle] = [name.strip()]
            else:
                reps_twitter_handles[twitter_handle].append(name.strip())
    return reps_twitter_handles

def update_reps_dict(tweet_json, reps_name, rep_handle, reps_dict):
    '''
    '''
    rep = reps_name[0]
    if len(reps_name) != 1:  # n.b. doc gives some general twitter accounts for multiple people
        rep = rep_handle

    if rep not in reps_dict:
        reps_dict[rep] = {'twitter_handle': rep_handle,
                                'tweets': {}}
    tweet = {}
    tweet_id = tweet_json['id']
    if tweet_id not in reps_dict[rep]['tweets']:
        tweet['text'] = tweet_json['full_text']
        tweet['url'] = 'https://twitter.com/{}/status/{}'\
                        .format(tweet_json['user']['screen_name'], tweet_id)
        reps_dict[rep]['tweets'][tweet_id] = tweet

def search_rep_twitter_data(reps_json_file='./data/reps.json'):
    '''
    '''
    reps_dict = {}

    reps_twitter_dict = get_twitter_handles('./data/illinois_reps_twitter_handles.txt')
    reps_twitter = reps_twitter_dict.keys()

    if limit:
        reps_twitter = reps_twitter[:limit]

    for i, rep_twitter in enumerate(reps_twitter):
        tweets_json = twitter_search(rep_twitter, i, 'users')
        if print_to_screen:
            return tweets_json
        if not tweets_json:
            break

        rep_names = reps_twitter_dict[rep_twitter]

        if tweets_json['statuses']:
            for t in tweets_json['statuses']:
                update_reps_dict(t, rep_names, rep_twitter, reps_dict)

    with open(reps_json_file, 'w') as output_file:
        json.dump(reps_dict, output_file)
