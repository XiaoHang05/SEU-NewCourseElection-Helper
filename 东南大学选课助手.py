# coding: utf-8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import random
import time
import datetime
import os
import sys
import msvcrt

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')


def Login():
    global t
    global error
    global username
    global password
    global teacher
    global driver
    global class_wanted
    global elecTurn

    try:
        driver = webdriver.Chrome(executable_path='chromedriver', chrome_options=chrome_options)
        driver.maximize_window()
        driver.set_window_size(500, 10000)
        url = "https://newxk.urp.seu.edu.cn/xsxk/profile/index.html"
        driver.get(url)
        
        print("start to login\n",flush=True)

        print("\nplease wait.", end="",flush=True)
        successLogin=False
        LoginTurn=1

        driver.find_element_by_xpath(
            '//*[@id="loginNameDiv"]/div/input').click()
        driver.find_element_by_xpath(
            '//*[@id="loginNameDiv"]/div/input').send_keys(username)
        driver.find_element_by_xpath(
            '//*[@id="loginPwdDiv"]/div/input').click()
        driver.find_element_by_xpath(
            '//*[@id="loginPwdDiv"]/div/input').send_keys(password)

        while not successLogin:
            driver.find_element_by_xpath(
                '//*[@id="verifyCode"]').click()
            driver.find_element_by_xpath(
                '//*[@id="verifyCode"]').send_keys(str(0))
            driver.find_element_by_xpath('//*[@id="loginDiv"]/button').click()
            print(".", end="",flush=True)
            time.sleep(1)
            try:
                driver.find_element_by_xpath(
                    '//*[@id="xsxkapp"]/div[4]/div/div[2]/div/table/tbody/tr['+str(elecTurn)+']/td/div/div/div[6]/div[2]/label/span[1]/span').click()
                successLogin=True
            except Exception as eLogin:
                successLogin=False
                print(".", end="",flush=True)
                LoginTurn=LoginTurn+1
                time.sleep(1)

        time.sleep(1)
        
        print(".", end="",flush=True)

        time.sleep(1)
        driver.find_element_by_xpath(
           '//*[@id="xsxkapp"]/div[4]/div/div[3]/span/button[1]').click()
        print(".", end="",flush=True)

        time.sleep(1)
        driver.find_element_by_xpath(
            '//*[@id="stundentinfoDiv"]/button').click()
        print(".", end="",flush=True)

        time.sleep(2)
        print(".\n\n",flush=True)

        checkUrl = driver.current_url
        print("\n"+checkUrl+"\n",flush=True)
        if not checkUrl.startswith("https://newxk.urp.seu.edu.cn/xsxk/elective/"):
            print('Login fail',flush=True)
            error = True
            return
        
        

        print("login successfully!\n",flush=True)
        return

    except Exception as e:
        print('\tlogin fail',flush=True)
        error = True
        return


def main():
    try:
        print("finding.", end="", flush=True)

        while len(classes_wanted) > 0:  # 当 classes_wanted 不为空时继续遍历
            curpages = 1  # 每次从第一页开始
            total_pages = driver.find_element_by_class_name('number.active').text  # 假设第一页已经加载，获取总页数

            # 开始循环翻页
            while curpages <= int(total_pages):
                driver.find_element_by_xpath('//*[@id="xsxkapp"]/div/div[1]/ul/li[1]/i').click()
                time.sleep(0.5)
                print(".", end="", flush=True)
                driver.find_element_by_xpath('//*[@id="xsxkapp"]/div/div[1]/ul/li[2]').click()
                time.sleep(1)
                print(".", end="", flush=True)

                # 跳转到当前页
                driver.find_element_by_xpath(
                    '//*[@id="xsxkapp"]/div/div[3]/div[3]/div/div[2]/span[2]/div/input').send_keys(Keys.BACKSPACE)
                driver.find_element_by_xpath(
                    '//*[@id="xsxkapp"]/div/div[3]/div[3]/div/div[2]/span[2]/div/input').send_keys(Keys.BACKSPACE)
                driver.find_element_by_xpath(
                    '//*[@id="xsxkapp"]/div/div[3]/div[3]/div/div[2]/span[2]/div/input').send_keys(str(curpages))
                driver.find_element_by_xpath(
                    '//*[@id="xsxkapp"]/div/div[3]/div[3]/div/div[2]/span[1]').click()
                time.sleep(1)
                print(".", end="", flush=True)

                # 遍历页面上的所有课程
                class_list = driver.find_elements_by_xpath(
                    '//*[@id="xsxkapp"]/div/div[3]/div[3]/div/div[1]/div')
                for cl in class_list:
                    class_num = cl.find_element_by_xpath(
                        './/*[@class="el-card__body"]/div[2]/div/div[2]/span').text
                    print(".", end="", flush=True)

                    # 遍历 classes_wanted 数组，检查课程号是否在数组中
                    for class_wanted in classes_wanted:
                        if class_wanted[0:-5] == class_num:  # 课程号匹配
                            cl.click()
                            time.sleep(0.2)
                            print(".", end="", flush=True)
                            teacher_list = cl.find_elements_by_xpath(
                                './/*[@class="card-list course-jxb el-row"]/div')

                            for tl in teacher_list:
                                print(".", end="", flush=True)
                                teacher_num = tl.find_element_by_xpath(
                                    './/*[@class="card-item head"]/div[1]/span[1]').text
                                if class_wanted[-3:-1] == teacher_num[1:3]:  # 教师号匹配
                                    print("\n\nfinded\n", flush=True)

                                    # 尝试抢一次
                                    try:
                                        tl.find_element_by_xpath('.//*[@class="el-row"]/button[2]').click()
                                        time.sleep(0.5)

                                        # 检查是否弹出确认框
                                        msgText = driver.find_element_by_xpath('/html/body/div[3]/div/div[2]/div[1]/div[2]/p').text
                                        if "确认选择课程吗？" in msgText:
                                            driver.find_element_by_xpath(
                                                '/html/body/div[3]/div/div[3]/button[2]').click()
                                            print(f"\n成功抢到课程: {class_wanted}\n", flush=True)
                                            classes_wanted.remove(class_wanted)  # 从数组中移除已成功抢到的课程
                                        else:
                                            print(f"\n抢课失败: {class_wanted}\n", flush=True)

                                    except Exception as eTmp:
                                        print(f"\n抢课过程中出现问题: {eTmp}\n", flush=True)

                                    break  # 不再尝试当前页面的其他教师
                            break  # 不再尝试其他课程号

                # 翻页
                curpages += 1

            # 如果翻完所有页后仍有未抢到的课程，重新从第一页开始
            print(f"\n当前未抢到的课程: {classes_wanted}\n", flush=True)
            if len(classes_wanted) > 0:
                print(f"\n翻完所有页，仍有未抢到的课程，重新从第一页开始\n", flush=True)
            else:
                print(f"\n所有课程已成功抢到，结束程序\n", flush=True)
                break

    except Exception as e:
        print(f"\n程序出错: {e}", flush=True)
        error = True
        return


if __name__ == '__main__':
    if "NAME" in os.environ:
        username = os.environ["NAME"]
    else:
        sys.exit()

    if "PASSWORD" in os.environ:
        password = os.environ["PASSWORD"]
    else:
        sys.exit() 

    if "TURN" in os.environ:
        elecTurn = os.environ["TURN"]
    else:
        elecTurn = "1"

    if "CLASS" in os.environ:
        class_wanted = os.environ["CLASS"]
    else:
        sys.exit()

    classes_wanted = ["B15M0011 [04]","B15M0090 [08]"]
    error = False
    Login()
    if not error:
        main()
