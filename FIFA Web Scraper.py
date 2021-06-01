# This Python Script is used to scrape World Cup data from https://www.fifa.com/worldcup/


# Import Libraries
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import re
import pandas as pd
import copy


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
####CODE FROM SCRATCH GOES BACK HERE#####
score_dict = {}
for i in range(len(grouped_match_list)):
    score_team1 = grouped_match_list[i][1][0]
    try:
        score_dict[grouped_match_list[i][0]].append(int(score_dict[grouped_match_list[i][0]][-1]) + int(score_team1))
    except:
        score_dict[grouped_match_list[i][0]] = [int(score_team1)]

    score_team2 = grouped_match_list[i][1][-1]
    try:
        score_dict[grouped_match_list[i][2]].append(int(score_dict[grouped_match_list[i][2]][-1]) + int(score_team2))
    except:
        score_dict[grouped_match_list[i][2]] = [int(score_team2)]

#print(df1)

max_key, max_value = max(score_dict.items(), key = lambda x: len(set(x[1])))
max_match = copy.copy(max_value)
for key in score_dict:
    while len(score_dict[key]) < len(max_match):
        score_dict[key].append(score_dict[key][-1])
    if len(score_dict[key]) < len(max_match)+1:
        score_dict[key].insert(0,0)


print(score_dict)

df = pd.DataFrame(columns=['Team Name', 'Score', 'Match Index'])
for key in score_dict:
    for i in range(len(max_value)):
        df2 = pd.DataFrame([[key, score_dict[key][i], i]], columns=['Team Name', 'Score', 'Match Index'])
        df = df.append(df2)

print(df)
import plotly.express as px

fig = px.bar(df, x="Score", y="Team Name", color="Team Name",orientation='h',category_orders=df['Score'],
  animation_frame="Match Index", animation_group="Team Name", range_x=[0,20])
fig.show()







import bar_chart_race as bcr

df1 = pd.DataFrame.from_dict(score_dict)

print(df1)
bcr.bar_chart_race(df = df1, n_bars = 10,period_length=1200,
                    filter_column_colors=True,
                   sort='desc',title='2018 FIFA World Cup Goals by Country',
                   filename = r'/Users/sulemanbazai/PycharmProjects/FIFA World Cup Data/test.mp4')
