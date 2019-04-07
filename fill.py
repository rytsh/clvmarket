#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  7 15:53:27 +03 2019.

@author: Eray Ates, Sibel Gürbüz
"""

from library.libx import *
from functools import reduce
from faker import Faker

fake = Faker('tr_TR')

def fill_user_data(database, tablename, count):
    """Generate user data."""
    print("{} filling..".format(tablename))
    t_user_data = migros.getTable(tablename)
    query = db.insert(t_user_data)
    values_list = [ {
        'loyalty_card_id' : fake.credit_card_number(card_type='visa16'),
        'first_name'      : fake.first_name(),
        'last_name'       : fake.last_name(),
        'email'           : fake.free_email(),
        'mobile_phone'    : fake.phone_number(),
        'birthday'        : fake.date_of_birth(tzinfo=None, minimum_age=15, maximum_age=115),
        'date_joined'     : fake.date_time_between(start_date="-20y", end_date="now", tzinfo=None)
    } for _ in range(count) ]

    ResultProxy = database.connection.execute(query,values_list)

def fill_category(database, tablename, jsonpath):
    """Fill category database with json file."""
    print("{} filling..".format(tablename))
    t_category = database.getTable(tablename)
    data = jsonread(jsonpath)
    query = db.insert(t_category)
    ResultProxy = database.connection.execute(query,data['category'])

def fill_invoice(database, tablename, usertablename, count):
    """Fill Invoice with user table.

    Get All ID of users and random value of invoices
    """
    print("{} filling..".format(tablename))
    t_invoice = database.getTable(tablename)
    t_user_data = database.getTable(usertablename)

    query = db.select([t_user_data.columns.id, t_user_data.columns.date_joined])
    ResultProxy = database.connection.execute(query)

    query_invoice = db.insert(t_invoice)

    for auser in ResultProxy:
        values_list = [ {
            'user_id': auser[0],
            'invoice_date': fake.date_time_between(start_date=auser[1], end_date="now", tzinfo=None),
            'total_amount': 0
        } for _ in range(fake.random_int(max=count, min=1)) ]
        ResultProxy_invoice = database.connection.execute(query_invoice,values_list)

def fill_invoice_detail(database, tablename, invoicetablename, categorytablename, count):
    """Fill Invoice Details."""
    print("{} filling..".format(tablename))
    max_price = 100
    t_invoice = database.getTable(invoicetablename)
    t_category = database.getTable(categorytablename)
    t_invoice_detail = database.getTable(tablename)

    query_invoice = db.select([t_category.columns.id])
    ResultProxy = database.connection.execute(query_invoice)
    category_ids = ResultProxy.fetchall()
    cate = tuple(map(lambda x: x[0], category_ids))

    query_invoice = db.select([t_invoice.columns.id])
    ResultProxy = database.connection.execute(query_invoice)

    query_invoice_d = db.insert(t_invoice_detail)

    for ainvoice in ResultProxy:
        values_list = [ {
            'invoice_id': ainvoice[0],
            'category_id': fake.random_choices(elements=cate, length=1)[0],
            'amount': float('{}.{}'.format(fake.random_int(max=max_price),fake.random_int(max=99)))
        } for _ in range(fake.random_int(max=count, min=1))]
        ResultProxy_invoice_d = database.connection.execute(query_invoice_d,values_list)
        
        plusinvoice = db.update(t_invoice).\
            values(total_amount=(t_invoice.columns.total_amount + reduce((lambda x, y: x + y['amount']), values_list, 0))).\
            where(t_invoice.columns.id == ainvoice[0])
        database.connection.execute(plusinvoice)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)

    config = jsonread("config.json")
    con_config = config["connection"]
    fake_config = config["fakedata"]

    migros = MySQL(
        con_config["username"],
        con_config["password"],
        con_config["URL"],
        con_config["port"],
        con_config["db"]
        )

    response = input("Do you want to clear all datas in the database? [y/N]: ")
    if response and response.lower()[0] == 'y':
        migros.clearData()

    user_count = fake_config["user_count"]
    max_invoice_per_user = fake_config["max_invoice_per_user"]
    max_item_per_invoice = fake_config["max_item_per_invoice"]

    fill_user_data(migros, 'user_data', user_count)
    fill_category(migros, 'category', "infrastructure/products.json")
    fill_invoice(migros, 'invoice', 'user_data', max_invoice_per_user)
    fill_invoice_detail(migros, 'invoice_detail', 'invoice', 'category', max_item_per_invoice)
