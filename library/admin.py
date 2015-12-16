from django.contrib import admin

from .models import Bundle, BundleType, Platform, Release

admin.site.register(Bundle)
admin.site.register(BundleType)
admin.site.register(Release)
admin.site.register(Platform)
