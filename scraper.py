# import required packages
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np
import os

############################################################################################################################################################

match_date="2023-07-07" #yyyy-mm-dd
batting_team="LAN"
match_name="LAN vs SUR - 2023-07-07"

############################################################################################################################################################

# Load the CSV file with all the html elements that we created inspecting the webpage
urls = pd.read_csv("Element List/ESPN Cricinfo Element Scraping URLs (LAN vs SUR).csv")
#Filtering data for one innings
urls=urls[urls["Batting Team"]==batting_team]

############################################################################################################################################################

if batting_team=="LAN":
    doc_link="HTML Files/Lancashire vs Surrey - 2023-07-07/Ball by Ball Commentary & Live Score - LANCS vs SUR, 2nd Quarter Final - Lancs Batting.html"
elif batting_team=="SUR":
    doc_link="HTML Files/Lancashire vs Surrey - 2023-07-07/Ball by Ball Commentary & Live Score - LANCS vs SUR, 2nd Quarter Final- Surrey Batting.html"
else:
    print("Wrong Team Name Input")
    exit()

############################################################################################################################################################

# opening html file with BeautifulSoup
with open(doc_link) as fp:
    innings_soup = BeautifulSoup(fp, "html5lib")

# create an empty dataframe for inserting scraped values
ball_df = pd.DataFrame(columns=['ball','score', 'commentary',])
wickets_df = pd.DataFrame(columns=['ball','score', 'commentary','fow'])

# create empty lists for each of the data you want
ball_numbers = list()
ball_score = list()
ball_desc = list()
wicket_des=list()

# get data from div classes and urls

# for ball numbers
for span in innings_soup.findAll('span', {
    
    'class': urls[urls["Field"] == "Over and Ball Numbers"]["Link"].iloc[0]}):
    ball_numbers.append(span.text.strip())  # Extract and clean the text

class_names = [ #Green for 4s, Purple for 6s, Red for W's, Transclucent Else
    
urls[urls["Field"] == "Other Balls"]["Link"].iloc[0],          # Normal Results (White Bg)
urls[urls["Field"] == "4s Balls"]["Link"].iloc[0],             # Boundaries Results (Green Bg)
urls[urls["Field"] == "6s Balls"]["Link"].iloc[0],             # 6s Results (Purple Bg)
urls[urls["Field"] == "Wicket Balls"]["Link"].iloc[0]]         # Wickets Results (Red Bg)

# Iterate over all div elements in the soup
for div in innings_soup.find_all('div',{'class':class_names}):
    span = div.find("span")  # Find the span inside the div containing the score
    if span:
        score = span.text.strip()  # Extract the score text
        ball_score.append(score)


# for description of each ball- Commentary

for div in innings_soup.findAll('div', {'class': urls[urls["Field"] == "Commentary"]["Link"].iloc[0]}):
    ball_desc.append(div.text)


# for fall of wickets

for div in innings_soup.find_all('div', {'class': urls[urls["Field"] == "FoW"]["Link"].iloc[0]}):
    strong = div.find("strong")  # Assuming the score is inside a span
    if strong:
        fow = strong.text.strip()  # Extract the score text
        wicket_des.append(fow)

# save lists in respective dataframe columns
ball_df.ball = ball_numbers
ball_df.score = ball_score
ball_df.commentary = ball_desc

#Adding Description to only Wicket Balls

wickets_df=ball_df[ball_df["commentary"].str.contains("OUT")]
wickets_df["fow"] = wicket_des

file_name_prefix = f"Scraped Data/{match_name}/{match_date}-{batting_team}-"

# Create the directory if it doesn't exist
os.makedirs(os.path.dirname(file_name_prefix), exist_ok=True)

# save dataframe as csv or json
ball_df.to_csv(f"{file_name_prefix}Batting.csv", sep=',', index=False)
ball_df.to_json(f"{file_name_prefix}Batting.json", orient='records')
wickets_df.to_csv(f"{file_name_prefix}FoW.csv", sep=',', index=False)