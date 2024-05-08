import streamlit as st
from corrected_text import extract_and_correct_text_from_srt, save_corrected_srt

def main():
    st.title('SRT 파일 맞춤법 검사기')

    srt_file_path = st.text_input('SRT 파일 경로를 입력하세요:', '')
    if srt_file_path:
        subtitles = extract_and_correct_text_from_srt(srt_file_path)
        if st.button('맞춤법 검사 결과 보기'):
            st.write(subtitles['changes'])

        with st.form("user_review_form"):
            for i, change in enumerate(subtitles["changes"]):
                st.write(f"변경 전: {change.split(' --> ')[0]}")
                st.write(f"변경 후: {change.split(' --> ')[1]}")
                choice = st.radio("이 변경을 적용하시겠습니까?", ('적용', '무시', '직접 수정'), key=f"choice_{i}")
                if choice == '직접 수정':
                    custom_text = st.text_area("수정할 텍스트를 입력하세요:", key=f"custom_text_{i}")
                    subtitles["corrected_text"][i] = custom_text
                st.markdown("---")  # 구분선 추가

            submitted = st.form_submit_button("변경 사항 저장")
            if submitted:
                output_file_path = st.text_input('저장할 SRT 파일 경로를 입력하세요:', '')
                if output_file_path:
                    save_corrected_srt(subtitles, output_file_path)
                    st.success('파일이 저장되었습니다.')

if __name__ == "__main__":
    main()