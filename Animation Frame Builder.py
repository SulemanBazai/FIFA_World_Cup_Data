import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.animation as animation
from IPython.display import HTML
import random
import FIFA_Web_Scraper as scraper


def map_colors(team_list, df):
    r_min = 40
    r_max = 255
    g_min = 40
    g_max = 255
    b_min = 40
    b_max = 255
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
    ax.barh(dff['Name'], dff['Score'], color=[colors[x] for x in dff['Name']])
    #dx = dff['Score'].max() / 2000
    for i, (value, name) in enumerate(zip(dff['Score'], dff['Name'])):
        ax.text(value , i,     name,           size=14, weight=600, ha='right', va='center')
        #ax.text(value , i- .25, name, size=10, color='#444444', ha='right', va='baseline')
        ax.text(value , i, f'{value:,.0f}', size=14, ha='left', va='center')
    # ... polished styles
    ax.text(1, 0.4, index, transform=ax.transAxes, color='#777777', size=46, ha='right', weight=800)
    ax.text(0, 1.06, 'Goals', transform=ax.transAxes, size=12, color='#777777')
    ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
    ax.xaxis.set_ticks_position('top')
    ax.tick_params(axis='x', colors='#777777', labelsize=12)
    ax.set_yticks([])
    ax.margins(0, 0.01)
    ax.grid(which='major', axis='x', linestyle='-')
    ax.set_axisbelow(True)
    ax.text(0, 1.12, '2018 FIFA World Cup Goals by Country',
            transform=ax.transAxes, size=18, weight=600, ha='left')
    ax.text(1, 0, 'by Suleman Bazai', transform=ax.transAxes, ha='right',
            color='#777777', bbox=dict(facecolor='white', alpha=0.8, edgecolor='white'))
    plt.box(False)


team_list = scraper.team_list
df = scraper.df
max_match = len(scraper.score_dict[team_list[0]])#scraper.max_match*len(scraper.url_list)
colors = map_colors(team_list, df)
fig, ax = plt.subplots(figsize=(15, 8))
animator = animation.FuncAnimation(fig, draw_barchart, frames=range(0,max_match),interval=600,repeat=False)
plt.show()