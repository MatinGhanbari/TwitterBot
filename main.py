from twitterBot.twitterBotController import TwitterBotController


def clearLog():
    with open('core/log', 'w') as file:
        file.write('Start: \n')


if __name__ == "__main__":
    clearLog()
    twitterController = TwitterBotController()
    twitterController.startBot()
