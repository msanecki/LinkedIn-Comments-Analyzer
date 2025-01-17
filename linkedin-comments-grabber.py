"""
LinkedIn Comments Analyzer

Copyright 2017 Amr Salama
Twitter: @amr_salama3
Github: rozester/LinkedInCommentAnalyzer

MIT License

Work Steps:-

1- Expand all comments and replies from linkedin post, 
    by clicking all "Show previous comments" until all comments are visible

2- Expand all comment replies by clicking all "Load previous replies" until all replies are visible

3- press f12 in your browser and select all comments with parent div it must be like this example:-

<div id="ember1482" class="feed-base-comments-list feed-base-comments-list--expanded ember-view"><!---->
<!---->
      <article>
      <article>
      <article>
      
      ....
      
      <article>
<div>

4- right click on that div and then press "Edit As HTML" and copy all contents

5- save these contents in a text file for example Comments.html and make sure that encoding is UTF-8

Enjoy Data Science :)
"""

import pandas as pd
from bs4 import BeautifulSoup
from datetime import date

# the file which contains all comments
file = open('Comments_Tesla.html', 'r',encoding='utf8')
html_doc = file.read()
file.close()

# Parse html file
soup = BeautifulSoup(html_doc, 'html.parser')

# Select all comments and replies html tags
comments = soup.find_all("article", recursive=True)

# Prepare Dataframe for loading all comments and replies inside it
output_comments_df = pd.DataFrame(columns=['CommentID', 'ParentID', 'LinkedIn ID', 'Name', 'Photo', 
                                           'Comment', 'Likes', 'Replies'])

# Data Cleansing Phase
def paragraph_cleaning(p):
    # Normal Comment
    print("comment: ", p)
    if (p):
        return p.string.replace('\n','').strip()

#    # mention comment
#    elif (p.span and p.span.a):#        return p.span.a.string.replace('\n','').strip()
#    elif (p.a.span):
#        return p.a.span.string.replace('\n','').strip()
#    # url comment
#    elif (cmnt.find('p').a):
#        return cmnt.find('p').a.string.replace('\n','').strip()
#    return p
        
    # Complicated Comment
  #  p_body = ""
   # for cmnt in p.children:
    #    if (cmnt.string):
     #       p_body = p_body + cmnt.string
      #  else:
       #     p_body = p_body + " " + cmnt.a.string
    #return p_body

def get_likes(comment):
    # likes exists
    likes = comment.find('button', class_="comments-comment-social-bar__reactions-count t-12 t-black--light t-normal hoverable-link-text display-flex")
    if (likes):
        return likes.span.get_text()
    return 0

def get_replies(comment):
    # replies exists
    replies = comment.find('button', class_="feed-base-comment-social-bar__comments-count Sans-13px-black-55% hoverable-link-text")
    if (replies):
        return replies.span.string.split(" ")[0]
    return 0

def get_cleanLinkedInId(arg):
    if(arg==None):
        return "FakeLinkedInID"
    else:
        if arg.a == None:
            return "FakeLinkedInID"
        else:
            return arg.a.attrs.get('href')

def get_cleanLinkedInName(arg):
    if(arg==None):
        return "FakeName"
    else:
        if arg.find('span',class_="comments-post-meta__name-text hoverable-link-text") == None:
            return "FakeLinkedInName"
        else:
            return arg.find('span',class_="comments-post-meta__name-text hoverable-link-text").string.replace('\n','').strip()
def get_cleanLinkedInPhoto(arg):
    if(arg==None):
        return "FakeName"
    else:
        if arg.img == None:
            return "FakeNum"
        else:
            return arg.img.attrs.get('src')

def get_cleanLinkedInComment(arg):
    if(arg==None):
        return "FakeName"
    else:
        if arg.find('div', class_='feed-shared-text relative') == None:
            return "FakeName"
        else:   
            return arg.find('div', class_='feed-shared-text relative').find('span').get_text().replace('\n','').strip()
i = 0
# Fill Dataframe with comments and replies
def add_comment(parent, comment):
    global i
    output_comments_df.loc[i] = \
        [
            i + 1, 
            parent, 
            get_cleanLinkedInId(comment), 
            get_cleanLinkedInName(comment), 
            get_cleanLinkedInPhoto(comment),
            #paragraph_cleaning(comment.find("span", dir_="ltr")), 
            get_cleanLinkedInComment(comment),
            get_likes(comment), 
            get_replies(comment)
        ]
    i = i + 1
    return i

# Get all replies
def add_comment_replies(parent, comment):
    if (comment.article):
        for cmnt in comment.find_all("article"):
            add_comment(parent, cmnt)

# the main iterator for all comments and replies
for cmnt in comments:
    cmnt_id = add_comment(0, cmnt)
    add_comment_replies(cmnt_id, cmnt)

# Fixing Data Types
output_comments_df['CommentID'] = output_comments_df['CommentID'].astype(int)
output_comments_df['ParentID'] = output_comments_df['ParentID'].astype(int)
output_comments_df['Likes'] = output_comments_df['Likes'].astype(int)
output_comments_df['Replies'] = output_comments_df['Replies'].astype(int)

# Exporting to Excel file
date_stamp = date.today().strftime('%Y-%m-%d')
writer = pd.ExcelWriter('output_'+date_stamp + '.xlsx')
output_comments_df.to_excel(writer,'Sheet1')
writer.save()