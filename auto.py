# -*- coding:utf8 -*-
from selenium import webdriver
import time
import os
from PIL import Image
import pytesseract

class IMG(object):

    def __init__(self):
        self.driver = ''
        self.w = 0
        self.h = 0
        self.Im = ''


    def _openImg(self, name):
        try:
            im = Image.open(name)
            return im
        except:
            print('[!] Open %s failed' % name)
            exit()

    def processImg(self, name_L):
        threshold = 140
        table = []
        for i in range(256):
            if i < threshold:
                table.append(0)
            else:
                table.append(1)
        img = self._openImg(name_L)
        imgry = img.convert('L')
        self.Im = imgry.point(table, '1')
        #filename = self.codeImg.capitalize()
        self.Im.save('im_L.png')

    def getCodes(self, name):
        self.driver = webdriver.Chrome()
        self.driver.get(
            '''http://geocloudsso.cgs.gov.cn/ssoserver/login/welcome?service=http%3A%2F%2Fgeocloud.cgs.gov.cn%3A8080%2FredirctPortal''')
        self.driver.refresh()  # 刷新页面
        time.sleep(1)
        self.driver.maximize_window()  # 浏览器最大化
        # # 获取全屏图片，并截取验证码图片的位置
        self.driver.get_screenshot_as_file('a.png')

        location = self.driver.find_element_by_xpath('''//*[@id="loginTypeWay"]/div/div[1]/div/div/span/img''').location
        print(location)
        size = self.driver.find_element_by_xpath('''//*[@id="loginTypeWay"]/div/div[1]/div/div/span/img''').size
        print(size)
        self.driver.quit()
        left = location['x']
        top = location['y']
        right = location['x'] + size['width']
        bottom = location['y'] + size['height']
        a = Image.open("a.png")
        im = a.crop((left, top, right, bottom))
        self.w, self.h = im.size
        im.save(name)

    def pIx(self):
        data = self.Im
        # 图片的长宽
        w = self.w
        h = self.h

        # data.getpixel((x,y))获取目标像素点颜色。
        # data.putpixel((x,y),255)更改像素点颜色，255代表颜色。

        try:
            for x in range(1, w - 1):
                left = 0
                right = 0
                if x > 1 and x != w - 2:
                    # 获取目标像素点左右位置
                    left = x - 1
                    right = x + 1

                for y in range(1, h - 1):
                    # 获取目标像素点上下位置
                    up = y - 1
                    down = y + 1

                    if x <= 2 or x >= (w - 2):
                        data.putpixel((x, y), 255)

                    elif y <= 2 or y >= (h - 2):
                        data.putpixel((x, y), 255)

                    elif data.getpixel((x, y)) == 0:
                        up_color = 0
                        down_color = 0
                        left_color = 0
                        right_color = 0
                        if y > 1 and y != h - 1:

                            # 以目标像素点为中心点，获取周围像素点颜色
                            # 0为黑色，255为白色
                            up_color = data.getpixel((x, up))
                            down_color = data.getpixel((x, down))
                            left_color = data.getpixel((left, y))
                            left_down_color = data.getpixel((left, down))
                            right_color = data.getpixel((right, y))
                            right_up_color = data.getpixel((right, up))
                            right_down_color = data.getpixel((right, down))

                            # 去除竖线干扰线
                            if down_color == 0:
                                if left_color == 255 and left_down_color == 255 and \
                                        right_color == 255 and right_down_color == 255:
                                    data.putpixel((x, y), 255)

                            # 去除横线干扰线
                            elif right_color == 0:
                                if down_color == 255 and right_down_color == 255 and \
                                        up_color == 255 and right_up_color == 255:
                                    data.putpixel((x, y), 255)

                        # 去除斜线干扰线
                        if left_color == 255 and right_color == 255 \
                                and up_color == 255 and down_color == 255:
                            data.putpixel((x, y), 255)
                    else:
                        pass

                    # 保存去除干扰线后的图片
                    data.save("test.png", "png")
        except:
            return False

    def Pytess(self, name):
        threshold = 140
        table = []

        for i in range(256):
            if i < threshold:
                table.append(0)
            else:
                table.append(1)

        # rep = {'O': '0',
        #        'I': '1',
        #        'L': '1',
        #        'Z': '2',
        #        'S': '8',
        #        'Q': '0',
        #        '}': '7',
        #        '*': '',
        #        'E': '6',
        #        ']': '0',
        #        '`': '',
        #        'B': '8',
        #        '\\': '',
        #        ' ': ''
        #        }

        data = self._openImg(name)
        imgry = data.convert('L')
        out = imgry.point(table, '1')
        try:
            text = pytesseract.image_to_string(out)
            text = text.strip()
          #text = text.upper()
        except:
            text = 0
        return text

    def loginSite(self, loginname, passwd, randnum, cookies):
        pass


if __name__ == '__main__':
    picname = 'a.png'
    I = IMG()
    # 获取验证码
    I.getCodes(picname)
    # 验证码图片处理
    I.processImg(picname)
    # 去除干扰线
    I.pIx()

   # codes = I.Pytess('test.png')
    out = I._openImg('test.png')
    text = pytesseract.image_to_string(out)
    print('text:')
    print(text)
