from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from speech_recognition import AudioFile, Recognizer
from pydub import AudioSegment
from requests import get
from time import sleep
import pyautogui
import json


#PROXY = "13.251.26.136:3128"
options = Options()
options.add_argument("--window-size=700,720")
options.add_argument("--incognito")
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
options.add_argument('--disable-infobars')
options.add_argument("--disable-extensions")
#options.add_argument('--proxy-server=%s' % PROXY)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
#options.add_argument("--user-agent=Mozilla/5.0 (X11; Linux i686 on x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2728.29 Safari/537.36")



def process_browser_log_entry(entry):
    response = json.loads(entry['message'])['message']
    return response



caps = DesiredCapabilities.CHROME
caps['goog:loggingPrefs'] = {'performance': 'ALL'}
driver = Chrome(options=options, desired_capabilities=caps)
URL = 'https://www.google.com/recaptcha/api2/demo'
driver.get(URL)

pyautogui.click(74,510)
sleep(5)
pyautogui.click(243,727)
sleep(5)
pyautogui.click(405,460)
sleep(10)


browser_log = driver.get_log('performance') 
events = [process_browser_log_entry(entry) for entry in browser_log]
for x in events:
    try:
        if x['params']['type'] == 'Media':
            lastaudio = x['params']['request']['url']
    except:
        pass

with open('1.mpeg', 'wb') as f:
    f.write(get(lastaudio).content)
    
sound = AudioSegment.from_mp3("1.mpeg")
sound.export("transcript.wav", format="wav")
                  
r = Recognizer()

with AudioFile('transcript.wav') as source:
        audio = r.record(source)
        transcript =  r.recognize_google(audio)
        print("Transcription: " + transcript)

driver.switch_to.default_content()
iframe = driver.find_elements_by_tag_name('iframe')[-1]
driver.switch_to.frame(iframe)
i = driver.find_elements_by_tag_name('input')[1].send_keys(transcript + Keys.ENTER)

sleep(5)
driver.switch_to.default_content()
driver.find_element_by_xpath('/html/body/div[1]/form/fieldset/ul/li[6]/input').click()



