# helper functions for projects
from .models import Project, Tag
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def paginateProjects(request, projects, results):
    # get page number 
    page = request.GET.get('page')
    # results = number of results we want per page
    # pass projects queryset to Paginator w/ results setting the number of projects we'll have per page
    paginator = Paginator(projects, results)
    # checks if page number is passed in
    try:
        # reset projects variable w/ paginated projects
        projects = paginator.page(page)
    # what is done if page is not passed in, such as when first visiting projects pg
    except PageNotAnInteger:
        page = 1
        # reset projects variable w/ paginated projects
        projects = paginator.page(page)
    # checks for empty page when user tries to access pages that don't exist
    except EmptyPage:
        # num_pages gives number of pages and page is set to last actual page
        page = paginator.num_pages
        projects = paginator.page(page)
    # limit the number of page buttons if there are many pages of projects, see a range of pages based on what page user is currently on
    # left limit for page buttons
    leftIndex = (int(page) - 4)
    # check if current page is among the first 4 and make leftIndex 1 to avoid negative pg num
    if leftIndex < 1:
        leftIndex = 1

    # right limit for page buttons
    rightIndex = (int(page) + 5)
    # check if current page is among the last 4 and make rightIndex the last page to avoid negative pg numbers
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1
    # make desired range of pages to display as buttons
    custom_range = range(leftIndex, rightIndex)

    return custom_range, projects

def searchProjects(request):
    # passed into filter on every request, setting to '' in case no data from frontend  so does no ruin filter
    search_query = ''
    # get what is being sent from frontend, extract search_query value sent in
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    # search for Tag is many-to-many not child projects
    tags = Tag.objects.filter(name__icontains=search_query)

    # owner__name__icontains is an example of querying parent object; tags__in checks if tags filter value is in tags for projects; distinct() gives one instance of each specific result ensuring no duplicates
    projects = Project.objects.distinct().filter(Q(title__icontains=search_query) | Q(description__icontains=search_query) | Q(owner__name__icontains=search_query) | Q(tags__in=tags))
    
    return projects, search_query
