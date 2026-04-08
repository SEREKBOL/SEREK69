import os, requests, json, time, sys, random
from rich.console import Console
from rich.prompt import Prompt
from pystyle import Colors, Colorate

# ==========================================
# 1. ТОХИРГОО
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
                # Auth token хадгалах
                data = res.get('data', {})
                self.auth_token = data.get('auth') if data.get('auth') else res.get('auth')
                return 0, "SUCCESSFUL"
            return 1, res.get('message', 'Login Failed')
        except: return 1, "Connection Error"

    # ЧИНИЙ ӨГСӨН: set_rank
    def set_rank(self, auth_token):
        try:
            payload = {"account_auth": auth_token}
            res = requests.post(f"{API_BASE_URL}/set_rank", params={"api_key": API_KEY}, json=payload).json()
            return res.get('ok') or res.get('error') == 0
        except: return False

    # ЧИНИЙ ӨГСӨН: change_email
    def change_email(self, auth_token, new_email):
        try:
            payload = {"account_auth": auth_token, "new_email": new_email}
            res = requests.post(f"{API_BASE_URL}/change_email", params={"api_key": API_KEY}, json=payload).json()
            return res.get('ok') or res.get('error') == 0
        except: return False

    # ЧИНИЙ ӨГСӨН: change_password
    def change_password(self, auth_token, new_password):
        try:
            payload = {"account_auth": auth_token, "new_password": new_password}
            res = requests.post(f"{API_BASE_URL}/change_password", params={"api_key": API_KEY}, json=payload).json()
            return res.get('ok') or res.get('error') == 0
        except: return False

    # ЧИНИЙ ӨГСӨН: account_register
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
    try:
        response = requests.get(FIREBASE_URL, timeout=10)
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
    print(Colorate.Horizontal(Colors.rainbow, f'           𝐓𝐞𝐥𝐞𝐠𝐫𝐚𝐦: @{__CHANNEL__} 𝐎𝐫 @TarganJackChat'))
    print(Colorate.Horizontal(Colors.rainbow, '='*60))

# ==========================================
# 4. ҮНДСЭН ПРОГРАМ
# ==========================================
def main():
    while True:
        banner()
        acc_email = Prompt.ask("[bold white][?] Account Email[/bold white]")
        acc_password = Prompt.ask("[bold white][?] Account Password[/bold white]")
        access_key = Prompt.ask("[bold white][?] Access Key[/bold white]")

        db = load_db()
        user_id_ref = None
        found_data = None
        is_unlimited = (access_key == ADMIN_KEY)

        if not is_unlimited:
            for uid, data in db.items():
                if str(data.get('key')) == str(access_key):
                    user_id_ref = uid
                    found_data = data
                    break

        cpm = CPMApiClient()
        login_res, login_msg = cpm.login(acc_email, acc_password)

        access_ok = is_unlimited or found_data
        
        if login_res != 0 or not access_ok:
            banner()
            print(f"[?] Account Email: {acc_email}")
            print(f"[?] Account Password: {acc_password}")
            print(f"[?] Access Key: {access_key}\n")
            if not access_ok:
                print(Colorate.Horizontal(Colors.red_to_white, "[✘] ACCESS KEY БУРУУ!"))
            else:
                print(Colorate.Horizontal(Colors.red_to_white, f"[✘] CPM API АЛДАА: {login_msg}"))
            print(Colorate.Horizontal(Colors.red_to_white, "[!] Note: make sure you filled out the fields !"))
            time.sleep(4); continue
        
        print(Colorate.Horizontal(Colors.green_to_white, f"[√] Trying to Login: SUCCESSFUL."))
        time.sleep(2)

        while True:
            banner()
            db = load_db()
            if not is_unlimited: found_data = db.get(user_id_ref)
            
            current_bal = 999999999 if is_unlimited else found_data.get('balance', 0)
            tg_id = "ADMIN" if is_unlimited else found_data.get('telegram_id', 'N/A')
            bal_txt = "Unlimited" if is_unlimited else f"{current_bal:,} ₮"

            print(f"Account Email    : {acc_email}")
            print(f"Account password : {acc_password}")
            print(f"Telegram id      : {tg_id}")
            print(f"Access key       : {access_key}")
            print(Colorate.Horizontal(Colors.green_to_white, f"Balance          : {bal_txt}"))
            print(Colorate.Horizontal(Colors.rainbow, '='*60))

            print(Colorate.Horizontal(Colors.rainbow, f"{{01}}: SET RANK".ljust(45) + "20.5K"))
            print(Colorate.Horizontal(Colors.rainbow, f"{{02}}: CHANGE EMAIL".ljust(45) + "15.5K"))
            print(Colorate.Horizontal(Colors.rainbow, f"{{03}}: CHANGE PASSWORD".ljust(45) + "10.0K"))
            print(Colorate.Horizontal(Colors.rainbow, f"{{04}}: REGISTER".ljust(45) + "1.0K"))
            print(Colorate.Horizontal(Colors.rainbow, f"{{05}}: LOGOUT FROM ACCOUNT"))
            print(Colorate.Horizontal(Colors.rainbow, f"{{06}}: EXIT FROM TOOL"))
            print(Colorate.Horizontal(Colors.rainbow, '='*60))

            choice = Prompt.ask("\n[bold yellow][?] Select Service[/bold yellow]")

            if choice == "5": break
            if choice == "6": sys.exit()

            costs = {"1": 20500, "2": 15500, "3": 10000, "4": 1000}
            if choice in costs:
                cost = costs[choice]
                if current_bal >= cost:
                    success = False
                    
                    if choice == "1": # SET RANK
                        console.print("[bold cyan][%] Giving you a King Rank...[/bold cyan]")
                        if cpm.set_rank(cpm.auth_token): success = True
                    
                    elif choice == "2": # CHANGE EMAIL
                        new_e = Prompt.ask("[bold cyan][?] Enter New Email[/bold cyan]")
                        console.print("[bold cyan][%] Saving your data...[/bold cyan]")
                        if cpm.change_email(cpm.auth_token, new_e):
                            acc_email = new_e # Update screen
                            success = True
                    
                    elif choice == "3": # CHANGE PASSWORD
                        new_p = Prompt.ask("[bold cyan][?] Enter New Password[/bold cyan]")
                        console.print("[bold cyan][%] Saving your data...[/bold cyan]")
                        if cpm.change_password(cpm.auth_token, new_p):
                            acc_password = new_p # Update screen
                            success = True
                    
                    elif choice == "4": # REGISTER
                        reg_e = Prompt.ask("[bold cyan][?] New Account Email[/bold cyan]")
                        reg_p = Prompt.ask("[bold cyan][?] New Account Password[/bold cyan]")
                        console.print("[bold cyan][%] Creating new Account...[/bold cyan]")
                        if cpm.register(reg_e, reg_p): success = True

                    if success:
                        if not is_unlimited:
                            new_bal = current_bal - cost
                            update_balance(user_id_ref, new_bal)
                        
                        print(Colorate.Horizontal(Colors.green_to_white, "SUCCESSFUL (√)"))
                        print(Colorate.Horizontal(Colors.rainbow, '='*40))
                        
                        answ = Prompt.ask("[bold][?] Do You want to Exit ?", choices=["y", "n"], default="n")
                        if answ == "y":
                            print(Colorate.Horizontal(Colors.rainbow, f"Thank You for using our tool, please join @{__CHANNEL__}."))
                            sys.exit()
                    else:
                        print(Colorate.Horizontal(Colors.red_to_white, "FAILED (✘)"))
                        time.sleep(2)
                else:
                    print(Colorate.Horizontal(Colors.red_to_white, "INSUFFICIENT BALANCE!"))
                    time.sleep(2)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()

