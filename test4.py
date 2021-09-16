import requests
from tkinter import messagebox
from bs4 import BeautifulSoup
import time
import mailUtils
import libraryUtils

print(libraryUtils.getUserInfoBySeat('2063','0133'))
# count = 0;
# while True:
#     print(count)
#     count += 1
#     r = requests.get("http://gs.ccnu.edu.cn/zsgz/ssyjs.htm")
#     r.encoding = 'utf-8'
#     soup = BeautifulSoup(r.text, 'html.parser')
#     li = soup.find('li', id='line_u10_5').find('a')
#
#     if li['title'] != '华中师范大学2021年硕士研究生招生复试录取工作方案':
#         messagebox.showinfo('提示', '更新了！')
#         mailUtils.sendEmail('提示', '官网消息更新，请查看')
#         print(li['title'])
#         break
#
#     time.sleep(5)

# def test():
#     messagebox.showinfo('提示', '人生苦短')
#
#
# t = Timer(10, test)
# t.start()


