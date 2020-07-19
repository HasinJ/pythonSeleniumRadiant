import MySQLdb
import config
import os
import os.path as path

def connectDB():
    mydb = MySQLdb.connect(host = config.RDS_HOSTNAME,
        user = config.RDS_USER,
        passwd = config.RDS_PASSWORD,
        db = config.RDS_DBNAME)
    return mydb

def insertDatePK(values):
    mydb = connectDB()
    cursor = mydb.cursor()

    sql = 'INSERT INTO DateTBL (`Date`,`DOW`,`TOD`,`Month`,`Day`,`Year`) VALUES (%s,%s,%s,%s,%s,%s)'
    val = values
    cursor.execute(sql,val)

    mydb.commit()
    cursor.close()

def moveOneTempSQL(target):
    mydb = connectDB()
    cursor = mydb.cursor()
    sql=''

    #this is pretty specific
    destination = config.dir + fr'\Consumption Table Queries\Insert Queries\{target} Insert.txt'
    if path.exists(destination)==True:
        with open(destination) as f:
            for line in f:
                if line.strip()=='Order by Item':
                    sql += line.strip()
                    break
                sql+=line.strip() + ' '

    cursor.execute(sql)
    mydb.commit()
    print(sql)
    cursor.close()

def moveAllTempSQL():
    mydb = connectDB()
    cursor = mydb.cursor()

    dirList = os.listdir(config.dir + fr'\Consumption Table Queries\Insert Queries')


    #for every file in directory
    for file in dirList:
        sql=''
        destination = config.dir + fr'\Consumption Table Queries\Insert Queries\{file}'
        if path.exists(destination)==True:
            with open(destination) as f:
                while True:
                    line = f.readline()
                    if not line:
                        sql+=line.strip()
                        break
                    sql+=line.strip() + ' '
                #print(sql) #checks sql
                cursor.execute(sql)

    mydb.commit()
    cursor.close()

def oneFile(folder, file):
    mydb = connectDB()
    cursor = mydb.cursor()

    destination = config.dir + fr'\Consumption Table Queries\{folder}\{file}'

    with open(destination) as f:
        sql=''
        while True:
            line = f.readline()
            if not line:
                sql+=line.strip()
                break
            sql+=line.strip() + ' '
        #print(sql) #checks sql
        cursor.execute(sql)

    cursor.execute(sql)
    mydb.commit()
    cursor.close()


#run this to empty temp table
#oneFile('Temp','TempTable Truncate.txt')

##sql query def template:
#mydb = connectDB()
#cursor = mydb.cursor()
#cursor.execute(sql) #the rest from here (including) are for commiting
#mydb.commit()
#cursor.close()
