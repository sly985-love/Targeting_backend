# import math
# import os
# import re
# import os
#
#
# def photo_directory_path(instance):
#     return os.path.join('uploads/', str(instance.user.id) + '/', 'photo/')
#
#
# # 告诉django存放之后的图片应该叫什么名字: image.jpg
# # 即：uploads/1/photo/image.jpg
# def photo_image_file_path(instance, filename):
#     ext = filename.split('.')[-1]
#     if ext not in ['jpg', 'jpeg', 'png']:
#         raise ValueError('image file not valid')
#     filename = f'image.{ext}'
#     return os.path.join(photo_directory_path(instance), filename)
#
#
# url = photo_image_file_path
# print(url)

# # url = 'C://Users//shuailuyu//PycharmProjects//yolov5-target//yolov5-target-sly//upload//1//photo//2.jpg'
# import cv2
#
# url1 = 'upload/1/photo/2.jpg'
#
# # 把src.jpg,best.pt,放到deeplearning文件夹下，注意修改图像文件路径，以及detect.py文件路径，将最后一张虚拟图像存在url同名文件夹下，以方遍同时给用户返回
# class ShootingScoreDetector():
#     def getholescore(url: str) -> int:
#         '''	处理图片
#         :param url:图片地址
#     	:return: 打靶次数，成绩，方向，环数
#     	'''
#         # C:\Users\shuailuyu\PycharmProjects\yolov5 - target\yolov5 - target - sly\detect.py
#         # cmd = r'python D:\pyproject\yolov5-django\detect.py --source ' + url + ' --classes 0 --exist-ok'
#         cmd = r'python C:\Users\shuailuyu\PycharmProjects\yolov5-target\yolov5-target-sly\detect.py  --weights runs/train/exp9/weights/best.pt --source ' + url + ' --save-txt --save-conf '
#         text = os.popen(cmd).readlines()
#         x = 0
#         y = 0
#         # 弹孔坐标中心坐标 列表数组
#         x_h = []
#         y_h = []
#         # 十环中心坐标，即靶心坐标
#         x_K = 0
#         y_k = 0
#         # 10环宽高
#         w_k = 0
#         h_K = 0
#         # 靶面中心坐标
#         x_t = 0
#         y_t = 0
#         # 靶面宽高
#         w_t = 0
#         h_t = 0
#         # 所有弹孔的x,y坐标
#         x_vv = []
#         y_vv = []
#         # 收集所有的弹孔坐标【（x，y）（x，y）....】的形式
#         index2 = []
#         # 一定要存全局呀，存循环的害死我
#         result = []
#         resultall = []
#         for line in text:
#             aa = line.split(" ")
#             if (aa[0] == '0'):
#                 x_t = float(aa[1]) * 1000
#                 y_t = float(aa[2]) * 1000
#                 w_t = float(aa[3]) * 1000
#                 h_t = float(aa[4]) * 1000
#             elif (aa[0] == '1'):
#                 x = float(aa[1]) * 1000
#                 x_h.append(x)
#                 y = float(aa[2]) * 1000
#                 y_h.append(y)
#             elif (aa[0] == '3'):
#                 x_K = float(aa[1]) * 1000
#                 y_k = float(aa[2]) * 1000
#                 w_k = float(aa[3]) * 1000
#                 h_K = float(aa[4]) * 1000
#             else:
#                 print("靶心获取不准暂时不处理")
#         # print(x_h, y_h, x_K, y_k, w_k, h_K, x_t, y_t, w_t, h_t)
#         for i in range(0, len(x_h)):
#             # print(i, x_h[i], y_h[i], x_K, y_k, w_k, h_K, x_t, y_t, w_t, h_t)
#             x_t0 = x_t - w_t / 2
#             y_t0 = y_t - h_t / 2
#             x_t1 = x_t + w_t / 2
#             y_t1 = y_t + h_t / 2
#             # 环间距
#             d_r = (w_k + h_K) / 4
#             print("环间距", d_r)
#             # 计算弹孔到靶心的距离
#             d_kh = math.sqrt((x_h[i] - x_K) * (x_h[i] - x_K) + (y_h[i] - y_k) * (y_h[i] - y_k))
#             print("弹靶心距", d_kh)
#             # 根据弹靶心距离与环间距的比例，计算输出精度为0.1的环值
#             score_n = 11 - d_kh / d_r
#             print(str("环值" + '%.1f' % (score_n)) + "环")
#             # 根据靶面坐标，靶心坐标，弹孔坐标，输出相对于靶心的八方位方位信息
#             score_a = "null"
#             if (x_t0 < x_h[i] < x_K and y_h[i] == y_k):
#                 score_a = '偏左方'
#             elif (x_t0 < x_h[i] < x_K and y_t0 < y_h[i] < y_k):
#                 score_a = "偏左上方"
#             elif (x_h[i] == x_K and y_t0 < y_h[i] < y_k):
#                 score_a = "偏上方"
#             elif (x_K < x_h[i] < x_t1 and y_t0 < y_h[i] < y_k):
#                 score_a = "偏右上方"
#             elif (x_K < x_h[i] < x_t1 and y_h[i] == y_k):
#                 score_a = "偏右方"
#             elif (x_t0 < x_h[i] < x_K and y_k < y_h[i] < y_t1):
#                 score_a = "偏左下方"
#             elif (x_h[i] == x_K and y_k < y_h[i] < y_t1):
#                 score_a = "偏下方"
#             elif (x_K < x_h[i] < x_t1 and y_k < y_h[i] < y_t1):
#                 score_a = "偏右下方"
#             else:
#                 print("出界了")
#             print("方向:" + str(score_a))
#             x_vk = 610
#             y_vK = 645
#             # 计算相对距离系数
#             k_x = round(float(x_h[i]) / float(x_K), 4)
#             k_y = round(float(y_h[i]) / float(y_k), 4)
#             print("比例系数", k_x, k_y)
#             # 判断弹孔相对于靶心的四方位
#             x_vh = k_x * x_vk
#             y_vh = k_y * y_vK
#             print("虚拟图像上靶点坐标", x_vh, y_vh)
#             index = [(int(x_vh), int(y_vh))]
#             path = r"scr.jpeg"
#             image = cv2.imread(path)
#             # 循环列表，添加多个点到图片上
#             for coor in index:
#                 print(coor)
#                 cv2.circle(image, coor, 10, (0, 0, 255), -1)  # 中心坐标,半径,颜色(BGR),线宽(若为-1,即为填充颜色)
#             # 保存图片
#             cv2.imwrite('result' + str(int(i)) + '.jpg', image)
#             result.append({"number": i, 'score_direction': score_a, 'score_grade': score_n})
#             print(result)
#             print("******************************")
#             x_vv.append(int(x_vh))
#             y_vv.append(int(y_vh))
#
#         for i in range(0, len(x_vv)):
#             index2.append((x_vv[i], y_vv[i]))
#
#         print(index2, )
#         # 循环列表，添加多个点到图片上
#         for coor in index2:
#             cv2.circle(image, coor, 10, (0, 0, 255), -1)  # 中心坐标,半径,颜色(BGR),线宽(若为-1,即为填充颜色)
#         # 保存图片
#         cv2.imwrite('result' + str(int(len(x_h))) + '.jpg', image)
#         return result
# # [[0, '偏右下方', 8.58], [1, '偏左下方', 9.03], [2, '偏右上方', 9.73], [3, '偏右上方', 9.37], [4, '偏右下方', 6.61], [5, '偏右下方', 10.01]]
#
#
# # def getholescore(url: str) -> int:
# #     '''	处理图片
# #     :param url:图片地址
# # 	:return: 打靶次数，成绩，方向，环数
# # 	'''
# #     # C:\Users\shuailuyu\PycharmProjects\yolov5 - target\yolov5 - target - sly\detect.py
# #     # cmd = r'python D:\pyproject\yolov5-django\detect.py --source ' + url + ' --classes 0 --exist-ok'
# #     cmd = r'python C:\Users\shuailuyu\PycharmProjects\yolov5-target\yolov5-target-sly\detect.py  --weights runs/train/exp9/weights/best.pt --source ' + url + ' --save-txt --save-conf '
# #     text = os.popen(cmd).readlines()
# #     x = 0
# #     y = 0
# #     # 弹孔坐标中心坐标 列表数组
# #     x_h = []
# #     y_h = []
# #     # 十环中心坐标，即靶心坐标
# #     x_K = 0
# #     y_k = 0
# #     # 10环宽高
# #     w_k = 0
# #     h_K = 0
# #     # 靶面中心坐标
# #     x_t = 0
# #     y_t = 0
# #     # 靶面宽高
# #     w_t = 0
# #     h_t = 0
# #     # 所有弹孔的x,y坐标
# #     x_vv = []
# #     y_vv = []
# #     # 收集所有的弹孔坐标【（x，y）（x，y）....】的形式
# #     index2 = []
# #     # 一定要存全局呀，存循环的害死我
# #     result = []
# #     resultall = []
# #     for line in text:
# #         aa = line.split(" ")
# #         if (aa[0] == '0'):
# #             x_t = float(aa[1]) * 1000
# #             y_t = float(aa[2]) * 1000
# #             w_t = float(aa[3]) * 1000
# #             h_t = float(aa[4]) * 1000
# #         elif (aa[0] == '1'):
# #             x = float(aa[1]) * 1000
# #             x_h.append(x)
# #             y = float(aa[2]) * 1000
# #             y_h.append(y)
# #         elif (aa[0] == '3'):
# #             x_K = float(aa[1]) * 1000
# #             y_k = float(aa[2]) * 1000
# #             w_k = float(aa[3]) * 1000
# #             h_K = float(aa[4]) * 1000
# #         else:
# #             print("靶心获取不准暂时不处理")
# #     # print(x_h, y_h, x_K, y_k, w_k, h_K, x_t, y_t, w_t, h_t)
# #     for i in range(0, len(x_h)):
# #         # print(i, x_h[i], y_h[i], x_K, y_k, w_k, h_K, x_t, y_t, w_t, h_t)
# #         x_t0 = x_t - w_t / 2
# #         y_t0 = y_t - h_t / 2
# #         x_t1 = x_t + w_t / 2
# #         y_t1 = y_t + h_t / 2
# #         # 环间距
# #         d_r = (w_k + h_K) / 4
# #         print("环间距", d_r)
# #         # 计算弹孔到靶心的距离
# #         d_kh = math.sqrt((x_h[i] - x_K) * (x_h[i] - x_K) + (y_h[i] - y_k) * (y_h[i] - y_k))
# #         print("弹靶心距", d_kh)
# #         # 根据弹靶心距离与环间距的比例，计算输出精度为0.1的环值
# #         score_n = 11 - d_kh / d_r
# #         print(str("环值" + '%.1f' % (score_n)) + "环")
# #         # 根据靶面坐标，靶心坐标，弹孔坐标，输出相对于靶心的八方位方位信息
# #         score_a = "null"
# #         if (x_t0 < x_h[i] < x_K and y_h[i] == y_k):
# #             score_a = '偏左方'
# #         elif (x_t0 < x_h[i] < x_K and y_t0 < y_h[i] < y_k):
# #             score_a = "偏左上方"
# #         elif (x_h[i] == x_K and y_t0 < y_h[i] < y_k):
# #             score_a = "偏上方"
# #         elif (x_K < x_h[i] < x_t1 and y_t0 < y_h[i] < y_k):
# #             score_a = "偏右上方"
# #         elif (x_K < x_h[i] < x_t1 and y_h[i] == y_k):
# #             score_a = "偏右方"
# #         elif (x_t0 < x_h[i] < x_K and y_k < y_h[i] < y_t1):
# #             score_a = "偏左下方"
# #         elif (x_h[i] == x_K and y_k < y_h[i] < y_t1):
# #             score_a = "偏下方"
# #         elif (x_K < x_h[i] < x_t1 and y_k < y_h[i] < y_t1):
# #             score_a = "偏右下方"
# #         else:
# #             print("出界了")
# #         print("方向:" + str(score_a))
# #         x_vk = 610
# #         y_vK = 645
# #         # 计算相对距离系数
# #         k_x = round(float(x_h[i]) / float(x_K), 4)
# #         k_y = round(float(y_h[i]) / float(y_k), 4)
# #         print("比例系数", k_x, k_y)
# #         # 判断弹孔相对于靶心的四方位
# #         x_vh = k_x * x_vk
# #         y_vh = k_y * y_vK
# #         print("虚拟图像上靶点坐标", x_vh, y_vh)
# #         index = [(int(x_vh), int(y_vh))]
# #         path = r"scr.jpeg"
# #         image = cv2.imread(path)
# #         # 循环列表，添加多个点到图片上
# #         for coor in index:
# #             print(coor)
# #             cv2.circle(image, coor, 10, (0, 0, 255), -1)  # 中心坐标,半径,颜色(BGR),线宽(若为-1,即为填充颜色)
# #         # 保存图片
# #         cv2.imwrite('result' + str(int(i)) + '.jpg', image)
# #         result.append({"number": i, 'score_direction': score_a, 'score_grade': score_n})
# #         print(result)
# #         print("******************************")
# #         x_vv.append(int(x_vh))
# #         y_vv.append(int(y_vh))
# #
# #     for i in range(0, len(x_vv)):
# #         index2.append((x_vv[i], y_vv[i]))
# #         resultall.append(result)
# #     print(index2, resultall)
# #     # 循环列表，添加多个点到图片上
# #     for coor in index2:
# #         cv2.circle(image, coor, 10, (0, 0, 255), -1)  # 中心坐标,半径,颜色(BGR),线宽(若为-1,即为填充颜色)
# #     # 保存图片
# #     cv2.imwrite('result' + str(int(len(x_h))) + '.jpg', image)
# #     return resultall
#
#
# #  python detect.py --weights runs/train/exp9/weights/best.pt --source  data/images/hole/2.jpg --save-txt --save-conf --save-crop
# # a = getholescore(url1)
# # print(a)
