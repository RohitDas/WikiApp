import xml.etree.ElementTree as etree
import time
import wikipediaapi
import re
import json

WIKI_PATH = "aawiki-20181101-pages-meta-current.xml"
OUTPUT_FILE = "db_info.dump"

def hms_string(sec_elapsed):
    """
    Nicely formatted time string
    """
    h = int(sec_elapsed / (60 * 60))
    m = int((sec_elapsed % (60 * 60)) / 60)
    s = sec_elapsed % 60
    return "{}:{:>02}:{:>05.2f}".format(h, m, s)


def strip_tag_name(t):
    idx = t.rfind("}")
    if idx != -1:
        t = t[idx + 1:]
    return t

def process_categories(category_map):
    """
    :param category_map:
    :return: List of categories
    """
    categories = []
    regx = re.compile(r'Category:(.*)')
    for category in category_map:
        categories.append((regx.match(category).group(1).strip().lower()))
    return categories

def process_links(link_map):
    """
    :param link_map:
    :return: List of Links
    """
    return [link.strip().lower() for link in link_map]

totalCount = 0
articleCount = 0
redirectCount = 0
templateCount = 0
title = None
start_time = time.time()

wiki_en = wikipediaapi.Wikipedia('en')

with open(OUTPUT_FILE, "w") as fp:

    for event, elem in etree.iterparse(WIKI_PATH, events=('start', 'end')):
        tname = strip_tag_name(elem.tag)

        if event == 'start':
            if tname == 'page':
                title = ''
                id = -1
                redirect = ''
                inrevision = False
                ns = 0
            elif tname == 'revision':
                # Do not pick up on revision id's
                inrevision = True
        else:
            if tname == 'title':
                title = elem.text
            elif tname == 'id' and not inrevision:
                id = int(elem.text)
            elif tname == 'id' and inrevision:
                rev_id = elem.text
            elif tname == 'timestamp' and inrevision:
                timestamp = elem.text
            elif tname == 'redirect':
                redirect = elem.attrib['title']
            elif tname == 'ns':
                ns = int(elem.text)
            elif tname == 'revision':
                inrevision = False
            elif tname == 'page':
                totalCount += 1

                print(id, rev_id, title, "|", redirect, timestamp)
                try:
                    page = wiki_en.page(title)
                    if page.exists():
                        categories = process_categories(page.categories)
                        links = process_links(page.links)
                except Exception as e:
                    print("Error occured: ", str(e))
                    print("Reconnecting...")
                    wiki_en = wikipediaapi.Wikipedia('en')
                    print("Connected..")
                    links, categories = None, None

                #Other info on info pages.
                store_page_info_dicts = {
                    'id': id,
                    'revId': rev_id,
                    'title': title,
                    'redirect': redirect,
                    'timestamp': timestamp,
                    'links': links if links else None,
                    'categories': categories if categories else None
                }

                fp.write(json.dumps(store_page_info_dicts))
                fp.write("\n")

                if totalCount % 50 == 0:
                    print("Time Elapsed: ", hms_string(time.time() - start_time), "totalCount: ", totalCount)

            elem.clear()

elapsed_time = time.time() - start_time
print("Total pages: {:,}".format(totalCount))
print("Template pages: {:,}".format(templateCount))
print("Article pages: {:,}".format(articleCount))
print("Redirect pages: {:,}".format(redirectCount))
print("Elapsed time: {}".format(hms_string(elapsed_time)))
