from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class UserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_active')

class QuestionAdmin(admin.ModelAdmin):
    # inlines = [AnswerQuestionAInline]
    list_display = ('question', 'question_type')
    radio_fields = {'question_type': admin.VERTICAL}   

class AnswerQuestionAdmin(admin.ModelAdmin):
    list_display = ('user', 'answered_question','answer') 
    def answered_question(self,obj):
        try:
            return obj.question_no.question
        except:
            return "Error!!"
        
class QuizAnswersSheetAdmin(admin.ModelAdmin):
    list_display = ('check_question','quiz_question_ans')        

class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ('quiz_question', 'quiz_question_type')
    radio_fields = {'quiz_question_type': admin.VERTICAL}

class AnswerQuizQuestionAdmin(admin.ModelAdmin):
    list_display = ('user', 'answered_question','quiz_answer') 
    def answered_question(self,obj):
        try:
            return obj.quiz_question_no.quiz_question
        except:
            return "Error!!"
        
class ScoreOfCandidateAdmin(admin.ModelAdmin):
    list_display = ("candidate", "marks_obtained", "Total_marks") 
    readonly_fields = ["marks_obtained","Unattempted_ques","total_ques_attempted", "Total_marks"]       
    ordering = ('-marks_obtained',)

class RankingAdmin(admin.ModelAdmin):
    list_display = ('user_name','marks_obtained','rank')
    ordering = ("rank",)
    def user_name(self, obj):
        try:
            return obj.user.username
        except:
            return "None!!"    
        
class TempQuizAnswerAdmin(admin.ModelAdmin):
    list_display = ("question","answer")     
    ordering = ("question",)

class TempQuizAdmin(admin.ModelAdmin):
    list_display = ("user_name","question", "answer","answer_check")
    def user_name(self, obj):
        try:
            return obj.user.username
        except:
            return "None!!"

class ContendersAdmin(admin.ModelAdmin):
    list_display = ("username","email")    

class TempScoreofCandidateAdmin(admin.ModelAdmin):
    list_display = ("username","marks_obtained")    
    def username(self, obj):
        try:
            return obj.user.username
        except:
            return None 
        
class TestingPurposeAdmin(admin.ModelAdmin):
    list_display = ("question","question_type")        

class TestingAttemptQuestionAdmin(admin.ModelAdmin):
    list_display = ('user', 'answered_question','answer') 
    def answered_question(self,obj):
        try:
            return obj.question_no.question
        except:
            return None 

class TestingQuizQuestionAdmin(admin.ModelAdmin):
    list_display = ('quiz_question','quiz_question_type')
       
class Testinglistfield1Admin(admin.ModelAdmin):
    list_display = ('chars','extra_info')       

class FriendAdmin(admin.ModelAdmin):
    list_display = ('user', 'all_friends')    
    def all_friends(self, obj):
        try:
            return ', '.join([i.username for i in obj.friends.all()])
        except:
            return None

admin.site.register(Question, QuestionAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(AnswerQuestion, AnswerQuestionAdmin)
admin.site.register(QuizQuestion, QuizQuestionAdmin)
admin.site.register(AnswerQuizQuestion, AnswerQuizQuestionAdmin)
admin.site.register(QuizAnswersSheet, QuizAnswersSheetAdmin)
admin.site.register(ScoreOfCandidate, ScoreOfCandidateAdmin)
admin.site.register(Ranking, RankingAdmin)
admin.site.register(TempQuizAnswer, TempQuizAnswerAdmin)
admin.site.register(TempQuiz, TempQuizAdmin)
admin.site.register(Contenders, ContendersAdmin)
admin.site.register(TempScoreofCandidate, TempScoreofCandidateAdmin)
admin.site.register(TestingPurpose, TestingPurposeAdmin)
admin.site.register(TestingAttemptQuestion, TestingAttemptQuestionAdmin)
admin.site.register(TestingQuizQuestion, TestingQuizQuestionAdmin)
admin.site.register(Testinglistfield1, Testinglistfield1Admin)
admin.site.register(Friend, FriendAdmin)