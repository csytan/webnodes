from django.utils import simplejson
import urllib2
from google.appengine.api import urlfetch
#link = "http://www.reddit.com/r/technology/comments/7b1iz/amazon_launches_frustrationfree_packaging/.json"
link = "http://www.reddit.com/r/WTF/comments/7b1pj/welcome_to_the_excuse_me/.json"
link = "http://www.reddit.com/r/funny/comments/7b38f/the_uss_enterprise_totally_looks_like_a_sink/.json"
#link="http://www.reddit.com/r/funny/comments/7b30l/roger_ebert_receives_email_that_proves_the_theory/.json"
link = "http://www.reddit.com/r/politics/comments/7b2t9/virginia_board_of_elections_secretary_nancy/.json"
#link = "http://www.reddit.com/r/programming/comments/7hzgs/my_encounter_with_larry_page_through_a_piece_of/.json"


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

