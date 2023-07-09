from bs4 import BeautifulSoup, NavigableString
from dotenv import load_dotenv
import os
import requests
import csv

def WriteToCsv(filename, content):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(content)

def ExtractTableInformation(text, table_id=None):

    page_obj = BeautifulSoup(text, 'html.parser')
    table_list = []

    if table_id:
        table = page_obj.css.select(f"#{table_id}")
    else:
        table = page_obj.find('table')

    if table == None or len(table) == 0:
        return ([], False)

    tbody = table.tbody

    if tbody:
        rows = tbody.children
    else:
        rows = table.children
    
    for row in rows:
        if isinstance(row, NavigableString):
            continue

        row_data = []
        for cell in row.children:
            if isinstance(cell, NavigableString):
                continue

            row_data.append(cell.get_text().strip())

        table_list.append(row_data)

    #print(table_list)

    return (table_list, True)

def ScrapeWebsite(options):
    """
    options: dict, contains url, table id, pagination, pages
    pages: 1 is all, for 0 refer to page_num
    """

    base_url = options.get('url')
    table_id = options.get('table_id')
    url_pagination = options.get('url_pagination')
    page_num = options.get('page_num')
    pages = options.get('pages')

    final_table = []

    if pages:
        page_nums = range(1, 999999)
    else:
        page_nums = range(1, page_num)


    #page_nums = range(1, 4)

    for page_n in page_nums:
        
        parsed_url = f"{base_url}?{url_pagination}={page_n}"
        print(parsed_url)

        page = requests.get(parsed_url)

        result, status = ExtractTableInformation(page.text, table_id)

        if not status:
            break
        
        final_table += result

    #print(final_table)
    return final_table


if __name__ == "__main__":

    """
    USING ENVIRONMENT VARIABLES TO HIDE URL USED FOR TESTING
    """
    load_dotenv()
    url = os.getenv('URL')

    options = {
        'url': url,
        'url_pagination': 'page',
        'pages': 1,
        'page_num': 10
    }

    table = ScrapeWebsite(options)
    WriteToCsv('output.csv', table)