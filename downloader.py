
import sqlite3
from concurrent.futures import ThreadPoolExecutor
from time import sleep

from database import Database
from skyblock_api import SkyblockApi
from utils import Utils


class Downloader:

  @staticmethod
  def _put_data_to_db(datas, put_function):
    while datas:
      data = datas[-1]
      try:
        put_function(data)
        Utils.log(f'[{data["type"]}] Saved data', data['lastUpdated'])
        datas.pop()
      except sqlite3.OperationalError:
        Utils.log(f'[{data["type"]}] DATABASE ACCESS FAILED')
        break
      except Exception as e:
        Utils.log(f'[{data["type"]}] FAILED TO PUT DATA TO DATABASE')
        Utils.log(e)
    if len(datas) > 1:
      Utils.log(f'[{data["type"]}] {len(datas)} datas are waiting in queue')

  @staticmethod
  def _catch_input():
    while not Utils.quitting:
      inp = input()
      if inp == 'q':
        Utils.quitting = True
        Utils.log('Quitting')

  @staticmethod
  def _quit():
    Utils.log('Saving database')
    Database.connection.commit()
    Database.connection.close()
    Utils.log('Done!')

  @staticmethod
  def download_and_save_data():
    executor = ThreadPoolExecutor()
    bazaar_data = []
    bazaar_future = executor.submit(SkyblockApi.get_new_bazaar, bazaar_data)
    auctions_data = []
    auction_future = executor.submit(SkyblockApi.get_new_ended_auctions, auctions_data)
    executor.submit(Downloader._catch_input)
    while not Utils.quitting or bazaar_data or auctions_data or not bazaar_future.done() or not auction_future.done():
      Downloader._put_data_to_db(bazaar_data, Database.insert_bazaar)
      Downloader._put_data_to_db(auctions_data, Database.insert_auctions)
      sleep(0.1)
    Downloader._quit()
