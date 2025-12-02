# 🤖 Discord Bot

it is a multifunctional Discord bot built using **discord.py**, providing advanced logging, moderation, automation, and utility features for the M305 community server.  
It includes full event tracking, slash commands, and even a system tray integration for desktop execution.

---

## 📌 Features

### **Slash Commands**
The bot provides a wide range of `/commands` powered by Discord Application Commands:

#### 📝 **Messaging Tools**
- **/send** — Send a message or reply to an existing message using the bot.

#### 🔊 **Voice Channel Controls**
- **/roller** — Rapidly move a member through all voice channels.
- **/toafk** — Move a selected member to the AFK channel.
- **/move** — Move all users from your current VC to another (restricted to a specific user).

#### 🛡️ **Moderation Tools**
- **/warn** — Warn members or apply a timeout if they were already warned.
- **/status** — Display server statistics including humans, bots, and total population.

#### 🧰 **Utility Commands**
- **/avatar** — Display the avatar of a mentioned member.
- **/convert** — Convert USD or ARS to SAR.
- **/welcome_test** — Preview the server’s welcome embed.

---

## 📡 Automated Event Logging

The bot logs nearly every important event in the server, helping staff monitor activity efficiently.

### **Member Events**
- Member joins (with auto-role assignment)
- Member leaves
- Member bans & unbans (with audit log tracking)

### **Message Events**
- Deleted messages (content, author, type)
- Bulk message deletions
- Edited messages (before and after content)

### **Voice Channel Events**
- Voice channel joins, exits, and moves  
- Server mute / unmute  
- Server deaf / undeaf  
- Detailed audit log tracking to show who performed each action  

### **Soundboard Events**
- Sound deletion notifications with audit log attribution

### **Log Channel Protection**
The bot automatically deletes any messages sent manually in the log channel to keep it clean and readable.

---

## 🖥️ System Tray Integration

When executed on a desktop environment, the bot:
- Runs inside a separate Python **thread**
- Displays a **system tray icon** using `pystray`
- Allows stopping the bot through the tray menu
- Loads a custom image as an icon

This makes it easy to keep the bot running quietly in the background.

---

## 🔧 Environment Configuration

The bot reads configuration values from a `.env` file, including:

- Bot token  
- Guild ID  
- Channel IDs  
- Role IDs  
