# FIFA World Cup Data Scraper and Bar Chart Race
The FIFA World Cup Data Scraper and Bar Chart Race is a project for automating the collection of FIFA world cup score data in order to create an animation displaying the top team scores, match by match.

## Usage
```python
FIFA_Web_Scraper.py # used to scrape World Cup data from https://www.fifa.com/worldcup/

Animation_Frame_Builder.py # used to create the animation of scores obtained in the data scraper

main.py # main script that calls in the FIFA_Web_Scraper and Animation_Frame_Builder scripts to build, display, and save the animation as a .gif file
```

## Libraries
BeautifulSoup used for parsing through the HTML returned from the FIFA website.<br />
re used for performing regular expression matching operations.<br />
pandas used for creating the DataFrame holding the score data.<br />
matplotlib used for creating the animated bar chart race visualization.
