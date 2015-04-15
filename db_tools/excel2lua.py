#!/usr/bin/python
# encoding=utf-8
import sys, os
import xlrd

reload(sys)
sys.setdefaultencoding('utf-8')
# l 存储当前生成的lua文件名字
l = []

def main(seachPath):
    InputPath = seachPath
    readPath(seachPath)


def readPath(path):
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

# 生成所有的db表集合文件DBName.lua
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
        # 顺序下标访问
        # file.write(str(rownum-9))
        # excel第一个字段做下标,要判断下类型
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
    #main()
    main(sys.argv[1])