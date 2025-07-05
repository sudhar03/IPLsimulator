from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.apis.user.serializers import LoginInSerializer
from apps.user.models import User   



class AuthView(APIView):
    serializer_class = LoginInSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get("user")
        if user:
            return Response(self.serializer_class(user).data, status=status.HTTP_201_CREATED)
        return Response({"detail": "Code sent to the email successfully"}, status=status.HTTP_200_OK)
    