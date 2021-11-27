from datetime import datetime
from django.http import JsonResponse
from django.contrib.auth import logout
from rest_framework import viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAdminUser
from .models import *
from .serializers import *


# user login and logout
class AdminLogin(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(AdminLogin, self).post(request=request, args=args, kwargs=kwargs)
        token = Token.objects.get(key=response.data['token'])
        return JsonResponse({'token': token.key})


class AdminLogout(ObtainAuthToken):
    def get(self, request):
        if request.user.is_authentificated:
            request.user.auth_token.delete()
            logout(request)
        return JsonResponse({'result': True})


# vote manage
class AdminVoteManage(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]

    def save(self, request, **kwargs):
        vote = Vote.objects.filter(pk=kwargs.get('id')).first()
        serializer = VoteSerializer(instance=vote, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        else:
            return JsonResponse(serializer.errors)

        return JsonResponse(serializer.data)

    def delete(self, request, **kwargs):
        result = False
        vote = Vote.objects.filter(pk=kwargs.get('id')).first()
        if vote:
            vote.delete()
            result = True

        return JsonResponse({'is_deleted': result})


# vote quest manage
class AdminVoteQuestManage(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]

    def save(self, request, **kwargs):
        vote_quest = VoteQuest.objects.filter(pk=kwargs.get('id')).first()

        serializer = VoteQuestSerializer(instance=vote_quest, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        else:
            return JsonResponse(serializer.errors)

        VoteQuest.objects.filter(
            vote_id=request.data.get('vote')
        ).update(quest_type=request.data.get('quest_type'))

        return JsonResponse(serializer.data)

    def delete(self, request, **kwargs):
        result = False
        vote_quest = VoteQuest.objects.filter(pk=kwargs.get('id')).first()
        if vote_quest:
            vote_quest.delete()
            result = True

        return JsonResponse({'is_deleted': result})


# vote list for user
class UserVoteList(ListAPIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        current_time = datetime.now()
        queryset = Vote.objects.filter(start_date__lte=current_time, end_date__gte=current_time).order_by('end_date')
        serializer = UserVoteListSerializer(instance=queryset, many=True)
        return JsonResponse(serializer.data, safe=False)


class UserAnswerVote(viewsets.ModelViewSet):
    permission_classes = [AllowAny]

    def answer(self, request, **kwargs):
        answer = request.data.get('answer', False)
        vote_id = kwargs.get('vote_id')
        user_id = kwargs.get('user_id', 0)
        vote = Vote.objects.filter(pk=vote_id).first()
        if vote and vote.quests.count() > 0 and answer:
            quest_type = vote.quests.first().quest_type

            if quest_type in ['select', 'multiselect']:
                if quest_type == 'multiselect':
                    quest_ids = [int(a.strip()) for a in answer.split(',')]
                else:
                    quest_ids = [int(answer.strip())]

                select_answer = AnswerSelect.objects.filter(
                    user_id=user_id, vote_id=vote_id
                ).first()

                if not select_answer:
                    select_answer = AnswerSelect.objects.create(user_id=user_id, vote_id=vote_id)

                select_answer.quests.set(VoteQuest.objects.filter(pk__in=quest_ids))

            else:
                AnswerText.objects.update_or_create(
                    defaults={'answer': str(answer)},
                    user_id=user_id, vote_id=vote_id
                )

        return JsonResponse({'vote': vote.name, 'your answer': answer})


class UserVoteStatistic(ListAPIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        text_answers = []
        select_answers = []
        user_id = kwargs.get('user_id')
        answer_texts = AnswerText.objects.filter(user_id=user_id).order_by('vote_id')
        answer_selects = AnswerSelect.objects.filter(user_id=user_id).order_by('vote_id')
        for answer_text in answer_texts:
            text_answers.append({
                'vote_id': answer_text.vote_id,
                'vote_name': answer_text.vote.name,
                'answer_text': answer_text.answer,
            })
        for answer_select in answer_selects:
            select_answers.append({
                'vote_id': answer_select.vote_id,
                'vote_name': answer_select.vote.name,
                'selected': [q.quest for q in answer_select.quests.all()]
            })

        return JsonResponse({'text_answers': text_answers, 'select_answers': select_answers})
