#!/usr/bin/env python
import mysql.connector as msql
from mysql.connector import Error
import time

conn=None
def connect():
    try:
        conn = msql.connect(host="185.145.254.208",port="3306",database="pricesuser_prices_db" ,user='pricesuser_umar',password='Price@123.,')
        return conn
    except Exception as e:
        print(e)
    

def getManufacturer(name):
    try:
        if(conn is not None):
            sql=f'''SELECT ID FROM tb_manufacturer WHERE Name="{name}"'''
            cursor=conn.cursor()
            result=cursor.execute(sql)
            result=cursor.fetchone()
            if(result is None):
                return result
            else:
                return result[0]
    except Exception as e:
        print(e)

def insertProduct(beIsWeighted,itemCode,itemName,itemStatus,itemType,manufacturerDescription,manufacturerID,qtyInPckg,quantity,unitOfMeasure,unitQty):
    try:
        if(conn is not None):
            if(conn.is_connected()):
                sql=f'''INSERT INTO `tb_products` (`ManufacturerID`, `ItemCode`, `ItemType`, `ItemName`,
                        `ManufacturerDescription`, `UnitQty`, `Quantity`, `BeIsWeighted`, `UnitOfMeasure`, `QtyInPackage`, `ItemStatus`)
                        VALUES ('{manufacturerID}', '{itemCode}', '{itemType}', '{itemName}', '{manufacturerDescription}', '{unitQty}', '{quantity}',
                        '{beIsWeighted}', '{unitOfMeasure}', '{qtyInPckg}','{itemStatus}')'''
                cursor=conn.cursor()
                cursor.execute(sql)
                conn.commit()
    except Exception as e:
        print(e)
def getProductID(branchID,companyID,itemCode):
    try:
        if(conn is not None):
            if(conn.is_connected()):
                sql=f'''SELECT ProductID FROM tb_products WHERE BranchID='{branchID}' AND CompanyID='{companyID}' AND ItemCode="{itemCode}"'''
                cursor=conn.cursor()
                result=cursor.execute(sql)
                result=cursor.fetchone()
                if(result is None):
                    return result
                else:
                    return result[0]
    except Exception as e:
        print(e)
def insertManufacturer(name,company):
    try:
        if(conn is not None):
            if(conn.is_connected()):
                sql=f'''INSERT INTO `tb_manufacturer` (`ID`, `Name`, `Country`) VALUES (NULL, '{name}', '{company}');'''
                cursor=conn.cursor()
                cursor.execute(sql)
                conn.commit()
    except Exception as e:
        print(e)

def insertBranch(branchID,companyID,chainID):
    try:
        if(conn is not None):
            if(conn.is_connected()):
                sql=f'''INSERT INTO `tb_branch` (`BranchID`, `CompanyID`, `ChainID`) VALUES ('{branchID}', '{companyID}', '{chainID}')'''
                cursor=conn.cursor()
                cursor.execute(sql)
                conn.commit()
    except Exception as e:
        print(e)


def insertPrice(itemCode,price,date,allowDiscount,unitOfMeasurePrice,companyID,branchID):
    try:
        if(conn is not None):
            if(conn.is_connected()):
                sql=f'''INSERT INTO `tb_price` (`ItemCode`, `CompanyID`, `BranchID`, `Price`, `Date`, `AllowDiscount`, `UnitOfMeasurePrice`)
                VALUES ('{itemCode}', '{companyID}', '{branchID}', '{price}', '{date}', '{allowDiscount}', "{unitOfMeasurePrice}")'''
                cursor=conn.cursor()
                cursor.execute(sql)
                conn.commit()
    except Exception as e:
        print(e)

