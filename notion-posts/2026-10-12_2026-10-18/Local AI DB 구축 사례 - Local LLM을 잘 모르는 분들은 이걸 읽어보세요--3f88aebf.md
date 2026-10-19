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
	![](https://prod-files-secure.s3.us-west-2.amazonaws.com/f9d8aebf-e9f1-81e8-bf87-0003a57463fd/1e21ec07-7ae9-4b38-bb71-543539f42de2/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB46656G5QP6S%2F20261019%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20261019T011449Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEFcaCXVzLXdlc3QtMiJHMEUCIF06RGB6vVsPrIt%2Fqrg%2FWg6d89A%2B1A4R7HPU7HF0sVuOAiEAj2Fvri4mCS%2FEyp%2ByQMArm4xjgTh9UB5yzXBQMpX855Aq%2FwMIHxAAGgw2Mzc0MjMxODM4MDUiDHOoiPRCRVrxp%2BG3circAxNALDjWjuyaAoPy75735Wxz0vEyNp1jEVKzsNGF5pKlwHW7LxyGKNfwp%2FwbdhAu%2Bcb%2B0RfwWDEtHRYbXGiu2w6lK94AZd0%2BprjsdlS5b96g5viv9iXREU%2FTOKXFPwjwonG4mNx595McFG3A78fPNjAydmmYJ3XkfgUyKDnSvZ%2Bpnmbh2SCtsqPBiFfrCwWpsAyRAmQQkkD98EziBABzStaB4DluA1v9GrWWkKk1xGEiO%2Bb4fKXCLPbM3RXDgqO56ZYqADmNwxJn4prID8sOQ7bN0f5tJj588FHINXMXkqcNp5ZR0%2F52cznOZATi%2FeZR13JVHumyaFwzX56K9uRs6NsXGIqwySDPdk5YOnOohD7jnX1kJycNFMkLjhy4lNdI%2BZ9L%2FoqgYYyN7zf%2BkDt7X7I1UIDu%2Bn8YKpND8y%2BqAF30vuuq8nJR40qc3eWWVzwXJ9ZcVT5%2BqT8dLW5h6FLlnzALUbgr9XqHCqXGpltf1IFTMmVDESfNRzSj3PBhspZR2CRJqOPsjXUHZe1IjDJbr8iy1dzqpD4ugPUms4JoD9Mc3JCYMDtNcK88omsE8FXrXRKScy%2B82Cde0Ug%2Bh0mK%2BKF0daQttLLungKT5gRd0N%2BMLW76ysgFSCCv9NG%2FMKmN1dYGOqUBDTEW1u48cCjeaDwdkVfurq533b6tefGTQGd5xyfWNR3LtuJEXIQQSBAzVyu75ZKsxIIW28BPgRLZCj1btSTu8w7QGJVHIVxxXzZ9xrauXk6AdxqRWmZJ1gHtwVWf%2Fd89lOw6H9E8QAlgq9bXy2Rzf4t9kU4YBgqlXEw3Oo8c%2Bh8%2B2wWC3nE2DlEQ%2BFo%2FGL1Wtye1lgMkACgTnxvdPWSvoUFiZ69c&X-Amz-Signature=313cf7a9aaec309bacfb85bb78273ca37b9af354a23167da71c86405b556ff55&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject#notion_record=block.3f88aebf-e9f1-80bc-80ed-d01df88a8070.f9d8aebf-e9f1-81e8-bf87-0003a57463fd)
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
	![](https://prod-files-secure.s3.us-west-2.amazonaws.com/f9d8aebf-e9f1-81e8-bf87-0003a57463fd/d35c589e-f722-4963-a076-e4fec25b3082/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB46656G5QP6S%2F20261019%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20261019T011449Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEFcaCXVzLXdlc3QtMiJHMEUCIF06RGB6vVsPrIt%2Fqrg%2FWg6d89A%2B1A4R7HPU7HF0sVuOAiEAj2Fvri4mCS%2FEyp%2ByQMArm4xjgTh9UB5yzXBQMpX855Aq%2FwMIHxAAGgw2Mzc0MjMxODM4MDUiDHOoiPRCRVrxp%2BG3circAxNALDjWjuyaAoPy75735Wxz0vEyNp1jEVKzsNGF5pKlwHW7LxyGKNfwp%2FwbdhAu%2Bcb%2B0RfwWDEtHRYbXGiu2w6lK94AZd0%2BprjsdlS5b96g5viv9iXREU%2FTOKXFPwjwonG4mNx595McFG3A78fPNjAydmmYJ3XkfgUyKDnSvZ%2Bpnmbh2SCtsqPBiFfrCwWpsAyRAmQQkkD98EziBABzStaB4DluA1v9GrWWkKk1xGEiO%2Bb4fKXCLPbM3RXDgqO56ZYqADmNwxJn4prID8sOQ7bN0f5tJj588FHINXMXkqcNp5ZR0%2F52cznOZATi%2FeZR13JVHumyaFwzX56K9uRs6NsXGIqwySDPdk5YOnOohD7jnX1kJycNFMkLjhy4lNdI%2BZ9L%2FoqgYYyN7zf%2BkDt7X7I1UIDu%2Bn8YKpND8y%2BqAF30vuuq8nJR40qc3eWWVzwXJ9ZcVT5%2BqT8dLW5h6FLlnzALUbgr9XqHCqXGpltf1IFTMmVDESfNRzSj3PBhspZR2CRJqOPsjXUHZe1IjDJbr8iy1dzqpD4ugPUms4JoD9Mc3JCYMDtNcK88omsE8FXrXRKScy%2B82Cde0Ug%2Bh0mK%2BKF0daQttLLungKT5gRd0N%2BMLW76ysgFSCCv9NG%2FMKmN1dYGOqUBDTEW1u48cCjeaDwdkVfurq533b6tefGTQGd5xyfWNR3LtuJEXIQQSBAzVyu75ZKsxIIW28BPgRLZCj1btSTu8w7QGJVHIVxxXzZ9xrauXk6AdxqRWmZJ1gHtwVWf%2Fd89lOw6H9E8QAlgq9bXy2Rzf4t9kU4YBgqlXEw3Oo8c%2Bh8%2B2wWC3nE2DlEQ%2BFo%2FGL1Wtye1lgMkACgTnxvdPWSvoUFiZ69c&X-Amz-Signature=1d3afe437ca3f1f40a633c5455ca5958fbe8efd31f37ef6bd6e50e934edd56e6&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject#notion_record=block.3f88aebf-e9f1-80b5-97cf-cbb313c5f2a1.f9d8aebf-e9f1-81e8-bf87-0003a57463fd)
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
