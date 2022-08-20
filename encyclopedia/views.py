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


def search(request):

    query = request.GET.get("q", None)
    entries_list = util.list_entries()

    if query is None:
        
        return render(request, "encyclopedia/index.html", {
            "entries": entries_list
        })

    elif query in entries_list:

        text = util.get_entry(query)
        return render(request, "encyclopedia/page.html", {
            "name": query,
            "text": text 
            })

    else:

        matched_list = [x for x in entries_list if query in x] 
        return render(request, "encyclopedia/index.html", {
                    "entries": matched_list 
                })






    return HttpResponse(query)

