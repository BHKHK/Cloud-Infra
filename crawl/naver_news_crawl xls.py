import requests
import re
from bs4 import BeautifulSoup
import pandas as pd


def crawl_naver_news():
    url = "https://news.naver.com"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    news_items = []
    news_cards = soup.select('div .cjs_channel_card')
    for item in news_cards:
        title = item.select_one('div.cjs_t')
        if title:
            title = title.text.strip()
        else:
            title = "제목 없음"
        
        publisher_time = item.select_one('h4.channel')
        if publisher_time:
            publisher_time_text = publisher_time.text.strip()
            # 신문사 이름과 시간 분리
            publisher_match = re.match(r'^([^\d]+)', publisher_time_text) # 첫 숫자가 나타나기 이전을 잘라서 표시
            time_match = re.search(r'(\d{2})월 (\d{2})일 (\d{2}:\d{2})', publisher_time_text)
            
            if publisher_match:
                publisher = publisher_match.group(1).strip()
            else:
                publisher = "언론사 정보 없음"
            
            if time_match:
                time = f"{time_match.group(1)}월 {time_match.group(2)}일 {time_match.group(3)}"
            else:
                time = "시간 정보 없음"
        else:
            publisher = "언론사 정보 없음"
            time = "시간 정보 없음"
        
        news_items.append({
            'title': title,
            'time': time,
            'publisher': publisher,
        })
    
    df = pd.DataFrame(news_items) # 이미 딕셔너리 처리가 되어있는 뉴스아이템은 데이터프레임에서 자동으로 변환해준다. 개꿀
    
    df.to_excel('./naver_news_scrape.xlsx', sheet_name='Sheet1', index=False)

    print("뉴스 스크랩이 'naver_news_scrape.xlsx'에 저장되었습니다.")

if __name__ == "__main__":
    crawl_naver_news()
