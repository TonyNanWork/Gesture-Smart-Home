from selenium import webdriver
import time


import unittest
import undetected_chromedriver as uc

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By



class HomeController():
    def __init__(self) -> None:


        options = uc.ChromeOptions()
        options.user_data_dir = 'Chrome'

        self.driver = uc.Chrome(options=options)
        self.driver.get("https://home.google.com/home/1-5cb82ee351e34c6928f27d86ed579aa963dfad35126bc80a370644826227cb20/automations")

        time.sleep(5)

        driver = self.driver
        elements = driver.find_elements(By.CLASS_NAME, "automations-container")
        print(len(elements))
        container = elements[1]

        buttonlist = container.find_elements(By.TAG_NAME, 'button')
        print(len(buttonlist))

        self.regular = buttonlist[0]
        self.thatTime = buttonlist[1]
        self.tvOn = buttonlist[2]
        self.tvOff = buttonlist[3]
        self.tvUp = buttonlist[4]
        self.tvDown = buttonlist[5]
    
    def clickRegular(self):
        self.regular.click()

    def clickThatTime(self):
        self.thatTime.click()

    def clickTvOn(self):
        self.tvOn.click()

    def clickTvOff(self):
        self.tvOff.click()

    def clickTvUp(self):
        self.tvUp.click()

    def clickTvDown(self):
        self.tvDown.click()


    def setList(self):
        

        driver = self.driver
        elements = driver.find_elements(By.CLASS_NAME, "automations-container")
        print(len(elements))
        container = elements[1]

        buttonlist = container.find_elements(By.TAG_NAME, 'button')
        print(len(buttonlist))
        return buttonlist



    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    hc = HomeController()
    time.sleep(5)
    hc.setList()
    
    time.sleep(1000)
