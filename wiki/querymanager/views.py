import time
import logging
from django.shortcuts import render
from django.db import connection
from .handlers import handle_category_query, handle_page_query, handle_pagelinks_query, handle_categorylinks_query
from .cache import cache
from .query_stats import query_stats
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

logger = logging.getLogger("info")
error_logger = logging.getLogger("django_error")

def index(request):
    return render(request, "querymanager/index.html", {})

def query(request):
    """
    View to handle the query page
    """
    logger.info("Received request {}".format(str(request)))
    return render(request, 'querymanager/query.html', {})


def general_query(request):
    logger.info("Received request {}".format(str(request)))
    return render(request, 'querymanager/general_query.html', {})


def results(request):
    logger.info("Received request {}".format(str(request)))
    if 'page' in request.POST:
        return handle_page_query(request)
    elif 'category' in request.POST:
        return handle_category_query(request)
    elif 'pl' in request.POST:
        return handle_pagelinks_query(request)
    elif 'cl' in request.POST:
        return handle_categorylinks_query(request)

g_paginator, g_desc= None, None

def general_results(request):
    global  g_paginator, g_desc
    start_time = time.time()
    cursor = connection.cursor()
    try:
        query = request.POST['query']
        logger.info("Running query: {}".format(query))
        if cache.has_key(query):
            logger.info("Data fetched from cache")
            page = request.GET.get('page', 1)
            desc, results, pages = cache.get(query + str(page))
        else:
            logger.info("Data fetched from database")
            page = request.GET.get('page', 1)
            if page == 1:
                cursor.execute(query)
                objs = cursor.fetchall()
                g_desc = [desc[0]for desc in cursor.description]
                g_paginator = Paginator(objs, 50)  # Show 50 contacts per page

            print('page', page)
            pages = g_paginator.get_page(page)
            results = []
            for page_obj in pages:
                results.append(page_obj)
            cache.put(query + str(page), (g_desc, results, pages))
            logger.info('Data stored in cache')
            logger.info("Data is cached")
            desc = g_desc
        end_time = time.time()
        return render(request, "querymanager/results.html", {
            'results': results,
            'error_message': '',
            'query': query,
            'page': pages,
            'desc': desc,
            'time_taken': end_time - start_time,
            'name': 'query'
        })
    except Exception as e:
        error_logger.error(str(e))
        end_time = time.time()
        return render(request, "querymanager/results.html", {
            'results': {},
            'error_message': str(e),
            'query': query,
            'desc': desc,
            'time_taken': end_time - start_time
        })


def category_view(request):
    return render(request, "querymanager/outdated.html", {})


def get_most_outdated(request):
    """
    This view handles the request which provides for each category
    supplied by the user what is the most outdated page belonging to a
    category.
    """
    start_time = time.time()
    category = request.POST['category']
    cursor = connection.cursor()
    try:
        if cache.has_key(category):
            most_outdated_page = cache.get(category)
        else:
            # The first query provides the timestamp of the maximum last modification time of the pages referred to by the page belonging to a category.
            query = """select distinct v2.pl_from as page_id, v2.pl_title as title,  max(w.ts - w1.ts) as diff from (select pl.pl_from, pl.pl_title, p.page_id from pagelinks as pl, page as p, (select p.page_id, p.page_title from categorylinks 
            as c,page as p  where c.cl_to = "{}" and c.cl_from = p.page_id) as v1 where v1.page_id = pl.pl_from and p.page_title = pl.pl_title) as v2, wiki_meta as w, wiki_meta as w1  where v2.pl_from = w.id and v2.page_id = w1.id and v2.pl_from != v2.page_id 
            group by v2.pl_from, v2.pl_title order by diff DESC limit 1;""".format(category)
            print(query)
            cursor.execute(query)
            most_outdated_page = cursor.fetchall()[0]
            print(most_outdated_page)
            cache.put(category, most_outdated_page)

        return render(request, "querymanager/outdated_result.html", {
            'category': category,
            'error_message': None,
            'desc': ('page_id', 'difference', 'time_taken(secs)'),
            'results': (most_outdated_page[0], most_outdated_page[1], time.time() - start_time)})

    except Exception as e:
        error_logger.error(str(e))
        render(request, "querymanager/outdated_result.html", {
            'category': category,
            'error_message': str(e),
            'desc': (),
            'results': ()
        })

def recent(request):
    recent = query_stats.get_latest()
    return render(request, "querymanager/recent.html", {
        'recent': recent
    })