import requests, threading, concurrent.futures
requests.packages.urllib3.disable_warnings()
from collections import Counter
from time import sleep
from urllib.parse import unquote_plus

lock = threading.Lock()

def check_url_alive(url, proxy, timeout, header, max_retry, retries=0):
    try:
        response = requests.get(url=url, headers=header, verify=False, proxies=proxy, timeout=timeout, stream=True)
        res_code = response.status_code
        if res_code < 500:
            return True

    except Exception as e:
        # print(e)
        if retries < max_retry:
            sleep(0.5)
            return check_url_alive(url, proxy, timeout, header, max_retry, retries + 1)
        
    print("[ERROR]The target appears to be inaccessible")
    return False

#因为后面目录扫描都是要禁止重定向的，所以这里也最好进行禁止重定向处理
#1.请求任何路径都200返回一样的页面，可以通过禁止重定向然后获取响应体的大小
#2.请求任何路径都301跳转到固定路径，可以通过禁止重定向然后获取Location的值
#3.请求任何路径都301跳转先跳转到"固定路径+该路径"下，其实该路径为统一错误界面，可以通过禁止重定向，需allow_redirects=False
def bodysize_blacklist(url, proxy, header, max_worker):
    # randomPath = ['oauth/login']
    randomPath = ['C1DE2af','wp-config111.php~','oauth/login','common.inc.php','database.php','adminpanel']
    bodySizeList = []          #处理1的情况
    location_list = []         #处理2的情况
    fixed_location_list = []   #处理3的情况

    def reques(url, path, proxy):
        path2 = url + "/" + path
        try:
            response = requests.get(url=path2, headers=header, allow_redirects=False, proxies=proxy, timeout=8, stream=True, verify=False)
            res_code = response.status_code
            if res_code == 200:
                # 获取Content-Length字段  
                content_length = response.headers.get('Content-Length') 
                if content_length == None:  
                    content_length = (len(response.content))
                with lock:
                    bodySizeList.append(content_length)
                    
            elif 300 <= res_code < 400:
                location = unquote_plus(response.headers.get('Location')) 
                location_list.append(location)
                fixed_location_list.append(location.replace(path, ""))

        except Exception as e:
            # print(e)
            pass
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_worker) as executor:
        tasks = []
        for path in randomPath:
            
            tasks.extend([executor.submit(reques, url, path, proxy)])
        concurrent.futures.wait(tasks)

    black_content_length = []
    black_location = []
    black_fixed_location = []

    count_dic = Counter(bodySizeList)                     #处理1的情况
    for element, count in count_dic.items():
        if count > 1:
            black_content_length.append(element)

    count_dic_location = Counter(location_list)           #处理2的情况
    for element, count in count_dic_location.items():
        if count > 1:
            black_location.append(element)
    
    count_fixed_location = Counter(fixed_location_list)    #处理3的情况
    for element, count in count_fixed_location.items():
        if count > 1:
            black_fixed_location.append(element)
 
    if black_fixed_location == ['/']:
        black_fixed_location = []

    # print(black_content_length)
    # print(black_location)
    # print(black_fixed_location)
            
    return black_location, black_content_length, black_fixed_location
