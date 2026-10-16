GitHub Actions의 `Sync Notion to GitHub` → `Run workflow` 버튼으로 노션 글을 동기화합니다.

글은 노션 DB의 `생성일` 속성을 기준으로 월요일부터 일요일까지 묶어서 저장합니다.
예를 들어 2026-10-12(월)부터 2026-10-18(일)까지의 글은 다음 폴더에 들어갑니다.

```text
notion-posts/
  2026-10-12_2026-10-18/
    글 제목--페이지ID.md
  2026-10-19_2026-10-25/
    다른 글 제목--페이지ID.md
```

- `생성일`은 날짜(`date`) 또는 생성 시각(`created_time`) 속성을 지원합니다. 날짜 범위는 시작일을 사용합니다.
- `생성일` 속성이 없거나 비어 있으면 경고를 출력하고 노션 페이지의 실제 생성 시각을 사용합니다.
- 날짜만 있으면 해당 날짜를 그대로 사용하고, 시간이 포함되면 한국 시간(`Asia/Seoul`)으로 변환해서 주차를 계산합니다.
- 월말이나 연말에도 월요일부터 일요일까지 하나의 폴더로 묶습니다.
- 글의 메타데이터에는 `created_date`, `week_start`, `week_end`를 기록합니다. 세션 속성은 더 이상 사용하지 않습니다.
- 한 번 실행할 때 모든 주차 폴더의 변경 사항을 하나의 커밋으로 저장합니다. 변경이 없으면 커밋하지 않습니다.

속성 이름이나 시간대를 바꾸려면 `.github/workflows/sync-notion.yml`의
`NOTION_CREATED_DATE_PROPERTY`, `NOTION_TIMEZONE` 값을 수정합니다.
기존 `NOTION_TOKEN`, `NOTION_DATA_SOURCE_ID` GitHub Secrets는 그대로 사용합니다.

다음 동기화 실행 시 기존 세션/미분류 폴더가 제거되고 노션에서 읽은 생성일에 따라 주차별 폴더로 다시 만들어집니다.
`notion-posts/`는 실행할 때마다 전체를 다시 생성하므로 사람이 직접 작성한 파일을 넣으면 안 됩니다.

주차 계산 및 동기화 검증: `python3 -m unittest discover -s tests -v`
