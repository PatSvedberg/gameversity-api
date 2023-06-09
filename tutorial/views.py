from django.http import Http404
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Tutorial
from .serializers import TutorialSerializer
from gameversity_api.permissions import IsOwnerOrReadOnly


class TutorialList(APIView):
      serializer_class = TutorialSerializer
      permission_classes = [
          permissions.IsAuthenticatedOrReadOnly
      ]
  
      def get(self, request):
          tutorial = Tutorial.objects.all()
          serializer = TutorialSerializer(
              tutorial, many=True, context={'request': request}
          )
          return Response(serializer.data)
  
      def post(self, request):
          serializer = TutorialSerializer(
              data=request.data, context={'request': request}
          )
          if serializer.is_valid():
              serializer.save(owner=request.user)
              return Response(
                  serializer.data, status=status.HTTP_201_CREATED
              )
          return Response(
              serializer.errors, status=status.HTTP_400_BAD_REQUEST
          )


class TutorialDetail(APIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = TutorialSerializer

    def get_object(self, pk):
        try:
            tutorial = Tutorial.objects.get(pk=pk)
            self.check_object_permissions(self.request, tutorial)
            return tutorial
        except Tutorial.DoesNotExist:
            raise Http404
    
    def get(self, request, pk):
        tutorial = self.get_object(pk)
        serializer = TutorialSerializer(
            tutorial, context={'request': request}
        )
        return Response(serializer.data)

    def put(self, request, pk):
        tutorial = self.get_object(pk)
        serializer = TutorialSerializer(
            tutorial, data=request.data, context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        tutorial = self.get_object(pk)
        tutorial.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )