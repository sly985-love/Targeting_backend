from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model, authenticate


# 1.重写模型对应的序列化器，指定返回的数据是什么，嵌套
# 2.返回一个字段的，通过source选项取代主键值
# 3.depth 深度找
class SoldierModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = Soldier
        fields = "__all__"
        # fields = ['id', 'name', 'army', 'telephone', "achievement"]


class InstructorModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = Instructor
        fields = "__all__"


class TargetModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = "__all__"
        depth = 1


class AchievementModelSerializers(serializers.ModelSerializer):
    # 如果自定义外键的话，要求提交post请求也要传来这两个数据
    # target_name = serializers.CharField(source="target.name")
    # instructor_name=serializers.CharField(source="target.instructor.name")

    class Meta:
        model = Achievement
        fields = "__all__"
        read_only_fields = ('id',)  # id 上传时间 是无法更改的
        extra_kwargs = {'user': {'read_only': True}, 'atarget': {'read_only': True},
                        'goshooting': {'read_only': True}}  # user也是不能更改，由于user不是一个field，而是一个映射关系
        depth = 2


class GoshootingModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = Goshooting
        fields = "__all__"
        depth = 2
        read_only_fields = ('id',)  # id 上传时间 是无法更改的
        extra_kwargs = {'user': {'read_only': True},
                        'target': {'read_only': True}, }  # user也是不能更改，由于user不是一个field，而是一个映射关系


class PhotoModelSerializers(serializers.ModelSerializer):
    # Meta中定义需要拿出哪些photo model里面的字段
    class Meta:
        model = Photo
        fields = ('id', 'score', 'direction', 'created_time', 'user', 'image')
        read_only_fields = ('id', 'created_time')  # id 上传时间 是无法更改的
        extra_kwargs = {'user': {'read_only': True}}  # user也是不能更改，由于user不是一个field，而是一个映射关系


# 用户序列化
class UserModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'name', 'army', 'telephone', 'password')

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

    # 更改用户所在部队
    def update(self, instance, validated_data):
        army = validated_data.pop('army', None)
        user = super().update(instance, validated_data)
        if army:
            user.set_army(army)
            user.save()
        return user


# tokenserializer
class AuthTokenSerializer(serializers.Serializer):
    # 需要两个输入：用户的姓名密码（部队），用户输入一次就能拿到可以使用很多次的token（钥匙）
    name = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'},
                                     trim_whitespace=False)  # trim_whitespace=False字符串修正

    def validate(self, attrs):
        name = attrs.get('name')
        password = attrs.get('password')
        # authenticate会拿到，姓名和密码帮你验证，这个姓名和密码是不是当前http request这个人的
        user = authenticate(requests=self.context.get('request'), username=name, password=password)
        # 如果是就会返回用户信息，如果不是（当前姓名和密码信息，和你当前操作的用户信息不符合）
        if not user:
            msg = "Unable to authenticate with provided credentials"
            raise serializers.ValidationError(msg, code='authorization')
        attrs['user'] = user
        return attrs


class SelectTargetModelSerializers(serializers.ModelSerializer):
    # 如果自定义外键的话，要求提交post请求也要传来这两个数据
    # target_name = serializers.CharField(source="target.name")
    # instructor_name=serializers.CharField(source="target.instructor.name")

    class Meta:
        model = SelectTarget
        fields = "__all__"
        depth = 2
