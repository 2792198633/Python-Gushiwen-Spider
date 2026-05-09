import urllib.parse
import time
import datetime
import re

#通过登录 然后进入到主页面

# 通过找登录接口我们发现 登录的时候需要参数很多
#https://www.gushiwen.cn/user/login.aspx?from=http://www.gushiwen.cn/user/wode.aspx
# __VIEWSTATE:woSGAoex/K+3xRiTsfgMpvmkg2YbzqOIHxpDx6yWdNbyx3TO9fdSDG1HgsWDXLOA1g6rend2HDgrnnc/vf1wcPmA7MyOfCFjNrjY0S7vL553hdvhF+YiMCiKpPTxeeUoxUofS14rBZ/mTNgS5aW1TVamWEY=
# __VIEWSTATEGENERATOR:C93BE1AE
# from:
# email:2792198633@qq.com
# pwd:0888888
# code:MN2Q
# denglu:登录

#我们观察到 __VIEWSTATE   __VIEWSTATEGENERATOR  code是一个可以变化的量

#难点：（1）__VIEWSTATE   __VIEWSTATEGENERATOR
#      我们观察到这两个数据在页面的源码中，所以我们需要获取页面的源码，然后进行解析就可以获取了（通过查看页面源码，然后搜索名称）

#     (2)验证码

import requests

#这是登录页面的url地址
url='https://www.gushiwen.cn/user/login.aspx?from=http://www.gushiwen.cn/user/wode.aspx'

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
    'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language':'en-US,en;q=0.9',
    'referer':'https://www.gushiwen.cn/user/login.aspx?from=http://www.gushiwen.cn/user/wode.aspx'
}

###注意：需要创建一个会话来完成全部的操作，要不然拿的到数据都不是同一次打开的那个网页
session_=requests.session()

# response=requests.get(url=url,headers=headers)
response=session_.get(url=url,headers=headers)
content=response.text

#解析页面源码，获取__VIEWSTATE   __VIEWSTATEGENERATOR
#<input type="hidden" name="__VIEWSTATE" id="__VIEWSTATE" value="Mk5ZxWZYdVZCw6vEyil0vaOpZPvXPnYumSuIAnghwEH9YN0QtLekdNMKAbHF2xf2ABtXgUFOCZ34+KwrVdyVapBK4aPONlHV1rxBGq1c57hbzPmNsiFBBgU+TwdufnNGAlQgztE2I/QBmUOLP0bAfFoppps=" />
#<input type="hidden" name="__VIEWSTATEGENERATOR" id="__VIEWSTATEGENERATOR" value="C93BE1AE" />
from bs4 import BeautifulSoup
soup=BeautifulSoup(content,'lxml')

#获取__VIEWSTATE
viewstate=soup.select('#__VIEWSTATE')[0].attrs.get('value')
#获取__VIEWSTATEGENERATOR
viewstategenerator=soup.select('#__VIEWSTATEGENERATOR')[0].attrs.get('value')

#获取验证码图片
code=soup.select('#imgCode')[0].attrs.get('src')
# print(code)
		# https://www.gushiwen.cn/RandCode.ashx
code_url='https://www.gushiwen.cn'+code
# print(code_url)

#有坑
# import urllib.request
# urllib.request.urlretrieve(url=code_url,filename='code.jpg')

#requests里面有一个方法 session() 通过session的返回值 就能使用请求变成一个对象
# session_=requests.session()

#验证码的url内容
response_code=session_.get(code_url)
# print(response_code.text.encode('utf-8'))
#注意此时要使用二进制数据   因为我们要使用的是图片的下载  图片需要二进制
content_code=response_code.content
# print(content_code)

#wb的模式就是将二进制数据写入到文件
with open('code.jpg','wb',) as fp:
    fp.write(content_code)



# 获取了验证码的图片之后 下载到本地 然后观察验证码 观察之后 然后在控制台输入这个验证码 就可以将这个值给code参数 进行登录
code_name=input('请输入你的验证码：')

#需要抓取登录接口，目前抓不到应该是隐藏了
url_post='https://www.gushiwen.cn/user/login.aspx?from=http%3a%2f%2fwww.gushiwen.cn%2fuser%2fwode.aspx'
data_post={
    '__VIEWSTATE':viewstate,
    '__VIEWSTATEGENERATOR':viewstategenerator,
    'from':'http://www.gushiwen.cn/user/wode.aspx',
    'email':'YOUR_EMALI_HERE@qq.com',
    'pwd':'YOUR_PASSWORD_HERE',
    'code':code_name,
    'denglu':'登录'
}

# response_post= requests.post(url=url_post,headers=headers,data=data_post)
response_post= session_.post(url=url_post,headers=headers,data=data_post)
#这里发送post请求在session中，请求成功的话由于这个网站是通过js跳转，而不是返回http302状态码（requests会自动识别），而js不能
#因此在这个会话请求成功后，需要再次通过get去跳转页面，在get过程中，session会话保存着一个专属id，即Set-Cookie
#在发送get请求时，session会带着cookie凭证去请求，服务器看到cookie就会跳转到个人中心页面
content_post=response_post.text
# print("登录后的最终 URL:", response_post.url)

# 检查是否返回了含有 window.location 的 JS 跳转脚本
if "window.location='http://www.gushiwen.cn/user/wode.aspx'" in response_post.text:
    print("状态：账号密码验证通过！服务器要求JS跳转。")

    #  核心 我们顺从服务器的意愿，手动请求个人中心页面
    wode_url = 'http://www.gushiwen.cn/user/wode.aspx'

    # 记得带着 headers 去请求，伪装到底
    response_wode = session_.get(url=wode_url, headers=headers)

    # 保存真正的个人中心源码
    with open('gushiwen.html', 'w', encoding='utf-8') as fp:
        fp.write(response_wode.text)

    print("成功抓取真正的个人中心源码，已保存至 gushiwen.html！")
else:
    print("状态：登录失败，请检查账号密码或验证码。")
    # 把失败的页面存下来看看原因
    with open('login_error.html', 'w', encoding='utf-8') as fp:
        fp.write(response_post.text)

# with open('gushiwen.html','w',encoding='utf-8') as fp:
#     fp.write(content_post)

#难点：1.隐藏域   2.验证码

#下一步可操作：
#继续用这个 session_ 去请求古诗文网的其他页面。比如：去请求某首诗的页面，然后调用收藏接口，用爬虫自动帮你收藏诗词！

#这是搜索李白的url  get请求
#https://www.gushiwen.cn/shiwens/default.aspx?astr=%e6%9d%8e%e7%99%bd
#第二页：https://www.gushiwen.cn/shiwens/default.aspx?page=2&tstr=&astr=%e6%9d%8e%e7%99%bd&cstr=&xstr=
#第三页：https://www.gushiwen.cn/shiwens/default.aspx?page=3&tstr=&astr=%e6%9d%8e%e7%99%bd&cstr=&xstr=
astr=input('请输入需要查询的诗人：')
max_pages=int(input('请输入需要收藏的页数：'))

for page in range(1,max_pages+1):
    print(f'正在处理第{page}页')
    coll_url='https://www.gushiwen.cn/shiwens/default.aspx?'
    params={
        'page':page,
        'tstr':'',
        'astr':astr,
        'cstr':'',
        'xstr':''
    }
    coll_response=session_.get(url=coll_url,params=params,headers=headers)
    coll_content=coll_response.text

#查找收藏接口：发现有参数：id是token、shoucang：Boolean、time：时间戳
#看网页源码：发现有三个参数：诗的唯一id、token令牌（每首诗的token都是服务器动态生成并硬编码在HTML里的)、当前页面url（用于referer校验）
#使用bs4
    soup=BeautifulSoup(coll_content,'lxml')
    shoucang_imgs=soup.select('div.shoucang img')

    if not shoucang_imgs:
        print('未发现诗文，可能到了最后一页，结束任务！')
    #由于get请求参数需要有time、正则表达式匹配re
    # import time
    # import datetime
    # import re

#通过观察可以发现：<img ... name="3" src="../img/tool/shou-cang.png">
#其中的name值 ： 已收藏时是2，未收藏是3    *注意：这是一个坑，不能这样判断，查看网页静态完整代码发现name初始都是0，由于onload(selectLike())原因
#当浏览器接收到 HTML 并加载图片时（onload），触发了 JavaScript 函数 selectLike()。
#1.把所有的 name 强行操作+1（猜测）
#2.偷偷去读取了你浏览器里的 Cookie，检查这首诗的 ID 在不在你的收藏列表里。
# 如果在，它就再进行一顿操作，把图标换成黑色的实心星星，把 alt 改成“已收藏”，并且可能把 name 变成了 2。

#解决：在收藏接口的set-cookie中：
# 有一长串 Cookie，里面有一个非常显眼的名字：idsShiwen2017。这个 Cookie 里面用逗号分隔，保存了你所有已收藏诗文的 ID。
#set-cookie: idsShiwen2017=%2c70874%2c7717%2c8180%2c8066%2c8488%2c2025%2c70862%2c1744%2c8027%2c; expires=Thu, 06-Aug-2026 13:20:37 GMT; path=/
#%2c是ASCII十六进制中的逗号 ，   70874,7717,8180...都是id
#获取所有接口的cookie session_.cookies 返回的是一个RequestsCookieJar 对象。

# cookie_dict=dict(session_.cookies)
# collected_ids_str=cookie_dict['idsShiwen2017']
#           同样的作用下面和上面两行

    cookies_dict = requests.utils.dict_from_cookiejar(session_.cookies)
#requests.utils.dict_from_cookiejar() 的作用是将 RequestsCookieJar 对象（requests 库用来存储 Cookie 的特殊对象）转换成一个标准的 Python 字典（dict）。
    collected_ids_str = cookies_dict.get('idsShiwen2017', '')
#想反过来操作，比如手上有一个字典，想把它塞进 session 供后续请求使用，可以使用它的“亲兄弟”函数：
# requests.utils.add_dict_to_cookiejar(session_.cookies, my_dict)




# 解码它！
    collected_ids_str=urllib.parse.unquote(collected_ids_str)
    print(collected_ids_str)

    for img in shoucang_imgs:

    # #如果name=2，说明已收藏过，直接跳过       坑！！！
    # is_shoucang=img.attrs.get('name')
    # print(is_shoucang)
    # if is_shoucang=='2':
    #     print('跳过')
    #     continue

        onclick_text=img.attrs.get('onclick')
    # print(onclick_text)

    # 使用正则表达式提取id和token
        match=re.search(r"changeLike\((\d+),'([A-Z0-9]+)'",onclick_text)

        if match:
            p_id=match.group(1)
            p_token=match.group(2)
            # print(f"id：{p_id}, token: {p_token}")

            #https://www.gushiwen.cn/shiwen2017/likeding.aspx?shoucang=false&id=681C004684E87726&time=20:37:23
            api_url='https://www.gushiwen.cn/shiwen2017/likeding.aspx'
            current_time = datetime.datetime.now().strftime('%H:%M:%S')

            if f",{p_id}," in collected_ids_str:
                print(f'已收藏。。。id:{p_id}')
                #在这里如果已收藏可以continue
                #如果想取消收藏，可以使用在这里定义一个变量shoucang_status = 'true'，然后在params中赋值给shoucang
            else:
                print(f'未收藏。。。id:{p_id}')
                #同理，想把未收藏的收藏，可以把变量shoucang_status = 'false',然后赋值
            params={
                'shoucang':'false',
                'id':p_token,
                'time':current_time
            }

            #准备请求头：更新Referer为当前搜索页面的url
            api_headers=headers.copy()
            api_headers['Referer']=coll_response.url

            #发送收藏请求
            like_response=session_.get(url=api_url,params=params,headers=api_headers)

            print(f"收藏结果：{like_response.text}")

            time.sleep(1.5)
#取消收藏只需要把false改成true
print('批量收藏完成')