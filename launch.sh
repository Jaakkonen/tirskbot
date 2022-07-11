#!/bin/bash
cd "$(dirname "$0")"
pkill -F tipahtanutbot.pid
sleep 1
export $(cat .env)
exec python3 -c 'import bot; bot.daemonize()'
