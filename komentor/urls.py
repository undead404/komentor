"""komentor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from .views import create_comment, create_document, document, document_creation, documents_list

urlpatterns = [
    url(r'^$', documents_list),
    url(r'^admin/', admin.site.urls),
    url(r'^create-comment/(.*)', create_comment, name="create_comment"),
    url(r'^create-document/', create_document, name='create_document'),
    url(r'^document/(.*)', document, name='document'),
    url(r'^document-creation/', document_creation, name="document_creation"),
    url(r'^documents/', documents_list, name='documents_list'),
]
