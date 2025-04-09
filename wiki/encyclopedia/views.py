from django.shortcuts import render, redirect


from . import util
from random import randrange
from markdown2 import markdown


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def search(request):
    searched = request.POST['q']
    if (searched in util.list_entries()):
        urlpath = "/wiki/" + searched
        return redirect(urlpath)
    entries = [entry for entry in util.list_entries() if searched in entry]
    return render(request, 'encyclopedia/results.html', {"entries": entries})
    
def title(request, title):
    entry = util.get_entry(title)
    if (entry is None):
        return render(request, 'encyclopedia/error.html', {"title": title})
    return render(request, "encyclopedia/title.html", {
        "entry": markdown(entry), "title": title
    })

def newpage(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        if (title in util.list_entries()):
            return render(request, 'encyclopedia/error.html')
        util.save_entry(title, content)
        url = '/wiki/' + title
        return redirect(url)
    return render(request, 'encyclopedia/newpage.html')

def editpage(request, title=None):
    if request.method == 'POST':
        content = request.POST['content']
        title = request.POST['title']
        util.save_entry(title, content)
        url = '/wiki/' + title
        return redirect(url)
    content = util.get_entry(title)
    return render(request, 'encyclopedia/edit.html', {"title": title,"content": content})
    
def random(request):
    titles = util.list_entries()
    title = titles[randrange(0,len(titles))]
    url = "/wiki/" + title
    return redirect(url)