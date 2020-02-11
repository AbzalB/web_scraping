import csv
import re
import plotly.graph_objects as go
import wordcloud

years = []
grosses = []

with open('imdb_scraped.csv', newline='') as csvfile:
    moviereader = csv.reader(csvfile, delimiter=',', quotechar='\"')
    for movie in moviereader:
        #print(movie)
        if len(movie) < 2:
            continue
        gross = movie[1]
        year = movie[-1]
        year = re.findall('\d\d\d\d', year)
        if year:
            year = int(year[0])
            if gross:
                gross_number = float(gross[1:][:-1]) * (10 * 10 * 10 * 10 * 10 * 10)
                years.append(year)
                grosses.append(gross_number)
                print(f"Year: {year}, gross: {gross_number}")

word_frequencies = {}

with open('rating_scraped.csv', newline='') as csvfile:
    ratingreader = csv.reader(csvfile, delimiter=',', quotechar='\"')
    for rating in ratingreader:
        if rating[0] == "text":
            continue
        text = rating[1]
        for word in text.split(" "):
            if word in word_frequencies:
                word_frequencies[word] += 1
            else:
                word_frequencies[word] = 1

fig = go.Figure(data=go.Bar(y=grosses, x=years))
fig.update_layout(
    title="Movie Gross Over Time",
    xaxis_title="Years",
    yaxis_title="Gross",
)
fig.show()

w = wordcloud.WordCloud()
w.fit_words(word_frequencies)
w.to_file("cloud.png")