from atlassian import Confluence
import csv
import datetime
import json

credential = None

with open('credential.json') as json_file:
    credential = json.load(json_file)

confluence = Confluence(
    url=credential["url"],
    username=credential["username"],
    password=credential["password"]
)


def print_children(csv_writer, root_page_id, level):
    pages = confluence.get_page_child_by_type(root_page_id, type='page', start=None, limit=None)

    for page in pages:
        page_id = page["id"]
        page_title = page["title"]

        history = confluence.get_content_history(page_id)
        last_updated = history["lastUpdated"]["when"]
        last_updated = last_updated[:-1]
        last_updated = datetime.datetime.fromisoformat(last_updated)
        last_updated = last_updated.strftime("%m/%d/%Y")
        link = credential["url"] + "/wiki" + page["_links"]["webui"]

        print("  " * level + page_title + ", " + last_updated)
        row = [""] * level
        row.append('=HYPERLINK("%s", "%s")' % (link, page_title))
        row += [""] * (5 - len(row))
        row.append(last_updated)

        csv_writer.writerow(row)
        print_children(csv_writer, page_id, level + 1)


if __name__ == '__main__':
    ROOT_PAGE_ID = "1577058409"

    with open('pages.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        print_children(csv_writer, ROOT_PAGE_ID, 0)

    print("Finished!")
