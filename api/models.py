from django.conf import settings
from django.db import models
from django.utils import timezone as datetime

# Create your models here.
# 战士 1
# 成绩 n n
# 靶位   1 n
# 指导员   1
# 用户

# _____________________________________________________
# 战士信息表
from api.photo_model import PhotoBase
from api.user_model import UserManagerBase, UserBase


class Soldier(models.Model):
    """战士信息"""
    name = models.CharField(max_length=50, verbose_name='战士姓名', help_text='战士姓名')
    army = models.CharField(max_length=50, verbose_name='战士所在部队')
    telephone = models.CharField(max_length=20, verbose_name='战士联系方式')

    class Meta:
        db_table = "soldier"

    def __str__(self):
        return self.name

    # @property  # 自定义模型方法属性方法
    # def achievement(self):
    #     return self.achievement.value("target__name", "score")


# 指导员信息表
class Instructor(models.Model):
    name = models.CharField(max_length=50, verbose_name='指导员姓名')
    army = models.CharField(max_length=50, verbose_name='指导员所在部队')
    telephone = models.CharField(max_length=20, verbose_name='指导员联系方式')
    type_choices = (
        (0, '普通指导员'),
        (1, '超级指导员'),
    )
    type = models.IntegerField(verbose_name='指导员等级', default=0, choices=type_choices)

    # type_choices = ((0, '普通指导员'), (1, '超级指导员'),)
    # type = models.IntegerField(verbose_name='指导员等级', default=0, choices=type_choices)

    class Meta:
        db_table = "instructor"

    def __str__(self):
        return self.name


# 靶位信息表
class Target(models.Model):
    name = models.CharField(max_length=50, verbose_name='靶位名称')

    # type_choices = ((0, '未使用'), (1, '使用中'),)
    # type = models.IntegerField(verbose_name='靶位使用状态', default=0, choices=type_choices)
    type_choices = (
        (0, '未使用'),
        (1, '使用中'),
    )
    type = models.IntegerField(verbose_name='靶位使用状态', default=0, choices=type_choices)

    class Meta:
        db_table = "target"

    def __str__(self):
        return self.name


# 战士打靶表
class Goshooting(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # on_delete=models.CASCADE用户被删除图片也被删除
    start_dtime = models.DateTimeField(default='', auto_created=datetime.now(), verbose_name='打靶开始时间')
    end_dtime = models.DateTimeField(default='', auto_created=datetime.now(), verbose_name='打靶结束时间')
    shooting_data = models.DateField(default='', verbose_name='打靶日期')
    gtarget = models.ForeignKey(Target, on_delete=models.DO_NOTHING, related_name='gtarget', db_constraint=False)

    class Meta:
        db_table = "go_shooting"

    def __str__(self):
        return str(self.shooting_data)


# 打靶成绩表
class Achievement(models.Model):
    score = models.DecimalField(default=0, max_length=4, decimal_places=1, max_digits=10, verbose_name="打靶环值")
    direction = models.CharField(default='', max_length=50, verbose_name='打靶方位')
    # solider = models.ForeignKey(Soldier, on_delete=models.DO_NOTHING, related_name='soldier',
    #                             db_constraint=False)  # 虚拟外键，不在mysql类刷新检测
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # on_delete=models.CASCADE用户被删除图片也被删除
    atarget = models.ForeignKey(Target, on_delete=models.DO_NOTHING, related_name='atarget', db_constraint=False)
    creat_dtime = models.DateTimeField(default='', auto_created=datetime.now(), verbose_name='成绩生成时间')
    simage = models.ImageField(null=True, upload_to='spic/', verbose_name='真实靶图')
    vimage = models.ImageField(null=True, upload_to='vpic/', verbose_name='虚拟靶图')
    goshooting = models.ForeignKey(Goshooting, on_delete=models.DO_NOTHING, related_name='goshooting',
                                   db_constraint=False)

    class Meta:
        db_table = "achievement"

    def __str__(self):
        return str(self.score)


# 不在此处写具体逻辑，为了models.py的简洁性
class UserManager(UserManagerBase):
    pass


class User(UserBase):
    pass


class Photo(PhotoBase):
    pass


class SelectTarget(models.Model):
    solider = models.ForeignKey(Soldier, on_delete=models.DO_NOTHING, related_name='soldier',
                                db_constraint=False)  # 虚拟外键，不在mysql类刷新检测
    target = models.ForeignKey(Target, on_delete=models.DO_NOTHING, related_name='target', db_constraint=False)
    creat_dtime = models.DateTimeField(default='', auto_created=datetime.now(), verbose_name='成绩生成时间')
    start_dtime = models.DateTimeField(default='', auto_created=datetime.now(), verbose_name='打靶开始时间')
    end_dtime = models.DateTimeField(default='', auto_created=datetime.now(), verbose_name='打靶结束时间')
    shooting_data = models.DateField(default='', verbose_name='打靶日期')
    simage = models.ImageField(null=True, upload_to='spic/', verbose_name='真实靶图')
    vimage = models.ImageField(null=True, upload_to='vpic/', verbose_name='虚拟靶图')
    score = models.CharField(default='', max_length=10, verbose_name='打靶成绩')  # 打靶成绩
    direction = models.CharField(default='', max_length=50, verbose_name='打靶方位')  # , verbose_name='打靶方位'

    class Meta:
        db_table = "select_target"
        unique_together = ('solider', 'target',)

    def __str__(self):
        return str(self.score)
