#!/usr/bin/env python3
"""
Daniel Telegram Bot
Bridges Telegram messages to Claude Code CLI with MS 365 MCP access.
Only responds to authorized user (Jindrich Trapl).
"""

import asyncio
import subprocess
import logging
import os

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Config
TELEGRAM_TOKEN = os.environ.get("DANIEL_TG_TOKEN", "8265623615:AAG8qse8yOqTEd0INpcinrXJe93VBh_75Ws")
ALLOWED_USER_ID = 1606073180  # Jindrich Trapl
WORKING_DIR = os.path.expanduser("~/Daniel")

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
log = logging.getLogger("daniel-bot")


def is_authorized(update: Update) -> bool:
    return update.effective_user and update.effective_user.id == ALLOWED_USER_ID


async def run_claude(prompt: str) -> str:
    """Run Claude Code CLI with a prompt and return the response."""
    try:
        proc = await asyncio.create_subprocess_exec(
            "claude", "-p", prompt,
            "--output-format", "text",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=WORKING_DIR,
        )
        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=120)
        result = stdout.decode().strip()
        if not result and stderr:
            result = f"Chyba: {stderr.decode().strip()}"
        return result or "Žádná odpověď."
    except asyncio.TimeoutError:
        return "Timeout — Claude neodpověděl do 2 minut."
    except FileNotFoundError:
        return "Claude Code CLI není nainstalovaný nebo není v PATH."
    except Exception as e:
        return f"Chyba: {e}"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        await update.message.reply_text("Nemáš přístup.")
        return
    await update.message.reply_text(
        "Ahoj Jindřichu! Jsem Daniel.\n\n"
        "Napiš mi cokoliv a já to zpracuju přes Claude Code "
        "s přístupem k tvému Outlooku, Teams a kalendáři.\n\n"
        "Příklady:\n"
        "• Co mám dnes v kalendáři?\n"
        "• Pošli Haně mail o schůzce\n"
        "• Jaké mám nepřečtené maily?\n"
        "• Napiš na Teams do Sales Strategy..."
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        await update.message.reply_text("Nemáš přístup.")
        return

    user_msg = update.message.text
    log.info(f"Message from Jindrich: {user_msg}")

    # Send typing indicator
    await update.message.chat.send_action("typing")

    # Run through Claude Code
    response = await run_claude(user_msg)

    # Telegram has 4096 char limit per message
    if len(response) > 4000:
        chunks = [response[i:i+4000] for i in range(0, len(response), 4000)]
        for chunk in chunks:
            await update.message.reply_text(chunk)
    else:
        await update.message.reply_text(response)

    log.info(f"Response sent ({len(response)} chars)")


def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    log.info("Daniel Telegram bot started")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
