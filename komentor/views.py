from django.shortcuts import redirect, render
from django.utils import timezone
from .models import Comment, Document
from operator import methodcaller


def create_comment(request, url):
    document = Document.objects.get(url=url)
    comment = Comment(place=document, author=request.POST['author'], text=request.POST['text'])
    comment.save()
    return redirect('document', url)


def create_document(request):
    if request.POST['title'] and request.POST['url']:
        document = Document(title=request.POST['title'], url=Document.clean_url(request.POST['url']))
        document.save()
        return redirect('documents_list')
    else:
        return redirect('document_creation')

def document(request, url):
    document = Document.objects.get(url=url)
    comments = Comment.objects.filter(place=document).order_by('date_published')
    return render(request, 'komentor/document.html', {'comments': comments, 'document': document})


def documents_list(request):
    documents = sorted(Document.objects.all(),
                       key=lambda document: -document.get_date_active().timestamp() if document.get_date_active() else 0)
    return render(request, 'komentor/documents_list.html', {'documents': documents})


def document_creation(request, **kwargs):
    return render(request, 'komentor/document_creation.html', kwargs)
