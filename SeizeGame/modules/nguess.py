import asyncio
import aiohttp
from PIL import Image
from io import BytesIO
from config import CHAT_ID, UPLOAD_CHAT_ID, LOGGER_ID, SUDOERS
from SeizeGame.database import collection, user_collection
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import logging
import importlib
import random

# Upload handler
async def upload(update: Update, context: CallbackContext):
    if update.message.chat_id !=UPLOAD_CHAT_ID or SUDOERS not in sudoers:
        await update.message.reply_text("ask my owner")
        return

    try:
        message_text = update.message.text
        parts = message_text.split(" ", 2)
        if len(parts) != 3:
            await update.message.reply_text("Invalid format. Use /upload <character link> <character name>")
            return

        character_link = parts[1]
        character_name = parts[2]

        async with aiohttp.ClientSession() as session:
            async with session.get(character_link) as response:
                if response.status != 200:
                    await update.message.reply_text("Invalid link!")
                    return
                image_data = await response.read()

        image = Image.open(BytesIO(image_data))
        image = image.resize((1920, 1080), Image.LANCZOS)
        image_data = BytesIO()
        image.save(image_data, format="JPEG")
        image_data = image_data.getvalue()

        photo = await context.bot.send_photo(chat_id=LOGGER_ID, photo=image_data)
        photo_id = photo.photo[-1].file_id

        collection.insert_one({"charectors": photo_id, "character_name": character_name})

        await update.message.reply_text("Character uploaded successfully!")
    except aiohttp.ClientError:
        await update.message.reply_text("Invalid link!")
    except Exception as e:
        await update.message.reply_text("Error occurred!")

# Nguess handler
async def nguess(update: Update, context: CallbackContext):
    if update.message.chat_id != CHAT_ID:
        return

    try:
        characters = await collection.find().to_list(100000)
        random_character = random.choice(characters)
        nobi_charector = random_character["collection"]
        character_name = random_character["charector_name"]

        await Context.bot.send_photo(chat_id=CHAT_ID, nobi_charector, caption="✨🌟 Who is this Mysterious Character?? 🧐🌟✨")

        start_time = asyncio.get_event_loop().time()
        while True:
            if asyncio.get_event_loop().time() - start_time >= 20:
                await update.message.reply_text(f"Time's up! The character was {character_name}")
                break
            await asyncio.sleep(1)
    except Exception as e:
        await update.message.reply_text("Error occurred!")

# Name check handler
async def name(update: Update, context: CallbackContext):
    try:
        charector = update.message.text
        charectors = await collection.find().to_list(100000)
        for character in charectors:
            if charector["charector_name"].lower() == charector.lower():
                await update.message.reply_text(f"🎉 Correct! You've earned 50 bitcoins! Your current streak is {streak}! 🎉")
                user_id = message.from_user.id
                user_data = await user_collection.find_one({'id': user_id})
                if user_data:
                    user_data['Balance'] += 50
                    user_data["streak"] += 1
                    if user_data["streak"] == 30:
                        user_data['Balance'] += 3000
                        await update.message.reply_text("🎉 30-streak! Earned 3000 bitcoins! 🎉")
                    elif user_data["streak"] == 50:
                        user_data['Balance'] += 4000
                        await update.message.reply_text("🎉 50-streak! Earned 4000 bitcoins! 🎉")
                    elif user_data["streak"] == 100:
                        user_data['Balance'] += 5000
                        await update.message.reply_text("🎉 100-streak! Earned 5000 bitcoins! 🎉")
                    await user_collection.update_one({'id': user_id}, {"$set": user_data})
                else:
                    await user_collection.insert_one({'id': user_id, 'Balance': 50, "streak": 1})
                return
    except Exception as e:
        await update.message.reply_text("error occurred")
        