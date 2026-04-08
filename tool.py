import os, requests, json, time, sys, random
from rich.console import Console
from rich.prompt import Prompt, IntPrompt
from pystyle import Colors, Colorate

# ==========================================
# 1. API ТОХИРГОО (КОД ДОТОР ХАДГАЛАХ ХЭСЭГ)
# ==========================================
API_BASE_URL = "https://kayzennv3.squareweb.app/api"
API_KEY = "APIKEY38"
FIREBASE_URL = "https://telmunn-79711-default-rtdb.firebaseio.com/users.json"
ADMIN_KEY = "0615"

# ==========================================
# 2. CPM API CLIENT (КОД ДОТОР БАГТСАН)
# ==========================================
class CPMApiClient:
    def __init__(self, access_key):
        self.access_key = access_key
        self.auth_token = None

    def login(self, email, password):
        payload = {"account_email": email, "account_password": password}
        params = {"api_key": API_KEY}
        try:
            res = requests.post(f"{API_BASE_URL}/account_login", params=params, json=payload).json()
            if res.get('ok') or res.get('error') == 0:
                self.auth_token = res['data'].get('auth')
                return 0 # Амжилттай
            return res.get('error', 1)
        except: return 1

    def get_player_data(self):
        params = {"auth": self.auth_token, "api_key": API_KEY}
        try:
            return requests.get(f"{API_BASE_URL}/get_player_data", params=params).json()
        except: return {"ok": False}

    def set_player_rank(self):
        payload = {"auth": self.auth_token}
        params = {"api_key": API_KEY}
        try:
            res = requests.post(f"{API_BASE_URL}/set_player_rank", params=params, json=payload).json()
            return res.get('ok')
        except: return False

    def set_player_name(self, new_name):
        payload = {"auth": self.auth_token, "name": new_name}
        params = {"api_key": API_KEY}
        try:
            res = requests.post(f"{API_BASE_URL}/set_player_name", params=params, json=payload).json()
            return res.get('ok')
        except: return False
    
    # Бусад API функцүүдээ (Email, Pass change) энд нэмж болно...

# ==========================================
# 3. ТУСЛАХ ФУНКЦҮҮД (FIREBASE & UI)
# ==========================================
console = Console()

def load_db():
    try:
        response = requests.get(FIREBASE_URL)
        return response.json() if response.json() else {}
    except: return {}

def update_balance(user_id, new_balance):
    url = f"https://telmunn-79711-default-rtdb.firebaseio.com/users/{user_id}.json"
    requests.patch(url, json={"balance": new_balance})

def banner():
    os.system('clear')
    brand = "Car Parking Multiplayer 1 Tool"
    print(Colorate.Horizontal(Colors.rainbow, brand.center(60)))
    print(Colorate.Horizontal(Colors.rainbow, '='*60))
    print(Colorate.Horizontal(Colors.rainbow, '       𝐏𝐋𝐄𝐀𝐒𝐄 𝐋𝐎𝐆𝐎𝐔𝐓 𝐅𝐑𝐎𝐌 𝐂𝐏𝐌 𝐁𝐄𝐅𝐎𝐑𝐄 𝐔𝐒𝐈𝐍𝐆 𝐓𝐇𝐈𝐒 𝐓𝐎𝐎𝐋'))
    print(Colorate.Horizontal(Colors.rainbow, '    𝐒𝐇𝐀𝐑𝐈𝐍𝐆 𝐓𝐇𝐄 𝐀𝐂𝐂𝐄𝐒𝐒 𝐊𝐄𝐘 𝐈𝐒 𝐍𝐎𝐓 𝐀𝐋𝐋𝐎𝐖𝐄𝐃 𝐀𝐍𝐃 𝐖𝐈𝐋𝐋 𝐁𝐄 𝐁𝐋𝐎𝐂𝐊𝐄𝐃'))
    print(Colorate.Horizontal(Colors.rainbow, '           𝐓𝐞𝐥𝐞𝐠𝐫𝐚𝐦: @TarganJackChannel 𝐎𝐫 @TarganJackChat'))
    print(Colorate.Horizontal(Colors.rainbow, '='*60))

# ==========================================
# 4. ҮНДСЭН ПРОГРАМ
# ==========================================
def main():
    while True:
        banner()
        email = Prompt.ask("[?] Account Email")
        password = Prompt.ask("[?] Account Password", password=True)
        access_key = Prompt.ask("[?] Access Key")

        db = load_db()
        user_id_ref = None
        found_data = None
        is_unlimited = (access_key == ADMIN_KEY)

        if not is_unlimited:
            for uid, data in db.items():
                if data.get('key') == access_key:
                    user_id_ref = uid
                    found_data = data
                    break

        # CPMApiClient-ийг дуудах
        cpm = CPMApiClient(access_key)
        login_response = cpm.login(email, password)

        if login_response != 0 or (not is_unlimited and not found_data):
            banner()
            print(f"[?] Account Email: {email}\n[?] Account Password: {password}\n[?] Access Key: {access_key}\n")
            print(Colorate.Horizontal(Colors.red_to_white, "[✘] Trying to Login: TRY AGAIN."))
            time.sleep(3); continue
        
        print(Colorate.Horizontal(Colors.green_to_white, "[√] Trying to Login: SUCCESSFUL."))
        time.sleep(2)

        while True:
            banner()
            current_bal = 999999999 if is_unlimited else found_data.get('balance', 0)
            print(f"Account Email    : {email}")
            print(f"Account Password : {password}")
            bal_display = "Unlimited" if is_unlimited else f"{current_bal:,} ₮"
            print(Colorate.Horizontal(Colors.green_to_white, f"Balance          : {bal_display}"))
            print("-" * 40)
            
            print("1. SET RANK (20.5K) | 2. LOGOUT | 3. EXIT")
            choice = Prompt.ask("Select")

            if choice == "2": break
            if choice == "3": sys.exit()

            if choice == "1":
                cost = 20500
                if current_bal >= cost:
                    if cpm.set_player_rank():
                        if not is_unlimited:
                            new_bal = current_bal - cost
                            update_balance(user_id_ref, new_bal)
                            found_data['balance'] = new_bal
                        print("SUCCESSFUL!"); time.sleep(2)
                else:
                    print("INSUFFICIENT BALANCE!"); time.sleep(2)

if __name__ == "__main__":
    main()

