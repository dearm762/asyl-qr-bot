import qrcode
from io import BytesIO
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram import executor

API_TOKEN = ""

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
white_black = True
background = "white"
color = "black"

@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Этот бот генерирует QR-коды. Просто отправьте текст или ссылку.")

@dp.message_handler(commands=['setting'])
async def setting(message: types.Message):
  if(white_black):
    await bot.send_message(message.chat.id,f"Цветовой фон: Черный-белый")
  else:
    await bot.send_message(message.chat.id,f"Цветовой фон: Белый-Черный")
    
  await bot.send_message(message.chat.id, "Для изменений между собой /switchColors")

@dp.message_handler(commands=['switchColors'])
async def setting(message: types.Message):
  global white_black
  global color
  global background
  if(white_black):
    white_black = False
    color = 'white'
    background = 'black'
  else:
    white_black = True
    background = "white"
    color = "black"
  await bot.send_message(message.chat.id,"Цвета успешно изменены")

@dp.message_handler()
async def generate_qr_code(message: types.Message):
    text = message.text
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=15,
        border=1,
    )
    qr.add_data(text)
    qr.make(fit=True)
    global white_black
    global color
    global background
    img = qr.make_image(fill_color=color, back_color=background)

    img_bytes = BytesIO()
    img.save(img_bytes)
    img_bytes.seek(0)

    await bot.send_photo(
        message.chat.id,
        photo=img_bytes,
        parse_mode=ParseMode.MARKDOWN,
    )
 

if __name__ == "__main__":
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)