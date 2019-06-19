# coding:utf-8
# 提取特征列表
import json
import pandas as pd

class Similairity(object):
    def __init__(self, syno_dict, cases, fail_cases): # 定义变量
        self.syno_dict = syno_dict
        self.cases = cases
        self.fail_cases = fail_cases

    def read_json(self, json_file): # 读取json文件
        with open(json_file, 'r', encoding='utf-8') as file:
            return json.load(file)

    def find_all_index(self, str, sub): # 找到字符串中关键词的位置
        i = 0
        index = []
        while i <= len(str):
            result = str.find(sub, i)
            if result != -1:
                index.append(result)
                i = result + 2
            else:
                break
        return index

    def index_to_keywords(self, dict): # 将index转换为keywords
        list_all = []
        for i in list(dict.keys()):
            list_all += dict[i]
        list_all.sort()
        # print(list_all)
        for i in list_all:
            # print(i)
            for j in list(dict.keys()):
                if i in dict[j]:
                    list_all[list_all.index(i)] = j
        return list_all

    def character_extraction(self, syno_dict, case_dict): # 特征提取
        index_dict = {}
        character_dict = {}
        for i in list(case_dict.keys()):
            result = case_dict[i]
            for j in list(syno_dict.keys()):
                index_list = []
                for k in syno_dict[j]:  # k 是key中每一个value
                    index_list += self.find_all_index(result, k)
                index_dict[j] = index_list
            character_dict[i] = self.index_to_keywords(index_dict)
        return character_dict

    def cal_corr(self, character_list_a, character_list_b): # 求两个特征提取后的case之间的相关系数
        same_element_length = min(len([l for l in character_list_a if l in character_list_b]),len([l for l in character_list_b if l in character_list_a]))
        dice = 2 * same_element_length / (len(character_list_a) + len(character_list_b))

        def order_sum(character_list):
            order = {}
            count = 0
            for i in set(character_list):
                for j in range(len(character_list)):
                    if character_list[j] == i:
                        count += j + 1
                        order[i] = count
                count = 0
            return order

        order_sum_dict_a = order_sum(character_list_a)
        order_sum_dict_b = order_sum(character_list_b)

        def all_list(arr):
            result = {}
            for i in set(arr):
                result[i] = arr.count(i) / len(arr)
            return result

        para_dict = all_list(character_list_a + character_list_b)

        order_sum_diff = {}
        all_keys = set(order_sum_dict_a.keys()) | set(order_sum_dict_b.keys())
        # print(all_keys)
        for i in all_keys:
            if i in order_sum_dict_a.keys() and i in order_sum_dict_b:
                order_sum_diff[i] = abs(order_sum_dict_a[i] - order_sum_dict_b[i])
            elif i not in order_sum_dict_a.keys():
                order_sum_diff[i] = order_sum_dict_b[i]
            elif i not in order_sum_dict_b.keys():
                order_sum_diff[i] = order_sum_dict_a[i]

        s = sum(order_sum_diff.values())
        for i in order_sum_diff.keys():
            if s != 0:
                order_sum_diff[i] = order_sum_diff[i] / s
            else:
                order_sum_diff[i] = 0
        # print(order_sum_diff)
        order = 0
        for i in para_dict.keys():
            for j in order_sum_diff.keys():
                if i == j:
                    order += para_dict[i] * order_sum_diff[j]
        if dice - 0.2 * order <= 0:
            corr = 0
        else:
            corr = dice - 0.2 * order
        return corr

    # def

    def main(self):
        # 数据导入
        syno_dict = self.read_json(self.syno_dict)
        case_dict = self.read_json(self.cases)
        # 数据预处理
        for i in list(case_dict.keys()):
            case_dict[i] = str("'" + i + "'") + ' : ' + str(case_dict[i])
        # 特征提取
        character_dict = self.character_extraction(syno_dict, case_dict)
        print('character_dict is %s' % character_dict)

if __name__ == '__main__':
    result = Similairity('syno_dict.json', 'cases.json', 'a')
    result.main()



