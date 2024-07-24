from django.urls import path

from . import views

app_name = "questionnaire"
urlpatterns = [
    # アンケート一覧画面
    path(
        route="",
        view=views.questionnaire_list,
        name="questionnaire_list",
    ),
    # アンケート作成画面
    path(
        route="create/",
        view=views.questionnaire_create,
        name="questionnaire_create",
    ),
    # アンケート結果画面
    path(
        route="<int:id>/answers",
        view=views.questionnaire_result,
        name="questionnaire_result",
    ),
    # アンケート回答画面
    path(
        route="<int:id>/answers/create",
        view=views.answer_create,
        name="answer_create",
    ),
]
