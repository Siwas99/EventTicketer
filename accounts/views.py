from django.shortcuts import redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from accounts.models import CustomUser
from accounts.serializers import CreateCustomUserSerializer, ListCustomUserSerializer, RegisterCustomUserSerializer


# Create your views here.
class CustomUserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CreateCustomUserSerializer
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if(self.action == "retrieve"):
            return ListCustomUserSerializer

        return super().get_serializer_class()

@api_view(['POST'])
@permission_classes([AllowAny])
def register_custom_user_view(request):
    serializer = RegisterCustomUserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return redirect("rest_framework:login")
    return Response(serializer.errors, status=400)

