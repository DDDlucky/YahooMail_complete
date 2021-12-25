from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import re
import sys
import time

# メールの入っているフォルダの名前　
# こちらの変数はmineo様ご自身で変更して頂けます。対象のメールを保存しているフォルダの名前をダブルクウォーテーションの中に正確にご記入ください。
FolderName = "あ"



'''
【処理説明】
受信箱に入っているメールの件数を取得
↓
その件数分だけメールを開いていく→開いてダウンロードチェック→次をチェックのくり返し
'''



# Chrome設定
options = webdriver.ChromeOptions()
options.add_argument('--lang=ja')
options.add_argument("--disable-blink-features=AutomationControlled")
# options.add_argument('--user-data-dir=/Users/do/Library/Application Support/Google/Chrome/Default')
options.add_argument('--user-data-dir=C:/Users/binoy/AppData/Local/Google/Chrome/User Data/Default')

print("↓下記の赤文字はエラーではありません")
# drivermanagerを利用
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.implicitly_wait(3)


def login_check():
    driver.get("https://mail.yahoo.co.jp/")
    while True:
        if driver.find_elements(by=By.ID, value="username"):
            print("ログインを終えたら、このコンソールでエンターを押してください。すると取得処理が始まります。")
            input("please Enter>>")
            driver.get("https://mail.yahoo.co.jp/")
        else:
            print("ログインしています")
            break
    return



def Check():  # 受信箱の件数を取得する関数
    global title
    check = 0
    for i in driver.find_elements(by=By.CSS_SELECTOR, value=".sc-1gs1ku3-11.ioHncI"):
        if i.text == FolderName:
            check = 1
            i.click()
            title = i.find_element(by=By.XPATH, value="..").find_element(by=By.XPATH, value="..").get_attribute("title")
    if check == 0:
        print("\n指定のフォルダが見つかりませんでした。フォルダ名が間違えていないか確認し、再実行していください。\n")
        sys.exit()

    result = re.sub(r"\D", "", title)
    print(f"\nフォルダ[{FolderName}]にメールが{result}件ありました")
    return int(result)


def Download():  # 1番上のメール開く(開いてダウンロードボタンがあったらダウンロードする)→「次へ」を押す　を繰り返す関数
    # 1番目のメールをダブルクリックして開く
    driver.find_elements(by=By.CSS_SELECTOR, value=".sc-1xxpdrg-12.dPxRUi")[0].click()
    time.sleep(1)
    driver.find_element(by=By.XPATH, value="//button[contains(text(), 'その他')]").click()
    time.sleep(1)
    driver.find_element(by=By.XPATH, value="//span[contains(text(), '開く')]").click()

    for i in range(MailCount):
        time.sleep(0.5)
        print(f"{i + 1}件目")
        # 「すべてダウンロード」のボタンがあるか確認
        if driver.find_elements(by=By.CSS_SELECTOR, value=".sc-1ns50jh-0.jcxzud"):
            # 添付されたファイルが何個か取得
            FILE_LEN = int(driver.find_element(by=By.CSS_SELECTOR, value=".sc-1ns50jh-0.jcxzud").text)
            if FILE_LEN == 1:
                driver.execute_script("arguments[0].style.visibility = 'visible';", driver.find_element(by=By.CSS_SELECTOR, value=".sc-1ns50jh-0.jcxzud"))
                webdriver.ActionChains(driver).move_to_element(driver.find_element(by=By.CSS_SELECTOR, value=".sc-1ns50jh-0.jcxzud")).perform()
                driver.find_element(by=By.CSS_SELECTOR, value=".sc-1ns50jh-0.jcxzud").click()
                while True:
                    try:
                        driver.find_element(by=By.XPATH, value="//a[contains(text(), 'ダウンロード')]").click()
                        break
                    except:
                        pass
            # 添付ファイルが2個以上の場合
            else:
                for v in driver.find_elements(by=By.CSS_SELECTOR, value=".qsxs13-16.dFPEno"):
                    driver.execute_script("arguments[0].style.visibility = 'visible';", v)
                    webdriver.ActionChains(driver).move_to_element(v).perform()
                    try:
                        v.click()
                    except:
                        webdriver.ActionChains(driver).move_to_element(v).perform()
                        v.click()
                    while True:
                        try:
                            driver.find_element(by=By.XPATH, value="//a[contains(text(), 'ダウンロード')]").click()
                            break
                        except:
                            pass
        # 次のメールへ行くボタンが効かないようなので削除に変更
        # driver.find_element(by=By.XPATH, value="//button[contains(text(), '削除')]").click()


        # 高速化するため、要素数が４つ（次のメールに行くボタンがある場合）は要素の3つ目をクリックし、要素数が4個ではない場合は次へ行くボタンの探索を行う
        if len(driver.find_elements(by=By.CSS_SELECTOR, value=".sc-1ns50jh-0.dLyDTl.sc-1tfa8og-4.fsRUzb")) == 4:
            driver.find_elements(by=By.CSS_SELECTOR, value=".sc-1ns50jh-0.dLyDTl.sc-1tfa8og-4.fsRUzb")[2].click()
    
    
        else:
            for q in driver.find_elements(by=By.CSS_SELECTOR, value=".sc-1ns50jh-0.dLyDTl.sc-1tfa8og-4.fsRUzb"):
                if q.get_attribute("title") == "次のメール":
                    q.click()

    print("終了")



login_check()
MailCount = Check()
Download()
