from rest_framework import serializers
from .models import *


class VoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vote
        fields = ('id', 'name', 'start_date', 'end_date', 'description')

    def update(self, instance, validated_data):
        del validated_data['start_date']
        return super().update(instance=instance, validated_data=validated_data)


class VoteQuestSerializer(serializers.ModelSerializer):

    class Meta:
        model = VoteQuest
        fields = ('id', 'vote', 'quest', 'quest_type')

    def validate_quest_type(self, value):
        if value not in ['text', 'select', 'multiselect']:
            raise serializers.ValidationError({'quest_type': '"quest_type" parameter allowed only "text", "select" and "multiselect"!'})
        return value


class UserVoteListSerializer(serializers.ModelSerializer):
    quests = serializers.SerializerMethodField()

    def get_quests(self, vote):
        quest_list = []
        quests = VoteQuest.objects.filter(vote_id=vote.id).all()
        for quest in quests:
            quest_list.append({
                'id': quest.id,
                'quest': quest.quest,
                'quest_type': quest.quest_type,
            })

        return quest_list

    class Meta:
        model = Vote
        fields = ('id', 'name', 'start_date', 'end_date', 'description', 'quests')


class UserVoteDetailListSerializer(serializers.ModelSerializer):
    answer = serializers.SerializerMethodField()

    def get_answer(self, vote):
        # quest_list = []
        # quests = VoteQuest.objects.filter(vote_id=vote.id).all()
        # for quest in quests:
        #     quest_list.append({
        #         'id': quest.id,
        #         'quest': quest.quest,
        #         'quest_type': quest.quest_type,
        #     })
        #
        # return quest_list
        pass

    class Meta:
        model = Vote
        fields = ('id', 'name', 'start_date', 'end_date', 'description', 'quests')
