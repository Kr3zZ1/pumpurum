import requests
import subprocess
import time

# URL для получения случайных прокси
PROXY_API_URL = "http://pubproxy.com/api/proxy"
TEST_URL = "http://httpbin.org/ip"  # URL для проверки прокси

# Функция для получения случайного прокси
def get_random_proxy():
    response = requests.get(PROXY_API_URL)
    if response.status_code == 200:
        data = response.json()
        return data['data'][0]['ipPort'] if data['count'] > 0 else None
    return None

# Функция для проверки работоспособности прокси
def check_proxy(proxy):
    proxy_url = f"http://{proxy}"
    try:
        response = requests.get(TEST_URL, proxies={"http": proxy_url, "https": proxy_url}, timeout=10)
        return response.status_code == 200  # Прокси работает
    except requests.RequestException:
        return False  # Прокси не работает

# Запуск клиента Discord с прокси
def launch_custom_discord(proxy):
    # Путь к клиенту Discord
    discord_client_path = r"C:\Users\MainPC\Documents\SDiscord-win32-x64\SDiscord.exe"
    # Аргументы запуска с прокси
    proxy_argument = f'--proxy-rules="socks5={proxy}"'
    
    try:
        # Запуск клиента Discord
        command = [discord_client_path, proxy_argument, "https://discord.com/app"]
        subprocess.Popen(command)
        print(f"Запущен клиент Discord с прокси: {proxy}")
    except FileNotFoundError:
        print(f"Ошибка: Не удалось найти файл по пути: {discord_client_path}")

def main():
    while True:
        print("Получение случайного прокси...")
        proxy = get_random_proxy()
        
        if proxy:
            print(f"Полученное прокси: {proxy}")
            if check_proxy(proxy):
                print(f"Работающее прокси: {proxy}")
                launch_custom_discord(proxy)  # Запуск клиента Discord
                break
            else:
                print(f"Прокси не работает: {proxy}")
        else:
            print("Не удалось получить случайное прокси, пытаемся снова...")
        
        time.sleep(2)  # Задержка перед следующей попыткой

if __name__ == "__main__":
    main()
