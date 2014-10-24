# coding: utf-8

__author__ = 'Enigma'

from AST14PyHeader import *
from AnalyseData import *
from FetchFile import *
from datetime import *
import os

mode = server_mode

#确定当前日期
cur_date = datetime.now()
#cur_date += timedelta(hours=-4) #for debug use only
date_str = str(cur_date.month).zfill(2) + str(cur_date.day).zfill(2)

#下载当前日期的配置文件
config_file_name = download_path[mode] + date_str + conf_file_suff
config_file_url = fixed_conf_url + date_str + conf_file_suff
check_file_name = download_path[mode] + date_str + check_file_suff
#先判断有无标记文件，避免重复下载
if os.path.isfile(check_file_name):
    print 'No contest today.'
    exit()
download_url_to_file(config_file_url, config_file_name)
#检测配置文件是否正确，如果不正确=没有比赛，直接退出
#如果是非法的配置文件，不需要转码，本身就是utf-8
if legal_config_file(config_file_name) == no_contest:
    debug_info_file = open(debug_file_name[mode], 'w')
    debug_info_file.writelines('No contest')
    debug_info_file.close()
    chk_file = open(check_file_name, 'w')
    chk_file.write('No contest')
    chk_file.close()
    print 'No contest'
    exit()
file_convert_pagecode(config_file_name, source_pagecode, config_file_name, dest_pagecode)

load_config_file(config_file_name)

#下载主投票所的首页文件
download_url_to_file(home_page_url, home_page_file_name[mode])
file_convert_pagecode(home_page_file_name[mode], source_pagecode, home_page_file_name[mode], dest_pagecode)
hp_file = open(home_page_file_name[mode], 'r')
hp_text = hp_file.read()
hp_file.close()

#根据主投票所的首页文件确定最新的投票页面
startpos = hp_text.find(fixed_data_url) + len(fixed_data_url)
data_url_id = hp_text[startpos:startpos + 10]
data_file_name = download_path[mode] + data_url_id + data_file_suff
data_url_1 = fixed_data_url + data_url_id + '/'
#根据主投票所的首页文件确定次新的投票页面，有时候会跨页
startpos2 = hp_text.find(fixed_data_url, startpos) + len(fixed_data_url)
checkpos = hp_text.find(bkup_title_pref, startpos2)
url_2_title = hp_text[checkpos + 13:checkpos + 17]
if url_2_title != bkup_title:
    startpos2 = hp_text.find(fixed_data_url, checkpos) + len(fixed_data_url)
data_url_id_2 = hp_text[startpos2:startpos2+10]
data_file_2_name = download_path[mode] + data_url_id_2 + data_file_suff
data_url_2 = fixed_data_url + data_url_id_2 + '/'

#下载最新和次新的主投票页面
download_url_to_file(data_url_1, data_file_name)
file_convert_pagecode(data_file_name, source_pagecode, data_file_name, dest_pagecode)
download_url_to_file(data_url_2, data_file_2_name)
file_convert_pagecode(data_file_2_name, source_pagecode, data_file_2_name, dest_pagecode)

#下载备用投票所的首页文件
download_url_to_file(home_page_url_2, home_page_file_2_name[mode])
file_convert_pagecode(home_page_file_2_name[mode], source_pagecode_2, home_page_file_2_name[mode], dest_pagecode)

hp_file = open(home_page_file_2_name[mode], 'r')
hp_text = hp_file.read()
hp_file.close()

#根据备用投票所的首页文件确定最新的备用投票页面
startpos = hp_text.find(data_url_2_filter) - len(data_url_2_offset)
data_url_id_3 = hp_text[startpos:startpos + 10]
data_file_3_name = download_path[mode] + 'b' + data_url_id_3 + data_file_suff
data_url_3 = fixed_data_url_2 + data_url_id_3 + '/'
#下载最新的备用投票页面
download_url_to_file(data_url_3, data_file_3_name)
file_convert_pagecode(data_file_3_name, source_pagecode_2, data_file_3_name, dest_pagecode)

for name in player_name:
    debug_info.append(name+'\n')

#解析下载的页面
print 'Download data over. Now start to analyse...'
debug_info.append('\nData from :' + data_url_1 + '\n')
analyse_file(data_file_name)
debug_info.append('\nData from :' + data_url_2 + '\n')
analyse_file(data_file_2_name)
debug_info.append('\nData from :' + data_url_3 + '\n')
analyse_file_b(data_file_3_name)

#不知为何不能直接调用group_num和group_size，只能写返回...
#但下面的rank可以直接引用......
[gn, gs] = get_final_rank()

print 'Analysis over. Now start to output result...'

sres = '<html><head>'
sres += '<meta http-equiv=Content-Type content="text/html;charset=utf-8">'
sres += '<title>AST 14 Web Data Scanner Ultra Lite</title>'
sres += '</head><body align=center>'

sres += 'AST 14 Web Data Scanner Ultra Lite, TestType, Enigma.H <br>'
sres += 'Report time : CST '+str(cur_date).split('.')[0]+'<br>'
sres += 'Counted token number = {0:d} <br>'.format(used_token.__len__())

for i in xrange(gn):
    sres += 'Group {0:d} <br>'.format(i+1)
    for j in xrange(gs):
        sres += 'Rank {0:d} : {1:3d} votes : {2:s} <br>'.format(j+1, rank[i][j][0], rank[i][j][1])

sres += '</body></html>'

res_html = open(result_file_name[mode], 'w')
res_html.write(sres)
res_html.close()
debug_info_file = open(debug_file_name[mode], 'w')
for info_str in debug_info:
    debug_info_file.writelines(info_str)
debug_info_file.close()

print 'Output result over.'