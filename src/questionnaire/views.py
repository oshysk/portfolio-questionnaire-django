from django.db.models import F, Count
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render, get_list_or_404, redirect
from django.http import (
    HttpResponse,
    HttpResponseRedirect,
    HttpResponseNotAllowed,
    HttpResponseServerError,
)
from django.template import loader
from django.urls import reverse
from typing import Any
from django import forms
import json

from .models import Questionnaire, Choice, Answer
from .forms import QuestionnaireForm, ChoiceForm, AnswerForm


# Create your views here.
def questionnaire_list(request: HttpRequest) -> HttpResponse:
    """アンケート一覧画面"""

    # GET以外は405エラーを返す。
    if request.method not in ["GET"]:
        return HttpResponseNotAllowed(["GET"])

    # アンケート一覧を取得する。
    questionnaire_list = Questionnaire.objects.all()

    # アンケート一覧画面を返す。
    return render(
        request=request,
        template_name="questionnaire/questionnaire_list.html",
        context={
            "questionnaire_list": questionnaire_list,
        },
    )


def questionnaire_create(request: HttpRequest) -> HttpResponse:
    """アンケート作成画面"""

    def get_questionnaire_create_response_init() -> HttpResponse:
        """アンケート作成画面を取得する。"""
        questionnaire_form: QuestionnaireForm = QuestionnaireForm()
        choice_form_list: list[ChoiceForm] = [ChoiceForm() for _ in range(5)]
        choice_form_list_errors: bool = False
        return render(
            request=request,
            template_name="questionnaire/questionnaire_create.html",
            context={
                "questionnaire_form": questionnaire_form,
                "choice_form_list": choice_form_list,
                "choice_form_list_errors": choice_form_list_errors,
            },
        )

    def is_form_valid(request: HttpRequest) -> bool:
        """フォームのバリデーションチェックを実行する。"""
        questionnaire_form: QuestionnaireForm = QuestionnaireForm(request.POST)
        if questionnaire_form.is_valid() is False:
            return False
        for choice in request.POST.getlist("text[]"):
            if len(choice) == 0:
                continue
            choice_form = ChoiceForm({"text": choice})
            if choice_form.is_valid() is False:
                return False
        return True

    def form_save(request: HttpRequest) -> None:
        """フォームを保存する。"""
        questionnaire_form: QuestionnaireForm = QuestionnaireForm(request.POST)
        questionnaire_model: Questionnaire = questionnaire_form.save()
        for choice in request.POST.getlist("text[]"):
            if len(choice) == 0:
                continue
            choice_form: ChoiceForm = ChoiceForm({"text": choice})
            choice_form.save(questionnaire_model=questionnaire_model)
        return None

    def get_questionnaire_create_response_errors(request: HttpRequest) -> HttpResponse:
        """エラー付きのアンケート作成画面を取得する。"""
        questionnaire_form: QuestionnaireForm = QuestionnaireForm(request.POST)
        choice_form_list_errors: bool = True
        choice_form_list: list[ChoiceForm] = list()
        for choice in request.POST.getlist("text[]"):
            if len(choice) == 0:
                choice_form = ChoiceForm()
            else:
                choice_form = ChoiceForm({"text": choice})
            choice_form_list.append(choice_form)
        return render(
            request=request,
            template_name="questionnaire/questionnaire_create.html",
            context={
                "questionnaire_form": questionnaire_form,
                "choice_form_list": choice_form_list,
                "choice_form_list_errors": choice_form_list_errors,
            },
        )

    # GET、POST以外は405エラーを返す。
    if request.method not in ["GET", "POST"]:
        return HttpResponseNotAllowed(["GET", "POST"])

    # GETの場合は、アンケート作成画面を返す。
    if request.method == "GET":
        return get_questionnaire_create_response_init()

    # POSTの場合は、アンケートを作成する。
    if request.method == "POST":
        if is_form_valid(request) is True:
            # バリデーションチェックがOKの場合は、アンケートを作成する。
            form_save(request)
            return redirect(reverse("questionnaire:questionnaire_list"))
        else:
            # バリデーションチェックがNGの場合は、エラーメッセージ付きアンケート作成画面を返す。
            return get_questionnaire_create_response_errors(request)

    # ロジックエラー、有り得ないルート。
    return HttpResponseServerError()


def questionnaire_result(request, id):
    """アンケート結果"""

    # GET以外は405エラーを返す。
    if request.method not in ["GET"]:
        return HttpResponseNotAllowed(["GET"])

    # アンケートを取得する。
    questionnaire = get_object_or_404(Questionnaire, questionnaire_id=id)

    # アンケートの回答結果を取得する。
    answers = (
        Answer.objects.filter(questionnaire_id=id)
        .values("choice", "choice__text")
        .annotate(count=Count("choice"))
    )

    # アンケート結果画面を返す。
    return render(
        request=request,
        template_name="questionnaire/questionnaire_result.html",
        context={
            "questionnaire": questionnaire,
            "answers": answers,
            "answers_labels_json": json.dumps(
                [answer["choice__text"] for answer in answers]
            ),
            "answers_values_json": json.dumps([answer["count"] for answer in answers]),
        },
    )


def answer_create(
    request: HttpRequest,
    id: int,
) -> HttpResponse:
    """アンケート回答画面"""

    def get_answer_create_response_init() -> HttpResponse:
        questionnaire: Questionnaire = get_object_or_404(
            Questionnaire, questionnaire_id=id
        )
        answer_form: AnswerForm = AnswerForm(questionnaire_id=id)
        return render(
            request=request,
            template_name="questionnaire/answer_create.html",
            context={
                "questionnaire": questionnaire,
                "answer_form": answer_form,
            },
        )

    def is_form_valid(request: HttpRequest, id: int) -> bool:
        """フォームのバリデーションチェックを実行する。"""
        answer_form: AnswerForm = AnswerForm(data=request.POST, questionnaire_id=id)
        if answer_form.is_valid() is False:
            return False
        return True

    def form_save(request: HttpRequest, id: int) -> None:
        """フォームを保存する。"""
        answer_form: AnswerForm = AnswerForm(data=request.POST, questionnaire_id=id)
        answer_form.is_valid()
        answer_form.save()
        return None

    # GET、POST以外は405エラーを返す。
    if request.method not in ["GET", "POST"]:
        return HttpResponseNotAllowed(["GET", "POST"])

    # GETの場合は、アンケート回答画面を返す。
    if request.method == "GET":
        return get_answer_create_response_init()

    # POSTの場合は、回答結果を保存する。
    if request.method == "POST":
        if is_form_valid(request=request, id=id) is False:
            return HttpResponseServerError()
        form_save(request=request, id=id)
        return redirect(
            reverse("questionnaire:questionnaire_result", kwargs={"id": id})
        )

    # ロジックエラー、有り得ないルート。
    return HttpResponseServerError()
