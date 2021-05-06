from django.shortcuts import render

from django.urls import reverse

from django.http import HttpResponseRedirect

from . import util

from random import choice

from markdown2 import Markdown

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    markdowner = Markdown()
    entryPage = util.get_entry(entry)
    if entryPage is None:
        return render(request, "encyclopedia/NonExistingEntry.html",{
            "pageTitle": entry,
            "entry": entry
        })
    else:
        return render(request,"encyclopedia/entry.html",{
            "entry": markdowner.convert(entryPage),
            "entryTitle":entry
        })

def search(request):
    value = request.GET.get('q','')
    if util.get_entry(value) is None:
        subEntries = []
        for entry in util.list_entries():
            if value.upper() in entry.upper():
                subEntries.append(entry)

        if len(subEntries) > 0:
            return render(request, "encyclopedia/index.html",{
                "entries": subEntries,
                "search": True,
                "value": value,
                "noPages": False
            })
        else:
            return render(request, "encyclopedia/index.html", {
                "entries": subEntries,
                "search": True,
                "value": value,
                "noPages": True
            })
    else:
        return HttpResponseRedirect(reverse("entry", kwargs={"entry": value}))

def random(request):
    listEntries = util.list_entries()
    randomChoice = choice(listEntries)
    randomPage = util.get_entry(randomChoice)
    markdowner = Markdown()
    return render(request, "encyclopedia/entry.html",{
        "entry": markdowner.convert(randomPage),
        "entryTitle": randomChoice
    })

def CreateNewPage(request):
    if request.method == "POST":
        title = request.POST['title']
        description = request.POST['description']
        editing = request.POST['editing']
        if util.get_entry(title) is None or editing == 'true':
            util.save_entry(title, description)
            return HttpResponseRedirect(reverse("entry", kwargs={"entry": title}))
        else:
            existing = True
            return render(request, "encyclopedia/CreateNew.html",{
                "existing": existing,
                "entry": title,
                "editing": False
            })
    else:
        return render(request,"encyclopedia/CreateNew.html")

def edit(request, entry):
    Page = util.get_entry(entry)
    if Page is None:
        return render(request, "encyclopedia/NonExistingEntry.html",{
            "pageTitle": entry,
            "entry": entry
        })
    else:
        editing = True
        return render(request,"encyclopedia/CreateNew.html",{
            "pageTitle": entry,
            "entry": entry,
            "title": entry,
            "content": Page,
            "editing": editing
        })


