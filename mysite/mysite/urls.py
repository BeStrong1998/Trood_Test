"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from polls import views


router = routers.DefaultRouter()
"""router.register(r'api/v1/choice', ChoiceViewSet, basename='oleg')
print(router.urls)"""
router.register(r'group', views.GroupViewset)
router.register(r'users', views.UserViewset)
router.register(r'question', views.QuestionViewSet)
router.register(r'choice', views.ChoiceViewSet)
router.register(r'survey', views.SurveyViewSet)


urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api-auth/', include(
        'rest_framework.urls', namespace='rest_framework')),
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),

    path('api/', views.api), #подключаем маршрутизатор для декоратора @api_view(api)
    #path('users/', views.GroupViewset.as_view()), #подключаем generics
]