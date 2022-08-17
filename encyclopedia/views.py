from django.shortcuts import HttpResponse, render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request ,name):

    text = util.get_entry(name)

    if text is None:
        text = "Error"

    return render(request, "encyclopedia/page.html", {
        "name": name,
        "text": text 
        })

