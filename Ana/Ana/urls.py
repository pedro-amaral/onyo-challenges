from Ana import views
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'bets', views.BetTicketViewSet)
router.register(r'users', views.UserViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
