---
title: "프롬프트 엔지니어링 관련 읽어 보면 좋은 공식 문서들"
created_date: "2026-10-19"
week_start: "2026-10-19"
week_end: "2026-10-25"
notion_page_id: "3fe8aebf-e9f1-8021-a6e0-c5d29737ef5a"
last_edited_time: "2026-10-19T10:08:00.000Z"
notion_url: "https://app.notion.com/p/3fe8aebfe9f18021a6e0c5d29737ef5a"
---
# 프롬프트 엔지니어링 관련 읽어 보면 좋은 공식 문서들

<callout>
	아까 올린 글에서<br><span color="red">너는 대학생 AI 스터디의 주간 읽을거리를 만드는 편집자다. → 이런식으로 프롬프트 넣는 게 요즘엔 엄청 올드한 거라던데 맞나요..? <br></span>이 부분에 있어서 궁금해서 찾아봤습니다. 프롬프트 엔지니어링 관련해서 AI 기업들에서 낸 공식 문서들을 일단 봤는데요.
	결론적으로는 위 프롬프트가 유효하다는 생각이 듭니다..? 근데 잘 모르겠는 게 아마 사용자들이 더 개발을 거친 게 더 효율적인 방법으로 나왔을 것 같긴 해요 (아무래도 공식이니까 스탠다드를 제시해줄뿐 트렌디한 부분은 좀 떨어지겠죠)
	<empty-block/>
	---
	<empty-block/>
	prompt library 라고 구글에 검색해보면 자료가 많이 나옵니다.
	프롬프트 엔지니어링에 대해서 다음차시 스터디에 다룰거기는 하지만 일단 공식 문서들 위주로 보면 좋을 것 같아서, 제가 읽어본 것들만 링크 달겠습니다. 
	<callout color="gray_bg">
		[Prompt engineering \| OpenAI API](https://developers.openai.com/api/docs/guides/prompt-engineering?utm_source=chatgpt.com&api-mode=responses)
		[Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)
	</callout>
	## 1.
	일단 간단하게 핵심을 정리해보자면 다음과 같은 프롬프트 구성이 좋다고 합니다.<br>- 독자가 누구인지 명시. 누구를 위한 프로그램인지 명시.<br>- 전체 상위 규칙 제시<br>- 출력 형식 제시 (어떤 문서로 결과물을 만들건지. 마크다운인지 JSON인지 등)<br>- 최종 출력 전에 확인할 사항들 (최종 검증)<br>- 이번 생성에서 하지 말아야 할 것들 (범위 제한)
	## 2.
	또한 openAI 자료를 살펴보니까, 모델에 따라서 어떻게 프롬프트를 넣어야 하는지도 중요합니다. <br>- 높은 추론 수준의 상위 AI 모델 (아스트라, Opus 최신모델 등) → 고수준 지침(즉 세부사항은 덜 정밀하지만 최종 목표/청사진 설계가 잘 되어 있는 명령. 조금은 모호해도 괜찮음.)이 있는 프롬프트에서 더 좋은 결과를 냄.<br>- 더 낮은 수준의 모델 → 특정 출력을 생성하기 위한 정확한 명시적인 지시가 있을 때 가장 잘 수행됨. 너무 넓은 차원의 모호한 지시는 잘 해석 못함.
	→ OpenAI Developers 자료에서, <br>높은 추론 모델 = 시니어 동료( 달성할 목표를 설정하고, 세부 사항을 해결하도록 신뢰)<br>낮은 모델 = 주니어 동료(특정 출력을 생성하기 위한 명시적인 지시가 있을 때 가장 잘 수행)<br>로 비유하고 있습니다. 
	## 3.
	그리고 복잡한 프롬프트를 넣을 때는 마크다운 또는 XML 문서에 프롬프트를 따로 작성해서 넣으면 AI가 더 이해하기 쉽습니다. (마크다운과 XML로 계층적 인덱싱을 해 주는 것만으로도 AI 입장에서 가독성이 올라감)
</callout>
<details>
<summary>출처</summary>
	아래에 출처를 입력하세요
</details>
<empty-block/>
