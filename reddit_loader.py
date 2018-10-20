import urllib3
import json
import io

# link = 'https://www.reddit.com/r/copypasta/new.json?limit=100'
link = 'https://api.pushshift.io/reddit/search/submission/?subreddit=copypasta&size=1000&sort_type=num_comments'

http = urllib3.PoolManager()
r = http.request('GET', link)
data = json.loads(r.data)['data']

with io.open('texts/reddit.txt', 'w', encoding='utf8') as f:
    for post in data:
        if 'selftext' in post:
            f.write(post['selftext'])
