from django.utils import simplejson
import urllib


def get_thread_data(id):
    response = urllib.urlopen('http://reddit.com/comments/' + \
        id + '/.json').read()
    nodes = simplejson.loads(response)
    
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
            data['content'] = data['title'] + '<br><a href="'+ data['url'] + '">Link</a>'
            ups = data['ups'] if data['ups'] else 0
            downs = data['downs'] if data['downs'] else 0
            data['score'] = ups - downs
            
            root.append(data['name'])
        elif kind == 't1':
            # normal comment
            comments.append(data)
            data['id'] = data['name']
            data['content'] = data['body']
            ups = data['ups'] if data['ups'] else 0
            downs = data['downs'] if data['downs'] else 0
            data['score'] = ups - downs
            
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
        'root': root[0]
    }


def hot_topics():
    response = urllib.urlopen('http://www.reddit.com/.json').read()
    data = simplejson.loads(response)
    return [topic['data'] for topic in data['data']['children']]
