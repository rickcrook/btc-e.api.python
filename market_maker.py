# -*- coding: utf-8 -*-

from btceapi_python3 import btce_api
from json import dumps
from time import sleep

LIVE = True

#debug helper functions
def jprint(json):
   print(dumps(json, sort_keys=True,indent=2, separators=(',', ': ')))

# Load API keys from file, move to API
f = open('key.txt', "r")
api_key = f.readline().strip()
api_secret = f.readline().strip()

# static
pair = 'ltc_btc'
margin = 0.5 / 100 # 0.2% x2 fee + 0.1% profit
delay = 60 # period in seconds between api calls
amount = 0.1 # minimum on btce is 0.1 LTC
fee = 0.2 / 100 # fee on btce is 0.2

# init
btce = btce_api(api_key,api_secret, True)
trades =[]
profit = 0.0

while True:
   ticker = btce.getTicker(pair)
   ticker['mid'] = (ticker['sell'] + ticker['buy']) / 2.0 # maximum precision
   #print(ticker)

   # Checks what orders exist
   orders = {}
   active_orders = btce.ActiveOrders(pair)
   #jprint(active_orders)
   if active_orders['success']: # if orders then
      for order_id in list(active_orders['return'].keys()):
         order = active_orders['return'][order_id]
         order['order_id'] = order_id
         orders[order['type']] = order
   #jprint(orders)

   for order_type in ['buy','sell']:
      # if missing create order
      if order_type not in orders:
         order = {'type': order_type, 'amount':amount, 'pair': pair, 'margin': margin, 'ticker_mid': round(ticker['mid'],5), 'created': ticker['server_time'] }
         if order_type=='sell':
            order['rate'] = round(ticker['mid'] * (1+margin),5)
         else:
            order['rate'] = round(ticker['mid'] * (1-margin),5)
         if LIVE:
            trade = btce.Trade(order['pair'], order['type'], order['rate'], order['amount'])
            order['success'] = trade['success']
            if not trade['success']:
               print('ORDER ERROR:'+trade['error'])
               order['order_id']='-1'
            else:
               order['order_id']=trade['return']['order_id']
         else:
            order['success'] = 1
         print('NEW ORDER:',order)
         trades += [order]
         orders[order['type']] = order
      # Order status
      print(ticker['server_time'],order_type, orders[order_type]['rate'],ticker[order_type])

   # print flash pnl and closure on open orders
   sleep(delay)