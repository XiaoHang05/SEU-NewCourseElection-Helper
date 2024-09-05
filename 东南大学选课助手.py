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
        
        print("Start to login\n", flush=True)

        print("\nPlease wait.", end="", flush=True)
        successLogin = False
        LoginTurn = 1

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
            print(".", end="", flush=True)
            time.sleep(1)
            try:
                driver.find_element_by_xpath(
                    '//*[@id="xsxkapp"]/div[4]/div/div[2]/div/table/tbody/tr['+str(elecTurn)+']/td/div/div/div[6]/div[2]/label/span[1]/span').click()
                successLogin = True
            except Exception as eLogin:
                successLogin = False
                print(".", end="", flush=True)
                LoginTurn = LoginTurn + 1
                time.sleep(1)

        time.sleep(1)
        
        print(".", end="", flush=True)

        time.sleep(1)
        driver.find_element_by_xpath(
           '//*[@id="xsxkapp"]/div[4]/div/div[3]/span/button[1]').click()
        print(".", end="", flush=True)

        time.sleep(1)
        driver.find_element_by_xpath(
            '//*[@id="stundentinfoDiv"]/button').click()
        print(".", end="", flush=True)

        time.sleep(2)
        print(".\n\n", flush=True)

        checkUrl = driver.current_url
        print("\n"+checkUrl+"\n", flush=True)
        if not checkUrl.startswith("https://newxk.urp.seu.edu.cn/xsxk/elective/"):
            print('Login failed', flush=True)
            error = True
            return

        print("Login successfully!\n", flush=True)
        return

    except Exception as e:
        print('\tLogin failed', flush=True)
        error = True
        return


def main():
    try:
        print("Searching...", end="", flush=True)

        while len(classes_wanted) > 0:  # Continue as long as classes_wanted is not empty
            curpages = 1  # Start from the first page
            total_pages = driver.find_element_by_class_name('number.active').text  # Assume first page is loaded, get total pages

            # Start looping through pages
            while curpages <= int(total_pages):
                driver.find_element_by_xpath('//*[@id="xsxkapp"]/div/div[1]/ul/li[1]/i').click()
                time.sleep(0.5)
                print(".", end="", flush=True)
                driver.find_element_by_xpath('//*[@id="xsxkapp"]/div/div[1]/ul/li[2]').click()
                time.sleep(1)
                print(".", end="", flush=True)

                # Jump to current page
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

                # Iterate through all classes on the page
                class_list = driver.find_elements_by_xpath(
                    '//*[@id="xsxkapp"]/div/div[3]/div[3]/div/div[1]/div')
                for cl in class_list:
                    class_num = cl.find_element_by_xpath(
                        './/*[@class="el-card__body"]/div[2]/div/div[2]/span').text
                    print(".", end="", flush=True)

                    # Iterate through classes_wanted array and check if the class number is in the array
                    for class_wanted in classes_wanted:
                        if class_wanted[0:-5] == class_num:  # Match class number
                            cl.click()
                            time.sleep(0.2)
                            print(".", end="", flush=True)
                            teacher_list = cl.find_elements_by_xpath(
                                './/*[@class="card-list course-jxb el-row"]/div')

                            for tl in teacher_list:
                                print(".", end="", flush=True)
                                teacher_num = tl.find_element_by_xpath(
                                    './/*[@class="card-item head"]/div[1]/span[1]').text
                                if class_wanted[-3:-1] == teacher_num[1:3]:  # Match teacher number
                                    print("\n\nClass found\n", flush=True)

                                    # Try to select the class once
                                    try:
                                        tl.find_element_by_xpath('.//*[@class="el-row"]/button[2]').click()
                                        time.sleep(0.5)

                                        # Check if the confirmation dialog appears
                                        msgText = driver.find_element_by_xpath('/html/body/div[3]/div/div[2]/div[1]/div[2]/p').text
                                        if "确认选择课程吗？" in msgText:
                                            driver.find_element_by_xpath(
                                                '/html/body/div[3]/div/div[3]/button[2]').click()
                                            print(f"\nClass successfully selected: {class_wanted}\n", flush=True)
                                            classes_wanted.remove(class_wanted)  # Remove successfully selected class from the array
                                        else:
                                            print(f"\nClass selection failed: {class_wanted}\n", flush=True)

                                    except Exception as eTmp:
                                        print(f"\nAn error occurred while selecting the class: {eTmp}\n", flush=True)

                                    break  # Stop trying other teachers on the current page
                            break  # Stop trying other class numbers

                # Go to the next page
                curpages += 1

            # If after going through all pages there are still classes left, start again from the first page
            print(f"\nClasses not yet selected: {classes_wanted}\n", flush=True)
            if len(classes_wanted) > 0:
                print(f"\nRestarting from the first page, some classes are still unselected.\n", flush=True)
            else:
                print(f"\nAll classes successfully selected, exiting program.\n", flush=True)
                break

    except Exception as e:
        print(f"\nError occurred: {e}", flush=True)
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
