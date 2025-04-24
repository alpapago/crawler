from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

def test_tag_crawler(url, tag_name, driver_path=None):
    """
    웹 페이지의 특정 태그 정보를 크롤링하는 함수
    
    Args:
        url (str): 크롤링할 웹 페이지 URL (내부망 URL도 가능)
        tag_name (str): 찾을 HTML 태그 (예: 'div', 'a', 'p', 'h1' 등)
        driver_path (str, optional): 크롬 드라이버 경로. 기본값은 None.
    
    Returns:
        list: 찾은 태그들의 텍스트 정보 리스트
    """
    # 크롬 옵션 설정
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    # 필요시 헤드리스 모드(화면 표시 없음)
    # chrome_options.add_argument('--headless')
    
    # 서비스 및 드라이버 설정
    if driver_path:
        service = Service(executable_path=driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
    else:
        # 드라이버 경로를 지정하지 않으면 시스템 PATH에서 검색
        driver = webdriver.Chrome(options=chrome_options)
    
    results = []
    
    try:
        # 웹 페이지 접속
        print(f"접속 중: {url}")
        driver.get(url)
        
        # 페이지 로딩 대기 (최대 10초)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # 페이지 title 출력
        print(f"페이지 제목: {driver.title}")
        
        # 지정된 태그 검색
        elements = driver.find_elements(By.TAG_NAME, tag_name)
        print(f"찾은 {tag_name} 태그 수: {len(elements)}")
        
        # 태그 정보 수집
        for i, element in enumerate(elements[:10]):  # 처음 10개만 출력
            text = element.text.strip()
            attributes = {}
            
            # 몇 가지 일반적인 속성 추출
            for attr in ['id', 'class', 'href', 'src', 'alt', 'title']:
                try:
                    value = element.get_attribute(attr)
                    if value:
                        attributes[attr] = value
                except:
                    pass
            
            # 결과 저장
            result = {
                'index': i,
                'text': text[:100] + '...' if len(text) > 100 else text,  # 텍스트가 너무 길면 자름
                'attributes': attributes,
                'html': element.get_attribute('outerHTML')[:200] + '...' if len(element.get_attribute('outerHTML')) > 200 else element.get_attribute('outerHTML')
            }
            
            results.append(result)
            
            # 콘솔에 정보 출력
            print(f"\n--- {tag_name} #{i+1} ---")
            print(f"텍스트: {result['text']}")
            print(f"속성: {result['attributes']}")
            print(f"HTML: {result['html']}")
        
        return results
        
    except Exception as e:
        print(f"오류 발생: {e}")
        return []
    
    finally:
        # 드라이버 종료
        print("테스트 완료, 드라이버 종료 중...")
        driver.quit()

if __name__ == "__main__":
    # 크롬드라이버 경로 (필요시 수정)
    # 경로를 지정하지 않고 시스템 PATH에 드라이버가 있다면 None으로 유지
    DRIVER_PATH = None  # 예: "C:/path/to/chromedriver.exe" 또는 "/path/to/chromedriver"
    
    # 내부망일 경우 해당 웹 서버 URL로 변경
    # 외부망 테스트시 실제 웹사이트 URL
<<<<<<< HEAD
    TEST_URL = "https://www.naver.com"  # 테스트용 URL (필요시 변경)
    
    # 찾을 태그 (필요시 변경)
    TAG_NAME = "span"  # 예: 링크 태그
    
    # 실행
    results = test_tag_crawler(TEST_URL, TAG_NAME, DRIVER_PATH)


    print(f"\n총 {len(results)}개의 {TAG_NAME} 태그 정보를 수집했습니다.")
=======
    TEST_URL = "http://example.com"  # 테스트용 URL (필요시 변경)
    
    # 찾을 태그 (필요시 변경)
    TAG_NAME = "b"  # 예: 링크 태그
    
    # 실행
    results = test_tag_crawler(TEST_URL, TAG_NAME, DRIVER_PATH)
    print(f"\n총 {len(results)}개의 {TAG_NAME} 태그 정보를 수집했습니다.")
>>>>>>> e74822ae5a56af07411f6d5f17bdd9c008ba34e3
