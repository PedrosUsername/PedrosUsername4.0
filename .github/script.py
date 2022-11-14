from datetime import datetime
import requests
import json
import sys
import os










SUB = sys.argv[1] if len(sys.argv) > 1 else None
TODAY = datetime.now()










def queryGActionsApp(SUB):
    if(SUB == None):
        return None

    headers = buildHeaders()

    url = 'https://oauth.reddit.com/r/'+ str(SUB) +'/hot'

    r = requests.get(url, headers=headers, params={'limit': 100})

    data = r.json()

    return data['data']['children']










def buildHeaders():
    auth = requests.auth.HTTPBasicAuth(os.environ['CLIENT_ID'], os.environ['SECRET_KEY'])
    data = { 'grant_type': 'password', 'username': 'rv_conspiracy', 'password': os.environ['R_PASSWORD'] }
    headers = { 'User-Agent': 'gActionsApp/0.0.2' }

    TOKEN = requests.post('https://www.reddit.com/api/v1/access_token', auth=auth, data=data, headers=headers).json()['access_token']

    return { **headers, **{'Authorization': f"bearer {TOKEN}"} }










def scoreCounter(post):
    return post['score']










def getTimeElapsed(seconds):
    hours = divmod(seconds, 3600)[0]
    days = divmod(seconds, 86400)[0]

    pluralHours = '' if hours < 2 else 's'
    pluralDays = '' if days < 2 else 's'

    return (f"{format(days, '.0f')} day{pluralDays} ago") if days > 0 else (f"{format(hours, '.0f')} hour{pluralHours} ago")












rawPosts = queryGActionsApp( SUB )
posts = []

for rawPost in rawPosts:
    if(rawPost['data']['domain'] == 'i.redd.it'):
        posts.append(rawPost['data'])

posts.sort(key = scoreCounter, reverse= True)


if( len(posts) > 0 ):
    post = posts[0]
    seconds_elapsed = (TODAY - datetime.fromtimestamp(post['created_utc'])).total_seconds()

    print('******************** selected')
    print("title: " + post['title'])
    print("author: " + post['author'])
    print("posted at: " + datetime.fromtimestamp(post['created_utc']).strftime('%d-%b-%Y %H:%M:%S'))
    print("score: " + str(post['score']))
    print("num_comments: " + str(post['num_comments']))
    print("full_link: " + 'https://reddit.com' + post['permalink'])
    print('********************')

    f = open('README.md', 'w')
    content = f"""### Hey, what's up?
<img align="right" alt="Pedro's GitHub Top Languages" src="https://github-readme-stats.vercel.app/api/top-langs/?username=PedrosUsername&exclude_repo=HW2&layout=compact" />

I'm Pedro. I like coding, animation, witch-house and video games.<br><br>

### More about me
- **Currently working on:**  
&nbsp;&nbsp;&nbsp;&nbsp;My internship
- **Currently learning:**  
&nbsp;&nbsp;&nbsp;&nbsp;Java and Typescript
- **Favorite song:**  
&nbsp;&nbsp;&nbsp;&nbsp;DEVILNOTCRY — NotEnoughOfYou<br><br>

### Scored well on r/{SUB} recently:

<p align="left"><sub>last updated at: {TODAY.strftime('%d %b %Y at %H:%M:%S')}</sub></p>

|   |
| --- |
| <sub>[Posted by: u/{post['author']}][source] &nbsp; {getTimeElapsed(seconds_elapsed)}</sub> |
| **{post['title']}** | 
|<p align="center"> <img alt="image" src="{post['url']}" width="550" /> </p>|
|   |

  



  
  
  
[linkedin]: https://linkedin.com/in/pedro-h-r-gomes-8a487b14a/
[gmail]: mailto:pilique11@gmail.com
[source]: https://reddit.com{post['permalink']}
[redditAPI]: https://www.reddit.com/dev/api/"""

    f.write( content )
    f.close()
else:
    errorMsg = 'no subreddit informed' if SUB == None else 'no post was found'
    print(errorMsg)