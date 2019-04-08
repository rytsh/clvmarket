# Customer Analytics [ CLV SuperMarket ]

__Eray Ates, Sibel Gurbuz__

This is an example CLV project for Customer Analytics lesson by Assoc.Prof.Dr. Başar ÖZTAYŞİ.

Before to run python, execute this command
```shell
sudo pip install -r requirements
```

For debug put this in where you want
```python
import ipdb; ipdb.set_trace()
```

## Create MySQL DB

For create database run this command with your username and password.
```shell
mysql -u <username> -p < DB/migrosdb.sql
```

Generate ER diagram with eralchemy use this command, if you don't have eralchemy install from pip
```shell
eralchemy -i mysql+mysqlconnector://muser:muser@localhost:3306/Migros -o erd_from
_sqlite.pdf
```

## Add fake values in it

Please edit __config.json__ file for authentication to database and fake data settings.

```shell
python fill.py
```

## Check analysis on jupyter notebook page
```shell
calculateCLV.ipynb
```