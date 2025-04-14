from django.urls import path,include
from .views import *
urlpatterns = [
    # path('',index,name="index"),
        # path('', Home.as_view()),
        path('signup/', Signup.as_view()),
        path('login/', Login.as_view()),
    
]
