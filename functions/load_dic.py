from functions.utils import dic_load

dic_data = dic_load()
language_type = dic_data['type']['language_type']    #网站脚本语言类型
sen_backup_type = dic_data['type']['sensitive_backup_format'] #敏感数据、备份文件类型

def load_dic(dicfile, extens):
    if extens:
        lt = [extens]
    else:
        lt = language_type
    dics = [] 
    with open(dicfile, "r", encoding="utf-8") as file:  
        for line in file:  
            line = line.lstrip("/").strip()
            # 检查line是否以.%t结尾  
            if '%t' in line or '%b' in line:  
                if '%t' in line:
                    dics.extend([line.replace("%t", l.lstrip('.')) for l in lt])  # 生成新的元素并添加到dics列表  
                if '%b' in line:
                    dics.extend([line.replace("%b", b.lstrip('.')) for b in sen_backup_type])
            else:  
                dics.append(line)  # 如果不是.%t结尾，则直接添加到dics列表
    # print(dics)
    return dics