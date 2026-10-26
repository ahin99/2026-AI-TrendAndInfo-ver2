---
title: "AI가 짜준 프롬프트 이행하기"
created_date: "2026-10-24"
week_start: "2026-10-19"
week_end: "2026-10-25"
notion_page_id: "4038aebf-e9f1-809a-b4a4-cea96172330e"
last_edited_time: "2026-10-25T17:55:00.000Z"
notion_url: "https://app.notion.com/p/AI-4038aebfe9f1809ab4a4cea96172330e"
---
# AI가 짜준 프롬프트 이행하기

<callout>
	이번에 해볼것은 ‘행복’이라는 주제입니다. 
	다음 건축 독서토론세미나를 준비하면서 읽고 있는 \<행복의 건축\>을 읽다가 떠오른 주제입니다. 
	<callout icon="/icons/cherries_red.svg" color="gray_bg">
		‘집은 식견을 갖춘 증인으로 성장했다. 집은 연애가 시작될 때에도 관여했으며, 숙제를 하는 것도 지켜보았고, 포대기에 폭 싸인 아기가 병원에 막 도착하는 관경도 지켜보았으며, 한밤중에 부엌에서 소곤거리며 나누는 이야기에 깜짝 놀라기도 했다. 창문이 언 콩이 담긴 자루처럼 차가웠던 겨울 저녁도 겪었으며, 벽돌 벽이 새로 구운 자루처럼 차가웠던 겨울 저녁도 겪었으며, 벽돌 벽이 새로 구운 빵의 온기를 간직하던 한여름의 어스름도 겪었다.’
		알랭 드 보통,\<행복의 건축\> 중에서 
	</callout>
	암튼, 그냥 집은 항상 우리를 관찰하고 있다는 부분이랑 뭐 행복 감정 이런 부분들을 생각하니, 우리가 항상 쳐다보고 있는 노트북도 우리를 아주 자세히 바라보는 관찰자가 아닌가라는 생각이 들었고, 또 언제 대학생들이 표정이 풍부해질까 생각을 해보니, 과제를 하거나 할 때가 아닌가 했습니다. 
	그래서 수업 중의 표정 변화를 측정해보면 재밌겠다 정도의 생각을 했습니다. 
		물론 아직 클로드를 어떻게 쓰는지 모르기 때문에 제미나이 플러스를 사용할 건데. 될지는 모르겠습니다. 
		<empty-block/>
	프롬프트를 써야하지만 생각하기 너무 귀찮았던 이슈로, AI한테 프롬프트로 명령을 해달라고 했습니다. 
	![이미 사용자의 귀차니즘이 익숙한 제미나이…](https://prod-files-secure.s3.us-west-2.amazonaws.com/f9d8aebf-e9f1-81e8-bf87-0003a57463fd/cec5276e-c3ec-462b-ba07-f602339c61fa/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB46635Y5FF7S%2F20261026%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20261026T065546Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEAYaCXVzLXdlc3QtMiJHMEUCIQDZYj33ltAthKtTNp3N58KWaEhjM4V6pz%2BeYE79Pzut2QIgOCTQUBicxo9gmSXRO9Q%2B5cdk%2BzhM7fj6WhqX6imydUEqiAQIz%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw2Mzc0MjMxODM4MDUiDEntsQbo9xB7FzsnsircA3NlXIWqet%2BzWpkxelkwyQ7WjlpoK568pL05GoWN5cOmgRyrcyZc8iwy0ly7ylxaAUezfklvKZ1TfIDIO8EtUr96k1Sq0v%2B7kUfA%2BLu4pmi8rxv067toawtNiChwvLVqiMmbBk7lCoKnoDpSVtQ%2FU2Zc0Y9ID4jCI4kr83iud8As%2BQRVY4KymMF%2FDF5U%2BHw9TZ54p532XfA17NEPiF%2FofxYp6JEZfSYcAPwd0LAooOC2uPYoObEa%2B%2FrSUQ3YcHQjVaCsGwiZHySMIqUHiRIRtdWAIoyfyLRr36qBptLDFCMv9tnrq6ayRizYXbxkQHUfijE5Epg1xyEdNCfDH1vOd9eNbELI%2FaUTWVUJe3DwXPGNxl2VEfwkYZCNJzBadXePYQQw%2BCM%2BgoM6%2B2XE1PXkEWTOQ3UIl1Mk0Ux3E6r%2BXlZ3FWQH8EA8U8Tcxo2MrsTd41LCN1yf7ZccbUtskRJvyvpqsEtMVnlO%2ByfTvjrXtCIgtG34qpEVaC%2FrMgu%2BfTCP2xFuPPIVyKYzf0Qpl0S3mYl%2FaNhSn41n95fd2pxc%2ByCU2PCOqPADAvlJQm3ZtCKSTkOkF%2BTIb%2B%2FEI3cX92jpp1ZyIYdwQOiqsA0rgkoYuQV3%2FJeZD6j1d7qXkJ0yMNDN%2B9YGOqUBrsZTorl560WnYEGEsEtw5V5nDfkxJzR9MY04bX%2BXJNq8Zf0B%2BlUgH90lC8N8RM0%2Fy5PHtTu06m7P0DiHclvOWp4hXcg7KwOxpa5RAJKQnZnW8fwB4cPMWmAvQnNBUDeiNJh5RKjkmyWP7j9Pq0pAeOf9qpLGgFYis%2B7R4C4lHZ%2FTKGp2D%2FWiVI3TlIvLAZTod1e7cO08S1dyZCsu3iB5PXljN11V&X-Amz-Signature=7e1ff76e4f84e46bf2120eb2b74ce7140e3a1649a15861f01be86a77782e53cd&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject#notion_record=block.4038aebf-e9f1-8061-8490-cc4e0efaad69.f9d8aebf-e9f1-81e8-bf87-0003a57463fd)
	 먼저 필요한 라이브러리를 설치합니다. 터미널을 열고 웹캠 제어와 얼굴 랜드마크 분석에 필요한 도구를 설치합니다. 
	```javascript
%pip install opencv-python mediapipe numpy(네트워크 이슈로,,;; 
	```
	이제부터는 제미나이가 하라는데로 움직이기만 하면 됩니다. 
	<callout icon="/icons/cherries_red.svg" color="gray_bg">
		### 2. 파이썬 코드 실행하기 (`happiness.py`)
		컴퓨터에 새 파일을 만들고 이름을 `happiness.py`로 저장한 뒤, 아래 코드를 **그대로 복사해서 붙여넣고 실행**해 주세요.
	</callout>
	그러나 저는 새 파일을? 컴퓨터에 만들 줄 모릅니다. 그래서 다시 제미나이에게 묻습니다. 
	![](https://prod-files-secure.s3.us-west-2.amazonaws.com/f9d8aebf-e9f1-81e8-bf87-0003a57463fd/af95bfd3-e62c-427e-928a-4ef636ae7050/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB46635Y5FF7S%2F20261026%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20261026T065546Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEAYaCXVzLXdlc3QtMiJHMEUCIQDZYj33ltAthKtTNp3N58KWaEhjM4V6pz%2BeYE79Pzut2QIgOCTQUBicxo9gmSXRO9Q%2B5cdk%2BzhM7fj6WhqX6imydUEqiAQIz%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw2Mzc0MjMxODM4MDUiDEntsQbo9xB7FzsnsircA3NlXIWqet%2BzWpkxelkwyQ7WjlpoK568pL05GoWN5cOmgRyrcyZc8iwy0ly7ylxaAUezfklvKZ1TfIDIO8EtUr96k1Sq0v%2B7kUfA%2BLu4pmi8rxv067toawtNiChwvLVqiMmbBk7lCoKnoDpSVtQ%2FU2Zc0Y9ID4jCI4kr83iud8As%2BQRVY4KymMF%2FDF5U%2BHw9TZ54p532XfA17NEPiF%2FofxYp6JEZfSYcAPwd0LAooOC2uPYoObEa%2B%2FrSUQ3YcHQjVaCsGwiZHySMIqUHiRIRtdWAIoyfyLRr36qBptLDFCMv9tnrq6ayRizYXbxkQHUfijE5Epg1xyEdNCfDH1vOd9eNbELI%2FaUTWVUJe3DwXPGNxl2VEfwkYZCNJzBadXePYQQw%2BCM%2BgoM6%2B2XE1PXkEWTOQ3UIl1Mk0Ux3E6r%2BXlZ3FWQH8EA8U8Tcxo2MrsTd41LCN1yf7ZccbUtskRJvyvpqsEtMVnlO%2ByfTvjrXtCIgtG34qpEVaC%2FrMgu%2BfTCP2xFuPPIVyKYzf0Qpl0S3mYl%2FaNhSn41n95fd2pxc%2ByCU2PCOqPADAvlJQm3ZtCKSTkOkF%2BTIb%2B%2FEI3cX92jpp1ZyIYdwQOiqsA0rgkoYuQV3%2FJeZD6j1d7qXkJ0yMNDN%2B9YGOqUBrsZTorl560WnYEGEsEtw5V5nDfkxJzR9MY04bX%2BXJNq8Zf0B%2BlUgH90lC8N8RM0%2Fy5PHtTu06m7P0DiHclvOWp4hXcg7KwOxpa5RAJKQnZnW8fwB4cPMWmAvQnNBUDeiNJh5RKjkmyWP7j9Pq0pAeOf9qpLGgFYis%2B7R4C4lHZ%2FTKGp2D%2FWiVI3TlIvLAZTod1e7cO08S1dyZCsu3iB5PXljN11V&X-Amz-Signature=b577f2d3c4db29d57be1c1f5708637acda0c038842ff660d1e8606d0ae14354e&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject#notion_record=block.4048aebf-e9f1-8005-adf1-e938eb30e570.f9d8aebf-e9f1-81e8-bf87-0003a57463fd)
	그럼 새 파일을 만들었습니다. 
	그리고 파일에 안에 제미나이가 알려준 코드를 복사해서 넣습니다. 
	```javascript
import cv2
import mediapipe as mp
import numpy as np

# MediaPipe 얼굴 랜드마크 모델 초기화
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
)

# 노트북 웹캠 연결 (0번 카메라)
cap = cv2.VideoCapture(0)

print(" [알림] 웹캠이 켜졌습니다. 종료하시려면 화면 창을 클릭하고 키보드의 'q'를 누르세요.")

while cap.isOpened():
  success, frame = cap.read()
  if not success:
    print("웹캠을 불러올 수 없습니다.")
    break

  # 거울 모드처럼 보이도록 좌우 반전 및 색상 변환
  frame = cv2.flip(frame, 1)
  h, w, c = frame.shape
  rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

  # 얼굴 랜드마크 감지 수행
  results = face_mesh.process(rgb_frame)

  happiness_score = 0

  if results.multi_face_landmarks:
    for face_landmarks in results.multi_face_landmarks:
      landmarks = face_landmarks.landmark

      # 주요 얼굴 부위 좌표 추출 (MediaPipe 인덱스 기준)
      # 입꼬리 좌우: 61번, 291번 / 윗입술 중앙: 13번
      # 얼굴 좌우 끝 (크기 정규화용): 234번, 454번
      p_left = np.array([landmarks[61].x * w, landmarks[61].y * h])
      p_right = np.array([landmarks[291].x * w, landmarks[291].y * h])
      p_top = np.array([landmarks[13].x * w, landmarks[13].y * h])
      p_edge_l = np.array([landmarks[234].x * w, landmarks[234].y * h])
      p_edge_r = np.array([landmarks[454].x * w, landmarks[454].y * h])

      # 얼굴 전체 너비와 입꼬리 너비 계산
      face_width = np.linalg.norm(p_edge_l - p_edge_r)
      mouth_width = np.linalg.norm(p_left - p_right)

      # 입술 중앙 대비 입꼬리가 올라간 정도 계산
      mouth_center_y = (p_left[1] + p_right[1]) / 2
      lift = p_top[1] - mouth_center_y

      # 미소 비율을 바탕으로 0~100점 사이의 행복도 점수로 변환
      ratio = mouth_width / face_width
      score = (ratio - 0.25) * 450 + (lift * 0.8)
      happiness_score = int(np.clip(score, 0, 100))

  # 화면 상단에 행복도 점수 글자 띄우기
  cv2.putText(
      frame,
      f"Happiness: {happiness_score} / 100",
      (30, 50),
      cv2.FONT_HERSHEY_SIMPLEX,
      1,
      (0, 255, 0),
      2,
  )

  # 화면 상단에 초록색 행복도 게이지(막대바) 그리기
  bar_width = int(happiness_score * 3)
  cv2.rectangle(frame, (30, 70), (30 + 300, 95), (200, 200, 200), -1)
  cv2.rectangle(frame, (30, 70), (30 + bar_width, 95), (0, 255, 0), -1)

  # 실시간 화면 출력
  cv2.imshow("Happiness Detector", frame)

  # 키보드 'q'를 누르면 프로그램 종료
  if cv2.waitKey(1) & 0xFF == ord("q"):
    break

cap.release()
cv2.destroyAllWindows()
	```
	이러고 터미널을 열어 파일을 엽니다. 입력을 합니다. 
	```javascript
cd Desktop 
python happiness.py
	```
	그러나 원래라면 카메라가 작동해야하는데 아무것도 작동하지 않습니다. 
	문제는 저는 코드를 모르고 원리도 모르기에 다시 제미나이에게 질문을 해야한다는 겁니다. 
	3시간 정도 붙잡고 있었지만, 모르겠습니다. 
	여러분 도와주세요. 
</callout>
와이파이 이슈로 곧 마저 작성해두겠습니당)
<details>
<summary>출처</summary>
	아래에 출처를 입력하세요
</details>
<empty-block/>
