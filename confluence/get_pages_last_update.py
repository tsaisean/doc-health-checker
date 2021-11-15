import os
import sys

from slack_helper.slack_helper import SlackHelper
from slack_output_handler import SlackOutputHandler

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from csv_output_handler import CsvOutputHandler
from gsheet_output_handler import GsheetOutputHandler
from output_handler_interface import OutputHandlerInterface

from atlassian import Confluence
import datetime
import json
from enum import Enum

config = None
config_confluence = None
config_slack = None

class OutputMode(Enum):
    CSV = 1
    GOOGLESHEET = 2
    SLACK = 3


with open('confluence/config.json') as json_file:
    config = json.load(json_file)
    config_confluence = config["confluence"]
    config_slack = config["slack"]

confluence = Confluence(
    url=config_confluence["url"],
    username=config_confluence["username"],
    password=config_confluence["password"]
)


def print_children(root_page_id, output_handler, level):
    pages = confluence.get_page_child_by_type(root_page_id, type='page', start=None, limit=None)

    for page in pages:
        page_id = page["id"]
        page_title = page["title"]

        history = confluence.get_content_history(page_id)
        last_updated = history["lastUpdated"]["when"]
        last_updated = last_updated[:-1]
        last_updated = datetime.datetime.fromisoformat(last_updated)
        link = config_confluence["url"] + "/wiki" + page["_links"]["webui"]

        print("  " * level + page_title + ", " + last_updated.__str__())

        if issubclass(output_handler, OutputHandlerInterface):
            output_handler.add(level, page_title, link, last_updated)
        else:
            raise Exception("output_handler is not subclass of OutputHandler.")

        print_children(page_id, output_handler, level + 1)


if __name__ == '__main__':
    ROOT_PAGE_ID = config_confluence["confluence_page_id"]
    mode = OutputMode.SLACK

    output_handler = None
    if mode == OutputMode.CSV:
        output_handler = CsvOutputHandler()
        print_children(ROOT_PAGE_ID, output_handler, 0)
    elif mode == OutputMode.GOOGLESHEET:
        output_handler = GsheetOutputHandler("Search")
        output_handler.clear()
        output_handler.clear_formating()
        output_handler.print_header()
        print_children(ROOT_PAGE_ID, output_handler, 0)
    elif mode == OutputMode.SLACK:
        slack_helper = SlackHelper(config_slack["bot_oauth_token"], config_slack["slack_channel_id"])
        output_handler = SlackOutputHandler(slack_helper, config["alert_rules"])
        print_children(ROOT_PAGE_ID, output_handler, 0)
        output_handler.flush()

    print("Finished!")
