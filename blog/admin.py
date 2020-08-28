from django.contrib import admin

from .models import Tag, Topic, Entry

# Register your models here.
admin.site.register(Topic)
admin.site.register(Entry)
admin.site.register(Tag)
