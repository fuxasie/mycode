from werobot import *
import requests#提取网页需要模块
import  re#加载正则
import json#json读写，存储用户信息
import random #随机数生成
import datetime


robot = WeRoBot(token='whythislongkey2541638672')
# 明文模式不需要下面三项
robot.config["APP_ID"]='wxec66ce7de87d5720'
robot.config["APP_SECRET"]='a5e139e6871ee668123e491f7bc7307b'
#robot.config['ENCODING_AES_KEY'] = 'M2TX61oyLhb5jdeiD8ek6tz0aVD1XlkY0njYDmXGTbk'
# 被关注
@robot.subscribe
def subscribe(message):
    return "您好，小伙伴～\n想要获取更多？发送：菜单"

# 处理文本消息
@robot.text
def echo(message):
    try:
        txt = message.content
    except:
        txt = message
    if  txt.strip()=="菜单":
        return help_txt()
    elif txt.strip()[0:2] == "唱歌" or  txt.strip()[0:2] == "点歌":
        return Music_search(txt)
    elif txt.strip()[0:2] == "天气" or txt.strip()[-2:] == "天气":
        return weather_forecast(txt.replace("天气" ,""))
    else:
        if random.randint(0, 5) == 1:  # 随机回复一言，否则复读
            return A_word()
    return txt

#
@robot.voice
def voiceis (message):
    #.recognition
    if message.recognition:
        txt=message.recognition.replace("。", "")#删除句号
        return echo(txt)
    return "请回复标准无误的语音，感谢配合/::>"


@robot.location
def position(message):
        return message.position
#_______________________________

#天气相关
def weather_forecast(location):
    WEATHER_KEY = '4ebc4f6d6188408eabdab8be01624cbd'  # 请填入自己申请的key
    WEATHER_API1 = 'https://free-api.heweather.com/s6/weather?'  # 天气集合
    WEATHER_API2 = 'https://free-api.heweather.com/s6/weather/forecast?'  # 3天天气
    WEATHER_API3 = 'https://free-api.heweather.com/s6/air/now?'  # 空气质量
    DICT_TYPE = {'comf': '舒适度指数', 'cw': '洗车指数', 'drsg': '穿衣指数', 'flu': '感冒指数', 'sport': '运动指数',
                 'trav': '旅游指数', 'uv': '紫外线指数', 'air': '空气污染扩散条件指数'}
    WEEKARR = ('周一', '周二', '周三', '周四', '周五', '周六', '周日')
    try:
        response = requests.get(WEATHER_API2, params={
            'key': WEATHER_KEY,
            'location': location
        }, timeout=1)
        json_data = response.json()
        arr = json_data['HeWeather6'][0]
        if arr["status"] != "ok":
            return_str = ''
            if arr['status'] == 'unknown city':
                return_str = '未知或错误城市/地区'
            if arr['status'] == 'no data for this location':
                return_str = '该城市/地区没有你所请求的数据'
            if arr['status'] == 'no more requests':
                return_str = '超过访问次数，需要等到当月最后一天24点后进行访问次数的重置或升级你的访问量'
            if return_str == '':
                return_str = '其他错误，请联系管理员'
            return return_str
        if 'parent_city' not in arr['basic'] or arr['basic']['parent_city'] == arr['basic']['location']:
            loc = arr['basic']['location']
        else:
            loc = arr['basic']['parent_city'] + arr['basic']['location']
        result = '%s未来两日天气预报\n' % loc
        result += '———————————————\n'
        weekday = datetime.datetime.now().weekday()
        for i in [1, 2]:
            forcast_arr = arr['daily_forecast'][i]
            weekday = (weekday + 1) % 7
            date_str = forcast_arr['date'][5:7] + '月' + forcast_arr['date'][8:10] + '日'
            result += '%s %s：\n' % (date_str, WEEKARR[weekday])
            result += '温度：%s℃～%s℃\n' % (forcast_arr['tmp_max'], forcast_arr['tmp_min'])
            if forcast_arr['cond_txt_d'] == forcast_arr['cond_txt_n']:
                result += '天气：%s\n' % forcast_arr['cond_txt_d']
            else:
                result += '天气：%s转%s\n' % (forcast_arr['cond_txt_d'], forcast_arr['cond_txt_n'])
            result += '风向：%s\n风力：%s\n' % (forcast_arr['wind_dir'], forcast_arr['wind_sc'])
            result += '相对湿度：%s%%\n降水概率：%s%%\n' % (forcast_arr['hum'], forcast_arr['pop'])
            result += '紫外线强度指数：%s\n' % forcast_arr['uv_index']
            if i == 1:
                result += '\n'
        result += '———————————————'
        return result
    except:
        return '系统繁忙或出错，请重试'


#古诗词版本一言
def A_word():
    url="https://api.77sec.cn/yiyan/api.php"
    html=requests.get(url).text
    html=re.findall("\".*?\"",html)
    try:
        return html[0]
    except IndexError:
         return "接口暂时出现问题！"
#点歌
def Music_search(message):
    message=message.replace("音乐","").strip()
    if not message:
        return "请输入正确的歌名，才能搜索。"
    html=requests.post("http://47.112.23.238/Music/getMusicList",data={"musicName":message,"type": "netease","number": "20"}).text
    #html=html.encode().decode("unicode_escape")
    htmlcode=re.findall("author...(\\\.*?)\"..url...(http.*?mp3).*?title...(\\\.*?)\"",html)#列表
    print("author...(\\.*?)\"..url...(http.*?mp3).*?title...(\\.*?)\"")
    if htmlcode:#如果正则搜索内容不为空
        musichost=htmlcode[0][0].encode().decode("unicode_escape")
        musictitle=htmlcode[0][2].encode().decode("unicode_escape")
        musicurl=htmlcode[0][1].replace("\\","/")
        musicurl = musicurl.replace("////", "//")
        musiclist = [musictitle,musichost,musicurl]
        return musiclist
    else:
        return "搜索不到！"
#菜单
def help_txt ():
    txt="/:rose当前机器人拥有如下功能：\n点歌|唱歌 歌曲名（唱歌 小幸运）\nXX天气|天气XX （汕头天气）\n发送位置回复位置。\n强大的复读功能/:pig\n支持回复语音，用的微信接口，感受一下/::D"
    return txt

robot.run(server="gunicorn",host='0.0.0.0',port="80")#启动robot
#print(voiceis(""))
