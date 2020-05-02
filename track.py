import tweepy as tw
from config import create_api
import pickle


def search_bio(api):
    user = ''  # target user without "@"
    # famous target: jrhunt, werner, ajassy, jeffbezos
    target_list = ''  # Target Twitter list ID

    keywords = ["@awscloud"]  # Follower bio terms you are interested in
    hits = []  # Array of twitter profiles/users

    # Identify user in list, count it and fill it
    # users_in_list = []
    # for user in tw.Cursor(api.list_members, list_id=target_list).items():
    #     print(user.screen_name)
    #     users_in_list.append(user.screen_name)
    # c = len(users_in_list)
    # print("===> Number of users in list: ", c)
    # print(users_in_list)
    # with open('list.pkl', 'wb') as f:
    #     pickle.dump(users_in_list, f)
    # f.close()

    # Load the current already crawled profiles and list profiles
    with open('list.pkl', 'rb') as f:
        users_in_list = pickle.load(f)
        b = len(users_in_list)
        f.close()
    for idx, follower in enumerate(tw.Cursor(api.followers, id=user).items(), start=1):
        print(idx, follower.screen_name)
        # don't redo if already crawled profiles (already in the list)
        if not (follower.screen_name in users_in_list):
            for word in keywords:
                # if keyword, not already crawled and not protected profiles
                if word in str(follower.description.encode('utf-8')) and not (follower in hits) and follower.protected is False:
                    print("===="*10)
                    print("matched!")
                    print("screen_name: ", follower.screen_name)
                    print("description: ", follower.description.encode('utf-8'))
                    hits.append(follower)
                    # Add to twitter list
                    api.add_list_member(screen_name=follower.screen_name, list_id=target_list)
                    print("Added to list: ", follower.screen_name)
                    print("===="*10)
        else:
            print("Already in list: ", follower.screen_name)
        users_in_list.append(follower.screen_name)
        # Dump result to the pickle local file: already crawled and list profiles
        with open('list.pkl', 'wb') as f:
            pickle.dump(users_in_list, f)
    f.close()
    # count
    c = len(users_in_list)
    h = len(hits)
    # Job summary
    print("===="*10)
    print("1-Number of users in list before crawling: ", b)
    print("2-Number of users in list after crawling: ", c)
    # delta
    d = c - b
    print("3-Crawled: ", d)
    print("4-Matched: ", h)
    print("===="*10)


def main():
    api = create_api()
    search_bio(api)


if __name__ == "__main__":
    main()
