from django.utils import timezone

from linetoken.models import LINEToken

from datetime import timedelta
import requests
import os


def issue_token():
    """Issue LINE Token. Return access token and expired datetime of token"""
    r = requests.post(
        "https://api.line.me/v2/oauth/accessToken",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "grant_type": "client_credentials",
            "client_id": f"{os.getenv('LINE_BOT_CHANNEL_ID')}",
            "client_secret": f"{os.getenv('LINE_BOT_CHANNEL_SECRET')}",
        },
    )

    res = r.json()
    return res["access_token"], timezone.now() + timedelta(seconds=res["expires_in"])


def get_token():
    """Get LINE Access Token. Either from model or issue new token"""
    try:
        obj = LINEToken.objects.latest()
    except:
        obj = None

    # Request new token
    if not obj or obj.expires_at < timezone.now():
        token, expired_at = issue_token()
        obj = LINEToken.objects.create(token=token, expired_at=expired_at)
    return obj.token
