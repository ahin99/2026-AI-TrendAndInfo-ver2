import json
import os
import re
import shutil
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo


NOTION_TOKEN = os.environ["NOTION_TOKEN"]
DATA_SOURCE_ID = os.environ["NOTION_DATA_SOURCE_ID"]

OUTPUT_DIR = Path(
    os.environ.get(
        "NOTION_OUTPUT_DIR",
        "notion-posts"
    )
)

# Notion DB의 생성일 속성 이름과 주차 계산 시간대
CREATED_DATE_PROPERTY = os.environ.get("NOTION_CREATED_DATE_PROPERTY", "생성일")
SYNC_TIMEZONE = ZoneInfo(os.environ.get("NOTION_TIMEZONE", "Asia/Seoul"))

API_BASE = "https://api.notion.com/v1"


def api_request(
    method,
    path,
    body=None,
    notion_version="2025-09-03"
):
    url = f"{API_BASE}{path}"

    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": notion_version,
        "Content-Type": "application/json",
    }

    data = None

    if body is not None:
        data = json.dumps(body).encode("utf-8")

    request = urllib.request.Request(
        url,
        data=data,
        headers=headers,
        method=method,
    )

    try:
        with urllib.request.urlopen(request) as response:
            return json.loads(
                response.read().decode("utf-8")
            )

    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")

        raise RuntimeError(
            f"Notion API error: HTTP {e.code}\n"
            f"{error_body}"
        ) from e


def query_all_pages():
    pages = []
    start_cursor = None

    while True:
        body = {
            "page_size": 100
        }

        if start_cursor:
            body["start_cursor"] = start_cursor

        result = api_request(
            "POST",
            f"/data_sources/{DATA_SOURCE_ID}/query",
            body=body,
            notion_version="2025-09-03",
        )

        pages.extend(
            result.get("results", [])
        )

        if not result.get("has_more"):
            break

        start_cursor = result.get("next_cursor")

    return pages


def retrieve_markdown(page_id):
    result = api_request(
        "GET",
        f"/pages/{page_id}/markdown",
        notion_version="2026-03-11",
    )

    if result.get("truncated"):
        print(
            f"WARNING: page {page_id} "
            f"markdown was truncated."
        )

    return result.get(
        "markdown",
        ""
    )


def get_page_title(page):
    properties = page.get(
        "properties",
        {}
    )

    for prop in properties.values():
        if prop.get("type") == "title":

            title_items = prop.get(
                "title",
                []
            )

            return "".join(
                item.get(
                    "plain_text",
                    ""
                )
                for item in title_items
            ).strip()

    return "untitled"


def get_created_date(page):
    """생성일 속성을 우선 사용하고, 비어 있으면 페이지 생성 시각을 사용합니다."""
    prop = page.get("properties", {}).get(CREATED_DATE_PROPERTY)
    value = None
    source_timezone = SYNC_TIMEZONE

    if prop:
        prop_type = prop.get("type")
        if prop_type == "date":
            date_value = prop.get("date") or {}
            value = date_value.get("start")
            if date_value.get("time_zone"):
                source_timezone = ZoneInfo(date_value["time_zone"])
        elif prop_type == "created_time":
            value = prop.get("created_time")
        else:
            raise ValueError(
                f"Page {page['id']}: '{CREATED_DATE_PROPERTY}' must be "
                f"a date or created_time property, got {prop_type!r}."
            )

    if not value:
        value = page.get("created_time")
        source_timezone = SYNC_TIMEZONE
        print(
            f"WARNING: page {page['id']} has no '{CREATED_DATE_PROPERTY}' "
            "value; using page created_time."
        )

    if not value:
        raise ValueError(f"Page {page['id']}: creation date is missing.")

    try:
        # 날짜만 입력된 값은 시간대 변환 없이 그대로 사용합니다.
        if len(value) == 10:
            return date.fromisoformat(value)
        timestamp = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if timestamp.tzinfo is None:
            timestamp = timestamp.replace(tzinfo=source_timezone)
        return timestamp.astimezone(SYNC_TIMEZONE).date()
    except ValueError as exc:
        raise ValueError(
            f"Page {page['id']}: invalid creation date {value!r}."
        ) from exc


def get_week_bounds(created_date):
    """생성일이 속한 주의 월요일과 일요일을 반환합니다."""
    monday = created_date - timedelta(days=created_date.weekday())
    return monday, monday + timedelta(days=6)


def safe_name(value):
    """
    파일명이나 폴더명으로 사용할 수 있도록
    위험한 문자를 제거합니다.
    """

    value = value.strip()

    value = re.sub(
        r'[\\/:*?"<>|]',
        "-",
        value,
    )

    value = re.sub(
        r"\s+",
        " ",
        value,
    )

    value = value.strip(" .")

    if not value:
        return "untitled"

    return value[:100]


def safe_filename(title):
    return safe_name(title)


def yaml_escape(value):
    value = str(value)

    value = value.replace(
        "\\",
        "\\\\"
    )

    value = value.replace(
        '"',
        '\\"'
    )

    return f'"{value}"'


def save_page(page, created_date=None):
    page_id = page["id"]

    title = get_page_title(
        page
    )

    if created_date is None:
        created_date = get_created_date(page)
    week_start, week_end = get_week_bounds(created_date)
    week_name = f"{week_start.isoformat()}_{week_end.isoformat()}"

    markdown = retrieve_markdown(
        page_id
    )

    filename = (
        f"{safe_filename(title)}"
        f"--{page_id.replace('-', '')[:8]}.md"
    )

    # 월요일부터 일요일까지 같은 주의 글을 한 폴더에 저장합니다.
    week_dir = OUTPUT_DIR / week_name

    week_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    file_path = (
        week_dir
        / filename
    )

    frontmatter = "\n".join(
        [
            "---",
            f"title: {yaml_escape(title)}",
            f"created_date: {yaml_escape(created_date.isoformat())}",
            f"week_start: {yaml_escape(week_start.isoformat())}",
            f"week_end: {yaml_escape(week_end.isoformat())}",
            f"notion_page_id: {yaml_escape(page_id)}",
            f"last_edited_time: "
            f"{yaml_escape(page.get('last_edited_time', ''))}",
            f"notion_url: "
            f"{yaml_escape(page.get('url', ''))}",
            "---",
            "",
        ]
    )

    content = frontmatter

    if title:
        content += (
            f"# {title}\n\n"
        )

    content += markdown.rstrip()
    content += "\n"

    file_path.write_text(
        content,
        encoding="utf-8",
    )

    print(
        f"Saved: "
        f"[{week_name}] "
        f"{file_path}"
    )


def main():
    print(
        "Querying Notion database..."
    )

    pages = query_all_pages()

    print(
        f"Found {len(pages)} pages."
    )

    # 날짜 오류가 있으면 기존 내보내기 파일을 지우기 전에 중단합니다.
    dated_pages = [(page, get_created_date(page)) for page in pages]

    # 전체를 다시 생성하여 기존 분류 폴더와 날짜가 변경된 글도 정리합니다.
    if OUTPUT_DIR.exists():
        shutil.rmtree(
            OUTPUT_DIR
        )

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    for page, created_date in dated_pages:
        save_page(page, created_date)

    print()
    print(
        f"Done. "
        f"Exported {len(pages)} pages."
    )


if __name__ == "__main__":
    main()
