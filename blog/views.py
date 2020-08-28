from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Topic, Entry
from .forms import TopicForm

# Create your views here.
def index(request):
    return render(request, 'blog/index.html')

def topics(request):
    topics = Topic.objects.all().order_by('-date_added')
    return render(request, 'blog/topics.html', {
        'topics': topics
    })

def topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    entries = topic.entry_set.order_by('-date_added')
    tags = topic.tag.all()
    return render(request, 'blog/topic.html', {
        'topic': topic,
        'entries': entries,
        'tags': tags
    })

def new_topic(request):
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('blog:topics'))
    return render(request, 'blog/new_topic.html', {
        'form': form
    })
