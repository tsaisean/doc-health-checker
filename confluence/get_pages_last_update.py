import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from csv_output_handler import CsvOutputHandler
from gsheet_output_handler import GsheetOutputHandler
from output_handler_interface import OutputHandlerInterface

from atlassian import Confluence
import datetime
import json
from enum import Enum

credential = None


class OutputMode(Enum):
    CSV = 1
    GOOGLESHEET = 2


with open('confluence/confluence_credential.json') as json_file:
    credential = json.load(json_file)

confluence = Confluence(
    url=credential["url"],
    username=credential["username"],
    password=credential["password"]
)


def print_children(root_page_id, output_handler, level):
    pages = confluence.get_page_child_by_type(root_page_id, type='page', start=None, limit=None)

    for page in pages:
        page_id = page["id"]
        page_title = page["title"]
        page_title_double_quoted = page_title.replace('"', '""')

        history = confluence.get_content_history(page_id)
        last_updated = history["lastUpdated"]["when"]
        last_updated = last_updated[:-1]
        last_updated = datetime.datetime.fromisoformat(last_updated)
        last_updated = last_updated.strftime("%m/%d/%Y")
        link = credential["url"] + "/wiki" + page["_links"]["webui"]

        print("  " * level + page_title + ", " + last_updated)
        row = [""] * level
        row.append('=HYPERLINK("%s", "%s")' % (link, page_title_double_quoted))
        row += [""] * (5 - len(row))
        row.append(last_updated)

        if issubclass(output_handler, OutputHandlerInterface):
            output_handler.print(row)
        else:
            raise Exception("output_handler is not subclass of OutputHandler.")

        print_children(page_id, output_handler, level + 1)


if __name__ == '__main__':
    ROOT_PAGE_ID = "1577058409"
    mode = OutputMode.GOOGLESHEET

    output_handler = None
    if mode == OutputMode.CSV:
        output_handler = CsvOutputHandler()
    elif mode == OutputMode.GOOGLESHEET:
        output_handler = GsheetOutputHandler("Search")
        output_handler.clear()
        output_handler.clear_formating()
        output_handler.print_header()

    print_children(ROOT_PAGE_ID, output_handler, 0)

    print("Finished!")
