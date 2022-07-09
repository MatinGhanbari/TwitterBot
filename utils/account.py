class TwitterAccount:
    def __init__(self, accountID: int):
        self.accountID = accountID
        file = open('core/accounts', 'r')
        accountsList = file.readlines()
        [self.email, self.password, self.username] = accountsList[accountID].replace("\n", "").split(":")

    def getEmail(self):
        return self.email

    def getPassword(self):
        return self.password

    def getUsername(self):
        return self.username

    def deleteAccount(self):
        try:
            with open('core/accounts', 'r') as file:
                wholeAccounts = file.readlines()
                wholeAccounts.remove(wholeAccounts[self.accountID])
            with open('core/accounts', 'w') as file:
                for line in wholeAccounts:
                    file.write(line)
        except Exception as e:
            print(e)

    def addAccount(self, email, password, username):
        accountID = self.accountID
        try:
            with open('core/accounts', 'a+') as file:
                file.write(f"\n{email}:{password}:{username}")
        except Exception as e:
            print(e)


if __name__ == '__main__':
    pass
