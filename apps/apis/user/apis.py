from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.apis.user.serializers import LoginInSerializer, UserSerializer
from apps.user.models import User   
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated


class AuthView(APIView):
    serializer_class = LoginInSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get("user")
        if user:
            return Response(self.serializer_class(user).data, status=status.HTTP_201_CREATED)
        return Response({"detail": "Code sent to the email successfully"}, status=status.HTTP_200_OK)


class UserModelViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ["get", "put", "patch", "delete"]

    def get_queryset(self):
        return self.queryset.filter(id=self.request.user.id)
    