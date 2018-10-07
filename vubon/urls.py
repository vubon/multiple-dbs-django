from django.conf.urls import url
from .views import GetAndCreate

urlpatterns = [
    url(r'^get-create/', GetAndCreate.as_view(), name='get-create'),
]
