from datetime import datetime, timedelta

def get_user_timezone():
    while True:
        timezone_input = input("Introduceți zona geografică (ex: GMT+3 sau GMT-5): ").strip().upper()
        if timezone_input.startswith("GMT+") or timezone_input.startswith("GMT-"):
            try:
                offset = int(timezone_input[4:])
                if -11 <= offset <= 11:
                    return offset
                else:
                    print("Valoarea trebuie să fie între -11 și +11.")
            except ValueError:
                print("Format invalid. Exemplu corect: GMT+3 sau GMT-5")
        else:
            print("Format invalid. Exemplu corect: GMT+3 sau GMT-5")

def show_time_for_timezone(offset):
    utc_time = datetime.utcnow()
    target_time = utc_time + timedelta(hours=offset)
    print(f"Ora exactă pentru GMT{'+' if offset >= 0 else ''}{offset}: {target_time.strftime('%H:%M:%S')}")

if __name__ == "__main__":
    offset = get_user_timezone()
    show_time_for_timezone(offset)
