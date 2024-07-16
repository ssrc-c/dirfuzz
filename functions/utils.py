import datetime, yaml, os, platform
from colorama import init,Fore
init(autoreset=True)

#判断系统类型

def systeminfo():
    system_name = platform.system()
    if system_name == "Windows":
        return True
    else:
        return False

def get_file_path(filename, *additional_folders):  
    script_dir = os.path.dirname(__file__) 
    script_dir = os.path.dirname(script_dir) 
    # 获取系统名称  
    system_name = platform.system()  
      
    # 初始化基础路径为脚本目录  
    base_path = script_dir  
      
    # 根据系统名称和额外的文件夹组件构建路径  
    if system_name == "Windows":  
        base_path = os.path.join(base_path)  
    elif system_name == "Linux":  
        base_path = os.path.join(base_path)  
    elif system_name == "Darwin":  # macOS  
        base_path = os.path.join(base_path)  
    else:  
        print("Unsupported system.")  
        return None  
      
    # 如果提供了额外的文件夹，将它们添加到基础路径中  
    for folder in additional_folders:  
        base_path = os.path.join(base_path, folder)  
      
    # 最后，将文件名添加到基础路径中  
    base_path = os.path.join(base_path, filename)  
      
    return base_path  

def dic_load():
    config_file = get_file_path("config.yaml", "inc")
    with open(config_file, 'r', encoding="utf-8") as file:  
        dic_data = yaml.safe_load(file) 
    return dic_data

def logo(version, extension, max_worker, language_type, dicfile):
    dicfile = os.path.basename(dicfile)
    dicfile = dicfile.replace('db/', '')
    logo0 = r'''  
     _  _         __                  
  __| |(_) _ __  / _| _   _  ____ ____
 / _` || || '__|| |_ | | | ||_  /|_  /
| (_| || || |   |  _|| |_| | / /  / / 
 \__,_||_||_|   |_|   \__,_|/___|/___|  飞天目录扫描工具：dirfuzz v{}                                                          
'''
    colored_logo = logo0.format(version)
    print(Fore.MAGENTA + colored_logo)
    outdata = ""
    exdata = ''
    if extension:
        exdata = extension
    else:
        for e in language_type:
            exdata += ', ' + e.lstrip('.')
    outdata = "Extensions: %s | Threads: %s | Dic: %s" %(exdata.lstrip(', '), max_worker, dicfile.replace('db/', ''))
    print(outdata)

def content_size(content_length):
    if content_length:

        body_size_bytes = int(content_length)  
                
        # 根据大小选择合适的单位  
        if body_size_bytes < 1024:  
            unit = 'B'  
        elif body_size_bytes < (1024 * 1024):  
            unit = 'KB'  
            body_size_bytes = body_size_bytes / 1024  
        else:  
            unit = 'MB'  
            body_size_bytes = body_size_bytes / (1024 * 1024)  
        
        # 打印响应体大小  
        bodySize = f"{int(body_size_bytes)}{unit}"  
    else:
        bodySize = ""
        
    return bodySize

def nowtime():
    current_date = datetime.datetime.now()
    formatted_date = current_date.strftime("%m-%d-%H%M%S")
    #返回月-日-时分秒，如08-22-102108
    return formatted_date
