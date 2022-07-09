from twitterBot.twitterBot import TwitterBot
from utils.utils import *
from threading import Thread


class TwitterBotController:
    def __init__(self):
        self.scale = 0
        self.bot = TwitterBot(0)
        self.isActive = True
        self.mainThread = Thread(target=self.startProgram, args=())
        # self.commandThread = Thread(target=self.doCommand, args=())
        # self.mainThread.start()
        # self.commandThread.join()

    def scrollTo(self, scale):
        if scale >= self.scale:
            for i in range(scale - self.scale):
                self.scale += 8
                self.bot.getDriver().execute_script(f'window.scrollTo(0,{self.scale})')
                miniSleep()
        else:
            for i in range(self.scale - scale):
                self.scale -= 8
                self.bot.getDriver().execute_script(f'window.scrollTo(0,{self.scale})')
                miniSleep()

    def scroll(self, scale):
        for i in range(scale):
            self.scale += 8
            self.bot.getDriver().execute_script(f'window.scrollTo(0,{self.scale})')
            miniSleep()

    def setActive(self, isActive):
        self.isActive = isActive

    def startProgram(self):
        twitterBot = self.bot
        twitterBot.login()
        while True:
            while self.isActive:
                try:
                    articles = twitterBot.listArticles()
                    for article in articles:
                        chance, lim = twitterBot.doILikeArticle(article)
                        if chance == 20:
                            break
                        if chance >= lim:
                            for j in range(3):
                                twitterBot.followUser()
                            twitterBot.like(article)
                        else:
                            systemLog("I don't like this article!", color=Fore.LIGHTRED_EX)
                            takeABreath()
                        self.scroll(50)
                except:
                    time.sleep(1)
                    break
            time.sleep(2)

    def start(self):
        self.isActive = True
        self.mainThread.start()

    def stop(self):
        self.isActive = False
        self.mainThread.join()

    def doCommand(self):
        while True:
            try:
                command = input(Fore.BLACK + "# Enter command: ")
                if command == "login":
                    self.bot.login()
                elif command == "logout":
                    self.bot.logout()
                elif command == "create account":
                    self.bot.createNewAccount()
                elif command == "start":
                    self.start()
                elif command == "stop":
                    self.stop()
                elif command == "scroll down":
                    self.scroll(100)
                elif command == "scroll up":
                    self.scroll(-100)
                elif command.split()[0] == "like":
                    self.bot.like(self.bot.listArticles()[stringToInt(command.split()[1])])
                elif command.split()[0] == "search":
                    self.bot.search(command.replace("search ", ""))
                elif command.split()[0] == "post":
                    self.bot.postTweet(command.replace("post ", ""))
                else:
                    systemLog("- Unknown command!", color=Fore.RED)
            except Exception as e:
                systemLog(e)

    def autoStart(self):
        self.bot.login()
        self.bot.like(50)
        self.bot.logout()

    def startBot(self):
        self.mainThread.start()
        # self.doCommand()
        # self.autoStart()
