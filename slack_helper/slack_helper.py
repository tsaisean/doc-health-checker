import ssl

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Essential value for `verify_certs`.
# This is used to detect if a user is passing in a value for `verify_certs`
# so we can raise a warning if using SSL kwargs AND SSLContext.
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE


class SlackHelper:
    def __init__(self, token, channel):
        self.client = WebClient(token=token, ssl=ssl_context)
        self.channel = channel

    def send_msg(self, msg):
        try:
            self.client.chat_postMessage(channel=self.channel, text=msg)
        except SlackApiError as e:
            # You will get a SlackApiError if "ok" is False
            assert e.response["ok"] is False
            assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
            print(f"Got an error: {e.response['error']}")
