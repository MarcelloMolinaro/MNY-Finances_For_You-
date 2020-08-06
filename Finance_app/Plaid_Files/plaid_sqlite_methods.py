# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 23:17:40 2020

@author: marcello
"""
import sqlite3

#changed indexNum from "index"
#replaced all "." with "_"'s
														
col_names_type =  '''
        indexNum INTEGER, 
        account_id TEXT,
        account_owner TEXT,
        amount DECIMAL,
        authorized_date DATETIME,
        category TEXT,
        category_id INTEGER,
        date DATETIME,
        iso_currency_code TEXT, 
        
        merchant_name TEXT,
        name TEXT,
        payment_channel TEXT,
        pending INTEGER,
        pending_transaction_id TEXT,
        transaction_code TEXT,
        transaction_id TEXT,
        transaction_type TEXT,
        unofficial_currency_code TEXT,

        location_address TEXT,
        location_city TEXT,
        location_country TEXT,
        location_lat TEXT,
        location_lon TEXT,
        location_postal_code TEXT,
        location_region TEXT,
        location_store_number TEXT,
        
        payment_meta_by_order_of TEXT,
        payment_meta_payee TEXT,
        payment_meta_payer TEXT,
        payment_meta_payment_method TEXT,
        payment_meta_payment_processor TEXT,
        payment_meta_ppd_id TEXT,
        payment_meta_reason TEXT,
        payment_meta_reference_number TEXT
        '''
col_names = '''
        indexNum,
        account_id,
        account_owner,
        amount,
        authorized_date,
        category,
        category_id,
        date,
        iso_currency_code,
        
        merchant_name,
        name,
        payment_channel,
        pending,
        pending_transaction_id,
        transaction_code,
        transaction_id,
        transaction_type,
        unofficial_currency_code,
        
        location_address,
        location_city,
        location_country,
        location_lat,
        location_lon,
        location_postal_code,
        location_region,
        location_store_number,
        
        payment_meta_by_order_of,
        payment_meta_payee,
        payment_meta_payer,
        payment_meta_payment_method,
        payment_meta_payment_processor,
        payment_meta_ppd_id,
        payment_meta_reason,
        payment_meta_reference_number
        '''

#Create table SQLite syntax
def createTable(connection, table_name):
                #unique to my database: ID and Timestamp
         connection.execute( "CREATE TABLE " + table_name + '''
                (database_ID INTEGER PRIMARY KEY,
                Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,''' + \
                col_names_type + ")")
                          
def updateTable(connection, table_name, temp_table):
        connection.execute( 
                "INSERT INTO " + table_name + \
                "(" + col_names + ")" + \
                "SELECT * FROM " + temp_table + \
              ''' WHERE transaction_id NOT IN 
                        (SELECT transaction_id FROM '''+ table_name + ") " + \
                "AND pending != 1"
                ) 
        
def countRows(connection, table_name):
        command = "SELECT count(*) FROM " + table_name
        connection.execute(command)
        row_count = int(connection.fetchone()[0])
        return row_count