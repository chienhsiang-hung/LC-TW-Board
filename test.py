import requests
# client = requests.session()
# Retrieve the CSRF token first
# client.get('https://leetcode.com/chienhsiang-hung/') # Sets cookie
# csrftoken = client.cookies['csrftoken']
# print(client.cookies)
# LEETCODE_SESSION = client.cookies['LEETCODE_SESSION']

# https://leetcode.com/discuss/general-discussion/1297705/is-there-public-api-endpoints-available-for-leetcode
html = requests.post(
    'https://leetcode.com/graphql/',
    # headers = {
    #     'referer': 'https://leetcode.com/chienhsiang-hung/',
    #     'cookie': f'csrftoken={csrftoken}'
    # },
    json={"query":"query userPublicProfile($username: String!) {\n  matchedUser(username: $username) {\n    contestBadge {\n      name\n      expired\n      hoverText\n      icon\n    }\n    username\n    githubUrl\n    twitterUrl\n    linkedinUrl\n    profile {\n      ranking\n      userAvatar\n      realName\n      aboutMe\n      school\n      websites\n      countryName\n      company\n      jobTitle\n      skillTags\n      postViewCount\n      postViewCountDiff\n      reputation\n      reputationDiff\n      solutionCount\n      solutionCountDiff\n      categoryDiscussCount\n      categoryDiscussCountDiff\n    }\n  }\n}\n    ","variables":{"username":"chienhsiang-hung"}}
)
print(html.text)
with open('test.txt', 'w') as txt:
    txt.write(html.text)
