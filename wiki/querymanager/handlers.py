from django.shortcuts import render
from .models import Page, Category, Pagelinks
from .cache import cache

def handle_page_query(request):
    query_text = request.POST['page']
    print(query_text)
    page_objs = Page.objects.raw(query_text)
    results = []
    for page_obj in page_objs:
        results.append(page_obj.content())
    return render(request, "querymanager/results.html", {
        'results': results,
        'error_message': '',
        'query': query_text,
        'desc': ('page_id','page_title', 'page_is_new', 'page_links_updated', 'page_len')
    })

def handle_category_query(request):
    query_text = request.POST['pl']
    cat_objs = Category.objects.raw(query_text)
    results = []
    for cat_obj in cat_objs:
        results.append(cat_obj.content())
    return render(request, "querymanager/results.html", {
        'results': results,
        'error_message': '',
        'query': query_text,
        'desc': ('cat_id', 'cat_title')
    })


def handle_pagelinks_query(request):
    print(request.POST)
    query_text = request.POST['pl']
    pl_objs = Pagelinks.objects.raw(query_text)
    results = []
    for pl_obj in pl_objs:
        results.append(pl_obj.content())
    return render(request, "querymanager/results.html", {
        'results': results,
        'error_message': '',
        'query': query_text,
        'desc': ('pl_from', 'pl_namespace', 'pl_title', 'pl_from_namespace')
    })