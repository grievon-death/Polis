"""
URL configuration for polis project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import include, path
from rest_framework import routers

from base import views as baseView
from user import views as userView


router = routers.DefaultRouter()
router.register(r'type', baseView.TypeViewSet)
router.register(r'theme', baseView.ThemeViewSet)
router.register(r'proposal', baseView.ProposalViewSet)
router.register(r'debate', baseView.DebateViewSet)
router.register(r'profile', userView.ProfileViewSet)


urlpatterns = [
    path('api/', include(router.urls)),
    path('api/comment/', baseView.CommentViewSet.as_view()),
]
