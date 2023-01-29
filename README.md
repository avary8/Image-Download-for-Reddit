# Image-Download-for-Reddit
Download Specific Images from Reddit using an AI model, Google Vision 
## Contents
- [Project Description](#project-description)
- [Implemented Features](#implemented-features)
- [Example Run](#example-run)
- [Usage](#usage)
- [Possible Future Implementation](#possible-future-implementation)

# Project Description
This script will take three inputs from the user
- a subreddit name
- a thing you want to search 
- number of pictures you want saved

This script will then search for any pictures in the subreddit.
Those pictures are run through Google Vision's API and are downloaded to a users computer in a folder called "SavedReddit/" + name of search.
The pictures are only downloaded if Google Vision's API returns a list of labels or descriptors that match the keyword the user wants.

# Implemented Features
- the program will stop searching after a certain constraint in order to not spam Reddit's API
- Not only can the user can search a specific object, but also a specific color. The script will compare the rgb values of Google Vision's dominant colors
- when comparing dominant colors, the script will only compare a certain amount to limit incorrect color matching

# Example Run
Right now I am limited to a command line interface; however, in the future, I plan to change this.
### Searching for 20 cat images in r/cats
![main py - swamphacks - Visual Studio Code 1_29_2023 10_17_46 AM](https://user-images.githubusercontent.com/64299012/215336972-7e992344-c52f-433f-8bb9-f64cb145a351.png)


### 20 cats images downloaded in the path declared in the script
![cats_results](https://user-images.githubusercontent.com/64299012/215337132-99454465-fdae-4c60-bb82-a4c2abeb2889.png)


# Usage
Right now, this script is more of a personal use; however, in the future, I hope to expand its capabilities.
- Python in VSC
- Google API service account 
- Reddit API credentials


# Possible Future Implementation
- allowing user to enter multiple words
- more use of Google Vision API such as people detection, only downloading images of a high resolution, etc)
- a website/better distributable implementation of this script (a website that could allow users to access the Reddit API and Google API without needed the licenses themselves)
