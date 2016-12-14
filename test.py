# -*- coding: utf-8 -*-


from bs4 import BeautifulSoup
import codecs


cj = BeautifulSoup(codecs.open("text.txt", "r+", "utf-8").read())

info_dict = {}
href = cj.find('a')
# if not href:
#     continue
info_dict.update({u'链接': href.attrs['href']})

# print href.attrs['href'],

content = href.text.split(" ")
if content:
    info_dict.update({u'小区名称': content[0]})
    info_dict.update({u'户型': content[1]})
    info_dict.update({u'面积': content[2]})

#
content = str(cj.find('div', {'class': 'houseInfo'}).text)
info_dict.update({u'朝向': content.split("|")[0]})

#
content = str(cj.find('div', {'class': 'positionInfo'}).text)
position = content.split(" ")
info_dict.update({u'楼层': position[0]})
info_dict.update({u'建造时间': position[1]})



content = cj.find('div', {'class': 'dealDate'}).text
info_dict.update({u'签约时间': content})


content = cj.find('div', {'class': 'unitPrice'}).text
info_dict.update({u'签约单价': content})

content = cj.find('div', {'class': 'totalPrice'}).text
info_dict.update({u'签约总价': content})

# content = cj.find('div', {'class': 'dealHouseInfo'}).text
# info_dict.update({u'地铁': content})

content = cj.find('div', {'class': 'dealHouseInfo'}).find('span', {'class': 'dealHouseTxt'}).find_all("span")

span_type = content[0].text
span_train = content[1].text

info_dict.update({u'房产类型': span_type})
info_dict.update({u'学区': ""})
info_dict.update({u'地铁': span_train})

# print repr(info_dict).decode("unicode")
#print info_dict[u"地铁"], info_dict[u"房产类型"]

# if content:
#     for c in content:
#         if c.find(u'满') != -1:
#             info_dict.update({u'房产类型': c})
#         elif c.find(u'学') != -1:
#             info_dict.update({u'学区': c})
#         elif c.find(u'距') != -1:
#             info_dict.update({u'地铁': c})


def gen_chengjiao_insert_command(info_dict):
    """
    生成成交记录数据库插入命令
    """
    info_list=[u'链接',u'小区名称',u'户型',u'面积',u'朝向',u'楼层',u'建造时间',u'签约时间',u'签约单价',u'签约总价',u'房产类型',u'学区',u'地铁']
    t=[]
    for il in info_list:
        if il in info_dict:
            t.append(info_dict[il])
        else:
            t.append('')
    t=tuple(t)
    command=(r"insert into chengjiao values(?,?,?,?,?,?,?,?,?,?,?,?,?)",t)

    print command
    return command
