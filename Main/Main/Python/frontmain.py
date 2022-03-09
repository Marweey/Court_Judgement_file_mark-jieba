from ltp import LTP
import jieba
import jieba.posseg as pseg
import json
import os
import sys

#print(sys.argv[0][:-12] + 'jieba_add_dic/selfdic.txt')
jieba.load_userdict(sys.argv[0][:-12] + 'jieba_add_dic/selfdic.txt')
#jieba.load_userdict(os.path.abspath('jieba_add_dic\\selfdic.txt'))

######################################初始化的数据
nr_dic = {}
nt_dic = {}
nz_dic = {}
zui_dic = {}
xingbie_dic = {}
Birthplace_dic = {}
count = 0

minzu_list = {'汉族', '蒙古族', '藏族', '苗族', '壮族', '回族', '维吾尔族', '彝族', '布依族', '朝鲜族', '侗族', '白族', '哈尼族', '傣族', '傈僳族', '畲族',
              '拉祜族', '满族', '瑶族', '土家族', '哈萨克族', '黎族', '佤族', '高山族', '水族', '东乡族', '景颇族', '土族', '仫佬族', '布朗族', '毛南族',
              '锡伯族', '普米族', '纳西族', '柯尔克孜族', '达斡尔族', '羌族', '撒拉族', '仡佬族', '阿昌族', '塔吉克族', '怒族', '俄罗斯族', '德昂族', '裕固族',
              '塔塔尔族', '鄂伦春族', '门巴族', '基诺族', '乌孜别克族', '鄂温克族', '保安族', '京族', '独龙族', '赫哲族', '珞巴族'}
zhixiashi = {'北京市', '重庆市', '上海市', '天津市'}

# with open(r"..\Transport\案件中转.txt", "r", encoding='gbk') as f:
#    names = f.read().split('\n')

# print(names)

path = sys.argv[0][:-19] + 'Transport'

with open(path + '/' + '案件中转' + '.txt', encoding='utf-16') as f:  # 打开新的文本
    strs = f.read()  # 读取文本数据

jieba.enable_paddle()
ltp = LTP()
sents = ltp.sent_split([strs])  # 分句

for sent in sents:
    seg_list = pseg.cut(sent)

    for word, flag in seg_list:
        # print('%s %s' % (word, flag))
        if flag == 'name':  # 人名
            if word in nr_dic.keys():
                nr_dic[word] += 1
            else:
                nr_dic[word] = 1

        if flag == 'nt':  # 机构名
            if word in nt_dic.keys():
                nt_dic[word] += 1
            else:
                nt_dic[word] = 1

        if flag == 'nz':  # 族别
            if word in nz_dic.keys():
                nz_dic[word] += 1
            else:
                nz_dic[word] = 1

        if flag == 'zui':  # 罪名
            if word in zui_dic.keys():
                zui_dic[word] += 1
            else:
                zui_dic[word] = 1

        if flag == 'xingbie':  # 性别
            if word in xingbie_dic.keys():
                xingbie_dic[word] += 1
            else:
                xingbie_dic[word] = 1

        if flag == 'ns':  # 出生地
            if word in Birthplace_dic.keys():
                Birthplace_dic[word] += 1
            else:
                Birthplace_dic[word] = 1

zubie = "未说明"
Ethnicities = nz_dic.keys()
for Ethnicity in Ethnicities:
    if Ethnicity in minzu_list:
        zubie = Ethnicity
        break

birth_index = 2
if list(Birthplace_dic.keys())[0] in zhixiashi:
    birth_index = 1
if list(Birthplace_dic.keys())[0] == '中华人民共和国':
    birth_index = 3
if len(list(Birthplace_dic.keys())) < birth_index:
    birth_index = len(list(Birthplace_dic.keys()))

xingbie = "未说明"
if len(list(xingbie_dic.keys())) != 0:
    xingbie = ''.join(xingbie_dic.keys())[0] + '  '

data = [{'Criminals': '、'.join(nr_dic.keys()),  # 姓名
         'Gender': xingbie * len(nr_dic),  # 性别
         'Ethnicity': zubie,  # 族别
         'Birthplace': ''.join(list(Birthplace_dic.keys())[:birth_index]),  # 出生地
         'Accusation': '、'.join(zui_dic.keys()),  # 罪名
         'Courts': sents[0],  # 法院
         }]
json_data = open(sys.argv[0][:-24] + 'Main' + '/myjson.json', "w+")
json_data.write(json.dumps(data, sort_keys=False, indent=4, separators=(',', ': '), ensure_ascii=False))
json_data.close()

json_data = open(sys.argv[0][:-24] + 'Main' + '/mytxt.txt', "w+")
json_data.write('、'.join(nr_dic.keys()) + ',' + xingbie * len(nr_dic) + ',' + zubie + ',' + ''.join(list(Birthplace_dic.keys())[:birth_index]) + ',' + '、'.join(zui_dic.keys())
                + ',' + sents[0])
json_data.close()

nr_dic.clear()
nt_dic.clear()
nz_dic.clear()
zui_dic.clear()
xingbie_dic.clear()
Birthplace_dic.clear()

f.close()

print("Complete!")
