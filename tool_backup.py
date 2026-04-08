import os, requests, json, time, sys, random
from rich.console import Console
from rich.prompt import Prompt
from pystyle import Colors, Colorate

# --- ТОХИРГОО ---
API_BASE_URL = "https://kayzennv3.squareweb.app/api"
API_KEY = "APIKEY38"
FIREBASE_URL = "https://telmunn-79711-default-rtdb.firebaseio.com/users.json"
ADMIN_KEY = "0615"
__CHANNEL__ = "TarganJackChannel"

console = Console()

class CPMApiClient:
    def __init__(self):
        self.auth_token = None

    def login(self, email, password):
        try:
            res = requests.post(f"{API_BASE_URL}/account_login", params={"api_key": API_KEY}, json={"account_email": email, "account_password": password}).json()
            msg = str(res.get('message', '')).upper()
            if res.get('ok') or res.get('error') == 0 or msg == "SUCCESSFUL":
                data = res.get('data', {})
                self.auth_token = data.get('auth') if data.get('auth') else res.get('auth')
                return 0
            return 1
        except: return 1

    def set_rank(self, auth):
        try:
            res = requests.post(f"{API_BASE_URL}/set_rank", params={"api_key": API_KEY}, json={"account_auth": auth}).json()
            return res.get('ok') or res.get('error') == 0
        except: return False

    def change_email(self, auth, new_email):
        try:
            res = requests.post(f"{API_BASE_URL}/change_email", params={"api_key": API_KEY}, json={"account_auth": auth, "new_email": new_email}).json()
            return res.get('ok') or res.get('error') == 0
        except: return False

    def change_password(self, auth, new_pass):
        try:
            res = requests.post(f"{API_BASE_URL}/change_password", params={"api_key": API_KEY}, json={"account_auth": auth, "new_password": new_pass}).json()
            return res.get('ok') or res.get('error') == 0
        except: return False

    def register(self, email, password):
        try:
            res = requests.post(f"{API_BASE_URL}/account_register", params={"api_key": API_KEY}, json={"account_email": email, "account_password": password}).json()
            return res.get('ok') or res.get('error') == 0
        except: return False

def load_db():
    try: return requests.get(FIREBASE_URL, timeout=10).json()
    except: return {}

def update_bal(uid, bal):
    url = f"https://telmunn-79711-default-rtdb.firebaseio.com/users/{uid}.json"
    requests.patch(url, json={"balance": bal})

def banner():
    os.system('clear')
    brand = "Car Parking Multiplayer 1 Tool"
    print(Colorate.Horizontal(Colors.rainbow, brand.center(60)))
    print(Colorate.Horizontal(Colors.rainbow, '='*60))
    print(Colorate.Horizontal(Colors.rainbow, '       𝐏𝐋𝐄𝐀𝐒𝐄 𝐋𝐎𝐆𝐎𝐔𝐓 𝐅𝐑𝐎𝐌 𝐂𝐏𝐌 𝐁𝐄𝐅𝐎𝐑𝐄 𝐔𝐒𝐈𝐍𝐆 𝐓𝐇𝐈𝐒 𝐓𝐎𝐎𝐋\n    𝐒𝐇𝐀𝐑𝐈𝐍𝐆 𝐓𝐇𝐄 𝐀𝐂𝐂𝐄𝐒𝐒 𝐊𝐄𝐘 𝐈𝐒 𝐍𝐎𝐓 𝐀𝐋𝐋𝐎𝐖𝐄𝐃 𝐀𝐍𝐃 𝐖𝐈𝐋𝐋 𝐁𝐄 𝐁𝐋𝐎𝐂𝐊𝐄𝐃\n           𝐓𝐞𝐥𝐞𝐠𝐫𝐚𝐦: @TarganJackChannel'))
    print(Colorate.Horizontal(Colors.rainbow, '='*60))

def main():
    while True:
        banner()
        email = Prompt.ask("[bold white][?] Account Email[/bold white]")
        password = Prompt.ask("[bold white][?] Account Password[/bold white]")
        key = Prompt.ask("[bold white][?] Access Key[/bold white]")

        db = load_db()
        user_id_ref, found_user = None, None
        is_unlimited = (key == ADMIN_KEY)

        if not is_unlimited:
            for uid, data in db.items():
                if str(data.get('key')) == str(key):
                    user_id_ref, found_user = uid, data
                    break

        # БЛОК ШАЛГАХ (ЧИНИЙ ХҮССЭНЭЭР)
        if not is_unlimited and (not found_user or found_user.get('is_blocked')):
            banner()
            print(f"[?] Account Email: {email}\n[?] Account Password: {password}\n[?] Access Key: {key}\n")
            print(Colorate.Horizontal(Colors.red_to_white, "[✘] Trying to Login: TRY AGAIN.\n[!] Note: make sure you filled out the fields !"))
            time.sleep(4); continue

        cpm = CPMApiClient()
        if cpm.login(email, password) != 0:
            print(Colorate.Horizontal(Colors.red_to_white, "[✘] CPM LOGIN FAILED.")); time.sleep(2); continue
        
        print(Colorate.Horizontal(Colors.green_to_white, "[√] Trying to Login: SUCCESSFUL.")); time.sleep(1)

        while True:
            banner()
            db = load_db()
            if not is_unlimited: found_user = db.get(user_id_ref)
            bal = 999999999 if is_unlimited else found_user.get('balance', 0)
            
            print(f"Account Email    : {email}\nAccount password : {password}")
            print(Colorate.Horizontal(Colors.green_to_white, f"Balance          : {'Unlimited' if is_unlimited else f'{bal:,} ₮'}"))
            print(Colorate.Horizontal(Colors.rainbow, '='*60))
            print(Colorate.Horizontal(Colors.rainbow, f"{{01}}: SET RANK".ljust(45) + "20.5K"))
            print(Colorate.Horizontal(Colors.rainbow, f"{{02}}: CHANGE EMAIL".ljust(45) + "15.5K"))
            print(Colorate.Horizontal(Colors.rainbow, f"{{03}}: CHANGE PASSWORD".ljust(45) + "10.0K"))
            print(Colorate.Horizontal(Colors.rainbow, f"{{04}}: REGISTER".ljust(45) + "1.0K"))
            print(Colorate.Horizontal(Colors.rainbow, f"{{05}}: LOGOUT\n{{06}}: EXIT\n" + '='*60))

            choice = Prompt.ask("\n[bold yellow][?] Select[/bold yellow]")
            if choice == "5": break
            if choice == "6": sys.exit()

            costs = {"1": 20500, "2": 15500, "3": 10000, "4": 1000}
            if choice in costs:
                cost = costs[choice]
                if bal >= cost:
                    success = False
                    if choice == "1":
                        if cpm.set_rank(cpm.auth_token): success = True
                    elif choice == "2":
                        new_e = Prompt.ask("[?] New Email")
                        if cpm.change_email(cpm.auth_token, new_e): email = new_e; success = True
                    elif choice == "3":
                        new_p = Prompt.ask("[?] New Password")
                        if cpm.change_password(cpm.auth_token, new_p): password = new_p; success = True
                    elif choice == "4":
                        re, rp = Prompt.ask("[?] Reg Email"), Prompt.ask("[?] Reg Pass")
                        if cpm.register(re, rp): success = True

                    if success:
                        if not is_unlimited: update_bal(user_id_ref, bal - cost)
                        print(Colorate.Horizontal(Colors.green_to_white, "SUCCESSFUL (√)"))
                        if Prompt.ask("[?] Exit?", choices=["y", "n"]) == "y": sys.exit()
                    else: print(Colorate.Horizontal(Colors.red_to_white, "FAILED (✘)"))
                else: print(Colorate.Horizontal(Colors.red_to_white, "INSUFFICIENT BALANCE!"))
                time.sleep(2)

if __name__ == "__main__":
    main()

