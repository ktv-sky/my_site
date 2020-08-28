from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

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

def new_entry(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(
                reverse('blog:topic', args=[topic_id])
                )
    return render(request, 'blog/new_entry.html', {
        'topic': topic,
        'form': form,
    })

def edit_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
                reverse('blog:topic', args=[topic.id])
                )
    return render(request, 'blog/edit_entry.html', {
        'entry': entry,
        'topic': topic,
        'form': form,
    })
