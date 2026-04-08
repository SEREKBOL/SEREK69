import os, requests, json, time, sys, random, signal
from rich.console import Console
from rich.prompt import Prompt, IntPrompt
from rich.text import Text
from rich.style import Style
from pystyle import Colors, Colorate
from cpmtooldev import CPMTooldev  # Чиний API Client

# CONFIG УНШИХ
def load_config():
    if os.path.exists("config.json"):
        with open("config.json", "r") as f: return json.load(f)
    return {"api_base_url": "https://kayzennv3.squareweb.app/api", "api_key": "APIKEY38", "admin_key": "0615"}

CONFIG = load_config()
DB_FILE = "keys.json"
__CHANNEL__ = "TarganJackChannel"

# Үйлчилгээний үнэ (Jack-ийн цэснээс авсан)
PRICES = {
    1: 1500, 2: 4500, 3: 8000, 4: 4500, 5: 100, 6: 100, 7: 2000, 10: 500,
    11: 5000, 12: 6000, 13: 3500, 14: 4000, 15: 3000, 16: 3000, 17: 3000,
    18: 4000, 19: 4000, 20: 4000, 21: 2000, 22: 3000, 23: 3000, 24: 1000,
    25: 1000, 26: 7000, 27: 2500, 28: 1500, 29: 1500, 30: 2000, 31: 2000
}

def load_db():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f: return json.load(f)
        except: return {}
    return {}

def save_db(data):
    with open(DB_FILE, "w") as f: json.dump(data, f, indent=4)

def banner(console):
    os.system('cls' if os.name == 'nt' else 'clear')
    brand = "Car Parking Multiplayer Tool V3"
    print(Colorate.Horizontal(Colors.rainbow, '============================================================'))
    print(Colorate.Horizontal(Colors.rainbow, f'\t         WELCOME TO MODIFIED TOOL BY JACK'))
    print(Colorate.Horizontal(Colors.rainbow, f' ‌           𝐓𝐞𝐥𝐞𝐠𝐫𝐚𝐦: @{__CHANNEL__}'))
    print(Colorate.Horizontal(Colors.rainbow, '============================================================'))

def load_client_details():
    try:
        data = requests.get("http://ip-api.com/json").json()
        print(Colorate.Horizontal(Colors.rainbow, '=============[ 𝐋𝐎𝐂𝐀𝐓𝐈𝐎𝐍 ]============='))
        print(Colorate.Horizontal(Colors.rainbow, f'Ip Address : {data.get("query")} | {data.get("country")}'))
        print(Colorate.Horizontal(Colors.rainbow, '===============[ 𝐌𝐄𝐍𝐔 ]==============='))
    except: pass

def rainbow_gradient_string(customer_name):
    modified_string = ""
    for char in customer_name:
        color = "{:06x}".format(random.randint(0, 0xFFFFFF))
        modified_string += f'[{color}]{char}'
    return modified_string

def main():
    console = Console()
    banner(console)
    
    # 1. LOGIN
    acc_email = Prompt.ask("[bold][?] Account Email[/bold]")
    acc_password = Prompt.ask("[bold][?] Account Password[/bold]", password=True)
    acc_access_key = Prompt.ask("[bold][?] Access Key[/bold]")
    
    # БАЛАНС БОЛОН KEY ШАЛГАХ
    db = load_db()
    is_unlimited = False
    user_id_ref = None
    
    if acc_access_key == CONFIG['admin_key']:
        is_unlimited = True
    else:
        found_uid = next((uid for uid, data in db.items() if data.get('key') == acc_access_key), None)
        if not found_uid:
            print(Colorate.Horizontal(Colors.red_to_white, "INVALID ACCESS KEY!")); sys.exit()
        if db[found_uid].get('is_blocked'):
            print(Colorate.Horizontal(Colors.red_to_white, "YOU ARE BLOCKED!")); sys.exit()
        user_id_ref = found_uid
        is_unlimited = db[found_uid].get('unlimited', False)

    # CPM LOGIN
    cpm = CPMTooldev(acc_access_key)
    print("[bold cyan][%] Trying to Login...[/bold cyan]")
    login_res = cpm.login(acc_email, acc_password)
    
    if login_res != 0:
        print(Colorate.Horizontal(Colors.red_to_white, "CPM LOGIN FAILED!")); sys.exit()

    while True:
        banner(console)
        # Player Data Load
        player_data = cpm.get_player_data()
        if player_data.get('ok'):
            d = player_data.get('data')
            print(Colorate.Horizontal(Colors.rainbow, f'Name: {d.get("Name")} | Money: {d.get("money")} | Coin: {d.get("coin")}'))
        
        # Balance Load
        db = load_db() # Refresh
        current_bal = 999999999 if is_unlimited else db[user_id_ref].get('balance', 0)
        bal_display = "Unlimited" if is_unlimited else f"{current_bal:,} ₮"
        print(Colorate.Horizontal(Colors.green_to_white, f"YOUR BALANCE: {bal_display}"))
        load_client_details()

        # SERVICES MENU (Jack-ийн цэс)
        print(Colorate.Horizontal(Colors.rainbow, '{01}: Increase Money 1.5K | {02}: Increase Coins 4.5K'))
        print(Colorate.Horizontal(Colors.rainbow, '{03}: King Rank 8K      | {04}: Change ID 4.5K'))
        print(Colorate.Horizontal(Colors.rainbow, '{05}: Name Change 100   | {06}: Rainbow Name 100'))
        print(Colorate.Horizontal(Colors.rainbow, '{11}: Unlock Paid Cars 5k| {12}: Unlock All Cars 6K'))
        print(Colorate.Horizontal(Colors.rainbow, '{27}: Custom HP 2.5K    | {28}: Custom Angle 1.5K'))
        print(Colorate.Horizontal(Colors.rainbow, '{0} : Exit'))

        service = IntPrompt.ask(f"[bold][?] Select [1-31][/bold]")
        
        if service == 0: break
        
        if service in PRICES:
            cost = PRICES[service]
            if current_bal >= cost:
                # ҮЙЛДЛҮҮД
                success = False
                if service == 1: # Money
                    amount = IntPrompt.ask("[?] Amount (Max 50M)")
                    if cpm.set_player_money(amount): success = True
                elif service == 2: # Coins
                    amount = IntPrompt.ask("[?] Amount (Max 50K)")
                    if cpm.set_player_coins(amount): success = True
                elif service == 3: # King Rank
                    if cpm.set_player_rank(): success = True
                elif service == 4: # ID
                    new_id = Prompt.ask("[?] New ID")
                    if cpm.set_player_localid(new_id.upper()): success = True
                elif service == 6: # Rainbow Name
                    name = Prompt.ask("[?] Name")
                    if cpm.set_player_name(rainbow_gradient_string(name)): success = True
                elif service == 27: # HP
                    car_id = IntPrompt.ask("[?] Car ID")
                    hp = IntPrompt.ask("[?] HP")
                    if cpm.hack_car_speed(car_id, hp, hp, hp, hp): success = True
                # ... Бусад service-үүдийг Jack-ийн код шиг энд нэмнэ ...

                if success:
                    if not is_unlimited:
                        db[user_id_ref]['balance'] -= cost
                        save_db(db)
                    print(Colorate.Horizontal(Colors.green_to_white, "SUCCESSFUL!"))
                else:
                    print(Colorate.Horizontal(Colors.red_to_white, "FAILED!"))
                time.sleep(2)
            else:
                print(Colorate.Horizontal(Colors.red_to_white, "INSUFFICIENT BALANCE!"))
                time.sleep(2)

if __name__ == "__main__":
    main()

