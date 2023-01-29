import os
from google.cloud import vision
from google.cloud import vision_v1 
import urllib.request #lib included in python 3
import urllib.error
import json
import os
import getpass
import praw
import requests
import time
import uuid
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

def verifySub(subred):
    if 'r/' in subred:
        return subred.replace('r/', '')
    else: 
        #-----------------------------fix this-------------------------------------------
        res = requests.get("https://oauth.reddit.com/r/" + subred +'?limit=5',
                   headers=headers)
        if len(res.json()['data']['children']) == 0:
            print("This subreddit does not exist.")
            return "False"
        else:
            return subred

def verifyMax(max):
    if max.isdigit() and int(max) < 101 and int(max) > 0:
        return True
    else:
        return False


def createURL(subred):
    return 'http://www.reddit.com/r/' + subred


def getInput():
    print("Enter subreddit: ")
    subred = input()
    # subred = verifySub(subred)
    # while verifySub(subred) == "False":
    #     print("Please enter a valid subreddit: ")
    #     subred = input()
    #     subred = verifySub(subred)
    # print(subred)
    print("Enter what you wish to save: ")
    saveThis = input()

    print("Enter the number of pictures you want saved (1-100): ")
    max = input()
    while verifyMax(max) == False:
        print("Please enter a valid number: ")
        subred = input()

    #url = createURL(subred)
    return subred, saveThis, max

def validPic(keyword, url):  
    client = vision.ImageAnnotatorClient()
    image = vision_v1.Image()
    image.source.image_uri = url
    urlLabels = labelImg(image, client)
    colorProps = colorProperties(image, client)
    valid = False

    try:
        keyCol = mcolors.to_rgb(keyword)
        if checkColor(keyword, colorProps):
            valid = True
    except ValueError as e:
        if checkLabel(keyword, urlLabels):
            valid = True
            
    # if checkLabel(keyword, urlLabels) or checkColor(keyword, colorProps):
    #     return True
    # else:
    #     return False
    return valid
    
def checkLabel(keyword, labeledPic):
    print("checking label")
    for label in labeledPic.label_annotations:
        #print({'label': label.description, 'score': label.score})    
        if label.description in keyword or keyword in label.description:
            return True
    return False

def checkColor(keyword, labeledPic):
    print("checking color")
    keyCol = mcolors.to_rgb(keyword)
    #if many dominant colors, only check first 3 
    check = len(labeledPic.image_properties_annotation.dominant_colors.colors)
    if check > 8:
        check = 3

    for c in labeledPic.image_properties_annotation.dominant_colors.colors:
        #print(labeledPic.image_properties_annotation.dominant_colors)
        if colorDist(keyCol, c.color) > 75000:
            return True
        check -=1
        if check == 0:
            break
    return False

    
def colorDist(c1, c2):
    rm = 3
    gm = 2
    if ((255*c1[0]) + c2.red)/2 < 128:
        rm = 2
        gm = 3

    r = rm*(((255*c1[0]) - c2.red))**2
    g = 4*(((255*c1[1]) - c2.green))**2
    b = gm*(((255*c1[2]) - c2.blue))**2

    return (r+g+b)**1/2


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'' #add google vision API service account json

#### LABEL DETECTION ######
def labelImg(image, client):
    response_label = client.label_detection(image=image)
    return response_label
    # for label in response_label.label_annotations:
    #     print({'label': label.description, 'score': label.score})
        

# print("------------Face Detection---------------")
# #### FACE DETECTION ######
# response_face = client.face_detection(image=image)

# face_data = []

# for face_detection in response_face.face_annotations:
#     d = {
#         'confidence': face_detection.detection_confidence,
#         'joy': face_detection.joy_likelihood,
#         'sorrow': face_detection.sorrow_likelihood,
#         'surprise': face_detection.surprise_likelihood,
#         'anger': face_detection.anger_likelihood
#     }
#     print(d)

#### IMAGE PROPERTIES ######
def colorProperties(image, client):
    response_image = client.image_properties(image=image)
    return response_image


# #### TEXT DETECTION ######

# response_text = client.text_detection(image=image)

# for r in response_text.text_annotations:
#     d = {
#         'text': r.description
#     }
#     print(d)



auth = requests.auth.HTTPBasicAuth('', '') #add reddit api credentials
data = {'grant_type': 'password',
        'username': '',
        'password': ''} #more credentials

headers = {'User-Agent': 'Swampy Saves/0.0.1'}


# send our request for an OAuth token
res = requests.post('https://www.reddit.com/api/v1/access_token',
                    auth=auth, data=data, headers=headers)

# convert response to JSON and pull access_token value
TOKEN = res.json()['access_token']
# add authorization to our headers dictionary
headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}
requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)

#get the input. put here so we can check if subreddit exists
subred, saveThis, max = getInput()

#create a directory to save pictures in
user = getpass.getuser()
directory = "C:/SavedReddit/"+saveThis
if not os.path.exists(directory):
    os.makedirs(directory)

res = requests.get("https://oauth.reddit.com/r/" + subred +'?limit=100',
                   headers=headers)

allowed_ext = ['.jpg', '.jpeg', '.png']
count = 0
breakNow = False
alreadyAccessed = list()

while (count <= int(max)): 
    for post in res.json()['data']['children']:
        #print(post['data']['url'])
        #print (post)
        if post['data']['url'] not in alreadyAccessed and 'comments' not in post['data']['url'] and any (ext in post['data']['url'] for ext in allowed_ext):
            if validPic(saveThis, post['data']['url']) == True:
                count +=1 
                save = requests.get(post['data']['url']).content
                #with open(directory,'wb') as handler:
                 #   handler.write(save)
                  #  handler.close()

                fp = open((directory + "/%s"+".jpg") %(uuid.uuid4().hex) ,"wb")
                fp.write(save)
                fp.close()
        alreadyAccessed.append(post['data']['url'])
        last_post_id = res.json()['data']['after']

        #breaks if you have found enough photos OR
        #if you have accessed everything in the subreddit
        if count >= int(max) or len(alreadyAccessed) >= len(res.json()['data']['children']):
            breakNow = True
            break
  
    #break while loop. if the image is not likely to be found, stop program (so it does not break anything)
    if breakNow == True or (len(alreadyAccessed) > 100 and count < 5):
        break
    #continues searching at the last post id 
    res = requests.get("https://oauth.reddit.com/r/" + subred,
                    headers=headers, params={'limit': '100', 'after': last_post_id})
    time.sleep(2)

print(str(count) + " images found in " + str(len(alreadyAccessed)) + " posts")
