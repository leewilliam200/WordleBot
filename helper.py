import matplotlib.pyplot as plt
from IPython import display
import random
import string

plt.ion()

count = {}

def plot(scores, mean_scores):
    display.clear_output(wait=True)
    display.display(plt.gcf())
    plt.clf()
    plt.title('Training...')
    plt.xlabel('Number of Games')
    plt.ylabel('Score')
    plt.plot(scores)
    plt.plot(mean_scores)
    plt.ylim(ymin=0)
    plt.text(len(scores)-1, scores[-1], str(scores[-1]))
    plt.text(len(mean_scores)-1, mean_scores[-1], str(mean_scores[-1]))
    plt.show(block=False)
    plt.pause(.1)

def create_short_list():
    with open('fiveLetter.txt') as word_file:
        lines = list(set(word.strip() for word in word_file))
    
    with open('testingWords.txt', 'w') as newFile:
        new_list = "\n".join(random.choice(lines) for _ in range(100))
        newFile.write(new_list)

def word_count():
    global count
    with open('testingWords.txt') as word_file:
        text = word_file.read().lower()
        for i in string.ascii_lowercase:
            count[i] = (text.count(i))
        print(count)

def most_common():
    global count
    with open('testingWords.txt') as word_file:
        lines = list(set(word.strip() for word in word_file))
    curr = 0
    max = 0
    line = ''
    for i in lines:
        j = i.lower()
        curr += count[j[0]]
        curr += count[j[1]]
        curr += count[j[2]]
        curr += count[j[3]]
        curr += count[j[4]]

        if curr > max:
            line = i
            max = curr
        
        curr = 0
    
    print(line)

if __name__ == '__main__':
    create_short_list()
    word_count()
    most_common()