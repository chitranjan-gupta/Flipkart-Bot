import re
import time
import requests
from bs4 import BeautifulSoup
from aiogram import *
import logging
import os

BOT_TOKEN = os.environ.get('token') #Token used by telegram to authorize the use of bot
logging.basicConfig(level=logging.INFO)
prices = []
url = "https://www.flipkart.com/oneplus-bullets-wireless-z2-bluetooth-headset/p/itm4c3852314bb61"
status = False
Time = 60*60

async def Request(message: types.Message):
    session = requests.Session()
    session.headers.update({
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
        'Accept-Language':'en-US, en;q=0.5'
    })
    data = session.get(url)
    if data.status_code == 200:
        soup = BeautifulSoup(data.content,'lxml')
        pricediv = soup.find("div",attrs={"class":'_30jeq3 _16Jk6d'})
        currentprice = float(re.sub("[₹,$]","",pricediv.string,flags=re.IGNORECASE))
        if len(prices) >= 1:
            if currentprice < prices[-1]:
                prices.append(currentprice)
                await message.answer(f"Current Price: ₹{currentprice}")
        else:
            prices.append(currentprice)
            await message.answer(f"Current Price: ₹{currentprice}")
    else:
        print("Error")

bot = Bot(token=BOT_TOKEN)
disp = Dispatcher(bot=bot)
@disp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
  await message.answer(f"""Hi! {message['from']['first_name']} \n Welcome You to Flipkart Product Price Tracker Bot \n 
  You can track the price of Flipkart Product by sending the link.\n You can send the link using the command /link url \n""")

@disp.message_handler(commands=['TStart'])
async def send_welcome(message: types.Message):
  global status,Time
  if status == False:
    status = True
    await message.answer("Started Tracking...")
    while status == True:
      await Request(message)
      time.sleep(Time)
  else:
    await message.answer("Tracking is already running")

@disp.message_handler(commands=['TStop'])
async def send_welcome(message: types.Message):
  global status
  if status == True:
    status = False
    await message.answer("Stopped Tracking.")
  else:
    await message.answer("Tracking is already stopped.")

@disp.message_handler(commands=['link'])
async def send_welcome(message: types.Message):
  global status,url
  if status == False:
    url = message['text'].replace("/link","")
    await message.answer("Link is Added to tracking\n To Start Tracking send command /TStart \nand to Stop Tracking send command /TStop")

@disp.message_handler(commands=['help'])
async def send_welcome(message: types.Message):
  await message.reply("Type /start to Interact With The Bot")

if __name__ == '__main__':
  executor.start_polling(disp)
