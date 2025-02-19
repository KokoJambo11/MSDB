# LoL Discord Bot 🎮

[![Riot API](https://img.shields.io/badge/Riot_API-v5-red)](https://developer.riotgames.com)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

Discord-бот для отслеживания статуса игроков и статистики матчей в League of Legends.

## 🔌 Используемые API
- **Account API v1** (получение PUUID)
- **Summoner API v5** (данные аккаунта)
- **Spectator API v5** (статус в игре)
- **Match API v5** (статистика матчей)

## 🛠 Установка
```bash
git clone https://github.com/KokoJambo11/MSDB.git
```
```bash
cd MSDB
```
Установите зависимости:
```bash
pip install -r requirements.txt
```
Создайте файл .env на основе примера:
```bash
cp example.env .env
```
Заполните .env реальными данными

## 🚀 Запуск
```bash
python bot.py
```
## 📋 Команды

Команда/Описание
- !add <регион> <имя> <тег>	Добавить игрока в список отслеживания (!add euw hqnnahxx 6969)
- !check	Проверить статус всех игроков
- !list	Показать список игроков
- !remove <номер>	Удалить игрока из списка


## ⚠️ Важно
- Бот полностью соответствует правилам разработчика Riot Games

- Не хранит данные матчей дольше 24 часов

- Соблюдает rate limits (20 запросов/сек)

## 📞 Поддержка
Для вопросов: 1dmitrykiselev2004@gmail.com
