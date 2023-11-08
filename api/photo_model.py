from django.db import models
from django.conf import settings
import uuid
import os


# 用户上传的图片我们存在django的哪个地方：uploads/userid/photo/
def photo_directory_path(instance):
    return os.path.join('uploads/', str(instance.user.id) + '/', 'photo/')


# 告诉django存放之后的图片应该叫什么名字: image.jpg
# 即：uploads/1/photo/image.jpg
def photo_image_file_path(instance, filename):
    ext = filename.split('.')[-1]
    if ext not in ['jpg', 'jpeg', 'png']:
        raise ValueError('image file not valid')
    filename = f'image.{ext}'
    return os.path.join(photo_directory_path(instance), filename)


# photo model
class PhotoBase(models.Model):
    """Photo object posted by the user"""

    # 为了代码简可读
    class Meta:
        abstract = True

    # 每一张图片都要关联到上传他的用户（外键映射关系）
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # on_delete=models.CASCADE用户被删除图片也被删除
    created_time = models.DateTimeField(auto_now_add=True)  # 图片上传时间
    updated_time = models.DateTimeField(auto_now=True)  # 图片被修改的时间
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # 随机给图片产生一个（唯一）字符串，更方便找图片
    image = models.ImageField(null=True, upload_to=photo_image_file_path)
    score = models.CharField(default='', max_length=10)  # 打靶成绩
    direction = models.CharField(default='', max_length=50)  # , verbose_name='打靶方位'
