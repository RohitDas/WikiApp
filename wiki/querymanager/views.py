import time
import logging
import re
from django.shortcuts import render
from django.db import connection
from .handlers import handle_category_query, handle_page_query, handle_pagelinks_query, handle_categorylinks_query
from .cache import cache
from .query_stats import query_stats

BATCH = 25
logger = logging.getLogger("info")
error_logger = logging.getLogger("django_error")
disallowed_queries = ['update', 'insert', 'alter']
r = re.compile(r"limit|describe|update|insert", re.IGNORECASE)


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

def general_results(request):
    start_time = time.time()
    cursor = connection.cursor()
    is_limiting_query = False
    try:
        original_query = request.POST['query'].strip().strip(";")
        logger.info("Running query: {}".format(original_query))
        desc = None
        if cache.has_key(original_query):
            logger.info("Data fetched from cache")
            page = request.GET.get('page', 1)
            desc, results = cache.get(original_query + str(page))
        else:
            logger.info("Data fetched from database")
            page = request.GET.get('page', 1)
            #Handling of limiting and original query
            if not r.findall(original_query):
                query = original_query + " limit {} offset {} ;".format(BATCH, (int(page) - 1)*BATCH)
            else:
                query = original_query
                is_limiting_query = True
            print(query)
            cursor.execute(query)
            objs = cursor.fetchall()
            desc = [desc[0]for desc in cursor.description]
            #pages = g_paginator.get_page(page)
            results = []
            for page_obj in objs:
                results.append(page_obj)
            cache.put(query + str(page), (desc, results))
            logger.info('Data stored in cache')
            logger.info("Data is cached")
        end_time = time.time()
        return render(request, "querymanager/results_2.html", {
            'results': results,
            'error_message': '',
            'query': original_query,
            'prev_page': None if page == 1 else int(page) - 1,
            'next_page': int(page)+1 if (len(results) == BATCH and not is_limiting_query) else None,
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
            query_1 = """select p.page_id, p.page_title from categorylinks 
                         as c,page as p  where c.cl_to = "{}" and c.cl_from = p.page_id
                      """.format(category)
            cursor.execute(query_1)

            max_outdated = None
            for val in cursor:
                print(val)
                #get ts of current val.
                ts_query = """select max(ts) from wiki_meta where id = {} group by id""".format(val[0])
                cursor.execute(ts_query)
                try:
                    ts_of_category_page = cursor.fetchall()[0][0]
                except:
                    continue
                pagelinks_query = """ select page_id from pagelinks, page  where pl_from = {} and pl_title = page_title""".format(val[0])
                cursor.execute(pagelinks_query)
                pagelinks_ids = [val[0] for val in cursor.fetchall()]
                if not pagelinks_ids:
                    continue
                else:
                    ts_query = """select id, max(ts) from wiki_meta where id in {} group by id""".format(tuple(pagelinks_ids))
                    cursor.execute(ts_query)
                    referree_list_max = sorted([(val[0], val[1] - ts_of_category_page) for val in cursor.fetchall()], key=lambda k: k[1], reverse=True)[0]

                if max_outdated is None or max_outdated[2] < referree_list_max[1]:
                    max_outdated = (val[0], referree_list_max[0], referree_list_max[1])
                print("TS: ", max_outdated)
            print("MAX", max_outdated)
            most_outdated_page = max_outdated
            print(most_outdated_page)
            cache.put(category, most_outdated_page)

        return render(request, "querymanager/outdated_result.html", {
            'category': category,
            'error_message': None,
            'desc': ('page_id', 'difference', 'time_taken(secs)'),
            'results': (most_outdated_page[0], most_outdated_page[2], time.time() - start_time)})

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