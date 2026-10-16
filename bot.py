import os
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎬 أهلاً! أرسل لي رابط فيديو من:\n"
        "✅ TikTok\n✅ Instagram\n✅ YouTube\n"
        "✅ Facebook\n✅ Twitter/X\n✅ وغيرها!"
    )

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    await update.message.reply_text("⏳ جاري التحميل...")

    ydl_opts = {
        'outtmpl': '/tmp/%(title)s.%(ext)s',
        'format': 'best[filesize<50M]/best',
        'noplaylist': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        await update.message.reply_video(
            video=open(filename, 'rb'),
            caption=f"✅ {info.get('title', 'الفيديو')}"
        )
        os.remove(filename)

    except Exception as e:
        await update.message.reply_text(f"❌ ما اكدرت أحمل\nالسبب: {str(e)}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))
    print("البوت شغال! ✅")
    app.run_polling()

if __name__ == "__main__":
    main()