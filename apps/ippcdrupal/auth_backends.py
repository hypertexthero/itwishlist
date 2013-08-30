# =todo: authenticate against drupal users db
# Looks like we'll need to upgrade to Django 1.4...

from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.models import User, check_password
from itwishlist.apps.ippcdrupal.models import DrupalUsers
# from itwishlist.apps.ippcdrupal.hashers import is_password_usable, get_hasher
# =todo: upgrade to django 1.4
# from django.contrib.auth.hashers import is_password_usable, get_hasher
from django.utils.encoding import smart_str

# http://stackoverflow.com/questions/16482531/django-registration-custom-backend

# class DrupalUserAuthBackend(object):
#    """
#    Authenticates against django.contrib.auth.models.User. with my modifications
#    """
#    supports_inactive_user = True
# 
#    """
#    This function does not upgrade the user password hasher
#    """
#    def check_password(self, password, encoded):
#        if not password or not is_password_usable(encoded): 
#        # is_password_usable is only available in Django 1.4
#        # https://docs.djangoproject.com/en/1.4/topics/auth/#django.contrib.auth.hashers.is_password_usable
#        # if not password:
#            return False
# 
#        password = smart_str(password)
#        encoded = smart_str(encoded)
#        
#        if encoded[0] == "$":
#            encoded = encoded[1:] # make it compatible so that drupal 7 sha512 hasher can work properly
#        
#        if len(encoded) == 32 and '$' not in encoded:
#            hasher = get_hasher('unsalted_md5')
#        else:
#            algorithm = encoded.split('$', 1)[0]          
#            hasher = get_hasher(algorithm)
# 
#        is_correct = hasher.verify(password, encoded)
# 
#        return is_correct
# 
#    def authenticate(self, username=None, password=None, db=None, **kwargs):
#        try:
#            user = DrupalUsers.objects.using(db).get(name=username) # name in ippcdrupal.models.DrupalUsers
#            if self.check_password(password, user.pass_field):
#                return user
#        except DrupalUsers.DoesNotExist:
#            return None
           

# # http://query7.com/django-authentication-backends
# http://djangosnippets.org/snippets/2729/
# from account.models import Account
# from itwishlist.apps.ippcdrupal.drupalhasher.DrupalPasswordHasher import verify
# from django.contrib.auth.models import User
# 
# class DrupalUserAuthBackend(object):
# 
#    def authenticate(self, username, password):
# 
#        try:
#            account = DrupalUsers.objects.using('drupaldb').get(username=username, sha_pass_hash=verify(username, password))
# 
#            try:
#                user = User.objects.get(username=username)
# 
#            except User.DoesNotExist:
# 
#                user = User(username=account.username)
#                user.is_staff = False
#                user.is_superuser = False
#                user.set_unusable_password()
#                user.save()
# 
#            return user
# 
#        except Account.DoesNotExist:
# 
#            return None
# 
#    def get_user(self, id):
#        try:
#            return User.objects.get(id=id)
#        except User.DoesNotExist:
#            return None

class DrupalUserAuthBackend:
    """
    Authenticate against the settings ADMIN_LOGIN and ADMIN_PASSWORD.

    Use the login name, and a hash of the password. For example:

    ADMIN_LOGIN = 'admin'
    ADMIN_PASSWORD = 'sha1$4e987$afbcf42e21bd417fb71db8c66b321e9fc33051de'
    """

    supports_object_permissions = False
    supports_anonymous_user = False
    supports_inactive_user = False

    def authenticate(self, username=None, password=None):
        # login_valid = (settings.ADMIN_LOGIN == username)
        # pwd_valid = check_password(password, settings.ADMIN_PASSWORD)
        # if login_valid and pwd_valid:
        try:
            user = DrupalUsers.objects.using('drupaldb').get(name=username)
        except DrupalUsers.DoesNotExist:
            # Create a new user. Note that we can set password
            # to anything, because it won't be checked; the password
            # from settings.py will.
            # user = User(username=username, password='test')
            # user.is_staff = False
            # user.is_active = False
            # user.is_superuser = False
            # user.save()
            return None
    # return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


# class DrupalUserAuthBackend(object):
#     """
#     Authenticates against ippcdrupal.models.DrupalUsers
#     """
#     
#     def authenticate(self, username=None, password=None, **kwargs):
#         # UserModel = get_user_model()
#         # if username is None:
#         #     username = kwargs.get(UserModel.USERNAME_FIELD)
#         try:
#             user = DrupalUsers.objects.using('drupaldb').get(name=username) # name in ippcdrupal.models.DrupalUsers
#             # if check_password(password):
#             if check_password(password):
#                 return user
#         except DrupalUsers.DoesNotExist:
#             return None

# class SettingsBackend(object):
#     """
#     Authenticate against the settings ADMIN_LOGIN and ADMIN_PASSWORD.
# 
#     Use the login name, and a hash of the password. For example:
# 
#     ADMIN_LOGIN = 'admin'
#     ADMIN_PASSWORD = 'sha1$4e987$afbcf42e21bd417fb71db8c66b321e9fc33051de'
#     """
# 
#     def DrupalUserAuth(self, username=None, password=None, db=None, **kwargs):
#         login_valid = (settings.ADMIN_LOGIN == username)
#         pwd_valid = check_password(password, settings.ADMIN_PASSWORD)
#         if login_valid and pwd_valid:
#             try:
#                 user = User.objects.using(db).get(username=name)
#                 if user.check_password(password):
#                     return user
#             #     user = User.objects.get(username=username)
#             # except User.DoesNotExist:
#             #     # Create a new user. Note that we can set password
#             #     # to anything, because it won't be checked; the password
#             #     # from settings.py will.
#             #     user = User(username=username, password='get from settings.py')
#             #     user.is_staff = True
#             #     user.is_superuser = True
#             #     user.save()
#             return user
#         return None
# 
#     def get_user(self, user_id):
#         try:
#             return User.objects.get(pk=user_id)
#         except User.DoesNotExist:
#             return None
# 
# from __future__ import unicode_literals
# from django.contrib.auth import get_user_model
# from django.contrib.auth.models import Permission
#  
# class DrupalUserAuth(object):
#     """
#     Authenticates against django.contrib.auth.models.User.
#     """
#  
#     def authenticate(self, username=None, password=None, db=None, **kwargs):
#         UserModel = get_user_model()
#         if username is None:
#             username = kwargs.get(UserModel.USERNAME_FIELD)
#         try:
#             user = UserModel.objects.using(db).get(username=username)
#             if user.check_password(password):
#                 return user
#         except UserModel.DoesNotExist:
#             return None

# from __future__ import unicode_literals
# from django.contrib.auth import get_user_model
# from django.contrib.auth.models import Permission
#  
# class DrupalUserAuth(object):
#     """
#     Authenticates against django.contrib.auth.models.User.
#     """
#  
#     def authenticate(self, username=None, password=None, db=None, **kwargs):
#         UserModel = get_user_model()
#         if username is None:
#             username = kwargs.get(UserModel.USERNAME_FIELD)
#         try:
#             user = UserModel.objects.using(db).get(username=username)
#             if user.check_password(password):
#                 return user
#         except UserModel.DoesNotExist:
#             return None





# 
# 
# 
