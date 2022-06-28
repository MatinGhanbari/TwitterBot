from selenium import webdriver
from selenium.webdriver.common import keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from random import Random
from colorama import Fore
import time
import json
import re


class TwitterBot:
    def __init__(self, email=None, password=None, username=None, accountNumber=None):
        chromeWebDriverPath = "C:\Program Files\Google\Chrome\chromedriver.exe"  # Google Chrome driver path
        driver = webdriver.Chrome(chromeWebDriverPath)
        acc = ''
        if email is None or password is None or username is None:
            file = open('data/accounts', 'r')
            for i in range(accountNumber):
                acc = file.readline().replace("\n", "")
            [email, password, username] = acc.split(":")
        self.systemLog(f"Email: \"{email}\" | Password: \"{password}\" | Username: \"{username}\"", color=Fore.BLUE)
        self.email = email
        self.username = username
        self.password = password
        self.bot = driver
        self.bot.set_window_size(450, 800)
        self.bot.set_window_position(975, 25)
        self.wait = WebDriverWait(driver, 5)
        self.XPaths = json.load(open('data/XPaths.json'))
        self.scroll = 100

    def login(self):
        self.bot.get('https://twitter.com/login')

        try:
            emailField = self.wait.until(
                EC.visibility_of_element_located((By.XPATH, self.XPaths['login']['emailField'])))
            emailField.clear()
            self.takeABreath(max=1)
            self.sendKeys(emailField, self.email)
            self.takeABreath(max=3)
            emailField.send_keys(keys.Keys.RETURN)
            self.systemLog(message="Successfully email field filled!", color=Fore.YELLOW)
        except Exception as e:
            self.systemLog(message=f"Unable to find email field", color=Fore.RED)

        self.takeABreath(max=2)
        try:
            usernameField = self.wait.until(
                EC.visibility_of_element_located((By.XPATH, self.XPaths['login']['usernameField'])))
            usernameField.clear()
            self.takeABreath(max=2)
            self.sendKeys(usernameField, self.username)
            self.takeABreath(max=4)
            usernameField.send_keys(keys.Keys.RETURN)
            self.systemLog(message="Successfully username field filled!", color=Fore.YELLOW)
        except Exception as e:
            self.systemLog(message="Unable to find username field", color=Fore.RED)

        self.takeABreath(max=1)
        try:
            passwordField = self.wait.until(
                EC.visibility_of_element_located((By.XPATH, self.XPaths['login']['passwordField'])))
            passwordField.clear()
            self.takeABreath(max=2)
            self.sendKeys(passwordField, self.password)
            self.takeABreath(max=4)
            passwordField.send_keys(keys.Keys.RETURN)
            self.systemLog(message="Successfully password field filled!", color=Fore.YELLOW)
        except Exception as e:
            self.systemLog(message="Unable to find password field", color=Fore.RED)

    def logout(self):
        try:
            profile = self.wait.until(EC.visibility_of_element_located((By.XPATH, self.XPaths['account']['profile'])))
            profile.click()
            self.systemLog(message="Successfully profile button found!")
        except Exception as e:
            self.systemLog(message="Unable to find profile in account page", color=Fore.RED)
            return

        self.takeABreath()

        try:
            logout = self.wait.until(EC.visibility_of_element_located((By.XPATH, self.XPaths['account']['logout'])))
            logout.click()
            self.systemLog(message="Successfully logout button found!")
        except Exception as e:
            self.systemLog(message="Unable to find logout in profile", color=Fore.RED)
            return

            self.takeABreath()

        try:
            confirmLogOut = self.wait.until(
                EC.visibility_of_element_located((By.XPATH, self.XPaths['account']['confirmLogOut'])))
            confirmLogOut.click()
            self.systemLog(message="Successfully confirm Logout button found!")
        except Exception as e:
            self.systemLog(message="Unable to find confirmLogOut in logout", color=Fore.RED)
            return

    def listTweets(self):
        source = self.bot.page_source
        pattern = '\<article aria\-labelledby\=\"(.*?)\"'
        return findAllMatches(pattern, source)

    def getLikeButtonXPath(self, tweetNumber=0):
        likeId = self.listTweets()[tweetNumber].split()[16]
        path = f"//*[@id=\"{likeId}\"]/div[3]/div/div"
        return path

    def getLikesCountXPath(self, tweetNumber=0):
        likeId = self.listTweets()[tweetNumber].split()[16]
        path = f"//*[@id=\"{likeId}\"]/div[3]/div/div/div[2]/span/span/span"
        return path

    def getCommentButtonXPath(self, tweetNumber=0):
        likeId = self.listTweets()[tweetNumber].split()[16]
        path = f"//*[@id=\"{likeId}\"]/div[1]/div/div"
        return path

    def getCommentCountXPath(self, tweetNumber=0):
        likeId = self.listTweets()[tweetNumber].split()[16]
        path = f"//*[@id=\"{likeId}\"]/div[1]/div/div/div[2]/span/span/span"
        return path

    def getCommentFieldXPath(self):
        path = '//*[@id="react-root"]/div/div/div[2]/main/div/div/div[3]/div/div/div[2]/div/div/div/div/div[2]/div[' \
               '1]/div/div/div/div/div/div/div/div/div/label/div[1]/div/div/div/div/div[2]/div/div/div/div'
        return path

    def getSendCommentButtonXPath(self):
        path = '//*[@id="react-root"]/div/div/div[2]/main/div/div/div[2]/div/div/div/div/div[3]/div/div'
        return path

    def getShareButtonXPath(self, tweetNumber=0):
        likeId = self.listTweets()[tweetNumber].split()[16]
        path = f"//*[@id=\"{likeId}\"]/div[4]/div/div"
        return path

    def getShareDirectMessageButtonXPath(self):
        path = '//*[@id="layers"]/div[2]/div/div/div/div[2]/div[3]/div/div/div/div[1]'
        return path

    def getShareBookmarkButtonXPath(self):
        path = '//*[@id="layers"]/div[2]/div/div/div/div[2]/div[3]/div/div/div/div[2]'
        return path

    def getShareCopyLinkButtonXPath(self):
        path = '//*[@id="layers"]/div[2]/div/div/div/div[2]/div[3]/div/div/div/div[3]'
        return path

    def getRetweetButtonXPath(self, tweetNumber=0):
        likeId = self.listTweets()[tweetNumber].split()[16]
        path = f"//*[@id=\"{likeId}\"]/div[2]/div/div"
        return path

    def getRetweetCountXPath(self, tweetNumber=0):
        likeId = self.listTweets()[tweetNumber].split()[16]
        path = f"//*[@id=\"{likeId}\"]/div[2]/div/div/div[2]/span/span/span"
        return path

    def getRetweetRetweetButtonXPath(self):
        path = '//*[@id="layers"]/div[2]/div/div/div/div[2]/div[3]/div/div/div/div'
        return path

    def getRetweetQuoteButtonXPath(self):
        path = '//*[@id="layers"]/div[2]/div/div/div/div[2]/div[3]/div/div/div/a'
        return path

    def getTweetTextXPath(self, tweetNumber=0):
        likeId = self.listTweets()[tweetNumber].split()[10]
        path = f"//*[@id=\"{likeId}\"]/span"
        return path

    def getTweetSenderNameXPath(self, tweetNumber=0):
        likeId = self.listTweets()[tweetNumber].split()[4]
        path = f"//*[@id=\"{likeId}\"]/div[1]/div/a/div/div[1]/span/span"
        return path

    def getTweetSenderUsernameXPath(self, tweetNumber=0):
        likeId = self.listTweets()[tweetNumber].split()[4]
        path = f"//*[@id=\"{likeId}\"]/div[2]/div/div/a/div/span"
        return path

    def getTweetSendTimeXPath(self, tweetNumber=0):
        likeId = self.listTweets()[tweetNumber].split()[7]
        path = f"//*[@id=\"{likeId}\"]/time"
        return path

    def getTweetMediaXPath(self, tweetNumber=0):  # todo : complete function!
        # likeId = self.listTweets()[tweetNumber].split()[11]
        # path = f"//*[@id=\"{likeId}\"]/div/div/div/div/div[2]"
        # return path
        pass

    def like_tweets(self, likes=Random().randrange(start=1, stop=5, step=1)):
        bot = self.bot

        # try:
        #     explore = self.wait.until(
        #         EC.visibility_of_element_located((By.XPATH, self.XPaths['account']['home'])))
        #     explore.click()
        #     self.systemLog(message="Successfully home button clicked!", color=Fore.YELLOW)
        #     self.takeABreath()
        # except Exception as e:
        #     self.systemLog(message="Unable to click home in account", color=Fore.RED)
        #     return

        for i in range(likes):
            try:
                self.systemLog(message=f"Read tweets! tweet number: {i}", color=Fore.MAGENTA)
                self.takeABreath(min=2, max=4.5)  # Read tweets
                like = self.wait.until(
                    EC.visibility_of_element_located((By.XPATH, self.getLikeButtonXPath(i))))
                if self.likePreference(i):
                    like.click()  # Like it
                    self.systemLog(message=f"Successfully like button clicked! tweet number: {i}", color=Fore.GREEN)
                else:
                    self.systemLog(message=f"You don't like this tweet! tweet number: {i}", color=Fore.CYAN)
                self.scroll = self.scroll + 500
                bot.execute_script(f'window.scrollTo(0,{self.scroll})')
                self.takeABreath()
            except Exception as e:
                print(e)
                self.takeABreath(max=1.5)
                self.scroll = self.scroll + 500
                bot.execute_script(f'window.scrollTo(0,{self.scroll})')
                self.takeABreath(min=2, max=4.5)  # Read tweets
                like = self.wait.until(
                    EC.visibility_of_element_located((By.XPATH, self.getLikeButtonXPath(i))))
                if self.likePreference(i):
                    like.click()  # Like it
                    self.systemLog(message=f"Successfully like button clicked! tweet number: {i}", color=Fore.GREEN)
                else:
                    self.systemLog(message=f"You don't like this tweet! tweet number: {i}", color=Fore.CYAN)

        self.scroll = self.scroll + 1000
        bot.execute_script(f'window.scrollTo(0,{self.scroll})')

    def search(self, searchText=''):
        self.takeABreath()
        try:
            explore = self.wait.until(
                EC.visibility_of_element_located((By.XPATH, self.XPaths['account']['explore'])))
            explore.click()
            self.takeABreath()
            searchBar = self.wait.until(
                EC.visibility_of_element_located((By.XPATH, self.XPaths['account']['searchBar'])))
            searchBar.click()
            self.takeABreath()
            searchBar.clear()
            self.takeABreath(max=2)
            self.sendKeys(searchBar, searchText)
            self.takeABreath()
            searchBar.send_keys(keys.Keys.RETURN)
            self.takeABreath()
            self.systemLog(message=f"Successfully \"{searchText}\" searched!", color=Fore.GREEN)
        except Exception as e:
            self.systemLog(message="Unable to search in explore", color=Fore.RED)
            return

    def post_tweets(self, tweet=''):
        try:
            writeTweet = self.wait.until(
                EC.visibility_of_element_located((By.XPATH, self.XPaths['account']['writeTweet'])))
            writeTweet.click()
            self.systemLog(message="Successfully writeTweet button clicked!", color=Fore.GREEN)
        except Exception as e:
            self.systemLog(message="Unable to find writeTweet in account", color=Fore.RED)
            return

        self.takeABreath()

        try:
            writeTweetBody = self.wait.until(
                EC.visibility_of_element_located((By.XPATH, self.XPaths['account']['writeTweetBody'])))
            writeTweetBody.click()
            self.takeABreath()
            writeTweetBody.clear()
            self.takeABreath(max=1.2)
            self.sendKeys(writeTweetBody, tweet)
            self.systemLog(message=f"Successfully tweet \"{tweet}\" wrote!")
        except Exception as e:
            self.systemLog(message="Unable to find writeTweetBody in account", color=Fore.RED)
            return

        self.takeABreath()

        try:
            postTweet = self.wait.until(
                EC.visibility_of_element_located((By.XPATH, self.XPaths['account']['postTweet'])))
            postTweet.click()
            self.takeABreath()
            self.systemLog(message="Successfully tweet posted!", color=Fore.GREEN)
        except Exception as e:
            self.systemLog(message="Unable to post tweet", color=Fore.RED)
            return

    def systemLog(self, message, time=time.strftime("%Y/%m/%d %H:%M:%S"), saveToLog=False, printToConsole=True,
                  color=Fore.BLACK):
        out = f"# [{time}] Message: {message}"
        if printToConsole:
            print(color + out)
        if saveToLog:
            file = open('data/log', 'a+')
            print(out, file=file)

    def takeABreath(self, min=1.5, max=7):
        rand = Random(Random(Random(Random().random()).random()).random()).uniform(a=min, b=max)
        # self.systemLog(f"Bot Will Breath {round(rand, 2)} seconds")
        time.sleep(rand)

    def sendKeys(self, element, keys=''):
        for c in keys:
            element.send_keys(c)
            self.takeABreath(min=0, max=0.2)

    def likePreference(self, tweetNumber):
        preference = json.load(open('data/preference.json'))
        maxChance = 16

        tweetSenderName = self.bot.find_element(by=By.XPATH, value=self.getTweetSenderNameXPath(tweetNumber)).text
        for tweetKey in list(preference['like']['senderName']):
            if tweetKey in tweetSenderName.lower():
                if preference['like']['senderName'][tweetKey] > maxChance:
                    maxChance = preference['like']['senderName'][tweetKey]

        tweetSenderUsername = self.bot.find_element(by=By.XPATH,
                                                    value=self.getTweetSenderUsernameXPath(tweetNumber)).text
        for tweetKey in list(preference['like']['senderUsername']):
            if tweetKey in tweetSenderUsername.lower():
                if preference['like']['senderUsername'][tweetKey] > maxChance:
                    maxChance = preference['like']['senderUsername'][tweetKey]

        tweetSendTime = self.bot.find_element(by=By.XPATH, value=self.getTweetSendTimeXPath(tweetNumber)).text
        for tweetKey in list(preference['like']['sendTime']):
            if tweetKey in tweetSendTime.lower():
                maxChance += preference['like']['sendTime'][tweetKey]

        tweetText = self.bot.find_element(by=By.XPATH, value=self.getTweetTextXPath(tweetNumber)).text
        for tweetKey in list(preference['like']['tweetText']):
            if tweetKey in tweetText.lower():
                if preference['like']['tweetText'][tweetKey] > maxChance:
                    maxChance = preference['like']['tweetText'][tweetKey]

        # likeCounts = self.bot.find_element(by=By.XPATH, value=self.getLikesCountXPath(tweetNumber)).text
        # for tweetKey in list(preference['like']['likesCount']):
        #     if toFloat(tweetKey) < toFloat(likeCounts):
        #         maxChance += preference['like']['commentsCounts'][tweetKey]
        #
        # commentCounts = self.bot.find_element(by=By.XPATH, value=self.getCommentCountXPath(tweetNumber)).text
        # for tweetKey in list(preference['like']['commentsCounts']):
        #     if toFloat(tweetKey) < toFloat(commentCounts):
        #         maxChance += preference['like']['commentsCounts'][tweetKey]
        #
        # retweetCounts = self.bot.find_element(by=By.XPATH, value=self.getRetweetCountXPath(tweetNumber)).text
        # for tweetKey in list(preference['like']['retweetsCounts']):
        #     if toFloat(tweetKey) < toFloat(retweetCounts):
        #         maxChance += preference['like']['commentsCounts'][tweetKey]

        self.systemLog(f"like maxChance: {maxChance} | Random: {round(Random().random() * 100)}")
        if maxChance >= round(Random().random() * 80):
            return True  # tweet will likes
        return False


def findAllMatches(regex, source):
    match_list = []
    while True:
        match = re.search(regex, source)
        if match:
            match_list.append(match.group(1))
            source = source[match.end():]
        else:
            return match_list


def toFloat(string):
    string = string.replace(",", "")
    if 'K' in string:
        return float(string.replace("K", "")) * 1000
    elif 'M' in string:
        return float(string.replace("M", "")) * 1000000
    return float(string)
