from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone

from user.models import LINEUser
from webhook.models import MentionData

from datetime import timedelta


def index(request):
    token = request.GET['token']
    try:
        line_user = LINEUser.objects.get(
            token = token
        )
    except:
        return JsonResponse({
            'details' : 'Token Invalid'
        }, status = 401)

    mention_data = MentionData.objects.filter(
        requester = line_user,
        created_at__gte = timezone.now() - timedelta(seconds=5)
    )

    members = []

    if len(mention_data) > 0:
        mention_data = mention_data[0]
        members = mention_data.member_name.split(',')
        
    return JsonResponse({
        'members' : members
    })