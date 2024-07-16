import argparse
from tqdm import tqdm
from functions.write_to_html import write_results_to_html
from functions.domain_dic import domain_auto_dic
from functions.common_request import check_url_alive, bodysize_blacklist
from functions.dirfuzz_request import dirfuzz_run
from functions.utils import nowtime, dic_load, logo, get_file_path

from functions.load_dic import load_dic
from colorama import init,Fore
init(autoreset=True)
version = '2.2'

dic_data = dic_load()
language_type = dic_data['type']['language_type'] 
max_retry = dic_data['http']['retry']
timeout = dic_data['http']['timeout']
max_work = dic_data['http']['max_worker']
header = dic_data['http']['headers']
autoDomainBackupDic = dic_data['http']['autoDomainBackupDic']
dic = dic_data['common']['dic']
auto_save = dic_data['common']['auto_save']

def get_parser():
    parser = argparse.ArgumentParser(description='飞天Web目录扫描工具-dirfuzz')
    p = parser.add_argument_group('参数')
    p.add_argument("-u", "--url", type=str, help="目标url")
    p.add_argument("-f", "--file", type=str, help="url所在文件")
    p.add_argument("-w", "--wordList", type=str, help="指定字典文件, 请放在db目录下")
    p.add_argument("-p", "--proxy", type=str, help="使用http代理,如-p 127.0.0.1:7890")
    p.add_argument("-o", "--outfile", type=str, help="结果输出到html文件, 无需带文件后缀名")
    p.add_argument("-e", "--extension", type=str, help="指定扫描网站的类型, 类型为php,jsp,jspx,asp,aspx。如-e php")
    p.add_argument("-t", "--threads", type=str, help="请求线程数")
    p.add_argument("-v", "--version", action='store_true', help="查看dirfuzz版本")
    args = parser.parse_args()
    return args

def processUrl():
    args = get_parser()
    target = args.url
    urlfile = args.file
    dicfile = get_file_path(args.wordList, "db") if args.wordList else get_file_path(dic, "db")
    proxyx = None if not args.proxy else {'http': 'http://{}'.format(args.proxy), 'https': 'http://{}'.format(args.proxy)}
    proxy = None if not args.proxy else 'http://%s' % args.proxy
    max_worker = int(args.threads) if args.threads else max_work
    outputFile = get_file_path(args.outfile + ".html", "reports") if args.outfile else get_file_path(nowtime() + ".html", "reports")
    extension = args.extension
    ver = args.version
    if extension and (('.' + extension) not in language_type):
        print("-e指定类型错误")
        exit()
    if ver:
        print("dirfuzz v" + version)

    if urlfile or target:
        if target:
            urls = [target.rstrip('/')]
        else:
            urls = [line.strip().rstrip('/') for line in open(urlfile, "r", encoding="utf-8")]

        n = 1
        printOutput = False
        logo(version, extension, max_worker, language_type, dicfile)
        for url in urls: 
            scan_results = []
            tqdm.write(Fore.LIGHTYELLOW_EX + "\nTarget[%s/%s]: " % (n, len(urls)) + Fore.LIGHTCYAN_EX + "%s\n" % url)
            if check_url_alive(url, proxyx, timeout, header, max_retry):
                #去除任何请求都返回相同的页面
                black_location, black_content_length, black_fixed_location = bodysize_blacklist(url, proxyx, header, max_worker)
                
                #加载所有字典
                dics = load_dic(dicfile, extension)
                
                #如果自动生成域名字典
                if autoDomainBackupDic:
                    #根据域名自动生成备份文件名
                    domain_backup_dic = domain_auto_dic(url)
                    # print(domain_backup_dic)
                    dics.extend(domain_backup_dic)
                
                dirfuzz_run(dics, url, max_worker, proxy, black_location, black_content_length, black_fixed_location, header, timeout, max_retry, scan_results)

            if (urlfile and scan_results) or (target and scan_results and (auto_save or args.outfile)):
                printOutput = True
                write_results_to_html(scan_results, outputFile)
            n += 1
        if printOutput:
            print("\nOutput File: %s" %outputFile)
        
processUrl()
