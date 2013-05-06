from datetime import datetime

from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import Http404, HttpResponse
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import date_based, list_detail
from django.conf import settings
from django.db.models import Q, Count # http://stackoverflow.com/a/1217911/412329

# from misc.json_encode import json_response
from itwishlist.apps.blog.models import Post, Vote, IS_DRAFT, IS_PUBLIC, EVERYTHING, EAT, SLEEP, SOCIALIZE, EXERCISE, ART#, SHOP, WORK
from itwishlist.apps.profiles.models import Profile
from itwishlist.apps.blog.forms import PostForm
from itwishlist.apps.blog.signals import post_published

from voting.models import Vote
from voting.managers import VoteManager

# homepage
from django.views.generic.date_based import archive_index
from django.views.generic.list_detail import object_list

def blog_post_detail(request, *kargs, **kwargs):
    blog = get_object_or_404(Blog, slug = kwargs.pop('blog', ''))
    kwargs['template_object_name'] = 'post'
    kwargs['queryset'] = Post.objects.filter(blog = blog)
    if request.user.is_authenticated():
        kwargs['queryset'] = kwargs['queryset'].filter(author=request.user) | kwargs['queryset'].filter(status=IS_PUBLIC)
    else:
        kwargs['queryset'] = kwargs['queryset'].filter(status=IS_PUBLIC)
    return list_detail.object_detail(request, *kargs, **kwargs)

def blog_user_post_detail(request, *kargs, **kwargs):
    user = get_object_or_404(User, username=kwargs.pop('username', ''))
    # =todo: show vote on post detail page
    # vote = get_object_or_404(Vote, int(0))
    if user==request.user:
        kwargs['queryset'] = kwargs['queryset'].filter(author=request.user)
    else:
        kwargs['queryset'] = kwargs['queryset'].filter(author=user, status=IS_PUBLIC)
    return list_detail.object_detail(request, *kargs, **kwargs)

@login_required
def desk(request, *kargs, **kwargs):
    # kwargs['queryset'] = Post.objects.filter(author = request.user).exclude(status = IS_DELETED)
    kwargs['queryset'] = Post.objects.filter(author = request.user)
    return list_detail.object_list(request, *kargs, **kwargs)

@login_required
def change_status(request, action, id):
    post = get_object_or_404(Post, pk = id)
    if post.author != request.user:
        request.user.message_set.create(message="You can't change statuses of posts that aren't yours")
    else:
        if action == 'draft' and post.status == IS_PUBLIC:
            post.status = IS_DRAFT
        if action == 'public' and post.status == IS_DRAFT:
            post.status = IS_PUBLIC
            post_published.send(sender=Post, post=post)
        post.save()
        request.user.message_set.create(message=_("Successfully change status for post '%s'") % post.title)
    return redirect("desk")

@login_required
def add(request, form_class=PostForm, template_name="blog/post_add.html"):
    u = request.GET.get('u', '')
    t = request.GET.get('t', '')
    post_form = form_class(request)
    if request.method == "POST" and post_form.is_valid():
        post = post_form.save(commit=False)
        post.author = request.user
        # creator_ip = request.META.get('HTTP_X_FORWARDED_FOR', None)
        # if not creator_ip:
            # creator_ip = request.META.get('REMOTE_ADDR', None)
        # post.creator_ip = creator_ip
        post.save()
        request.user.message_set.create(message=_("Successfully created post '%s'") % post.title)
        return redirect("blog_user_post_detail", username=request.user.username, slug=post.slug)
    return render_to_response(template_name, {"post_form": post_form, "u": u, "t": t}, context_instance=RequestContext(request))

@login_required
def edit(request, id, form_class=PostForm, template_name="blog/post_edit.html"):
    post = get_object_or_404(Post, id=id)
    if post.author != request.user:
        request.user.message_set.create(message="You can't edit posts that aren't yours")
        return redirect("desk")
    post_form = form_class(request, instance=post)
    if request.method == "POST" and post_form.is_valid():
        post = post_form.save(commit=False)
        post.updated_at = datetime.now()
        post.save()
        request.user.message_set.create(message=_("Successfully updated post '%s'") % post.title)
        return redirect("blog_user_post_detail", username=request.user.username, slug=post.slug)
    return render_to_response(template_name, {"post_form": post_form, "post": post}, context_instance=RequestContext(request))

# delete entry
from django.views.generic.create_update import delete_object
@login_required
def delete(request, id):
    """Delete a post based on id"""

    return delete_object(request,
        model=Post,
        object_id=id,
        template_object_name='post', # so I can write {{ note.title }} in templates/notes/delete.html (otherwise I would need to write {{ object.title }})
        template_name='blog/post_delete.html',
        post_delete_redirect=reverse("desk")
    )

# =todo: export all posts to plain text in markdown format
# https://docs.djangoproject.com/en/1.0/topics/generic-views/#performing-extra-work
@login_required
def backup(request):
    """ export all posts to plain text in markdown format """
    return object_list(request,
        queryset = Post.objects.all(),
        # mimetype = "text/plain",
        template_object_name='post',
        template_name = "blog/backup.txt"
    )
    # response["Content-Disposition"] = "attachment; filename=MyitwishlistPosts.txt"
    # return response
# @login_required
# def backup(request, *kargs, **kwargs):
#     user = get_object_or_404(User, username = kwargs.pop('username', ''))
#     kwargs['queryset'] = kwargs['queryset'].filter(author=user)
#     kwargs['extra_context'] = {'current_user': user, 'author': user}
#     return list_detail.object_list(request, *kargs, **kwargs)

# https://docs.djangoproject.com/en/1.0/topics/generic-views/#adding-extra-context
def get_profiles():
    return Profile.objects.all()

from django.shortcuts import render_to_response
from django.db.models import Q
def search(request):
    """ search """    
    query = request.GET.get('q', '') # both /search/ and /search/?q=query work
    results = []
    player_results = []
    user = request.user # http://stackoverflow.com/a/4338108/412329 - passing the user variable into the context

    if query:
        # INSTEAD OF THIS:
        # title_results = Post.objects.filter(title__icontains=query)
        # results = Post.objects.filter(content_html__icontains=query)
        # DO THIS avoid duplicate results when query word is both in title and content_html:
        # http://stackoverflow.com/questions/744424/django-models-how-to-filter-out-duplicate-values-by-pk-after-the-fact
        # results = Post.objects.filter(Q(title__icontains=query)|Q(content_html__icontains=query)).distinct()

        # https://groups.google.com/forum/?fromgroups=#!msg/django-users/JKhf05HOezg/klz7A-vs_U0J
        results = Post.objects.filter(Q(title__icontains=query)|Q(content_html__icontains=query)).distinct().filter(status=IS_PUBLIC)
        player_results = Profile.objects.filter(Q(name__icontains=query)).distinct()
    return render_to_response('search.html',
            {   'query': query, 
                'results': results,
                'user': user,
                'player_results': player_results
                # 'profile': get_profiles
            },
            context_instance=RequestContext(request)) # http://stackoverflow.com/questions/8625601/yourlabs-subscription-error-caught-variabledoesnotexist-while-rendering

@login_required
def following(request): 
    """Show following posts"""   
    return object_list(request, 
        queryset=Post.objects.all().filter(status=IS_PUBLIC),
        template_name='following.html',
        template_object_name='post',
        extra_context= {'author': request.user}
    )

@login_required
def followers(request): 
    """Show following posts"""   
    return object_list(request, 
        queryset=Post.objects.all().filter(status=IS_PUBLIC),
        template_name='followers.html',
        template_object_name='post',
        extra_context= {'author': request.user}
    )

# http://stackoverflow.com/a/2807393/412329
# def homepage(request):
#     post_list = Post.objects.all().order_by('-popularity')[:300]
#     # post_list = Post.objects.select_related().annotate(votes=Count('rank')).order_by('-created_at')[:300]
#     # for post in post_list:
#     #     delta_in_hours = (int(datetime.now().strftime("%s")) - int(post.created_at.strftime("%s"))) / 3600
#     #     post.popularity = ((post.rank - 1) / (delta_in_hours + 2)**1.5)

#     # post_list = sorted(post_list, key=lambda x: x.popularity, reverse=True)

#     # posts = paginate(request, post_list, 5)

#     return render_to_response('homepage.html',
#                 {   'profile': get_profiles,
#                     'post_list': post_list,
#                     # 'post': post,
#                     'user': request.user,
#                 },
#                 context_instance=RequestContext(request)) # http://stackoverflow.com/questions/8625601/yourlabs-subscription-error-caught-variabledoesnotexist-while-rendering

def homepage(request): 
    """Show top posts"""   

    return object_list(request, 
        # http://eflorenzano.com/blog/2008/05/24/managers-and-voting-and-subqueries-oh-my/
        queryset=Post.hot.most_loved().filter(status=IS_PUBLIC)[:300], # .annotate(num_votes=Count('score')) 
        # queryset=Post.objects().filter(status=IS_PUBLIC).order_by('-popularity'), # .annotate(num_votes=Count('score')) 
        template_name='homepage.html',
        template_object_name='post',
        extra_context= {'profile': get_profiles}
    )

def new(request): 
    """Show new posts"""
    return object_list(request, 
        queryset=Post.objects.filter(status=IS_PUBLIC).order_by('-created_at')[:300], 
        template_name='new.html',
        template_object_name='post',
        extra_context= {"profile": get_profiles}
    )

def user_post_list(request, *kargs, **kwargs):
    user = get_object_or_404(User, username = kwargs.pop('username', ''))
    kwargs['queryset'] = kwargs['queryset'].filter(author=user)
    kwargs['extra_context'] = {'current_user': user, 'author': user, 'profile': get_profiles}
    return list_detail.object_list(request, *kargs, **kwargs)


# def get_category():
#     category = 
#     return category
    # except Post.DoesNotExist:
    #     raise Http404
    # return category

# =todo: These should probably be a Categories model, but need to move on in the simplest possible way for now
def feature(request): 
    """Features"""
    return object_list(request, 
        # Display Eat OR Everything
        # queryset=Post.hot.most_loved().filter(Q(category=EAT)|Q(category=EVERYTHING))[:300], 
        queryset=Post.hot.most_loved().filter(status=IS_PUBLIC, kind='F').order_by('-created_at')[:300], 
        template_name='new.html',
        template_object_name='post',
        extra_context= {"profile": get_profiles}
    )
    
def bug(request): 
    """Bugs"""
    return object_list(request, 
        # Display Eat OR Everything
        # queryset=Post.hot.most_loved().filter(Q(category=EAT)|Q(category=EVERYTHING))[:300], 
        queryset=Post.hot.most_loved().filter(status=IS_PUBLIC, kind='B').order_by('-created_at')[:300], 
        template_name='new.html',
        template_object_name='post',
        extra_context= {"profile": get_profiles}
    )
    
def eat(request): 
    """Eat category"""
    return object_list(request, 
        # Display Eat OR Everything
        # queryset=Post.hot.most_loved().filter(Q(category=EAT)|Q(category=EVERYTHING))[:300], 
        queryset=Post.hot.most_loved().filter(category=EAT)[:300], 
        template_name='category-eat.html',
        template_object_name='post',
        extra_context= {"profile": get_profiles}
    )

def sleep(request): 
    """Sleep category"""
    return object_list(request, 
        queryset=Post.hot.most_loved().filter(category=SLEEP)[:300], 
        template_name='category-sleep.html',
        template_object_name='post',
        extra_context= {"profile": get_profiles}
    )

def socialize(request): 
    """Socialize category"""
    return object_list(request, 
        queryset=Post.hot.most_loved().filter(category=SOCIALIZE)[:300], 
        template_name='category-socialize.html',
        template_object_name='post',
        extra_context= {"profile": get_profiles}
    )

def exercise(request): 
    """excercise category"""
    return object_list(request, 
        queryset=Post.hot.most_loved().filter(category=EXERCISE)[:300], 
        template_name='category-exercise.html',
        template_object_name='post',
        extra_context= {"profile": get_profiles}
    )

def art(request): 
    """art category"""
    return object_list(request, 
        queryset=Post.hot.most_loved().filter(category=ART)[:300], 
        template_name='category-art.html',
        template_object_name='post',
        extra_context= {"profile": get_profiles}
    )

# def shop(request): 
#     """shop category"""
#     return object_list(request, 
#         queryset=Post.hot.most_loved().filter(category=SHOP)[:300], 
#         template_name='category-shop.html',
#         template_object_name='post',
#         extra_context= {"profile": get_profiles}
#     )

# def work(request): 
#     """work category"""
#     return object_list(request, 
#         queryset=Post.hot.most_loved().filter(category=WORK)[:300], 
#         template_name='category-work.html',
#         template_object_name='post',
#         extra_context= {"profile": get_profiles}
#     )


# http://stackoverflow.com/a/2167434/412329
from django.http import HttpResponseRedirect
from django.contrib.comments import Comment
from django.contrib.auth.models import User

def comment_posted(request):
    if request.GET['c']:
        comment_id = request.GET['c'] #B
        comment = Comment.objects.get( pk=comment_id )
        # name = request.user
        post = Post.objects.get(id=comment.object_pk) #C
        if post:
            return HttpResponseRedirect( post.get_absolute_url() ) #D
    return HttpResponseRedirect( "/" )