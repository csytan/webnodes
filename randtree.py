import random
import randtext
count = 0
def rand_tree(node, depth=0):
    global count
    
    node.setdefault("replies", [])

    if depth > 200 or count > 1000: return    
    
    for x in range(0, random.randint(0, 10)):
        count += 1
        new_node = {"id":str(count), "content": randtext.chomsky(times=random.randint(1,5)),"author":None, "depth":depth+1}
        node["replies"].append(new_node)
        rand_tree(new_node, depth+1)
        
        
total = 100
def filter_comments(node, max_replies=3, depth=10):
    global total
    
    #if len(node["replies"]) > max_replies:
    #    node["next_replies"] = "asdf"#str(node["replies"][max_replies:])
        
    if total <= 0 or depth <=0:
        node["replies"] = []
    else:
        node["replies"] = node["replies"][:max_replies]
        
    total -= len(node["replies"])        
        
    for reply in node["replies"]:
        filter_comments(reply, depth=depth-1)

import simplejson


graph = {}
comments = []
def get_graph(node):
    comments.append(node)
    graph[node["id"]] = [reply["id"] for reply in node["replies"]]
    for reply in node["replies"]:
        get_graph(reply)
        

d = {"id":"root", "content":randtext.chomsky(times=random.randint(1,5))}
rand_tree(d)
filter_comments(d)
get_graph(d)
