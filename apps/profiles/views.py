from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

try:
    from django.views.generic import ListView, DetailView, CreateView, UpdateView
except ImportError:
    try:
        from cbv import ListView, DetailView, CreateView, UpdateView
    except ImportError:
        raise ImportError(
            "It appears you are running a version of Django < "
            "1.3. To use idios with this version of Django, install "
            "django-cbv==0.1.5."
        )

from idios.utils import get_profile_model, get_profile_base

if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification
else:
    notification = None

def group_and_bridge(kwargs):
    """
    Given kwargs from the view (with view specific keys popped) pull out the
    bridge and fetch group from database.
    """

    bridge = kwargs.pop("bridge", None)

    if bridge:
        try:
            group = bridge.get_group(**kwargs)
        except ObjectDoesNotExist:
            raise Http404
    else:
        group = None

    return group, bridge


def group_context(group, bridge):
    # @@@ use bridge
    return {
        "group": group,
    }


class SquadXMLView(DetailView):

    template_name = "profiles/squad.xml"
    context_object_name = "profile"

    def get_object(self):

        username = self.kwargs.get("username")
        profile_class = get_profile_model(self.kwargs.get("profile_slug"))

        if profile_class is None:
            raise Http404

        if username:
            self.page_user = get_object_or_404(User, username=username)
            return get_object_or_404(profile_class, user=self.page_user)
        else:
            profile = get_object_or_404(
                profile_class, pk=self.kwargs.get("profile_pk")
            )
            self.page_user = profile.user
            return profile

    def get_context_data(self, **kwargs):

        base_profile_class = get_profile_base()
        profiles = base_profile_class.objects.filter(user=self.page_user)

        group, bridge = group_and_bridge(kwargs)
        is_me = self.request.user == self.page_user

        ctx = group_context(group, bridge)
        ctx.update({
            "is_me": is_me,
            "page_user": self.page_user,
            "profiles": profiles,
        })
        ctx.update(
            super(SquadXMLView, self).get_context_data(**kwargs)
        )

        return ctx




# =todo: authenticate against drupal users db
# http://chirale.wordpress.com/2013/03/15/unified-login-in-django-and-drupal/
# from django.contrib.auth.decorators import login_required
# from django.conf import settings
# import subprocess
# 
# @login_required
# def sso(request):
#    try:
#        assert request.user.drupal_id > 0
#        # user id to log in
#        drupal_id = str(request.user.drupal_id)
#        output = ""
#        try:
#            # DRUPAL_SITE_PATH is the absolute path to Drupal installation
#            # DRUPAL_SITE_NAME is the Drupal site name, e.g. example.com
#            output = check_output(["drush", "-r", settings.DRUPAL_SITE_PATH, "-l", settings.DRUPAL_SITE_NAME, "user-login", drupal_id])
#        except CalledProcessError:
#            # @todo add additional control statement?
#            pass
#        if output:
#            # Declare DRUPAL_SITE_URL on settings.py and set it as 'www.example.com'
#            #     your Drupal site name
#            drupal_login_url = output.replace("http://ippcdrupal.dev/", "http://%s/" % settings.DRUPAL_SITE_URL).strip()
#            # set Drupal login destination using DRUPAL_LOGIN_DESTINATION
#            destination = "%s?destination=%s" % (drupal_login_url, settings.DRUPAL_LOGIN_DESTINATION)
#            return redirect(destination)
#        else:
#            # no output from the drush command
#            return HttpResponse('Wrong request')
#    except AssertionError:
#        # Drupal id is not assigned
#        return HttpResponse('Not registered user')