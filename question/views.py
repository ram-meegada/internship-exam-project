from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import *
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import models
from django.views.generic import TemplateView
from django.urls import reverse
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.schemas import AutoSchema
from rest_framework.compat import coreapi, coreschema, uritemplate
import ast

class loginAPI(APIView):
    def post(self, request):
        username = request.data.get("username")
        # password = request.data.get("password")
        try:
            user = User.objects.get(username=username)
            # chk_pwd = check_password(password, user.password)
            if user:
                token = RefreshToken.for_user(user)
                data = {"username":user.username, "access_token":str(token.access_token), "refresh_token":str(token)}
                return Response(data)
            # elif not chk_pwd:
            #     return Response({"message":"password not matching"}, status=status.HTTP_400_BAD_REQUEST)    
        except:
            return Response({"message":"user not found"}, status=status.HTTP_400_BAD_REQUEST)    

class AddQuestion(APIView):
    # permission_classes = (IsAdminUser,)
    serializer_class = AddQuestionSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.validated_data
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class EditDeleteQuestion(APIView):
    # permission_classes = (IsAdminUser,)
    serializer_class = AddQuestionSerializer
    def get_object(self,id):
        try:
            return Question.objects.get(id=id)
        except:
            raise Http404
        
    def get(self, request,id):
        item = self.get_object(id)
        serializer = self.serializer_class(item)
        serialized_data = serializer.data
        return Response(serialized_data, status=status.HTTP_200_OK)    

    def put(self, request, id):
        item = self.get_object(id)
        serializer = self.serializer_class(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DisplayAllQuestions(APIView):
    serializer_class = AddQuestionSerializer
    def get(self, request):
        items = Question.objects.all()
        serializer = self.serializer_class(items, many=True)
        serialized_data = serializer.data
        return Response(serialized_data, status=status.HTTP_200_OK)    

class AttemptAnswer(APIView):
    # permission_classes = (IsAuthenticated,)
    def post(self, request):
        user = request.data["user"]
        question_no = request.data["question_no"]
        attempt_check = AnswerQuestion.objects.filter(user_id=user).filter(question_no_id=question_no)
        if not attempt_check:
            class AnswerQuestionSerializer(serializers.ModelSerializer):
                item = Question.objects.get(id = question_no)
                if item.question_type == "3":
                    CHOICES = [item.option_1,item.option_2,item.option_3,item.option_4]
                    answer = serializers.ChoiceField(choices=CHOICES)
                elif item.question_type == "1":
                    answer = serializers.CharField()  
                elif item.question_type == "2":
                    CHOICES = [item.option_1,item.option_2,item.option_3,item.option_4]
                    answer = serializers.MultipleChoiceField(choices=CHOICES)
                question_n = serializers.SerializerMethodField()   
                user_name = serializers.SerializerMethodField() 
                class Meta:
                    model = AnswerQuestion
                    fields = ["id","user","user_name","question_no","question_n","answer"]
                def get_question_n(self, obj):
                    try:
                        return obj.question_no.question
                    except:
                        return "None"    
                def get_user_name(self, obj):
                    try:
                        return obj.user.username
                    except:
                        return "None"    
            serializer = AnswerQuestionSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif attempt_check: 
            class AnswerQuestionSerializer(serializers.ModelSerializer):
                item = Question.objects.get(id = question_no)
                if item.question_type == "3":
                    CHOICES = [item.option_1,item.option_2,item.option_3,item.option_4]
                    answer = serializers.ChoiceField(choices=CHOICES)
                elif item.question_type == "1":
                    answer = serializers.CharField()  
                elif item.question_type == "2":
                    CHOICES = [item.option_1,item.option_2,item.option_3,item.option_4]
                    answer = serializers.MultipleChoiceField(choices=CHOICES)
                question_n = serializers.SerializerMethodField()
                user_name = serializers.SerializerMethodField()
                class Meta:
                    model = AnswerQuestion
                    fields = ["id","user","user_name","question_no","question_n","answer"]    
                def get_question_n(self, obj):
                    try:
                        return obj.question_no.question
                    except:
                        return "None"  
                def get_user_name(self, obj):
                    try:
                        return obj.user.username
                    except:
                        return "None"      
            serializer = AnswerQuestionSerializer(attempt_check[0],data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DisplayAllAnswers(APIView):
    serializer_class =  AnswersSerializer
    def get(self, request):
        items = AnswerQuestion.objects.all()
        serializer = self.serializer_class(items, many=True)
        serialized_data = serializer.data
        return Response(serialized_data, status=status.HTTP_200_OK)

class DisplayAllUsers(APIView):
    serializer_class = UserSerializer
    def get(self, request):
        items = User.objects.all()
        serializer = self.serializer_class(items, many=True)
        serialized_data = serializer.data
        return Response(serialized_data, status=status.HTTP_200_OK)

# class AttemptAnswer(APIView):
#     def post(self, request,id):
#         question_no = request.data["question_no"]
#         context = {"ques": question_no}
#         serializer = AnswerQuestionSerializer(data= request.data, context=context)
#         if serializer.is_valid():
#             serializer.validated_data
#             serializer.save()
#             serialized_data = serializer.data
#             # AnswerQuestionSerializer.nothing(serialized_data)
#             return Response(serializer.data,status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class AttemptAnswer(APIView):
#     def post(self, request):
#         user = request.data["user"]
#         question_no = request.data["question_no"]
#         item = Question.objects.get(id=question_no)
#         class AnswerQuestion(models.Model):
#             CHOICES = (("1",item.option_1), ("2",item.option_2),("3",item.option_3),("4",item.option_4))
#             user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="nothing")
#             question_no = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="qsn", default=None) 
#             answer = models.CharField(max_length=255,choices=CHOICES ,blank=True, null=True)
#         answer = request.data["answer"]
#         obj = AnswerQuestion.objects.create(user=user, question_no=question_no, answer=answer)
#         return Response({"data":"done"})

class AddQuizQuestion(APIView):
    serializer_class = AddQuizQuestionSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.validated_data
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DisplayAllQuizQuestions(APIView):
    serializer_class = AddQuizQuestionSerializer
    def get(self, request):
        items = QuizQuestion.objects.all()
        serializer = self.serializer_class(items, many=True)
        serialized_data = serializer.data
        return Response(serialized_data, status=status.HTTP_200_OK)

class AddQuizAnswers(APIView):
    def post(self, request):
        check_question = request.data["check_question"]
        class AddQuizAnswersSerializer(serializers.ModelSerializer):
            item = QuizQuestion.objects.get(id=check_question)
            if item.quiz_question_type == "3":
                CHOICES = [item.quiz_option_1,item.quiz_option_2,item.quiz_option_3,item.quiz_option_4]
                quiz_question_ans = serializers.ChoiceField(choices=CHOICES)
            elif item.quiz_question_type == "2":
                CHOICES = [item.quiz_option_1,item.quiz_option_2,item.quiz_option_3,item.quiz_option_4]
                quiz_question_ans = serializers.MultipleChoiceField(choices=CHOICES)
            elif item.quiz_question_type == "1":
                quiz_question_ans = serializers.CharField()          
            class Meta:
                model = QuizAnswersSheet
                fields = ["id","check_question", "quiz_question_ans"]
        serializer = AddQuizAnswersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            serialized_data = serializer.data
            return Response(serialized_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DisplayQuizSheetAnswers(APIView):
    serializer_class = QuizAnswersSheetSerializer
    def get(self, request):
        items = QuizAnswersSheet.objects.all()
        serializer = self.serializer_class(items, many=True)
        serialized_data = serializer.data
        return Response(serialized_data, status=status.HTTP_200_OK)
    
class UserAttemptQuizAnswer(APIView):
    def put(self, request):
        user = request.data["user"]
        quiz_question_no = request.data["quiz_question_no"]
        attempt_check = AnswerQuizQuestion.objects.filter(user_id=user).filter(quiz_question_no_id=quiz_question_no)
        if not attempt_check:
            class AnswerQuizQuestionSerializer(serializers.ModelSerializer):
                item = QuizQuestion.objects.get(id=quiz_question_no)
                if item.quiz_question_type == "3":
                    CHOICES = [item.quiz_option_1,item.quiz_option_2,item.quiz_option_3,item.quiz_option_4]
                    quiz_answer = serializers.ChoiceField(choices=CHOICES)
                elif item.quiz_question_type == "2":
                    CHOICES = [item.quiz_option_1,item.quiz_option_2,item.quiz_option_3,item.quiz_option_4]
                    quiz_answer = serializers.MultipleChoiceField(choices=CHOICES)
                elif item.quiz_question_type == "1":
                    quiz_answer = serializers.CharField()
                question_n = serializers.SerializerMethodField()
                user_name = serializers.SerializerMethodField()
                class Meta:
                    model = AnswerQuizQuestion
                    fields = ["id","user","user_name","quiz_question_no","question_n","quiz_answer"]
                def get_question_n(self, obj):
                    try:
                        return obj.quiz_question_no.quiz_question
                    except:
                        return "None"
                def get_user_name(self, obj):
                    try:
                        return obj.user.username
                    except:
                        return "None"    
            serializer = AnswerQuizQuestionSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif attempt_check:
            class AnswerQuizQuestionSerializer(serializers.ModelSerializer):
                item = QuizQuestion.objects.get(id=quiz_question_no)
                if item.quiz_question_type == "3":
                    CHOICES = [item.quiz_option_1,item.quiz_option_2,item.quiz_option_3,item.quiz_option_4]
                    quiz_answer = serializers.ChoiceField(choices=CHOICES)
                elif item.quiz_question_type == "2":
                    CHOICES = [item.quiz_option_1,item.quiz_option_2,item.quiz_option_3,item.quiz_option_4]
                    quiz_answer = serializers.MultipleChoiceField(choices=CHOICES)
                elif item.quiz_question_type == "1":
                    quiz_answer = serializers.CharField()
                question_n = serializers.SerializerMethodField()   
                user_name = serializers.SerializerMethodField() 
                class Meta:
                    model = AnswerQuizQuestion
                    fields = ["id","user","user_name","quiz_question_no","question_n","quiz_answer"]
                def get_question_n(self, obj):
                    try:
                        return obj.quiz_question_no.quiz_question
                    except:
                        return "None"    
                def get_user_name(self, obj):
                    try:
                        return obj.user.username
                    except:
                        return "None"      
            serializer = AnswerQuizQuestionSerializer(attempt_check[0],data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class ShowAllUsers(APIView):
    serializer_class = UserQuizSerializer
    def get(self, request):
        items = User.objects.all()
        serializer = self.serializer_class(items, many=True)
        serialized_data = serializer.data
        return Response(serialized_data, status=status.HTTP_200_OK)        
    
class ShowAllQuizAnswers(APIView):
    serializer_class =  QuizAnswersSerializer
    def get(self, request):
        items = AnswerQuizQuestion.objects.all()
        serializer = self.serializer_class(items, many=True)
        serialized_data = serializer.data
        return Response(serialized_data, status=status.HTTP_200_OK)

class CalculateMarks(APIView):
    serializer_class = ScoreOfCandidateSerializer
    def post(self,request):
        candidate = request.data.get("candidate")
        try:
            score = ScoreOfCandidate.objects.get(candidate_id=candidate)
            serializer = self.serializer_class(score)
            serialized_data = serializer.data
            return Response(serialized_data, status=status.HTTP_200_OK)
        except:    
            Total = 0
            ans_cand = AnswerQuizQuestion.objects.filter(user_id=candidate).values()
            for i in ans_cand:
                q_type = QuizQuestion.objects.get(id = i["quiz_question_no_id"]).quiz_question_type
                answer = QuizAnswersSheet.objects.get(check_question_id = i["quiz_question_no_id"]).quiz_question_ans
                if q_type != "2":
                    if i["quiz_answer"] == answer:
                        Total += 1        
                elif q_type == "2":
                    a = i["quiz_answer"]
                    b = answer
                    a = ''.join(a.split(" "))
                    b = ''.join(b.split(" "))
                    a = sorted(a)
                    b = sorted(b)
                    if a ==b:
                        Total += 2
            total_ques_attempted = len(ans_cand)
            Unattempted_ques = 10-total_ques_attempted
            item = ScoreOfCandidate.objects.create(candidate_id=candidate,total_ques_attempted=total_ques_attempted,
                                                Unattempted_ques=Unattempted_ques,marks_obtained=Total)
            item.save()
            serializer = self.serializer_class(item)
            serialized_data = serializer.data
            return Response(serialized_data, status=status.HTTP_201_CREATED)
    
class UserQuizAnswers(APIView):
    serializer_class = QuizAnswersSerializer
    def get(self, request, id):
        answers = AnswerQuizQuestion.objects.filter(user_id=id)
        serializer = self.serializer_class(answers, many=True)
        serialized_data = serializer.data
        return Response(serialized_data, status=status.HTTP_200_OK)
    
class ScoresOfCandidates(APIView):
    serializer_class = ScoreOfCandidateSerializer
    def get(self, request):
        scores = ScoreOfCandidate.objects.all().order_by("-marks_obtained")
        serializer = self.serializer_class(scores, many=True)
        serialized_data = serializer.data
        return Response(serialized_data, status=status.HTTP_200_OK)
    
class RankingsofCandidate(APIView):
    serializer_class = RankingSerializer
    def get(self, request):
        rankings = Ranking.objects.all()
        record = ScoreOfCandidate.objects.all().order_by("-marks_obtained")
        rank, ptr = 1, 0
        if rankings:
            serializer = self.serializer_class(rankings, many=True)
            serialized_data = serializer.data
            return Response(serialized_data, status=status.HTTP_200_OK)
        else:
            while ptr<len(record):
                if ptr == 0 or record[ptr].marks_obtained != record[ptr-1].marks_obtained:
                    item = Ranking.objects.create(user_id=record[ptr].candidate_id, marks_obtained=record[ptr].marks_obtained, rank=rank)
                    ptr += 1
                    rank += 1
                elif record[ptr].marks_obtained == record[ptr-1].marks_obtained:
                    item = Ranking.objects.create(user_id=record[ptr].candidate_id, marks_obtained=record[ptr].marks_obtained, rank=rank-1)
                    ptr += 1
            ranks = Ranking.objects.all()
            serializer = self.serializer_class(ranks, many=True)
            serialized_data = serializer.data
            return Response(serialized_data, status=status.HTTP_200_OK)
        
class TemplQuizQuestions(TemplateView):
    template_name = "quiz.html"
    def post(self, request):
        data = {
        'question1' :request.POST.get("question1"),
        'question2' : request.POST.get("question2"),
        'question3' : request.POST.get("question3"),
        'question4' : request.POST.getlist("question4[]"),
        'question5' : request.POST.get("question5"),
        'question6' : request.POST.getlist("question6[]"),
        'question7' : request.POST.getlist("question7[]"),
        'question8' : request.POST.get("question8"),
        }
        for i,j in enumerate(data):
            TempQuizAnswer.objects.create(question=i+1, answer=data[j])
        return HttpResponse("Quiz answer responses are recorded")

class EnterDetails(TemplateView):
    template_name = "details.html"
    def post(self, request):
        data = {
            "username": request.POST.get("username"),
            "first_name": request.POST.get("first_name"),
            "last_name": request.POST.get("last_name"),
            "email": request.POST.get("email"),
        }
        Contenders.objects.create(username=data["username"], first_name=data["first_name"], last_name=data["last_name"],
                                  email=data["email"])
        item = Contenders.objects.get(username=data["username"])
        return HttpResponseRedirect(reverse("attempt_quiz", args=(item.id,)))
    
class TempAttemptQuiz(TemplateView):
    template_name = "quiz.html"
    def post(self, request, id):
        data = {
        'question1' :request.POST.get("question1"),
        'question2' : request.POST.get("question2"),
        'question3' : request.POST.get("question3"),
        'question4' : request.POST.get("question4",[]),
        'question5' : request.POST.get("question5"),
        'question6' : request.POST.get("question6",[]),
        'question7' : request.POST.get("question7",[]),
        'question8' : request.POST.get("question8"),
        }
        marks_weightage = {"1":1,"2":1,"3":1,"4":2,"5":1,"6":2,"7":2,"8":1} 
        Total = 0
        for i,j in enumerate(data):
            crt_ans = TempQuizAnswer.objects.get(question=str(i+1)).answer
            if str(data[j]) == crt_ans:
                TempQuiz.objects.create(user_id=id,question=i+1, answer=data[j], answer_check=True)
                Total += marks_weightage[str(i+1)]
            elif str(data[j]) != crt_ans:
                TempQuiz.objects.create(user_id=id,question=i+1, answer=data[j])
        TempScoreofCandidate.objects.create(user_id=id, marks_obtained=Total)
        return render(request,"scoredisplay.html", locals())
        # return HttpResponse(f"Your quiz is completed. You scored {Total}/11.")

class DisplayScores(TemplateView):
    template_name = "scoredisplay.html"
    def get(self, request):
        pass

class TestingAddQuestion(APIView):
    # permission_classes = (IsAdminUser,)
    serializer_class = TestingAddQuestionSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.validated_data
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TestingAttemptAnswer(APIView):
    # permission_classes = (IsAuthenticated,)
    def post(self, request):
        user = request.data["user"]
        question_no = request.data["question_no"]
        attempt_check = TestingAttemptQuestion.objects.filter(user_id=user).filter(question_no_id=question_no)
        class TestingAnswerQuestionSerializer(serializers.ModelSerializer):    
                item = TestingPurpose.objects.get(id = question_no)
                if item.question_type == "3":
                    CHOICES = []
                    valid_options = {}
                    for i in item.options:
                        CHOICES.append(i)
                        valid_options[i] = item.options[i]
                    answer = serializers.ChoiceField(choices=CHOICES)
                elif item.question_type == "1":
                    answer = serializers.CharField()  
                elif item.question_type == "2":
                    CHOICES = []
                    valid_options = {}
                    for i in item.options:
                        CHOICES.append(i)
                        valid_options[i] = item.options[i]
                    print(CHOICES,"==================")    
                    answer = serializers.MultipleChoiceField(choices=CHOICES)
                question_n = serializers.SerializerMethodField()
                user_name = serializers.SerializerMethodField()
                class Meta:
                    model = TestingAttemptQuestion
                    fields = ["id","user","user_name","question_no","question_n","answer"]
                def get_question_n(self, obj):
                    try:
                        return obj.question_no.question
                    except:
                        return None   
                def get_user_name(self, obj):
                    try:
                        return obj.user.username
                    except:
                        return None
        if not attempt_check:
            serializer = TestingAnswerQuestionSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                serialized_data = serializer.data
                item = TestingPurpose.objects.get(id=serialized_data["question_no"])
                selected_options = []
                if item.question_type == "2":
                    for i in serialized_data["answer"]:
                        selected_options.append(item.options[i])   
                elif item.question_type == "3":
                    selected_options = item.options[serialized_data["answer"]]       
                return Response({"data":serialized_data, "selected_option(s)":selected_options}, status=status.HTTP_201_CREATED)
            return Response({"erros":serializer.errors, "valid_options":TestingAnswerQuestionSerializer.valid_options}, status=status.HTTP_400_BAD_REQUEST)
        elif attempt_check:  
            serializer = TestingAnswerQuestionSerializer(attempt_check[0],data=request.data)
            if serializer.is_valid():
                serializer.save()
                serialized_data = serializer.data
                item = TestingPurpose.objects.get(id=serialized_data["question_no"])
                selected_options = []
                if item.question_type == "2":
                    for i in serialized_data["answer"]:
                        selected_options.append(item.options[i])
                elif item.question_type == "3":
                    selected_options = item.options[serialized_data["answer"]]       
                return Response({"data":serialized_data, "selected_option(s)":selected_options}, status=status.HTTP_201_CREATED)
            return Response({"erros":serializer.errors, "valid_options":TestingAnswerQuestionSerializer.valid_options}, status=status.HTTP_400_BAD_REQUEST)
        

# class TestingAttemptAnswer(APIView):
#     serializer_class = TestingAnswerQuestionSerializer
#     def post(self, request):
#         user = request.data["user"]
#         question_no = request.data["question_no"]
#         attempt_check = TestingAttemptQuestion.objects.filter(user_id=user).filter(question_no_id=question_no)
#         if not attempt_check:
#             qsn = TestingPurpose.objects.get(id=question_no)
#             if qsn.question_type == "3": #radio type question
#                 answer = request.data.get("answer")
#                 if answer in qsn.options:
#                     serializer = self.serializer_class(data=request.data)
#                     if serializer.is_valid():
#                         serializer.save()
#                         serialized_data = serializer.data
#                         return Response(serialized_data, status=status.HTTP_200_OK)
#                     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#                 else:
#                     return Response({"message":"This is not the valid option","valid options":qsn.options})
#             elif qsn.question_type == "1":   #text type question
#                 answer = request.data.get("answer")
#                 serializer = self.serializer_class(data=request.data)
#                 if serializer.is_valid():
#                     serializer.save()
#                     serialized_data = serializer.data
#                     return Response(serialized_data, status=status.HTTP_200_OK)
#                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#             elif qsn.question_type == "2":    #checkbox type question
#                 # answer = list(map(str, request.data.get('answer').split()))
#                 answer = request.data.get('answer',[])
#                 answer = ast.literal_eval(answer)
#                 invalid_options = []
#                 for i in answer:
#                     if i not in qsn.options:
#                         invalid_options.append(i)
#                 if invalid_options: 
#                     return Response({"message":f"Invalid option(s) selected:- {invalid_options}", "valid_options":qsn.options})
#                 serializer = self.serializer_class(data=request.data)    
#                 if serializer.is_valid():
#                     serializer.save()
#                     serialized_data = serializer.data
#                     for i in answer:
#                         selected_options.append(qsn.options[i])
#                     return Response({"data":serialized_data, "selected_options":selected_options}, status=status.HTTP_200_OK)
#                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         if attempt_check:
#             qsn = TestingPurpose.objects.get(id=question_no)
#             if qsn.question_type == "3":
#                 answer = request.data.get("answer")
#                 if answer in qsn.options:
#                     serializer = self.serializer_class(attempt_check[0],data=request.data)
#                     if serializer.is_valid():
#                         serializer.save()
#                         serialized_data = serializer.data
#                         return Response(serialized_data, status=status.HTTP_200_OK)
#                     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#                 else:
#                     return Response({"message":"This is not the valid option","valid options":qsn.options})
#             elif qsn.question_type == "1":
#                 answer = request.data.get("answer")
#                 serializer = self.serializer_class(attempt_check[0],data=request.data)
#                 if serializer.is_valid():
#                     serializer.save()
#                     serialized_data = serializer.data
#                     return Response(serialized_data, status=status.HTTP_200_OK)
#                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
#             elif qsn.question_type == "2":   
#                 # answer = list(map(str, request.data.get('answer').split(',')))
#                 answer = request.data.get('answer',[])
#                 answer = ast.literal_eval(answer)
#                 invalid_options = []
#                 for i in answer:
#                     if i not in qsn.options:
#                         invalid_options.append(i)
#                 if invalid_options: 
#                     return Response({"message":f"Invalid option(s) selected:- {invalid_options}", "valid_options":qsn.options})
#                 serializer = self.serializer_class(attempt_check[0],data=request.data)  
#                 if serializer.is_valid():
#                     serializer.save()
#                     serialized_data = serializer.data
#                     selected_options = []
#                     for i in answer:
#                         selected_options.append(qsn.options[i])
#                     return Response({"data":serialized_data, "selected_options":selected_options}, status=status.HTTP_200_OK)
#                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TestingEditQuestion(APIView):
    # permission_classes = (IsAdminUser,)
    serializer_class = TestingAddQuestionSerializer
    def get_object(self,id):
        try:
            return TestingPurpose.objects.get(id=id)
        except:
            raise Http404
    def get(self, request,id):
        item = self.get_object(id)
        serializer = self.serializer_class(item)
        serialized_data = serializer.data
        return Response(serialized_data, status=status.HTTP_200_OK)    
    def put(self, request, id):
        item = self.get_object(id)
        serializer = self.serializer_class(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, id):
        item = self.get_object(id)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class TestingDisplayAllQuestions(APIView):
    serializer_class = TestingAddQuestionSerializer
    def get(self, request):
        items = TestingPurpose.objects.all()
        serializer = self.serializer_class(items, many=True)
        serialized_data = serializer.data
        return Response(serialized_data, status=status.HTTP_200_OK)
    
class DisplayAnswersOfUser(APIView):
    serializer_class = TestingAttemptSerializer
    def get(self, request,id):
        ans = TestingAttemptQuestion.objects.filter(user_id=id)
        serializer = self.serializer_class(ans, many=True)
        serialized_data = serializer.data
        return Response(serialized_data, status=status.HTTP_200_OK)  

class AddTestingQuizQuestion(APIView):
    serializer_class = AddTestingQuizQuestionSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.validated_data
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AllTestingQuizQuestions(APIView):
    serializer_class = AddTestingQuizQuestionSerializer
    def get(self, request):
        qns = TestingQuizQuestion.objects.all()
        serializer = self.serializer_class(qns, many=True)
        serialized_data = serializer.data
        return Response(serialized_data, status=status.HTTP_200_OK)

class AddItems(APIView):
    serializer_class = TestinglistfieldSerializer
    def post(self, request):
        # items = request.data.getlist("items[]")
        colors = request.data.get('colors',[])
        # items = list(map(int, request.data.get("items").split(",")))
        print(colors,"-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            serialized_data = serializer.data
            return Response(serialized_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AllListItems(APIView):
    serializer_class = TestinglistfieldSerializer
    def get(self, request):
        items = Testinglistfield1.objects.all()
        serializer = self.serializer_class(items, many=True)
        serialized_data = serializer.data
        return Response(serialized_data, status=status.HTTP_200_OK)
    
class AddFriends(APIView):
    serializer_class = FriendSerializer
    def post(self, request):
        user = request.data.get("user")
        friends = request.data.get("friends")
        adding_user = User.objects.get(id=user)
        if user in friends:
            friends.remove(user)
        if not adding_user:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                serialized_data = serializer.data
                return Response(serialized_data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif adding_user:
            serializer = self.serializer_class(adding_user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                serialized_data = serializer.data
                return Response(serialized_data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class SignupView(APIView):
    # schema = AutoSchema(manual_fields=[
    #     coreapi.Field(
    #         "email",
    #         required=False,
    #         location="form",
    #         schema=coreschema.String()
    #     ),
    #     ])
    def post(self, request, format=None):
        pass