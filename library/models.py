from __future__ import unicode_literals

from django.db import models

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
    description = models.CharField(max_length=500)
    authors = models.CharField(max_length=500)
    homepage = models.CharField(max_length=500)
    previous_names = models.CharField(max_length=255)
    tags = models.CharField(max_length=255)
    platforms = models.CharField(max_length=255)
    sg_versions = models.CharField(max_length=500)
    last_modified = models.DateTimeField()
    last_seen = models.DateTimeField()
    readme = models.TextField()
    issues = models.CharField(max_length=500)
    donate = models.CharField(max_length=500)
    buy = models.CharField(max_length=500)

    def __str__(self):
        return "%d/%s" % (self.id, self.name)

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
    bundle = models.ForeignKey(
        Bundle,
        on_delete=models.CASCADE,
    )
    platforms = models.CharField(max_length=255)
    shotgun = models.CharField(max_length=255)
    version = models.CharField(max_length=255)
    url = models.CharField(max_length=500)
    date = models.DateTimeField()

class BundleType(models.Model):
    name = models.CharField(max_length=50)

class Platform(models.Model):
    name = models.CharField(max_length=50)

