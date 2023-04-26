import requests as rq
from bs4 import BeautifulSoup
from .models import Session

LOGIN_URL = "https://varank.hrstop.com/Account/Login?ReturnUrl=%2FDashboard%2FIndex"
DASHBOARD_URL = "https://varank.hrstop.com/Dashboard/Index"
PUNCH_URL = "https://varank.hrstop.com/MyHome/MyProfile?handler=PunchTimeOut&{}"
        

HEADERS = {
    'Host': 'varank.hrstop.com',
    'Content-Length': '248',
    'Cache-Control': 'max-age=0',
    'Sec-Ch-Ua': '',
    'Sec-Ch-Ua-Mobile': '',
    'Sec-Ch-Ua-Platform': '',
    'Upgrade-Insecure-Requests': '',
    'Origin': '',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': '',
    'Accept': '',
    'Sec-Fetch-Site': '',
    'Sec-Fetch-Mode': '',
    'Sec-Fetch-User': '',
    'Sec-Fetch-Dest': '',
    'Referer': 'https://varank.hrstop.com/Account/Login?ReturnUrl=%2FDashboard%2FIndex'
}


class PunchHttpRequest:
    
    def getRequiredLoginData(self):
        resp = rq.get(url = LOGIN_URL)
        self._csrfToken = resp.cookies.get(".AspNetCore.Antiforgery.OGpdCikpHUU")
        soup = BeautifulSoup(resp.text, 'html.parser')
        self._requestToken = soup.find('input', {'name': '__RequestVerificationToken'})["value"]
        resp.close()
    
    def getCSRFToken(self,url):
        resp = rq.get(url = url)
        self._csrfToken = resp.cookies.get(".AspNetCore.Antiforgery.OGpdCikpHUU")
        resp.close()
    
    def login(self,email,password):
        
        self.getRequiredLoginData()
        
        formData = {}
        formData["Email"] = email
        formData["Password"]=password
        formData["__RequestVerificationToken"]=self._requestToken
        
        COOKIES = {
            '.AspNetCore.Antiforgery.OGpdCikpHUU': self._csrfToken,
        }     
        resp = rq.post(url=LOGIN_URL, data=formData,cookies=COOKIES, headers=HEADERS,allow_redirects=False)
        self.session = resp.cookies.get(".AspNetCore.Cookies")
        
        person = Session(email=self.email, password=self.password, token = self.session)
        person.save()
        
        resp.close()
        
    def sessionFromDb(self):
        data = Session.objects.filter(email=self.email,password=self.password)
        if data.exists():
            self.session = data.values('token')[0]['token']
            return True
        return False
    
    def makePunch(self,email,password):
        self.email = email
        self.password = password
        tokenExists = self.sessionFromDb()
        if tokenExists == False:
            self.login(email, password)
        
        COOKIES = {
            ".AspNetCore.Cookies" : self.session 
        }
        
        resp = rq.get(url=PUNCH_URL,cookies=COOKIES)
        success = len(resp.text)
        resp.close()
        return 1 if success > 100 else 0
        
    # def makePunch(self):
        
        
# HttpRequestMaker().login("","")

if __name__ == '__main__':
    PunchHttpRequest().makePunch('pandey.abhishek@vesimplify.com','185880V7')