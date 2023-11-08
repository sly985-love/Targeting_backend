from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("soldier", views.SoldierModelViewSet, basename="soldier")
router.register("instructor", views.InstructorModelViewSet, basename="instructor")
router.register("target", views.TargetModelViewSet, basename="target")
router.register("achievement", views.AchievementModelViewSet, basename="achievement")
router.register('photo', views.PhotoModelViewSet, basename='photo')
router.register('select', views.SelectTargetModelViewSet, basename='select')
router.register('goshooting', views.GoshootingModelViewSet, basename='goshooting')
urlpatterns = [
                  # path("home/", views.HomeView.as_view()),
                  path('user/create/', views.CrerateUserView.as_view(), name='create'),
                  path('user/me/', views.ManageUserView.as_view(), name='me'),
                  path('user/list/', views.ListUserView.as_view(), name='list'),
                  path('user/token/', views.CreateTokenView.as_view(), name='token'),
              ] + router.urls
