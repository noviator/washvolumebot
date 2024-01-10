import os
import logging
from dotenv import load_dotenv
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from utils.redis_db import get_redis_client

load_dotenv()

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")


def check_user_connected(user_id: int) -> bool:
    redis_client = get_redis_client()
    all_users = redis_client.lrange("UserIDs", 0, -1)
    if str(user_id) in all_users:
        return True
    return False

async def connect(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        
        args = context.args
        if len(args) != 1:
            await update.message.reply_text("Invalid number of arguments")
            return
        private_key = args[0]
        
        # validate private key
        # if len(private_key) != 64:
        #     await update.message.reply_text("Invalid private key")
        #     return
        
        user = update.effective_user
        user_id = user.id

        # check if user already connected
        if check_user_connected(user_id):
            await update.message.reply_text("User already connected, use /disconnect to disconnect the wallet")
            return
        
        
        redis_client = get_redis_client()
        key = f"PrivateKeysOfUsers:{user_id}"
        redis_client.hset(key, 'private_key', private_key)
        redis_client.lpush("UserIDs", user_id)
        await update.message.reply_text("User connected")

    except Exception as e:
        logger.error(e)
        await update.message.reply_text("Error")

async def disconnect(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        user = update.effective_user
        user_id = user.id

        if not check_user_connected(user_id):
            await update.message.reply_text("User not connected")
            return
        
        redis_client = get_redis_client()
        redis_client.lrem("UserIDs", 0, user_id)
        redis_client.delete(user_id)
        await update.message.reply_text("User disconnected")

        # remove user orders
    
    except Exception as e:
        logger.error(e)
        await update.message.reply_text("Error")

async def place(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        args = context.args
        if len(args) != 2:
            await update.message.reply_text("Invalid number of arguments")
            return
        
        user = update.effective_user
        user_id = user.id

        # check if user connected
        if not check_user_connected(user_id):
            await update.message.reply_text("User not connected")
            return
        
        # validate token_address
        token_address = args[0]
        pair_address = "pairrrrr"
        # complete later
        
        eth_amount = args[1]
        if not eth_amount.isdigit():
            await update.message.reply_text("Invalid amount")
            return
        
        # place order
        # change later -> order gets over written
        redis_client = get_redis_client()
        user_order_key = f"OrdersOfUser:{user_id}1"
        redis_client.hset(user_order_key, 'token_address', token_address)
        redis_client.hset(user_order_key, 'pair_address', pair_address)
        redis_client.hset(user_order_key, 'eth_amount', eth_amount)
        await update.message.reply_text("Order placed")

    except Exception as e:
        logger.error(e)
        await update.message.reply_text("Error")

def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("connect", connect))
    application.add_handler(CommandHandler("disconnect", disconnect))
    application.add_handler(CommandHandler("place", place))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()