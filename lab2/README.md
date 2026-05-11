# Задание 2 - API-пайплайн: данные → LLM → результат

## Описание

Python-скрипт, который автоматически анализирует тональность и тему отзывов с помощью LLM.

**Задача:** классификация отзывов: определение тональности (positive/negative/neutral) и ключевой темы (price, quality, delivery и т.д.).

### Пайплайн

```  
result.json
^
| Сохранение
|
Структурированный JSON (sentiment, topic для каждого отзыва)
^
| GitHub Models API (GPT-4o-mini)
|
CSV-файл (отзывы)
```


## Датасет

Используется собственный CSV-файл `reviews.csv` с колонками:
- `comment_id` — идентификатор
- `review_text` — текст отзыва на русском языке

Пример на 10 отзывов (можно расширять до любого количества).

## Инструкция запуска

### 1. Установка зависимостей

```bash
pip install -r requirements.txt

### 2. Настройка API-ключа

Получите бесплатный API-ключ через GitHub Models:

1. Перейдите в настройки GitHub → Developer settings → Personal access tokens → Fine-grained tokens.

2. Создайте токен с разрешением Read-only для Models.

3. Скопируйте токен.

```bash
cp .env.example .env
# Отредактируйте .env и вставьте ваш GITHUB_TOKEN
```

### 3. Запуск

```bash
python script.py
```

### 4. Результат
Файл `result.json` в текущей директории — структурированный JSON от LLM.

## Пример входных данных

Файл `data/comments.csv`:

| comment_id | comment_text                                              |
|------------|-----------------------------------------------------------|
|     1      | Отличный смартфон! Быстрая доставка, батарея держит долго.|
|     2      | Курьер опоздал на 3 часа, товар пришёл в помятой коробке. |
|     3      | Нормальный товар за свои деньги. Ничего особенного.       |

## Пример выходных данных

```json
 {
    "id": 1,
    "review": "Отличный смартфон! Быстрая доставка, батарея держит долго.",
    "llm_answer": {
      "sentiment": "positive",
      "topic": "battery"
    }
  },
  {
    "id": 2,
    "review": "Курьер опоздал на 3 часа, товар пришёл в помятой коробке.",
    "llm_answer": {
      "sentiment": "negative",
      "topic": "delivery"
    }
  },
  {
    "id": 3,
    "review": "Нормальный товар за свои деньги. Ничего особенного.",
    "llm_answer": {
      "sentiment": "neutral",
      "topic": "value for money"
    }
  }
```

## Технологии
- Python 3.10+
- GitHub Models API (GPT-4o-mini)
- Requests, Python-dotenv
