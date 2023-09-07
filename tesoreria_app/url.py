from django.urls import path

from .views import LimitesTipoInversionView

urlpatterns = [
    path('LimitesTipoInversion/', LimitesTipoInversionView.as_view()),
    
]
