from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from crime_app_api.views import (RegisterView, query1 , query2, query3, query4, query5, query6, query7, 
                                 query8, query9, query10, query11, query12, query13, query14, query15, addNewCrime)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('query1/', query1.as_view(), name='query1'),
    path('query2/', query2.as_view(), name='query2'),
    path('query3/', query3.as_view(), name='query3'),
    path('query4/', query4.as_view(), name='query4'),
    path('query5/', query5.as_view(), name='query5'),
    path('query6/<str:flag>/', query6.as_view(), name='query6'),
    path('query7/', query7.as_view(), name='query7'),
    path('query8/', query8.as_view(), name='query8'),
    path('query9/', query9.as_view(), name='query9'),
    path('query10/<str:flag>/', query10.as_view(), name='query10'),
    path('query11/', query11.as_view(), name='query11'),
    path('query12/', query12.as_view(), name='query12'),
    path('query13/', query13.as_view(), name='query13'),
    path('query14/', query14.as_view(), name='query14'),
    path('query15/', query15.as_view(), name='query15'),
    path('addNewCrime/', addNewCrime.as_view(), name='addNewCrime')
]
