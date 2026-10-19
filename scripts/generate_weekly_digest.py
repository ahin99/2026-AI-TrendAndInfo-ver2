import os
import re
import hashlib
from pathlib import Path

from google import genai


# ============================================================
# 기본 설정
# ============================================================

# Notion → Markdown 결과가 저장되는 폴더
POSTS_DIR = Path("notion-posts")

# Gemini 통합 읽을거리 저장 폴더
OUTPUT_DIR = Path("weekly-digests")

# Gemini 모델
MODEL_NAME = "gemini-3.8-flash"


# ============================================================
# Markdown 전처리
# ============================================================

def strip_frontmatter(text: str) -> str:
    """
    Markdown 맨 위의 YAML frontmatter를 제거한다.

    예:
    ---
    title: "공강 블럭"
    week_start: "2026-10-12"
    week_end: "2026-10-18"
    ---
    """

    return re.sub(
        r"^---\s*\n.*?\n---\s*\n",
        "",
        text,
        count=1,
        flags=re.DOTALL,
    ).strip()


def clean_markdown(text: str) -> str:
    """
    Notion Markdown에 포함된 불필요한 태그 등을 정리한다.
    실제 글 내용은 최대한 유지한다.
    """

    # YAML frontmatter 제거
    text = strip_frontmatter(text)

    # 빈 블럭 제거
    text = text.replace("<empty-block/>", "")

    # callout 태그는 제거하지만 내용은 유지
    text = re.sub(
        r"</?callout[^>]*>",
        "",
        text,
        flags=re.IGNORECASE,
    )

    # span 태그 제거
    text = re.sub(
        r"</?span[^>]*>",
        "",
        text,
        flags=re.IGNORECASE,
    )

    # Notion 첨부파일 태그 제거
    text = re.sub(
        r"<file[^>]*>.*?</file>",
        "[첨부파일 생략]",
        text,
        flags=re.DOTALL | re.IGNORECASE,
    )

    # Notion의 매우 긴 이미지 URL 제거
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
# 글 제목 가져오기
# ============================================================

def get_article_title(file_path: Path, text: str) -> str:
    """
    Markdown의 첫 번째 # 제목을 글 제목으로 사용한다.

    없으면 파일명을 사용한다.
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
# 내용 없는 글 제외
# ============================================================

def is_empty_article(text: str) -> bool:
    """
    제목만 있고 실제 본문이 거의 없는 파일은 제외한다.
    """

    temp = text

    # Markdown 제목 제거
    temp = re.sub(
        r"^#+\s*",
        "",
        temp,
        flags=re.MULTILINE,
    )

    # details / summary 태그 제거
    temp = re.sub(
        r"</?(details|summary)[^>]*>",
        "",
        temp,
        flags=re.IGNORECASE,
    )

    # 기본 출처 문구 제거
    temp = temp.replace(
        "아래에 출처를 입력하세요",
        "",
    )

    # Markdown 기호 / 공백 제거
    temp = re.sub(
        r"[\s#>*_`\-]",
        "",
        temp,
    )

    # 실제 내용이 너무 적으면 제외
    return len(temp) < 80


# ============================================================
# 한 주 폴더의 Markdown 읽기
# ============================================================

def read_week_articles(week_folder: Path):
    """
    최신 주차 폴더 안의 Markdown 파일을 모두 읽는다.
    """

    articles = []

    markdown_files = sorted(
        week_folder.rglob("*.md")
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
                f"  [SKIP] 내용이 거의 없음: {file_path.name}"
            )

            continue

        title = get_article_title(
            file_path,
            content
        )

        articles.append(
            {
                "title": title,
                "content": content,
                "path": str(file_path),
            }
        )

    return articles


# ============================================================
# 현재 주차 글 변경 여부 확인용 hash
# ============================================================

def calculate_source_hash(articles):
    """
    현재 주차의 글 내용이 변경됐는지 확인하기 위한 hash.

    과거 주차에는 사용하지 않는다.
    """

    combined = ""

    for article in articles:

        combined += article["path"]
        combined += "\n"

        combined += article["content"]
        combined += "\n\n"

    return hashlib.sha256(
        combined.encode("utf-8")
    ).hexdigest()


# ============================================================
# 기존 현재 주차 digest의 hash 읽기
# ============================================================

def get_existing_hash(output_file: Path):

    if not output_file.exists():
        return None

    text = output_file.read_text(
        encoding="utf-8"
    )

    match = re.search(
        r'^source_hash:\s*"?([0-9a-f]{64})"?',
        text,
        flags=re.MULTILINE,
    )

    if match:
        return match.group(1)

    return None


# ============================================================
# Gemini 프롬프트
#
# 지금은 임시 버전.
# 나중에 별도로 정교하게 수정 예정.
# ============================================================

def build_prompt(week_name: str, articles):

    articles_text = ""

    for index, article in enumerate(
        articles,
        start=1
    ):

        articles_text += f"""

============================================================
읽을거리 {index}
제목: {article["title"]}
============================================================

{article["content"]}

"""

    prompt = f"""
너는 대학생 AI 스터디의 주간 읽을거리 편집자다.

아래 자료들은 "{week_name}" 한 주 동안
스터디원들이 공유한 읽을거리이다.

이 자료들을 바탕으로
하나의 읽기 좋은 Markdown 문서를 작성하라.


전체 문서 구성:

1. 약 70%
   여러 글의 내용을 관련 있는 주제끼리 연결하여
   하나의 읽기 좋은 통합 읽을거리로 작성한다.

2. 약 30%
   이번 주 읽을거리 가운데 내용이 좋은 TOP 3를 선정한다.

   TOP 3 각각에 대해:
   - 핵심 내용을 쉬운 말로 정리
   - 이해에 필요한 간단한 배경지식
   - 같이 알아두면 좋은 연계 지식

주의사항:

- 글을 하나씩 단순 요약해서 나열하지 않는다.
- 서로 관련된 글의 연결점을 찾아 설명한다.
- 원문 내용을 왜곡하지 않는다.
- 원문에 없는 구체적 사실을 임의로 만들지 않는다.
- 내용이 빈약한 글을 억지로 사용하지 않는다.
- 읽기 좋은 Markdown 문서로 작성한다.
- 답변 앞뒤에 부가 설명을 붙이지 않는다.
- Markdown 본문만 출력한다.


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

    prompt = build_prompt(
        week_name,
        articles,
    )

    print(
        f"  Gemini API 호출 ({len(articles)}개 글)"
    )

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
    )

    if not response.text:
        raise RuntimeError(
            "Gemini가 응답을 반환하지 않았습니다."
        )

    return response.text.strip()


# ============================================================
# 결과 저장
# ============================================================

def save_digest(
    week_name: str,
    source_hash: str,
    content: str,
):

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_file = (
        OUTPUT_DIR
        / f"{week_name}.md"
    )

    header = f"""---
source_week: "{week_name}"
generated_by: "Gemini"
model: "{MODEL_NAME}"
source_hash: "{source_hash}"
---

"""

    output_file.write_text(
        header + content + "\n",
        encoding="utf-8",
    )

    print(
        f"  [SAVE] {output_file}"
    )


# ============================================================
# main
# ============================================================

def main():

    # --------------------------------------------------------
    # Gemini API Key 확인
    # --------------------------------------------------------

    api_key = os.getenv(
        "GEMINI_API_KEY"
    )

    if not api_key:

        raise RuntimeError(
            "GEMINI_API_KEY 환경변수가 없습니다."
        )

    # --------------------------------------------------------
    # notion-posts 확인
    # --------------------------------------------------------

    if not POSTS_DIR.exists():

        raise FileNotFoundError(
            f"{POSTS_DIR} 폴더를 찾을 수 없습니다."
        )

    # --------------------------------------------------------
    # 주차 폴더 목록 가져오기
    # --------------------------------------------------------

    week_folders = sorted(
        [
            folder
            for folder in POSTS_DIR.iterdir()
            if folder.is_dir()
        ]
    )

    if not week_folders:

        print(
            "주차 폴더가 없습니다."
        )

        return

    # ========================================================
    # 핵심:
    #
    # 가장 최신 주차 폴더 하나만 처리한다.
    #
    # 과거 주차는 원문이 변경돼도
    # 절대 다시 확인하거나 수정하지 않는다.
    # ========================================================

    current_week_folder = week_folders[-1]

    week_name = current_week_folder.name

    print(
        f"현재 처리 대상 주차: {week_name}"
    )

    print(
        f"과거 {len(week_folders) - 1}개 주차는 처리하지 않습니다."
    )

    # --------------------------------------------------------
    # 현재 주차 글 읽기
    # --------------------------------------------------------

    articles = read_week_articles(
        current_week_folder
    )

    if not articles:

        print(
            "현재 주차에 읽을 수 있는 글이 없습니다."
        )

        return

    print(
        f"유효한 읽을거리: {len(articles)}개"
    )

    # --------------------------------------------------------
    # 현재 주차의 원문 hash 생성
    # --------------------------------------------------------

    source_hash = calculate_source_hash(
        articles
    )

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_file = (
        OUTPUT_DIR
        / f"{week_name}.md"
    )

    existing_hash = get_existing_hash(
        output_file
    )

    # --------------------------------------------------------
    # 현재 주차의 원문이 바뀌지 않았다면 API 호출 X
    # --------------------------------------------------------

    if existing_hash == source_hash:

        print(
            "현재 주차 글에 변경이 없습니다."
        )

        print(
            "Gemini API를 호출하지 않습니다."
        )

        return

    # --------------------------------------------------------
    # 현재 주차가 새로 생겼거나
    # 현재 주차 글이 추가/수정된 경우
    # --------------------------------------------------------

    client = genai.Client(
        api_key=api_key
    )

    digest = generate_digest(
        client,
        week_name,
        articles,
    )

    save_digest(
        week_name,
        source_hash,
        digest,
    )

    print()
    print(
        "Weekly Digest 생성 완료"
    )


if __name__ == "__main__":
    main()