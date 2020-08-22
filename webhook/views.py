from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from webhook.decorators import verify_from_line
from webhook.utils import send_reply, get_group_display_name, get_room_display_name
from user.models import LINEUser
from groups.models import LINEGroup, LINEGroupMember
from webhook.models import MentionData

import json


@csrf_exempt
@verify_from_line
def index(request):
    data = json.loads(request.body)

    for event_data in data['events']:
        if event_data['type'] == 'follow':
            # Remove all previouse LINE User
            LINEUser.objects.filter(
                userid = event_data['source']['userId']
            ).delete()

            user = LINEUser.objects.create(
                userid = event_data['source']['userId']
            )

            send_reply(f"Token kamu adalah : {user.token}", event_data['replyToken'])

        # Create new group
        if event_data['type'] == 'join':
            if event_data['source']['type'] == 'group':
                groupid = event_data['source']['groupId']
                type = 'group'
            else:
                groupid = event_data['source']['roomId']
                type = 'room'

            try: 
                LINEGroup.objects.get(
                    groupid = groupid,
                    type = type
                )
            except:
                LINEGroup.objects.create(
                    groupid = groupid,
                    type = type
                )
            
        if event_data['type'] == 'memberJoined':
            groupid = None
            if event_data['source']['type'] == 'group':
                groupid = event_data['source']['groupId']
            elif event_data['source']['type'] == 'room':
                groupid = event_data['source']['roomId']

            if groupid:
                line_group = LINEGroup.objects.get(groupid = groupid)
                for member in event_data['joined']['members']:
                    if member['type'] == 'user':
                        try:
                            LINEGroupMember.objects.get(
                                group = line_group,
                                userid = member['userId']
                            )
                        except:
                            LINEGroupMember.objects.create(
                                group = line_group,
                                userid = member['userId']
                            )
            
        if event_data['type'] == 'message':
            groupid = None
            if event_data['source']['type'] == 'group':
                groupid = event_data['source']['groupId']
            elif event_data['source']['type'] == 'room':
                groupid = event_data['source']['roomId']

            if groupid:
                try:
                    line_group = LINEGroup.objects.get(groupid = groupid)
                except:
                    # Create group if not exist
                    if event_data['source']['type'] == 'group':
                        groupid = event_data['source']['groupId']
                        type = 'group'
                    else:
                        groupid = event_data['source']['roomId']
                        type = 'room'

                    try: 
                        line_group = LINEGroup.objects.get(
                            groupid = groupid,
                            type = type
                        )
                    except:
                        line_group = LINEGroup.objects.create(
                            groupid = groupid,
                            type = type
                        )
                # Add LINE User ID to Group Data
                if 'userId' in event_data['source']:
                    try:
                        LINEGroupMember.objects.get(
                            group = line_group,
                            userid = event_data['source']['userId']
                        )
                    except:
                        LINEGroupMember.objects.create(
                            group = line_group,
                            userid = event_data['source']['userId']
                        )

                if event_data['message']['text'] == 'mentionAll':
                    try:
                        user = LINEUser.objects.get(
                            userid = event_data['source']['userId']
                        )

                        member = []
                        group_members = LINEGroupMember.objects.filter(
                            group = line_group
                        )
                        for group_member in group_members:
                            if group_member.userid != event_data['source']['userId']:
                                if line_group.type == 'group':
                                    display_name = get_group_display_name(groupid, group_member.userid)
                                else:
                                    display_name = get_room_display_name(groupid, group_member.userid)
                                member.append(display_name)
                                
                        MentionData.objects.create(
                            requester = user,
                            member_name = ",".join(member)
                        )

                    except:
                        pass

    return HttpResponse()

