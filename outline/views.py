from django.shortcuts import render
from . import util
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
import random
from markdown2 import Markdown


markdowner = Markdown()

class SearchForm(forms.Form):
    query = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'placeholder': 'Search here...'}))

class CreateForm(forms.Form):
    title = forms.CharField(label="Add Title")
    body = forms.CharField(label="Add Body", widget=forms.Textarea(
        attrs={'rows': 1, 'cols': 10}))

class EditForm(forms.Form):
    title = forms.CharField(label="Edit Title")
    body = forms.CharField(label="Edit Body", widget=forms.Textarea(
        attrs={'rows': 1, 'cols': 10}))
# Create your views here.
def index(request):
    form = SearchForm()
    return render(request, "outline/index.html", {
        "topics": util.list_topics(),"form": form
    })

def entry(request, title):
    flag = util.get_topic(title)
    if flag is None:
        form = SearchForm()
        content = "The page you requested is not available."
        return render(request, "outline/error.html", {"form": form, "content": content})
    else:
        form = SearchForm()
        mdcontent = util.get_topic(title)
        htmlcontent = markdowner.convert(mdcontent)
        return render(request, "outline/entry.html", {
            "title": title, "content": htmlcontent, "form": form
        })

def search(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data.get("query")
            present = False
            for entry in util.list_topics():
                if  data == entry:
                    mdcontent = util.get_topic(data)
                    htmlcontent = markdowner.convert(mdcontent)
                    present = True
                    break
            if present:
                return render(request, "outline/entry.html", {"content": htmlcontent, "form": form, "title": data})
            else:
                lst = []
                for entry in util.list_topics():
                    if data.lower() in entry.lower():
                        lst.append(entry)
                if len(lst) == 0:
                    form = SearchForm()
                    content = "The page you requested for is not available"
                    return render(request, "outline/error.html", {'form': form, "content": content})
                else:
                    return render(request, "outline/index.html", {"topics": lst, "form": form})
    else:
        form = SearchForm()
        content = "Search for some page in order to see the result"
        return render(request, "outline/error.html", {'form': form, "content": content})

def create(request):
    if request.method == "POST":
        createform = CreateForm(request.POST)
        if createform.is_valid():
            title = createform.cleaned_data.get("title")
            body = createform.cleaned_data.get("body")
            present = False
            for entry in util.list_topics():
                if title == entry:
                    present = True
                    break
            if present:
                content = "This Page is Already Present"
                form = SearchForm()
                return render(request, "outline/error.html", {'form': form, "content": content})
            else:
                util.save_topic(title, body)
                form = SearchForm()
                mdcontent = util.get_topic(title)
                htmlcontent = markdowner.convert(mdcontent)
                return render(request, "outline/entry.html", {
                    "title": title, "content": htmlcontent, "form": form
                })
    else:
        form = SearchForm()
        createform = CreateForm()
        return render(request, "outline/create.html", {"form": form, "createform": createform})
    
def edit(request, title):
    if request.method == "POST":
        editform = EditForm(request.POST)
        if editform.is_valid():
            title = editform.cleaned_data.get("title")
            body = editform.cleaned_data.get("body")
            util.save_topic(title, body)
            form = SearchForm()
            htmlcontent = markdowner.convert(body)
            return render(request, "outline/entry.html", {
                "title": title, "content": htmlcontent, "form": form
            })
    else:
        form = SearchForm()
        editform = EditForm({"title": title, "body": util.get_topic(title)})
        return render(request, "outline/edit.html", {"form": form, "editform": editform})

def randoms(request):
    entries = util.list_topics()
    num = len(entries)
    entry = random.randint(0, num-1)
    title = entries[entry]
    mdcontent = util.get_topic(title)
    htmlcontent = markdowner.convert(mdcontent)
    form = SearchForm()
    return render(request, "outline/randoms.html", {"form": form, "title": title, "content": htmlcontent})




