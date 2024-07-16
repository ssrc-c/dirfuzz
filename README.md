## dirfuzz介绍
DirFuzz是一款高效且精准的Python 3敏感目录与文件扫描工具。该工具能够根据输入的域名自动生成针对该站点的备份文件字典。

- 建议环境：python 3.10

![image.png](https://cdn.nlark.com/yuque/0/2024/png/22971806/1721109466551-9111a657-1a90-43e9-a6f0-e6af62f0a964.png#averageHue=%233b3b39&clientId=u0fe91aca-1232-4&from=paste&height=420&id=u4286c9f4&originHeight=839&originWidth=1881&originalType=binary&ratio=2&rotation=0&showTitle=false&size=592156&status=done&style=none&taskId=u3320f288-da72-4cf9-aa6b-0dc9b349d03&title=&width=940.5)
## dirfuzz目录说明
/db/dicc.txt存放着默认字典，可以根据需要自动添加删除。其中

- 字典中的%t会替换为config.yaml中language_type列表中的网站脚本语言类型如php,jsp,asp等
- 字典中的%b会替换为config.yaml中sensitive_backup_format列表中的值如rar,tar,zip等

/inc/config.yaml 为配置文件
默认输出到html文件中，目前模板借鉴的是dirsearch。
欢迎您提出宝贵的意见。

