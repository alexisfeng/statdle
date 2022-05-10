from datetime import datetime, date
import io
import re
from matplotlib import pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import base64


def current_time() -> str:
    return datetime.now().strftime("%B %d, %Y at %H:%M:%S")

def parse_pasted_wordle(text):
    split_text = text.split("\n")
    split_text = [line for line in split_text if len(line) != 0] # remove empty lines
    match = re.search(r"Wordle (?P<day>\d{1,4}) (?P<guesses>[123456X])/6", split_text[0])
    
    if match is not None:
        # check for invalid grid data
        for line in split_text[1:]:
            if re.search(r"\w+", line) is not None:
                return None

        return {
            "day": match.group("day"),
            "guesses": match.group("guesses"),
            "grid": "\n".join(split_text[1:])
        }
    else:
        return None

def todays_wordle():
    today = date.today()
    wordle_300 = date(2022, 4, 15)
    return 300 + (today - wordle_300).days

def generate_figure(wordles):
    all_guesses = []

    # load data
    for wordle in wordles:
        all_guesses.append(wordle.guesses)

    data = {
        "1": 0,
        "2": 0,
        "3": 0,
        "4": 0,
        "5": 0,
        "6": 0,
        "X": 0
    }
    for g in all_guesses:
        data[g] = data.get(g, 0) + 1
        
    max_value = max(data.values())
    buffer = max_value / 30

    for g in data: # mimic actual wordle stat page, bars with 0 count should have width > 0
        data[g] = data[g] + buffer

    guesses, counts = zip(*data.items())

    # make figure
    fig = plt.figure(figsize=(7, 4))

    # barplot
    bars = plt.barh(guesses, counts, color="#538d4e", height=0.6)
    bars[-1].set_color("#e03f3f")
    plt.gca().invert_yaxis()

    # ticks
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.gca().tick_params(axis=u"both", which=u"both",length=0, pad=15)
    plt.gca().tick_params(axis="x", labelsize=0)

    for label in plt.gca().get_yticklabels(): # guess tick labels
        label.set_fontweight("bold")
        label.set_color("gray")

    # bar labels
    rects = plt.gca().patches
    widest = max([r.get_width() - buffer for r in rects])

    for rect in rects:
        width = rect.get_width()
        label = round(width - buffer)
        offset = widest / 100

        if (widest - width) / widest <= .95: # freq can go inside bar
            x = width - offset
            ha = "right"
            color = "white"
        else: # bar too narrow, freq goes on right of bar
            x = width + offset
            ha = "left"
            color = "gray"

        plt.gca().text( # draw label
            x, 
            rect.get_y() + rect.get_height() / 2, 
            label, 
            ha=ha, 
            va="center",
            color=color,
            fontsize=14,
            fontweight="bold"
        )

    plt.gca().margins(x=0.1)
    plt.setp(plt.gca().spines.values(), color="white")

    fig.tight_layout()

    # return base64 figure image
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output, transparent=True)
    return base64.b64encode(output.getvalue()).decode()