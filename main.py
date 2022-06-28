import time

from twitterBot import TwitterBot


def commandRun():
    twitterBot = TwitterBot(accountNumber=3)
    try:
        while True:
            command = input("# Enter command: ")
            if command == "login":  # e.g. login
                twitterBot.login()
            elif command == "logout":  # e.g. logout
                twitterBot.logout()
            elif command.split()[0] == "like":  # e.g. like 10
                twitterBot.like_tweets(int(command.split()[1]))
            elif command.split()[0] == "search":  # e.g. search coding
                twitterBot.search(command.replace("search ", ""))
            elif command.split()[0] == "post":  # e.g. post Hello to every one!
                twitterBot.post_tweets(command.replace("post ", ""))
            else:
                print("- Unknown command!")
    except Exception as e:
        print(e)


def autoRun():
    twitterBot = TwitterBot(accountNumber=3)
    try:
        twitterBot.login()
        twitterBot.like_tweets(2)
    except Exception as e:
        twitterBot.systemLog(e)


if __name__ == "__main__":
    # autoRun()
    commandRun()
