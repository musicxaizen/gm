from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from motor import motor_asyncio
from pymongo import MongoClient
import aiohttp
import json
import os
import config
from PIL import Image
from io import BytesIO
from config import BOT_TOKEN, CHAT_ID, UPLOAD_CHAT_ID, LOGGER_ID, SUDOERS
import random

# Client setup
app = Client("seize", bot_token=BOT_TOKEN)

# MongoDB connection

#client 1 collection db url
Client_1 = motor_asyncio.asyncIOMotorClient(config.MONGO_DB_URI)
db_1 = Client_1['seize_collection']

#client 2 coin update db url
Client_2 = motor_asynio.asyncIOMotorClient(config.MONGO_DB_UPDATE_URI)
db_2 = Client_2['Charector_catcher']

user_collection = db_2["user_collection_lmaoooo"]


#-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_
collection = db_1["charectors"]


# Upload handler
@app.on_message(filters.command("upload"))
async def upload(client, message):
    if update.message.chat_id != UPLOAD_CHAT_ID or SUDOERS not in sudoers:
        await message.reply("Ask my owner")
        return
    try:
        message_text = message.text
        parts = message_text.split(" ", 2)
        if len(parts) != 3:
            await message.reply("Invalid format. Use /upload <character link> <character name>")
            return
        character_link = parts[1]
        character_name = parts[2]
        async with aiohttp.ClientSession() as session:
            async with session.get(character_link) as response:
                if response.status != 200:
                    await message.reply("Invalid link! Please check the link and try again.")
                    return
                image_data = await response.read()
                image = Image.open(BytesIO(image_data))
                image_data = BytesIO()
                image.save(image_data, format="JPEG")
                image_data = image_data.getvalue()
                photo = await app.send_photo(chat_id=LOGGER_ID, photo=image_data)
                photo_id = photo.photo[-1].file_id
                collection.insert_one({"charectors": photo_id, "character_name": character_name})
                await message.reply("Character uploaded successfully!")
    except Exception as e:
        await message.reply("Error occurred! Please try again.")

# Nguess handler
@app.on_message(filters.command("nguess"))
async def nguess(client, message):
    if update.message.chat_id != CHAT_ID:
        return
    try:
        characters = await collection.find().to_list(100000)
        random_character = random.choice(characters)
        nobi_charector = random_character["charectors"]
        character_name = random_character["character_name"]
        await app.send_photo(chat_id=CHAT_ID, photo=nobi_charector, caption="Guess the character!")
        start_time = asyncio.get_event_loop().time()
        while True:
            if asyncio.get_event_loop().time() - start_time >= 20:
                await message.reply(f"Time's up! The character was {character_name}")
                break
            await asyncio.sleep(1)
    except Exception as e:
        await message.reply("Error occurred! Please try again.")

# Nguess handler
@app.on_message(filters.command("nguess"))
async def nguess(client, message):
    if update.message.chat_id != CHAT_ID:
        return
    try:
        characters = await collection.find().to_list(100000)
        random_character = random.choice(characters)
        nobi_charector = random_character["charectors"]
        character_name = random_character["character_name"]
        await app.send_photo(chat_id=CHAT_ID, photo=nobi_charector, caption="Guess the character!")
        start_time = asyncio.get_event_loop().time()
        while True:
            if asyncio.get_event_loop().time() - start_time >= 20:
                await message.reply(f"Time's up! The character was {character_name}")
                break
            await asyncio.sleep(1)
    except Exception as e:
        await message.reply("Error occurred!")

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


# Start handler
@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("Welcome to the seize game!")

# Help handler
@app.on_message(filters.command("help"))
async def help(client, message):
    await message.reply("You can use the following commands:\n/start - Start the game\n/help - Show this message\n/upload - Upload a character\n/nguess - Play the guessing game\n/name - Check if a character name is correct")


if __name__ == '__main__':
    main()
    
    
    
app.run()