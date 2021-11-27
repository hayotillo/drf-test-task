from django.db import models


class Vote(models.Model):
    name = models.CharField(max_length=255, blank=False)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(blank=True)
    description = models.TextField(blank=True, null=True)


class VoteQuest(models.Model):
    quest = models.TextField(max_length=1000, blank=False)
    quest_type = models.CharField(max_length=12, blank=False)
    vote = models.ForeignKey(Vote, on_delete=models.CASCADE, related_name='quests', blank=False)


class AnswerText(models.Model):
    answer = models.TextField(max_length=1000, blank=False)
    vote = models.ForeignKey(Vote, on_delete=models.CASCADE)
    user_id = models.PositiveIntegerField(blank=False, default=0)


class AnswerSelect(models.Model):
    vote = models.ForeignKey(Vote, on_delete=models.CASCADE)
    user_id = models.PositiveIntegerField(blank=False, default=0)
    quests = models.ManyToManyField(VoteQuest, related_name='quests')
