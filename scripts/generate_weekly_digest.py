import os
import re
import hashlib
from datetime import datetime
from pathlib import Path

from google import genai


POSTS_DIR = Path("notion-posts")
OUTPUT_DIR = Path("weekly-digests")

MODEL_NAME = "gemini-3.8-flash"


# ============================================================
# Markdown 정리
# ============================================================

def strip_frontmatter(text: str) -> str:
    return re.sub(
        r"^---\s*\n.*?\n---\s*\n",
        "",
        text,
        count=1,
        flags=re.DOTALL,
    ).strip()


def clean_markdown(text: str) -> str:
    text = strip_frontmatter(text)

    text = text.replace("<empty-block/>", "")

    text = re.sub(
        r"</?callout[^>]*>",
        "",
        text,
        flags=re.IGNORECASE,
    )

    text = re.sub(
        r"</?span[^>]*>",
        "",
        text,
        flags=re.IGNORECASE,
    )

    text = re.sub(
        r"<file[^>]*>.*?</file>",
        "[첨부파일 생략]",
        text,
        flags=re.DOTALL | re.IGNORECASE,
    )

    text = re.sub(
        r"!\[[^\]]*\]\(https://prod-files-secure\.s3[^)]*\)",
        "[이미지 생략]",
        text,
        flags=re.IGNORECASE,
    )

    text = re.sub(
        r"\n{4,}",
        "\n\n\n",
        text,
    )

    return text.strip()


# ============================================================
# 제목 추출
# ============================================================

def get_article_title(file_path: Path, text: str) -> str:
    match = re.search(
        r"^#\s+(.+)$",
        text,
        flags=re.MULTILINE,
    )

    if match:
        return match.group(1).strip()

    return file_path.stem


# ============================================================
# 내용 없는 글 판단
# ============================================================

def is_empty_article(text: str) -> bool:
    temp = text

    temp = re.sub(
        r"^#+\s*",
        "",
        temp,
        flags=re.MULTILINE,
    )

    temp = re.sub(
        r"</?(details|summary)[^>]*>",
        "",
        temp,
        flags=re.IGNORECASE,
    )

    temp = temp.replace(
        "아래에 출처를 입력하세요",
        "",
    )

    temp = re.sub(
        r"[\s#>*_`\-]",
        "",
        temp,
    )

    return len(temp) < 80


# ============================================================
# 주차 폴더 찾기
# ============================================================

def get_latest_week_folder():
    """
    notion-posts 아래에서 실제 Markdown 파일이 들어 있는
    폴더들을 찾고, 폴더명에 포함된 첫 날짜를 기준으로
    가장 최신 주차를 선택한다.
    """

    candidates = []

    print("주차 폴더 검색 시작")

    for folder in POSTS_DIR.iterdir():

        if not folder.is_dir():
            continue

        md_files = list(folder.rglob("*.md"))

        print(
            f"  폴더 발견: {folder.name} "
            f"(Markdown {len(md_files)}개)"
        )

        # Markdown이 없는 폴더는 주차 폴더가 아님
        if not md_files:
            continue

        # 폴더명에서 YYYY-MM-DD 찾기
        date_match = re.search(
            r"\d{4}-\d{2}-\d{2}",
            folder.name
        )

        if not date_match:
            print(
                f"  [SKIP] 날짜를 찾을 수 없음: {folder.name}"
            )
            continue

        date_text = date_match.group()

        try:
            start_date = datetime.strptime(
                date_text,
                "%Y-%m-%d"
            )

        except ValueError:
            print(
                f"  [SKIP] 잘못된 날짜 형식: {folder.name}"
            )
            continue

        candidates.append(
            (start_date, folder)
        )

    if not candidates:
        raise RuntimeError(
            "Markdown이 들어 있는 주차 폴더를 찾지 못했습니다. "
            "notion-posts 폴더 구조를 확인하세요."
        )

    candidates.sort(
        key=lambda item: item[0]
    )

    latest_folder = candidates[-1][1]

    print(
        f"최신 주차 폴더 선택: {latest_folder}"
    )

    return latest_folder


# ============================================================
# 주차 Markdown 읽기
# ============================================================

def read_week_articles(week_folder: Path):
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
                f"  [SKIP] 내용 부족: {file_path.name}"
            )

            continue

        title = get_article_title(
            file_path,
            content
        )

        print(
            f"  [READ] {title}"
        )

        articles.append(
            {
                "title": title,
                "content": content,
                "path": str(file_path),
            }
        )

    if not articles:
        raise RuntimeError(
            "최신 주차 폴더에 Gemini에 전달할 "
            "유효한 Markdown 글이 없습니다."
        )

    return articles


# ============================================================
# 변경 여부 hash
# ============================================================

def calculate_source_hash(articles):
    combined = ""

    for article in articles:

        combined += article["path"]
        combined += "\n"

        combined += article["content"]
        combined += "\n\n"

    return hashlib.sha256(
        combined.encode("utf-8")
    ).hexdigest()


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
# 프롬프트
# 나중에 다시 정교하게 개발 예정
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

    return f"""
너는 대학생 AI 스터디의 주간 읽을거리 편집자다.

아래는 "{week_name}" 기간에
스터디원들이 공유한 읽을거리이다.

하나의 읽기 좋은 Markdown 문서로 재구성하라.

전체 분량의 약 70%는
여러 글의 내용을 관련 주제끼리 연결한
통합 읽을거리로 작성한다.

전체 분량의 약 30%는
내용이 좋은 TOP 3 글을 선정하여 다음을 작성한다.

- 핵심 내용을 쉬운 말로 정리
- 이해에 필요한 간단한 배경지식
- 같이 알아두면 좋은 연계 지식

주의:

- 글을 하나씩 단순 요약해서 나열하지 않는다.
- 서로 관련 있는 내용을 연결한다.
- 원문 내용을 왜곡하지 않는다.
- 원문에 없는 구체적인 사실을 임의로 만들지 않는다.
- Markdown 본문만 출력한다.


============================================================
원본 읽을거리
============================================================

{articles_text}
""".strip()


# ============================================================
# Gemini 호출
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

    print()
    print(
        f"Gemini API 호출 시작"
    )

    print(
        f"모델: {MODEL_NAME}"
    )

    print(
        f"입력 글 수: {len(articles)}"
    )

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
    )

    if not response.text:
        raise RuntimeError(
            "Gemini 응답 내용이 비어 있습니다."
        )

    print(
        "Gemini 응답 수신 완료"
    )

    return response.text.strip()


# ============================================================
# 저장
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

    print()
    print(
        f"통합 읽을거리 저장 완료:"
    )

    print(
        output_file
    )


# ============================================================
# main
# ============================================================

def main():

    print(
        "===== Weekly Digest Generator ====="
    )

    # API Key
    api_key = os.getenv(
        "GEMINI_API_KEY"
    )

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY가 설정되어 있지 않습니다."
        )

    # notion-posts 확인
    if not POSTS_DIR.exists():
        raise RuntimeError(
            "notion-posts 폴더가 없습니다."
        )

    # 최신 주차 찾기
    week_folder = get_latest_week_folder()

    week_name = week_folder.name

    print()
    print(
        f"처리 대상: {week_name}"
    )

    # 최신 주차 글 읽기
    articles = read_week_articles(
        week_folder
    )

    print()
    print(
        f"유효한 읽을거리: {len(articles)}개"
    )

    # 현재 주차 원문 hash
    source_hash = calculate_source_hash(
        articles
    )

    output_file = (
        OUTPUT_DIR
        / f"{week_name}.md"
    )

    existing_hash = get_existing_hash(
        output_file
    )

    # 같은 현재 주차이고 내용도 동일하면 재생성 안 함
    if existing_hash == source_hash:

        print(
            "현재 주차 원문에 변경이 없습니다."
        )

        print(
            "기존 통합 읽을거리를 유지합니다."
        )

        return

    # Gemini 호출
    client = genai.Client(
        api_key=api_key
    )

    digest = generate_digest(
        client,
        week_name,
        articles,
    )

    # 저장
    save_digest(
        week_name,
        source_hash,
        digest,
    )

    print()
    print(
        "===== 완료 ====="
    )


if __name__ == "__main__":
    main()