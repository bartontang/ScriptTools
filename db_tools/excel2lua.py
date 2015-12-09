#!/usr/bin/python
# encoding=utf-8
import sys, os, shutil, json
import xlrd

reload(sys)
sys.setdefaultencoding('utf-8')
# l 存储当前生成的lua文件名字
l = []
# 存放mutable的表
dic = {}

def main(seachPath):
    InputPath = seachPath
    readPath(seachPath)


def readPath(path):
    readJsonKeys(path)

    # for key in dic:
    #     print "key = %s" % key
    #     array = dic[key]
    #     for i in xrange(0, len(array)):
    #         print array[i]

	#
    filelist = os.listdir(path)
	# 遍历文件夹下的所有文件
    for n in range(len(filelist)):
        file = filelist[n]
        if ".xls" in file:
            readExcel(path+"/"+file, path)

    outputPath = path + "/" + "out/"
    createDBFile(l, outputPath)

def open_excel(file):
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception,e:
        print str(e)

# 生成所有的db表集合
def createDBFile(l, path):
    targetFileName = path + "DBName.lua"
    f = open(targetFileName, "w")
 
    for i in xrange(0, len(l)):
        element = l[i]
        lua_file_name = "require \"db." + element + "\""
        f.write(lua_file_name)
        print(lua_file_name)
        f.write("\n")
    f.close()

# 是否为服务器字段
def isServerField(field):
    if "server" in field:
        return True
    return False

# 是否为MutableTable(不打入表的第一个字段)
def isMutableTable(file, dirPath):
    # fp = open(dirPath + '/mutable_client.json', 'r') 
    # jsonobj = json.load(fp)
    # obj = jsonobj['mutable']

    # if file in obj:
    #     return True
    return False

# 读取mutable_client_keys json文件，保存需要多个key支持的excel文件名
def readJsonKeys(dirPath):
    allpath = dirPath + os.sep + 'mutable_client_keys.json'
    if os.path.exists(allpath) == False:
        return
    fp = open(allpath, 'r') 
    jsonobj = json.load(fp)
    for key in jsonobj:
        keys_array = jsonobj[key]
        dic[key] = keys_array
    fp.close()


def readExcel(fileWithPathAndExt, dirPath):
    # 打开工作表
    excel = open_excel(fileWithPathAndExt)
    # 获得表名
    tableName = os.path.split(fileWithPathAndExt)[1].split(".")[0]
    # 获得第一个sheet,约定只在sheet1中配置数据
    sheet = excel.sheet_by_index(0)

    # #sheet数量
    # count = len(excel.sheets()) 
    # for sheet in excel.sheets():
    #     print sheet.name 

    # print(tableName)
    
    is_MutableTable = False

    # if isMutableTable(tableName, dirPath):
    #     is_MutableTable = True

    # # 行数
    nrows = sheet.nrows
    outputPath = dirPath + "/" + "out/"
    # 加一个db_前缀, 标记为excel导出的db数据
    reallyTableName = "db_" + tableName
    l.append(reallyTableName)

    targetFileName = outputPath+reallyTableName+".lua"
    file = open(targetFileName, "w")
    file.write(reallyTableName)
    file.write(" = ")
    file.write("{\n");
    
    spaceIndex = 0
    #真实数据开始行
    dbBeginRow = 9
    # 获取每个字段名
    # 总共多少个字段
    colnames = sheet.row_values(dbBeginRow)
    # 最后一列也打进去
    totalColNum = len(colnames) - 1
    # for x in range(totalColNum):
    #     print colnames[x]

    typeNameList = sheet.row_values(dbBeginRow - 2)
    # for x in range(len(typeNameList)):
    #     print typeNameList[x]

    for rownum in range(dbBeginRow+1,nrows):
        row = sheet.row_values(rownum)
        file.write("[")
        # 如果在多个key支持的表里
        if dic.has_key(tableName):
            file.write("\"")
            keys_array = dic[tableName]
            for index in xrange(0,len(keys_array)):
                row_index = int(keys_array[index])
                value = row[row_index]
                file.write(str(value))
                if index < len(keys_array)-1:
                    file.write(", ")    
            file.write("\"")
        else:
            if typeNameList[0] == "string":
                file.write("\"")
                tmp = str(row[0])
                file.write(tmp)
                file.write("\"")
            else:
                tmp = str(row[0])
                file.write(tmp)
        file.write("] = ")
        
        file.write("{");
        for i in range(totalColNum):
            if isServerField(colnames[i]):
                continue
            file.write(colnames[i])
            # 字段的类型值
            typeValue = typeNameList[i]
            file.write(" = ")
            if typeValue == "string":
                file.write("\"")
                tmp = str(row[i])
                file.write(tmp)
                file.write("\"")
            else:
                tmp = str(row[i])
                file.write(tmp)
            if rownum < nrows:
                file.write(", ")
        file.write("},")
        file.write("\n")
    file.write("}")
    file.close()
        
if __name__=="__main__":
    main(sys.argv[1])