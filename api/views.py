from django.shortcuts import render
# Create your views here.
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

from .authentication import ExpiringTokenAuthentication, token_expire_handler
from .models import *
from .serializers import *
from .models import *
from .serializers import PhotoModelSerializers
# from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework import generics, permissions, authentication, status
from rest_framework.settings import api_settings
from rest_framework.authtoken.views import ObtainAuthToken
# from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


# from io import BytesIO
#
# from django.core.files.base import ContentFile
#
# from PIL import Image, ImageDraw, ImageFont


class SoldierModelViewSet(ModelViewSet):
    """
    战士信息模型
    create:添加一个战士信息
    read:查询一个战士信息
    """
    queryset = Soldier.objects.all()
    serializer_class = SoldierModelSerializers
    # 过滤查询（即可以根据什么查询）
    # 单个字段过滤:GET / api / soldier /?telephone = 13780546889
    # http: // 127.0.0.1: 8000 / api / soldier /?telephone = 13780546889
    # 多个字段过滤（xx=xx&xx=xx）
    # （1.1）局部配置过滤
    # filter_backends = [DjangoFilterBackend]
    # （1.2）全局配置过滤
    # REST framework会在请求的查询字符串参数中检查是否包含了ordering参数，如果包含了ordering参数，
    # 则按照ordering参数指明的排序字段对数据集进行排序,前端可以传递的ordering参数的可选字段值需要在ordering_fields中指明
    filter_fields = ['id', 'name', 'army', 'telephone']
    # 排序:http: // 127.0.0.1: 8000 / api / soldier /?ordering = id
    # -id 表示针对id字段进行倒序排序
    # id 表示针对id字段进行升序排序
    # （1-2）一般过滤和排序都是用局部:如果需要在过滤以后再次进行排序，则需要两者结合!
    # 全局配置下的过滤组件不能和排序组件一起使用，只支持局部配置的过滤组件和排序组件一起使用。
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    # （2.1）局部配置排序
    # filter_backends=[OrderingFilter]
    # （2.2）全局配置排序
    ordering_fields = ['id', 'telephone']

    # （3.1）全局配置分页（关闭）：关闭来自全局配置中的分页信息，默认全局配置已经在setting中开启
    # pagination_class = None
    # （3.2）局部配置分页（一定要先注释掉全局配置） PAGE_SIZE在setting中设置， 当然以上所有组件都可以自定义
    # pagination_class = PageNumberPagination

    # 登录
    # http://127.0.0.1:8000/api/soldier/user/login/
    @action(methods=['get'], detail=False, url_path='user/login')
    def login(self, request):
        return Response({"msg": "登陆成功"})

    # 用户登录历史记录
    @action(methods=['get'], detail=False, url_path='user/login/log')
    def login_log(self, request, pk):
        return Response({"msg": "用户登录历史记录"})


class InstructorModelViewSet(ModelViewSet):
    queryset = Instructor.objects.all()
    serializer_class = InstructorModelSerializers
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filter_fields = ['id', 'name', 'army', 'telephone']
    ordering_fields = ['id']


class TargetModelViewSet(ModelViewSet):
    queryset = Target.objects.all()
    serializer_class = TargetModelSerializers
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filter_fields = ['id', 'name', 'type']
    ordering_fields = ['id']


class GoshootingModelViewSet(ModelViewSet):
    queryset = Goshooting.objects.all()
    serializer_class = GoshootingModelSerializers
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filter_fields = ['id', 'name', 'type', 'user_id', 'gtarget', 'shooting_data', 'end_dtime', 'start_dtime']
    ordering_fields = ['id', 'name', 'type', 'user_id', 'gtarget', 'shooting_data', 'end_dtime', 'start_dtime']


class AchievementModelViewSet(ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementModelSerializers
    # filter_fields = '__all__'
    filter_fields = ['id', 'creat_dtime', 'score', 'user_id', ]
    ordering_fields = ['id', 'creat_dtime', 'score', ]
    filter_backends = [DjangoFilterBackend, OrderingFilter]

    # 当前用户近五天成绩（日期数组，环数数组，每天平均环数，平均方向，最多环数）
    # http://127.0.0.1:8000/api/soldier/achievement/fivehistory/
    @action(methods=['get'], detail=False, url_path='fivehistory')
    def fivedayscore(self, request):
        # 先获取当前战士的近五天所有成绩（25条）
        queryset = self.queryset.filter(user=self.request.user)
        queryset = queryset.order_by('-creat_dtime')[:25]
        five_serializer = AchievementModelSerializers(queryset)
        return Response(five_serializer.data)

    # 返回用户当天成绩（即5条成绩）
    # http://127.0.0.1:8000/api/soldier/achievement/nowdayscore/
    @action(methods=['get'], detail=False, url_path='nowdayscore')
    def nowdayscore(self, request):
        queryset = self.queryset.filter(user=self.request.user)
        queryset = queryset.order_by('-creat_dtime')[:5]
        now_serializer = AchievementModelSerializers(queryset)
        return Response(now_serializer.data)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        if not serializer.is_valid():  # 判断从http得到的用户上传信息是否正确
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # photo_data = serializer.save(user=self.request.user)
        # # 拿到图片地址，然后跑这个模型
        # img_path = photo_data.image.path
        # print(img_path)
        # detector = ShootingScoreDetector(img_path)
        # result = detector.getholescore()
        # result = [[0, '偏右下方', 8.58], [1, '偏左下方', 9.03], [2, '偏右上方', 9.73], [3, '偏右上方', 9.37], [4, '偏右下方', 6.61],
        #           [5, '偏右下方', 10.01]]
        result = [[0, '偏右下方', 8.58], ]
        print("Predicted result: ", result)  # 在django中将识别结果打印出来
        # result[[num,score,direction],....]
        print(len(result))
        for i in range(0, len(result)):
            print(i)
            photo_data = serializer.save(user=self.request.user)
            photo_data.direction = result[i][1]
            photo_data.score = result[i][2]
            print(result[i][1], result[i][2])
            photo_data.save()
            photo_serializer = PhotoModelSerializers(photo_data)
            print("serializer data: ", photo_serializer.data)
            return Response(photo_serializer.data, status=status.HTTP_201_CREATED)  # 将photomodel的所有字段返回到前端


# # 设置单独不同的认证方式,401未认证，403权限被禁止,token认证更优秀
# class HomeView(APIView):
#     # authentication_classes = [SessionAuthentication, BasicAuthentication]
#     # 单独设置认证方式
#
#     def get(self, request):
#         print(request.user)
#         # 在中间件AuthenticationMiddleware中完成用户身份识别的，如果没有登陆，request.user值为AnonymousUser
#         if request.user.id is None:
#             return Response("未登录用户：游客")
#         else:
#             return Response(f"已登录用户：{request.user}")
#         # return Response({"msg": "ok"})

# 用户视图
# 创建一个用户
class CrerateUserView(generics.CreateAPIView):
    serializer_class = UserModelSerializers


# 查询一个用户的信息，更改一个用户的信息
class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserModelSerializers
    permission_classes = (permissions.IsAuthenticated,)  # 输入密码，更改信息必须是已登录用户

    # 修改得到用户信息
    # authentication_classes = (ExpiringTokenAuthentication,)  # django不要再用你默认的的用户认证模式了，用我写的

    def get_object(self):
        return self.request.user


# 查询所有用户的信息
class ListUserView(generics.ListAPIView):
    serializer_class = UserModelSerializers
    queryset = User.objects.all()


# tokenview
# 需要有一个新的网址，用户可以通过这个网址输入姓名和密码得到一个token（钥匙）
class CreateTokenView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    # 查询token若失效要求django给一个新的token
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']  # 让django后端知道当前的user是谁
        token, created = Token.objects.get_or_create(user=user)  # user对应的token和token创建的时间

        is_expired, token, token_expired_timestamp = token_expire_handler(
            token)
        return Response({  # 以http request的形式反馈给前端
            'user_id': user.id,
            'token': token.key,
            'token_expired_timestamp': token_expired_timestamp})


# photoview
class PhotoModelViewSet(ModelViewSet):
    serializer_class = PhotoModelSerializers
    queryset = Photo.objects.all()  # 看所有用户上传的信息
    # authentication_classes = (ExpiringTokenAuthentication,)# 只有拿到token才能访问
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        # 只返回当前用户上传的图片以及检测结果信息
        queryset = self.queryset.filter(user=self.request.user)
        # 最后上传的5张图片排序
        if self.action == 'list':
            queryset = queryset.order_by('-created_time')[:5]
        return queryset
        # return Photo.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SelectTargetModelViewSet(ModelViewSet):
    queryset = SelectTarget.objects.all()
    serializer_class = SelectTargetModelSerializers
