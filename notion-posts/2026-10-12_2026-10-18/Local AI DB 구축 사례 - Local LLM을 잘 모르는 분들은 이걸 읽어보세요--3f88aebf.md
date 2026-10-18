---
title: "Local AI DB 구축 사례 - Local LLM을 잘 모르는 분들은 이걸 읽어보세요."
created_date: "2026-10-13"
week_start: "2026-10-12"
week_end: "2026-10-18"
notion_page_id: "3f88aebf-e9f1-8025-b7c4-e8eeac277180"
last_edited_time: "2026-10-13T14:47:00.000Z"
notion_url: "https://app.notion.com/p/Local-AI-DB-Local-LLM-3f88aebfe9f18025b7c4e8eeac277180"
---
# Local AI DB 구축 사례 - Local LLM을 잘 모르는 분들은 이걸 읽어보세요.

<callout>
	### 로컬 LLM에 대해 같이 이야기하면 좋을 것 같아서, 제가 아는 잡지식들을 조금 공유해 보겠습니다.
	![](https://prod-files-secure.s3.us-west-2.amazonaws.com/f9d8aebf-e9f1-81e8-bf87-0003a57463fd/1e21ec07-7ae9-4b38-bb71-543539f42de2/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB4666MKJKFBG%2F20261018%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20261018T235635Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEFcaCXVzLXdlc3QtMiJHMEUCID5rdVOJoD5qv%2BhuNAyZ0tvLW9E%2FoMrFiIZgLDOx55BgAiEAxe%2Fy3TwqI1PSc6vPSMYMWkRG10JRtNPtYT3NFjPg%2BaYq%2FwMIHxAAGgw2Mzc0MjMxODM4MDUiDDyHX%2FjHXJudYnvFYSrcA%2F50wqKyqb%2FfQDovy7xWkmf51DMK%2BgJ%2BphAWMLueC3qgFgpStbN%2BgT%2FB531lp%2FsVwlASJbnZVU4fLgsEQaT5gHUFH2W48n%2BzJtKCvnDyWLAGwg%2BebNUGnrcmkUkV4Al7sqmcaBnrVeOAUgFpSwa9dVlMi8nZRAvDRWeJ7EqgYvmGEOVbcI694K4llqidUo2qgmEJwhCGy%2BHXdoubyxfqbVPCRgkpBxvGNNsAgTIZex1VLLzt%2BZIo38bJv9xcntPSe6M%2Fd%2BcINmvBpfz2YQtJVg1oi%2BvBdszkqFiCbHLUJzSNF3e05mfpNgR0MwNg6HI%2F%2B%2BqyXSZXYXBoj1ZOGFu9rj6Jr2EbLzreF%2FWLQwoQtOEQcGYIY29%2FbJ0AOnfe1EuFMDTVTw6SaCmC74FAfu%2F7Y36Fr8xNjFzUBccpvn%2BBHcDZbQK32d%2BgWD6O47mFfde6Ksae2NJxS0HopZ0l8umiSWM%2B9Ah2NcmagHmi%2F8K2MTwiZId2qLowvx%2FvQhocTJSv3wVKIHK%2FGxdqroE4SqNvPCjS%2BP2JZZ%2FXwmEZDklohkEx5tnr4ViQ%2FkpIlTBTDG92TOiJyr7lPjJ0kHgF92Zqhuqi70tWBZ08kTGc52s0kSgDyrs8gVVdaxL1ZAVdMKuN1dYGOqUB0UkjEOShLXkc9rmo75hf%2Fre6JgbUpcFviZeE6RsoeMsh5aHCheMSqDHVZiR34ymDZ%2FrrIamHVLkiwV0l%2B4ee80Ky9tr0LHgdSCJ3brGFFoxz3JjXZboOA%2BPNvhC6iV4y0Ab3vcqCUJPgah6I47FmdNksn%2FeXNeM1rEMBsWiWx%2B9QfYaP%2Bf43RabBuvmQeVSy0g0n1PAmPAfVtnld4n7Aip90V9pa&X-Amz-Signature=11a83a7e3f88534d325a7cf114db50715fc6f5ef780ac2fe2e4c1d013c2b9f9e&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject#notion_record=block.3f88aebf-e9f1-80bc-80ed-d01df88a8070.f9d8aebf-e9f1-81e8-bf87-0003a57463fd)
	<callout color="gray_bg">
		<details>
		<summary>**로컬 LLM이란 뭘까요? 처음 들어보는 분들은 이 토글을 봐주세요.**</summary>
			LLM = large language model. 이라는 뜻으로, 거대 언어 모델을 뜻합니다. 방대한 양의 데이터를 인공신경망으로 학습합니다. 우리에게 익숙한 챗지피티도 LLM 기술이라고 볼 수 있습니다.
			‘<span color="purple_bg">로컬’ LLM은, 쉽게 말하면 챗 지피티 같은 인공지능 모델을 인터넷 서버가 아니라 ‘내 컴퓨터’ 에서 직접 실행하는 것을 말합니다. </span>
			<br>1. 인터넷이 없어도 돌아갑니다.<br>2. 내 문서와 코드가 외부로 나가지 않기 때문에 보안이 좋습니다.<br>3. 개인 맞춤으로 학습시키고 개발하기가 너무 좋습니다. (재미있을 것 같아요.)<br>4. 그러나.. 아무래도 ‘로컬’ 이다 보니까 로컬에서 돌릴 때 사용 가능한 RAM, GPU 등이 현실적으로 큰 모델을 돌리기에는 힘듭니다. 그래서 로컬 LLM은 대형 클라우드 모델(지피티 등) 보다 성능이 부족한 편입니다.
		</details>
	</callout>
	<empty-block/>
	### 굉장히 기억에 남았던 로컬 LLM 사용 사례가 있습니다.
	어떤 강사분이 본인이 AI를 활용하는 방법을 말씀해주셨는데요.
	그분은 직업이 ‘기업의 큰 규모의 사업 프레젠테이션을 점검해주는’ 일이었어요. 그래서 기업에서 사용할 좋은 캐치프레이즈, 발표자료의 제목, 문구 등을 제안하는 일을 하셨습니다.
	그분은 좋은 발표자료들을 만들기 위해서 로컬 AI 데이터베이스를 구축했다고 했습니다. 본인이 평소에 직업상 책을 많이 읽고 레퍼런스 조사도 많이 하는데, <span color="yellow_bg">그때 마음에 들었던 느낌의 문구들을 데이터베이스에 다 기록해 놓는 겁니다.</span>
	그리고 <span color="yellow_bg">어떤 캐치프레이즈가 필요할 때, 수집한 로컬 데이터로 학습시킨 인공지능으로 캐치프레이즈를 뽑아냅니다. 본인이 원하는 느낌, 최적의 문구가 나옵니다. </span>단순히 AI에게 ‘이러이러한 상황에 쓸 건데 좋은 문구 뽑아줘’ 라고 한 줄로 명령하는 것이랑은 차원이 다릅니다.
	<span discussion-urls="discussion://3f88aebf-e9f1-8025-b7c4-e8eeac277180/3f88aebf-e9f1-8033-96d1-ebcca6067c7a/3fd8aebf-e9f1-80fd-8c9b-001c446c40a7">이게 로컬 LLM의 힘인 것 같아요. 저도 로컬로 인공지능을 돌려 보고 싶다는 생각을 늘 하는데요.. 바쁘지 않은 시기가 오면 꼭 해보고 싶어요. → 라고 하지만..? 매번 못하고 있어요ㅜㅜ</span>
	이런 것들을 보면 인공지능은 꼭 코딩 관련 직업군이 아니더라도 모든 직업에서 활발하게 사용하면 할수록 내 스킬이 되는 것 같습니다. AI로 코딩하기, 앱/웹 만들기 이런 것들보다 오히려 더 배워 볼 만한 흥미로운 아이디어라고 생각합니다.
	<empty-block/>
	---
	<empty-block/>
	### 로컬 LLM과 맥미니 재테크?
	![](https://prod-files-secure.s3.us-west-2.amazonaws.com/f9d8aebf-e9f1-81e8-bf87-0003a57463fd/d35c589e-f722-4963-a076-e4fec25b3082/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB4666MKJKFBG%2F20261018%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20261018T235635Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEFcaCXVzLXdlc3QtMiJHMEUCID5rdVOJoD5qv%2BhuNAyZ0tvLW9E%2FoMrFiIZgLDOx55BgAiEAxe%2Fy3TwqI1PSc6vPSMYMWkRG10JRtNPtYT3NFjPg%2BaYq%2FwMIHxAAGgw2Mzc0MjMxODM4MDUiDDyHX%2FjHXJudYnvFYSrcA%2F50wqKyqb%2FfQDovy7xWkmf51DMK%2BgJ%2BphAWMLueC3qgFgpStbN%2BgT%2FB531lp%2FsVwlASJbnZVU4fLgsEQaT5gHUFH2W48n%2BzJtKCvnDyWLAGwg%2BebNUGnrcmkUkV4Al7sqmcaBnrVeOAUgFpSwa9dVlMi8nZRAvDRWeJ7EqgYvmGEOVbcI694K4llqidUo2qgmEJwhCGy%2BHXdoubyxfqbVPCRgkpBxvGNNsAgTIZex1VLLzt%2BZIo38bJv9xcntPSe6M%2Fd%2BcINmvBpfz2YQtJVg1oi%2BvBdszkqFiCbHLUJzSNF3e05mfpNgR0MwNg6HI%2F%2B%2BqyXSZXYXBoj1ZOGFu9rj6Jr2EbLzreF%2FWLQwoQtOEQcGYIY29%2FbJ0AOnfe1EuFMDTVTw6SaCmC74FAfu%2F7Y36Fr8xNjFzUBccpvn%2BBHcDZbQK32d%2BgWD6O47mFfde6Ksae2NJxS0HopZ0l8umiSWM%2B9Ah2NcmagHmi%2F8K2MTwiZId2qLowvx%2FvQhocTJSv3wVKIHK%2FGxdqroE4SqNvPCjS%2BP2JZZ%2FXwmEZDklohkEx5tnr4ViQ%2FkpIlTBTDG92TOiJyr7lPjJ0kHgF92Zqhuqi70tWBZ08kTGc52s0kSgDyrs8gVVdaxL1ZAVdMKuN1dYGOqUB0UkjEOShLXkc9rmo75hf%2Fre6JgbUpcFviZeE6RsoeMsh5aHCheMSqDHVZiR34ymDZ%2FrrIamHVLkiwV0l%2B4ee80Ky9tr0LHgdSCJ3brGFFoxz3JjXZboOA%2BPNvhC6iV4y0Ab3vcqCUJPgah6I47FmdNksn%2FeXNeM1rEMBsWiWx%2B9QfYaP%2Bf43RabBuvmQeVSy0g0n1PAmPAfVtnld4n7Aip90V9pa&X-Amz-Signature=721555e7313e1f6bdaad10ecc94b4495454ee3fb072a0b90269abf27c33df05f&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject#notion_record=block.3f88aebf-e9f1-80b5-97cf-cbb313c5f2a1.f9d8aebf-e9f1-81e8-bf87-0003a57463fd)
	지금 Mac 미니(애플에서 만든, 모니터와 마우스를 따로 연결하는 소형 컴퓨터)의 가격이 엄청 올랐잖아요. 이것도 로컬 LLM 개발 열풍의 영향이 크다고 들었어요. 
	여러분 노트북은 지금 몇 GB인가요? 맥미니는 통합 메모리를 사용해서, CPU와 GPU가 같은 메모리 풀을 공유하기 때문에 더 큰 모델을 GPU에서 활용할 수 있어요. 그래서 GPU를 많이 사용해야 하는 LLM을 돌리기가 좋습니다.
	이런 이유 때문에` 인공지능이 핫해짐 → 맥미니도 인기가 올라감` 이 과정을 겪었던 것 같습니다. 아마 올해 새로운 맥미니가 나온다고 들었던 것 같은데, 맥미니 구버전 가격이 오히려 판매당시보다 지금 더 올랐어요. 그래서 구버전 맥미니를 산 사람들은 이걸 팔고 조금 더 보태서 새로운 맥미니를 산다는 경우도 있는 것 같습니다. 재테크네요..
	<empty-block/>
</callout>
<details>
<summary>출처</summary>
	제가 알고 있던 잡지식들입니다..
</details>
<empty-block/>
