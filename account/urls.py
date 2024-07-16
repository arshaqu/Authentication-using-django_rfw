
from django.urls import path
from .views import RegisterView ,LoginView,OtpVerificationView

urlpatterns = [
    path('api/register/', RegisterView.as_view(), name="sign_up"),
    path('api/verify/', OtpVerificationView.as_view(),name='otp_sign'),
    path('api/login/',LoginView.as_view(), name='sign_in')

]