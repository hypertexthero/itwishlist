from datetime import datetime
from django.template.defaultfilters import slugify
from BeautifulSoup import BeautifulSoup

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from voting.models import Vote
from voting.managers import VoteManager

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

import markdown
from typogrify.templatetags.typogrify_tags import typogrify

# defining html sanitizer to subsequently use in content_markdown to content_html conversion of user content at post save
# http://code.google.com/p/html5lib/wiki/UserDocumentation
# http://djangosnippets.org/snippets/2444/
# http://michelf.ca/blog/2010/markdown-and-xss/
import html5lib
from html5lib import sanitizer
def sanitize(value):
    p = html5lib.HTMLParser(tokenizer=sanitizer.HTMLSanitizer)
    return p.parseFragment(value).toxml()

IS_DRAFT = 1
IS_PUBLIC = 2
IN_PROGRESS = 3
DONE = 4

STATUS_CHOICES = (
    (IS_DRAFT, _("Draft (does not appear on wishlist)")), 
    (IS_PUBLIC, _("Pending")),
    (IN_PROGRESS, _("In Progress")),
    (DONE, _("Done")),
)

# WAIT = 5
# 
# CATEGORY_CHOICES = (
#     (WAIT, _("Wait")), 
# )

KIND = (
    ('B', 'Bug Report'),
    ('F', 'Feature Request'),
    # ('A', 'Action Request'),
)

# =todo: would be nicer to do the SQL calculation below in Python like the following, but alas, can't get it to work on separate Vote table together with Post table. Tried it in views.py, too:

# loved = score
# for post in loved:
#     delta_in_hours = (int(datetime.now().strftime("%s")) - int(post.created_at.strftime("%s"))) / 3600
#     post.popularity = ((score - 1) / (delta_in_hours + 2)**1.5)
# loved = sorted(loved, key=lambda x: x.popularity, reverse=True)
# return loved

# - http://amix.dk/blog/post/19574
# - http://stackoverflow.com/questions/3783892/implementing-the-hacker-news-ranking-algorithm-in-sql
# - http://stackoverflow.com/questions/1965341/implementing-a-popularity-algorithm-in-django
# - http://stackoverflow.com/questions/1964395/complex-ordering-in-django
# - http://stackoverflow.com/questions/12545840/hacker-news-algorithm-for-django-voting-sort-order
# - http://stackoverflow.com/questions/1964544/timestamp-difference-in-hours-for-postgresql
# - http://eflorenzano.com/blog/2008/05/24/managers-and-voting-and-subqueries-oh-my/

# from django.db.models import Count # http://stackoverflow.com/a/1217911/412329
# Manager methods are intended to do "table-wide" things
class VoteAwareManager(models.Manager):
    """ Get recent top voted items (hacker news ranking algorythm, without the -1 for now since it breaks the calculation as all scores return 0.0)
        (p - 1) / (t + 2)^1.5
        where p = points and t = age in hours
    """
    def _get_score_annotation(self):
        model_type = ContentType.objects.get_for_model(self.model)
        table_name = self.model._meta.db_table

        return self.extra(select={

            # =todo: try to do the calculation in python again using F() expressions: https://docs.djangoproject.com/en/dev/topics/db/queries/#filters-can-reference-fields-on-the-model

            # MANY USERS - once lots and lots of items are available (-1 vote to negate user's own vote):
            # http://stackoverflow.com/questions/1964544/timestamp-difference-in-hours-for-postgresql
            # needed COALESCE(...,0) so that items with no votes get a score of 0.0 instead of NULL and don't go first on the list
            # 'score': 'SELECT COALESCE(SUM(vote / ((EXTRACT(EPOCH FROM current_timestamp - created_at)/3600)+2)^1.5),0) FROM %s WHERE content_type_id=%d AND object_id=%s.id' % (Vote._meta.db_table, int(model_type.id), table_name)
            
            # FEW USERS - once many items are available
            # http://stackoverflow.com/questions/1964544/timestamp-difference-in-hours-for-postgresql
            # 'score': 'SELECT COALESCE(SUM( vote / ((EXTRACT(EPOCH FROM current_timestamp - created_at)/3600)+2)^1.5)) FROM %s WHERE content_type_id=%d AND object_id=%s.id' % (Vote._meta.db_table, int(model_type.id), table_name)

            # LAUNCH (almost no users) - use in beginning when there are few items
            'score': 'SELECT COALESCE(SUM(vote),0) FROM %s WHERE content_type_id=%d AND object_id=%s.id' % (Vote._meta.db_table, int(model_type.id), table_name)
            })

    def most_loved(self):        
        # post_list = self._get_score_annotation().order_by('-score')[:300]
        # # post_list = Post.objects.select_related().annotate(votes=Count('rank')).order_by('-created_at')[:300]
        # for post in post_list:
        #     delta_in_hours = (int(datetime.now().strftime("%s")) - int(post.created_at.strftime("%s"))) / 3600
        #     post.popularity = ((post.vote - 1) / (delta_in_hours + 2)**1.5)

        # post_list = sorted(post_list, key=lambda x: x.popularity, reverse=True)

        # return post_list
        return self._get_score_annotation().order_by('-score',)

    def most_hated(self):
        return self._get_score_annotation().order_by('score')
        # return self._get_score_annotation().order_by('score', 'created_at')

class Post(models.Model):
    """Post model"""
    title = models.CharField(_("Title"), max_length=500, blank=False)
    slug = models.SlugField(_("URL Slug"), max_length=500, blank=True)
    author = models.ForeignKey(User, related_name="added_posts")
    # creator_ip = models.CharField(_("IP Address of the Post Creator"), max_length=255, blank=True, null=True)
    kind = models.CharField(max_length=1, choices=KIND, default=1)
    url = models.URLField(_("Bug URL"), blank=True, null=True, help_text="Not required, but helpful if relevant. With or without http://", default='')
    content_markdown = models.TextField(_("Description"), blank=True, help_text="<a data-toggle='modal' href='#markdownhelp'>Markdown syntax</a>.")
    content_html = models.TextField(blank=True, null=True, editable=False)
    status = models.IntegerField(_("Status"), choices=STATUS_CHOICES, default=IS_PUBLIC)
    # responsible = models.ForeignKey(User, verbose_name=_("Responsible"), related_name="assigned_tickets", blank=True, null=True)
    allow_comments = models.BooleanField(_("Allow Comments?"), blank=False, default=1)
    publish = models.DateTimeField(_("Date Published"), default=datetime.now)
    created_at = models.DateTimeField(_("Date Created"), default=datetime.now)
    updated_at = models.DateTimeField(_("Last Updated"))

    # Categorization.
    # category = models.IntegerField(_("category"), choices=CATEGORY_CHOICES, default=WAIT)

    # Get top votes
    objects = models.Manager()
    hot = VoteAwareManager()

    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')

    def __unicode__(self):
        return self.title

    # def get_category(self):
    #     return self.category

    # model methods should act on a particular model instance
    @models.permalink
    def get_absolute_url(self):
        return ('blog_user_post_detail', None, {
            'username': self.author.username,
            'slug': self.slug,
        })

    def save(self, force_insert=False, force_update=False, update_date=True):
        # http://www.freewisdom.org/projects/python-markdown/Extra
        self.content_html = sanitize(typogrify(markdown.markdown(self.content_markdown, ["extra", "footnotes", "tables", "nl2br", "codehilite"])))
        
        if update_date:
            self.updated_at = datetime.now()
            self.slug = '%s' % (slugify(self.title))
        # if (self.slug == None or self.slug == ''):
        if not self.id:
            super(Post, self).save(force_insert, force_update)
        self.slug = '%d-%s' % (self.id, slugify(self.title))

        super(Post, self).save(force_insert, force_update)

    def is_public(self):
        return self.status == IS_PUBLIC
    
    def get_owners(self):
        return [self.author]

    # =todo: next/prev links
    # def get_next(self):
    #     next = Post.objects.filter(id__gt=self.id)
    #     if next:
    #         return next[0]
    #     return False
      
    # def get_prev(self):
    #     prev = Post.objects.filters(id__lt=self.id)
    #     if prev:
    #         return prev[0]
    #     return False

# Notifications when users comment
# http://stackoverflow.com/questions/8603469/how-to-use-django-notification-to-inform-a-user-when-somebody-comments-on-their
from django.contrib.sites.models import Site
from django.db.models import signals
from notification import models as notification

def create_notice_types(app, created_models, verbosity, **kwargs):
    notification.create_notice_type("new_comment", "Comment posted", "A comment has been posted")

signals.post_syncdb.connect(create_notice_types, sender=notification)


# =todo: send email to responsible user if post kind is Action Request

def new_comment(sender, instance, created, **kwargs):   
    # remove this if-block if you want notifications for comment edit too
    if not created:
        return None

    context = {
        'comment': instance,
        'site': Site.objects.get_current(),
    }
    recipients = []

    # add all users who commented the same object to recipients
    for comment in instance.__class__.objects.for_model(instance.content_object):
        if comment.user not in recipients and comment.user != instance.user:
            recipients.append(comment.user)
            # content_object creator to recipients list
            recipients.append(instance.content_object.author)

    # if the commented object is a user then notify him as well
    if isinstance(instance.content_object, models.get_model('auth', 'User')):
        # if he is the one who posts the comment then don't add him to recipients
        if instance.content_object != instance.user and instance.content_object not in recipients:
            recipients.append(instance.content_object)

    notification.send(recipients, 'new_comment', context)

signals.post_save.connect(new_comment, sender=models.get_model('comments', 'Comment'))

# http://djangodays.com/2008/10/02/django-10-mail-notification-of-new-comments/

# from django.contrib.comments.models import Comment
# from django.core.mail import send_mail
# from django.db.models import signals
# 
# def mail_comment(instance, **kwargs):
#     subject = 'subject of the mail'
#     msg = 'Comment text:\n\n%s' % instance.comment
#     send_mail(subject, msg, 'noreply@it.ippc.int', ['email@address.com'])
# 
# signals.post_save.connect(mail_comment, sender=Comment)