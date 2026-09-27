from rest_framework.viewsets import ModelViewSet

from accounts.models import CustomUser
from accounts.serializers import CreateCustomUserSerializer, ListCustomUserSerializer


# Create your views here.
class CustomUserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CreateCustomUserSerializer

    def get_serializer_class(self):
        if(self.action == "retrieve"):
            return ListCustomUserSerializer

        return super().get_serializer_class()