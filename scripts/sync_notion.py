import json
import os
import re
import shutil
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


NOTION_TOKEN = os.environ["NOTION_TOKEN"]
DATA_SOURCE_ID = os.environ["NOTION_DATA_SOURCE_ID"]

OUTPUT_DIR = Path(
    os.environ.get(
        "NOTION_OUTPUT_DIR",
        "notion-posts"
    )
)

# Notion DB의 세션 속성 이름
SESSION_PROPERTY = os.environ.get(
    "NOTION_SESSION_PROPERTY",
    "세션"
)

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


def get_session_name(page):
    """
    Notion DB의 '세션' Select 속성에서
    선택된 세션 이름을 가져옵니다.

    예:
        세션01
        세션02
        세션03

    세션이 지정되지 않았으면 '미분류' 폴더에 저장합니다.
    """

    properties = page.get(
        "properties",
        {}
    )

    session_prop = properties.get(
        SESSION_PROPERTY
    )

    if not session_prop:
        print(
            f"WARNING: "
            f"'{SESSION_PROPERTY}' "
            f"property not found."
        )

        return "미분류"

    prop_type = session_prop.get(
        "type"
    )

    # Select 속성
    if prop_type == "select":

        select_value = session_prop.get(
            "select"
        )

        if select_value:
            name = select_value.get(
                "name",
                ""
            ).strip()

            if name:
                return name

    # 혹시 Status 속성으로 변경할 경우에도 대응
    if prop_type == "status":

        status_value = session_prop.get(
            "status"
        )

        if status_value:
            name = status_value.get(
                "name",
                ""
            ).strip()

            if name:
                return name

    return "미분류"


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


def save_page(page):
    page_id = page["id"]

    title = get_page_title(
        page
    )

    session_name = get_session_name(
        page
    )

    markdown = retrieve_markdown(
        page_id
    )

    filename = (
        f"{safe_filename(title)}"
        f"--{page_id.replace('-', '')[:8]}.md"
    )

    # ---------------------------------
    # 세션별 폴더 생성
    # ---------------------------------

    session_dir = (
        OUTPUT_DIR
        / safe_name(session_name)
    )

    session_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    file_path = (
        session_dir
        / filename
    )

    frontmatter = "\n".join(
        [
            "---",
            f"title: {yaml_escape(title)}",
            f"session: {yaml_escape(session_name)}",
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
        f"[{session_name}] "
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

    # notion-posts 폴더는
    # Notion DB의 현재 상태를 그대로 반영합니다.
    #
    # 따라서:
    #
    # - 삭제된 글
    # - 세션이 변경된 글
    # - 기존 세션 폴더
    #
    # 모두 한번 지운 뒤 현재 Notion 상태를 기준으로
    # 다시 생성합니다.
    #
    # 예:
    #
    # 세션02 → 세션03
    #
    # 으로 변경하면 예전 세션02 파일은 사라지고
    # 세션03 폴더에 새로 생성됩니다.

    if OUTPUT_DIR.exists():
        shutil.rmtree(
            OUTPUT_DIR
        )

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    for page in pages:
        save_page(page)

    print()
    print(
        f"Done. "
        f"Exported {len(pages)} pages."
    )


if __name__ == "__main__":
    main()