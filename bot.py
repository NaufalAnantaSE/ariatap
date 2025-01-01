import requests
import concurrent.futures
import time

def send_tap_request(user_id, authorization_token):
    """
    Mengirimkan satu permintaan POST ke endpoint tap_reward.
    """
    tap_url = f"https://ariagames.io/aria_kombat_api_update/tap_reward?user_id={user_id}"
    headers = {
        "Authorization": f"Basic {authorization_token}",
        "Content-Type": "application/json",
        "Accept-Language": "en-US,en;q=0.9",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.86 Safari/537.36",
        "Referer": "https://ariagames.io/aria_kombat/aria_kombat",
    }

    try:
        response = requests.put(tap_url, headers=headers)
        if response.status_code == 200:
            return True  # Tap berhasil
        else:
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def fetch_user_details(user_id, authorization_token):
    """
    Mengambil data detail pengguna dan menampilkan informasi sederhana.
    """
    url = f"https://ariagames.io/aria_kombat_api/fetch_user_details?user_id={user_id}"
    headers = {
        "Authorization": f"Basic {authorization_token}",
        "Content-Type": "application/json",
        "Accept-Language": "en-US,en;q=0.9",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.86 Safari/537.36",
        "Referer": "https://ariagames.io/aria_kombat/aria_kombat",
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            user_data = response.json().get("api_output", {}).get("user_details", {})
            username = user_data.get("Username", "Unknown")
            coins_earned_tapping = user_data.get("Coins Earned from Tapping", 0.0)
            return username, coins_earned_tapping
        else:
            print(f"Failed to fetch user details. Status code: {response.status_code}, Response: {response.text}")
            return None, None
    except Exception as e:
        print(f"Error fetching user details: {e}")
        return None, None

def unlimited_tap_requests(user_id, authorization_token, max_workers=20):
    """
    Mengirimkan permintaan POST tap_reward tanpa batas secara paralel
    dan menampilkan pesan sederhana setiap kali tap berhasil.
    """
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        while True:
            futures = [
                executor.submit(send_tap_request, user_id, authorization_token)
                for _ in range(max_workers)
            ]

            # Tunggu hasil untuk setiap batch
            for future in concurrent.futures.as_completed(futures):
                if future.result():  # Jika tap berhasil
                    username, coins_earned_tapping = fetch_user_details(user_id, authorization_token)
                    if username and coins_earned_tapping is not None:
                        print(f"Tap berhasil {username} - Coins Earned (Tap): {coins_earned_tapping}")
                else:
                    print("Tap gagal.")

            # Jeda antar batch
            time.sleep(0.5)

if __name__ == "__main__":
    # Masukkan informasi yang diperlukan di sini
    USER_ID = "6580806500"  # ID pengguna
    AUTHORIZATION_TOKEN = "dGVzdF9hZG1pbjpqdHRJWHJoUU1DdWpvcUR1Q3Vo"  # Token Basic Auth

    # Jumlah maksimum thread untuk tap requests
    MAX_WORKERS = 10

    # Menjalankan fungsi
    unlimited_tap_requests(USER_ID, AUTHORIZATION_TOKEN, MAX_WORKERS)
