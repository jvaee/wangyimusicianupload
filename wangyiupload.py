import time
import os
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

setting_lines = []
with open('wangyi.setting', 'r', encoding='utf-8') as f:
    setting_lines = f.readlines()
chrome_options = Options()
# chrome 地址栏输入chrome://version  获取 个人资料路径
chrome_options.add_argument(setting_lines[1].strip())
# 创建 Service 对象，指定 chromedriver 的路径
service_obj = Service(setting_lines[13].strip())
# service_obj = ""
# 使用 service 参数初始化 webdriver.Chrome
driver = webdriver.Chrome(service=service_obj, options=chrome_options)
# 打开网页
driver.get("https://music.163.com/musician/artist/manage/album/nalbum/songupload")

language_template = (
    '//*[@id="mcc-page-layout-body"]/div/div[2]/div/div[2]/div[2]/div[2]/div/div/div/div[{index}]/div[2]/div/div/form/div[5]/div[2]/div/div/div/div/div/div/ul/li/div/input'
)

style_template = (
    '//*[@id="mcc-page-layout-body"]/div/div[2]/div/div[2]/div[2]/div[2]/div/div/div/div[{index}]/div[2]/div/div/form/div[6]/div[2]/div/div/div/div/div/div/ul/li/div/input'
)

lyrics_template = (
    '//*[@id="mcc-page-layout-body"]/div/div[2]/div/div[2]/div[2]/div[2]/div/div/div/div[{index}]/div[2]/div/div/form/div[13]/div[2]/div/div/div/div[1]/div/div/div/div[1]/p'
)

style_icon_template =(
    '//*[@id="mcc-page-layout-body"]/div/div[{index}]/div/div/div/div[2]'
)

# 继续进行其他操作
user_input = input("登录完成请输入1:")


def get_wave_path():
    while True:
        wave_path = input("请输入待上传文件路径：")
        if os.path.exists(wave_path) and os.path.isdir(wave_path):
            return wave_path
        else:
            print("路径不存在或不是一个有效的目录，请重新输入！")

def get_wave_file(wave_path):
    wav_files = []
    for root, dirs, files in os.walk(wave_path):
        for file in files:
            if file.lower().endswith('.wav'):
                wav_files.append(os.path.join(root, file))
    return wav_files

if  user_input == "1":
    print(driver.title)
    print("获取输入框")
    file_input_element = driver.find_element(By.XPATH,
                                              "//*[@id=\"mcc-page-layout-body\"]/div/div[2]/div/div[2]/div[2]/div[3]/input")
    # 构造多个文件的绝对路径，并用换行符分隔（确保路径正确）
    wave_path = setting_lines[3].strip()
    if wave_path == "":
        wave_path = get_wave_path()
    # 遍历获取路径下的.wav 文件
    wave_list = get_wave_file(wave_path)
    num = 1
    files = ""
    wave_name = []
    upload_wave_file = []
    max_num = int(setting_lines[11])
    for wave in wave_list:
        num = num + 1
        print(num)
        wave_name.append(os.path.basename(wave))
        upload_wave_file.append(wave)
        if num > max_num:
            break
    files_to_upload = '\n'.join(upload_wave_file)
    file_input_element.send_keys(files_to_upload)
    time.sleep(float(setting_lines[5].strip()))
    for i in  range(1,num):
        language = language_template.format(index=i)
        language_element = driver.find_element(By.XPATH,language)
        language_element.send_keys(setting_lines[7].strip())
        style = style_template.format(index=i)
        style_element = driver.find_element(By.XPATH,style)
        driver.execute_script("arguments[0].scrollIntoView();", style_element)
        time.sleep(2)
        style_element.click()
        time.sleep(4)
        style_icon = style_icon_template.format(index=2+i)
        style_sub_body_element = driver.find_element(By.XPATH,style_icon)
        stlye_icon = style_sub_body_element.find_elements(By.CLASS_NAME,'panel-item')
        time.sleep(2)
        style_index = setting_lines[9].strip().split('#')
        for index in style_index:
            stlye_icon[int(index)].click()
        body = driver.find_element(By.TAG_NAME, "body")
        body.click()
        time.sleep(2)
        print('style end')
        lyrics = lyrics_template.format(index=i)
        lyrics_element = driver.find_element(By.XPATH,lyrics)
        driver.execute_script("arguments[0].scrollIntoView();",lyrics_element)
        lyrics_name = wave_name[i-1].replace('.wav','.txt')
        lyrics_path = setting_lines[3].strip() + "/" + lyrics_name
        print(lyrics_path)
        if(os.path.exists(lyrics_path)):
            with open(lyrics_path, 'r', encoding='utf-8') as f:
                lyrics_element.send_keys(f.readlines())
                time.sleep(5)
    while True:
        close_input = input("输入exit关闭")
        if close_input == "exit":
            # 关闭浏览器
            driver.quit()
            break
