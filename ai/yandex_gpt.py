import os
import logging as log
import requests
from typing import Optional

async def ask_yandex_gpt(
    health_data: str, 
    psychological_data: str, 
    study_data: str
) -> Optional[str]:
    
    api_key = os.getenv("YANDEX_API_KEY")
    folder_id = os.getenv("FOLDER_ID")
    
    if not api_key or not folder_id:
        log.error("❌ Не настроены YANDEX_API_KEY или FOLDER_ID в .env")
        return "Ошибка: не настроен ключ API"

    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    
    prompt = f"""
    Ты - заботливый персональный ассистент по здоровому образу жизни для подростков.
    Проанализируй информацию о пользователе и дай персонализированные рекомендации.
    
    Информация о физическом здоровье и активности:
    {health_data if health_data and health_data != "Пропущено" else "Пользователь не указал информацию"}
    
    Психологическое состояние:
    {psychological_data if psychological_data and psychological_data != "Пропущено" else "Пользователь не указал информацию"}
    
    Информация об учебе:
    {study_data if study_data and study_data != "Пропущено" else "Пользователь не указал информацию"}
    
    Дай комплексные рекомендации, учитывающие все аспекты жизни пользователя.
    Ответ должен быть дружелюбным и практичным.
    """
    
    headers = {
        "Authorization": f"Api-Key {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "modelUri": f"gpt://{folder_id}/yandexgpt-lite",
        "completionOptions": {
            "stream": False,
            "temperature": 0.7,
            "maxTokens": 1000
        },
        "messages": [
            {
                "role": "system",
                "text": "Ты - заботливый персональный ассистент для подростков."
            },
            {
                "role": "user",
                "text": prompt
            }
        ]
    }
    
    try:
        log.info("📤 Отправляю запрос к Yandex GPT...")
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        answer = result['result']['alternatives'][0]['message']['text']
        log.info("✅ Получен ответ от Yandex GPT")
        return answer
        
    except Exception as e:
        log.error(f"❌ Ошибка: {e}")
        return None