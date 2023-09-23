from .models import *
from rest_framework import serializers
import json, ast
# class UserRegistration(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ["id", "username", "first_name", "last_name", "password"]

class AddQuestionSerializer(serializers.ModelSerializer):
    question_type_name = serializers.SerializerMethodField()
    class Meta:
        model = Question
        fields = ["id","question","question_type","question_type_name","option_1",\
                  "option_2","option_3","option_4"]
    def get_question_type_name(self, obj):
        return obj.get_question_type_display()

class AddQuizQuestionSerializer(serializers.ModelSerializer):
    quiz_question_type_name = serializers.SerializerMethodField()
    class Meta:
        model = QuizQuestion
        fields = ["id","quiz_question","quiz_question_type","quiz_question_type_name","quiz_option_1",\
                  "quiz_option_2","quiz_option_3","quiz_option_4"]
    def get_quiz_question_type_name(self, obj):
        return obj.get_quiz_question_type_display()

class AnswersSerializer(serializers.ModelSerializer):
    question_no = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    class Meta:
        model = AnswerQuestion
        fields = ["user","question_no","answer"]
    def get_question_no(self, obj):
        try:
            return obj.question_no.question
        except:
            return "None"
    def get_user(self, obj):
        try:
            return obj.user.username
        except:
            return "None"

class QuizAnswersSerializer(serializers.ModelSerializer):
    quiz_question_no = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    class Meta:
        model = AnswerQuizQuestion
        fields = ["user","quiz_question_no","quiz_answer"]
    def get_quiz_question_no(self, obj):
        try:
            return obj.quiz_question_no.quiz_question
        except:
            return "None"
    def get_user(self, obj):
        try:
            return obj.user.username
        except:
            return "None"        

class UserSerializer(serializers.ModelSerializer):
    qns_ans = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ["id","username","email","is_active","qns_ans"]  
    def get_qns_ans(self, obj):
        id = getattr(obj, "id")
        # item = User.objects.get(id=id)
        display_values = []
        items = AnswerQuestion.objects.filter(user_id=id)
        val = items.values("question_no","answer")
        for i in val:
            obj = Question.objects.get(id=i["question_no"]).question
            display_values.append({"question":obj, "answer":i["answer"]})
        return display_values
    
class UserQuizSerializer(serializers.ModelSerializer):
    quiz_ans = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ["id","username","email","is_active","quiz_ans"]
    def get_quiz_ans(self, obj):
        id = getattr(obj, "id")
        # item = User.objects.get(id=id)
        display_values = []
        items = AnswerQuizQuestion.objects.filter(user_id=id)
        val = items.values("quiz_question_no","quiz_answer")
        for i in val:
            obj = QuizQuestion.objects.get(id=i["quiz_question_no"]).quiz_question
            display_values.append({"question":obj, "answer":i["quiz_answer"]})
        return display_values    
    
class QuizAnswersSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizAnswersSheet
        fields = ['id','check_question', 'quiz_question_ans']

class ScoreOfCandidateSerializer(serializers.ModelSerializer):
    candidate_name = serializers.SerializerMethodField()
    class Meta:
        model = ScoreOfCandidate     
        fields = ["id", "candidate_name","total_ques_attempted",
                  "Unattempted_ques","marks_obtained"]
    def get_candidate_name(self, obj):
        try:
            return obj.candidate.username
        except:
            return "NONE!!"
        
class RankingSerializer(serializers.ModelSerializer):
    # user = UserSerializer()
    user_name = serializers.SerializerMethodField()
    class Meta:
        model = Ranking
        fields = ["id", "user_name", "marks_obtained", "rank"]
    def get_user_name(self, obj):
        try:
            return obj.user.username
        except:
            return None

class TestingAddQuestionSerializer(serializers.ModelSerializer):
    question_type_name = serializers.SerializerMethodField()
    class Meta:
        model = TestingPurpose
        fields = ["id","question","question_type","question_type_name","options"]
    def get_question_type_name(self, obj):
        return obj.get_question_type_display()
    
class TestingAttemptSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()
    attempted_question = serializers.SerializerMethodField()
    class Meta:
        model = TestingAttemptQuestion
        fields = ["id","user_name","attempted_question", "answer", "answers"]
    def get_answers(self, obj):
        question_no = getattr(obj, "question_no_id")
        answers = TestingAttemptQuestion.objects.get(question_no_id=question_no)
        questions = TestingPurpose.objects.get(id=question_no)
        display = []
        user_ans = answers.answer
        if questions.question_type == "2":
            js_ans = ast.literal_eval(user_ans)
            for i in js_ans:
                display.append(questions.options[i])
            return display    
        elif questions.question_type == "3":
            return questions.options[user_ans]
        elif questions.question_type == "1":
            return user_ans
    def get_user_name(self, obj):
        try:
            return obj.user.username
        except:
            return None
    def get_attempted_question(self, obj):
        try:
            return obj.question_no.question
        except:
            return None
        
class AddTestingQuizQuestionSerializer(serializers.ModelSerializer):
    quiz_question_type_name = serializers.SerializerMethodField()
    class Meta:
        model = TestingQuizQuestion
        fields = ["id","quiz_question","quiz_question_type","quiz_question_type_name","options"]
    def get_quiz_question_type_name(self, obj):
        return obj.get_quiz_question_type_display()
    
class TestingAnswerQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestingAttemptQuestion
        fields = ['id','user','question_no','answer'] 

class TestinglistfieldSerializer(serializers.ModelSerializer):
    extra_info = serializers.DictField()
    class Meta:
        model = Testinglistfield1
        fields = ["id", "chars", "extra_info", "left_info"]

class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friend
        fields = ["id", "user", "friends"]

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "username", "password"]
                