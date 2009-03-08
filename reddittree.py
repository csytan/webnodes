from django.utils import simplejson
import urllib2
from google.appengine.api import urlfetch

link = "http://www.reddit.com/r/programming/comments/7yruv/so_i_told_my_wife_i_do_have_a_social_life_i_share/.json"
link = "http://www.reddit.com/r/reddit.com/comments/82uj2/for_all_of_reddits_antiestablishment_posturing/.json"
#txt = urllib2.urlopen(link).read()
txt = urlfetch.fetch(link).content

root = simplejson.loads(txt)[1]

comments = []
graph = {}

def process(root):
    data = root["data"]
    comment = {
        "id": data.get("id", "root"),
        "content": data.get("body", "i am root"),
        "author": data.get("author", "rooooot")
    }
    
    comments.append(comment)
    
    try:
        replies = data["replies"]["data"]["children"]
    except (KeyError, TypeError):
        try:
            replies = data["children"]
        except KeyError:
            return
    
    if not replies:
        return
        
    graph[comment["id"]] = [reply["data"]["id"] for reply in replies]
        
    for reply in replies:
        process(reply)

process(root)

graph = simplejson.dumps(graph)

