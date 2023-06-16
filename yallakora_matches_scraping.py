import requests
from bs4 import BeautifulSoup
import csv
import lxml

# step one creating the GUI and get the inputs
import PySimpleGUI as sg

# Define the layout of the GUI
layout = [
    [sg.Text("Enter the Day           :"), sg.Input(key="-STRING1-")],
    [sg.Text("Enter the month        :"), sg.Input(key="-STRING2-")],
    [sg.Text("Enter the Directory    :"), sg.Input(key="-STRING3-")],
    [sg.Button("Submit")]
]

# Create a window with the layout
window = sg.Window("YallaKora Matches", layout)

# Start an event loop
while True:
    # Read the events and values from the window
    event, values = window.read()
    # If the user closes the window or clicks Submit, break the loop
    if event in (sg.WIN_CLOSED, "Submit"):
        break

# Get the input from the values dictionary
day = int(values["-STRING1-"])
month = int(values["-STRING2-"])
directory = values["-STRING3-"]
# Close the window
window.close()

date = f"{month}/{day}/2023"
modified_directory = directory.replace("\\", "/")
page = requests.get(
    f"https://www.yallakora.com/match-center/%D9%85%D8%B1%D9%83%D8%B2-%D8%A7%D9%84%D9%85%D8%A8%D8%A7%D8%B1%D9%8A%D8%A7%D8%AA?date={date}#days")


def main(page):
    source = page.content
    soup = BeautifulSoup(source, "lxml")
    matches_details = []

    champion = soup.find_all("div", {"class": "matchCard"})

    def get_match_info(champion):
        champion_title = champion.find('h2').text.strip()
        all_matches = champion.contents[3].find_all('li')
        number_of_matches = len(all_matches)

        for i in range(number_of_matches):
            # get names of the teams
            team_a = all_matches[i].find("div", {'class': 'teams teamA'}).text.strip()
            team_b = all_matches[i].find("div", {'class': 'teams teamB'}).text.strip()

            # get score
            match_result = all_matches[i].find('div', {'class': "MResult"}).find_all('span', {'class': 'score'})
            score = f"{match_result[0].text.strip()} -:-  {match_result[1].text.strip()}"

            # get match time
            match_time = all_matches[i].find('div', {'class': "MResult"}).find('span', {'class': "time"}).text.strip()

            # add match info

            matches_details.append({"نوع البطولة": champion_title, "الفريق الاول": team_a, "الفريق الثاني": team_b,
                                    "ميعاد المباراة": match_time, "النتيجة": score})

    for i in range(len(champion)):
        get_match_info(champion[i])

    # create a csv file
    keys_ot_table = matches_details[0].keys()

    with open(f"{modified_directory}/matches{day}-{month}-2023.csv", "w", encoding='utf-8-sig') as output_file:
        dic_writer = csv.DictWriter(output_file, keys_ot_table)
        dic_writer.writeheader()
        dic_writer.writerows(matches_details)
        print("file created")


main(page)

