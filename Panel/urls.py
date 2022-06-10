from django.urls import path
from Panel.views import (
    Container,
    Home,
    Delete_Container,
    Create_Container,
    toggle_turn_OffOn,
    Restart_Container,
)


app_name = "Panel"
urlpatterns = [
    path("", Home, name="Home"),
    path("container/<str:id>", Container, name="Container"),
    path("delete-container/<str:id>", Delete_Container, name="Delete_Container"),
    path("create-container/", Create_Container, name="Create_Container"),
    path("toggle_status/<str:id>", toggle_turn_OffOn, name="Toggle_Status"),
    path("restart_container/<str:id>", Restart_Container, name="Restart_Container"),
]
