# from django.http import JsonResponse #to return python data as JSON data # removed after adding api decarotor
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .serializers import ProjectSerializer
from projects.models import Project, Review

# list specifies what methods function can take (only GET in this case)
@api_view(['GET'])
# gives all url paths or routes inside of api
def getRoutes(request):
    # list dictionaries that will be turned into javascript objects 
    # specifying method that a specific route takes
    routes = [
        # returns a list of project objects
        {'GET': 'api/projects'}, 
        # returns a single project object
        {'GET': 'api/projects/id'}, 
        # passes in vote
        {'POST': 'api/projects/id/vote'}, 

        # built-in class to generate a token for user login
        {'POST': 'api/users/token'}, 
        # built-in class to generate a new json web token after it expires
        {'POST': 'api/users/token/refresh'}, 
    ]
    # return python data as json data
    # safe parameter allows us to return back something other than
    # a python dictionary, since we're sending a list, set safe to False
    # this is saying it's ok to turn any data into JSON data
    # return JsonResponse(routes, safe=False)
    # can use this instead of above b/c function is now wrapped in an api decarator
    return Response(routes)

# list specifies what methods function can take (only GET in this case)
@api_view(['GET'])
# requires authentication for user to get projects
# @permission_classes([IsAuthenticated])
def getProjects(request):
    projects = Project.objects.all()
    # takes queryset and turns it into json data
    # many = True b/c serializing multiple objects
    serializer = ProjectSerializer(projects, many=True)
    # .data used to get data out of serializer which is a class
    return Response(serializer.data)

# list specifies what methods function can take (only GET in this case)
@api_view(['GET'])
# requires authentication for user to get projects
# @permission_classes([IsAuthenticated])
def getProject(request, pk):
    project = Project.objects.get(id=pk)
    # takes queryset and turns it into json data
    # many = False b/c not serializing multiple objects
    serializer = ProjectSerializer(project, many=False)
    # .data used to get data out of serializer which is a class
    return Response(serializer.data)

# list specifies what methods function can take (only POST in this case)
@api_view(['POST'])
# requires authentication for user to get projects
@permission_classes([IsAuthenticated])
# takes in post request and modifies a project vote
def projectVote(request, pk):
    project = Project.objects.get(id=pk)
    user = request.user.profile
    # property available b/c of api decorator
    data = request.data
    # checks if object exists already and gets that instance
    # if it does and creates one if not
    # created will be true or false
    review, created = Review.objects.get_or_create(
        owner=user, 
        project=project,
        )
    # getting vote value and setting it
    review.value = data['value']
    # update project vote count
    review.save()
    # because used @property decorator in models do not have to call as
    # traditional function
    project.getVoteCount

    # takes queryset and turns it into json data
    # many = False b/c not serializing multiple objects
    serializer = ProjectSerializer(project, many=False)
    # .data used to get data out of serializer which is a class
    return Response(serializer.data)