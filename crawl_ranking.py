import os, requests, time, pymongo
import pandas as pd
from tqdm import tqdm


ranking_DF = pd.DataFrame(columns=['currentRating', 'currentGlobalRanking', 'userAvatar', 'username', 'realName', 'ranking', 'school'])
currentRating=[]; currentGlobalRanking=[]; userAvatar=[]; username=[]; realName=[]; ranking=[]; school=[]
for i in tqdm(range(13878)):
    # POST for ranking data of the page
    graphql_ranking = requests.post(
        'https://leetcode.com/graphql/',
        json = {"query": "{\n  globalRanking(page: "+str(i+1)+") {\n    totalUsers\n    userPerPage\n    myRank {\n      ranking\n      currentGlobalRanking\n      currentRating\n      dataRegion\n      user {\n        nameColor\n        activeBadge {\n          displayName\n          icon\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    rankingNodes {\n      ranking\n      currentRating\n      currentGlobalRanking\n      dataRegion\n      user {\n        username\n        nameColor\n        activeBadge {\n          displayName\n          icon\n          __typename\n        }\n        profile {\n          userAvatar\n          countryCode\n          countryName\n          realName\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"}
    )
    # try to catch no reponse (retry 3 times)
    retry = 0
    while graphql_ranking.status_code != 200 and retry < 3:
        print(f'page {str(i+1)} retry {retry+1} times')
        time.sleep(60)
        graphql_ranking = requests.post(
            'https://leetcode.com/graphql/',
            json = {"query": "{\n  globalRanking(page: "+str(i+1)+") {\n    totalUsers\n    userPerPage\n    myRank {\n      ranking\n      currentGlobalRanking\n      currentRating\n      dataRegion\n      user {\n        nameColor\n        activeBadge {\n          displayName\n          icon\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    rankingNodes {\n      ranking\n      currentRating\n      currentGlobalRanking\n      dataRegion\n      user {\n        username\n        nameColor\n        activeBadge {\n          displayName\n          icon\n          __typename\n        }\n        profile {\n          userAvatar\n          countryCode\n          countryName\n          realName\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"}
        )
        retry += 1
    if retry == 3:
        print(f'skip page {str(i+1)}')
        continue


    for rankingNode in graphql_ranking.json()['data']['globalRanking']['rankingNodes']:
        if rankingNode['user']['profile']['countryCode'] == 'TW':
            # POST for user data of the username
            graphql_user = requests.post(
                'https://leetcode.com/graphql/',
                json = {
                    "query": "query userPublicProfile($username: String!) {\n  matchedUser(username: $username) {\n    contestBadge {\n      name\n      expired\n      hoverText\n      icon\n    }\n    username\n    githubUrl\n    twitterUrl\n    linkedinUrl\n    profile {\n      ranking\n      userAvatar\n      realName\n      aboutMe\n      school\n      websites\n      countryName\n      company\n      jobTitle\n      skillTags\n      postViewCount\n      postViewCountDiff\n      reputation\n      reputationDiff\n      solutionCount\n      solutionCountDiff\n      categoryDiscussCount\n      categoryDiscussCountDiff\n    }\n  }\n}\n    ",
                    "variables": {"username": rankingNode['user']['username']}
                }
            )
            # try to catch no reponse (retry 3 times)
            retry = 0
            while graphql_user.status_code != 200 and retry < 3:
                print(f'user {rankingNode["user"]["username"]} retry {retry+1} times')
                time.sleep(60)
                graphql_user = requests.post(
                    'https://leetcode.com/graphql/',
                    json = {
                        "query": "query userPublicProfile($username: String!) {\n  matchedUser(username: $username) {\n    contestBadge {\n      name\n      expired\n      hoverText\n      icon\n    }\n    username\n    githubUrl\n    twitterUrl\n    linkedinUrl\n    profile {\n      ranking\n      userAvatar\n      realName\n      aboutMe\n      school\n      websites\n      countryName\n      company\n      jobTitle\n      skillTags\n      postViewCount\n      postViewCountDiff\n      reputation\n      reputationDiff\n      solutionCount\n      solutionCountDiff\n      categoryDiscussCount\n      categoryDiscussCountDiff\n    }\n  }\n}\n    ",
                        "variables": {"username": rankingNode['user']['username']}
                    }
                )
                retry += 1
            if retry == 3:
                print(f'user {rankingNode["user"]["username"]} query failed')
            

            currentRating.append(rankingNode['currentRating'])
            currentGlobalRanking.append(rankingNode['currentGlobalRanking'])
            userAvatar.append(rankingNode['user']['profile']['userAvatar'])
            username.append(rankingNode['user']['username'])
            realName.append(rankingNode['user']['profile']['realName'])
            ranking.append(
                graphql_user.json()['data']['matchedUser']['profile']['ranking'] if (
                    graphql_user.status_code == 200 and graphql_user.json()['data']['matchedUser'] # handle 'That user does not exist.'
                ) else None
            )
            school.append(
                graphql_user.json()['data']['matchedUser']['profile']['school'] if (
                    graphql_user.status_code == 200 and graphql_user.json()['data']['matchedUser'] # handle 'That user does not exist.'
                ) else None
            )


ranking_DF['currentRating'] = currentRating
ranking_DF['currentGlobalRanking'] = currentGlobalRanking
ranking_DF['userAvatar'] = userAvatar
ranking_DF['username'] = username
ranking_DF['realName'] = realName
ranking_DF['ranking'] = ranking
ranking_DF['school'] = school


client = pymongo.MongoClient( os.environ['MONGODB_URI'] )
db = client['LC-TW-Board']
col = db['main']
col.delete_many({})
col.insert_many(ranking_DF.to_dict('records'))