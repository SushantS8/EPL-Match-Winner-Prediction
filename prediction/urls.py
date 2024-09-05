from django.urls import path
from prediction.views import home,login_view,register_view,logout_view
app_name = "prediction"
urlpatterns = [
    path('home/',home,name="home"),
    path('login/',login_view,name="login"),
    path('',register_view,name="register"),
    path('logout/',logout_view,name="logout")
    

]
