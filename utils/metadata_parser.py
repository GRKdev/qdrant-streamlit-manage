from datetime import datetime
import time


def parse_source_documents(input_text):
    lines = [line.strip() for line in input_text.split("\n") if line.strip()]
    source_docs = []
    for i in range(0, len(lines), 4):
        if i + 3 < len(lines):
            source_docs.append(
                {
                    "file_name": lines[i],
                    "url": lines[i + 1],
                    "year": lines[i + 2],
                    "month": lines[i + 3],
                }
            )
    return source_docs


def parse_news_document(input_text):
    lines = [line.strip() for line in input_text.split("\n") if line.strip()]
    if len(lines) >= 2:
        return {"news_title": lines[0], "news_url": lines[1]}
    return None


def parse_custom_metadata(input_text):
    lines = [line.strip() for line in input_text.split("\n") if line.strip()]
    custom_metadata = {}
    for line in lines:
        if ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            if key == "date":
                timestamp = date_to_timestamp(value)
                if timestamp is not None:
                    custom_metadata[key] = timestamp
            elif key in custom_metadata:
                if isinstance(custom_metadata[key], list):
                    custom_metadata[key].append(value)
                else:
                    custom_metadata[key] = [custom_metadata[key], value]
            else:
                custom_metadata[key] = value
    return custom_metadata


def date_to_timestamp(date_str):
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return int(time.mktime(date_obj.timetuple()))
    except ValueError:
        return None
