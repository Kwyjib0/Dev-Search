from rest_framework import serializers
from projects.models import Project, Tag, Review
from users.models import Profile

# model serializer converts profile to json object
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

# model serializer converts profile to json object
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

# model serializer converts tag to json object
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


# model serializer converts project to json object
class ProjectSerializer(serializers.ModelSerializer):
    # set owner to override what is normally returned
    # so that get profile of owner object instance
    owner = ProfileSerializer(many=False)
    # set tags to override what is normally returned
    # so that get profile of tag object instances
    tags = TagSerializer(many=True)
    # add review attribute just to serializer
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = '__all__'

    # serializer methods start with get
    # self refers to reviews serializer class
    # obj is the object being serialized (project)
    def get_reviews(self, obj):
        reviews = obj.review_set.all()
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data