# This is the main script that calls in the FIFA_Web_Scraper and Animation_Frame_Builder
#  scripts to build, display, and save the animation as a .gif file.


# Import Libraries
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import Animation_Frame_Builder as grapher


# main entry point to run the FIFA_Web_Scraper and Animation_Frame_Builder scripts to
#  build, display, and save the animation as a .gif file.
if __name__ == '__main__':
    animator = grapher.animator
    plt.show()

    # Save the animation as a .gif file
    Writer = animation.PillowWriter(fps=1.6)
    animator.save('/Users/sulemanbazai/PycharmProjects/FIFA World Cup Data/goal_animation.gif', writer=Writer)
