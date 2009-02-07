import random
count = 0
def rand_tree(node, depth=0):
    global count
    
    node.setdefault("replies", [])

    if depth > 900 or count > 2000: return    
    
    for x in range(0, random.randint(0, 5)):
        count += 1
        new_node = {"content": "text "* 10,"depth": depth+1}
        node["replies"].append(new_node)
        rand_tree(new_node, depth+1)
        
d = {}

rand_tree(d)

    
#import pickle
#print d
#p = pickle.dumps(d)
#d = pickle.loads(p)