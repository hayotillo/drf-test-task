from django.conf.urls import url
from .views import *

urlpatterns = [
    # admin urls
    url('admin/login', view=AdminLogin.as_view()),
    url('admin/logout', view=AdminLogout.as_view()),
    # vote
    url(r'admin/vote/save/(?P<id>\d+)', view=AdminVoteManage.as_view({'post': 'save'})),
    url(r'admin/vote/save', view=AdminVoteManage.as_view({'post': 'save'})),
    url(r'admin/vote/delete/(?P<id>\d+)', view=AdminVoteManage.as_view({'post': 'delete'})),
    # vote quest
    url('admin/vote-quest/save', view=AdminVoteQuestManage.as_view({'post': 'save'})),
    url(r'admin/vote-quest/delete/(?P<id>\d+)', view=AdminVoteManage.as_view({'post': 'delete'})),
    # user urls
    url('user/vote/list', view=UserVoteList.as_view()),
    url(r'user/vote/answer/(?P<vote_id>\d+)/(?P<user_id>\d+)', view=UserAnswerVote.as_view({'get': 'answer'})),
    url(r'user/vote/statistic/(?P<user_id>\d+)', view=UserVoteStatistic.as_view())
]
