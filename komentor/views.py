from django.shortcuts import redirect, render
from .models import Comment, Document, Commenter
from django.views.decorators.clickjacking import xframe_options_exempt


def create_comment(request, url):
    document = Document.objects.get(url=url)
    commenter, is_new = Commenter.objects.get_or_create(name=request.POST['author'])
    if is_new:
        commenter.save()
    comment = Comment(place=document, author=commenter, text=request.POST['text'])
    comment.save()
    return redirect('document', url)


def create_document(request):
    if request.POST['title'] and request.POST['url']:
        document = Document.objects.create_document(title=request.POST['title'], url=request.POST['url'])
        document.save()
        return redirect('documents_list')
    else:
        return redirect('document_creation')

@xframe_options_exempt
def show_document(request, url):
    document, is_new = Document.objects.get_or_create(url=url)
    if is_new:
        document.save()
    # comments = Comment.objects.filter(place=document).order_by('date_published')
    return render(request, 'komentor/document.html', {'comments': document.comments.all(), 'document': document})


def show_documents(request):
    documents = sorted(Document.objects.all(),
                       key=lambda document: -document.get_date_active().timestamp() if document.get_date_active() else 0)
    return render(request, 'komentor/documents_list.html', {'documents': documents})


def new_document(request, **kwargs):
    return render(request, 'komentor/document_creation.html', kwargs)
