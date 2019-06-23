# -*- coding:utf8 -*-
from selenium import webdriver
import time
import os
from PIL import Image
import pytesseract
import cv2
import copy


def del_noise(img,number):
    '''
    根据该像素周围点为黑色的像素数（包括本身）来判断是否把它归属于噪声，如果是噪声就将其变为白色
    	input:  img:二值化图
    			number：周围像素数为黑色的小于number个，就算为噪声，并将其去掉，如number=6，
    			就是一个像素周围9个点（包括本身）中小于6个的就将这个像素归为噪声
    	output：返回去噪声的图像
    '''
    height = img.shape[0]
    width = img.shape[1]

    img_new = copy.deepcopy(img)
    for i in range(1, height - 1):
        for j in range(1, width - 1):
            point = [[], [], []]
            count = 0
            point[0].append(img[i - 1][j - 1])
            point[0].append(img[i - 1][j])
            point[0].append(img[i - 1][j + 1])
            point[1].append(img[i][j - 1])
            point[1].append(img[i][j])
            point[1].append(img[i][j + 1])
            point[2].append(img[i + 1][j - 1])
            point[2].append(img[i + 1][j])
            point[2].append(img[i + 1][j + 1])
            for k in range(3):
                for z in range(3):
                    if point[k][z] == 0:
                        count += 1
            if count <= number:
                img_new[i, j] = 255
    return img_new

for i in range(10):
    driver = webdriver.Chrome()
    driver.get(
        '''http://www.cgssafety.com/''')
    driver.maximize_window()  # 浏览器最大化

    driver.refresh()  # 刷新页面
    time.sleep(2)
    # # 获取全屏图片，并截取验证码图片的位置
    driver.get_screenshot_as_file('a_full.png')

    location = driver.find_element_by_xpath('''//*[@id="login_verifycode"]''').location
    print(location)
    size = driver.find_element_by_xpath('''//*[@id="login_verifycode"]''').size
    print(size)
    driver.quit()
    left = location['x']
    top = location['y']
    right = location['x'] + size['width']
    bottom = location['y'] + size['height']
    a = Image.open("a_full.png")
    im = a.crop((left, top, right, bottom))
    im.save('a.png')
    time.sleep(1)
    # # #打开保存的验证码图片
    image = cv2.imread("a.png")
    # # # 图片转换成字符
    im_l = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite('tt.jpg', im_l)

    result = cv2.adaptiveThreshold(im_l, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, 1)

    # 去噪声
    img = del_noise(result, 4)
    # img = del_noise(img, 4)
    #img = del_noise(img, 3)
    # 加滤波去噪
    # im_temp = cv2.bilateralFilter(src=img, d=15, sigmaColor=130, sigmaSpace=150)
    # im_temp = im_temp[1:-1,1:-1]
    # im_temp = cv2.copyMakeBorder(im_temp, 83, 83, 13, 13, cv2.BORDER_CONSTANT, value=[255])

    print("图片预处理完成！")
    cv2.imwrite('temp%d.jpg' %(i), img)

    vd = pytesseract.image_to_string(img)
    if vd != "":
            vd = vd[0:5]
    print("code" + str(i))
    print(vd)
    print("finish")

    #driver.find_element_by_name("")
    #    find_element_by_id("staffCode").send_keys("username")
    #driver.find_element_by_id("pwd").send_keys("password")
   # driver.find_element_by_id("validateCode").send_keys(vcode)
    # 点击登录
   # driver.find_element_by_id("loginBtn").click()