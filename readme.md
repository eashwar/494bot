# 494Bot

A simple office hours Discord bot, made for the University of Michigan's EECS 494.

## Bot Documentation
Here's a list of commands: that the bot supports:
- `join` will let you join the office hours queue.
- `status` will let you check your position in the queue.
- `list` will list all the students in the queue.
- `pop` can only be used by anybody with the admininstrative role named in the `494_DISCORD_ADMIN_ROLE` environment variable. It will remove the next student from the queue, and if they're in the voice channel named `494_DISCORD_VOICE_WAIT_CHANNEL`, they'll be moved into the `494_DISCORD_VOICE_OH_CHANNEL` channel (both of these variables being environment variables the bot is running with.)
- `clear` can only be used by anybody with the admininstrative role named in the `494_DISCORD_ADMIN_ROLE` environment variable. It clears the office hours queue completely.

## Setup

### Dependencies

This bot requires `python3`, with `pip`. It requires the installation of `discord.py` (and `python-dotenv` if you're doing development):

```
pip3 install -U discord.py python-dotenv
```

### Making the Discord Bot and adding it to the server

- Go to [the Discord developer portal](https://discord.com/developers/applications).
- Select 'New Application' in the top right corner.
- Name it whatever you'd like, e.g. "494BotF20".
- In the application, on the left column, select "Bot".
- Click "Add Bot" to add a bot.
- To get the bot's token for the environment variable (see below), select "Copy" under the Token section to add it to your clipboard.

To add the bot to your Discord server:
- Navigate to "OAuth" in the left column.
- Scroll down to the "OAuth2 URL Generator". Select the "bot" check box, and then in the second box that appears, choose "View Channels" from General Permissions; "Send Messages", "Manage Messages", "Read Message History", "Mention Everyone", and "Add Reactions" from Text Permissions; and "Move Members" from Voice Permissions.
- Copy the URL that's generated, and paste it into your browser. **Save this URL somewhere safe for future use!**
- Add the bot to the server you want to be in.

### On a new semester

- If you have access to the URL from the previous semester, you can use the same URL to add the bot to the next semester's server.
- However, the bot in it current state is built to assume it is only in one server. **If you do not want to write more code, ensure the bot is only in one server at a time by kicking it out of the old server, or create a new bot for the new server and use that bot's URL and token.**

### Environment Variables

There are four environment variables that must be set before running this bot:

- `494_DISCORD_BOT_TOKEN` should be the ID token provided to you in the Discord developer portal, as instructed above.
- `494_DISCORD_VOICE_WAIT_CHANNEL` should be the name of the voice channel in which students can wait to be helped.
- `494_DISCORD_VOICE_OH_CHANNEl` should be the private voice channel that students will individually receive help in for office hours.
- `494_DISCORD_ADMIN_ROLE` should be the name of the administrative role that's given to course instructors; the bot checks that someone invoking the `pop` or `clear` command has this role.

If you're doing development, you can set these environment values in a `.env` file created in the same folder as `bot.py`:

```
494_DISCORD_BOT_TOKEN={YOUR_SECURE_DISCORD_BOT_TOKEN}
494_DISCORD_VOICE_WAIT_CHANNEL=office_hours_waiting
494_DISCORD_VOICE_OH_CHANNEL=office_hours_private
494_DISCORD_ADMIN_ROLE=admin
```

If you're running this for production, on a server or wherever, you should set these same environment variables directly for security.
