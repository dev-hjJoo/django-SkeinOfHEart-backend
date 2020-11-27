from django.urls import path, include
from SOH import views

urlpatterns = [
    path('test/', views.test),
    path('wordcloud/', views.make_wordcloud),
    path('correcting/', views.correct_content)
]
