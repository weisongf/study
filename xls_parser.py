#!/usr/bin/env python
# -*- coding:utf-8 -*-

import xlrd
import json
import codecs
import os


def read_excel():
    # 打开文件
    workbook = xlrd.open_workbook(r'test.xlsx')
    # 获取所有sheet
    print workbook.sheet_names()  # [u'sheet1', u'sheet1']
    sheet1_name = workbook.sheet_names()[0]

    # 根据sheet索引或者名称获取sheet内容
    sheet1 = workbook.sheet_by_index(0)  # sheet索引从0开始
    sheet1 = workbook.sheet_by_name('sheet1')

    # sheet的名称，行数，列数
    print sheet1.name, sheet1.nrows, sheet1.ncols
    total_rows = sheet1.nrows
    #计算nodes的数量
    nodes_nums = (total_rows - 8)/43
    print(nodes_nums)
    #获取nodes节点信息
    # nodes在第9行
    nodes_inrow = 8
    # nodes在第3列
    nodes_incol = 2
    #for i in xrange(1,nodes_nums,1):
    x1 = 9
    print(sheet1.col_slice(2, 9, 19), sheet1.col_slice(3, 9, 19))
    for i in (1,4,1):

        y1 = x1 + 43*i - 1
        x1 = y1 + 1
        print(sheet1.col_slice(2,x1-32,x1-32),sheet1.col_slice(3,x1-32,y1))
        #print(sheet1.col_values(2,x2,x2+1),sheet1.col_slice(3,x2+1,y2))

    # # 获取整行和整列的值（数组）
    # rows = sheet1.row_values(0) # 获取第四行内容
    # cols = sheet1.col_values(0)  # 获取第三列内容
    # print rows
    # #print cols
    # new_cols = cols.remove('')
    # print(sheet1.col_values(0,0)[0])
    # #环境整体信息
    # for list1,list2 in zip(sheet1.col_values(1, 0)[0:7],sheet1.col_values(2, 0)[0:7]):
    #     print(str(list1) + ":" + str(list2))
    # #nodes信息，8行第2列
    # print sheet1.cell_value(8,1)
    # #nodes通用信息serverid---ctime
    # nodes_row = 8
    # nodes_col = 1
    # print sheet1.col_values(2,8,19)
    #
    # #print(sheet1.col_values(1, 0)[0:7])
    # #print(new_cols[0])
    # # 获取单元格内容
    # # print sheet1.cell(1, 0).value.encode('utf-8')
    # # print sheet1.cell_value(1, 0).encode('utf-8')
    # # print sheet1.row(1)[0].value.encode('utf-8')
    #
    # # 获取单元格内容的数据类型
    # # print sheet1.cell(1, 0).ctype


if __name__ == '__main__':
    read_excel()