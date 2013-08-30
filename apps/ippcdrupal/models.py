from django.db import models

class DrupalUsers(models.Model):
    uid = models.IntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=180)
    pass_field = models.CharField(max_length=384, db_column='pass') # Field renamed because it was a Python reserved word.
    mail = models.CharField(max_length=762, blank=True)
    theme = models.CharField(max_length=765)
    signature = models.CharField(max_length=765)
    signature_format = models.CharField(max_length=765, blank=True)
    created = models.IntegerField()
    access = models.IntegerField()
    login = models.IntegerField()
    status = models.IntegerField()
    timezone = models.CharField(max_length=96, blank=True)
    language = models.CharField(max_length=36)
    picture = models.IntegerField()
    init = models.CharField(max_length=762, blank=True)
    data = models.TextField(blank=True)
    class Meta:
        db_table = u'users'

    def __unicode__(self):
        return u"%s - drupal user" % (self.name)
            
# class Actions(models.Model):
#     aid = models.CharField(max_length=765, primary_key=True)
#     type = models.CharField(max_length=96)
#     callback = models.CharField(max_length=765)
#     parameters = models.TextField()
#     label = models.CharField(max_length=765)
#     class Meta:
#         db_table = u'actions'
# 
# class Authmap(models.Model):
#     aid = models.IntegerField(primary_key=True)
#     uid = models.IntegerField()
#     authname = models.CharField(unique=True, max_length=384)
#     module = models.CharField(max_length=384)
#     class Meta:
#         db_table = u'authmap'
# 
# class Batch(models.Model):
#     bid = models.IntegerField(primary_key=True)
#     token = models.CharField(max_length=192)
#     timestamp = models.IntegerField()
#     batch = models.TextField(blank=True)
#     class Meta:
#         db_table = u'batch'
# 
# class Block(models.Model):
#     bid = models.IntegerField(primary_key=True)
#     module = models.CharField(max_length=192)
#     delta = models.CharField(unique=True, max_length=96)
#     theme = models.CharField(max_length=192)
#     status = models.IntegerField()
#     weight = models.IntegerField()
#     region = models.CharField(max_length=192)
#     custom = models.IntegerField()
#     visibility = models.IntegerField()
#     pages = models.TextField()
#     title = models.CharField(max_length=192)
#     cache = models.IntegerField()
#     class Meta:
#         db_table = u'block'
# 
# class BlockCustom(models.Model):
#     bid = models.IntegerField(primary_key=True)
#     body = models.TextField(blank=True)
#     info = models.CharField(unique=True, max_length=384)
#     format = models.CharField(max_length=765, blank=True)
#     class Meta:
#         db_table = u'block_custom'
# 
# class BlockNodeType(models.Model):
#     module = models.CharField(max_length=192, primary_key=True)
#     delta = models.CharField(max_length=96, primary_key=True)
#     type = models.CharField(max_length=96)
#     class Meta:
#         db_table = u'block_node_type'
# 
# class BlockRole(models.Model):
#     module = models.CharField(max_length=192, primary_key=True)
#     delta = models.CharField(max_length=96, primary_key=True)
#     rid = models.IntegerField()
#     class Meta:
#         db_table = u'block_role'
# 
# class BlockedIps(models.Model):
#     iid = models.IntegerField(primary_key=True)
#     ip = models.CharField(max_length=120)
#     class Meta:
#         db_table = u'blocked_ips'
# 
# class Cache(models.Model):
#     cid = models.CharField(max_length=765, primary_key=True)
#     data = models.TextField(blank=True)
#     expire = models.IntegerField()
#     created = models.IntegerField()
#     serialized = models.IntegerField()
#     class Meta:
#         db_table = u'cache'
# 
# class CacheBlock(models.Model):
#     cid = models.CharField(max_length=765, primary_key=True)
#     data = models.TextField(blank=True)
#     expire = models.IntegerField()
#     created = models.IntegerField()
#     serialized = models.IntegerField()
#     class Meta:
#         db_table = u'cache_block'
# 
# class CacheBootstrap(models.Model):
#     cid = models.CharField(max_length=765, primary_key=True)
#     data = models.TextField(blank=True)
#     expire = models.IntegerField()
#     created = models.IntegerField()
#     serialized = models.IntegerField()
#     class Meta:
#         db_table = u'cache_bootstrap'
# 
# class CacheField(models.Model):
#     cid = models.CharField(max_length=765, primary_key=True)
#     data = models.TextField(blank=True)
#     expire = models.IntegerField()
#     created = models.IntegerField()
#     serialized = models.IntegerField()
#     class Meta:
#         db_table = u'cache_field'
# 
# class CacheFilter(models.Model):
#     cid = models.CharField(max_length=765, primary_key=True)
#     data = models.TextField(blank=True)
#     expire = models.IntegerField()
#     created = models.IntegerField()
#     serialized = models.IntegerField()
#     class Meta:
#         db_table = u'cache_filter'
# 
# class CacheForm(models.Model):
#     cid = models.CharField(max_length=765, primary_key=True)
#     data = models.TextField(blank=True)
#     expire = models.IntegerField()
#     created = models.IntegerField()
#     serialized = models.IntegerField()
#     class Meta:
#         db_table = u'cache_form'
# 
# class CacheMenu(models.Model):
#     cid = models.CharField(max_length=765, primary_key=True)
#     data = models.TextField(blank=True)
#     expire = models.IntegerField()
#     created = models.IntegerField()
#     serialized = models.IntegerField()
#     class Meta:
#         db_table = u'cache_menu'
# 
# class CachePage(models.Model):
#     cid = models.CharField(max_length=765, primary_key=True)
#     data = models.TextField(blank=True)
#     expire = models.IntegerField()
#     created = models.IntegerField()
#     serialized = models.IntegerField()
#     class Meta:
#         db_table = u'cache_page'
# 
# class CachePath(models.Model):
#     cid = models.CharField(max_length=765, primary_key=True)
#     data = models.TextField(blank=True)
#     expire = models.IntegerField()
#     created = models.IntegerField()
#     serialized = models.IntegerField()
#     class Meta:
#         db_table = u'cache_path'
# 
# class DateFormatLocale(models.Model):
#     format = models.CharField(max_length=300)
#     type = models.CharField(max_length=192, primary_key=True)
#     language = models.CharField(max_length=36, primary_key=True)
#     class Meta:
#         db_table = u'date_format_locale'
# 
# class DateFormatType(models.Model):
#     type = models.CharField(max_length=192, primary_key=True)
#     title = models.CharField(max_length=765)
#     locked = models.IntegerField()
#     class Meta:
#         db_table = u'date_format_type'
# 
# class DateFormats(models.Model):
#     dfid = models.IntegerField(primary_key=True)
#     format = models.CharField(unique=True, max_length=300)
#     type = models.CharField(unique=True, max_length=192)
#     locked = models.IntegerField()
#     class Meta:
#         db_table = u'date_formats'
# 
# class FieldConfig(models.Model):
#     id = models.IntegerField(primary_key=True)
#     field_name = models.CharField(max_length=96)
#     type = models.CharField(max_length=384)
#     module = models.CharField(max_length=384)
#     active = models.IntegerField()
#     storage_type = models.CharField(max_length=384)
#     storage_module = models.CharField(max_length=384)
#     storage_active = models.IntegerField()
#     locked = models.IntegerField()
#     data = models.TextField()
#     cardinality = models.IntegerField()
#     translatable = models.IntegerField()
#     deleted = models.IntegerField()
#     class Meta:
#         db_table = u'field_config'
# 
# class FieldConfigInstance(models.Model):
#     id = models.IntegerField(primary_key=True)
#     field_id = models.IntegerField()
#     field_name = models.CharField(max_length=96)
#     entity_type = models.CharField(max_length=96)
#     bundle = models.CharField(max_length=384)
#     data = models.TextField()
#     deleted = models.IntegerField()
#     class Meta:
#         db_table = u'field_config_instance'
# 
# class FileManaged(models.Model):
#     fid = models.IntegerField(primary_key=True)
#     uid = models.IntegerField()
#     filename = models.CharField(max_length=765)
#     uri = models.CharField(unique=True, max_length=765)
#     filemime = models.CharField(max_length=765)
#     filesize = models.IntegerField()
#     status = models.IntegerField()
#     timestamp = models.IntegerField()
#     class Meta:
#         db_table = u'file_managed'
# 
# class FileUsage(models.Model):
#     fid = models.IntegerField()
#     module = models.CharField(max_length=765)
#     type = models.CharField(max_length=192)
#     id = models.IntegerField()
#     count = models.IntegerField()
#     class Meta:
#         db_table = u'file_usage'
# 
# class Filter(models.Model):
#     format = models.CharField(max_length=765, primary_key=True)
#     module = models.CharField(max_length=192)
#     name = models.CharField(max_length=96)
#     weight = models.IntegerField()
#     status = models.IntegerField()
#     settings = models.TextField(blank=True)
#     class Meta:
#         db_table = u'filter'
# 
# class FilterFormat(models.Model):
#     format = models.CharField(max_length=765, primary_key=True)
#     name = models.CharField(unique=True, max_length=765)
#     cache = models.IntegerField()
#     status = models.IntegerField()
#     weight = models.IntegerField()
#     class Meta:
#         db_table = u'filter_format'
# 
# class Flood(models.Model):
#     fid = models.IntegerField(primary_key=True)
#     event = models.CharField(max_length=192)
#     identifier = models.CharField(max_length=384)
#     timestamp = models.IntegerField()
#     expiration = models.IntegerField()
#     class Meta:
#         db_table = u'flood'
# 
# class History(models.Model):
#     uid = models.IntegerField(primary_key=True)
#     nid = models.IntegerField()
#     timestamp = models.IntegerField()
#     class Meta:
#         db_table = u'history'
# 
# class MenuLinks(models.Model):
#     menu_name = models.CharField(max_length=96)
#     mlid = models.IntegerField(primary_key=True)
#     plid = models.IntegerField()
#     link_path = models.CharField(max_length=765)
#     router_path = models.CharField(max_length=765)
#     link_title = models.CharField(max_length=765)
#     options = models.TextField(blank=True)
#     module = models.CharField(max_length=765)
#     hidden = models.IntegerField()
#     external = models.IntegerField()
#     has_children = models.IntegerField()
#     expanded = models.IntegerField()
#     weight = models.IntegerField()
#     depth = models.IntegerField()
#     customized = models.IntegerField()
#     p1 = models.IntegerField()
#     p2 = models.IntegerField()
#     p3 = models.IntegerField()
#     p4 = models.IntegerField()
#     p5 = models.IntegerField()
#     p6 = models.IntegerField()
#     p7 = models.IntegerField()
#     p8 = models.IntegerField()
#     p9 = models.IntegerField()
#     updated = models.IntegerField()
#     class Meta:
#         db_table = u'menu_links'
# 
# class MenuRouter(models.Model):
#     path = models.CharField(max_length=765, primary_key=True)
#     load_functions = models.TextField()
#     to_arg_functions = models.TextField()
#     access_callback = models.CharField(max_length=765)
#     access_arguments = models.TextField(blank=True)
#     page_callback = models.CharField(max_length=765)
#     page_arguments = models.TextField(blank=True)
#     delivery_callback = models.CharField(max_length=765)
#     fit = models.IntegerField()
#     number_parts = models.IntegerField()
#     context = models.IntegerField()
#     tab_parent = models.CharField(max_length=765)
#     tab_root = models.CharField(max_length=765)
#     title = models.CharField(max_length=765)
#     title_callback = models.CharField(max_length=765)
#     title_arguments = models.CharField(max_length=765)
#     theme_callback = models.CharField(max_length=765)
#     theme_arguments = models.CharField(max_length=765)
#     type = models.IntegerField()
#     description = models.TextField()
#     position = models.CharField(max_length=765)
#     weight = models.IntegerField()
#     include_file = models.TextField(blank=True)
#     class Meta:
#         db_table = u'menu_router'
# 
# class Node(models.Model):
#     nid = models.IntegerField()
#     vid = models.IntegerField(unique=True, null=True, blank=True)
#     type = models.CharField(max_length=96)
#     language = models.CharField(max_length=36)
#     title = models.CharField(max_length=765)
#     uid = models.IntegerField()
#     status = models.IntegerField()
#     created = models.IntegerField()
#     changed = models.IntegerField()
#     comment = models.IntegerField()
#     promote = models.IntegerField()
#     sticky = models.IntegerField()
#     tnid = models.IntegerField()
#     translate = models.IntegerField()
#     class Meta:
#         db_table = u'node'
# 
# class NodeAccess(models.Model):
#     nid = models.IntegerField(primary_key=True)
#     gid = models.IntegerField(primary_key=True)
#     realm = models.CharField(max_length=765, primary_key=True)
#     grant_view = models.IntegerField()
#     grant_update = models.IntegerField()
#     grant_delete = models.IntegerField()
#     class Meta:
#         db_table = u'node_access'
# 
# class NodeRevision(models.Model):
#     nid = models.IntegerField()
#     vid = models.IntegerField(primary_key=True)
#     uid = models.IntegerField()
#     title = models.CharField(max_length=765)
#     log = models.TextField()
#     timestamp = models.IntegerField()
#     status = models.IntegerField()
#     comment = models.IntegerField()
#     promote = models.IntegerField()
#     sticky = models.IntegerField()
#     class Meta:
#         db_table = u'node_revision'
# 
# class NodeType(models.Model):
#     type = models.CharField(max_length=96, primary_key=True)
#     name = models.CharField(max_length=765)
#     base = models.CharField(max_length=765)
#     module = models.CharField(max_length=765)
#     description = models.TextField()
#     help = models.TextField()
#     has_title = models.IntegerField()
#     title_label = models.CharField(max_length=765)
#     custom = models.IntegerField()
#     modified = models.IntegerField()
#     locked = models.IntegerField()
#     disabled = models.IntegerField()
#     orig_type = models.CharField(max_length=765)
#     class Meta:
#         db_table = u'node_type'
# 
# class Queue(models.Model):
#     item_id = models.IntegerField(primary_key=True)
#     name = models.CharField(max_length=765)
#     data = models.TextField(blank=True)
#     expire = models.IntegerField()
#     created = models.IntegerField()
#     class Meta:
#         db_table = u'queue'
# 
# class Registry(models.Model):
#     name = models.CharField(max_length=765, primary_key=True)
#     type = models.CharField(max_length=27)
#     filename = models.CharField(max_length=765)
#     module = models.CharField(max_length=765)
#     weight = models.IntegerField()
#     class Meta:
#         db_table = u'registry'
# 
# class RegistryFile(models.Model):
#     filename = models.CharField(max_length=765, primary_key=True)
#     hash = models.CharField(max_length=192)
#     class Meta:
#         db_table = u'registry_file'

# class Role(models.Model):
#     rid = models.IntegerField(primary_key=True)
#     name = models.CharField(max_length=192)
#     weight = models.IntegerField()
#     class Meta:
#         db_table = u'role'
# 
# class RolePermission(models.Model):
#     rid = models.IntegerField(primary_key=True)
#     permission = models.CharField(max_length=384)
#     module = models.CharField(max_length=765)
#     class Meta:
#         db_table = u'role_permission'

# class Semaphore(models.Model):
#     name = models.CharField(max_length=765, primary_key=True)
#     value = models.CharField(max_length=765)
#     expire = models.FloatField()
#     class Meta:
#         db_table = u'semaphore'
# 
# class Sequences(models.Model):
#     value = models.IntegerField(primary_key=True)
#     class Meta:
#         db_table = u'sequences'

# class Sessions(models.Model):
#     uid = models.IntegerField()
#     sid = models.CharField(max_length=384, primary_key=True)
#     ssid = models.CharField(max_length=384)
#     hostname = models.CharField(max_length=384)
#     timestamp = models.IntegerField()
#     cache = models.IntegerField()
#     session = models.TextField(blank=True)
#     class Meta:
#         db_table = u'sessions'

# class System(models.Model):
#     filename = models.CharField(max_length=765, primary_key=True)
#     name = models.CharField(max_length=765)
#     type = models.CharField(max_length=36)
#     owner = models.CharField(max_length=765)
#     status = models.IntegerField()
#     bootstrap = models.IntegerField()
#     schema_version = models.IntegerField()
#     weight = models.IntegerField()
#     info = models.TextField(blank=True)
#     class Meta:
#         db_table = u'system'
# 
# class UrlAlias(models.Model):
#     pid = models.IntegerField()
#     source = models.CharField(max_length=765)
#     alias = models.CharField(max_length=765)
#     language = models.CharField(max_length=36)
#     class Meta:
#         db_table = u'url_alias'



# class UsersRoles(models.Model):
#     uid = models.IntegerField(primary_key=True)
#     rid = models.IntegerField()
#     class Meta:
#         db_table = u'users_roles'

# class Variable(models.Model):
#     name = models.CharField(max_length=384, primary_key=True)
#     value = models.TextField()
#     class Meta:
#         db_table = u'variable'
# 
# class Watchdog(models.Model):
#     wid = models.IntegerField(primary_key=True)
#     uid = models.IntegerField()
#     type = models.CharField(max_length=192)
#     message = models.TextField()
#     variables = models.TextField()
#     severity = models.IntegerField()
#     link = models.CharField(max_length=765, blank=True)
#     location = models.TextField()
#     referer = models.TextField(blank=True)
#     hostname = models.CharField(max_length=384)
#     timestamp = models.IntegerField()
#     class Meta:
#         db_table = u'watchdog'