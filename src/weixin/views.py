import hashlib
import xml.etree.ElementTree as ET

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import Message, Event, PublicAccount


@csrf_exempt
def weixin(request, user_id, token):
    user = get_object_or_404(User, id=user_id)
    public_account = get_object_or_404(PublicAccount, user=user, token=token)

    signature = request.REQUEST.get('signature', None)
    timestamp = request.REQUEST.get('timestamp', None)
    nonce = request.REQUEST.get('nonce', None)
    echostr = request.REQUEST.get('echostr', None)

    if timestamp and nonce:
        list = [public_account.token, timestamp, nonce]
        list.sort()
        sha1 = hashlib.sha1()
        map(sha1.update, list)
        hashcode = sha1.hexdigest()

        if hashcode == signature:
            if public_account.connect_status == False:
                public_account.connect_status = True
                public_account.save()

            if request.method == 'GET':
                return HttpResponse(echostr)
            else:
                handle_weixin_request(request, public_account)

    return HttpResponse('error')


def handle_weixin_request(request, public_account):
    xml_string = request.body
    xml = ET.fromstring(xml_string)

    to_user_name = xml.find('ToUserName').text
    from_user_name = xml.find('FromUserName').text
    create_time = xml.find('CreateTime').text
    msg_type = xml.find('MsgType').text

    if msg_type == 'event':
        event_type = xml.find('Event').text
        event = Event(
            public_account = public_account,
            to_user_name=to_user_name,
            from_user_name=from_user_name,
            create_time=create_time,
            event_type=event_type,
            xml_content=xml_string
        )
        event.save()

    else:
        msg_id = xml.find('MsgId').text
        message = Message(
            public_account = public_account,
            to_user_name=to_user_name,
            from_user_name=from_user_name,
            create_time=create_time,
            msg_type=msg_type,
            msg_id=msg_id,
            xml_content=xml_string
        )
        message.save()

    return HttpResponse('success')
