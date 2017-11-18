'''
I gotta give credit where credit is due.
The base of this was learned from an amazing tutorial by Shantnu.
His blog can be found at http://pythonforengineers.com/build-a-reddit-bot-part-1/
'''

#!/usr/bin/python
import praw
import pdb
import re
import os


# Create the Reddit instance
reddit = praw.Reddit('bot1')

# and login
#reddit.login(REDDIT_USERNAME, REDDIT_PASS)

# Have we run this code before? If not, create an empty list
if not os.path.isfile("posts_replied_to.txt"):
    posts_replied_to = []

# If we have run the code before, load the list of posts we have replied to
else:
    # Read the file into a list and remove any empty values
    with open("posts_replied_to.txt", "r") as f:
        posts_replied_to = f.read()
        posts_replied_to = posts_replied_to.split("\n")
        posts_replied_to = list(filter(None, posts_replied_to))

git_commands_set = ("add","am","archive","bisect","branch","bundle","checkout","cherry-pick","citool","clean","clone","commit","describe","diff","fetch","format-patch","gc","grep","gui","init","log","merge","mv","notes","pull","push","rebase","reset","revert","rm","shortlog","show","stash","status","submodule","tag","worktree")

# Get the top 5 values from our subreddit
def checkcommands(subreddit):
	print("commands called")
	for submission in subreddit.hot(limit=10):
	    #print(submission.title)

	    # If we haven't replied to this post before
	    if submission.id not in posts_replied_to:

		# Do a case insensitive search
		if re.search("git ", submission.title, re.IGNORECASE):
	            command = re.search('git\s(\w+)',submission.title, re.IGNORECASE)
		    # Reply to the post
	            if command.group(1) not in git_commands_set:
			    submission.reply("git: " + command.group(1) + " is not a git command. See \'git --help\'.")
                            print("Bot replying to : ", submission.title, "::", submission.id)

		    # Store the current id into our list
		    posts_replied_to.append(submission.id)

subreddit = reddit.subreddit('HackUSU2017+learnpython')
'''
try:
    checkcommands(subreddit)
except:
    print("rejected")
    pass
'''
subreddit.SubredditStream.comments()

# Write our updated list back to the file
with open("posts_replied_to.txt", "w") as f:
    for post_id in posts_replied_to:
        f.write(post_id + "\n")
