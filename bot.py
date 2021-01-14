import os
import discord
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv('494_DISCORD_BOT_TOKEN')
VOICE_WAITING_ROOM = os.getenv('494_DISCORD_VOICE_WAIT_CHANNEL')
VOICE_HELP_ROOM = os.getenv('494_DISCORD_VOICE_OH_CHANNEL')
ADMIN_ROLE_NAME = os.getenv('494_DISCORD_ADMIN_ROLE')
_client = discord.Client()
_server = None
_voice_help_room = None
_queue = []

async def get_list():
    if len(_queue) == 0:
        return 'No students in the queue!'
    student_names = []
    for student in _queue:
        student_names.append(student.display_name)
    return 'The students in the queue, in order, are: ' + ', '.join(student_names)

@_client.event
async def on_ready():
    global _server
    global _voice_help_room
    _server = _client.guilds[0]
    _voice_help_room = discord.utils.get(_server.voice_channels, name=VOICE_HELP_ROOM)
    print(f'{_client.user} connected to {_server.name}')

@_client.event
async def on_message(message, pass_context=True):
    if _client.user in message.mentions:
        contents = message.content.lower().split()
        if len(contents) != 2:
            await message.channel.send(f'<@{message.author.id}> error: unable to parse command. please use `help` for a list of valid commands.')
        if contents[1] == 'help':
            await message.channel.send('Here\'s a list of commands:\n'
                                      + '- `join` will let you join the office hours queue.\n' 
                                      + '- `status` will let you check your position in the queue.\n'
                                      + '- `list` will list all the students in the queue.\n'
                                      + f'- `pop` can only be used by instructors. it will remove the next student from the queue, and if they\'re in the {VOICE_WAITING_ROOM} channel, they\'ll be moved into the {VOICE_HELP_ROOM} channel.\n'
                                      + '- `clear` can only be used by instructors. it clears the queue completely.')
        if contents[1] == 'ping':
            await message.channel.send('pong!')
        if contents[1] == 'join':
            if message.author in _queue:
                await message.channel.send(f'<@{message.author.id}> you\'re already in line, position {_queue.index(message.author) + 1}. If you stay in the {VOICE_WAITING_ROOM} voice call, you will be moved into the {VOICE_HELP_ROOM} channel when it is your turn!')
            else:
                _queue.append(message.author)
                await message.channel.send(f'<@{message.author.id}> you\'ve been added to the queue, position {_queue.index(message.author) + 1}! If you stay in the {VOICE_WAITING_ROOM} voice call, you will be moved into the {VOICE_HELP_ROOM} channel when it is your turn!')
        if contents[1] == 'status':
            if message.author in _queue:
                await message.channel.send(f'<@{message.author.id}>, you\'re  position {_queue.index(message.author) + 1} in the queue!')
            else:
                await message.channel.send(f'<@{message.author.id}>, you\'re not in the queue. use `join` to join the queue.')
        if contents[1] == 'list':
            response = await get_list()
            await message.channel.send(response)
        if contents[1] == 'pop':
            if any(role.name == ADMIN_ROLE_NAME for role in message.author.roles):
                next_student = _queue.pop(0)
                if next_student.voice != None and next_student.voice.channel.name == VOICE_WAITING_ROOM:
                    await message.channel.send(f'<@{next_student.id}>, it\'s your turn! Moving you to private voice channel.')
                    await next_student.move_to(_voice_help_room)
                else:
                    await message.channel.send(f'<@{next_student.id}>, it\'s your turn! Please join the {VOICE_WAITING_ROOM} voice call so that the instructor can pull you into the private call.')
            else:
                await message.channel.send(f'<@{message.author.id}> error: you do not have permission to use this command.')
        if contents[1] == 'clear':
            if any(role.name == ADMIN_ROLE_NAME for role in message.author.roles):
                _queue.clear()
                await message.channel.send('The office hours queue has been completely cleared.')
            else:
                await message.channel.send(f'<@{message.author.id}> error: you do not have permission to use this command.')
        else:
            await message.channel.send(f'<@{message.author.id}> error: unable to parse command. please use `help` for a list of valid commands.')
_client.run(BOT_TOKEN)