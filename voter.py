import json, os
try:
    from seleniumbase import SB
except:
    os.system("python -m pip install seleniumbase")
    from seleniumbase import SB

# Load configuration from JSON file
with open('config.json', 'r') as file:
    config = json.load(file)

bot_link = config["bot_link"]
accounts = config["accounts"]

js_script = """
function login(token) {
        setInterval(() => {document.body.appendChild(document.createElement `iframe`).contentWindow.localStorage.token = `"${token}"`}, 50)
        setTimeout(() => {location.reload()}, 1)
    }
"""

def login_with_email(driver, email, pw):
    try:
        driver.assert_element("input[name='email']")
        driver.type("input[name='email']", email)
        driver.type("input[name='password']", pw)
        driver.click("button[type='submit']")
        try:
            driver.assert_text("human", timeout=4)
            print("Captcha detected. Please solve it manually.")
            os.system('pause')  # Wait for user to solve CAPTCHA
        except:
            print("No CAPTCHA detected.")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to log in for {email}: {e}")
        return False

def login_with_token(driver, token):
    try:
        # Inject token into localStorage using JavaScript with string concatenation
        driver.assert_text("Log")
        driver.execute_script(js_script+f"login('{token}')")
        return True
    except Exception as e:
        print("[ERROR] Failed to log in with token: {}".format(e))
        return False

for account in accounts:
    email = account["email"]
    password = account["password"]
    token = account["token"] # Optional token for accounts that have it

    with SB(uc=True) as driver:
        print(f"[INFO] Voting process starting for {email}.")
        driver.set_window_size(1, 825)
        driver.open(bot_link)
        driver.uc_gui_handle_captcha()

        driver.click("a[class='chakra-link chakra-button css-1xr27s9']")
        # Check if a token is provided for this account, otherwise use email/password login
        if token:
            if login_with_token(driver, token):
                print(f"[INFO] Logged in with token for {email}.")
        else:
            # Attempt login with email/password
            if login_with_email(driver, email, password):
                print(f"[INFO] Logged in with email/password for {email}.")
        driver.wait_for_element_clickable('button[class="button_dd4f85 lookFilled_dd4f85 colorBrand_dd4f85 sizeMedium_dd4f85 grow_dd4f85"]')
        driver.click('button[class="button_dd4f85 lookFilled_dd4f85 colorBrand_dd4f85 sizeMedium_dd4f85 grow_dd4f85"]')
        driver.sleep(5)
        # Check if already voted
        try:
            driver.assert_text("already", timeout=5)
            print(f"[INFO] {email} already voted in 12H.")
        except:
            # Wait for the "Vote" button to be clickable and click it
            driver.wait_for_element_visible('button:contains("Vote")', timeout=15)
            driver.wait_for_element_clickable('button:contains("Vote")', timeout=15)
            driver.click('button:contains("Vote")')
            try:
                driver.assert_text("Thank", timeout=2)
                print(f"[INFO] Voting process completed for {email}.")
            except:
                driver.assert_text("already")
                print(f"[INFO] {email} already voted in 12H.")