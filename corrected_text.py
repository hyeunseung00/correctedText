from pprint import pprint
from hanspell import spell_checker

def extract_and_correct_text_from_srt(srt_file_path):
    # 결과 저장할 딕셔너리
    subtitles = {
        "original": [],
        "text_only": [],
        "corrected_text": [],
        "changes": []  
    }
    
    # SRT 파일 열기 및 처리
    with open(srt_file_path, 'r', encoding='utf-8') as file:
        block = []
        
        for line in file:   
            #파일 한줄한줄 까보기. 일단 빈 줄인지 아닌지
            #빈 줄이 아니다? 그럼 바로 block에 추가
            if line.strip() == "":  #비어있는 줄이다? 그럼 하나의 자막 덩이가 완성된 거니까 개행문자로 조합하고 block 리셋
                if len(block) > 2:
                    subtitles["original"].append("\n".join(block) + "\n")
                    subtitles["text_only"].append("\n".join(block[2:]) + "\n")
                block = []
            else:
                block.append(line.strip())

        #제일 마지막 자막 덩이에서는 빈 줄이 없으니까 한 번 더 돌려줌
        if len(block) > 2:
            subtitles["original"].append("\n".join(block) + "\n")
            subtitles["text_only"].append("\n".join(block[2:]) + "\n")

    for i, text_only in enumerate(subtitles["text_only"]):
        check_result = spell_checker.check(text_only)
        corrected_text = check_result.checked
        # 수정된 텍스트에 타임스탬프를 포함하여 저장
        corrected_block = subtitles["original"][i].split("\n")
        if len(corrected_block) > 2:
            # 타임스탬프 유지하면서 텍스트 부분만 교체
            corrected_block[2:] = corrected_text.split("\n")
        subtitles["corrected_text"].append("\n".join(corrected_block) + "\n")
        
        # 오류가 수정된 경우에만 changes에 추가하는 로직으로 변경
        if check_result.modifications:
            change = f"{text_only.strip()} --> {corrected_text.strip()}"
            subtitles["changes"].append(change)
            
    return subtitles

# 사용자 입력을 받아 변경 사항을 확인하고 수정하는 함수
def user_review_and_edit(subtitles):
    for i, change in enumerate(subtitles["changes"]):
        print(f"변경 전: {change.split(' --> ')[0]}")
        print(f"변경 후: {change.split(' --> ')[1]}")
        while True:
            user_input = input("이 변경을 적용하시겠습니까? (y/n/edit): ")
            if user_input.lower() in ['y', 'n', 'edit']:
                break
            else:
                print("잘못된 입력입니다. 다시 입력해주세요.")
                
        if user_input.lower() == 'y':
            continue
        elif user_input.lower() == 'n':
            # 변경 사항을 무시하고 원본을 유지
            subtitles["corrected_text"][i] = subtitles["original"][i]
        elif user_input.lower() == 'edit':
            # 사용자가 직접 수정
            custom_text = input("수정할 텍스트를 입력하세요: ")
            corrected_block = subtitles["original"][i].split("\n")
            if len(corrected_block) > 2:
                corrected_block[2:] = custom_text.split("\n")
            subtitles["corrected_text"][i] = "\n".join(corrected_block) + "\n"

def save_corrected_srt(subtitles, output_file_path):
    with open(output_file_path, 'w', encoding='utf-8') as file:
        for corrected_text in subtitles["corrected_text"]:
            file.write(corrected_text)



# srt_file_path = f'/Users/HyeunseungYu/Desktop/test.srt'  # SRT 파일 경로
# subtitles = extract_and_correct_text_from_srt(srt_file_path)
# pprint(subtitles)

# output_srt_file_path = f'/Users/HyeunseungYu/Desktop/test_corrected.srt'  # 수정된 SRT 파일 경로
# save_corrected_srt(subtitles, output_srt_file_path)

