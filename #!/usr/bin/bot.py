#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
بوت تليجرام لإدارة تقييمات Google Maps
Google Maps Reviews Management Bot
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from config import BOT_TOKEN, ADMIN_IDS
from database import Database
from maps_handler import MapsHandler
from scraper import ReviewsScraper

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

class GoogleMapsBot:
    def __init__(self):
        self.db = Database()
        self.maps_handler = MapsHandler(self.db)
        self.scraper = ReviewsScraper()
        
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        self.db.add_user(user.id, user.username, user.first_name)
        
        keyboard = []
        if user.id in ADMIN_IDS:
            keyboard = [
                [InlineKeyboardButton("🗺️ استخراج التقييمات", callback_data="extract_reviews")],
                [InlineKeyboardButton("⭐ إدارة التقييمات", callback_data="manage_reviews")],
                [InlineKeyboardButton("📊 التحليلات", callback_data="analytics")],
                [InlineKeyboardButton("⚙️ الإعدادات", callback_data="settings")]
            ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        welcome_text = f"""
🗺️ **مرحباً {user.first_name}!**

بوت إدارة تقييمات Google Maps

**المميزات:**
✅ استخراج التقييمات من أي مكان
✅ تحليل المشاعر التلقائي
✅ إحصائيات مفصلة
✅ إدارة احترافية
        """
        
        await update.message.reply_text(welcome_text, parse_mode='Markdown', reply_markup=reply_markup)
    
    def run(self):
        application = Application.builder().token(BOT_TOKEN).build()
        application.add_handler(CommandHandler("start", self.start_command))
        application.add_handler(CallbackQueryHandler(self.callback_handler))
        
        logger.info("🚀 تم بدء بوت Google Maps بنجاح!")
        application.run_polling(allowed_updates=Update.ALL_TYPES)
    
    async def callback_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        
        if query.data == "extract_reviews":
            await self.maps_handler.extract_reviews_menu(update, context)

if __name__ == '__main__':
    bot = GoogleMapsBot()
    bot.run()
