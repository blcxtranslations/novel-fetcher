#!/usr/bin/python
# -*- coding: utf-8 -*-


def send_instapaper(service, link, folder_id=None, mercury_api=None):
    # Circular dependency requires that we only import this
    # And only import it inside this function
    ############################################################
    from utilities.utility_common import get_page
    from utilities.utility_common import print_colour
    import json
    ############################################################

    if mercury_api:
        page = get_page('https://mercury.postlight.com/parser?url=' + link, mercury_api)
        if page:
            page = json.loads(page)
            success, msg = service.bookmark_add(link, folder_id, page['content'])
        else:
            success, msg = service.bookmark_add(link, folder_id)
    else:
        success, msg = service.bookmark_add(link, folder_id)

    if success:
        print_colour('Instapaper', 'Success', link, 'success')
        return True

    print_colour('Instapaper', 'Failed', link, 'error')
    print_colour('Instapaper', 'Failed', msg, 'error')
    return False
