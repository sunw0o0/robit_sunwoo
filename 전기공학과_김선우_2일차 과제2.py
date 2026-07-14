import requests
import json
import urllib3
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_backup_lifetime_boxoffice():

    return [
        {"순위": "1", "영화제목": "명량", "개봉일": "2014-07-30", "누적관객수": 17616141, "감독": "김한민"},
        {"순위": "2", "영화제목": "왕과 사는 남자", "개봉일": "2026-02-04", "누적관객수": 16911114, "감독": "장항준"},
        {"순위": "3", "영화제목": "극한직업", "개봉일": "2019-01-23", "누적관객수": 16266480, "감독": "이병헌"},
        {"순위": "4", "영화제목": "신과함께: 죄와 벌", "개봉일": "2017-12-20", "누적관객수": 14414658, "감독": "김용화"},
        {"순위": "5", "영화제목": "국제시장", "개봉일": "2014-12-17", "누적관객수": 14265222, "감독": "윤제균"}
    ]

def fetch_lifetime_boxoffice():

    api_key = "430156241533de1d58c8d01b5ca24dad"
    url = f"http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchMultiMovieBestList.json?key={api_key}"
    
    try:
        response = requests.get(url, timeout=3, verify=False)
        response.raise_for_status()
        data = response.json()
        
        if "boxOfficeResult" in data and "lifetimeBoxOfficeList" in data["boxOfficeResult"]:
            raw_list = data["boxOfficeResult"]["lifetimeBoxOfficeList"][:5] # 상위 5개만 슬라이싱
            processed_movies = []
            
            for item in raw_list:
                try:
                    audi_acc = int(item.get("audiAcc", 0))
                except (ValueError, TypeError):
                    audi_acc = 0

                processed_movies.append({
                    "순위": item.get("rank"),
                    "영화제목": item.get("movieNm"),
                    "개봉일": item.get("openDt"),
                    "누적관객수": audi_acc,
                    "감독": item.get("director", "정보 없음")
                })
            return processed_movies, False 
        else:
            return get_backup_lifetime_boxoffice(), True
            
    except Exception as e:
        print(f"\n⚠️ [네트워크 지연 안내] 영화진흥위원회 통계 서버 연결에 지연이 발생했습니다. ({e})")
        print("💡 수집된 2026 역대 누적 데이터 세트로 우회하여 리포트를 작성합니다.\n")
        return get_backup_lifetime_boxoffice(), True


def main():
    print("🏆 [영화진흥위원회 공식 집계 역대 영화 누적 흥행 순위 분석 시스템] 🏆")
    print("대한민국 영화 역사상 가장 많은 사랑을 받은 TOP 5 영화를 분석합니다...\n")
    
    movie_list, is_backup = fetch_lifetime_boxoffice()
    
    if movie_list:
        source_label = "오프라인 백업 데이터" if is_backup else "실시간 LIVE 데이터"
        
        print("================================================================================")
        print(f"🎬 대한민국 역대 영화 누적 관객수 TOP 5 ({source_label})")
        print("================================================================================")
        print(f"{'순위':<4} | {'영화 제목':<25} | {'개봉일':<11} | {'누적 관객수':<13} | {'감독'}")
        print("-" * 80)
        
        for movie in movie_list:
            audi_acc_formatted = f"{movie['누적관객수']:,}명"
            print(f"{movie['순위']:^4} | {movie['영화제목']:<28} | {movie['개봉일']:<11} | {audi_acc_formatted:<17} | {movie['감독']}")
            
        print("-" * 80)
        
        output_file = "latest_query.json"
        summary_report = {
            "분석종류": "역대_영화_누적_관객수_TOP_5",
            "조회시간": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "데이터출처": source_label,
            "흥행_기록_데이터": movie_list
        }
        
        with open(output_file, mode='w', encoding='utf-8') as f:
            json.dump(summary_report, f, ensure_ascii=False, indent=4)
            
        print(f"📝 역대 종합 순위 보고서가 '{output_file}'에 안전하게 저장되었습니다.")
    else:
        print("\n❌ 시스템 오류로 정보를 불러오지 못했습니다.")

if __name__ == "__main__":
    main()