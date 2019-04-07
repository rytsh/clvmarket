#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  4 22:03:23 2018.

@author: Eray Ates, Sibel Gürbüz
"""
from library.libx import *

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)

    config = jsonread("config.json")
    con_config = config["connection"]

    migros = MySQL(
        con_config["username"],
        con_config["password"],
        con_config["URL"],
        con_config["port"],
        con_config["db"]
        )
    
    