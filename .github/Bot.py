import telebot
import yt_dlp
import os

# ضع التوكن الذي حصلت عليه من BotFather هنا
TOKEN = os.getenv('7468611784:AAH9ccG70XzzeQ89xsNVQZoYZTSY5IhDh1A')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "مرحبًا! أرسل لي رابط الفيديو لتنزيله.")

@bot.message_handler(func=lambda message: True)
def download_video(message):
    url = message.text
    bot.reply_to(message, f"جارٍ تنزيل الفيديو من {url}")
    
    ydl_opts = {
        'outtmpl': '%(title)s.%(ext)s',
        'format': 'best'
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            video_title = info_dict.get('title', None)
            video_file = ydl.prepare_filename(info_dict)
            ydl.download([url])

        with open(video_file, 'rb') as video:
            bot.send_video(message.chat.id, video)
        
        os.remove(video_file)
        bot.send_message(message.chat.id, "تم التحميل بنجاح!")

    except Exception as e:
        bot.reply_to(message, f"حدث خطأ: {e}")

bot.polling()
