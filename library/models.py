from __future__ import unicode_literals
import copy
import datetime
from django.db import models

class BundleType(models.Model):
    TOOLKIT = 1
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

# CREATE TABLE packages (
#     name                     varchar(500)  NOT NULL PRIMARY KEY,
#     description              varchar       NOT NULL DEFAULT '',
#     authors                  varchar[],
#     homepage                 varchar       NOT NULL DEFAULT '',
#     previous_names           varchar[],
#     tags                     varchar[],
#     platforms                varchar[],
#     sg_versions              integer[],
#     last_modified            timestamp     NOT NULL,
#     last_seen                timestamp     NOT NULL,
#     sources                  varchar[]     NOT NULL,
#     readme                   varchar,
#     issues                   varchar,
#     donate                   varchar,
#     buy                      varchar
# );

class Bundle(models.Model):
    name = models.CharField(max_length=500)
    description = models.CharField(max_length=500, blank=True)
    category = models.ForeignKey(BundleType, on_delete=models.CASCADE, default=BundleType.TOOLKIT)
    authors = models.CharField(max_length=500)
    homepage = models.CharField(max_length=500)
    previous_names = models.CharField(max_length=255, blank=True)
    tags = models.CharField(max_length=255)
    platforms = models.CharField(max_length=255)
    sg_versions = models.CharField(max_length=500)
    last_modified = models.DateTimeField()
    last_seen = models.DateTimeField()
    source_url = models.CharField(max_length=500, unique=True)
    readme = models.TextField()
    issues = models.CharField(max_length=500, blank=True)
    donate = models.CharField(max_length=500, blank=True)
    buy = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return "%d/%s" % (self.id, self.name)

    @staticmethod
    def map_channel_fields_to_db(bundle_dict):
        """
        {
            u'name': u'ShotgunORM',
            'description': u'Python ORM library for Shotgun',
            u'details': u'https://github.com/ndunsworth/python-shotgunorm',
            'homepage': None,
            'issues': u'https://api.github.com/repos/ndunsworth/python-shotgunorm/issues{/number}',
            'readme': '{"name":"README.md","path":"README.md","sha":"1521ec340c1bb68936f8bbe6a72cf913043c5a9b","size":875,"url":"https://api.github.com/repos/ndunsworth/python-shotgunorm/contents/README.md?ref=master","html_url":"https://github.com/ndunsworth/python-shotgunorm/blob/master/README.md","git_url":"https://api.github.com/repos/ndunsworth/python-shotgunorm/git/blobs/1521ec340c1bb68936f8bbe6a72cf913043c5a9b","download_url":"https://raw.githubusercontent.com/ndunsworth/python-shotgunorm/master/README.md","type":"file","content":"VGhlIFNob3RndW5PUk0gUHl0aG9uIGxpYnJhcnkgaXMgYW4gb2JqZWN0IHJl\\nbGF0aW9uYWwgbWFwcGluZyBwYWNrYWdlIGZvciBTaG90Z3VuIFNvZnR3YXJl\\nJ3MgU2hvdGd1biB3ZWIgZGF0YWJhc2UuCgojIEZlYXR1cmVzCiogT2JqZWN0\\nIG9yaWVudGVkCiogRWFzaWx5IGN1c3RvbWl6YWJsZSwgY3JlYXRlIHlvdXIg\\nb3duIHN1Yi1jbGFzc2VzIGZvciBhbnkgRW50aXR5IHR5cGUKKiBDYWxsYmFj\\nayBzeXN0ZW0KKiBDdXN0b20gc2NyaXB0aW5nIGxhbmd1YWdlIGZvciBTaG90\\nZ3VuIGRhdGFiYXNlIHNlYXJjaGVzCiogU3VwcG9ydCBmb3IgRW50aXR5IHN1\\nbW1hcnkgZmllbGRzCiogQWJpbGl0eSB0byBhdHRhY2ggY3VzdG9tIHVzZXIg\\nZmllbGRzIG9uIEVudGl0aWVzIHdoaWNoIGRvIG5vdCBleGlzdCBhcyBwYXJ0\\nIG9mIHRoZSBkYXRhYmFzZSBTY2hlbWEKKiBBc3luY2hyb25vdXMgYmFja2dy\\nb3VuZCBmaWVsZCBwdWxsaW5nCiogVGhyZWFkIHNhZmUKKiBSZWR1Y2VzIGNv\\nZGUgY29tcGxleGl0eQoKIyBEZXBlbmRlbmNpZXMKUmVxdWlyZWQ6CiogUHl0\\naG9uIFZlcnNpb24gMi42IG9yIGdyZWF0ZXIKKiBTaG90Z3VuIFNvZnR3YXJl\\nIFB5dGhvbiBBUEkgLSBbbGlua10oaHR0cHM6Ly9naXRodWIuY29tL3Nob3Rn\\ndW5zb2Z0d2FyZS9weXRob24tYXBpKQoKIyBJbnN0YWxsYXRpb24KSW5zdGFs\\nbCBTaG90Z3VuT1JNIGRpcmVjdG9yeSBpbnRvIHlvdXIgUHl0aG9uIHBhdGgu\\nCgojIERvY3VtZW50YXRpb24KRG9jdW1lbnRhdGlvbiBjYW4gYmUgZm91bmQg\\nb24gdGhlIFNob3RndW5PUk0gR2l0SHViIFt3aWtpXShodHRwczovL2dpdGh1\\nYi5jb20vbmR1bnN3b3J0aC9weXRob24tc2hvdGd1bm9ybS93aWtpL0hvbWUj\\nd2lraS1Eb2N1bWVudGF0aW9uKQo=\\n","encoding":"base64","_links":{"self":"https://api.github.com/repos/ndunsworth/python-shotgunorm/contents/README.md?ref=master","git":"https://api.github.com/repos/ndunsworth/python-shotgunorm/git/blobs/1521ec340c1bb68936f8bbe6a72cf913043c5a9b","html":"https://github.com/ndunsworth/python-shotgunorm/blob/master/README.md"}}',
            u'releases': [{u'branch': u'master', u'shotgun_api': u'*'}],
            'updated_at': datetime.datetime(2015, 7, 13, 14, 55, 8),
            'user': {'avatar_url': u'https://avatars.githubusercontent.com/u/2954795?v=3',
                  'company': None,
                  'html_url': u'https://github.com/ndunsworth',
                  'login': u'ndunsworth',
                  'name': u'Nathan Dunsworth'}
        }
        """
        bundle_copy = copy.deepcopy(bundle_dict)
        db_ready = {
            "name": bundle_copy["name"],
            "description": bundle_copy["description"],
            "category": BundleType.objects.get(name=bundle_copy["category"]),
            "authors": bundle_copy["user"].get("login"),
            "homepage": bundle_copy.get("homepage_gh"),
            "previous_names": bundle_copy.get("previous_names", ""),
            "last_modified": bundle_copy.get("updated_at"),
            "last_seen": datetime.datetime.utcnow(),
            "source_url": bundle_copy.get("details"),
            "readme": bundle_copy["readme"].get("content"),
            "issues": bundle_copy.get("issues", ""),
            "tags": ",".join(bundle_copy.get("labels", ""))
        }

        # override authors from bundle json if provided
        if "authors" in bundle_copy:
            db_ready["authors"] = bundle_copy["authors"]

        # override homepage from bundle json if provided
        if "homepage" in bundle_copy:
            db_ready["homepage"] = bundle_copy.get("homepage", "")

        return db_ready






# -- Each package can have more than one release at a time, and for different platforms
# CREATE TABLE releases (
#     package                  varchar(500)  NOT NULL REFERENCES packages(name) ON DELETE CASCADE ON UPDATE CASCADE,
#     platforms                varchar[]     NOT NULL,
#     sublime_text             varchar       NOT NULL,
#     version                  varchar       NOT NULL,
#     url                      varchar       NOT NULL,
#     date                     timestamp     NOT NULL,
#     dependencies             varchar[],
#     PRIMARY KEY(package, platforms, sublime_text, version)
# );
class Release(models.Model):
    bundle = models.ForeignKey(Bundle, on_delete=models.CASCADE)
    platforms = models.CharField(max_length=255)
    shotgun = models.CharField(max_length=255)
    version = models.CharField(max_length=255)
    url = models.CharField(max_length=500)
    download_url = models.CharField(max_length=500)
    date = models.DateTimeField()

    @staticmethod
    def map_version_fields_to_db(bundle, version_data):
        version_copy = copy.deepcopy(version_data)
        db_ready = {
            "bundle": bundle,
            "platforms": "*",
            "shotgun": "*",
            "version": version_copy["name"],
            "url": version_copy.get("url"),
            "download_url": version_copy.get("download", ""),
            "date": version_copy.get("date")
        }
        return db_ready


class Platform(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class BundleRating(models.Model):
    bundle = models.ForeignKey(Bundle, on_delete=models.CASCADE)
    rating = models.IntegerField()

    def __str__(self):
        return "%s/%d" % (self.name, self.rating)
