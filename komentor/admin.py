from django.contrib import admin
from .models import Comment, Document

admin.site.register(Comment)
admin.site.register(Document)