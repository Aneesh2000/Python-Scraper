import time

from selenium import webdriver
import csv
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd

designition= input("Enter designition :")

driver = webdriver.Chrome("C:\\Users\\anees\\Downloads\\chromedriver.exe")  # Optional argument, if not specified will search path.
wait = WebDriverWait(driver, 40)
driver.get("https://www.naukri.com/browse-jobs")


text_area = driver.find_element_by_name('qp')
text_area.send_keys(designition)
text_area.submit()

count = 400
index, new_index, i = '0', 1, 0


time.sleep(5) 

name_xpath= '//*[@id="root"]/div[3]/div[2]/section[2]/div[2]/article['+index+']/div[1]/div[1]/div/a[1]'
#            //*[@id="root"]/div[3]/div[2]/section[2]/div[2]/article[20]/div[1]/div[1]/div/a[1]
title_xpath = '//*[@id="root"]/div[3]/div[2]/section[2]/div[2]/article['+index+']/div[1]/div[1]/a'
#              //*[@id="root"]/div[3]/div[2]/section[2]/div[2]/article[20]/div[1]/div[1]/a
exp_xpath='//*[@id="root"]/div[3]/div[2]/section[2]/div[2]/article['+index+']/div[1]/div[1]/ul/li[1]/span'
#          //*[@id="root"]/div[3]/div[2]/section[2]/div[2]/article[20]/div[1]/div[1]/ul/li[1]/span
salary_xpath='//*[@id="root"]/div[3]/div[2]/section[2]/div[2]/article['+index+']/div[1]/div[1]/ul/li[2]/span'
#             //*[@id="root"]/div[3]/div[2]/section[2]/div[2]/article[20]/div[1]/div[1]/ul/li[2]/span
location_xpath='//*[@id="root"]/div[3]/div[2]/section[2]/div[2]/article['+index+']/div[1]/div[1]/ul/li[3]/span'
#               //*[@id="root"]/div[3]/div[2]/section[2]/div[2]/article[20]/div[1]/div[1]/ul/li[3]/span
skills_xpath='//*[@id="root"]/div[3]/div[2]/section[2]/div[2]/article['+index+']/ul'
#             //*[@id="root"]/div[3]/div[2]/section[2]/div[2]/article[20]/ul


csv_file = open('Naukri_scrape.csv', 'a', encoding="utf-8", newline='')
csv_writer = csv.writer(csv_file)

time.sleep(10)
#wait.until()

# action = webdriver.ActionChains(driver)
# element = wait.until(driver.find_element_by_id("_qej4k1g2sDrawer"))
# action.move_to_element(element)

# driver.find_element_by_class_name("crossIcon chatBot chatBot-ic-cross").click()
driver.refresh()



csv_writer.writerow(['Company Name','Title','Experience','Salary','Location','Skills'])


while i < count:
    
    for j in range(20):
        
        
        temp_index = str(new_index).zfill(2)
        name_xpath= name_xpath.replace(index,temp_index)
        title_xpath = title_xpath.replace(index,temp_index)
        exp_xpath = exp_xpath.replace(index,temp_index)
        salary_xpath = salary_xpath.replace(index,temp_index)
        location_xpath = location_xpath.replace(index,temp_index)
        skills_xpath = skills_xpath.replace(index,temp_index)
        index = str(new_index).zfill(2)
        
        
        try:
            # Capturing the Heading from webpage and storing that into Heading variable.
            name = wait.until(EC.presence_of_element_located((By.XPATH, name_xpath))).text
            print(name)
        except:
            name = "NULL"

        try:
            title = wait.until(EC.presence_of_element_located((By.XPATH, title_xpath))).text
            print(title)
        except:
            title = "NULL"

        try:
            exp = wait.until(EC.presence_of_element_located((By.XPATH, exp_xpath))).text
            print(exp)
        except:
            exp = "NULL"
            
        try:
            salary = wait.until(EC.presence_of_element_located((By.XPATH, salary_xpath))).text
            print(salary)
        except:
            salary = "NULL"
            
        try:
            location = wait.until(EC.presence_of_element_located((By.XPATH, location_xpath))).text
            print(location)
        except:
            location = "NULL"
            
        try:
            skills = wait.until(EC.presence_of_element_located((By.XPATH, skills_xpath))).text
            #skills = ','.join([line.splitlines() for line in skills])
            skills= ','.join(skills.splitlines())
            print(skills)
        except:
            skills = "NULL"
          
        new_index += 1  
        i += 1
        print("--------------------------- "+str(i)+" ----------------------------------")           
        csv_writer.writerow([name,title,exp,salary,location,skills])  
        if i >= count:
            break
    if i >= count:
        break
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div[3]/div[2]/section[2]/div[3]/a[2]'))).click()
    new_index = 1
      
        
csv_file.close()                
time.sleep(5) # Let the user actually see something!

driver.quit()


df = pd.read_csv("Naukri_scrape.csv")
#print(df['Skills'])

list1=[]

for i in range(400):
    list2=(df['Skills'][i].split(','))
    list1+= list2
    
#print(list1)
df1 = pd.DataFrame(list1,columns=['skills'])
df2 = df1.value_counts().rename_axis('key skills').reset_index(name='Freq')
#print(df1['skills'].value_counts())
df2.head()
df2.to_csv('SkillFreq.csv')