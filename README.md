# Universal OSINT Tool v1.0

**Advanced Information Search System**

Полнофункциональная программа для поиска информации о пользователях по различным идентификаторам.

## Возможности

✅ Поиск по номерам телефонов
✅ Поиск по ФИО
✅ Поиск по номерам автомобилей
✅ Поиск по номерам паспортов
✅ Поиск по email-адресам
✅ Поиск по IP-адресам
✅ Поиск по VIN номерам
✅ Поиск в социальных сетях
✅ Проверка утечек данных
✅ Анализ судебных дел
✅ Поиск в реестрах компаний
✅ Проверка информации об автомобилях
✅ Проверка паспортных данных
✅ Анализ новостных архивов
✅ Проверка IP геолокации

## Установка

```bash
git clone https://github.com/Anonim1346/osint-tool.git
cd osint-tool
pip install -r requirements.txt
```

## Использование

### Консольное приложение

```bash
python main.py
```

### Примеры запросов

**По номеру телефона:**
```
+7 (999) 999-99-99
79999999999
```

**По ФИО:**
```
Иван Иванов
John Doe
```

**По номеру машины:**
```
А123БВ77
ABC1234
```

**По номеру паспорта:**
```
1234567890
```

**По email:**
```
user@example.com
```

**По IP адресу:**
```
192.168.1.1
```

## Архитектура

```
osint-tool/
├── main.py                 # Главный входной файл
├── core/
│   ├── __init__.py
│   ├── osint_engine.py     # Основной поисковый движок
│   ├── data_sources.py     # Интеграции с БД и API
│   ├── ui.py               # Пользовательский интерфейс
│   ├── config.py           # Конфигурация
│   ├── logger.py           # Логирование
│   ├── database.py         # Работа с БД
│   ├── api_handler.py      # Управление API
│   └── cache.py            # Кеширование результатов
├── modules/
│   ├── __init__.py
│   ├── phone_module.py     # Модуль поиска по телефонам
│   ├── name_module.py      # Модуль поиска по ФИО
│   ├── car_module.py       # Модуль поиска по номерам машин
│   ├── passport_module.py  # Модуль поиска по паспортам
│   ├── email_module.py     # Модуль поиска по email
│   ├── ip_module.py        # Модуль поиска по IP
│   ├── socnet_module.py    # Модуль поиска в соцсетях
│   └── breach_module.py    # Модуль проверки утечек
├── integrations/
│   ├── __init__.py
│   ├── viber.py            # Интеграция Viber
│   ├── telegram.py         # Интеграция Telegram
│   ├── vk.py               # Интеграция VK
│   ├── instagram.py        # Интеграция Instagram
│   ├── facebook.py         # Интеграция Facebook
│   ├── twitter.py          # Интеграция Twitter
│   ├── linkedin.py         # Интеграция LinkedIn
│   ├── hlr.py              # HLR Lookup
│   ├── iplookup.py         # IP Lookup
│   ├── dataleak.py         # Проверка утечек
│   └── court.py            # Судебные реестры
├── utils/
│   ├── __init__.py
│   ├── validators.py       # Валидация данных
│   ├── parsers.py          # Парсеры данных
│   ├── formatters.py       # Форматирование результатов
│   └── helpers.py          # Вспомогательные функции
├── data/
│   ├── databases/          # Локальные БД
│   └── cache/              # Кеш результатов
├── logs/                   # Логи программы
├── config.json             # Конфигурация
├── requirements.txt        # Зависимости
└── README.md               # Документация
```

## Структура данных результатов

```json
{
  "query": "input_data",
  "query_type": "phone|name|car|passport|email|ip|vin",
  "results": {
    "phone_info": {
      "phone": "+7999999999",
      "operator": "Megafon",
      "status": "active",
      "region": "Moscow"
    },
    "person_info": {
      "name": "John Doe",
      "age": 35,
      "address": "Moscow",
      "phones": ["79999999999"],
      "emails": ["user@example.com"]
    },
    "social_media": {
      "vkontakte": [{"id": "123456", "name": "John Doe", "verified": false}],
      "telegram": [{"username": "@username", "verified": true}],
      "instagram": [{"username": "username", "followers": 5000}]
    },
    "car_info": {
      "number": "А123БВ77",
      "owner": "John Doe",
      "model": "Toyota Camry",
      "year": 2020,
      "status": "registered"
    },
    "passport_info": {
      "number": "1234567890",
      "holder": "John Doe",
      "birthdate": "1990-01-01",
      "issued": "2015-05-15",
      "expires": "2025-05-15"
    },
    "email_info": {
      "email": "user@example.com",
      "in_breaches": true,
      "breaches": ["LinkedIn", "Facebook"]
    },
    "ip_info": {
      "ip": "192.168.1.1",
      "country": "Russia",
      "city": "Moscow",
      "isp": "Rostelecom",
      "coordinates": {"lat": 55.7558, "lon": 37.6173}
    }
  }
}
```

## Конфигурация

Отредактируйте `config.json`:

```json
{
  "timeout": 10,
  "retries": 3,
  "output_format": "json",
  "log_level": "INFO",
  "database": {
    "enabled": true,
    "path": "data/osint.db"
  },
  "apis": {
    "enable_hlr": true,
    "enable_viber": true,
    "enable_telegram": true,
    "enable_vk": true,
    "enable_instagram": true,
    "enable_facebook": true,
    "enable_twitter": true,
    "enable_ip_lookup": true,
    "enable_court": true
  },
  "api_keys": {
    "hlr_api_key": "your_api_key",
    "ip_lookup_key": "your_api_key",
    "breach_check_key": "your_api_key"
  }
}
```

## Модули и их функции

### Phone Module
- HLR Lookup (оператор, статус, регион)
- Проверка наличия в Viber/WhatsApp
- Поиск в публичных справочниках
- История активности

### Name Module
- Поиск в судебных реестрах
- Поиск в реестрах компаний
- Поиск в новостных архивах
- Анализ конфликтов интересов

### Car Module
- Поиск в реестрах ГИБДД
- Декодирование VIN
- История ДТП
- Информация об владельце

### Passport Module
- Проверка в реестре МВД
- Анализ валидности
- История паспорта
- Данные владельца

### Email Module
- Проверка утечек (HaveIBeenPwned)
- Анализ активности
- Связанные аккаунты
- История использования

### IP Module
- Геолокация
- Проверка угроз
- История использования
- WHOIS информация

### Social Media Module
- VKontakte
- Telegram
- Instagram
- Facebook
- Twitter
- LinkedIn

## Интеграции

- **HLR Lookup API** - получение информации об операторе мобильной сети
- **Viber API** - проверка наличия номера в Viber
- **Telegram Bot API** - поиск в Telegram
- **VK API** - поиск профилей ВКонтакте
- **Instagram API** - поиск профилей
- **Facebook API** - поиск профилей
- **Twitter API** - поиск аккаунтов
- **LinkedIn API** - поиск профилей
- **IP Geolocation API** - геолокация IP адресов
- **HaveIBeenPwned API** - проверка утечек
- **WHOIS API** - информация о доменах

## Примеры использования

### Как Python модуль

```python
from core.osint_engine import OSINTEngine

engine = OSINTEngine()
results = engine.search("+79999999999")
print(results)
```

### Как REST API

```bash
curl -X POST http://localhost:5000/search \
  -H "Content-Type: application/json" \
  -d '{"query": "+79999999999"}'
```

### Как Telegram Bot

```
/start
/search +79999999999
/results
```

## Лицензия

Для использования только в рамках закона вашей страны.

## Дисклеймер

⚠️ Данный инструмент предназначен ТОЛЬКО для легального использования в соответствии с законодательством вашей страны. Автор не несет ответственность за незаконное использование программы.

## Поддержка

Для вопросов и предложений создавайте Issues в репозитории.
