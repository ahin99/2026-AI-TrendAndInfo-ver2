---
title: "통합 Reading Material 시스템의 자세한 개발 과정"
created_date: "2026-10-19"
week_start: "2026-10-19"
week_end: "2026-10-25"
notion_page_id: "3fe8aebf-e9f1-8091-8c68-cf00a297c2b5"
last_edited_time: "2026-10-19T10:05:00.000Z"
notion_url: "https://app.notion.com/p/Reading-Material-3fe8aebfe9f180918c68cf00a297c2b5"
---
# 통합 Reading Material 시스템의 자세한 개발 과정

<callout>
	## Notion의 AI 스터디 글을 GitHub로 모으고, Gemini로 주간 통합 Reading Materials 까지 자동 생성해보기
	<details>
	<summary>API란 뭘까? API라는 용어를 처음 들어보신 분들은 이 토글을 봐주세요.</summary>
		[https://www.google.com/search?q=API+개념&sca_esv=9e597e613f614ac0&sxsrf=APpeQnsl49C02cWkyESflkFuj3Yiosqjuw%3A1792381095190&ei=p5DVasuHC9mbhvcPgP-F8Ag&biw=1197&bih=670&uact=5&oq=API+개념&gs_lp=Egxnd3Mtd2l6LXNlcnAiCkFQSSDqsJzrhZAyBRAAGIAEMgYQABgeGA0yCBAAGAgYHhgNMggQABgIGB4YDTIIEAAYCBgeGA0yBRAAGO8FMggQABgFGB4YDTIIEAAYBRgeGA0yCBAAGAUYHhgNMggQABgFGB4YDUihJlDJBVimJXALeAGQAQGYAawBoAHuDKoBAzguN7gBA8gBAPgBAZgCFaAC9QrCAgoQABhHGNYEGLADwgINEAAYgAQYigUYQxiwA8ICExAuGIAEGIoFGEMYxwEYrwEYsAPCAg4QABjkAhjWBBiwA9gBAcICFxAuGNwGGLgGGNoGGNgCGMgDGLAD2AEBwgIKEAAYgAQYigUYQ8ICCBAAGIAEGMsBwgIFECEYoAHCAgcQABiABBgNmAMAiAYBkAYRugYGCAEQARgJkgcEMTMuOKAHzDWyBwMyLji4B-oJwgcGMC4xLjIwyAdZgAgB&sclient=gws-wiz-serp](https://www.google.com/search?q=API+%EA%B0%9C%EB%85%90&sca_esv=9e597e613f614ac0&sxsrf=APpeQnsl49C02cWkyESflkFuj3Yiosqjuw%3A1792381095190&ei=p5DVasuHC9mbhvcPgP-F8Ag&biw=1197&bih=670&uact=5&oq=API+%EA%B0%9C%EB%85%90&gs_lp=Egxnd3Mtd2l6LXNlcnAiCkFQSSDqsJzrhZAyBRAAGIAEMgYQABgeGA0yCBAAGAgYHhgNMggQABgIGB4YDTIIEAAYCBgeGA0yBRAAGO8FMggQABgFGB4YDTIIEAAYBRgeGA0yCBAAGAUYHhgNMggQABgFGB4YDUihJlDJBVimJXALeAGQAQGYAawBoAHuDKoBAzguN7gBA8gBAPgBAZgCFaAC9QrCAgoQABhHGNYEGLADwgINEAAYgAQYigUYQxiwA8ICExAuGIAEGIoFGEMYxwEYrwEYsAPCAg4QABjkAhjWBBiwA9gBAcICFxAuGNwGGLgGGNoGGNgCGMgDGLAD2AEBwgIKEAAYgAQYigUYQ8ICCBAAGIAEGMsBwgIFECEYoAHCAgcQABiABBgNmAMAiAYBkAYRugYGCAEQARgJkgcEMTMuOKAHzDWyBwMyLji4B-oJwgcGMC4xLjIwyAdZgAgB&sclient=gws-wiz-serp)
	</details>
	```markdown
# 폴더 구조 (참고)

	2026-AI-TrendAndInfo-ver2/ -> 최상위 레포명
	│
	├─ .github/
	│  └─ workflows/ -> 노션 동기화, 통합 읽을거리 생성을 위한 yml
	│     ├─ sync-notion.yml
	│     └─ generate-weekly-digest.yml
	│
	├─ scripts/ -> 노션 동기화, 통합 읽을거리 생성을 위한 파이썬코드
	│  ├─ sync_notion.py
	│  └─ generate_weekly_digest.py
	│
	├─ notion-posts/ -> 팀원들이 노션 DB에 올린 것 동기화되어 올라감.
	│  ├─ 2026-10-12_2026-10-18/
	│  │  ├─ 글1.md
	│  │  ├─ 글2.md
	│  │  └─ ...
	│  │
	│  └─ 2026-10-19_2026-10-25/
	│
	├─ weekly-digests/ -> 이곳에 주차별 통합 읽을거리가 올라감. 톡방에 복붙하기.
	│  ├─ 2026-10-12_2026-10-18.md
	│  └─ ...
	│
	└─ README.md -> 리드미 (프로젝트 설명 대문)
	```
	<empty-block/>
	---
	<empty-block/>
	제가 개발하여 실제로 우리 스터디에서 사용 중인 이 시스템을,
	- 어떻게 설계했는지
	- 그 과정에서 AI는 어디에 어떤 방식으로 활용했는지     
	를 알아봅시다 :
	<callout color="gray_bg">
		- 노션-깃허브 커밋 자동화 개발 과정
			1. 노션과 깃허브에 각각 DB, 레포지토리 생성
			2. 노션 API 개발자 페이지를 이용한 DB 토큰 발급받기 
			3. 깃허브 Secret에 노션 토큰 키, DB 등록하기 
			4. 로컬 맥에 폴더 구조 생성, 깃 레포에 연결
			5. 주차별 구분을 위한 파이썬 코드 작성
			6. 깃허브 액션 등록을 위한 YAML 작성
			7. 깃허브 액션 Run Workflow로 동기화!
		→ 노션 DB에 올라간 글들은 기본적으로 마크다운 형식의 글입니다. (이를 CSV 또는 JSON으로 변환해 다운받을 수 있습니다.) 매주 올라온 노션 포스트들을 마크다운 형식으로, 깃허브 레포지토리에 버튼 하나를 누르면 자동으로 커밋해 정리 가능하게 했습니다.
		<empty-block/>
		- 제미나이 API를 이용한 통합 Reading Materials 생성
			1. 제미나이 API 키를 구글 AI 스튜디오에서 발급받아 오기
			2. 깃허브 Secret에 제미나이 API 키 등록
			3. 프롬프트를 포함한 파이썬 코드 작성
			4. 깃허브 액션 등록을 위한  YAML 작성
			5. 깃허브 액션 Run Workflow로 이주의 통합 읽을거리 생성!
		→ 제미나이 API를 이용해 기존에 동기화된 노션 포스트 마크다운 문서 내용을 파악하고, 프롬프트에 따라서 새로운 마크다운 문서 생성 및 자동 커밋합니다. 제가 수동으로 해야 하는 일은 깃허브 액션 버튼 딸깍 눌러주기, 그리고 이 최종 통합 읽을거리를 저장해서 톡방에 보내기가 전부입니다.
	</callout>
	<br>대부분 지피티에게 물어보면서 진행했습니다. 주제와 대략적인 구조를 잡을 때에는 지피티와 비교적 자유롭게 티키타카 하면서 진행했고, 가닥이 잡힌 이후에는 <span color="yellow_bg">*지금까지 우리가 대화한 것들을 바탕으로 \~하는 방법에 대해 단계적으로 제시해*</span><span color="yellow_bg"> </span>라고 명령했습니다. (<span color="purple_bg">한 Chat 안에서 진행하면 주제 잡기 이후 다시 구상을 설명할 필요 없이, 그냥 ‘지금까지 이 대화를 바탕으로’ 이런 식으로 퉁칠 수 있어서 편합니다.</span>)
	코덱스를 활용하기에는 애매해서 (=인간이 직접 해야하는 것들이 많아서..) 지피티에게 <span color="yellow_bg">*”단계적으로 설명해줘”*</span> 라고 프롬프트를 넣고, 이해가 안 되는 단계를 직접 <span color="yellow_bg">*”몇번 단계에 대해서 다시 설명해”*</span> 하고 요청했습니다. (단 조금 주의할 점은, 몇번 단계에 대해서 다시 설명 → 이 부분 분량이 너무 길어지면 지피티가 앞의 대화내용을 기억하기를 힘들어해서 채팅이 느려집니다. <span color="purple_bg">적당히 질문을 조절하고, 또 굳이 앞의 대화내용 기억이 필요없는 질문이면 다른 전용 Chat을 두 탭으로 띄워놓고 병행하는 걸 추천합니다.</span>)<br><br>또 지금 단계에서 지피티가 해야 할 역할을 명확히 규정했는데, 이때 ‘<span color="yellow_bg">하지 말아야 하는 것’을 제한</span>해서 프롬프트에 넣었습니다. 예를 들어서, 이런 식으로 :
	```markdown
(위의 설명한 내용들 .. ) 이걸 명심하면서, 구글 제미나이 프롬프트 개발은 조금 나중에 하고. 지금은 어떻게 제미나이 api를 깃 레포에 연결하는지 그 단계를 설명해. 
	```
	아래 내용은 제가 제미나이에게 사용한 프롬프트입니다. 깃허브 scripts/generate_weekly_digest.py 에서 확인 가능합니다.<br>너무 바빠서.. 아직 제대로 프롬프트 구상을 해서 넣지는 않았습니다. 그냥 지피티에게 “이러이러한 걸 할 건데, 프롬프트 넣어라” 하고 명령한 그대로입니다. (그래도 생성물을 봤을 때 나쁘진 않죠?)<br>프롬프트 엔지니어링을 고려해서, 다음 차시 스터디에 팀원들과 함께 고쳐보려고 생각 중입니다.
	<span color="red">+) 너는 대학생 AI 스터디의 주간 읽을거리를 만드는 편집자다. → 이런식으로 프롬프트 넣는 게 요즘엔 엄청 올드한 거라던데 맞나요..? 거의 구석기시대 프롬프트라던데요. </span>지피티는 이렇게 생성했기는 한데.. 나중에 같이 고쳐보시죠.
	```python
============================================================
읽을거리 {index}
제목: {article["title"]}
============================================================

{article["content"]}

"""

    prompt = f"""
너는 대학생 AI 스터디의 주간 읽을거리를 만드는 편집자다.

아래는 "{week_name}" 기간 동안
스터디원들이 공유한 읽을거리이다.

이 자료들을 바탕으로
하나의 읽기 좋은 Markdown 통합 읽을거리를 작성하라.


## 전체 구성

전체 문서의 약 70%는
여러 글의 내용을 관련 있는 주제끼리 연결하여
하나의 읽기 좋은 통합 읽을거리 형태로 작성한다.

단순히

글 1 요약
글 2 요약
글 3 요약

형태로 나열하지 않는다.

여러 글 사이에서 공통된 흐름이나
연결할 수 있는 내용을 찾아
하나의 자연스러운 글처럼 구성한다.


전체 문서의 약 30%는
이번 주 읽을거리 가운데
내용이 좋은 TOP 3를 선정하여 작성한다.

TOP 3 각각에는 다음 내용을 포함한다.

- 핵심 내용을 더 쉬운 말로 정리
- 이해하는 데 필요한 간단한 배경지식
- 같이 알아두면 좋은 연계 지식


## 작성 원칙

- 원문 내용을 왜곡하지 않는다.
- 원문을 단순히 이어 붙이지 않는다.
- 서로 관련 있는 글들의 연결점을 찾아 설명한다.
- 원문에 없는 구체적인 사실을 임의로 만들어내지 않는다.
- 내용이 빈약한 글을 억지로 활용하지 않는다.
- 대학생이 부담 없이 읽을 수 있게 작성한다.
- Markdown 형식을 사용한다.
- 답변 앞뒤에 별도의 설명을 붙이지 않는다.
- 완성된 Markdown 문서 본문만 출력한다.


============================================================
이번 주 원본 읽을거리
============================================================

{articles_text}
"""

    return prompt.strip()
	```
	---
	<empty-block/>
	## 사용한 다양한 팁들 : 한 번 참고해 주세요!
	### 1. 노션 API 개발자 페이지
	이건 AI랑 직접적인 연관은 없지만 그냥 소개하고 싶었어요 유용해서요! 노션을 깃허브 등에 연동하고 싶을 때 사용하면 유용합니다. 사진에 보이는 ‘API 토큰’ 이걸 사용해서 깃허브에 등록, 연동하는 것입니다.
	‘연결 만들기’ 로 사용하면 됩니다. 노션 CLI 버전은 안 써봤는데 궁금하네요.
	<callout color="gray_bg">
		![](https://prod-files-secure.s3.us-west-2.amazonaws.com/f9d8aebf-e9f1-81e8-bf87-0003a57463fd/afa195c5-76c1-43f7-ac55-528b98a3bc62/%E1%84%89%E1%85%B3%E1%84%8F%E1%85%B3%E1%84%85%E1%85%B5%E1%86%AB%E1%84%89%E1%85%A3%E1%86%BA_2026-10-19_%E1%84%8B%E1%85%A9%E1%84%92%E1%85%AE_12.20.39.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB4662WOTUZVE%2F20261026%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20261026T065547Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEAYaCXVzLXdlc3QtMiJIMEYCIQDcuO9MWQYRDEFRiFJCrMZiEPoKndN7eacPRRVsr7lkigIhANhmHtNrDUn5c1iN5pCZITxBTfSvzQnoMNouQRZDOZJMKogECM%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQABoMNjM3NDIzMTgzODA1Igy4APQFwQwqoVmO9a8q3ANI7uNJnhVWQhPabPX1PqGBUihPXiGQnOtfisrlkDT0rmoxXp9gt6CYMDcNt3yGZFX%2BSYd6kNJqelwKuUqcvoQBqShDjf5YjtIFhnHtEIRPBMaxBhK0FAOPsDMeSvhT04PQrGZilwtTbigJZOPvwAJSjuekYVWEb5%2BAxfSh6MzRv4ZuZAQE4JVtpuaakB8ZfDE2zALjxyI5YEpCq21jn4o1Q0h4A7zLt50A3w1fEia%2FPsY1lyuZv0ghHaDOvjP0XobFxvMt1Ueq1w52TxpBg5ePsfhUxf87soTZGAwIOch3dahaJjhNCv4GOva%2F8dp1EmjL3VrUiFKfWKzof1LEdKgkSVohI2E1fQ8r2NpvuTrAsfgiS79zcZSTrzDly6V6zSaSq6%2Br1u72eICml7ucyBnzq0CjQ5bkVhFP5qyHja750gVnEfXoTdGa%2F7JHADNkIkCpMVvK1AWegs0htUjWb%2Bh5vSFcOh%2BtmEvskkEtLjrSrrJWTQ%2FxlUCPhktZ2I6hIaRxxpMVy%2BLDz2hczTOmmkDrmaJzZMQDGsG3JiKT%2BG%2FtKS4Wd2WhhVtB9eTmri7iAlAsnesjmXwbIh6TQWXV3Gt9SruIpZie7aHsWkZb9CdVixlLl0WqKAyZYfQ37jDuzfvWBjqkAbzOVjtoYaHkJqACJh%2BMnHIpfx3HqYh4QfwxAOfWPdSHfQqcRKnQFc5BCQmzni85o3BLAa5QA%2FOlKiA8IDP2sUGKGd%2FpL6zs%2FSSsIHioPbsyzwjmRfdCj9PvbkTGN9XcVB7V53ERrSzTLoFchx%2FASeAKVcJ9y0DaOMJ%2BGtRlzhK0EAO7WnpR3wl69pNVp0jEWiEMCzgtRKnRfZ0NnEIiXNSPvEIf&X-Amz-Signature=6a82e3fcc9404d9a64f4de54836626bebcbd0e8a165d192d756914d13faf6a2b&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject#notion_record=block.3fe8aebf-e9f1-8043-bd34-c311b3f69555.f9d8aebf-e9f1-81e8-bf87-0003a57463fd)
		![](https://prod-files-secure.s3.us-west-2.amazonaws.com/f9d8aebf-e9f1-81e8-bf87-0003a57463fd/2926d5bd-9f35-43ff-9d5d-406d47567cc3/%E1%84%89%E1%85%B3%E1%84%8F%E1%85%B3%E1%84%85%E1%85%B5%E1%86%AB%E1%84%89%E1%85%A3%E1%86%BA_2026-10-19_%E1%84%8B%E1%85%A9%E1%84%92%E1%85%AE_12.21.38.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB4662WOTUZVE%2F20261026%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20261026T065547Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEAYaCXVzLXdlc3QtMiJIMEYCIQDcuO9MWQYRDEFRiFJCrMZiEPoKndN7eacPRRVsr7lkigIhANhmHtNrDUn5c1iN5pCZITxBTfSvzQnoMNouQRZDOZJMKogECM%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQABoMNjM3NDIzMTgzODA1Igy4APQFwQwqoVmO9a8q3ANI7uNJnhVWQhPabPX1PqGBUihPXiGQnOtfisrlkDT0rmoxXp9gt6CYMDcNt3yGZFX%2BSYd6kNJqelwKuUqcvoQBqShDjf5YjtIFhnHtEIRPBMaxBhK0FAOPsDMeSvhT04PQrGZilwtTbigJZOPvwAJSjuekYVWEb5%2BAxfSh6MzRv4ZuZAQE4JVtpuaakB8ZfDE2zALjxyI5YEpCq21jn4o1Q0h4A7zLt50A3w1fEia%2FPsY1lyuZv0ghHaDOvjP0XobFxvMt1Ueq1w52TxpBg5ePsfhUxf87soTZGAwIOch3dahaJjhNCv4GOva%2F8dp1EmjL3VrUiFKfWKzof1LEdKgkSVohI2E1fQ8r2NpvuTrAsfgiS79zcZSTrzDly6V6zSaSq6%2Br1u72eICml7ucyBnzq0CjQ5bkVhFP5qyHja750gVnEfXoTdGa%2F7JHADNkIkCpMVvK1AWegs0htUjWb%2Bh5vSFcOh%2BtmEvskkEtLjrSrrJWTQ%2FxlUCPhktZ2I6hIaRxxpMVy%2BLDz2hczTOmmkDrmaJzZMQDGsG3JiKT%2BG%2FtKS4Wd2WhhVtB9eTmri7iAlAsnesjmXwbIh6TQWXV3Gt9SruIpZie7aHsWkZb9CdVixlLl0WqKAyZYfQ37jDuzfvWBjqkAbzOVjtoYaHkJqACJh%2BMnHIpfx3HqYh4QfwxAOfWPdSHfQqcRKnQFc5BCQmzni85o3BLAa5QA%2FOlKiA8IDP2sUGKGd%2FpL6zs%2FSSsIHioPbsyzwjmRfdCj9PvbkTGN9XcVB7V53ERrSzTLoFchx%2FASeAKVcJ9y0DaOMJ%2BGtRlzhK0EAO7WnpR3wl69pNVp0jEWiEMCzgtRKnRfZ0NnEIiXNSPvEIf&X-Amz-Signature=fec1f09c1d25fcfa526fa43f3f43f444584e7c1a75fe41c9eaa74c9c32da8756&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject#notion_record=block.3fe8aebf-e9f1-800f-8fd0-cefc67b605a4.f9d8aebf-e9f1-81e8-bf87-0003a57463fd)
	</callout>
	### 2. 제미나이 API key 발급
	구글 AI 스튜디오에서 발급 가능합니다. 연동해서 이것저것 해보세요! (익숙하지 않은 분들을 위해 나중에 스터디에서 API에 대해서 다룰 예정입니다.) 아마 AI 조금 사용해 보신 경험이 있는 분들은 한번쯤은 사용해 봤을 거라고 생각합니다.
	근데 무료라서 엄청난 작업에 사용하기는 무리가 있어요. 다른 API (예를들어 오픈AI라던지)를 발급하려면 돈을 내야합니다. 이런 부분 때문에 지금 제미나이가 AI 시장 경쟁에서 ‘아예 다른 방향으로 달리고 있다’ 라고 말하는 것 같아요. (이 방향이 맞는지는 모르겠지만) 남들이 안 하는 걸 한다..? 독보적..? 인 느낌입니다.
	<callout color="gray_bg">
		![](https://prod-files-secure.s3.us-west-2.amazonaws.com/f9d8aebf-e9f1-81e8-bf87-0003a57463fd/6cc929d7-12e0-4d0c-bc36-f59f36fbfe10/%E1%84%89%E1%85%B3%E1%84%8F%E1%85%B3%E1%84%85%E1%85%B5%E1%86%AB%E1%84%89%E1%85%A3%E1%86%BA_2026-10-19_%E1%84%8B%E1%85%A9%E1%84%92%E1%85%AE_12.23.30.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB4662WOTUZVE%2F20261026%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20261026T065547Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEAYaCXVzLXdlc3QtMiJIMEYCIQDcuO9MWQYRDEFRiFJCrMZiEPoKndN7eacPRRVsr7lkigIhANhmHtNrDUn5c1iN5pCZITxBTfSvzQnoMNouQRZDOZJMKogECM%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQABoMNjM3NDIzMTgzODA1Igy4APQFwQwqoVmO9a8q3ANI7uNJnhVWQhPabPX1PqGBUihPXiGQnOtfisrlkDT0rmoxXp9gt6CYMDcNt3yGZFX%2BSYd6kNJqelwKuUqcvoQBqShDjf5YjtIFhnHtEIRPBMaxBhK0FAOPsDMeSvhT04PQrGZilwtTbigJZOPvwAJSjuekYVWEb5%2BAxfSh6MzRv4ZuZAQE4JVtpuaakB8ZfDE2zALjxyI5YEpCq21jn4o1Q0h4A7zLt50A3w1fEia%2FPsY1lyuZv0ghHaDOvjP0XobFxvMt1Ueq1w52TxpBg5ePsfhUxf87soTZGAwIOch3dahaJjhNCv4GOva%2F8dp1EmjL3VrUiFKfWKzof1LEdKgkSVohI2E1fQ8r2NpvuTrAsfgiS79zcZSTrzDly6V6zSaSq6%2Br1u72eICml7ucyBnzq0CjQ5bkVhFP5qyHja750gVnEfXoTdGa%2F7JHADNkIkCpMVvK1AWegs0htUjWb%2Bh5vSFcOh%2BtmEvskkEtLjrSrrJWTQ%2FxlUCPhktZ2I6hIaRxxpMVy%2BLDz2hczTOmmkDrmaJzZMQDGsG3JiKT%2BG%2FtKS4Wd2WhhVtB9eTmri7iAlAsnesjmXwbIh6TQWXV3Gt9SruIpZie7aHsWkZb9CdVixlLl0WqKAyZYfQ37jDuzfvWBjqkAbzOVjtoYaHkJqACJh%2BMnHIpfx3HqYh4QfwxAOfWPdSHfQqcRKnQFc5BCQmzni85o3BLAa5QA%2FOlKiA8IDP2sUGKGd%2FpL6zs%2FSSsIHioPbsyzwjmRfdCj9PvbkTGN9XcVB7V53ERrSzTLoFchx%2FASeAKVcJ9y0DaOMJ%2BGtRlzhK0EAO7WnpR3wl69pNVp0jEWiEMCzgtRKnRfZ0NnEIiXNSPvEIf&X-Amz-Signature=c200c48469b2f67b4b00c9fc5b38d738cb705f556534c2352946fa487ce977f0&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject#notion_record=block.3fe8aebf-e9f1-8060-98e1-c6e2689d9930.f9d8aebf-e9f1-81e8-bf87-0003a57463fd)
		![](https://prod-files-secure.s3.us-west-2.amazonaws.com/f9d8aebf-e9f1-81e8-bf87-0003a57463fd/6ddfb7b5-dfe5-4fcb-b62b-7f66ff684224/%E1%84%89%E1%85%B3%E1%84%8F%E1%85%B3%E1%84%85%E1%85%B5%E1%86%AB%E1%84%89%E1%85%A3%E1%86%BA_2026-10-19_%E1%84%8B%E1%85%A9%E1%84%92%E1%85%AE_12.26.55.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB4662WOTUZVE%2F20261026%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20261026T065547Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEAYaCXVzLXdlc3QtMiJIMEYCIQDcuO9MWQYRDEFRiFJCrMZiEPoKndN7eacPRRVsr7lkigIhANhmHtNrDUn5c1iN5pCZITxBTfSvzQnoMNouQRZDOZJMKogECM%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQABoMNjM3NDIzMTgzODA1Igy4APQFwQwqoVmO9a8q3ANI7uNJnhVWQhPabPX1PqGBUihPXiGQnOtfisrlkDT0rmoxXp9gt6CYMDcNt3yGZFX%2BSYd6kNJqelwKuUqcvoQBqShDjf5YjtIFhnHtEIRPBMaxBhK0FAOPsDMeSvhT04PQrGZilwtTbigJZOPvwAJSjuekYVWEb5%2BAxfSh6MzRv4ZuZAQE4JVtpuaakB8ZfDE2zALjxyI5YEpCq21jn4o1Q0h4A7zLt50A3w1fEia%2FPsY1lyuZv0ghHaDOvjP0XobFxvMt1Ueq1w52TxpBg5ePsfhUxf87soTZGAwIOch3dahaJjhNCv4GOva%2F8dp1EmjL3VrUiFKfWKzof1LEdKgkSVohI2E1fQ8r2NpvuTrAsfgiS79zcZSTrzDly6V6zSaSq6%2Br1u72eICml7ucyBnzq0CjQ5bkVhFP5qyHja750gVnEfXoTdGa%2F7JHADNkIkCpMVvK1AWegs0htUjWb%2Bh5vSFcOh%2BtmEvskkEtLjrSrrJWTQ%2FxlUCPhktZ2I6hIaRxxpMVy%2BLDz2hczTOmmkDrmaJzZMQDGsG3JiKT%2BG%2FtKS4Wd2WhhVtB9eTmri7iAlAsnesjmXwbIh6TQWXV3Gt9SruIpZie7aHsWkZb9CdVixlLl0WqKAyZYfQ37jDuzfvWBjqkAbzOVjtoYaHkJqACJh%2BMnHIpfx3HqYh4QfwxAOfWPdSHfQqcRKnQFc5BCQmzni85o3BLAa5QA%2FOlKiA8IDP2sUGKGd%2FpL6zs%2FSSsIHioPbsyzwjmRfdCj9PvbkTGN9XcVB7V53ERrSzTLoFchx%2FASeAKVcJ9y0DaOMJ%2BGtRlzhK0EAO7WnpR3wl69pNVp0jEWiEMCzgtRKnRfZ0NnEIiXNSPvEIf&X-Amz-Signature=8fad310764f411ff72a6214062af95bfc3bddd6df33c941395041d116951233b&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject#notion_record=block.3fe8aebf-e9f1-80a1-999b-c2d6dcad4b0f.f9d8aebf-e9f1-81e8-bf87-0003a57463fd)
		→ 이렇게 등록.
	</callout>
</callout>
<empty-block/>
<details>
<summary>출처</summary>
	제 깃허브 레포입니다. 여기에 저희 Reading Materials DB 가 동기화되어 올라갑니다. 여기에 ‘Action’ 부분을 보면 워크플로우 두개가 있습니다. 또한 Setting - Secret Value 뭐 이런 곳에 들어가면 키가 3개 등록되어 있는 걸 확인할 수 있습니다.<br><link-preview url="https://app.notion.com/p/3fe8aebfe9f180918c68cf00a297c2b5#3fe8aebfe9f180b785c4e46f4d6e448c" source="https://github.com/ahin99/2026-AI-TrendAndInfo-ver2" /> 
	<unknown url="https://app.notion.com/p/3fe8aebfe9f180918c68cf00a297c2b5#3fe8aebfe9f180178d69e1e24b4c1a4a" alt="external_object_instance"/>
</details>
![](https://prod-files-secure.s3.us-west-2.amazonaws.com/f9d8aebf-e9f1-81e8-bf87-0003a57463fd/3b145099-3e57-48a9-a0b3-113a03dd7021/%E1%84%89%E1%85%B3%E1%84%8F%E1%85%B3%E1%84%85%E1%85%B5%E1%86%AB%E1%84%89%E1%85%A3%E1%86%BA_2026-10-19_%E1%84%8B%E1%85%A9%E1%84%92%E1%85%AE_12.26.15.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB4662WOTUZVE%2F20261026%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20261026T065547Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEAYaCXVzLXdlc3QtMiJIMEYCIQDcuO9MWQYRDEFRiFJCrMZiEPoKndN7eacPRRVsr7lkigIhANhmHtNrDUn5c1iN5pCZITxBTfSvzQnoMNouQRZDOZJMKogECM%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQABoMNjM3NDIzMTgzODA1Igy4APQFwQwqoVmO9a8q3ANI7uNJnhVWQhPabPX1PqGBUihPXiGQnOtfisrlkDT0rmoxXp9gt6CYMDcNt3yGZFX%2BSYd6kNJqelwKuUqcvoQBqShDjf5YjtIFhnHtEIRPBMaxBhK0FAOPsDMeSvhT04PQrGZilwtTbigJZOPvwAJSjuekYVWEb5%2BAxfSh6MzRv4ZuZAQE4JVtpuaakB8ZfDE2zALjxyI5YEpCq21jn4o1Q0h4A7zLt50A3w1fEia%2FPsY1lyuZv0ghHaDOvjP0XobFxvMt1Ueq1w52TxpBg5ePsfhUxf87soTZGAwIOch3dahaJjhNCv4GOva%2F8dp1EmjL3VrUiFKfWKzof1LEdKgkSVohI2E1fQ8r2NpvuTrAsfgiS79zcZSTrzDly6V6zSaSq6%2Br1u72eICml7ucyBnzq0CjQ5bkVhFP5qyHja750gVnEfXoTdGa%2F7JHADNkIkCpMVvK1AWegs0htUjWb%2Bh5vSFcOh%2BtmEvskkEtLjrSrrJWTQ%2FxlUCPhktZ2I6hIaRxxpMVy%2BLDz2hczTOmmkDrmaJzZMQDGsG3JiKT%2BG%2FtKS4Wd2WhhVtB9eTmri7iAlAsnesjmXwbIh6TQWXV3Gt9SruIpZie7aHsWkZb9CdVixlLl0WqKAyZYfQ37jDuzfvWBjqkAbzOVjtoYaHkJqACJh%2BMnHIpfx3HqYh4QfwxAOfWPdSHfQqcRKnQFc5BCQmzni85o3BLAa5QA%2FOlKiA8IDP2sUGKGd%2FpL6zs%2FSSsIHioPbsyzwjmRfdCj9PvbkTGN9XcVB7V53ERrSzTLoFchx%2FASeAKVcJ9y0DaOMJ%2BGtRlzhK0EAO7WnpR3wl69pNVp0jEWiEMCzgtRKnRfZ0NnEIiXNSPvEIf&X-Amz-Signature=75eb8942e9df2b1dab7a049b9a86a9157ecb90c69b841c24c8659cf4c0539c3f&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject#notion_record=block.3fe8aebf-e9f1-80ba-a26b-f9a6fc7d6312.f9d8aebf-e9f1-81e8-bf87-0003a57463fd)
<empty-block/>
