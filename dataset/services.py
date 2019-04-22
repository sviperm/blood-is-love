def page_navigation(page, pages_nav_num):
    page_num = page.number
    max_page = page.paginator.num_pages

    result = {
        'pages': [],
    }

    if (max_page > pages_nav_num):
        start_page = page_num - int(pages_nav_num / 2)
        end_page = page_num + int(pages_nav_num / 2)

        if (start_page < 1):
            start_page = 1
            end_page = pages_nav_num
        elif (end_page > max_page):
            start_page = max_page - pages_nav_num + 1
            end_page = max_page

        result['first'] = 1
        result['last'] = max_page

    else:
        start_page = 1
        end_page = max_page

    if page.has_previous():
        result['previous'] = page.number - 1

    if page.has_next():
        result['next'] = page.number + 1

    for i in range(start_page, end_page + 1):
        result['pages'].append(i)

    return result
