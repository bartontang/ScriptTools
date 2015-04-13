#!/usr/bin/python
# encoding=utf-8
import sys, os
import xlrd
import sqlite#, mysql

reload(sys)
sys.setdefaultencoding('utf-8')

def main(dbName, seachPath):
    readPath(dbName, seachPath)

def readPath(dbName, path):
    if os.path.isfile(path):
        ext = os.path.splitext(path)
        if ext[1] == ".xlsx" or ext[1] == ".xls":
            ############################
            readExcel(sqlite, dbName, path)
 #           readExcel(mysql, dbName, path)
    elif os.path.isdir(path):
        for item in os.listdir(path):     
            readPath(dbName, os.path.join(path, item))

def readExcel(db, dbName, fileWithPathAndExt):
    excel = open_excel(fileWithPathAndExt)

    tableName = os.path.split(fileWithPathAndExt)[1].split(".")[0]

    con = db.connect(dbName)
    cur = con.cursor()

    db.init(con, cur)

    isSucceed = True
    try:
        cur.execute(db.getDropTableSqlString(tableName))
        # col_name = excel.sheets()[0].row_values(db.dataNameRow,0,-1)
        # print ".....str=%s" % col_name
        cur.execute(db.getCreateTableSqlString(tableName, excel.sheets()[0].row_values(db.dataNameRow, db.dataBeginCol, -db.dateEndColBackOffset), excel.sheets()[0].row_values(db.dataTypeRow, db.dataBeginCol, -db.dateEndColBackOffset)))
        for sheet in excel.sheets():
            readSheet(db, tableName, sheet, cur)
        con.commit()
    except Exception as e:
        isSucceed = False
        db.printException(e)
    finally:
        cur.close
        con.close 

    db.printResult(tableName, isSucceed)


def readSheet(db, tableName, sheet, cursor):
    if not isSheetIsGood(sheet):
        return
    insertSqlString, array = db.getInsertSqlString(tableName, sheet.row_values(db.dataNameRow, db.dataBeginCol, -db.dateEndColBackOffset))
    for row in range(db.dataBeginRow, sheet.nrows):
        row_data = []
        for col in range(db.dataBeginCol, sheet.ncols - db.dateEndColBackOffset):
            if col in array:
                continue
            data = sheet.cell(row, col).value
            row_data.append(data)
        cursor.execute(insertSqlString, row_data)

###################################
def open_excel(file):
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception,e:
        print str(e)
   

#################################
#各种判断
#判断是否是有效的sheet
def isSheetIsGood(sheet):
    return sheet.nrows > 0 and sheet.ncols > 0
#End各种判断




if __name__=="__main__":
    #main()
    main(sys.argv[1], sys.argv[2])
