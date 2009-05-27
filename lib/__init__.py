import os
import sys

# add lib directory to sys.path for global import
path = os.path.dirname(__file__)
sys.path.append(path)

# import modules within the directory so they are cached, since
# appengine resets sys.path between requests
for name in os.listdir(path):
    if name.endswith('.py') and '__init__' not in name:
        name = name.rstrip('.py')
    elif not os.path.isdir(os.path.join(path, name)):
        continue
    __import__(name)
