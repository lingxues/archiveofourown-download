# 多章节爬虫，爬取单章节报错
import requests
import time
import sys
import random
from bs4 import BeautifulSoup
# 可以修改代理地址 不使用就删掉
proxies = {
    "http": "http://127.0.0.1:10809",
    "https": "http://127.0.0.1:10809"
}

url = input("请输入ao3文章网址：:")
url = url+"?view_full_work=true"
response = requests.get(url, proxies=proxies) # 不使用代理删掉, proxies=proxies
soup = BeautifulSoup(response.text, "html.parser")
if response.status_code == 429:
        print(f"请求太频繁力，让我小睡一会Zzz")
        sleeptime=random.randint(60, 90)
        time.sleep(sleeptime)
        print(f"睡醒了，又充满活力啦！")
        sys.exit()
title = soup.find("h2", class_="title").text
# 去除文章中包含系统不允许保存的字符
title = title.replace('\n', '')
title = title.replace('/', '')
title = title.replace('  ', '')
title = title.replace('|', '')
title = title.replace(':', '')
title = title.replace('?', '')
title = title.replace('*', '')
title = title.replace('\\', '')
if soup.find("a", rel="author").text:
    author = soup.find("a", rel="author").text
else:
    author = soup.find("h3", class_="author").text
chapters = soup.find_all('div', id=lambda x: x and x.startswith('chapter-'))
with open(title + '-' + author + '.txt', 'w', encoding='utf-8') as f:
    for chapter in chapters:
        f.write(title + '\n')
        f.write('作者：'+author + '\n')
        f.write(chapter.text)

print("好耶！爬取成功！标题：{}，作者：{}".format(title, author))
