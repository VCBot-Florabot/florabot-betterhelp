# 前言,这里用不到的函数可以不定义,可以直接删去,包括API也可以删去不定义,不会报错的
import json
import os
from pprint import pprint


flora_api = {}  # 顾名思义,FloraBot的API,载入(若插件已设为禁用则不载入)后会赋值上


def occupying_function(*values):  # 该函数仅用于占位,并没有任何意义
    pass


send_msg = occupying_function


def init():  # 插件初始化函数,在载入(若插件已设为禁用则不载入)或启用插件时会调用一次,API可能没有那么快更新,可等待,无传入参数
    global send_msg
    print(flora_api)
    send_msg = flora_api.get("SendMsg")
    print("FloraBot 帮助插件 加载成功")


def api_update_event():  # 在API更新时会调用一次(若插件已设为禁用则不调用),可及时获得最新的API内容,无传入参数
    #print(flora_api)
    global command_list
    command_list = "命令列表：\n"
    plugin={}
    plugin_info={}
    base=flora_api.get("FloraPath")
    plugin_info=dict(flora_api.get("PluginsInfoDict")) #dict
    plugins=plugin_info.items()
    #pprint(plugin_info)
    for name,i in plugins:
        #print(name)
        for j,k in i.items():
            if j == "ThePluginPath":
                print(base+"/./"+k+"/command.json")
                command_list+=f"- {name} \n"
                if not file_exists(base+"/./"+k+"/command.json"):
                    command_list+="     暂无已声明的命令\n"
                    print("未找到"+name+"的command.json文件")
                    continue
                json_data=json.load(open(base+"/./"+k+"/command.json"))
                print(json_data)
                for i in json_data:
                    command_list+=f"    {i['command']} - {i['content']} \n"
                continue
            continue
        #print(command_list)

def file_exists(file_path):
    return os.path.exists(file_path)

def event(data: dict):  # 事件函数,FloraBot每收到一个事件都会调用这个函数(若插件已设为禁用则不调用),传入原消息JSON参数
    print(data)
    uid = data.get("user_id")  # 事件对象QQ号
    gid = data.get("group_id")  # 事件对象群号
    mid = data.get("message_id")  # 消息ID
    msg = data.get("raw_message")  # 消息内容
    try:
        global ws_client
        global ws_server
        send_address = data.get("SendAddress")
        ws_client = send_address.get("WebSocketClient")
        ws_server = send_address.get("WebSocketServer")
    except:
        ws_server=None
        ws_client=None
        pass
    # 处理消息
    if msg is not None:
        msg = msg.replace("&#91;", "[").replace("&#93;", "]").replace("&amp;", "&").replace("&#44;", ",")  # 消息需要将URL编码替换到正确内容
        #print(uid, gid, mid, msg)
        if msg in["帮助","/帮助","help","/help","/?","?"]:
            send_compatible(msg=command_list, gid=gid, uid=uid, mid=mid)

def send_compatible(msg:str,uid:str|int,gid: str|int,mid:int|str=None):  #兼容性函数,用于兼容旧版本API(请直接调用本函数)
    if flora_api.get("FloraVersion") == 'v1.01': #旧版本API
        send_msg(msg=msg,gid=gid,uid=uid,mid=mid)
    else:
        send_type=flora_api.get("ConnectionType")
        send_address=flora_api.get("FrameworkAddress")
        send_msg(msg=msg,gid=gid,uid=uid,mid=mid,send_type=send_type,ws_client=ws_client,ws_server=ws_server)