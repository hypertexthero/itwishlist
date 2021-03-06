from datetime import datetime

from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import Http404, HttpResponse
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.contrib import messages

from django.views.generic import date_based, list_detail
from django.conf import settings
from django.db.models import Q, Count # http://stackoverflow.com/a/1217911/412329

# from misc.json_encode import json_response
from itwishlist.apps.blog.models import Post, Vote, IS_DRAFT, IS_PUBLIC, DONE, IN_PROGRESS, KNOWLEDGE_BASE
from itwishlist.apps.fileupload.models import File
from itwishlist.apps.profiles.models import Profile
from itwishlist.apps.blog.forms import PostForm
from itwishlist.apps.blog.signals import post_published

# http://stackoverflow.com/a/2167434/412329
from django.http import HttpResponseRedirect
from django.contrib.comments import Comment
from django.contrib.auth.models import User

from voting.models import Vote
from voting.managers import VoteManager

from django.shortcuts import render_to_response
from django.db.models import Q

# homepage
from django.views.generic.date_based import archive_index
from django.views.generic.list_detail import object_list

# @login_required
def blog_post_detail(request, *kargs, **kwargs):
    blog = get_object_or_404(Blog, slug = kwargs.pop('blog', ''))
    kwargs['template_object_name'] = 'post'
    kwargs['queryset'] = Post.objects.filter(blog = blog)
    if request.user.is_authenticated():
        kwargs['queryset'] = kwargs['queryset'].filter(author=request.user) | kwargs['queryset'].filter(Q(status=IS_PUBLIC)|Q(status=DONE)|Q(status=IN_PROGRESS)|Q(status=KNOWLEDGE_BASE))
    else:
        kwargs['queryset'] = kwargs['queryset'].filter(Q(status=IS_PUBLIC)|Q(status=DONE)|Q(status=IN_PROGRESS)|Q(status=KNOWLEDGE_BASE))
    return list_detail.object_detail(request, *kargs, **kwargs)

# @login_required
def blog_user_post_detail(request, *kargs, **kwargs):
    user = get_object_or_404(User, username=kwargs.pop('username', ''))
    # =todo: show vote on post detail page
    # vote = get_object_or_404(Vote, int(0))
    if user==request.user:
        kwargs['queryset'] = kwargs['queryset'].filter(author=request.user)
    else:
        kwargs['queryset'] = kwargs['queryset'].filter(author=user).filter(Q(status=IS_PUBLIC)|Q(status=DONE)|Q(status=IN_PROGRESS)|Q(status=KNOWLEDGE_BASE))
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
        messages.add_message(request, messages.ERROR, message="You can't change statuses of items that aren't yours")
    else:
        if action == 'draft' and post.status in [IS_PUBLIC,IN_PROGRESS,DONE,KNOWLEDGE_BASE]:
            post.status = IS_DRAFT
        elif action == 'public' and post.status in [IS_DRAFT,IN_PROGRESS,DONE,KNOWLEDGE_BASE]:
            post.status = IS_PUBLIC
        elif action == 'inprogress' and post.status in [IS_PUBLIC,IS_DRAFT,DONE,KNOWLEDGE_BASE]:
            post.status = IN_PROGRESS
        elif action == 'done' and post.status in [IS_DRAFT,IS_PUBLIC,IN_PROGRESS,KNOWLEDGE_BASE]:
            post.status = DONE
        # elif action == 'kb' and post.status in [IS_DRAFT,IS_PUBLIC,IN_PROGRESS,DONE]:
        #     post.status = DONE
        post_published.send(sender=Post, post=post)
        post.save()
        messages.add_message(request, messages.SUCCESS, message=_("Successfully changed status for post '%s'") % post.title)
    return redirect("blog_user_post_detail", username=request.user.username, slug=post.slug)

@login_required
def add(request, form_class=PostForm, template_name="blog/post_add.html"):
    u = request.GET.get('u', '')
    t = request.GET.get('t', '')
    post_form = form_class(request)
    if request.method == "POST" and post_form.is_valid():
        post = post_form.save(commit=False)
        post.author = request.user
        post_form.save()
        post.id = post.id
        # need to call save again so notification gets sent to observers 
        # https://docs.djangoproject.com/en/dev/ref/models/instances/#saving-objects
        post_form.save()
        messages.add_message(request, messages.SUCCESS, message=_("Successfully created post '%s'") % post.title)
        return redirect("blog_user_post_detail", username=request.user.username, slug=post.slug)
    return render_to_response(template_name, {"post_form": post_form, "u": u, "t": t}, context_instance=RequestContext(request))

@login_required
def edit(request, id, form_class=PostForm, template_name="blog/post_edit.html"):
    post = get_object_or_404(Post, id=id)
    # observers = User.objects.filter(is_staff=True)
    if post.author != request.user:
        request.user.message_set.create(message="You can't edit items that aren't yours")
        return redirect("desk")
    post_form = form_class(request, instance=post)
    if request.method == "POST" and post_form.is_valid():
        post = post_form.save(commit=False)
        post.updated_at = datetime.now()
        post_form.save()
        # request.user.message_set.create(message=_("Successfully updated post '%s'") % post.title)
        # http://stackoverflow.com/a/11728475/412329
        messages.add_message(request, messages.SUCCESS, message=_("Successfully updated post '%s'") % post.title)
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

# =todo: export all items to plain text in markdown format
# https://docs.djangoproject.com/en/1.0/topics/generic-views/#performing-extra-work
@login_required
def backup(request):
    """ export all items to plain text in markdown format """
    return object_list(request,
        queryset = Post.objects.all(),
        # mimetype = "text/plain",
        template_object_name='post',
        template_name = "blog/backup.txt"
    )

# https://docs.djangoproject.com/en/1.0/topics/generic-views/#adding-extra-context
def get_profiles():
    return Profile.objects.all()

# http://stackoverflow.com/questions/744424/django-models-how-to-filter-out-duplicate-values-by-pk-after-the-fact
from itertools import chain
# =search
@login_required
def search(request):
    """ search """    
    query = request.GET.get('q', '') # both /search/ and /search/?q=query work
    post_list = []
    file_list = []
    profile_list = []
    comment_list = []
    result_list = list(chain(post_list, file_list, profile_list, comment_list))
    user = request.user # http://stackoverflow.com/a/4338108/412329 - passing the user variable into the context

    if query:
        # https://groups.google.com/forum/?fromgroups=#!msg/django-users/JKhf05HOezg/klz7A-vs_U0J
        post_list = Post.objects.filter(Q(
            title__icontains=query)|Q(content_html__icontains=query)).distinct().filter(Q(
            status=IS_PUBLIC)|Q(status=DONE)|Q(status=IN_PROGRESS)|Q(status=KNOWLEDGE_BASE))
        file_list = File.objects.filter(Q(slug__icontains=query)).distinct()
        profile_list = Profile.objects.filter(Q(name__icontains=query)).distinct()
        comment_list = Comment.objects.filter(Q(comment__icontains=query)).distinct()
        result_list = sorted(
            chain(post_list, file_list, profile_list, comment_list),
            key=lambda instance: instance)
            # key=lambda instance: instance.pub_date)
    return render_to_response('search.html',
            {   'query': query, 
                'user': user,
                'post_results': post_list,
                'file_results': file_list,
                'profile_results': profile_list,
                'comment_results': comment_list,
            },
            context_instance=RequestContext(request)) # http://stackoverflow.com/questions/8625601/yourlabs-subscription-error-caught-variabledoesnotexist-while-rendering

@login_required
def following(request): 
    """Show following items"""   
    return object_list(request, 
        queryset=Post.objects.all().filter(Q(status=IS_PUBLIC)|Q(status=IN_PROGRESS)|Q(status=KNOWLEDGE_BASE)),
        template_name='following.html',
        template_object_name='post',
        extra_context= {'author': request.user}
    )

@login_required
def followers(request): 
    """Show followers items"""   
    return object_list(request, 
        queryset=Post.objects.all().filter(Q(status=IS_PUBLIC)|Q(status=IN_PROGRESS)|Q(status=KNOWLEDGE_BASE)),
        template_name='followers.html',
        template_object_name='post',
        extra_context= {'author': request.user}
    )

@login_required
def homepage(request): 
    """Show top items"""   

    return object_list(request, 
        # http://eflorenzano.com/blog/2008/05/24/managers-and-voting-and-subqueries-oh-my/
        queryset=Post.hot.most_loved().filter(Q(status=IS_PUBLIC)|Q(status=IN_PROGRESS)|Q(status=KNOWLEDGE_BASE))[:300], # .annotate(num_votes=Count('score')) 
        # queryset=Post.objects().filter(status=IS_PUBLIC).order_by('-popularity'), # .annotate(num_votes=Count('score')) 
        template_name='homepage.html',
        template_object_name='post',
        extra_context= {'profile': get_profiles}
    )

@login_required
def new(request): 
    """Show new items"""
    return object_list(request, 
        queryset=Post.objects.filter(Q(status=IS_PUBLIC)|Q(status=IN_PROGRESS)|Q(status=KNOWLEDGE_BASE)).order_by('-created_at')[:300], 
        template_name='new.html',
        template_object_name='post',
        extra_context= {"profile": get_profiles}
    )

@login_required
def user_post_list(request, *kargs, **kwargs):
    user = get_object_or_404(User, username = kwargs.pop('username', ''))
    kwargs['queryset'] = kwargs['queryset'].filter(author=user)
    kwargs['extra_context'] = {'current_user': user, 'author': user, 'profile': get_profiles}
    return list_detail.object_list(request, *kargs, **kwargs)

@login_required
def feature(request): 
    """Features"""
    return object_list(request, 
        queryset=Post.hot.most_loved().filter(Q(status=IS_PUBLIC)|Q(status=IN_PROGRESS), kind='F').order_by('-created_at')[:300], 
        template_name='feature.html',
        template_object_name='post',
        extra_context= {"profile": get_profiles}
    )
    
@login_required
def bug(request): 
    """Bugs"""
    return object_list(request, 
        queryset=Post.hot.most_loved().filter(Q(status=IS_PUBLIC)|Q(status=IN_PROGRESS), kind='B').order_by('-created_at')[:300], 
        template_name='bug.html',
        template_object_name='post',
        extra_context= {"profile": get_profiles}
    )
    
@login_required
def done(request): 
    """Done - Stuff that's been finished"""
    return object_list(request, 
        queryset=Post.hot.most_loved().filter(status=DONE).order_by('-updated_at')[:300], 
        template_name='done.html',
        template_object_name='post',
        extra_context= {"profile": get_profiles}
    )

@login_required
def inprogress(request): 
    """In Progress - Stuff that's in progress"""
    return object_list(request, 
        queryset=Post.hot.most_loved().filter(status=IN_PROGRESS).order_by('-updated_at')[:300], 
        template_name='inprogress.html',
        template_object_name='post',
        extra_context= {"profile": get_profiles}
    )

@login_required
def kb(request): 
    """Show IT Knowledge Base items"""
    return object_list(request, 
        queryset=Post.objects.filter(Q(status=KNOWLEDGE_BASE), kind='K').order_by('-created_at')[:300], 
        template_name='kb.html',
        template_object_name='post',
        extra_context= {"profile": get_profiles}
    )

# http://stackoverflow.com/a/2167434/412329
def comment_posted(request):
    if request.GET['c']:
        comment_id = request.GET['c'] #B
        comment = Comment.objects.get( pk=comment_id )
        # name = request.user
        post = Post.objects.get(id=comment.object_pk) #C
        if post:
            return HttpResponseRedirect( post.get_absolute_url() ) #D
    return HttpResponseRedirect( "/" )