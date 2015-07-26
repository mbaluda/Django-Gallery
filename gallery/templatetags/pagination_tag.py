import math
from django import template
from django.template import resolve_variable
from django.template import Library, Node
register = template.Library()

class Pages:
  def __init__(self, page, pages, segment):
    self.page = page + 1
    self.pages = pages
    self.left = []
    self.middle = []

    self.right = []
    self.next = None
    self.previous = None
    if self.page > 1:
        self.previous = self.page - 1
    p = int(1)

    while p < segment and p <= self.pages:
        self.left.append(p)
        p = p + 1
    if p < self.page - segment:
        p = self.page - segment

    if p > segment:
        while p < self.page + segment/2 and p <= self.pages:
            self.middle.append(int(p))
            p = p + 1
    else:

        while p < self.page + segment/2 and p <= self.pages:
            self.left.append(int(p))
            p = p + 1
    if p < self.pages - segment:
        p = self.pages - segment

    if p > self.pages - segment:
        while p < self.pages:
            self.middle.append(int(p))
            p = p + 1
    else:
        while p <= self.pages:
            self.right.append(int(p))
            p = p + 1

    if self.page < self.pages:
        self.next = self.page + 1

class PaginationNode(Node):
  def __init__(self, objects_var, page_var, step, segment, variable):

    self.objects_var = objects_var
    self.page_var = page_var
    self.step = int(step)
    self.segment = int(segment)
    self.variable = variable
  def render(self, context):

    objects = template.resolve_variable(self.objects_var, context)
    page = template.resolve_variable(self.page_var, context)
    if page is None:
        page = 1
    page = int(page) - 1
    count = objects.count()

    pages = math.ceil(float(count) / self.step)
    try:
        context[self.variable] = objects[page * self.step: (page + 1) * self.step]
        context['pagination'] = Pages(page, pages, self.segment)
    except:
        pass

    return ''

def paginate(parser, token):
    tokens = token.contents.split()
    if len(tokens) != 6:
        raise template.TemplateSyntaxError, "pagination tag takes objects, page, step, segment, and variable as arguments"
    return PaginationNode(*tokens[1:])

register.tag('paginate', paginate)