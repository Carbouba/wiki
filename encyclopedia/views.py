import random

from django.http import HttpResponse
from django.shortcuts import render, redirect
from markdown2 import Markdown

from . import util

def converter_md_to_html(title):
    entry = util.get_entry(title)
    if entry == None:
        return None
    else:
        markdowner = Markdown()
        html = markdowner.convert(entry)
        return html

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = converter_md_to_html(title)
    if content == None:
        return render(request, 'encyclopedia/error.html')
    else:
        return render(request, 'encyclopedia/entry.html', {'title': title, 'content': content})

def search(request):
    entries = util.list_entries()
    result = []
    if request.method == "GET":
        query = request.GET.get("q")
        entry_research = util.get_entry(query)
        if entry_research == None:
            for entry_result in entries:
                if query.lower() in entry_result.lower():
                    result.append(entry_result)
            return render(request, "encyclopedia/search.html", context={'query': query, 'result': result})
        else:
           return entry(request, query)


def new(request):
    if request.method == 'POST':
        new_title = request.POST.get('title')
        new_content = request.POST.get('content')

        existed_title = util.get_entry(new_title)
        if existed_title is not None:
            return HttpResponse(f"<h1>A page with the same title '{new_title}' already exist</h1>")
        else:
            util.save_entry(new_title, new_content)
            return redirect("entry", title=new_title)
    return render(request, 'encyclopedia/new-page.html')


def edit(request, title):
    if request.method == "POST":
        edited_title = request.POST.get('title')
        edited_content = request.POST.get('content')

        util.save_entry(edited_title, edited_content)
        return redirect("entry", title=edited_title)

    return render(request, 'encyclopedia/edit.html', {'title': title, 'content': util.get_entry(title)})

def random_entry(request):
    entries = util.list_entries()

    random_title = random.choice(entries)

    return entry(request, random_title)
