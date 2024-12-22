import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# API credentials
API_ID = int(os.getenv("API_ID", 23855030))  # Default value provided as 
API_HASH = os.getenv("API_HASH", "b153175da5f13f048abbce89b49f80cc")

# Bot token
BOT_TOKEN = os.getenv("BOT_TOKEN", "7114363278:AAHEgyquAA8ij_pURKAWmBh2s51HJhzxvSI")

# Owner and Sudoers
OWNER_ID = int(os.getenv("OWNER_ID", 6806897901))  # Default OWNER_ID
SUDOERS = list(
    map(int, os.getenv("SUDOERS", "5743956401,6368715469,6806897901,6777860063").split(","))
)  # Convert to a list of integers

# Chat-related IDs
CHAT_ID = list(map(int, os.getenv("CHAT_ID", "-1002374835450,-1002453608705").split(",")))
UPLOAD_CHAT_ID = int(os.getenv("UPLOAD_CHAT_ID", -1002453608705))
LOGGER_ID = int(os.getenv("LOGGER_ID", -1002453608705))

# MongoDB URIs
MONGO_DB_URI = os.getenv(
    "MONGO_DB_URI",
    "mongodb+srv://shivaiaxz:YfVBSatihAQlPAXc@cluster0.rqcpm.mongodb.net/?retryWrites=true&w=majority",
)
MONGO_DB_UPDATE_URI = os.getenv(
    "MONGO_DB_UPDATE_URI",
    "mongodb+srv://shivaiaxz:YfVBSatihAQlPAXc@cluster0.rqcpm.mongodb.net/?retryWrites=true&w=majority",
)
