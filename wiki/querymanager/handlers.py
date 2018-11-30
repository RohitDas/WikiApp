import logging
from django.shortcuts import render
from .models import Page, Category, Pagelinks, Categorylinks
from .cache import cache
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
import time

logger = logging.getLogger("info")
error_logger = logging.getLogger("django_error")


def handle_page_query(request):
    start_time = time.time()
    query_text = request.POST['page']
    logger.info("Running query: {}".format(query_text))
    error_message = ""
    desc = ('page_id','page_title', 'page_is_new', 'page_links_updated', 'page_len')

    if cache.has_key(query_text):
        logger.info('Data is fetched from cache')
        page = request.GET.get('page', 1)
        results, pages = cache.get(query_text+str(page))
    else:
        try:
            logger.info('Data is fetched from database')
            page_objs = Page.objects.raw(query_text)
            paginator = Paginator(page_objs, 50)  # Show 50 contacts per page
            page = request.GET.get('page', 1)
            print('page', page)
            pages = paginator.get_page(page)
            results = []
            for page_obj in pages:
                 results.append(page_obj.content())
            cache.put(query_text+str(page), (results, pages))
            logger.info('Data stored in cache')
        except Exception as e:
            print(str(e))
            error_logger.error(str(e))
            error_message = str(e)
            pages = []
            desc = []
    end_time = time.time()

    return render(request, "querymanager/results.html", {
        'results': results,
        "page": pages,
        'error_message': error_message,
        'query': query_text,
        'desc': desc,
        'time_taken': end_time - start_time,
        'name': 'page'
    })

def handle_category_query(request):
    start_time = time.time()
    query_text = request.POST['category']
    logger.info("Running query: {}".format(query_text))
    desc = ('cat_id', 'cat_title')
    error_message = ''
    if cache.has_key(query_text):
        page = request.GET.get('page', 1)
        results, pages = cache.get(query_text + str(page))
    else:
        try:
            cat_objs = Category.objects.raw(query_text)
            paginator = Paginator(cat_objs, 50)  # Show 50 contacts per page
            page = request.GET.get('page', 1)
            print('page', page)
            pages = paginator.get_page(page)
            results = []
            for page_obj in pages:
                results.append(page_obj.content())
            cache.put(query_text + str(page), (results, pages))

        except Exception as e:
            error_logger.error(str(e))
            error_message = str(e)
            results = []
            desc = []
    end_time = time.time()
    return render(request, "querymanager/results.html", {
        'results': results,
        "page": pages,
        'error_message': error_message,
        'query': query_text,
        'desc': desc,
        'time_taken': end_time - start_time,
        'name': 'category'
    })


def handle_pagelinks_query(request):
    start_time = time.time()
    query_text = request.POST['pl']
    logger.info("Running query: {}".format(query_text))
    desc = ('pl_from', 'pl_namespace', 'pl_title', 'pl_from_namespace')
    error_message = ''
    if cache.has_key(query_text):
        page = request.GET.get('page', 1)
        results, pages = cache.get(query_text + str(page))
    else:
        try:
            pl_objs = Pagelinks.objects.raw(query_text)
            paginator = Paginator(pl_objs, 50)  # Show 50 contacts per page
            page = request.GET.get('page', 1)
            print('page', page)
            pages = paginator.get_page(page)
            results = []
            for page_obj in pages:
                results.append(page_obj.content())
            cache.put(query_text + str(page), (results, pages))
        except Exception as e:
            error_logger.error(str(e))
            error_message = str(e)
            results = []
            desc = []

    end_time = time.time()
    return render(request, "querymanager/results.html", {
        'results': results,
        "page": pages,
        'error_message': error_message,
        'query': query_text,
        'desc': desc,
        'time_taken': end_time - start_time,
        'name': 'pl'
    })

def handle_categorylinks_query(request):
    start_time = time.time()
    query_text = request.POST['cl']
    logger.info("Running query: {}".format(query_text))
    desc = ('cl_from', 'self.cl_to', 'self.cl_collation', 'self.cl_sortkey', 'self.cl_timestamp')
    error_message = ''
    if cache.has_key(query_text):
        page = request.GET.get('page', 1)
        results, pages = cache.get(query_text + str(page))
    else:
        try:
            cl_objs = Categorylinks.objects.raw(query_text)
            paginator = Paginator(cl_objs, 50)  # Show 50 contacts per page
            page = request.GET.get('page', 1)
            print('page', page)
            pages = paginator.get_page(page)
            results = []
            for page_obj in pages:
                results.append(page_obj.content())
            cache.put(query_text + str(page), (results, pages))
        except Exception as e:
            error_logger.error(str(e))
            error_message = str(e)
            results = []
            desc = []

    end_time = time.time()
    return render(request, "querymanager/results.html", {
        'results': results,
        "page": pages,
        'error_message': error_message,
        'query': query_text,
        'desc': desc,
        'time_taken': end_time - start_time,
        'name': 'cl'
    })