import time
import logging
from django.shortcuts import render
from django.db import connection
from .handlers import handle_category_query, handle_page_query, handle_pagelinks_query
from .cache import cache

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


def general_results(request):
    cursor = connection.cursor()
    try:
        query = request.POST['query']
        if cache.has_key(query):
            logger.info("Data fetched from cache")
            desc, results = cache.get(query)
        else:
            logger.info("Data fetched from database")
            cursor.execute(query)
            results = cursor.fetchall()
            desc = [desc[0]for desc in cursor.description]
            logger.info("Data is cached")
            cache.put(query, (desc, results))
        return render(request, "querymanager/results.html", {
            'results': results,
            'error_message': '',
            'query': query,
            'desc': desc
        })
    except Exception as e:
        error_logger.error(str(e))
        return render(request, "querymanager/results.html", {
            'results': {},
            'error_message': str(e),
            'query': query,
            'desc': desc
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
            query_1 = """select cl_from, MAX(t7.ts_page) from (select cl_from, page_id, ts as ts_page from (select cl_from, page_id from (select * from categorylinks as t1 join pagelinks as t2 on t1.cl_from = t2.pl_from where t1.cl_to = "{}") as t3, page as t4 where t3.pl_title = t4.page_title) as t5 join wiki_meta as t6 on t5.page_id = t6.wid) as t7 group by t7.cl_from;""".format(category)
            cursor.execute(query_1)
            results_1 = cursor.fetchall()

            # The second query provides the timestamp of the last modification time of the pages belonging to a category.
            query_2 = """select cl_from, MAX(ts) from (select cl_from, ts from (select cl_from from categorylinks as t1 join pagelinks as t2 on t1.cl_from = t2.pl_from where t1.cl_to = "{}") as t3 join wiki_meta as t4 where t3.cl_from = t4.wid) as t5 group by t5.cl_from;""".format(category)
            cursor.execute(query_2)
            results_2 = cursor.fetchall()

            page_id_to_timestamp = {}
            for result in results_2:
                page_id_to_timestamp.update({
                    result[0]: result[1]
                })

            for result in results_1:
                if result[0]  in page_id_to_timestamp:
                    page_id_to_timestamp.update({
                        result[0]: result[1] - page_id_to_timestamp[result[0]]
                    })
            most_outdated_page = sorted(page_id_to_timestamp.items(), key=lambda k: k[1], reverse=True)[0]
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

