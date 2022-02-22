from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views 

urlpatterns = [
    path('', views.index, name='INDEX'),
    #path('', views.home, name='CARPOOLING'),
    path('index', views.index, name='INDEX'),
    path('search/', views.search, name='SEARCH'),
    path('share/', views.share, name='SHARE'),
    path('trips/', views.trips, name='TRIPS'),
    path('login/', views.login, name='LOGIN'),
    path('logout/', views.logout, name='LOGOUT'),
    path('signup/', views.signup, name='SIGNUP'),
    path('share_form_submission/', views.share_form_submission, name='SHARESUB'),
    path('search_results/', views.search_results, name = 'SEARCHRES'),
    path(r'request_ride/(?P<username>\w{0,50})/(?P<id>[0-9]+)/(?P<spots>[0-9]+)/$', views.request_ride, name = 'REQRID'),
    path(r'accept/(?P<id>[0-9]+)/$', views.ride_status_accept, name = 'ACCEPT'),
    path(r'reject/(?P<id>[0-9]+)/$', views.ride_status_reject, name = 'REJECT'),
    path('profile/', views.user_profiles, name = 'PROFILE'),
    path(r'del_trip_pro/(?P<id>[0-9]+)/$', views.del_trip_pro, name = 'DELTRP'),
    path('edit_profile', views.edit_profile, name = 'EDITPRO'),
    path('edit_profile_form', views.edit_profile_form, name = 'EDITPROFO'),
    path('user_driving_details', views.user_driving_details, name = 'DRIVDET'),
    path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    path('home', views.home, name='home'),
    path('<str:room>/', views.room, name='room'),
    path('checkview', views.checkview, name='checkview'),
    path('send', views.send, name='send'),
    path('getMessages/<str:room>/', views.getMessages, name='getMessages'),
    path('approve_msg', views.approve_msg, name = 'APRMSG'),
    path('denied_msg', views.denied_msg, name = 'DNDMSG'),
    path('pending_msg', views.pending_msg, name = 'PNGMSG'),
    path('deleted_msg', views.deleted_msg, name = 'DELMSG'),
    path('inter', views.inter, name = 'INTER'),
    path('edit_list', views.edit_list, name = 'edit_list'),
    path('query_mail', views.query_mail, name = "QUERY"),
    path('index_query', views.index_query_mail, name = 'IQUERY'),
    path(r'rating/(?P<id>[0-9]+)/$  ', views.rating, name = 'RATING' ),
    path(r'view_profile/(?P<id>[0-9]+)/$', views.view_profile, name = 'OPROFILE'),
    ]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



