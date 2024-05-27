import jieba
from matplotlib import pylab as plt
from wordcloud import WordCloud
from PIL import Image
import numpy as np
import json
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE','travel.settings')
django.setup()
from app.models import TravelInfo


def getIntroCloudImg(targetImgSrc,resImgSrc):
    travelList = TravelInfo.objects.all()
    text = ''
    stopwords = ['的', '是', '在', '这', '那', '他', '她', '它', '我', '你','和','等','为','有','与','了','就','都','也','可以','到','去','我们']
    for travel in travelList:
         text += travel.detailIntro

    cut = jieba.cut(text)
    newCut = []
    for tex in cut:
        if tex not in stopwords:
            newCut.append(tex)

    string = ' '.join(newCut)

    img = Image.open(targetImgSrc)
    img_arr = np.array(img)
    wc = WordCloud(
        background_color='white',
        mask=img_arr,
        # font_path='arial.ttf'
        font_path = 'STHUPO.TTF'   # 原始
    )

    wc.generate_from_text(string)

    # 绘制图片
    fig = plt.figure(1)
    plt.imshow(wc)
    plt.axis('off') # 不显示坐标轴

    # plt.show()

    plt.savefig(resImgSrc,dpi=500)


def getCommentContentCloudImg(targetImgSrc,resImgSrc):
    travelList = TravelInfo.objects.all()
    text = ''
    stopwords = ['的', '是', '在', '这', '那', '他', '她', '它', '我', '你','和','等','为','有','与','了','就','都','也','可以','到','去','我们']
    for travel in travelList:
        comments = json.loads(travel.comments)
        for comm in comments:
            text += comm['content']

    cut = jieba.cut(text)
    newCut = []
    for tex in cut:
        if tex not in stopwords:
            newCut.append(tex)

    string = ' '.join(newCut)

    img = Image.open(targetImgSrc)
    img_arr = np.array(img)
    wc = WordCloud(
        background_color='white',
        mask=img_arr,
        # font_path='arial.ttf'
        font_path = 'STHUPO.TTF'
    )

    wc.generate_from_text(string)

    # 绘制图片
    fig = plt.figure(1)
    plt.imshow(wc)
    plt.axis('off') # 不显示坐标轴

    # plt.show()

    plt.savefig(resImgSrc,dpi=500)

if __name__ == '__main__':
    getCommentContentCloudImg('./static/2.jpg','./static/commentContentCloud.jpg')









