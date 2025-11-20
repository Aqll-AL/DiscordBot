**# 📌 Project Overview**

This repository contains the source code for M305 Discord Bot, a multifunctional moderation, utility, and logging bot built using discord.py, slash commands, and Python threading. The bot provides server automation, moderation tools, logging for nearly all server activities, and several convenience commands for users and admins.

The bot is packaged with a system tray icon (via pystray) so it can run in the background on a desktop environment.

**## 🚀 Features & Functionality**
**🔹 Slash Commands**

The bot uses Discord application commands (/commands) to provide structured, easy-to-use functionality:

Messaging Tools

/send — Sends a message in the current channel, optionally replying to a specific message ID. Logs command usage with an embed.

Voice Channel Controls

/roller — Moves a member rapidly between all voice channels (for fun / trolling). Includes a cooldown timer.

/toafk — Moves a selected member to the AFK channel.

/move — Moves all members from your current voice channel to another channel (restricted to a specific user).

Moderation Tools

/warn — Adds a warn role to a user; if they already have it, they get timed out for 1 hour.

/status — Shows server statistics such as number of humans, bots, and total members.

/avatar — Displays the avatar of any server member.

Utility Tools

/welcome_test — Previews the welcome embed message.

/convert — Converts USD or ARS into SAR using fixed rates.

### **🔹 Automated Event Logging**

The bot extensively logs server activity to a designated logging channel, including:

Member Events

Member joins (with auto-role assignment)

Member leaves

Member bans & unbans (with audit log lookup)

Message Events

Deleted messages (content, author, type, and who deleted it)

Bulk deleted messages

Edited messages (before/after)

Voice Channel Events

Joins, leaves, and moves between voice channels

Server mute/unmute + deaf/undeaf actions

Attempts to move specific protected users

Audit log integration to show who performed each action

Soundboard Events

Deletion of soundboard sounds with audit log reference

Security

Bot automatically deletes any messages sent in the log channel to keep it clean.

**#### 🖥️ System Tray Integration**

When running locally, the bot creates a system tray icon using pystray. This allows:

Running the bot in the background

Clicking the tray icon menu to exit the program

Custom icon loaded from environment variables

This feature runs on a separate thread, ensuring the bot remains responsive.

**##### 🔧 Environment Variables**

The bot is configured via a .env file, which stores:

Bot token

Guild and channel IDs

Roles IDs

Icon path

Other bot settings

This adds a layer of security and avoids hard-coding sensitive values.