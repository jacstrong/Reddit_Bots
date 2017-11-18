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
from praw.models import MoreComments

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

if not os.path.isfile("comments_replied_to.txt"):
    comments_replied_to = []
else:
    with open("comments_replied_to.txt", "r") as f:
        comments_replied_to = f.read()
        comments_replied_to = comments_replied_to.split("\n")
        comments_replied_to = list(filter(None, comments_replied_to))

git_commands_set = ("add","am","archive","bisect","branch","bundle","checkout","cherry-pick","citool","clean","clone","command","commit","describe","diff","fetch","format-patch","gc","grep","gui","init","log","merge","mv","notes","pull","push","rebase","reset","revert","rm","shortlog","show","stash","status","submodule","tag","worktree","--version","--help","-C","-c","--exec-path[=<path>]","--html-path","--man-path","--info-path","-p|--paginate|--no-pager","no-replace-objects","--bare","--git-dir=<path>","--work-tree=<path>","--namespace=<name>","<command>","config","fast-export","fast-import","filter-branch","mergetool","pack-refs","prune","reflog","relink","remote","repack","replace","annotate","blame","cherry","count-objects","difftool","fsck","get-tar-commit-id","help","instaweb","merge-tree","rerere","rev-parse","show-branch","verify-tag","whatchanged","archimport","cvsexportcommit","cvsexportcommit","cvsserver","imap-send","p4","quiltimport","request-pull","send-email","snv")

# Get the top 5 values fr"om our subreddit
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
                        try:   
                            submission.reply("####`git: \'" + command.group(1) + "\' is not a git command. See \'git --help\'.`")
                            print("Bot replying to : ", submission.title, "::", submission.id)
                        except Exception, e:
                            print('S comment rejected: ' + str(e))
                            pass

		    # Store the current id into our list
		    posts_replied_to.append(submission.id)

        for submission in subreddit.hot(limit=10):
            submission.comments.replace_more(limit=0)
            comment_queue = submission.comments[:]
            while comment_queue:
                comment = comment_queue.pop(0)
                if comment.id not in comments_replied_to:
                    if re.search("git ", comment.body, re.IGNORECASE):
	                command = re.search('git\s(\w+)', comment.body, re.IGNORECASE)
		        # Reply to the post
	                if command.group(1) not in git_commands_set:
                            try:
			        comment.reply("####`git: \'" + command.group(1) + "\' is not a git command. See \'git --help\'.`")
                                print("Bot replying to comment: ", comment.body, "::", submission.id,"::",comment.id)
                            except Exception, e:
                                print('Comment rejected: ' + str(e))
                                pass
                comments_replied_to.append(comment.id)
                comment_queue.extend(comment.replies)

subreddit = reddit.subreddit('HackUSU2017+pythonforengineers')

try:
    checkcommands(subreddit)
    print("completed")
except:
    print("rejected")
    pass

# Write our updated list back to the file
with open("posts_replied_to.txt", "w") as f:
    for post_id in posts_replied_to:
        f.write(post_id + "\n")


with open("comments_replied_to.txt", "w") as f:
    for comment_id in comments_replied_to:
        f.write(comment_id + "\n")
