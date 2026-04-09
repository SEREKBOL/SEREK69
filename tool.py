import os, requests, json, time, sys, random
from rich.console import Console
from rich.prompt import Prompt
from pystyle import Colors, Colorate

# ==========================================
# 1. ТОХИРГОО (API & FIREBASE)
# ==========================================
API_BASE_URL = "https://kayzennv3.squareweb.app/api"
API_KEY = "APIKEY38"
FIREBASE_URL = "https://telmunn-79711-default-rtdb.firebaseio.com/users.json"
ADMIN_KEY = "0615"
__CHANNEL__ = "TarganJackChannel"

console = Console()

# ==========================================
# 2. CPMApiClient (ЧИНИЙ ӨГСӨН БҮТЦЭЭР)
# ==========================================
class CPMApiClient:
    def __init__(self):
        self.auth_token = None

    def login(self, email, password):
        payload = {"account_email": email, "account_password": password}
        try:
            res = requests.post(f"{API_BASE_URL}/account_login", params={"api_key": API_KEY}, json=payload).json()
            msg = str(res.get('message', '')).upper()
            if res.get('ok') or res.get('error') == 0 or msg == "SUCCESSFUL":
                data = res.get('data', {})
                self.auth_token = data.get('auth') if data.get('auth') else res.get('auth')
                return 0, "SUCCESSFUL"
            return 1, res.get('message', 'Login Failed')
        except: return 1, "Connection Error"

    def set_rank(self, auth):
        try:
            payload = {"account_auth": auth}
            res = requests.post(f"{API_BASE_URL}/set_rank", params={"api_key": API_KEY}, json=payload).json()
            return res.get('ok') or res.get('error') == 0
        except: return False

    def change_email(self, auth, new_email):
        try:
            payload = {"account_auth": auth, "new_email": new_email}
            res = requests.post(f"{API_BASE_URL}/change_email", params={"api_key": API_KEY}, json=payload).json()
            return res.get('ok') or res.get('error') == 0
        except: return False

    def change_password(self, auth, new_password):
        try:
            payload = {"account_auth": auth, "new_password": new_password}
            res = requests.post(f"{API_BASE_URL}/change_password", params={"api_key": API_KEY}, json=payload).json()
            return res.get('ok') or res.get('error') == 0
        except: return False

    def register(self, email, password):
        try:
            payload = {"account_email": email, "account_password": password}
            res = requests.post(f"{API_BASE_URL}/account_register", params={"api_key": API_KEY}, json=payload).json()
            return res.get('ok') or res.get('error') == 0
        except: return False

# ==========================================
# 3. ТУСЛАХ ФУНКЦҮҮД
# ==========================================
def load_db():
    try: return requests.get(FIREBASE_URL, timeout=10).json()
    except: return {}

def update_balance(user_id, new_balance):
    url = f"https://telmunn-79711-default-rtdb.firebaseio.com/users/{user_id}.json"
    requests.patch(url, json={"balance": new_balance})

def banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    brand = "Car Parking Multiplayer 1 Tool"
    print(Colorate.Horizontal(Colors.rainbow, brand.center(60)))
    print(Colorate.Horizontal(Colors.rainbow, '='*60))
    print(Colorate.Horizontal(Colors.rainbow, ' 𝐏𝐋𝐄𝐀𝐒𝐄 𝐋𝐎𝐆𝐎𝐔𝐓 𝐅𝐑𝐎𝐌 𝐂𝐏𝐌 𝐁𝐄𝐅𝐎𝐑𝐄 𝐔𝐒𝐈𝐍𝐆 𝐓𝐇𝐈𝐒 𝐓𝐎𝐎𝐋'.center(60)))
    print(Colorate.Horizontal(Colors.rainbow, ' 𝐒𝐇𝐀𝐑𝐈𝐍𝐆 𝐓𝐇𝐄 𝐀𝐂𝐂𝐄𝐒𝐒 𝐊𝐄𝐘 𝐈𝐒 𝐍𝐎𝐓 𝐀𝐋𝐋𝐎𝐖𝐄𝐃 𝐀𝐍𝐃 𝐖𝐈𝐋𝐋 𝐁𝐄 𝐁𝐋𝐎𝐂𝐊𝐄𝐃'.center(60)))
    print(Colorate.Horizontal(Colors.rainbow, f' 𝐓𝐞𝐥𝐞𝐠𝐫𝐚𝐦: @{__CHANNEL__}'.center(60)))
    print(Colorate.Horizontal(Colors.rainbow, '='*60))

# ==========================================
# 4. ҮНДСЭН ПРОГРАМ
# ==========================================
def main():
    while True:
        banner()
        acc_email = Prompt.ask("[bold white][?] Account Email[/bold white]")
        acc_password = Prompt.ask("[bold white][?] Account Password[/bold white]")
        acc_key = Prompt.ask("[bold white][?] Access Key[/bold white]")

        # 1. Шалгалт (Key & Block)
        db = load_db()
        user_id_ref, found_user = None, None
        is_unlimited = (acc_key == ADMIN_KEY)

        if not is_unlimited:
            for uid, data in db.items():
                if str(data.get('key')) == str(acc_key):
                    user_id_ref, found_user = uid, data
                    break

        # Хэрэв блоктой эсвэл Key байхгүй бол (Чиний хүссэн алдааны мессеж)
        if not is_unlimited and (not found_user or found_user.get('is_blocked')):
            banner()
            print(f"[?] Account Email    : {acc_email}")
            print(f"[?] Account Password : {acc_password}")
            print(f"[?] Access Key       : {acc_key}\n")
            print(Colorate.Horizontal(Colors.red_to_white, "[✘] Trying to Login: TRY AGAIN."))
            print(Colorate.Horizontal(Colors.red_to_white, "[!] Note: make sure you filled out the fields !"))
            time.sleep(4); continue

        # 2. API Login
        cpm = CPMApiClient()
        login_res, login_msg = cpm.login(acc_email, acc_password)

        if login_res != 0:
            banner()
            print(f"[?] Account Email    : {acc_email}")
            print(f"[?] Account Password : {acc_password}")
            print(f"[?] Access Key       : {acc_key}\n")
            print(Colorate.Horizontal(Colors.red_to_white, f"[✘] Trying to Login: TRY AGAIN."))
            print(Colorate.Horizontal(Colors.red_to_white, f"[!] Note: {login_msg} !"))
            time.sleep(4); continue
        
        print(Colorate.Horizontal(Colors.green_to_white, "[√] Trying to Login: SUCCESSFUL.")); time.sleep(1)

        # 3. Үйлчилгээний цэс
        while True:
            banner()
            # Баланс шинэчлэх
            db = load_db()
            if not is_unlimited: found_user = db.get(user_id_ref, {})
            current_bal = 999999999 if is_unlimited else int(found_user.get('balance', 0))
            bal_display = "Unlimited" if is_unlimited else f"{current_bal:,}"

            print(f"Account Email    : {acc_email}")
            print(f"Account password : {acc_password}")
            print(f"Balance          : {bal_display}")
            print(f"Access key       : {acc_key}")
            print(Colorate.Horizontal(Colors.rainbow, '='*60))

            # Цэсийн жагсаалт (Jack загвар)
            print(Colorate.Horizontal(Colors.rainbow, f"{{01}}: SET RANK".ljust(35) + "20.5K"))
            print(Colorate.Horizontal(Colors.rainbow, f"{{02}}: CHANGE EMAIL".ljust(35) + "15.5K"))
            print(Colorate.Horizontal(Colors.rainbow, f"{{03}}: CHANGE PASSWORD".ljust(35) + "10.0K"))
            print(Colorate.Horizontal(Colors.rainbow, f"{{04}}: REGISTER".ljust(35) + "1.0K"))
            print(Colorate.Horizontal(Colors.rainbow, f"{{05}}: LOGOUT"))
            print(Colorate.Horizontal(Colors.rainbow, f"{{06}}: EXIT"))
            print(Colorate.Horizontal(Colors.rainbow, '='*60))

            choice = Prompt.ask("\n[bold yellow][?] Select[/bold yellow]", choices=["1","2","3","4","5","6","01","02","03","04","05","06"])

            if choice in ["5", "05"]: break
            if choice in ["6", "06"]: sys.exit()

            costs = {"01": 20500, "1": 20500, "02": 15500, "2": 15500, "03": 10000, "3": 10000, "04": 1000, "4": 1000}
            clean_choice = choice.zfill(2) if len(choice) == 1 else choice
            cost = costs.get(clean_choice, 0)

            if current_bal >= cost:
                success = False
                if clean_choice == "01": # Rank
                    if cpm.set_rank(cpm.auth_token): success = True
                elif clean_choice == "02": # Email
                    new_e = Prompt.ask("[?] Enter New Email")
                    if cpm.change_email(cpm.auth_token, new_e): acc_email = new_e; success = True
                elif clean_choice == "03": # Pass
                    new_p = Prompt.ask("[?] Enter New Password")
                    if cpm.change_password(cpm.auth_token, new_p): acc_password = new_p; success = True
                elif clean_choice == "04": # Reg
                    re, rp = Prompt.ask("[?] Reg Email"), Prompt.ask("[?] Reg Pass")
                    if cpm.register(re, rp): success = True

                if success:
                    if not is_unlimited:
                        update_balance(user_id_ref, current_bal - cost)
                    print(Colorate.Horizontal(Colors.green_to_white, "SUCCESSFUL (√)"))
                    if Prompt.ask("[?] Do You want to Exit ?", choices=["y", "n"], default="n") == "y":
                        print(Colorate.Horizontal(Colors.rainbow, "Thank you for using SEREK69 Tool!")); sys.exit()
                else:
                    print(Colorate.Horizontal(Colors.red_to_white, "FAILED (✘)"))
            else:
                print(Colorate.Horizontal(Colors.red_to_white, "INSUFFICIENT BALANCE!"))
            time.sleep(2)

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: sys.exit()

