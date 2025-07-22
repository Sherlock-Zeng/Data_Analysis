# 微博可视化

from wordcloud import WordCloud
import jieba
import pandas as pd


def draw():
    df = pd.read_excel('微博搜索1.xlsx', engine='openpyxl')
    stop = []
    kinds = df['内容'].tolist()
    words = jieba.cut('/'.join(kinds))
    newtxt = ''
    for word in words:
        if len(word) > 1 and word not in stop:
            newtxt += word + '/'
    wordcloud = WordCloud(background_color='white', width=800, height=600, font_path='msyh.ttc', max_words=200,
                          max_font_size=130).generate(newtxt)
    wordcloud.to_file('微博词云1.png')


if __name__ == '__main__':
    draw()
