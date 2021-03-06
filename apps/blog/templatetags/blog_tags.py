# -*- coding: utf-8 -*-
import re

from django import template
from django.conf import settings
from django.template import Variable
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.template import RequestContext

# http://www.b-list.org/weblog/2006/jun/07/django-tips-write-better-template-tags/
from django.template import Library, Node
from django.db.models import get_model

from itwishlist.apps.blog.models import Post, IS_DRAFT, IS_PUBLIC, IN_PROGRESS, DONE, KNOWLEDGE_BASE

register = template.Library()

# http://www.b-list.org/weblog/2006/jun/07/django-tips-write-better-template-tags/
class LatestCommentsNode(Node):
    """ 
    Usage:
    {% get_latest comments.Comment 5 as recent_comments %}
    
    Needed to customize this for comments submit_date for now.
    See below for the normal one to be used for all site content.
    
    """
    def __init__(self, model, num, varname):
        self.num, self.varname = num, varname
        self.model = get_model(*model.split('.'))

    def render(self, context):
        # context[self.varname] = self.model._default_manager.all()[:self.num]
        context[self.varname] = self.model._default_manager.order_by('-submit_date')[:self.num]
        return ''

def get_latest_comments(parser, token):
    bits = token.contents.split()
    if len(bits) != 5:
        raise TemplateSyntaxError, "get_latest tag takes exactly four arguments"
    if bits[3] != 'as':
        raise TemplateSyntaxError, "third argument to get_latest tag must be 'as'"
    return LatestCommentsNode(bits[1], bits[2], bits[4])

get_latest_comments = register.tag(get_latest_comments)





class LatestContentNode(Node):
    """
    Template tag, which lets us fetch any number of objects 
    from any installed model and store them in any 
    context variable we want. 
     
    Call it like this:

    {% get_latest ApplicationName.ModelName 5 as some_variable_name %}

    Eg1:

    {% get_latest weblog.Entry 10 as latest_entries %}
    
    """
    def __init__(self, model, num, varname):
        self.num, self.varname = num, varname
        self.model = get_model(*model.split('.'))
    
    def render(self, context):
        context[self.varname] = self.model._default_manager.all()[:self.num]
        return ''
 
def get_latest(parser, token):
    bits = token.contents.split()
    if len(bits) != 5:
        raise TemplateSyntaxError, "get_latest tag takes exactly four arguments"
    if bits[3] != 'as':
        raise TemplateSyntaxError, "third argument to get_latest tag must be 'as'"
    return LatestContentNode(bits[1], bits[2], bits[4])
    
get_latest = register.tag(get_latest)



# from django.contrib.flatpages.models import FlatPage
# @register.simple_tag
# def get_page(title, attr):
#     # page = richtext_filter(get_object_translation(getattr(RichTextPage.objects.get(pk=int(pk)), attr)))
#     page = FlatPage.objects.get(title=title)
#     if 'enabled' in page.title:
#         return page.content
#     else:
#         return ''






@register.tag
def check_post_status(parser, token):
    bits = token.contents.split(' ')
    return CheckPostStatus(bits[1], bits[2])

class CheckPostStatus(template.Node):
    def __init__(self, user, post):
        self.user = user
        self.post = post

    def render(self, context):
        user = Variable(self.user).resolve(context)
        post = Variable(self.post).resolve(context)
        if not user or not post:
            return ''
        if post.author == user or post.status == IS_PUBLIC or post.status == IN_PROGRESS or post.status == DONE or post.status == KNOWLEDGE_BASE:
            context['show_post'] = True
        else:
            context['show_post'] = False
        return ''

@register.inclusion_tag("blog/post_item.html", takes_context = True)
def show_blog_post(context, post):
    context['post'] = post
    context['post_undetailed'] = True
    return context

@register.inclusion_tag("blog/post_item.html", takes_context = True)
def show_full_blog_post(context, post):
    context['post'] = post
    context['post_undetailed'] = False
    return context


@register.simple_tag
def active(request, pattern):
    if re.search(pattern, request.path):
        return ' class="active"'
    return ''

# http://stackoverflow.com/a/9250304
@register.filter
def tabindex(value, index):
    """
    Add a tabindex attribute to the widget for a bound field.
    """
    value.field.widget.attrs['tabindex'] = index
    return value


# http://stackoverflow.com/questions/203859/how-do-i-get-python-markdown-to-additionally-urlify-links-when-formatting-plai
urlfinder = re.compile("""(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))""")
@register.filter('urlify_markdown')
def urlify_markdown(value):
    return urlfinder.sub(r'<a href="\1">\1</a>', value)

@register.filter
def rootdomain(value):
    """
    Get root domain of a link
    """
    # return re.match(value.split())
    value = re.search("(?<=\/\/)(.*?)(?=\/)", value)
    if value:
        # return "value.group() : ", value.group()
        return value.group(1)
    else:
        return ""
    # url = value
    # value = url
    # value = urlparse.urlparse(url).value.split(".")
    # value = ".".join(len(value[-2]) < 4 and value[-3:] or value[-2:])



# http://djangosnippets.org/snippets/178/
class RomanError(Exception): pass
class OutOfRangeError(RomanError): pass
class NotIntegerError(RomanError): pass

ROMAN_NUMBER_MAP = (('M',  1000),
                    ('CM', 900),
                    ('D',  500),
                    ('CD', 400),
                    ('C',  100),
                    ('XC', 90),
                    ('L',  50),
                    ('XL', 40),
                    ('X',  10),
                    ('IX', 9),
                    ('V',  5),
                    ('IV', 4),
                    ('I',  1))

@register.filter
def to_roman(n):
    """convert integer to Roman numeral"""
    if not isinstance(n, int):
        try:
            n = int(n)
        except ValueError:
            raise NotIntegerError, "non-integers cannot be converted"
    
    if not (0 < n < 4000):
        raise OutOfRangeError, "number out of range (must be 1..3999)"

    result = ""
    for numeral, integer in ROMAN_NUMBER_MAP:
        while n >= integer:
            result += numeral
            n -= integer
    return result

@register.filter
def roman_number(value):
    """
    Converts a number to its roman value

    Example usage::
        {{ 2007|roman_number }}
        {{ "2007"|roman_number }}
        {{ pub_date|date:"Y"|roman_number }}
    """
    try:
        value = to_roman(value)
    except RomanError, e:
        raise TemplateSyntaxError, "roman_number error: %s" % str(e)
    return value

# http://djangosnippets.org/snippets/2019/
# from django.db.models.loading import get_model
# from django.db.models.query import QuerySet
# 
# @register.filter
# def call_manager(model_or_obj, method):
#     # load up the model if we were given a string
#     if isinstance(model_or_obj, basestring):
#         model_or_obj = get_model(*model_or_obj.split('.'))
# 
#     # figure out the manager to query
#     if isinstance(model_or_obj, QuerySet):
#         manager = model_or_obj
#         model_or_obj = model_or_obj.model
#     else:
#         manager = model_or_obj._default_manager
# 
#     return getattr(manager, method)()