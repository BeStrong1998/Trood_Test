from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),

    #path('users/', views.UserList.as_view({"get": "list"})),
    #path('users/<int:pk>/', views.UserDetail.as_view({"get": "list"})),
]

#urlpatterns = format_suffix_patterns(urlpatterns)