from django.contrib import admin
from django.urls import path
from CHATBOT import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.chat_interface, name='chat_interface'),
    path('send/', views.send_message, name='send_message'),
]