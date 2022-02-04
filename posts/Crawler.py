import asyncio
import aiohttp
import urllib
from bs4 import BeautifulSoup
import re
import time

class NBA_Crawler:
    
    def __init__(self,max_jump=10,root="https://www.ptt.cc/bbs/NBA/index.html",keywords = ["Westbrook","龜","龜龜","西河","衛少"]):
        self.max_jump = max_jump
        self.root = root
        self.domain = "https://www.ptt.cc"
        self.seen_page = set()
        self.keywords = keywords
        self.results = []
        self.pages=[]

    def find_keywords(self,string):
        found = -1
        for keyword in self.keywords:
            if string.count(keyword)>0:
                found = 1
                return string
        return found
    
    async def view_page(self,url):
        
        next_page = None
        async with aiohttp.ClientSession() as session:
            async with await session.get(url) as response:
                assert response.status == 200
                
                doc = await response.text()
                soup = BeautifulSoup(re.sub("<!--|-->","", doc),"lxml") #ignore comments
                
                #search related topics
                topics = soup.find_all("div",class_="r-ent")
                outcomes=[]
                await asyncio.sleep(0.5)
                for topic in topics:
                    title = topic.find("div",class_="title").find("a")
                    if title is not None:
                        outcomes.append(self.find_keywords(title.string))
                        
                for outcome in outcomes:
                     if outcome !=-1:
                         self.results.append(outcome)

                return response.status

    async def all_pages(self,root):
        async with aiohttp.ClientSession() as session:
            async with await session.get(root) as response:
                assert response.status==200

                text = await response.text()
                soup = BeautifulSoup(re.sub("<!--|-->","", text),"lxml")
                main_container = soup.find("div",class_="r-ent")
                action_bar = soup.find("div",class_="action-bar")
                bars = action_bar.find_all("a",class_= "btn wide")
                
                for bar in bars:
                    if bar.string.count("上頁")>0:
                        self.pages.append(self.domain+bar["href"])
                        if(len(self.pages)>=self.max_jump):
                            return True
                        await self.all_pages(self.domain+bar["href"])
                        return True
                return False
    
    async def crawl(self):
        tasks=[]
        if(await self.all_pages(self.root)):
            for page in self.pages:
                tasks.append(self.view_page(page))
            outcome = await asyncio.gather(*tasks,return_exceptions=True)
        else:
            print("fail")

# if __name__ == "__main__":
#     start = time.time()
#     keywords = []
#     keywords.append('幹')
#     crawler = NBA_Crawler(keywords=keywords)
#     # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
#     asyncio.run(crawler.crawl())
#     end = time.time()
#     process_time = end-start
#     for result in crawler.results:
#         print(result)
#     print(process_time)