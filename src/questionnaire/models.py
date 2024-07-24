from django.db import models


# Create your models here.
class Questionnaire(models.Model):

    class Meta:
        verbose_name = "アンケート"
        verbose_name_plural = "アンケート"

    def __str__(self):
        return self.title

    questionnaire_id = models.AutoField(
        verbose_name="アンケートID",
        primary_key=True,
        null=False,
    )
    title = models.CharField(
        verbose_name="アンケートタイトル",
        max_length=20,
        null=False,
    )
    overview = models.CharField(
        verbose_name="アンケートの概要",
        max_length=200,
        null=False,
    )
    created_at = models.DateTimeField(
        verbose_name="作成日時",
        auto_now_add=True,
        null=False,
    )
    updated_at = models.DateTimeField(
        verbose_name="更新日時",
        auto_now=True,
        null=False,
    )


class Choice(models.Model):

    class Meta:
        verbose_name = "選択内容"
        verbose_name_plural = "選択内容"

    def __str__(self):
        return f"{self.text}（{self.questionnaire.title}）"

    questionnaire = models.ForeignKey(
        verbose_name="アンケート",
        to=Questionnaire,
        on_delete=models.CASCADE,
        null=False,
    )
    choice_id = models.AutoField(
        verbose_name="選択内容ID",
        primary_key=True,
        null=False,
    )
    text = models.CharField(
        verbose_name="選択内容",
        max_length=40,
        null=False,
    )
    created_at = models.DateTimeField(
        verbose_name="作成日時",
        auto_now_add=True,
        null=False,
    )
    updated_at = models.DateTimeField(
        verbose_name="更新日時",
        auto_now=True,
        null=False,
    )


class Answer(models.Model):

    class Meta:
        verbose_name = "回答"
        verbose_name_plural = "回答"

    def __str__(self):
        return f"{self.choice.text}（{self.questionnaire.title}）"

    questionnaire = models.ForeignKey(
        verbose_name="アンケート",
        to=Questionnaire,
        on_delete=models.CASCADE,
        null=False,
    )
    choice = models.ForeignKey(
        verbose_name="選択内容",
        to=Choice,
        on_delete=models.CASCADE,
        null=False,
    )
    created_at = models.DateTimeField(
        verbose_name="作成日時",
        auto_now_add=True,
        null=False,
    )
    updated_at = models.DateTimeField(
        verbose_name="更新日時",
        auto_now=True,
        null=False,
    )
