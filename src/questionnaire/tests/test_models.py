from django.test import TestCase
from questionnaire.models import Questionnaire, Choice, Answer
import datetime


class QuestionnaireTestCase(TestCase):
    def setUp(self):
        Questionnaire.objects.create(
            title="アンケートタイトル１",
            overview="アンケート概要１",
        )
        Questionnaire.objects.create(
            title="アンケートタイトル２",
            overview="アンケート概要２",
        )

    def test_create(self):
        obj: Questionnaire = Questionnaire.objects.get(questionnaire_id=1)
        self.assertEqual(obj.title, "アンケートタイトル１")
        self.assertEqual(obj.overview, "アンケート概要１")
        self.assertIsInstance(obj.created_at, datetime.datetime)
        self.assertIsInstance(obj.updated_at, datetime.datetime)

        obj: Questionnaire = Questionnaire.objects.get(questionnaire_id=2)
        self.assertEqual(obj.title, "アンケートタイトル２")
        self.assertEqual(obj.overview, "アンケート概要２")
        self.assertIsInstance(obj.created_at, datetime.datetime)
        self.assertIsInstance(obj.updated_at, datetime.datetime)


class ChoiceTestCase(TestCase):
    def setUp(self):
        questionnaire: Questionnaire = Questionnaire.objects.create(
            title="アンケートタイトル",
            overview="アンケート概要",
        )
        Choice.objects.create(
            questionnaire=questionnaire,
            text="選択内容１",
        )
        Choice.objects.create(
            questionnaire=questionnaire,
            text="選択内容２",
        )

    def test_create(self):
        obj: Choice = Choice.objects.get(choice_id=1)
        self.assertEqual(obj.choice_id, 1)
        self.assertEqual(obj.text, "選択内容１")
        self.assertIsInstance(obj.created_at, datetime.datetime)
        self.assertIsInstance(obj.updated_at, datetime.datetime)

        obj: Choice = Choice.objects.get(choice_id=2)
        self.assertEqual(obj.choice_id, 2)
        self.assertEqual(obj.text, "選択内容２")
        self.assertIsInstance(obj.created_at, datetime.datetime)
        self.assertIsInstance(obj.updated_at, datetime.datetime)


class AnswerTestCase(TestCase):
    def setUp(self):
        questionnaire: Questionnaire = Questionnaire.objects.create(
            title="アンケートタイトル",
            overview="アンケート概要",
        )
        choice: Choice = Choice.objects.create(
            questionnaire=questionnaire,
            text="選択内容１",
        )
        Answer.objects.create(
            questionnaire=questionnaire,
            choice=choice,
        )

    def test_create(self):
        obj: Answer = Answer.objects.get()
        self.assertIsInstance(obj.created_at, datetime.datetime)
        self.assertIsInstance(obj.updated_at, datetime.datetime)
