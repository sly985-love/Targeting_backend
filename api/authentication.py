from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed

import time
from datetime import timedelta
from django.utils import timezone
from django.conf import settings


# 将能够使得28天之后失效的token 功能写进去
# if token is expired, it be will replaced by the new token
# and new one with different key will be created
def token_expire_handler(token):
    time_elapsed = timezone.now() - token.created  # 从token创建到现在一共过了多少天
    left_time = timedelta(  # 如果超过了我们设置变量的28天，那我们让is_expired变量变为true
        seconds=settings.TOKEN_EXPIRED_AFTER_SECONDS) - time_elapsed

    is_expired = left_time < timedelta(seconds=0)
    if is_expired:  # 那我们让is_expired变量变为true
        token.delete()
        token = Token.objects.create(user=token.user)  # token失效就delet，并让django后台给user一个新的token

    token_expired_time = token.created + \
                         timedelta(seconds=settings.TOKEN_EXPIRED_AFTER_SECONDS)  # token失效的时间=token创建时间+28天
    token_expired_timestamp = int(
        time.mktime(token_expired_time.timetuple()))
    return is_expired, token, token_expired_timestamp  # 返回


# 可失效的token的验证方式
class ExpiringTokenAuthentication(TokenAuthentication):
    """
    If token is expired then it will be removed
    and new one with different key will be created
    """  # 如果这个token失效会被删除，然后会有一个新的token

    def authenticate_credentials(self, key):
        try:
            token = Token.objects.get(key=key)
        except Token.DoesNotExist:  # token不存在
            raise AuthenticationFailed("Invalid Token")

        if not token.user.is_active:  # 这个token对应的user是不是一个已经激活的用户
            raise AuthenticationFailed("User is not active")

        is_expired, token, token_expired_timestamp = token_expire_handler(  # 判断token是否失效，返回是否失效，token，失效日期
            token)
        if is_expired:
            raise AuthenticationFailed("The Token is expired")  # token失效
        return (token.user, token)  # 返回user和token本身
