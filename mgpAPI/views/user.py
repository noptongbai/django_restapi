from mgpAPI.serializers.user_serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework import generics
from mgpAPI.pages.page import StandardResultsSetPagination


class UserList(generics.ListAPIView):
    pagination_class = StandardResultsSetPagination
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        if self.request.GET.get("q"):
            return User.objects.filter(groups__name=self.request.GET.get("q"))
        return User.objects.all()


class MyUserList(generics.ListAPIView):
    pagination_class = StandardResultsSetPagination
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)
