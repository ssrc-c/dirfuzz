from urllib.parse import urlparse
import socket
from functions.utils import dic_load

dic_data = dic_load()
# 获取压缩文件后缀类型的列表  
compressed_file_formats = dic_data['type']['domain_backup_format'] 

#从完整的 URL 中提取域名或ip，并去除 "http://" 或 "https://" 以及端口号
def extract_domain(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.split(':')[0]  # Extract domain and remove port if present
    return domain

#判断目标是否为域名
def is_domian(address):  
    try:  
        socket.inet_aton(address)  
        return False        #是ip则返回False
    except socket.error:  
        return address      #是则返回域名
    
#提取域名的各个部分生成字典
def create_domain_dic(url):
    #最终判断目标是否为域名
    domain = is_domian(extract_domain(url))
    if domain:
        domainDic = []
        parts = domain.split(".")
        #如果域名只有2部分组成
        if len(parts) == 2:
            domainDic.append(parts[0])

        #如果域名只有三部分组成
        elif len(parts) == 3:
            #域名是www开头
            if parts[0] == "www":
                domainDic.append(parts[1])
            #域名不是www开头
            else:
                domainDic.append(parts[0])
                domainDic.append(parts[1])

        #说明域名超过3个部分组成
        else:
            if parts[0] == "www":
                for i in range(1, len(parts) - 1): 
                    domainDic.append(parts[i])
            else:
                #添加除了第一个和最后一个元素
                for i in range(0, len(parts) - 1): 
                    domainDic.append(parts[i])

        domainDic.append(domain)
        return domainDic
    else:
        return False
    
#生成域名字典
def domain_auto_dic(url):
    domain_backup_dic = []
    domainDic = create_domain_dic(url)
    if domainDic:
        for dd in domainDic:
            for cff in compressed_file_formats:
                full_url = dd + cff
                domain_backup_dic.append(full_url)
    return domain_backup_dic