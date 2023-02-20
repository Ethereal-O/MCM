import re
import csv
# name = "草种植"
# for name in ["种植草+引导+扩展"]:
# # for name in ["草种植","畜牧区保护","畜牧区缓冲","畜牧区引导","电网","电网增强","耕种区保护+引导","禁止捕猎","设立保护区","设立缓冲区","狩猎","引导","增加迁入迁出"]:
#     with open("./result/"+name+".txt","r",encoding="utf-8") as f:
#         content = f.read()
#         list = re.findall(r"\d+\.*\d*",content)
#         list = [list[0:60],list[60:120],list[120:180],list[180:240],list[240:300],list[300:360]]
#         with open("./result/"+name+'.csv', 'w', encoding='utf-8', newline='') as file:
#             writer = csv.writer(file)
#             writer.writerows(list)
            
files=[]
for name in ["开放","草种植","畜牧区保护","畜牧区缓冲","畜牧区引导","电网","电网增强","耕种区保护+引导","禁止捕猎","设立保护区","设立缓冲区","狩猎","引导","增加迁入迁出"]:
    file = open("./result/"+name+".csv","r",encoding="utf-8")
    reader = csv.reader(file)
    files.append(reader)
    # with open("./result/"+name+".csv","r",encoding="utf-8") as f:
    #     reader = csv.reader(file)
    #     reader.
    

with open("./result/tot_食肉动物离散度.csv","w",encoding="utf-8") as f:
    lists = []
    for file in files:
        writer = csv.writer(f)
        lists.append(list(file)[5])
    writer.writerows(lists)
            
