from django.urls import path,include
from .views import *
urlpatterns = [
    # path('',index,name="index"),
        path('', image_view,name="image_view"),
        path('image_upload/',image_upload,name="image_upload"),
        path('signup/', Signup.as_view()),
        path('login/', Login.as_view()),
        path('api/costumes/', CostumeCRUD.as_view({'get': 'list'})),
        path('api/costumes/add/', CostumeCRUD.as_view({'post': 'create'})),
        path('api/costumes/<int:pk>/', CostumeCRUD.as_view({'get': 'retrieve'})),
        path('api/costumes/<int:pk>/update/', CostumeCRUD.as_view({'put': 'update'})),
        path('api/costumes/<int:pk>/delete/', CostumeCRUD.as_view({'delete': 'destroy'})),
        path('api/packages/', view_packages),
        path('api/book/', book_costume),
    
    
]
