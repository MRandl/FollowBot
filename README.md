#Followbot
##Introduction

Followbot is a proof-of-concept software we developed in the context of our bachelor semester project "Followback prediction" at EPFL in the LSIR lab.

In this project, our goal was to develop a framework that would predict whether a user on Twitter was likely to followback or not, based on a certain number of parameters.

This repository contains a wrapper for the final product of the project; how it works is explained below.

##Requirements

To be able to use the Followbot, you're going to need a few things:
- Python installed
- An approved Twitter developer account and the corresponding key, to be able to get information about the users (followers, followings, etc)

#####A Python environment with the following packages:

- Tweepy
- Pandas
- Numpy
- Joblib
##How it works

Here is a brief explanation of how Followbot proceeds:

Step 1: If it is the first time you use it, the bot will ask you for your developer Twitter API key. This step is crucial as otherwise, you won't be able to use the bot. If you already typed your API key at least once before, this step is skipped.

Step 2: In this step, you either:

are asked to enter a list of screen names of the people you wish to follow; the bot will then decide if those people are likely to followback or not.
if you followed people using this bot before, it will check whether they followed back or not. If at least one user did, the bot will propose a list of at most 15 people to follow using a Breadth First Search search algorithm; it is up to you to accept or not. If you refuse or if nobody followed you back, you will be asked to type in names once more. Either way, the bot will learn from this experience by fitting the new data.

Step 3: after you are done, you must follow the users manually. Relaunch Followbot after a few days in order to let the potential followbacks happen


##How to launch

Simply go to the "src" directory in your terminal and launch the main program with "python main.py" or "python3 main.py". You may need to launch this from an environment with the required packages.

##Authors
@AttiaYoussef

@MRandl