import logging
import os
import time
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from blessID_gen import embed_message, extract_message  # Import functions from blessID_gen
from putrID_gen import PlanetGenerator  # Import the planet generator

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Greeting message
GREETING_MESSAGE = (
    "GREETINGS\n\n"
    "YOU CAN SEND ME SACRED MESSAGES UP TO 100 SYMBOLS\n\n"
    "OR WRETCHED PLANETS TO DEVOUR\n\n"
    "COOLDOWN IS 60 SECONDS"
)

# Initialize user activity tracking
user_activity = {}

# Base path for storing files
BASE_PATH = 'user_planets'
if not os.path.exists(BASE_PATH):
    os.makedirs(BASE_PATH)

# Cooldown period in seconds
COOLDOWN_PERIOD = 60

# Command handler for the /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(chat_id=update.effective_chat.id, text=GREETING_MESSAGE)

# Check if user is on cooldown
def is_on_cooldown(user_id):
    last_activity = user_activity.get(user_id, 0)
    return time.time() - last_activity < COOLDOWN_PERIOD

# Message handler for text messages (encryption)
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    message = update.message

    # Check cooldown
    if is_on_cooldown(user_id):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="COOLDOWN BETWEEN SACRED MESSAGES IS 60 SECONDS")
        return

    # Update last activity
    user_activity[user_id] = time.time()

    if len(message.text) > 100:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="NO MORE THAN 100 SYMBOLS")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="PROCESSING YOUR SACRED MESSAGE...")

        # Generate a unique ID for this message
        unique_id = f"{user_id}{int(time.time())}"
        
        # Generate a new planet image
        generator = PlanetGenerator()
        planet_path = os.path.join(BASE_PATH, f"putrID_{unique_id}.png")
        generator.output_image.save(planet_path)

        # Embed the user's message in the generated planet
        encrypted_planet_path = os.path.join(BASE_PATH, f"blessID_{unique_id}.png")
        embed_message(generator.output_image, message.text, unique_id)

        # Send the generated planet with embedded message back to the user
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"YOUR SACRED MESSAGE WAS ENCRYPTED IN PLANET blessID_{unique_id}")
        await context.bot.send_document(chat_id=update.effective_chat.id, document=open(encrypted_planet_path, 'rb'))

# Message handler for photo messages
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#    user_id = update.effective_user.id
#    message = update.message

    await context.bot.send_message(chat_id=update.effective_chat.id, text="ONLY PNG FILES ARE ACCEPTED")

# Message handler for document messages (like PNG files sent as files)
async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    message = update.message

    if message.document.mime_type == "image/png":
        await context.bot.send_message(chat_id=update.effective_chat.id, text="DEVOURING YOUR WRETCHED PLANET...")

        # Get the document file ID
        document_file_id = message.document.file_id
        new_file = await context.bot.get_file(document_file_id)

        # Save the file with a unique filename in the shared folder
        planet_path = os.path.join(BASE_PATH, f"deblessID_{user_id}{int(time.time())}.png")
        await new_file.download_to_drive(planet_path)
        
        # Attempt to extract the message from the image
        try:
            extracted_message = extract_message(planet_path)
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"EXTRACTED MESSAGE:\n\n{extracted_message}")
        except Exception as e:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="FAILED TO EXTRACT MESSAGE. PLANET SEEMS EMPTY.")
            logging.error(f"Failed to extract message: {e}")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="ONLY PNG FILES ARE ACCEPTED")

if __name__ == '__main__':
    application = ApplicationBuilder().token('TOKEN').build()
    
    # Add command handler
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    
    # Add message handlers
    application.add_handler(MessageHandler(filters.TEXT, handle_text))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))  # Use filters.Document.ALL

    # Run the bot
    application.run_polling()