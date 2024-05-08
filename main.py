import pprint
from corrected_text import extract_and_correct_text_from_srt, save_corrected_srt, user_review_and_edit

def main():
    srt_file_path = '/Users/HyeunseungYu/Desktop/5_5_0.srt'
    output_file_path = '/Users/HyeunseungYu/Desktop/5_5_0_corrected.srt'
    
    subtitles = extract_and_correct_text_from_srt(srt_file_path) # 맞춤법 검사를 진행한 결과를 딕셔너리로 리턴
    user_review_and_edit(subtitles) # 수정이 필요한 내용을 사용자가 직접 고칠 수 있도록 함
    save_corrected_srt(subtitles, output_file_path) # 사용자가 선택한 내용을 반영하여 바로 젖
    pprint.pprint(subtitles['changes'])

if __name__ == "__main__":
    main()