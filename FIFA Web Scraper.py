# This Python Script is used to scrape World Cup data from https://www.fifa.com/worldcup/


# Import Libraries
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import re


# Set URL, open and read the html page, and create the BeautifulSoup object.
url = "https://www.fifa.com/worldcup/archive/russia2018/matches/"
req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
page = urlopen(req)
html = page.read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")


# Set up the team_list list that contains all the team names.
team_list = ['Australia','IR Iran','Japan','Saudi Arabia','Korea Republic','Egypt','Morocco','Nigeria',
             'Senegal','Tunisia','Mexico','Costa Rica','Panama','Argentina','Brazil','Colombia',
             'Peru','Uruguay','Belgium','Croatia','Denmark','England','France','Germany',
             'Iceland','Poland','Portugal','Russia','Serbia','Spain','Sweden','Switzerland']

# Use the getText() function from the bs4 library to convert the BeautifulSoup object to a string.
all_text = soup.getText()


# Set up the game lists.

# score_list is a list that will contain the score for the match.
score_list = []
# paren is the pattern that we will be using to make sure we do not pull penalty kick scores, since
#  penalty kick score from the website are in parentheses - example: (3-4) meaning second team wins in PKs.
paren = re.compile("\([0-9]-[0-9]\)")

# first_team_list is a list that will contain the team name for the first number in the score.
first_team_list = []

# second_team_list is a list that will contain the team name for the second number in the score.
second_team_list = []


# Loop through the all_text variable to build the score_list, first_team_list and
# second_team_list game lists. This is done using search() and finditer() from the re module.
# First, we loop through to find the score pattern "#-#" in all_text.
for score_match in re.finditer("[0-9]-[0-9]", all_text):
    s = score_match.start()-40
    e = score_match.end()

    # If the found score pattern does not have parentheses surrounding it, then the score is the
    #  actual score. If parentheses are found, then the score pattern is for the penalty shootout,
    #  which we do not want to keep as a score.
    if paren.search(all_text[s+39:e+1]) is None:
        score_list.append(all_text[s+40:e])

    # Next, we loop through 40 characters before the found score pattern up until the pattern in order to
    #  find the pattern which matches a team name in the team_list list, and append to first_team_list.
    for team1 in re.finditer(".*", all_text[s:e]):
        s2 = team1.start()
        e2 = team1.end()
        if all_text[s:e][s2:e2] in team_list:
            first_team_list.append(all_text[s:e][s2:e2])

    # Finally, we do a similar loop from the end of the found score pattern up until 40 characters after
    #  the found score pattern in order to find the second team in the match to append to second_team_list.
    for team2 in re.finditer(".*", all_text[e:e+40]):
        s3 = team2.start()
        e3 = team2.end()
        if all_text[e:e+40][s3:e3] in team_list:
            second_team_list.append(all_text[e:e+40][s3:e3])


# Loop through the score_list, first_team_list and second_team_list to create a grouped match list.
# This list will have the format [[first team match 1, score match 1, second team match 1],..[]..].
grouped_match_list = []
for i in range(len(score_list)):
    grouped_match_list.append([first_team_list[i], score_list[i], second_team_list[i]])

print(grouped_match_list)