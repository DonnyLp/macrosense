from django.contrib.auth.models import Group
from user.models import User
from rest_framework import permissions, viewsets


from api.serializers import GroupSerializer, UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    """_summary_
    API endpoint that allows users to be viewed/edited
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class GroupViewSet(viewsets.ModelViewSet):
    """_summary_
    API endpoint that allows groups to be viewed/edited
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
    

#model instance testing


