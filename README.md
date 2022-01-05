# LinkedIn Comment Analyzer

Extracting LinkedIn comments from any post and export it to Excel file

1- Expand all comments and replies from linkedin post, 
    by clicking all "Show previous comments" until all comments are visible

2- Expand all comment replies by clicking all "Load previous replies" until all replies are visible. To get really all comments choose the "Most recent" instead of "Most relevant".

3- You can use i.e. Inspect features in Chrome web browse to select all comments by finding the right parent div  in the HTML document structure. This step is crucial to get the right data structure (document fragment) for processing. It may be like in this example:

```
<div id="ember785" class="comments-comments-list
    comments-comments-list--expanded">
  <!---->
  <!---->
  <div>
    <article id="ember1081" class="comments-comment-item
```

4- Right click on that div and then press "Edit As HTML" and copy all contents

5- Save these contents in a text file "Comments.html" and make sure that encoding is UTF-8

6- Put this file inside the same directory with this python file "linkedin-comments-grabber.py"

7- Excute linkedin-comments-grabber.py

<img src="Sample - Blurred.png" />

# TODOs:
Having the list of commnets extracted can be a good start point for text statistic analysis like (no of words used in the communication)
1. Use some lib to analyze text - statistic
2. Try to understand the comminication, meaning, key messages/words - to get in social listening mode 
