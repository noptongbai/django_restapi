from django.conf.urls import url, include
from mgpAPI.views.user import UserList, MyUserList

urlpatterns = [
    url(r'^$', UserList.as_view()),
    url(r'^mine/$', MyUserList.as_view()),

]
