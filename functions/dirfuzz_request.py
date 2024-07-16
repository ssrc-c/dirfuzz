from urllib.parse import unquote_plus
from .utils import content_size, systeminfo
import asyncio, aiohttp 
from tqdm.asyncio import tqdm  # 导入 tqdm 的异步版本  
from colorama import init, Fore
init(autoreset=True)

if systeminfo():
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

lock = asyncio.Lock()  

async def dirfuzz(session, max_worker, url, pa, proxy, progress_bar, black_location, black_content_length, black_fixed_location, header, timeout, max_retry, scan_results):  
    retries = 0
    while retries <= max_retry:
        try:
            async with max_worker:
                path = url + "/" + pa
                async with session.get(url=path, headers=header, allow_redirects=False, proxy=proxy, timeout=timeout) as response:  
                    res_code = response.status
                    if res_code < 500:
                        # 获取Content-Length字段  
                        row_content_length = response.headers.get('Content-Length') if response.headers.get('Content-Length') else ""                      
                        #格式化content-length
                        content_length = content_size(row_content_length)
                        try:
                            content_type = response.headers.get('content-type').split(';')[0]
                        except:
                            content_type = "unkown"
                        
                        if res_code < 300: 
                            if row_content_length not in black_content_length:
                                tqdm.write(Fore.GREEN + "%s - %s - %s" %(res_code, content_length, path))
                                progress_bar.update()
                                data = {"contentLength": "%s" % content_length, "contentType": "%s" % content_type, "redirect": "", "status": "%s" % res_code, "statusColorClass": "text-success", "url": "%s" % path}  
                                async with lock: 
                                    scan_results.append(data)
                            else:
                                progress_bar.update()

                        elif 300 <= res_code < 400:
                            locationPath = response.headers.get('Location') 
                            locationPath = unquote_plus(locationPath)
                            fixed_location = locationPath.replace(pa, "")
                            # print(fixed_location)
                            # print(black_fixed_location)
                            if row_content_length not in black_content_length and locationPath not in black_location and fixed_location not in black_fixed_location:
                                tqdm.write(Fore.CYAN + "%s - %s - %s -> %s" %(res_code, content_length, path, locationPath))  
                                progress_bar.update()
                                data = {"contentLength": "%s" % content_length, "contentType": "%s" % content_type, "redirect": "%s" % locationPath, "status": "%s" % res_code, "statusColorClass": "text-warning", "url": "%s" % path}  
                                async with lock: 
                                    scan_results.append(data)
                            else:
                                progress_bar.update()

                        elif res_code == 403:
                            tqdm.write(Fore.BLUE + "%s - %s - %s" %(res_code, content_length, path))
                            progress_bar.update()
                            data = {"contentLength": "%s" % content_length, "contentType": "%s" % content_type, "redirect": "", "status": "%s" % res_code, "statusColorClass": "text-danger", "url": "%s" % path}  
                            async with lock: 
                                scan_results.append(data)

                        elif res_code == 401:
                            if row_content_length not in black_content_length:
                                tqdm.write(Fore.MAGENTA + "%s - %s - %s" %(res_code, content_length, path))
                                progress_bar.update()
                                data = {"contentLength": "%s" % content_length, "contentType": "%s" % content_type, "redirect": "", "status": "%s" % res_code, "statusColorClass": "text-success", "url": "%s" % path}  
                                async with lock: 
                                    scan_results.append(data)
                            else:
                                progress_bar.update()
                        
                        else:
                            progress_bar.update()
                    
                    else:
                        progress_bar.update() 
                break
            
        except (KeyboardInterrupt, asyncio.CancelledError):
            break
        except Exception as e:
            # print(e)
            retries += 1  
            if retries > max_retry:  
                # 如果达到最大重试次数，处理失败情况  
                progress_bar.update()  
                break  # 退出循环  
            await asyncio.sleep(0.5)  # 等待一段时间后重试  

async def dirfuzz_main(dicc, url, max_worker, proxy, black_location, black_content_length, black_fixed_location, header, timeout, max_retry, scan_results):  
    
    max_worker = asyncio.Semaphore(max_worker)
    connector = aiohttp.TCPConnector(ssl=False)
    with tqdm(total=len(dicc), desc="Requesting", bar_format='{desc}: {percentage:.0f}% ({n_fmt}/{total_fmt}) {elapsed}') as progress_bar: 
        async with aiohttp.ClientSession(connector=connector) as session:  
            # 创建一个任务列表  
            tasks = []   
            for pa in dicc: 
                task = asyncio.create_task(dirfuzz(session, max_worker, url, pa, proxy, progress_bar, black_location, black_content_length, black_fixed_location, header, timeout, max_retry, scan_results))  
                tasks.append(task)  
    
            # 等待所有任务完成  
            await asyncio.gather(*tasks) 
  
def dirfuzz_run(dicc, url, max_worker, proxy, black_location, black_content_length, black_fixed_location, header, timeout, max_retry, scan_results):
    try:
        asyncio.run(dirfuzz_main(dicc, url, max_worker, proxy, black_location, black_content_length, black_fixed_location, header, timeout, max_retry, scan_results))  
    except (KeyboardInterrupt, asyncio.CancelledError):  
        print("Exiting due to Ctrl+C...")