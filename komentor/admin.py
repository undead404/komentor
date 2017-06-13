from django.contrib import admin
from .models import Comment, Commenter, Document, Site, Vote

admin.site.register(Comment)
admin.site.register(Commenter)
admin.site.register(Document)
admin.site.register(Site)
admin.site.register(Vote)