import logging
from django.shortcuts import render
from .models import Page, Category, Pagelinks, Categorylinks
from .cache import cache
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
        results = cache.get(query_text)
    else:
        try:
            logger.info('Data is fetched from database')
            page_objs = Page.objects.raw(query_text)
            results = []
            for page_obj in page_objs:
                results.append(page_obj.content())
            cache.put(query_text, results)
            logger.info('Data stored in cache')
        except Exception as e:
            error_logger.error(str(e))
            error_message = str(e)
            results = []
            desc = []
    end_time = time.time()

    return render(request, "querymanager/results.html", {
        'results': results,
        'error_message': error_message,
        'query': query_text,
        'desc': desc,
        'time_taken': end_time - start_time
    })

def handle_category_query(request):
    start_time = time.time()
    query_text = request.POST['category']
    logger.info("Running query: {}".format(query_text))
    desc = ('cat_id', 'cat_title')
    error_message = ''
    if cache.has_key(query_text):
        results = cache.get(query_text)
    else:
        try:
            cat_objs = Category.objects.raw(query_text)
            results = []
            for cat_obj in cat_objs:
                results.append(cat_obj.content())
            cache.put(query_text, results)
        except Exception as e:
            error_logger.error(str(e))
            error_message = str(e)
            results = []
            desc = []
    end_time = time.time()
    return render(request, "querymanager/results.html", {
        'results': results,
        'error_message': error_message,
        'query': query_text,
        'desc': desc,
        'time_taken': end_time - start_time
    })


def handle_pagelinks_query(request):
    start_time = time.time()
    query_text = request.POST['pl']
    logger.info("Running query: {}".format(query_text))
    desc = ('pl_from', 'pl_namespace', 'pl_title', 'pl_from_namespace')
    error_message = ''
    if cache.has_key(query_text):
        results = cache.get(query_text)
    else:
        try:
            pl_objs = Pagelinks.objects.raw(query_text)
            results = []
            for pl_obj in pl_objs:
                results.append(pl_obj.content())
            cache.put(query_text, results)
        except Exception as e:
            error_logger.error(str(e))
            error_message = str(e)
            results = []
            desc = []

    end_time = time.time()
    return render(request, "querymanager/results.html", {
        'results': results,
        'error_message': error_message,
        'query': query_text,
        'desc': desc,
        'time_taken': end_time - start_time
    })

def handle_categorylinks_query(request):
    start_time = time.time()
    query_text = request.POST['cl']
    logger.info("Running query: {}".format(query_text))
    desc = ('cl_from', 'self.cl_to', 'self.cl_collation', 'self.cl_sortkey', 'self.cl_timestamp')
    error_message = ''
    if cache.has_key(query_text):
        results = cache.get(query_text)
    else:
        try:
            cl_objs = Categorylinks.objects.raw(query_text)
            results = []
            for cl_obj in cl_objs:
                results.append(cl_obj.content())
            cache.put(query_text, results)
        except Exception as e:
            error_logger.error(str(e))
            error_message = str(e)
            results = []
            desc = []

    end_time = time.time()
    return render(request, "querymanager/results.html", {
        'results': results,
        'error_message': error_message,
        'query': query_text,
        'desc': desc,
        'time_taken': end_time - start_time
    })