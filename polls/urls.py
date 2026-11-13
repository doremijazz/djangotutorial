from django.urls import path

from . import views

app_name = "polls"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("all/", views.AllView.as_view(), name="all"),
    path("connexion/", views.connexion_personnalisee, name="connexion_personnalisee"),
    path("inscription/", views.register, name="inscription"),
    path("account/<int:pk>/", views.UserView.as_view(), name="account"),
    path("change_question/<int:pk>/", views.change_question, name="change_question"),
    path("password/", views.ChangePasswordView.as_view(), name="change_password"),
    path("deconnexion/", views.deconnexion, name="deconnexion"),
    path("statistics/", views.StatisticsView.as_view(), name="statistics"),
    path("form/", views.get_question, name="form"),
    path("<int:pk>/frequency/", views.FrequencyView.as_view(), name="frequency"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
]