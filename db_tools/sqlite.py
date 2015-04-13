#!/usr/bin/python
# encoding=utf-8

import sqlite3

import sys, os, stat

reload(sys)
sys.setdefaultencoding('utf-8')

####################################
#常量
dataNameRow = 9     #字段名所在行数，从0开始，1表示第二行
dataTypeRow = 7     #类型名所在行数
dataBeginRow = 10    #数据开始的行数
dataBeginCol = 0    #数据开始的列数
dateEndColBackOffset = 1   #向后偏移一行
####################################
def connect(dbname):
    return sqlite3.connect(dbname + ".db")    

def init(con, cur):
    return True

def printResult(tablename, isSucceed):
    result = "succeed!"
    if not isSucceed:
        result = "failed!"
    print "SQLite:", tablename, result

def printException(e):
    print "SQLite Exception: ", e.args[0]

###################################
#sql语句
def getCreateTableSqlString(tableName, colNames, colTypes):
    sqlString = "create table if not exists " + tableName + "(_id integer primary key"

    if len(colNames) != len(colTypes):
        print "getCreateTableSqlString: 列名和列类型数量不一致"
        return

    for i in range(dataBeginCol, len(colNames)):
        if isServerWord(colNames[i]):
            continue
        aClo = ", " + colNames[i] + " " + colTypes[i]
        sqlString += aClo
    sqlString += ")"
    return sqlString

def getInsertSqlString(tableName, colNames):
    array = []
    sqlString = "insert into " + tableName + "("
    for i in range(dataBeginCol, len(colNames)):
        if isServerWord(colNames[i]):
            array.append(i)
            continue
        if i == dataBeginCol:
            sqlString += colNames[i]
        else:
            sqlString += ", " + colNames[i]
    sqlString += ") values("

    for i in range(dataBeginCol, len(colNames)):
        if isServerWord(colNames[i]):
            continue
        if i == dataBeginCol:
            sqlString += "?"
        else:
            sqlString += ", ?"
    sqlString += ")"
    return sqlString, array

def getDropTableSqlString(tableName):
    sqlString = "drop table if exists " + tableName
    return sqlString       

#是否是服务器独有的字段
def isServerWord(colNames):
    if "_server" in colNames:
        return True
    return False
    
#################################
#各种判断

#End各种判断
