# Customer Analytics Final

__Eray Ates, Sibel Gurbuz__

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

## Add fake values in it

Please edit __config.json__ file for authentication to database and fake data settings.

```shell
python main.py
```