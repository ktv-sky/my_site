from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

# Create your views here.
def index(request):
    return render(request, 'blog/index.html')

@login_required
def topics(request):
    topics = Topic.objects.filter(owner=request.user).order_by('-date_added')
    return render(request, 'blog/topics.html', {
        'topics': topics
    })

@login_required
def topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    check_topic_owner(topic.owner, request.user)
    entries = topic.entry_set.order_by('-date_added')
    tags = topic.tag.all()
    return render(request, 'blog/topic.html', {
        'topic': topic,
        'entries': entries,
        'tags': tags
    })

@login_required
def new_topic(request):
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('blog:topics')

    return render(request, 'blog/new_topic.html', {
        'form': form
    })

@login_required
def new_entry(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    check_topic_owner(topic.owner, request.user)
    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('blog:topic', topic_id=topic_id)

    return render(request, 'blog/new_entry.html', {
        'topic': topic,
        'form': form,
    })

@login_required
def edit_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    check_topic_owner(topic.owner, request.user)
    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('blog:topic', topic_id=topic.id)

    return render(request, 'blog/edit_entry.html', {
        'entry': entry,
        'topic': topic,
        'form': form,
    })

def check_topic_owner(owner, user):
    if owner != user:
        raise Http404
