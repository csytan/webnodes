import urllib
from datetime import datetime
from django.utils import simplejson



def topics():
    json = urllib.urlopen('http://www.reddit.com/r/programming/.json').read()
    data = simplejson.loads(json)
    topics = [topic['data'] for topic in data['data']['children']]
    
    for topic in topics:
        topic['updated'] = datetime.fromtimestamp(float(topic['created']))
        ups = topic['ups'] if topic['ups'] else 0
        downs = topic['downs'] if topic['downs'] else 0
        topic['points'] = ups - downs
    return topics
 
def topic(id):
    json = urllib.urlopen('http://reddit.com/comments/' + \
        id + '/.json').read()
    nodes = simplejson.loads(json)
    
    comments = []
    graph = {}
    root = []
    
    def process(node):
        if not node: return
        
        data = node['data']
        kind = node['kind']
        
        if kind == 't3':
            # root comment
            comments.append(data)
            data['id'] = data['name']
            data['body'] = data['url']
            ups = data['ups'] if data['ups'] else 0
            downs = data['downs'] if data['downs'] else 0
            data['points'] = ups - downs
            data['updated'] = datetime.fromtimestamp(float(data['created']))
            
            root.append(data)
        elif kind == 't1':
            # normal comment
            comments.append(data)
            data['id'] = data['name']
            ups = data['ups'] if data['ups'] else 0
            downs = data['downs'] if data['downs'] else 0
            data['points'] = ups - downs
            data['updated'] = datetime.fromtimestamp(float(data['created']))
            
            p_children = graph.setdefault(data['parent_id'], [])
            p_children.append(data['name'])
            process(data['replies'])
        elif kind == 'Listing':
            for node in data['children']:
                process(node)
    
    for node in nodes:
        process(node)
        
    return {
        'graph': simplejson.dumps(graph),
        'comments': comments,
        'topic': root[0]
    }

