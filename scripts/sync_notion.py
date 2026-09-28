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
OUTPUT_DIR = Path(os.environ.get("NOTION_OUTPUT_DIR", "notion-posts"))

API_BASE = "https://api.notion.com/v1"


def api_request(method, path, body=None, notion_version="2025-09-03"):
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
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        raise RuntimeError(
            f"Notion API error: HTTP {e.code}\n{error_body}"
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

        pages.extend(result.get("results", []))

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
            f"WARNING: page {page_id} markdown was truncated."
        )

    return result.get("markdown", "")


def get_page_title(page):
    properties = page.get("properties", {})

    for prop in properties.values():
        if prop.get("type") == "title":
            title_items = prop.get("title", [])

            return "".join(
                item.get("plain_text", "")
                for item in title_items
            ).strip()

    return "untitled"


def safe_filename(title):
    title = title.strip()

    title = re.sub(
        r'[\\/:*?"<>|]',
        "-",
        title,
    )

    title = re.sub(r"\s+", " ", title)

    title = title.strip(" .")

    if not title:
        return "untitled"

    return title[:100]


def yaml_escape(value):
    value = str(value)
    value = value.replace("\\", "\\\\")
    value = value.replace('"', '\\"')
    return f'"{value}"'


def save_page(page):
    page_id = page["id"]
    title = get_page_title(page)

    markdown = retrieve_markdown(page_id)

    filename = (
        f"{safe_filename(title)}"
        f"--{page_id.replace('-', '')[:8]}.md"
    )

    file_path = OUTPUT_DIR / filename

    frontmatter = "\n".join(
        [
            "---",
            f"title: {yaml_escape(title)}",
            f"notion_page_id: {yaml_escape(page_id)}",
            f"last_edited_time: {yaml_escape(page.get('last_edited_time', ''))}",
            f"notion_url: {yaml_escape(page.get('url', ''))}",
            "---",
            "",
        ]
    )

    content = frontmatter

    if title:
        content += f"# {title}\n\n"

    content += markdown.rstrip()
    content += "\n"

    file_path.write_text(
        content,
        encoding="utf-8",
    )

    print(f"Saved: {file_path}")


def main():
    print("Querying Notion database...")

    pages = query_all_pages()

    print(f"Found {len(pages)} pages.")

    # notion-posts 폴더는 Notion의 현재 상태를 그대로 반영합니다.
    # 따라서 이전에 존재하다가 Notion DB에서 삭제된 페이지도
    # GitHub에서 같이 제거됩니다.
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    for page in pages:
        save_page(page)

    print()
    print(f"Done. Exported {len(pages)} pages.")


if __name__ == "__main__":
    main()