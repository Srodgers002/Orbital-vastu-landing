import httpx


async def send_newsletter(email_api_url: str, subscribers: list[str], digest: str) -> None:
    async with httpx.AsyncClient(timeout=15) as client:
        await client.post(email_api_url, json={'subscribers': subscribers, 'digest': digest})


async def send_telegram_alert(bot_token: str, chat_id: str, message: str) -> None:
    async with httpx.AsyncClient(timeout=15) as client:
        await client.post(f'https://api.telegram.org/bot{bot_token}/sendMessage', json={'chat_id': chat_id, 'text': message})
