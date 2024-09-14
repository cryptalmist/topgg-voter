import os
try:
    from seleniumbase import SB
except:
    os.system("pip install seleniumbase")
    from seleniumbase import SB
from config import *

def login(driver, email, pw):
    try:
        # if use_cookies and os.path.exists(f"saved_cookies/{email}.txt"):
        #     driver.load_cookies(email)
        #     driver.sleep(2)
        #     driver.reload()
        #     print(f"[INFO] Loaded saved cookies for {email}.")
        # else:
        driver.click("a[class='chakra-link chakra-button css-1xr27s9']")
        driver.type("input[name='email']", email)
        driver.type("input[name='password']", pw)
        driver.click("button[type='submit']")
        driver.click('button[class="button_dd4f85 lookFilled_dd4f85 colorBrand_dd4f85 sizeMedium_dd4f85 grow_dd4f85"]')
        driver.sleep(5)
        print(f"[INFO] Successfully logged in with credentials for {email}.")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to log in for {email}: {e}")
        return 

for account in accounts:
    email = account["email"]
    password = account["password"]

    with SB(uc=True, maximize=True) as driver:
            driver.open(bot_link)
            driver.uc_gui_click_captcha()

            # Attempt login and check status
            if login(driver, email, password):
                # Wait for the "Vote" button to be clickable
                driver.wait_for_element_visible('button:contains("Vote")', timeout=15)
                driver.wait_for_element_clickable('button:contains("Vote")', timeout=15)
                driver.click('button:contains("Vote")')
                # driver.save_cookies(name=email)
                try:
                    driver.assert_text("Thank",timeout=2)
                    print(f"[INFO] Voting process completed for {email}.")
                except:
                    driver.assert_text("already")
                    print(f"[INFO] {email} already voted in 12H.")
            else:
                print(f"[INFO] Skipping voting for {email} due to login failure.")
