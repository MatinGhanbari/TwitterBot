import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

from utils.account import TwitterAccount
from utils.utils import *


class TwitterBot:
    def __init__(self, accountNumber=0):
        self.preference = json.load(open('core/preference.json', 'r', encoding='utf-8'))
        self.paths = json.load(open('core/paths.json', 'r', encoding='utf-8'))
        self.driver = webdriver.Chrome(self.paths['chromeDriver'])
        self.account = TwitterAccount(accountNumber)
        self.driver.set_window_size(450, 800)
        self.driver.set_window_position(975, 25)
        self.wait = WebDriverWait(self.driver, 5)
        self.driver.set_page_load_timeout(30)

    def getDriver(self):
        return self.driver

    def findElementByXPath(self, xpath):
        try:
            return self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        except:
            return None

    def findElementById(self, id):
        try:
            return self.wait.until(EC.visibility_of_element_located((By.ID, id)))
        except:
            return None

    def findElementByText(self, text):
        try:
            return self.wait.until(EC.visibility_of_element_located((By.XPATH, f"//*[text()='{text}']")))
        except:
            return None

    def findElementContainsText(self, text):
        try:
            return self.wait.until(EC.visibility_of_element_located((By.XPATH, f"//*[contains(text(),'{text}')]")))
        except:
            return None

    def login(self):
        bot = self.driver
        bot.get('https://twitter.com/login')

        fill(self.findElementByXPath(self.paths['login']['emailField']), self.account.getEmail(), "email")
        fill(self.findElementByXPath(self.paths['login']['usernameField']), self.account.getUsername(), "username")
        fill(self.findElementByXPath(self.paths['login']['passwordField']), self.account.getPassword(), "password")

    def logout(self):
        click(self.driver, self.findElementByXPath(self.paths['account']['profile']))
        click(self.driver, self.findElementByXPath(self.paths['account']['logout']))
        click(self.driver, self.findElementByXPath(self.paths['account']['confirmLogOut']))

    def goToHome(self):
        click(self.driver, self.findElementByXPath(self.paths['account']['home']))

    def goToExplore(self):
        click(self.driver, self.findElementByXPath(self.paths['account']['explore']))

    def goToMyProfile(self):
        click(self.driver, self.findElementByXPath(self.paths['account']['info']))

    def goToEditProfile(self):
        click(self.driver, self.findElementByXPath(self.paths['info']['editProfile']))

    def goToMyTweets(self):
        click(self.driver, self.findElementByXPath(self.paths['info']['tweets']))

    def goToMyReplies(self):
        click(self.driver, self.findElementByXPath(self.paths['info']['replies']))

    def goToMyMedia(self):
        click(self.driver, self.findElementByXPath(self.paths['info']['media']))

    def followUser(self):
        click(self.driver, self.findElementByText("Follow"))

    def unfollowUser(self):
        click(self.driver, self.findElementByText("Following"))
        click(self.driver, self.findElementByText("Unfollow"))

    def listArticles(self):
        source = self.driver.page_source
        pattern = '\<article aria\-labelledby\=\"(.*?)\"'
        return findAllRegexMatches(pattern, source)

    def changeProfileInfo(self, newName=None, newBio=None, newLocation=None, newWebsite=None):
        if newName is not None:
            fill(self.findElementByXPath(self.paths['editProfile']['name']), newName)

        if newBio is not None:
            fill(self.findElementByXPath(self.paths['editProfile']['bio']), newName)

        if newLocation is not None:
            fill(self.findElementByXPath(self.paths['editProfile']['location']), newName)

        if newWebsite is not None:
            fill(self.findElementByXPath(self.paths['editProfile']['website']), newName)

    def search(self, searchText):
        click(self.driver, self.findElementByXPath(self.paths['account']['explore']))
        fill(self.findElementByXPath(self.paths['account']['searchBar']), searchText)

    def postTweet(self, tweet):
        click(self.driver, self.findElementByXPath(self.paths['account']['writeTweet']))
        fill(self.findElementByXPath(self.paths['account']['writeTweetBody']), tweet)
        click(self.driver, self.findElementByXPath(self.paths['account']['postTweet']))

    def like(self, article):
        click(self.driver, self.findElementByXPath(getLikeButtonXPath(article)))

    def retweet(self, article):
        click(self.driver, self.findElementByXPath(getRetweetButtonXPath(article)))
        click(self.driver, self.findElementByXPath(getRetweetQuoteButtonXPath()))

    def doILikeArticle(self, article, startChance=20):
        preference = self.preference
        chance = startChance
        try:
            tweetSenderName = self.findElementByXPath(getTweetSenderNameXPath(article)).text
            for tweetKey in list(preference['like']['senderName']):
                if tweetKey in tweetSenderName.lower():
                    chance += preference['like']['senderName'][tweetKey]
                    # systemLog(f"{tweetSenderName} Adds {preference['like']['senderName'][tweetKey]} to chance",
                    #           color=Fore.BLACK)
        except Exception as e:
            systemLog("tweetSenderName Ignored!", color=Fore.BLACK)

        try:
            tweetSenderUsername = self.findElementByXPath(getTweetSenderUsernameXPath(article)).text
            for tweetKey in list(preference['like']['senderUsername']):
                if tweetKey in tweetSenderUsername.lower():
                    chance += preference['like']['senderUsername'][tweetKey]
                    # systemLog(f"{tweetSenderUsername} Adds {preference['like']['senderUsername'][tweetKey]} to chance",
                    #           color=Fore.BLACK)
        except Exception as e:
            systemLog("tweetSenderUsername Ignored!", color=Fore.BLACK)

        try:
            tweetSendTime = self.findElementByXPath(getTweetSendTimeXPath(article)).text
            for tweetKey in list(preference['like']['sendTime']):
                if tweetKey in tweetSendTime.lower():
                    chance += preference['like']['sendTime'][tweetKey]
                    # systemLog(f"{tweetSendTime} Adds {preference['like']['sendTime'][tweetKey]} to chance",
                    #           color=Fore.BLACK)
        except Exception as e:
            systemLog("tweetSendTime Ignored!", color=Fore.BLACK)

        try:
            tweetText = self.findElementByXPath(getTweetTextXPath(article)).text
            for tweetKey in list(preference['like']['tweetText']):
                if tweetKey in tweetText.lower():
                    chance += preference['like']['tweetText'][tweetKey]
                    # systemLog(f"{tweetText} Adds {preference['like']['tweetText'][tweetKey]} to chance",
                    #           color=Fore.BLACK)
        except Exception as e:
            systemLog("tweetText Ignored!", color=Fore.BLACK)

        try:
            likeCounts = self.findElementByXPath(getLikesCountXPath(article)).text
            for tweetKey in list(preference['like']['likesCount']):
                if stringToFloat(tweetKey) < stringToFloat(likeCounts):
                    chance += preference['like']['likesCount'][tweetKey]
                    # systemLog(f"{likeCounts} Adds {preference['like']['likesCount'][tweetKey]} to chance",
                    #           color=Fore.BLACK)
        except Exception as e:
            systemLog("likeCounts Ignored!", color=Fore.BLACK)

        try:
            commentCounts = self.findElementByXPath(getCommentCountXPath(article)).text
            for tweetKey in list(preference['like']['commentsCounts']):
                if stringToFloat(tweetKey) < stringToFloat(commentCounts):
                    chance += preference['like']['commentsCounts'][tweetKey]
                    # systemLog(f"{commentCounts} Adds {preference['like']['commentsCounts'][tweetKey]} to chance",
                    #           color=Fore.BLACK)
        except Exception as e:
            systemLog("commentCounts Ignored!", color=Fore.BLACK)

        try:
            retweetCounts = self.findElementByXPath(getRetweetCountXPath(article)).text
            for tweetKey in list(preference['like']['retweetsCounts']):
                if stringToFloat(tweetKey) < stringToFloat(retweetCounts):
                    chance += preference['like']['retweetsCounts'][tweetKey]
                    # systemLog(f"{retweetCounts} Adds {preference['like']['retweetsCounts'][tweetKey]} to chance",
                    #           color=Fore.BLACK)
        except Exception as e:
            systemLog("retweetCounts Ignored!", color=Fore.BLACK)
        try:
            if chance >= 85:
                click(self.driver, self.findElementByXPath(getRetweetButtonXPath(article)))
                click(self.driver, self.findElementByXPath(getRetweetRetweetButtonXPath()))
        except Exception as e:
            systemLog("Can't Retweet now!", color=Fore.RED)

        rnd = round(Random().random() * 80)
        systemLog(f"chance: {chance} | Limit: {rnd}")
        return chance, rnd

    def createNewAccount(self):
        self.driver.get("https://twitter.com/signup")
        systemLog("Twitter SignUp opened!")
        click(self.driver, self.findElementByXPath(self.paths['createAccount']['signWithEmail']), 'signWithEmail')
        fill(self.findElementByXPath(self.paths['createAccount']['nameField']), generateNewName(), 'nameField')
        click(self.driver, self.findElementByXPath(self.paths['createAccount']['useEmailButton']), 'useEmailButton')
        newMail = self.generateNewMail()
        fill(self.findElementByXPath(self.paths['createAccount']['emailField']), newMail, 'emailField')
        click(self.driver, self.findElementByXPath(self.paths['createAccount']['monthSelector']), 'monthSelector')
        click(self.driver, self.findElementByText(generateMonth()), 'monthSelector')
        click(self.driver, self.findElementByXPath(self.paths['createAccount']['daySelector']), 'daySelector')
        click(self.driver, self.findElementByText(generateDay()), 'daySelector')
        click(self.driver, self.findElementByXPath(self.paths['createAccount']['yearSelector']), 'yearSelector')
        click(self.driver, self.findElementByText(generateYear()), 'yearSelector')
        click(self.driver, self.findElementByText("Next"))
        click(self.driver, self.findElementByText("Sign Up"))
        vCode = self.getVCode()
        fill(self.findElementByXPath(self.paths['createAccount']['vCode']), vCode, 'vCode')
        click(self.driver, self.findElementByText("Next"))
        newPassword = generateNewPass()
        fill(self.findElementByXPath(self.paths['createAccount']['passwordField']), newPassword, 'passwordField')
        click(self.driver, self.findElementByText("Next"))
        click(self.driver, self.findElementContainsText("Skip"))
        click(self.driver, self.findElementContainsText("Skip"))
        username = self.findElementByXPath(self.paths['createAccount']['usernameField']).text
        click(self.driver, self.findElementByText("Skip"))
        click(self.driver, self.findElementContainsText("Skip"))
        for i in range(Random().randint(a=3, b=7)):
            click(self.driver, self.findElementByText(getRandomFavorites()))
        click(self.driver, self.findElementByText("Next"))
        click(self.driver, self.findElementByText("Next"))
        for i in range(Random().randint(a=1, b=4)):
            self.followUser()
        click(self.driver, self.findElementByText("Next"))
        click(self.driver, self.findElementContainsText("Skip"))
        systemLog(f"Account Created: [{newMail}:{newPassword}:{username}]")
        self.account.addAccount(newMail, newPassword, username)

    def generateNewMail(self) -> str:
        mail = requests.get("https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1").json()[0]
        return mail

    def getVCode(self, mail) -> str:
        data = requests.get(
            "https://www.1secmail.com/api/v1/?action=getMessages&login=" + mail[:mail.find("@")] + "&domain="
            + mail[mail.find("@") + 1:]).json()[0]
        return data[0]['subject'].split()[0]
