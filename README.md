# Telegram Translation Bot

A Python-based Telegram bot that translates English text to **German**, **French**, or **Spanish** using [Helsinki-NLP MarianMT](https://huggingface.co/Helsinki-NLP) models. Containerized with Docker for easy deployment.

---

## Features
- Translate text to German, French, or Spanish.
- Inline keyboard for language selection.

---

## Installation

### Local Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/hamidthri/translator-en-de
   cd translator-en-de
# Install dependencies:
```bash
pip install -r requirements.txt
```
# Set your Telegram bot token:
```bash
export TELEGRAM_BOT_TOKEN=<your-telegram-bot-token>
```
# Docker Setup
# Build the Docker image:
```bash
make build
```
# Run the bot in a container:
```bash
make run TELEGRAM_BOT_TOKEN=<your-telegram-bot-token>

```
