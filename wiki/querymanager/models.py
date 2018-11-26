# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class Category(models.Model):
    cat_id = models.AutoField(primary_key=True)
    cat_title = models.CharField(unique=True, max_length=255)
    cat_pages = models.IntegerField()
    cat_subcats = models.IntegerField()
    cat_files = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'category'

    def content(self):
        return (self.cat_id, self.cat_title)

    def __repr__(self):
        return "({},{})".format(self.cat_id,self.cat_title)

    def __str__(self):
        return "({},{})".format(self.cat_id,self.cat_title)


class Categorylinks(models.Model):
    cl_from = models.PositiveIntegerField(primary_key=True)
    cl_to = models.CharField(max_length=255)
    cl_sortkey = models.CharField(max_length=230)
    cl_timestamp = models.DateTimeField()
    cl_sortkey_prefix = models.CharField(max_length=255)
    cl_collation = models.CharField(max_length=32)
    cl_type = models.CharField(max_length=6)

    class Meta:
        managed = False
        db_table = 'categorylinks'
        unique_together = (('cl_from', 'cl_to'),)

    def content(self):
        return (self.cl_from, self.cl_to, self.cl_collation, self.cl_sortkey, self.cl_timestamp)

    def __repr__(self):
        return "({},{},{},{},{})".format(self.cl_from, self.cl_to, self.cl_collation, self.cl_sortkey, self.cl_timestamp)

    def __str__(self):
       return "({},{},{},{},{})".format(self.cl_from, self.cl_to, self.cl_collation, self.cl_sortkey,self.cl_timestamp)

class Page(models.Model):
    page_id = models.AutoField(primary_key=True)
    page_namespace = models.IntegerField()
    page_title = models.CharField(max_length=255)
    page_restrictions = models.CharField(max_length=255)
    page_counter = models.BigIntegerField()
    page_is_redirect = models.PositiveIntegerField()
    page_is_new = models.PositiveIntegerField()
    page_random = models.FloatField()
    page_touched = models.CharField(max_length=14)
    page_links_updated = models.CharField(max_length=14, blank=True, null=True)
    page_latest = models.PositiveIntegerField()
    page_len = models.PositiveIntegerField()
    page_no_title_convert = models.IntegerField()
    page_content_model = models.CharField(max_length=32, blank=True, null=True)
    page_lang = models.CharField(max_length=35, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'page'
        unique_together = (('page_namespace', 'page_title'),)

    def content(self):
        return (self.page_id,self.page_title, self.page_is_new, self.page_links_updated, self.page_len)

    def __repr__(self):
        return "({},{},{},{},{})".format(self.page_id,self.page_title, self.page_is_new, self.page_links_updated, self.page_len)

    def __str__(self):
        return "({},{},{},{},{})".format(self.page_id,self.page_title, self.page_is_new, self.page_links_updated, self.page_len)


class Pagelinks(models.Model):
    pl_from = models.PositiveIntegerField(primary_key=True)
    pl_namespace = models.IntegerField()
    pl_title = models.CharField(max_length=255)
    pl_from_namespace = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'pagelinks'
        unique_together = (('pl_from', 'pl_namespace', 'pl_title'),)

    def content(self):
        return (self.pl_from,self.pl_namespace, self.pl_title, self.pl_from_namespace)

    def __repr__(self):
        return "({},{},{},{})".format(self.pl_from,self.pl_namespace, self.pl_title, self.pl_from_namespace)

    def __str__(self):
        return "({},{},{},{})".format(self.pl_from,self.pl_namespace, self.pl_title, self.pl_from_namespace)

class WikiLink(models.Model):
    wid = models.IntegerField()
    title = models.CharField(max_length=256, blank=True, null=True)
    link = models.CharField(max_length=256, blank=True, null=True)
    pos = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wiki_link'


class WikiMeta(models.Model):
    wid = models.IntegerField()
    revid = models.CharField(db_column='revId', max_length=256, blank=True, null=True)  # Field name made lowercase.
    title = models.CharField(max_length=256, blank=True, null=True)
    redirect = models.CharField(max_length=256, blank=True, null=True)
    category = models.CharField(max_length=256, blank=True, null=True)
    ts = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wiki_meta'
