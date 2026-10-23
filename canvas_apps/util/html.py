"""
Utilities to work with html
"""

from canvasapi.canvas import Canvas
from canvasapi.course import Course

from bs4 import BeautifulSoup
from bs4.element import Tag

def cleanse(html:str) -> str:
    """Cleanse the Canvas HTML strings of script and link tags.

    Parameters
    ----------
    html : str
        The HTML string from Canvas

    Returns
    -------
    str
        The cleansed version of the HTML string
    """
    soup = BeautifulSoup(html, 'html.parser')

    for tag in soup.find_all('link') + soup.find_all('script'):
        tag.decompose()

    return str(soup)

def deTeX(html:str) -> str:
    soup = BeautifulSoup(html, 'html.parser')

    for tag in soup.find_all('img', class_="equation_image"):
        tex = tag.get('alt')[7:]
        tag.replace_with(f'${tex}$')

    return str(soup)

def make_announcement_link(canvas:Canvas, course:Course, announcement_id:int) -> Tag:
    """Creates a Beautiful Soup <a> tag for a Canvas announcement from the announcement_id

    Parameters
    ----------
    announcement_id : int
        The ID of the announcement to be linked.

    Returns
    -------
    Tag
        A bs4 <a> Tag that matches the Canvas pattern for an announcement
    """
    from canvas_apps.util.data import load_announcements

    announcements = load_announcements(canvas, course)
    announcement = announcements[str(announcement_id)]

    soup = BeautifulSoup('', 'html.parser')
    tag = soup.new_tag('a')
    tag['title'] = announcement['title']
    tag['href'] = f'/courses/{course.id}/discussion_topics/{announcement_id}'
    tag['data-course-type'] = 'announcements'
    tag.string = announcement['title']

    return tag

def make_assignment_link(course:Course, assignment_id:int) -> Tag:
    """Creates a Beautiful Soup <a> tag for a Canvas assignment from the assignment_id

    Parameters
    ----------
    assignment_id : int
        The ID of the assignment to be linked.

    Returns
    -------
    Tag
        A bs4 <a> Tag that matches the Canvas pattern for an assignment
    """
    from canvas_apps.util.data import load_assignments

    assignments = load_assignments(course)
    assignment = assignments[str(assignment_id)]

    soup = BeautifulSoup('', 'html.parser')
    tag = soup.new_tag('a')
    tag['title'] = assignment['name']
    tag['href'] = f'/courses/{course.id}/assignments/{assignment_id}'
    tag['data-course-type'] = 'assignments'
    tag['data-published'] = assignment['published']
    tag.string = assignment['name']

    return tag

def make_file_link(course:Course, file_id:int) -> Tag:
    """Creates a Beautiful Soup <a> tag for a Canvas file from the file_id

    Parameters
    ----------
    file_id : int
        The ID of the file to be linked.

    Returns
    -------
    Tag
        A bs4 <a> Tag that matches the Canvas pattern for a file
    """
    from canvas_apps.util.data import load_files

    files = load_files(course)
    file = files[str(file_id)]

    soup = BeautifulSoup('', 'html.parser')
    tag = soup.new_tag('a')
    tag['class'] = 'instructure_file_link instructure_scribd_file inline_disabled'
    tag['title'] = file['filename']
    tag['href'] = f'/courses/{course.id}/files/{file_id}?wrap=1'
    tag['target'] = '_blank'
    tag['rel'] = 'noopener'
    tag.string = file['display_name']

    return tag

def make_module_link(course:Course, module_id:int) -> Tag:
    """Creates a Beautiful Soup <a> tag for a Canvas module from the module_id

    Parameters
    ----------
    module_id : int
        The ID of the module to be linked.

    Returns
    -------
    Tag
        A bs4 <a> Tag that matches the Canvas pattern for a module
    """
    from canvas_apps.util.data import load_modules

    modules = load_modules(course)
    module = modules[str(module_id)]

    soup = BeautifulSoup('', 'html.parser')
    tag = soup.new_tag('a')
    tag['title'] = module['name']
    tag['href'] = f'/courses/{course.id}/modules/{module_id}'
    tag['data-course-type'] = 'modules'
    tag['data-published'] = module['published']
    tag.string = module['name']

    return tag

def make_page_link(course:Course, page_id:int) -> Tag:
    """Creates a Beautiful Soup <a> tag for a Canvas page from the page_id

    Parameters
    ----------
    page_id : int
        The ID of the page to be linked.

    Returns
    -------
    Tag
        A bs4 <a> Tag that matches the Canvas pattern for a page
    """
    from canvas_apps.util.data import load_pages

    pages = load_pages(course)
    page = pages[str(page_id)]

    soup = BeautifulSoup('', 'html.parser')
    tag = soup.new_tag('a')
    tag['title'] = page['title']
    tag['href'] = f'/courses/{course.id}/pages/{page['url']}'
    tag['data-course-type'] = 'wikiPages'
    tag['data-published'] = page['published']
    tag.string = page['title']

    return tag
