from time import time

import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

from database import Database


class DataPlotter:

  @staticmethod
  def _format_coins(x: int, pos):
    if abs(x) < 1000:
      return x
    elif abs(x) < 1000 ** 2:
      return f'{x / 1000}k'
    elif abs(x) < 1000 ** 3:
      return f'{x / 1000 ** 2}m'
    else:
      return f'{x / 1000 ** 3}b'

  @staticmethod
  def _format_date(y: float, pos):
    sec = time() - y / 1000
    if abs(sec) < 60:
      return f'{round(sec, 1)}s'
    elif abs(sec) < 60 * 60:
      return f'{round(sec / 60, 1)}m'
    elif abs(sec) < 60 * 60 * 24:
      return f'{round(sec / 60 / 60, 1)}h'
    elif abs(sec) < 60 * 60 * 24 * 30:
      return f'{round(sec / 60 / 60 / 24, 1)}d'
    elif abs(sec) < 60 * 60 * 24 * 30 * 12:
      return f'{round(sec / 60 / 60 / 24 / 30, 1)}mo'
    else:
      return f'{round(sec / 60 / 60 / 24 / 30 / 12, 1)}y'

  @staticmethod
  def show_bazaar(product_id: str, complex=False):
    product_id = product_id.upper().replace(' ', '_')
    product_data = Database.get_bazaar_for_product(product_id)
    fig = plt.figure()
    fig.suptitle(product_id, fontsize=24)
    if complex:
      gs = gridspec.GridSpec(2, 2)
    else:
      gs = gridspec.GridSpec(1, 1)

    ax_price = plt.subplot(gs[0, 0])
    ax_price.plot(product_data['BazaarBuyPrice']['times'],
                  product_data['BazaarBuyPrice']['values'], 'r', label='Insta Buy = Sell Offer')
    ax_price.plot(product_data['BazaarSellPrice']['times'],
                  product_data['BazaarSellPrice']['values'], 'b', label='Insta Sell = Buy Order')
    ax_price.legend()
    ax_price.set_ylabel('Price', fontsize=18)
    ax_price.set_xlabel('Time ago', fontsize=18)
    ax_price.yaxis.set_major_formatter(FuncFormatter(DataPlotter._format_coins))
    ax_price.xaxis.set_major_formatter(FuncFormatter(DataPlotter._format_date))
    fig.add_subplot(ax_price)

    if complex:
      ax_volume = plt.subplot(gs[0, 1])
      ax_volume.plot(product_data['BazaarBuyVolume']['times'],
                     product_data['BazaarBuyVolume']['values'], 'r', label='Insta Buy = Sell Offer')
      ax_volume.plot(product_data['BazaarSellVolume']['times'],
                     product_data['BazaarSellVolume']['values'], 'b', label='Insta Sell = Buy Order')
      ax_volume.legend()
      ax_volume.set_ylabel('Volume', fontsize=18)
      ax_volume.set_xlabel('Time ago', fontsize=18)
      ax_volume.yaxis.set_major_formatter(FuncFormatter(DataPlotter._format_coins))
      ax_volume.xaxis.set_major_formatter(FuncFormatter(DataPlotter._format_date))
      fig.add_subplot(ax_volume)

      ax_moving = plt.subplot(gs[1, 0])
      ax_moving.plot(product_data['BazaarBuyMovingWeek']['times'],
                     product_data['BazaarBuyMovingWeek']['values'], 'r', label='Insta Buy = Sell Offer')
      ax_moving.plot(product_data['BazaarSellMovingWeek']['times'],
                     product_data['BazaarSellMovingWeek']['values'], 'b', label='Insta Sell = Buy Order')
      ax_moving.legend()
      ax_moving.set_ylabel('Weekly Moving Coins', fontsize=18)
      ax_moving.set_xlabel('Time ago', fontsize=18)
      ax_moving.yaxis.set_major_formatter(FuncFormatter(DataPlotter._format_coins))
      ax_moving.xaxis.set_major_formatter(FuncFormatter(DataPlotter._format_date))
      fig.add_subplot(ax_moving)

      ax_orders = plt.subplot(gs[1, 1])
      ax_orders.plot(product_data['BazaarBuyOrders']['times'],
                     product_data['BazaarBuyOrders']['values'], 'r', label='Insta Buy = Sell Offer')
      ax_orders.plot(product_data['BazaarSellOrders']['times'],
                     product_data['BazaarSellOrders']['values'], 'b', label='Insta Sell = Buy Order')
      ax_orders.legend()
      ax_orders.set_ylabel('Orders', fontsize=18)
      ax_orders.set_xlabel('Time ago', fontsize=18)
      ax_orders.yaxis.set_major_formatter(FuncFormatter(DataPlotter._format_coins))
      ax_orders.xaxis.set_major_formatter(FuncFormatter(DataPlotter._format_date))
      fig.add_subplot(ax_orders)

    plt.grid()
    plt.show()
