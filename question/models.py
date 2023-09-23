from django.db import models
from django.contrib.auth.models import AbstractUser
import json
from .fields import ListField
from django.db.models import CharField, Model, IntegerField, JSONField
from picklefield.fields import PickledObjectField
from django_mysql.models import ListCharField, ListTextField

TYPE_OF_QUESTION = (("1", "text"),("2", "checkbox"),("3", "radio"))

class Question(models.Model):
    question = models.CharField(max_length=255, default=None)
    question_type = models.CharField(max_length=255, choices=TYPE_OF_QUESTION, default="1")
    option_1 = models.CharField(max_length=20,null=True, blank=True)
    option_2 = models.CharField(max_length=20,null=True, blank=True)
    option_3 = models.CharField(max_length=20,null=True, blank=True)
    option_4 = models.CharField(max_length=20,null=True, blank=True)
    class Meta:
        verbose_name_plural = "Questions" #4

class User(AbstractUser):
    username = models.CharField(max_length=255,unique=True,db_index=True)
    class Meta:
        verbose_name_plural = "Users" #5

class AnswerQuestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="nothing")
    question_no = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="qsn", default=None)
    answer = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        verbose_name_plural = "AnswerQuestions" #3

class QuizQuestion(models.Model):
    quiz_question = models.CharField(max_length=255, default=None)
    quiz_question_type = models.CharField(max_length=255, choices=TYPE_OF_QUESTION, default="1")
    quiz_option_1 = models.CharField(max_length=20,null=True, blank=True)
    quiz_option_2 = models.CharField(max_length=20,null=True, blank=True)
    quiz_option_3 = models.CharField(max_length=20,null=True, blank=True)
    quiz_option_4 = models.CharField(max_length=20,null=True, blank=True)
    class Meta:
        verbose_name_plural = "QuizQuestions" #1

class QuizAnswersSheet(models.Model):
    check_question = models.OneToOneField(QuizQuestion, on_delete=models.CASCADE)
    quiz_question_ans = models.CharField(max_length=255)
    class Meta:
        verbose_name_plural = "QuizAnswersSheet" #6

class AnswerQuizQuestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="nothing2")
    quiz_question_no = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE, related_name="qsn2", default=None)
    quiz_answer = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        verbose_name_plural = "AnswerQuizQuestions" #2

class ScoreOfCandidate(models.Model):
    candidate = models.OneToOneField(User, on_delete=models.CASCADE)
    total_ques_attempted = models.IntegerField(default=0)
    Unattempted_ques = models.IntegerField(default=0)
    marks_obtained = models.IntegerField(default=0)
    Total_marks = models.IntegerField(default=13)
    class Meta:
        verbose_name_plural = "ScoreofCandidates"

class Ranking(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    marks_obtained = models.IntegerField()
    rank = models.IntegerField()
    class Meta:
        verbose_name_plural = "Rankings of candidates"

class TempQuizAnswer(models.Model):
    question = models.CharField(max_length=200)
    answer = models.CharField(max_length=255)
    class Meta:
        verbose_name_plural = "TempQuizAnswer"

class Contenders(models.Model):
    username = models.CharField(max_length=255, default=None, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    class Meta:
        verbose_name_plural = "Contenders"

class TempQuiz(models.Model):
    user = models.ForeignKey(Contenders, on_delete=models.CASCADE, default=None)
    question = models.CharField(max_length=200)
    answer = models.CharField(max_length=255)
    answer_check = models.BooleanField(default=False)
    class Meta:
        verbose_name_plural = "TempQuiz"

class TempScoreofCandidate(models.Model):
    user = models.ForeignKey(Contenders, on_delete=models.CASCADE, default=None)
    marks_obtained = models.IntegerField()
    class Meta:
        verbose_name_plural = "TempScoreofCandidate"

class TestingPurpose(models.Model):
    question = models.CharField(max_length=255)
    question_type = models.CharField(max_length=255, choices=TYPE_OF_QUESTION, default="1")
    options = models.JSONField(default=dict)

class TestingAttemptQuestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="nothing3")
    question_no = models.ForeignKey(TestingPurpose, on_delete=models.CASCADE, related_name="qsn3", default=None, verbose_name="attempt_question")
    answer = models.CharField(max_length=200)
    # def set_answer(self, x):
    #     self.answer = json.dumps(x)
    # def get_answer(self):
    #     return json.loads(self.answer)

class TestingQuizQuestion(models.Model):
    quiz_question = models.CharField(max_length=255, default=None)
    quiz_question_type = models.CharField(max_length=255, choices=TYPE_OF_QUESTION, default="1")
    options = models.JSONField(default=dict)

class Testinglistfield1(models.Model):
    chars = ListCharField(
        base_field = IntegerField(),
        default = None,
        null = True,
        blank = True,
        size=6,
        max_length=(6 * 11)
    )
    extra_info=PickledObjectField(default=dict)
    left_info = models.JSONField(default=dict)
    # left_info1 = ListTextField(
    #     base_field = JSONField(default=dict),
    #     size = 6
    # )
    class Meta:
        verbose_name = "TestingModel"

class Friend(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="mainuser")
    friends = models.ManyToManyField(User)