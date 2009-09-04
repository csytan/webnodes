###############################################################################
# Recurse template tag for Django v1.1
# Copyright (C) 2008 Lucas Murray
# http://www.undefinedfire.com
#
# http://www.undefinedfire.com/lab/recursion-django-templates/
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
###############################################################################
 
from django import template
 
register = template.Library()
 
class RecurseNode(template.Node):
    def __init__(self, var, name, child, nodeList):
        self.var = var
        self.name = name
        self.child = child
        self.nodeList = nodeList
 
    def __repr__(self):
        return '<RecurseNode>'
 
    def renderCallback(self, context, vals, level):
        output = []
        try:
            if len(vals):
                pass
        except:
            vals = [vals]
        if len(vals):
            if 'loop' in self.nodeList:
                output.append(self.nodeList['loop'].render(context))
            for val in vals:
                context.push()
                context['level'] = level
                context[self.name] = val
                if 'child' in self.nodeList:
                    output.append(self.nodeList['child'].render(context))
                    child = self.child.resolve(context)
                    if child:
                        output.append(self.renderCallback(context, child, level + 1))
                if 'endloop' in self.nodeList:
                    output.append(self.nodeList['endloop'].render(context))
                else:
                    output.append(self.nodeList['endrecurse'].render(context))
                context.pop()
            if 'endloop' in self.nodeList:
                output.append(self.nodeList['endrecurse'].render(context))
        return ''.join(output)
 
    def render(self, context):
        vals = self.var.resolve(context)
        output = self.renderCallback(context, vals, 1)
        return output
 
def do_recurse(parser, token):
    bits = list(token.split_contents())
    if len(bits) != 6 and bits[2] != 'with' and bits[4] != 'as':
        raise template.TemplateSyntaxError, "Invalid tag syxtax expected '{% recurse [childVar] with [parents] as [parent] %}'"
    child = parser.compile_filter(bits[1])
    var = parser.compile_filter(bits[3])
    name = bits[5]
 
    nodeList = {}
    while len(nodeList) < 4:
        temp = parser.parse(('child','loop','endloop','endrecurse'))
        tag = parser.tokens[0].contents
        nodeList[tag] = temp
        parser.delete_first_token()
        if tag == 'endrecurse':
            break
 
    return RecurseNode(var, name, child, nodeList)
do_recurse = register.tag('recurse', do_recurse)