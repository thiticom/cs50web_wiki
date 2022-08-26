from ast import Pass
from django.shortcuts import HttpResponse, render, HttpResponseRedirect
from django import forms
from django.urls import reverse

from . import util
import random
import markdown2


class new_entry_form(forms.Form):
    title = forms.CharField(label="Title")
    body = forms.CharField(widget=forms.Textarea, label="Content")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request ,name):

    m_text = util.get_entry(name)

    if m_text is None:
        return render(request, "encyclopedia/error.html", {
                    "text": "Do not find entry."
                })

    html = markdown2.markdown(m_text)

    return render(request, "encyclopedia/page.html", {
        "name": name,
        "text": html 
        })


def search(request):

    query = request.GET.get("q", None)
    entries_list = util.list_entries()

    if query is None:
        
        return render(request, "encyclopedia/index.html", {
            "entries": entries_list
        })

    elif query in entries_list:
        return HttpResponseRedirect(reverse('entry', args=[query]))

    else:

        matched_list = [x for x in entries_list if query in x] 
        return render(request, "encyclopedia/index.html", {
                    "entries": matched_list 
                })


def add(request):
    if request.method == "POST":

        form = new_entry_form(request.POST)

        if form.is_valid():

            title = form.cleaned_data["title"]
            body = form.cleaned_data["body"]

            if util.get_entry(title) is None:
                util.save_entry(title,body)
            else:
                return render(request, "encyclopedia/error.html", {
                    "text": "Entry already exist"
                })
            
            return HttpResponseRedirect(reverse('entry', args=[title]))     

        else:
            return render(request, "encyclopedia/error.html", {
                    "text": "Form is not valid."
                })

    return render(request, "encyclopedia/add.html", {
        "form": new_entry_form()
    })


def edit(request, name):

    if request.method == "POST":
        form = new_entry_form(request.POST)

        if form.is_valid():

            title = form.cleaned_data["title"]
            body  = form.cleaned_data["body"]

            util.save_entry(title, body)
            
            return HttpResponseRedirect(reverse('entry', args=[title]))

        
    body = util.get_entry(name)

    if body is None:

        return render(request, "encyclopedia/error.html", {
                "text": "Please specify the page you want to edit."
                })

    else:

        return render(request, "encyclopedia/edit.html", {
                "form": new_entry_form(initial={'title':name,'body':body}),
                "name": name
            })


def random_page(request):

    entry_list = util.list_entries();
    title = random.choice(entry_list)


    return HttpResponseRedirect(reverse('entry', args=[title]))