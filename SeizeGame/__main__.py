import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import Update, ForceReply
import importlib
from config import BOT_TOKEN

#logging 
# Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)



#seize modules
seize_game_modules = importlib.import_module("SeizeGame.modules")
nguess_module = getattr(seize_game_modules, 'nguess')



def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    
    
    dp = updater.dispatcher
    
    
    dp.add_handler(CommandHandler("nguess", nguess))
    
    dp.add_handler(CommandHandler("upload", upload))

dp.add_handler(CommandHandler(Filters.text, name))
    
    
    
    updater.start_polling()
    updater.idle()
    
    
if __name__ == '__main__':
    main()
    
    

