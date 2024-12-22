import logging
from pyrogram import Client, filters
from pyrogram.types import Message
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import aiohttp
from PIL import Image
from io import BytesIO
import random
from config import BOT_TOKEN, CHAT_ID, UPLOAD_CHAT_ID, LOGGER_ID, SUDOERS, MONGO_DB_URI, MONGO_DB_UPDATE_URI

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Client setup
app = Client("seize", bot_token=BOT_TOKEN)
)


# MongoDB connection
client_1 = AsyncIOMotorClient(MONGO_DB_URI)
db_1 = client_1['seize_collection']
collection = db_1["characters"]

client_2 = AsyncIOMotorClient(MONGO_DB_UPDATE_URI)
db_2 = Client_2['Charector_catcher']

user_collection = db_2["user_collection_lmaoooo"]
# Upload handler
@app.on_message(filters.command("upload") & filters.user(SUDOERS))
async def upload(client, message: Message):
    if message.chat.id != UPLOAD_CHAT_ID:
        await message.reply("You are not allowed to use this command.")
        return
    try:
        parts = message.text.split(" ", 2)
        if len(parts) != 3:
            await message.reply("Invalid format. Use /upload <character link> <character name>")
            return
        character_link, character_name = parts[1], parts[2]
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
                await collection.insert_one({"character_id": photo_id, "character_name": character_name})
                await message.reply("Character uploaded successfully!")
    except Exception as e:
        await message.reply(f"Error occurred! Please try again. {e}")

# Guess handler
@app.on_message(filters.command("nguess") & filters.chat(CHAT_ID))
async def nguess(client, message: Message):
    try:
        characters = await collection.find().to_list(100000)
        if not characters:
            await message.reply("No characters found in the database.")
            return
        random_character = random.choice(characters)
        character_id = random_character["character_id"]
        character_name = random_character["character_name"]
        await app.send_photo(chat_id=CHAT_ID, photo=character_id, caption="Guess the character!")
        start_time = asyncio.get_event_loop().time()

        while True:
            if asyncio.get_event_loop().time() - start_time >= 20:
                await message.reply(f"Time's up! The character was {character_name}")
                break
            await asyncio.sleep(1)
    except Exception as e:
        await message.reply(f"Error occurred! Please try again. {e}")

# Name check handler
@app.on_message(filters.text & filters.chat(CHAT_ID))
async def name_check(client, message: Message):
    try:
        character_name = message.text.lower()
        characters = await collection.find().to_list(100000)
        for character in characters:
            if character["character_name"].lower() == character_name:
                user_id = message.from_user.id
                user_data = await user_collection.find_one({'id': user_id})
                if not user_data:
                    user_data = {'id': user_id, 'Balance': 50, "streak": 1}
                    await user_collection.insert_one(user_data)
                else:
                    user_data['Balance'] += 50
                    user_data["streak"] += 1
                    if user_data["streak"] == 30:
                        user_data['Balance'] += 3000
                        await message.reply("🎉 30-streak! Earned 3000 bitcoins! 🎉")
                    elif user_data["streak"] == 50:
                        user_data['Balance'] += 4000
                        await message.reply("🎉 50-streak! Earned 4000 bitcoins! 🎉")
                    elif user_data["streak"] == 100:
                        user_data['Balance'] += 5000
                        await message.reply("🎉 100-streak! Earned 5000 bitcoins! 🎉")
                    await user_collection.update_one({'id': user_id}, {"$set": user_data})
                await message.reply(f"🎉 Correct! You've earned 50 bitcoins! Your current streak is {user_data['streak']}! 🎉")
                return
        await message.reply("Incorrect! Try again.")
    except Exception as e:
        await message.reply(f"Error occurred! {e}")

# Start handler
@app.on_message(filters.command("start"))
async def start(client, message: Message):
    await message.reply("Welcome to the seize game!")

# Help handler
@app.on_message(filters.command("help"))
async def help(client, message: Message):
    await message.reply(
        "You can use the following commands:\n"
        "/start - Start the game\n"
        "/help - Show this message\n"
        "/upload - Upload a character (Admin only)\n"
        "/nguess - Play the guessing game\n"
        "/name - Check if a character name is correct"
    )

if __name__ == '__main__':
    app.run()
