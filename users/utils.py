
# helper functions for users
from django.db.models import Q
from .models import Profile, Skill
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def paginateProfiles(request, profiles, results):
    # get page number 
    page = request.GET.get('page')
    # results = number of results we want per page
    # pass profiles queryset to Paginator w/ results setting the number of profiles we'll have per page
    paginator = Paginator(profiles, results)
    # checks if page number is passed in
    try:
        # reset profiles variable w/ paginated profiles
        profiles = paginator.page(page)
    # what is done if page is not passed in, such as when first visiting profiles pg
    except PageNotAnInteger:
        page = 1
        # reset profiles variable w/ paginated profiles
        profiles = paginator.page(page)
    # checks for empty page when user tries to access pages that don't exist
    except EmptyPage:
        # num_pages gives number of pages and page is set to last actual page
        page = paginator.num_pages
        profiles = paginator.page(page)
    # limit the number of page buttons if there are many pages of profiles, see a range of pages based on what page user is currently on
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

    return custom_range, profiles

def searchProfiles(request):
    # passed into filter on every request, setting to '' in case no data from frontend  so does no ruin filter
    search_query = ''
    # get what is being sent from frontend, extract search_query value sent in
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    # print('SEARCH:', search_query)
    #name__icontains will search for partial words/phrases name__iexact would make sure name matches exactly...case, etc., 
    skills = Skill.objects.filter(name__icontains=search_query)
    # multiple parameters for multiple search by options, must import Q to search using comparison, OR = |, otherwise functions as an AND search, AND would = &; skill__in allows filtering by child object; distinct eliminate duplicates caused by repeating the profile by the numbers of skills listed for that account, b/c query spans multiple tables
    profiles = Profile.objects.distinct().filter(Q(name__icontains=search_query) | Q(headline__icontains=search_query) | Q(skill__in=skills))

    return profiles, search_query