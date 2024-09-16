# Betterhelp

为florabot插件社区提供的帮助插件，目的是提供一个指令声明的规范

## 使用

安装插件后，发送`help`/`?`/`帮助`即可

## For Developer

这个帮助插件在获得 **`FloraBot`** 的api时（即`api_update_event`），会自动获取`PluginsInfoDict`的字典，然后遍历尝试获取插件目录下的`command.json`文件

如果没有找到这个文件，会自动补充为`暂无已声明命令`

下面是`command.json`文件的格式

```json
[
    {
        "command": "help",
        "content": "获取帮助"
    }
]
```
