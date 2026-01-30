from django.urls import path

from . import views

app_name = "polls"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),

    # API endpoints
    path("api/", views.api_index, name="api_index"),
    path("api/<int:pk>/", views.api_detail, name="api_detail"),
    path("api/<int:pk>/vote/", views.api_vote, name="api_vote"),
    path("api/<int:pk>/results/", views.api_results, name="api_results"),
]