from django.test import TestCase, Client
from django.urls import reverse
from questionnaire.models import Questionnaire


class QuestionnaireListTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.model = Questionnaire.objects.create(
            title="アンケートタイトル１",
            overview="アンケート概要１",
        )

    def test_view_renders_correct_template(self):
        response = self.client.get(reverse("questionnaire:questionnaire_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "questionnaire/questionnaire_list.html")
