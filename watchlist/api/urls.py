from django.urls import path,include
from watchlist.api.views import WatchListAV,Review_list,ReviewUser,WatchListDetail,StreamPlatformVS,StreamPlatformDetail,ReviewList,ReviewDetail,CreateReview
from rest_framework.routers import DefaultRouter
router=DefaultRouter()
router.register('stream',StreamPlatformVS,basename='stream')

urlpatterns=[path('list1/',WatchListAV.as_view(),name='movie-list'),
             path('list/<int:pk>/',WatchListDetail.as_view(),name='movie_detail'),
            # path('stream/',Stream_platform.as_view(),name='streamplatform'),
             path('',include(router.urls),),
             path('list1/<str:pk>/review/',ReviewUser.as_view(),name='Review'),
              path('list1/reviews/',Review_list.as_view(),name='Reviews'),
             path('review/<int:pk>/',ReviewDetail.as_view(),name='review_detail'),
             path('movie/<int:pk>/createreview/',CreateReview.as_view(),name='review_detail'),
            # path('stream/<int:pk>/movies/',Stream_platform.as_view(),name='Stream_platform'),
            ]
            