def page_navigation(page_object, pages_num):
    page = page_object.number
    result = {
        'pages': {},
    }
    start_page = page - int(pages_num/2)
    end_page = page + int(pages_num / 2)

    if (start_page > 0) and (end_page < page_object.paginator.num_pages):
        pass
    elif (start_page < 0):
        nf

    for i in range(start_page, end_page + 1):
        pass

    if page_object.has_previous():
        result['previous'] = page_object.number - 1

    if page_object.has_next():
        result['next'] = page_object.number + 1

    if page_object.has_other_pages():
        result['first'] = 1
        result['last'] = page_object.paginator.num_pages
