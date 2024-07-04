import telebot
import os
import requests  # For Telegram API requests
import google.generativeai as genai
import tempfile


# Replace with your actual API keys and bot token
GOOGLE_API_KEY = 'API'
BOT_TOKEN = "Token"

# Configure Google Generative AI
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("model")

# Initialize the Telegram bot
bot = telebot.TeleBot(BOT_TOKEN)

# Initial keyboard with one button
initial_reply_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
initial_reply_markup.add(telebot.types.KeyboardButton(text="Aforative Media's Services"))

# Follow-up keyboard with three buttons
followup_reply_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
followup_reply_markup.add(telebot.types.KeyboardButton(text="Photography"))
followup_reply_markup.add(telebot.types.KeyboardButton(text="Videography"))
followup_reply_markup.add(telebot.types.KeyboardButton(text="Special offer"))

@bot.message_handler(commands=['start'])  # Use /start command to trigger the message
def send_welcome_message(message):
    chat_id = message.chat.id
    text = ("Aforative Media's Generative AI សូមស្វាគមន៍\n"
            "Improve your business email writing, digital marketing concepts, and more\n"
            "with Aforative Media's Generative AI. Simply state your goal, copy and paste the text you want to enhance, or ask a specific question. Get started now!")
    bot.send_message(chat_id, text, reply_markup=initial_reply_markup)  # Send message with keyboard

@bot.message_handler(func=lambda message: message.text == "Aforative Media's Services")
def ask_donation_method(message):
    chat_id = message.chat.id
    text = ("Thank you for interesting our services")
    bot.send_message(chat_id, text, reply_markup=followup_reply_markup)

@bot.message_handler(func=lambda message: message.text in ["Photography", "Special offer", "Videography"])
def send_bank_photo(message):
    chat_id = message.chat.id
    text = message.text

    if text == "Photography":
        bot.send_message(chat_id, "We offer a variety of photography services as following\n"
                                  "1- Grab your personalize photography service experience 👉 https://aforativemedia.com/hire-siem-reap-local-photographer/\n\n"
                                  "2- Corporate Event & Meeting Photography 👉 https://aforativemedia.com/siem-reap/event-meeting-siemreap-photographer/\n\n"
                                  "3- Instant Printing & Sharing Photo Booth 👉 https://aforativemedia.com/instant-photo-printing-event-mr-ms-booth/")

    elif text == "Videography":
        bot.send_message(chat_id, "We bring your vision to life with a full range of videography services, including TVCs, documentaries, social media reels, short-form content, and more.👉 https://aforativemedia.com/siem-reap-cambodia-video-journalist-travel-filmmaker/")

    elif text == "Special offer":
        print(message.text)
        bot.send_message(chat_id, "1- Celebrate your Love with a Traditional Khmer Wedding: Half-Day Package 👉 https://aforativemedia.com/siem-reap-khmer-wedding-arrangement/\n\n"
                                  "2- Uncover Angkor's Secrets & Be Blessed by a Monk 👉 https://aforativemedia.com/siemreap-monk-blessing-arrangement/\n\n"
                                  "3- See Siem Reap Shine: Photography Tour of Nightlife Hotspots 👉 https://aforativemedia.com/experience-siem-reap-night-life-photography-low-light/")
    else:
        bot.send_message(chat_id, "Invalid option")

@bot.message_handler(content_types=['text'])
def handle_text_messages(message):
    """Handles text messages and responds based on predefined questions or Generative AI."""
    try:
        chat_session = model.start_chat()  # Start a new chat session for context
        prompt = f"Respond to the user: {message.text}"
        response = chat_session.send_message(prompt)  # Generate response using text and prompt
        response_text = response.text
        bot.reply_to(message, response_text) if message.chat.type == 'private' else bot.send_message(message.chat.id, response_text)
    except Exception as e:
        print(f"Error during GenAI processing: {e}")
        error_message = "Sorry, I can't answer this query right now but I will improve from time to time."
        bot.reply_to(message, error_message) if message.chat.type == 'private' else bot.send_message(message.chat.id, error_message)

if __name__ == "__main__":
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"Error occurred: {e}")

