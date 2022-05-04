from datetime import datetime, date
import io
import re
from matplotlib import pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import base64


def current_time() -> str:
    return datetime.now().strftime("%B %d, %Y at %H:%M:%S")

def parse_pasted_wordle(text):
    split_text = text.split('\n')
    match = re.search(r'Wordle (?P<day>\d{1,4}) (?P<guesses>[123456X])/6', split_text[0])
    
    if match is not None:
        return {
            'day': match.group('day'),
            'guesses': match.group('guesses'),
            'grid': '\n'.join(split_text[2:])
        }
    else:
        return None

def todays_wordle():
    today = date.today()
    wordle_300 = date(2022, 4, 15)
    return 300 + (today - wordle_300).days

def generate_figure(wordles):
    all_guesses = []
    buffer = 0.4 # mimic actual wordle stat page, bars with 0 count should have width > 0

    # load data
    for wordle in wordles:
        all_guesses.append(wordle.guesses)

    data = {
        '1': buffer,
        '2': buffer,
        '3': buffer,
        '4': buffer,
        '5': buffer,
        '6': buffer,
        'X': buffer
    }
    for g in all_guesses:
        data[g] = data.get(g, 0) + 1
        
    guesses, counts = zip(*data.items())

    # make figure
    fig = plt.figure(figsize=(7, 4))

    # barplot
    bars = plt.barh(guesses, counts, color='#538d4e', height=0.6)
    bars[-1].set_color('#e03f3f')
    plt.gca().invert_yaxis()

    # ticks
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.gca().tick_params(axis=u'both', which=u'both',length=0, pad=15)
    plt.gca().tick_params(axis='x', labelsize=0)

    for label in plt.gca().get_yticklabels(): # guess tick labels
        label.set_fontweight("bold")
        label.set_color("gray")

    # bar labels
    rects = plt.gca().patches
    widest = max([r.get_width() - buffer for r in rects])

    for rect in rects:
        width = rect.get_width()
        label = int(width)
        offset = (1.01 ** widest) - 1

        if (widest - width) / widest < 0.95: # freq can go inside bar
            plt.gca().text(
                width - offset, 
                rect.get_y() + rect.get_height() / 2, 
                label, 
                ha="right", 
                va="center",
                color="white",
                fontsize=14,
                fontweight="bold"
            )
        else: # bar too narrow, freq goes on right of bar
            plt.gca().text(
                width + offset, 
                rect.get_y() + rect.get_height() / 2, 
                label, 
                ha="left", 
                va="center",
                color="gray",
                fontsize=14,
                fontweight="bold"
            )

    plt.gca().margins(x=0.1)
    plt.setp(plt.gca().spines.values(), color='white')
    plt.title("Guess Distribution", fontsize=16)

    # return base64 figure image
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return base64.b64encode(output.getvalue()).decode()