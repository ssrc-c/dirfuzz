## dirfuzz介绍
dirfuzz是一款基于Python3的敏感目录文件扫描工具，具有非常快的扫描速度和很高的准确性。可根据域名自动生成网站备份文件字典。

- 建议环境：python 3.10

![image.png](https://cdn.nlark.com/yuque/0/2024/png/22971806/1721109425161-4d97b1a4-1896-4c67-851e-87006bc4337d.png#averageHue=%23363636&clientId=u0fe91aca-1232-4&from=paste&height=392&id=u1a7c0eaf&originHeight=784&originWidth=1753&originalType=binary&ratio=2&rotation=0&showTitle=false&size=514217&status=done&style=none&taskId=u603ae170-d18b-442d-9ff8-a46668135e3&title=&width=876.5)
## dirfuzz目录说明
/db/dicc.txt存放着默认字典，目前字典数量1500+。可以根据需要自动添加删除。其中

- 字典中的%t会替换为config.yaml中language_type列表中的网站脚本语言类型如php,jsp,asp等
- 字典中的%b会替换为config.yaml中sensitive_backup_format列表中的值如rar,tar,zip等

/inc/config.yaml 为配置文件
默认输出到html文件中，目前模板借鉴的是dirsearch。
欢迎您提出宝贵的意见。

