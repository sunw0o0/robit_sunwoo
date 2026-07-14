import csv
import json
import os

def validate_and_process_data(raw_rows):
    clean_data = []
    total_score = 0
    max_score = -1
    
    for row in raw_rows:
        name = row.get('name', '').strip()
        score_raw = row.get('score', '').strip()
        
        try:
            score = int(score_raw)
        except ValueError:
            print(f"[오류 행 제외] {name},{score_raw} -> 숫자 변환 실패")
            continue
            
        if score < 0 or score > 100:
            print(f"[오류 행 제외] {name},{score} -> 허용 범위 초과")
            continue
            
        clean_data.append({'name': name, 'score': score})
        total_score += score
        if score > max_score:
            max_score = score

    count = len(clean_data)
    average = round(total_score / count, 2) if count > 0 else 0
    
    summary = {
        "인원수": count,
        "평균": average,
        "최고점": max_score if count > 0 else 0
    }
    
    return clean_data, summary


def main():
    input_filename = "students.csv"
    output_csv = "clean_students.csv"
    output_json = "summary.json"
    
    with open(input_filename, mode='w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['name', 'score'])
        writer.writerows([
            ['민준', '85'],
            ['서연', '92'],
            ['지우', 'abc'],
            ['하늘', '105'],
            ['유진', '78']
        ])

    try:
        with open(input_filename, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            raw_rows = list(reader)  
            
        clean_students, summary_data = validate_and_process_data(raw_rows)
        
        with open(output_csv, mode='w', encoding='utf-8', newline='') as f:
            fieldnames = ['name', 'score']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(clean_students)
            
        with open(output_json, mode='w', encoding='utf-8') as f:
            json.dump(summary_data, f, ensure_ascii=False, indent=4)
            
        print("\n=== 데이터 정제 및 파일 저장 완료 ===")
        print(f"-> 정제 데이터 저장 완료: {output_csv}")
        print(f"-> 요약 결과 통계 저장 완료: {output_json}")

    except FileNotFoundError:
        print(f"ERROR: {input_filename} 파일을 찾을 수 없습니다.")
    except Exception as e:
        print(f"ERROR: 시스템 예상치 못한 오류 발생 ({e})")


if __name__ == "__main__":
    main()