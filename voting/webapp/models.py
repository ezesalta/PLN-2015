from django.db import models
from iepy.data.models import Entity
from django.contrib import admin
from django.utils import timezone
from django.contrib.auth.models import User


class Law(models.Model):
    id = models.AutoField(primary_key=True)
    expedient = models.CharField(max_length=20)
    #expedient = models.ForeignKey(Entity, on_delete=models.CASCADE, unique=True)
    #law = models.TextField(max_length=300, unique=True)
    law = models.ForeignKey(Entity, on_delete=models.CASCADE, unique=True)
    status = models.BooleanField(default=0)
    date = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.law.key


class Question(models.Model):
    id = models.AutoField(primary_key=True)
    law = models.ForeignKey(Law, on_delete=models.CASCADE)
    question = models.TextField(max_length=300)
    date = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.question


class Vote(models.Model):
    id = models.AutoField(primary_key=True)
    vote = models.CharField(max_length=20)

    def __str__(self):
        return self.vote


class Choice(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Vote, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now())


class Voting(models.Model):
    id = models.AutoField(primary_key=True)
    law = models.ForeignKey(Law, on_delete=models.CASCADE)
    person = models.ForeignKey(Entity, on_delete=models.CASCADE)
    vote = models.ForeignKey(Vote, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now())


class LawAdmin(admin.ModelAdmin):
    pass


class QuestionAdmin(admin.ModelAdmin):
    pass


class VoteAdmin(admin.ModelAdmin):
    pass


class ChoiceAdmin(admin.ModelAdmin):
    pass


class VotingAdmin(admin.ModelAdmin):
    pass

admin.site.register(Law, LawAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Vote, VoteAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Voting, VotingAdmin)
