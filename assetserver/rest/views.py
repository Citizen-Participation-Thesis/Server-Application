from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
from bundler.models import Project
from rest_framework.decorators import api_view
from .serializers import ConfigSerializer

from .serializers import ProjectSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().order_by("-id")
    serializer_class = ProjectSerializer
    permission_classes = [permissions.AllowAny]


@api_view(['POST'])
def update_config(request):
    if request.method == 'POST':
        pass
