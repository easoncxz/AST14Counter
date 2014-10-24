# coding: utf-8
__author__ = 'Enigma'

#信号与范围定义
max_player_size   = 100
token_used        = 0x1401
no_token          = 0x1402
player_too_much   = 0x1403
no_contest        = 0x1404
contest_not_start = 0x1405
contest_ended     = 0x1407
server_mode       = 1
local_mode        = 0

#页面转码用到的编码
source_pagecode   = 'shift_jisx0213'
source_pagecode_2 = 'euc_jisx0213' 
dest_pagecode     = 'utf-8'

#解析投票页面所需要用到的字符串
fixed_data_url    = 'http://saimoe.thread.jp/test/read.cgi/ast/'
fixed_data_url_2  = 'http://jbbs.shitaraba.net/bbs/read.cgi/anime/10101/'
data_url_2_filter = '投票補助'
data_url_2_offset = '1411915367/l50">2</a> : <a href="#2">アニメ最萌トーナメント2014 '
fixed_conf_url    = 'http://www2.saimoe2014.info/2014/config/config'
home_page_url     = 'http://saimoe.thread.jp/ast/'
home_page_url_2   = 'http://jbbs.shitaraba.net/anime/10101/'
bkup_title        = 'アニ'
bkup_title_pref   = '<a href'

#下载文件保存的路径
home_page_file_name   = ['E://Playground//AST14Py//data//homepage.html', '/AST14Py/data/homepage.html']
home_page_file_2_name = ['E://Playground//AST14Py//data//homepage2.html', '/AST14Py/data/homepage2.html']
download_path         = ['E://Playground//AST14Py//data//', '/AST14Py/data/']
result_file_name      = ['E://Playground//AST14Py//res.html', '/var/www/res.html']
debug_file_name       = ['E://Playground//AST14Py//debuginfo.txt', '/var/www/debuginfo.txt']

#文件名后缀
data_file_suff  = '.html'
conf_file_suff  = '.txt'
check_file_suff = '.chk'

#解析投票页面用到的字符串
vote_pref      = '&lt;&lt;'
vote_suff      = '&gt;&gt;'
floor_pref     = '<dt>'
floor_suff     = '<font'
floor_pref_2   = '>'
floor_suff_2   = '</a>'
floor_filter   = ' '
token_pref     = '[[AS14-'
token_suff     = ']]-'
date_pref      = '：2014'
date_pref2     = '：'
date_suff      = '('
vote_time_pref = ') '
vote_time_suff = ' ID:'

#解析数据使用的变量
group_num = int()
group_size = int()
start_time_abs_min = 0
max_vote_per_group = 0
player_name  = []
used_token   = []
vote_time    = [[] for i in xrange(max_player_size)]
vote_floor   = [[] for i in xrange(max_player_size)]
player_group = [[] for i in xrange(max_player_size)]
rank         = [[] for i in xrange(max_player_size)]

debug_info   = []