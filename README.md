# NEUTRALIZATION ARENA (웹 버전)

기존 Tkinter 중화반응 프로그램을 브라우저에서 실행할 수 있도록 옮긴 Streamlit 버전입니다.

## 포함 파일
- `app.py`: 웹 앱 본체
- `requirements.txt`: 필요한 패키지

원래의 `중화반응 7.py` 파일은 삭제하거나 덮어쓰지 마세요. 이 웹 버전은 별도 파일로 추가합니다.

## GitHub에 올리기
1. 기존 `joonghwassawoogi` 저장소에 들어갑니다.
2. **Add file → Create new file**을 누릅니다.
3. 파일 이름에 `app.py`를 입력하고 이 폴더의 `app.py` 내용을 붙여넣어 저장합니다.
4. 같은 방법으로 `requirements.txt` 파일을 만들고 내용을 붙여넣어 저장합니다.

## 웹사이트 배포 (Streamlit Community Cloud)
1. https://share.streamlit.io/ 에 접속해 GitHub 계정으로 로그인합니다.
2. **Create app**을 선택합니다.
3. Repository: `ddigguunpyojung/joonghwassawoogi`
4. Branch: `main`
5. Main file path: `app.py`
6. **Deploy**를 누릅니다.

배포가 끝나면 `https://....streamlit.app` 형태의 주소가 생성됩니다. 이 주소를 친구에게 보내면 브라우저에서 사용할 수 있습니다.

## 참고
- GitHub Pages는 Python/Tkinter 앱을 실행하지 못합니다. Streamlit 배포 주소를 공유하세요.
- 이 웹 버전은 원본의 화학 물질 선택, 농도·부피 입력, 중화 계산, 이온 목록, pH 분석, 전투 체력바 애니메이션을 웹 UI로 재구성했습니다.
- 화면 배치는 웹 브라우저와 모바일 화면에 맞게 조정되어 있어 Tkinter 창과 픽셀 단위로 완전히 같지는 않습니다.
