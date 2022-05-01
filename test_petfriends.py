import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(autouse=True)
def testing():
   # get webdriver and arguments
   pytest.driver = webdriver.Chrome('/home/dmk/Tests/chromedriver')
   pytest.driver.set_window_size(1024, 600)
   pytest.driver.maximize_window()
   # go to login page
   pytest.driver.get('http://petfriends1.herokuapp.com/login')
   # input email
   pytest.driver.find_element_by_id('email').send_keys('kevopo8078@sofrge.com')
   # input password
   pytest.driver.find_element_by_id('pass').send_keys('ara157lima')
   # press login button
   pytest.driver.find_element_by_css_selector('button[type="submit"]').click()
   # testing main page presence
   assert pytest.driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

   yield
   pytest.driver.quit()

def test_my_pets():
   # implicit wait
   pytest.driver.implicitly_wait(10)
   # get pet card info
   images = pytest.driver.find_elements_by_css_selector('.card-deck .card-img-top')
   names = pytest.driver.find_elements_by_css_selector('.card-deck .card-tittle')
   descriptions = pytest.driver.find_elements_by_css_selector('.card-deck .card-text')
   # testing pet card info
   for i in range(len(names)):
      assert images[i].get_attribute('src') != ''
      assert names[i].text != ''
      assert descriptions[i].text != ''
      assert ', ' in descriptions[i]
      parts = descriptions[i].text.split(", ")
      assert len(parts[0]) > 0
      assert len(parts[1]) > 0
        
        
def test_number_my_pets():
   # press button "Мои питомцы"
   WebDriverWait(pytest.driver, 10).until(
      EC.presence_of_element_located((By.CSS_SELECTOR, 'a.nav-link[href="/my_pets"]'))
      )
   pytest.driver.find_element_by_css_selector('a.nav-link[href="/my_pets"]').click()
   # testing my pets page presence
   assert pytest.driver.current_url == 'http://petfriends1.herokuapp.com/my_pets'
   # get count of my pets with explicit wait
   element = WebDriverWait(pytest.driver, 10).until(
      EC.presence_of_element_located((By.CSS_SELECTOR, ".\\.col-sm-4.left")))
   
   my_pets = (pytest.driver.find_element_by_xpath('/html/body/div[1]/div/div[1]').text).split()
  
   # get my pets names with explicit wait
   names = pytest.driver.find_elements_by_xpath('//*[@id="all_my_pets"]/table/tbody/tr/td[1]')
   
   # testing my pets presence
   assert int(my_pets[2]) == len(names)
   
   
   # get my pets photos
   images = pytest.driver.find_elements_by_xpath('//*[@id="all_my_pets"]//img')
   images_lst = []
   for i in range(len(images)):
      if images[i].get_attribute('src') != '':
         images_lst.append(images[i])

   # testing that at least half of the pets have a photo
   assert len(images_lst) >= int(my_pets[2]) / 2
   
   # checking all pets have a name, age and breed
   # checking names
   names_all_lst = []
   names_with_lst = []
   for i in range(len(names)):
      names_all_lst.append(names[i].text)
      if names[i].text != '':
         names_with_lst.append(names[i].text)
   
   # get breeds
   breeds = pytest.driver.find_elements_by_xpath('//*[@id="all_my_pets"]/table/tbody/tr/td[2]')
   # checking breeds
   breeds_all_lst = []
   breeds_with_lst = []
   for i in range(len(breeds)):
      breeds_all_lst.append(breeds[i].text)
      if breeds[i].text != '':
         breeds_with_lst.append(breeds[i].text)
   
   # get age
   ages = pytest.driver.find_elements_by_xpath('//*[@id="all_my_pets"]/table/tbody/tr/td[3]')
   # checking ages
   ages_all_lst = []
   ages_with_lst = []
   for i in range(len(ages)):
      ages_all_lst.append(ages[i].text)
      if ages[i].text != '':
         ages_with_lst.append(ages[i].text)
   
   # testing all pets have a name, age and breed    
   assert int(my_pets[2]) == len(names_with_lst) and int(my_pets[2]) == len(breeds_with_lst) and int(my_pets[2]) == len(ages_with_lst)
   
   # checking all pets have different names
   names_same_lst = []
   for i in range(len(names_all_lst)):
      for j in range(i+1, len(names_all_lst)):
         if names_all_lst[i] == names_all_lst[j]:
            names_same_lst.append(names_all_lst[i])
            
   # testing all pets have different names
   assert len(names_same_lst) == 0
   
   # checking no duplicate pets in the list
   # get my pets
   pets = pytest.driver.find_elements_by_xpath('//*[@id="all_my_pets"]/table/tbody/tr')
   pets_all_lst = []
   pets_same_lst = []
   for i in range(len(pets)):
      pets_all_lst.append(pets[i].text)
      
   for i in range(len(pets_all_lst)):
      for j in range(i+1, len(pets_all_lst)):
         if pets_all_lst[i] == pets_all_lst[j]:
            pets_same_lst.append(pets_all_lst[i])
            
   assert len(pets_same_lst) == 0

