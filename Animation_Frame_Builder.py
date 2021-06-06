import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.animation as animation
import numpy as np
from IPython.display import HTML
import random
import FIFA_Web_Scraper as scraper


def map_colors(team_list, df):
    r_min = 90
    r_max = 245
    g_min = 90
    g_max = 245
    b_min = 90
    b_max = 245
    colors = dict()

    for key in team_list:
        red = random.randint(r_min, r_max)
        green = random.randint(g_min, g_max)
        blue = random.randint(b_min, b_max)
        rgb_string = (red, green, blue)
        colors[key] = '#%02x%02x%02x' % rgb_string

    return colors


def draw_barchart(index):
    dff = df[df['Index'].eq(index)].sort_values(by='Score', ascending=True).tail(10)
    ax.clear()
    if index > 0:
        ax.barh(dff['Name'], dff['Score'], color=[colors[x] for x in dff['Name']])
        #dx = dff['Score'].max() / 2
        for i, (value, name) in enumerate(zip(dff['Score'], dff['Name'])):
            ax.text(value, i,     name, size=8, weight=525, ha='right', va='center')
            #ax.text(value - dx, i- .25, group_lk[name], size=40, color='#444444', ha='right', va='baseline')
            ax.text(value, i, f'{value:,.0f}', size=8, ha='left', va='center')
    # ... polished styles
    current_round = ''
    current_worldcup = ''

    # Set the correct round to display in the graph
    if (index % 7 == 1) and (index != 0):
        current_round = 'Group Stage'
    if (index % 7 == 2) and (index != 0):
        current_round = 'Group Stage'
    if (index % 7 == 3) and (index != 0):
        current_round = 'Group Stage'
    if (index % 7 == 4) and (index != 0):
        current_round = 'Round of 16'
    if (index % 7 == 5) and (index != 0):
        current_round = 'Quarter-finals'
    if (index % 7 == 6) and (index != 0):
        current_round = 'Semi-finals'
    if (index % 7 == 0) and (index != 0):
        current_round = 'Finals'

    # Set the correct World Cup to display in the graph
    if index > 0:
        current_worldcup = str(int(4*np.floor((index / 7) - .01)) + int(first_worldcup))

    ax.text(1, 0.15, current_round+" "+current_worldcup, transform=ax.transAxes, color='#777777', size=9, ha='right', weight=800)
    ax.text(0, 1.06, 'Goals', transform=ax.transAxes, size=6, color='#777777')
    ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
    ax.xaxis.set_ticks_position('top')
    ax.tick_params(axis='x', colors='#777777', labelsize=6)
    ax.set_yticks([])
    ax.margins(0, .01)
    ax.grid(which='major', axis='x', linestyle='-')
    ax.set_axisbelow(True)
    ax.text(0, 1.10, 'FIFA World Cup Goals by Country '+str(first_worldcup)+' - '+last_worldcup,
            transform=ax.transAxes, size=11, weight=550, ha='left')
    ax.text(1, 0, 'by Suleman Bazai', transform=ax.transAxes, ha='right',
            color='#777777', bbox=dict(facecolor='white', alpha=0.8, edgecolor='white'))
    plt.box(False)


first_worldcup = scraper.url_list[0][-13:-9]
last_worldcup = scraper.url_list[-1][-13:-9]
team_list = scraper.team_list
df = scraper.df
max_match = len(scraper.score_dict[team_list[0]])
colors = map_colors(team_list, df)
fig, ax = plt.subplots(figsize=(7, 4.5))
animator = animation.FuncAnimation(fig, draw_barchart, frames=range(0, max_match),
                                   interval=600, repeat=False)
plt.show()

# Save the animation as a .gif file
Writer = animation.PillowWriter(fps=1.6)
animator.save('/Users/sulemanbazai/PycharmProjects/FIFA World Cup Data/goal_animation.gif', writer=Writer)