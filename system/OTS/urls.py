from django.urls import path
from OTS.views import *

app_name = 'OTS'


urlpatterns = [
    path('',welcome),
    path('new-candidate',candidateRegistrationForm, name= 'registrationForm'),
    path('store-candidate',candidateRegistration, name='storeCandidate'),
    path('login',loginView, name='login'),
    path('home',candidateHome,name='home'),
    path('testpaper',testPaper, name='testPaper'),
    path('calculateresult',calculateTestResult, name='calculateTest'),
    path('test-history',testResultHistory,name='testHistory'),
    path('result',showTestResult, name='result'),
    path('logout',logout,name='logout')
]