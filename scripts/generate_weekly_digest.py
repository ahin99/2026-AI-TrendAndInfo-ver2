import os
import re
import time
import random
from pathlib import Path

from google import genai
from google.genai import errors


# ============================================================
# 기본 설정
# ============================================================

POSTS_DIR = Path("notion-posts")
OUTPUT_DIR = Path("weekly-digests")

MODEL_NAME = "gemini-3.8-flash"
FALLBACK_MODELS = ["gemini-3.6-flash", "gemini-3.5-flash-lite"]
MAX_ATTEMPTS_PER_MODEL = 2  # SDK 자체 재시도 외 추가 시도 횟수


# ============================================================
# Markdown frontmatter 제거
# ============================================================

def strip_frontmatter(text: str) -> str:
    """
    Markdown 맨 위의 YAML frontmatter를 제거한다.

    예:

    ---
    title: "공강 블럭"
    created_date: "2026-10-13"
    week_start: "2026-10-12"
    week_end: "2026-10-18"
    ---

    Gemini에게는 실제 글 내용을 중심으로 전달한다.
    """

    return re.sub(
        r"^---\s*\n.*?\n---\s*\n",
        "",
        text,
        count=1,
        flags=re.DOTALL,
    ).strip()


# ============================================================
# Markdown 정리
# ============================================================

def clean_markdown(text: str) -> str:
    """
    Notion → Markdown 변환 과정에서 들어간
    불필요한 태그나 지나치게 긴 이미지 주소를 정리한다.

    글 내용은 최대한 그대로 유지한다.
    """

    text = strip_frontmatter(text)

    # Notion empty block 제거
    text = text.replace(
        "<empty-block/>",
        "",
    )

    # callout 태그만 제거
    # 내부 내용은 그대로 남긴다.
    text = re.sub(
        r"</?callout[^>]*>",
        "",
        text,
        flags=re.IGNORECASE,
    )

    # span 태그만 제거
    text = re.sub(
        r"</?span[^>]*>",
        "",
        text,
        flags=re.IGNORECASE,
    )

    # Notion 첨부 파일 태그 제거
    text = re.sub(
        r"<file[^>]*>.*?</file>",
        "[첨부파일 생략]",
        text,
        flags=re.DOTALL | re.IGNORECASE,
    )

    # Notion의 매우 긴 S3 이미지 링크 제거
    text = re.sub(
        r"!\[[^\]]*\]\(https://prod-files-secure\.s3[^)]*\)",
        "[이미지 생략]",
        text,
        flags=re.IGNORECASE,
    )

    # 지나치게 많은 빈 줄 정리
    text = re.sub(
        r"\n{4,}",
        "\n\n\n",
        text,
    )

    return text.strip()


# ============================================================
# 글 제목 추출
# ============================================================

def get_article_title(
    file_path: Path,
    text: str,
) -> str:
    """
    Markdown의 첫 번째 # 제목을 글 제목으로 사용한다.

    없다면 파일명을 사용한다.
    """

    match = re.search(
        r"^#\s+(.+)$",
        text,
        flags=re.MULTILINE,
    )

    if match:
        return match.group(1).strip()

    return file_path.stem


# ============================================================
# 사실상 빈 글인지 판단
# ============================================================

def is_empty_article(text: str) -> bool:
    """
    Notion에서 새 페이지를 만들기만 하고
    실제 내용을 작성하지 않은 글 등을 제외한다.

    너무 엄격하게 판단하지 않고,
    정말 내용이 없는 경우만 제거한다.
    """

    temp = text

    # details / summary 태그 제거
    temp = re.sub(
        r"</?(details|summary)[^>]*>",
        "",
        temp,
        flags=re.IGNORECASE,
    )

    # 기본 안내문 제거
    meaningless_texts = [
        "아래에 출처를 입력하세요",
        "새 읽을거리 생성! 제목을 입력하세요",
        "출처",
    ]

    for meaningless in meaningless_texts:
        temp = temp.replace(
            meaningless,
            "",
        )

    # Markdown 제목 기호 제거
    temp = re.sub(
        r"^#+\s*",
        "",
        temp,
        flags=re.MULTILINE,
    )

    # 기타 HTML 태그 제거
    temp = re.sub(
        r"<[^>]+>",
        "",
        temp,
    )

    # Markdown 기호 및 공백 제거
    temp = re.sub(
        r"[\s#>*_`\-]",
        "",
        temp,
    )

    # 실제 텍스트가 거의 없다면 빈 글로 처리
    return len(temp) < 30


# ============================================================
# 선택한 주차의 Markdown 읽기
# ============================================================

def read_week_articles(
    week_folder: Path,
):
    """
    사용자가 선택한 주차 폴더에 있는
    Markdown 파일들만 읽는다.
    """

    articles = []

    markdown_files = sorted(
        week_folder.rglob("*.md")
    )

    print(
        f"Markdown 파일 {len(markdown_files)}개 발견"
    )

    for file_path in markdown_files:

        raw_text = file_path.read_text(
            encoding="utf-8"
        )

        content = clean_markdown(
            raw_text
        )

        if is_empty_article(content):

            print(
                f"[SKIP] 내용 없음: {file_path.name}"
            )

            continue

        title = get_article_title(
            file_path,
            content,
        )

        print(
            f"[READ] {title}"
        )

        articles.append(
            {
                "title": title,
                "content": content,
            }
        )

    if not articles:

        raise RuntimeError(
            "선택한 주차에 Gemini에게 전달할 "
            "유효한 읽을거리가 없습니다."
        )

    return articles


# ============================================================
# Gemini 프롬프트
#
# ★ 나중에 프롬프트 개발할 때 주로 이 함수만 수정하면 됨
# ============================================================

def build_prompt(
    week_name: str,
    articles,
):

    articles_text = ""

    for index, article in enumerate(
        articles,
        start=1,
    ):

        articles_text += f"""

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


# ============================================================
# Gemini API 호출
# ============================================================

def generate_digest(
    client,
    week_name: str,
    articles,
):
    prompt = build_prompt(week_name, articles)

    print()
    print("Gemini API 호출 시작")
    print(f"기본 모델: {MODEL_NAME}")
    print(f"입력 글 수: {len(articles)}")

    models = [MODEL_NAME, *FALLBACK_MODELS]
    last_error = None

    for model in models:
        for attempt in range(1, MAX_ATTEMPTS_PER_MODEL + 1):
            print(f"[Gemini] 모델={model}, 시도={attempt}/{MAX_ATTEMPTS_PER_MODEL}", flush=True)
            try:
                response = client.models.generate_content(
                    model=model,
                    contents=prompt,
                )
                if not response.text:
                    raise RuntimeError(
                        f"Gemini가 빈 응답을 반환했습니다. 모델: {model}"
                    )

                print(f"Gemini 응답 수신 완료 (실제 사용 모델: {model})")
                return response.text.strip(), model

            except errors.APIError as exc:
                last_error = exc
                status = getattr(exc, "code", None)
                print(f"[Gemini 오류] 모델={model}, HTTP={status}: {exc}", flush=True)

                # 일시적인 오류에 대해서만 재시도/대체 모델을 적용한다.
                # 인증/잘못된 요청 등은 재시도로 해결되지 않으므로 즉시 알린다.
                if status not in (408, 429, 500, 502, 503, 504):
                    raise

                if attempt < MAX_ATTEMPTS_PER_MODEL:
                    delay = 5 * (2 ** (attempt - 1)) + random.uniform(0, 2)
                    print(f"[RETRY] {delay:.1f}초 후 재시도", flush=True)
                    time.sleep(delay)

        print(f"[FALLBACK] {model} 사용 실패, 다음 모델 확인", flush=True)

    raise RuntimeError(
        "모든 Gemini 모델이 일시적인 API 오류로 실패했습니다. "
        "잠시 후 워크플로를 다시 실행하세요."
    ) from last_error


# ============================================================
# 통합 읽을거리 저장
# ============================================================

def save_digest(
    week_name: str,
    content: str,
    used_model: str,
):
    """
    weekly-digests/주차.md 로 저장한다.

    같은 파일이 이미 존재하면
    write_text()에 의해 새 결과로 완전히 교체된다.
    """

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_file = (
        OUTPUT_DIR
        / f"{week_name}.md"
    )

    if output_file.exists():

        print()
        print(
            "기존 통합 읽을거리가 존재합니다."
        )

        print(
            "새 Gemini 결과로 덮어씁니다."
        )

    header = f"""---
source_week: "{week_name}"
generated_by: "Gemini"
model: "{used_model}"
---

"""

    output_file.write_text(
        header + content + "\n",
        encoding="utf-8",
    )

    print()
    print(
        f"저장 완료: {output_file}"
    )


# ============================================================
# main
# ============================================================

def main():

    print(
        "===== Weekly Digest Generator ====="
    )

    # --------------------------------------------------------
    # Gemini API Key
    # --------------------------------------------------------

    api_key = os.getenv(
        "GEMINI_API_KEY"
    )

    if not api_key:

        raise RuntimeError(
            "GEMINI_API_KEY가 설정되어 있지 않습니다."
        )

    # --------------------------------------------------------
    # GitHub Actions에서 선택한 주차
    # --------------------------------------------------------

    week_name = os.getenv(
        "WEEK_FOLDER"
    )

    if not week_name:

        raise RuntimeError(
            "WEEK_FOLDER가 설정되어 있지 않습니다."
        )

    # --------------------------------------------------------
    # 보안 / 잘못된 경로 방지
    #
    # 주차 폴더명 하나만 허용
    # 예:
    # 2026-10-12_2026-10-18
    # --------------------------------------------------------

    if (
        Path(week_name).name != week_name
        or "/" in week_name
        or "\\" in week_name
    ):

        raise RuntimeError(
            "잘못된 WEEK_FOLDER 값입니다."
        )

    week_folder = (
        POSTS_DIR
        / week_name
    )

    # --------------------------------------------------------
    # 선택한 주차 폴더 확인
    # --------------------------------------------------------

    if not week_folder.exists():

        raise RuntimeError(
            f"주차 폴더가 없습니다: {week_folder}"
        )

    if not week_folder.is_dir():

        raise RuntimeError(
            f"주차 경로가 폴더가 아닙니다: {week_folder}"
        )

    print()
    print(
        f"선택한 주차: {week_name}"
    )

    print(
        f"읽을 폴더: {week_folder}"
    )

    # --------------------------------------------------------
    # 해당 주차의 글 읽기
    # --------------------------------------------------------

    articles = read_week_articles(
        week_folder
    )

    print()
    print(
        f"유효한 읽을거리: {len(articles)}개"
    )

    # --------------------------------------------------------
    # Gemini Client
    # --------------------------------------------------------

    client = genai.Client(
        api_key=api_key
    )

    # --------------------------------------------------------
    # 매번 새로 생성
    #
    # 기존 통합 읽을거리가 있는지 여부와 관계없이
    # Gemini API를 다시 호출한다.
    # --------------------------------------------------------

    digest, used_model = generate_digest(
        client,
        week_name,
        articles,
    )

    # --------------------------------------------------------
    # 저장
    #
    # 기존 파일이 있으면 overwrite
    # --------------------------------------------------------

    save_digest(
        week_name,
        digest,
        used_model,
    )

    print()
    print(
        "===== Weekly Digest 생성 완료 ====="
    )


if __name__ == "__main__":
    main()
