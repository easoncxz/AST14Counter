# coding: utf8

import time
from AST14PyHeader import *

__author__ = 'Enigma'

#返回值的list顺序是[楼层，Token，投票绝对分钟，[投票列]]
def analyse_floor(floor_str):
    if floor_str.find('</dl>') > 0:
        return [-1, 'N/A', -1, 'N/A']

    if floor_str.find('ID') == -1:
        return [-1, 'N/A', -1, 'N/A']

    floor_num = floor_str[floor_str.find(floor_pref) + len(floor_pref):floor_str.find(floor_suff)]
    floor_num = floor_num[0:floor_num.find(floor_filter)]
    floor_num = int(floor_num)
    if floor_num == 1:
        return [-1, 'N/A', -1, 'N/A']

    token_start_pos = floor_str.find(token_pref)
    token_end_pos = floor_str.find(token_suff, token_start_pos)
    token = floor_str[token_start_pos:token_end_pos + len(token_suff) + 5]
    if not ((token_start_pos > 0) and (token_end_pos > token_start_pos)):
        token = 'N/A'
    if len(token) != 29:
        token = 'N/A'

    vote_date_str = floor_str[floor_str.find(date_pref) + len(date_pref2):floor_str.find(date_suff)]
    vote_time_str = floor_str[floor_str.find(vote_time_pref) + len(vote_time_pref):floor_str.find(vote_time_suff) - 3]
    vote_date_time = time.strptime(vote_date_str + ' ' + vote_time_str, '%Y/%m/%d %H:%M:%S')
    vote_abs_min = vote_date_time.tm_yday * 24 * 60 + vote_date_time.tm_hour * 60 + vote_date_time.tm_min
    vote_abs_min -= start_time_abs_min

    if vote_abs_min < 60:
        return [floor_num, token, contest_not_start, 'N/A']

    if vote_abs_min > (23 * 60):
        return [floor_num, token, contest_ended, 'N/A']

    if token == 'N/A':
        return [floor_num, token, vote_abs_min, 'N/A']

    ori_votes = floor_str.split(vote_suff)
    ori_votes.pop(ori_votes.__len__() - 1)
    votes = []
    for ov in ori_votes:
        pos = ov.find(vote_pref)
        votes.append(ov[pos + len(vote_pref):])
    votes = [floor_num] + [token] + [vote_abs_min] + votes

    return votes


#返回值的list顺序是[楼层，Token，投票绝对分钟，[投票列]]
def analyse_floor_b(floor_str):
    if floor_str.find('ID') == -1:
        return [-1, 'N/A', -1, 'N/A']

    floor_num = floor_str[floor_str.find(floor_pref_2) + len(floor_pref_2):floor_str.find(floor_suff_2)]
    floor_num = int(floor_num)
    if floor_num == 1:
        return [-1, 'N/A', -1, 'N/A']

    token_start_pos = floor_str.find(token_pref)
    token_end_pos = floor_str.find(token_suff, token_start_pos)
    token = floor_str[token_start_pos:token_end_pos + len(token_suff) + 5]
    if not ((token_start_pos > 0) and (token_end_pos > token_start_pos)):
        token = 'N/A'
    if len(token) != 29:
        token = 'N/A'

    vote_date_str = floor_str[floor_str.find(date_pref) + len(date_pref2):floor_str.find(date_suff)]
    vote_time_str = floor_str[floor_str.find(vote_time_pref) + len(vote_time_pref):floor_str.find(vote_time_suff) - 1]
    vote_date_time = time.strptime(vote_date_str + ' ' + vote_time_str, '%Y/%m/%d %H:%M:%S')
    vote_abs_min = vote_date_time.tm_yday * 24 * 60 + vote_date_time.tm_hour * 60 + vote_date_time.tm_min
    vote_abs_min -= start_time_abs_min

    if vote_abs_min < 60:
        return [floor_num, token, contest_not_start, 'N/A']

    if vote_abs_min > (23 * 60):
        return [floor_num, token, contest_ended, 'N/A']

    if token == 'N/A':
        return [floor_num, token, vote_abs_min, 'N/A']

    ori_votes = floor_str.split(vote_suff)
    ori_votes.pop(ori_votes.__len__() - 1)
    votes = []
    for ov in ori_votes:
        pos = ov.find(vote_pref)
        votes.append(ov[pos + len(vote_pref):])
    votes = [floor_num] + [token] + [vote_abs_min] + votes

    return votes


def legal_config_file(file_name):
    cfg_file = open(file_name, 'r')
    s = cfg_file.read()
    if s.find('404 Not Found') >= 0:
        return no_contest
    else:
        return 1


def load_config_file(file_name):
    global start_time_abs_min, group_num, group_size, max_vote_per_group
    cfg_file = open(file_name, 'r')
    strat_time_str = cfg_file.readline()

    cfg_file.readline()
    [group_num, group_size, max_vote_per_group] = cfg_file.readline().split(' ')

    start_time = time.strptime(strat_time_str+' 00:00:00', '%y/%m/%d %H:%M:%S')
    start_time_abs_min = start_time.tm_yday * 24 * 60

    group_num = int(group_num)
    group_size = int(group_size)
    max_vote_per_group = int(max_vote_per_group)

    for i in xrange(group_num):
        for j in xrange(group_size):
            s = cfg_file.readline()
            player_name.append(s)
            player_group[i].append(s)

    return 1


def has_player(cur_player):
    for i in xrange(player_name.__len__()):
        if player_name[i].find(cur_player) >= 0:
            return i
    return -1


def group_of_user(cur_player):
    for i in xrange(group_num):
        if player_group[i].count(cur_player) > 0:
            return i


def add_vote(vote):
    [floor, token, vote_min] = vote[0:3]

    vote_players = vote[3:]
    if (vote_players.__len__() < 1) or (vote_players[0] == 'N/A'):
        return

    if used_token.count(token) > 0:
        return token_used
    if token == 'N/A':
        return no_token
    used_token.append(token)

    vote_min = int(vote_min)

    for vote_player in vote_players:
        player_id = has_player(vote_player)
        if player_id >= 0:
            vote_time[player_id].append(vote_min)
            vote_floor[player_id].append(floor)


def get_final_rank():
    for i in xrange(player_name.__len__()):
        group_id = group_of_user(player_name[i])
        player_id = player_name.index(player_name[i])
        vote_num = vote_floor[player_id].__len__()
        rank[group_id].append((vote_num, player_name[i].split(',')[0]))

    for i in xrange(group_num):
        rank[i].sort(reverse=True)

    return [group_num, group_size]


def analyse_file(dfname):
    data_file = open(dfname, 'r')
    data_text = data_file.read()
    floors = data_text.split('</dd>')
    floor_num = data_text.count('</dd>')
    data_file.close()

    for j in xrange(0, floor_num, 1):
        floor_res = analyse_floor(floors[j])
        add_vote(floor_res)
        if (floor_res[0] > -1) and (floor_res[2] != contest_not_start) and (floor_res[2] != contest_ended):
            if (floor_res[1] == 'N/A'):
                tmp_s = str(floor_res[0]).zfill(3) + ': Token not found \n'
            else:
                tmp_s = str(floor_res[0]).zfill(3) + ':' + str(floor_res[1]) + '\n'
            debug_info.append(tmp_s)


def analyse_file_b(dfname):
    data_file = open(dfname, 'r')
    data_text = data_file.read()
    floors = data_text.split('<dt>')
    floor_num = data_text.count('<dt>')
    data_file.close()

    #把分割出来的第一块扔掉
    floors.remove(floors[0])

    for j in xrange(797, floor_num, 1):
        floor_res = analyse_floor_b(floors[j])
        add_vote(floor_res)
        if (floor_res[0] > -1) and (floor_res[2] != contest_not_start) and (floor_res[2] != contest_ended):
            if (floor_res[1] == 'N/A'):
                tmp_s = str(floor_res[0]).zfill(3) + ': Token not found \n'
            else:
                tmp_s = str(floor_res[0]).zfill(3) + ':' + str(floor_res[1]) + '\n'
            debug_info.append(tmp_s)