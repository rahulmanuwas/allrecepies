from bs4 import BeautifulSoup
import requests
import sqlite3
import csv

url_base = "http://allrecipes.com/recipe/"

i = 0

# open csv
with open('allrecepies.csv','w') as fp:
    write_in_csv = csv.writer(fp, delimiter=',')
    csv_header = ["URL", "Name", "Ingredients", "Preparation Time", "Cooking Time", "Ready In", "Directions"]
    write_in_csv.writerow(csv_header)
                 
    for i in range(20):

        data_list = []
        # Request Data from URL 
        url = url_base + str(17680 + i).replace("\n", "")
        r = requests.get(url)
        r.raise_for_status()
        soup = BeautifulSoup(r.content,'html.parser')
        #print (soup.prettify())


        # Process HTML

        # Name of the Receipe
        receipe_name_html = soup.find_all("h1", {"class" : "recipe-summary__h1"})
        receipe_name = receipe_name_html[0].text.replace("\n", "")
        print (receipe_name)

        # ETA and Energy          
        # receipe_time = soup.find_all("span", {"class" : "recipe-ingredients__header__toggles"})
        # print (receipe_time)

        # Ingredients

        receipe_ingredients = soup.find_all("li", {"class" : "checkList__line"})
        receipe_ingredients_list = []
        for ingredients in receipe_ingredients:
            try:
                ingredient = ingredients.find_all("span", {"class" : "recipe-ingred_txt added"})
                print (ingredient[0].text.replace("\n", ""))
                receipe_ingredients_list.append(ingredient[0].text.replace("\n", ""))
            except:
                pass


        # Directions

        directions = soup.find_all("div", {"class" : "directions--section"}) 

        try:
            prep_time = directions[0].find_all("li", {"class" : "prepTime__item"})
            preparation_time = prep_time[1].text.replace("\n", "").replace("Prep","")
            cooking_time = prep_time[2].text.replace("\n", "").replace("Cook","")
            ready_in = prep_time[3].text.replace("\n", "").replace("Ready In","")

            print(preparation_time, cooking_time,  ready_in)
        except:
            pass
        steps = directions[0].find_all("span", {"class" : "recipe-directions__list--item"})
        steps_list = []
        for step in steps:
            try:
                print (step.text.replace("\n",""))
                steps_list.append(step.text.replace("\n",""))
            except:
                pass

        try:
            data_list.append(url)
            data_list.append(receipe_name)
            data_list.append(receipe_ingredients_list)
            data_list.append(preparation_time)
            data_list.append(cooking_time)
            data_list.append(ready_in)
            data_list.append(steps_list)
            print (data_list)
            write_in_csv.writerow(data_list)
        except:
            print ("Error while appending")
            pass

fp.close()
