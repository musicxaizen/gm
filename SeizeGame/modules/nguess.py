from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import random
from SeizeGame.database import collection, user_collection
from config import CHAT_ID
import asyncio

# nguess
async def nguess(update: Update, context: CallbackContext):
    if CHAT_ID:
        return
    if chat_id in current_charector:
        await update.message.reply_text("Guess is already in progress")
        return
    try:
        characters = await collection.find().to_list(100000)
        random_character = random.choice(characters)
        nobi_charector = random_character["collection"]
        character_name = random_character["charector_name"]
        await update.message.reply_photo(nobi_charector, caption="✨🌟 Who is this Mysterious Character?? 🧐🌟✨")
        start_time = asyncio.get_event_loop().time()
        while True:
            if asyncio.get_event_loop().time() - start_time >= 20:
                await update.message.reply_text(f"Time's up! The character was {character_name}")
                break
            await asyncio.sleep(1)
    except Exception as e:
        await update.message.reply_text("Error occurred!")

# name check
async def name(update: Update, context: CallbackContext):
    try:
        charector = update.message.text
        charectors = await collection.find().to_list(100000)
        for character in charectors:
            if charector["charector_name"].lower() == charector.lower():
                await update.message.reply_text(f"🎉 Correct! You've earned 50 coins! Your current streak is {streak}! 🎉")
                user_id = mesaaage.from_user.id
                user_data = await user_collection.find_one({'id': user_id})
                if user_data:
                    user_data['Balance'] += 50
                    user_data["streak"] += 1
                    if user_data["streak"] == 30:
                        user_data['Balance'] += 3000
                        await update.message.reply_text("🎉 30-streak! Earned 3000 coins! 🎉")
                    elif user_data["streak"] == 50:
                        user_data['Balance'] += 4000
                        await update.message.reply_text("🎉 50-streak! Earned 4000 coins! 🎉")
                    elif user_data["streak"] == 100:
                        user_data['Balance'] += 5000
                        await update.message.reply_text("🎉 100-streak! Earned 5000 coins! 🎉")
                    await user_collection.update_one({'id': user_id}, {"$set": user_data})
                else:
                    await user_collection.insert_one({'id': user_id, 'Balance': 50, "streak": 1})
                return
    except Exception as e:
        await update.message.reply_text("error occurred")
        
        