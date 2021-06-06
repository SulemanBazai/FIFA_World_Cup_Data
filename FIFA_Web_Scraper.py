# This Python Script is used to scrape World Cup data from https://www.fifa.com/worldcup/


# Import Libraries
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import re
import pandas as pd
import copy


# Set URL list
url_list = ["https://www.fifa.com/worldcup/archive/koreajapan2002/matches/",
            "https://www.fifa.com/worldcup/archive/germany2006/matches/",
            "https://www.fifa.com/worldcup/archive/southafrica2010/matches/",
            "https://www.fifa.com/worldcup/archive/brazil2014/matches/",
            "https://www.fifa.com/worldcup/archive/russia2018/matches/"]

# Set up the team_list list that contains all the team names.
team_list = ['Belgium','France','Brazil','England','Portugal','Spain','Italy',
                 'Argentina','Uruguay','Denmark','Mexico','Germany','Switzerland',
                 'Croatia','Colombia','Netherlands','Wales','Sweden','Chile','USA',
                 'Poland','Senegal','Austria','Ukraine','Serbia','Tunisia','Peru','Japan',
                 'Turkey','Venezuela','IR Iran','Nigeria','Algeria','Morocco','Paraguay',
                 'Slovakia','Hungary','Russia','Korea Republic','Czech Republic','Australia',
                 'Norway','Romania','Scotland','Jamaica','Egypt','Republic of Ireland',
                 'Northern Ireland','Ghana','Costa Rica','Greece','Iceland','Ecuador',
                 'Finland','Cameroon','Bosnia and Herzegovina','Mali','Qatar',"Côte d'Ivoire",
                 'Burkina Faso','Congo DR','North Macedonia','Slovenia','Montenegro',
                 'Saudi Arabia','Albania','Honduras','Iraq','El Salvador','Canada','Bulgaria',
                 'Guinea','United Arab Emirates','Cabo Verde','South Africa','Curaçao',
                 'China PR','Panama','Syria','Oman','Bolivia','Benin','Haiti','Uganda','Israel',
                 'Uzbekistan','Zambia','Gabon','Belarus','Armenia','Georgia','Vietnam','Lebanon',
                 'Congo','Jordan','Luxembourg','Cyprus','Bahrain','Kyrgyz Republic','Madagascar',
                 'Mauritania','Kenya','Trinidad and Tobago','Palestine','India','Thailand',
                 'Zimbabwe','Guinea-Bissau','Korea DPR','Azerbaijan','Namibia','Niger',
                 'Faroe Islands','Sierra Leone','Malawi','Estonia','Mozambique',
                 'Central African Republic','Libya','Kosovo','Tajikistan','New Zealand','Sudan',
                 'Kazakhstan','Philippines','Angola','Guatemala','Antigua and Barbuda','Rwanda',
                 'Turkmenistan','Comoros','Equatorial Guinea','Togo','Lithuania',
                 'St. Kitts and Nevis','Suriname','Tanzania','Latvia','Myanmar','Ethiopia',
                 'Chinese Taipei','Burundi','Solomon Islands','Hong Kong','Yemen',
                 'Lesotho','Nicaragua','Kuwait','Afghanistan','Botswana']


# score_dict is the dictionary used to build the pandas dataframe used to make the animation graph.
score_dict = {}

# The first value for each team should be 0 since no games have been played, and no goals scored yet.
for team in team_list:
    score_dict[team] = [0]

# url_count keeps track of which count of url we are processing - 1 is first, 2 is second, etc.
url_count = 0

# Loop through the URLs to open and read the html page, and create the BeautifulSoup object "soup".
for url in url_list:
    url_count += 1

    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    page = urlopen(req)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")

    # Use the getText() function from the bs4 library to convert the BeautifulSoup object to a string.
    all_text = soup.getText()
    # print(all_text)

    # paren is the pattern that we will be using to make sure we do not pull penalty kick scores,
    #  since penalty kick scores from the website are in parentheses.
    # Example: (3-4) meaning second team wins in PKs.
    paren = re.compile("\([0-9]-[0-9]\)")

    # Loop through the all_text variable to find the score and team names for each match.
    # This is done using search() and finditer() from the re module.

    # match_count keeps track of which count of match in the URL we are processing.
    # For example, 1 is the first match, 2 is second, etc. There are 64 matches in a World Cup.
    # A team reaching the finals will have played 7 total games when the World Cup has finished.
    # Because of this, each team (regardless of whether they were in the World Cup or not, and
    #  regardless of whether they made it to the finals) will need 7 data points for their score
    #   per World Cup. This is to ensure the graphing animation works appropriately.
    # There will also be a score of 0 in the first spot for each team since this is before the first
    #  World Cup match has been played for the first World Cup in the graph animation.
    match_count = 0

    # First, we loop through to find the score pattern "#-#" in all_text.
    for score_match in re.finditer("[0-9]-[0-9]", all_text):
        s = score_match.start() - 45
        e = score_match.end()
        found1 = 0
        found2 = 0
        trigger = 0

        # If the found score pattern does not have parentheses surrounding it, then the score is the
        #  actual score. If parentheses are found, then the score pattern is for the penalty shootout,
        #   which we do not want to keep as a score.
        if paren.search(all_text[s + 44:e + 1]) is None:
            score = all_text[s + 45:e]
            team1_score = score.split("-")[0]
            team2_score = score.split("-")[1]
            match_count += 1

            # The score is valid, so we also need the team names.

            # To do this we loop through 45 characters before the found score pattern up until
            #  the pattern in order to find the pattern which matches a team name
            #   in the team_list list, and append to first_team_list.
            for team1_iter in re.finditer(".*", all_text[s:e]):
                s2 = team1_iter.start()
                e2 = team1_iter.end()
                if (all_text[s:e][s2:e2] in team_list) and (found1 != 1):
                    team1 = all_text[s:e][s2:e2]
                    found1 = 1

            # Finally, we do a similar loop from the end of the found score pattern up until
            #  45 characters afterthe found score pattern in order to find the second team
            #   in the match to append to second_team_list.
            for team2_iter in re.finditer(".*", all_text[e:e + 45]):
                s3 = team2_iter.start()
                e3 = team2_iter.end()
                if (all_text[e:e + 45][s3:e3] in team_list) and (found2 != 1):
                    team2 = all_text[e:e + 45][s3:e3]
                    found2 = 1

        # print(team1,team1_score,"    ",team2_score,team2)

        # Break out of current match loop since the score returned was not valid.
        # This score was most likely a penalty score case with (#-#)
        else:
            trigger = 1

        # Append the score of the team to the correct key in score_dict. The latest value in the
        #  dictionary list should be the previous match scores total + the new match score.
        if trigger != 1:
            score_dict[team1].append(int(team1_score) + score_dict[team1][-1])
            score_dict[team2].append(int(team2_score) + score_dict[team2][-1])

    # Loop through the score dictionary that will be building the dataframe. This is to add a 0 score
    #  for when a team does not play in a match.
    for key in score_dict:
        try:
            if score_dict[key][url_count*7] == "":
                print("yes")
                while len(score_dict[key]) != ((url_count * 7) + 1):
                    score_dict[key].append(score_dict[key][-1])
        except IndexError:
            while len(score_dict[key]) != ((url_count * 7) + 1):
                score_dict[key].append(score_dict[key][-1])

print(score_dict)

df = pd.DataFrame(columns=['Name', 'Score', 'Index'])
for key in score_dict:
    for i in range(len(score_dict[key])):
        df2 = pd.DataFrame([[key, score_dict[key][i], i]], columns=['Name', 'Score', 'Index'])
        df = df.append(df2)

print(df)
