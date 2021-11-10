import googleapiclient

from google.google_api_client import create_gsheet_client


class GsheetOutputHandler:
    def __init__(self, sheet_name):
        # The ID and range of a sample spreadsheet.
        self.SPREADSHEET_ID = '1ZopiZ6TThoDvAvlmE01_cfO_u5BsB0vkXebgPWx-Sr0'
        self.sheet_id = "1993041101"
        self.sheet_name = sheet_name
        self.range_name = self.sheet_name + "!A1"
        self.gsheet_client = create_gsheet_client()
        self.row = 1

    def __merge_cells(self, requests):
        # Change the spreadsheet's title.
        requests.append({
            "mergeCells": {
                "range": {
                    "sheetId": self.sheet_id,
                    "startRowIndex": 0,
                    "endRowIndex": 1,
                    "startColumnIndex": 0,
                    "endColumnIndex": 4
                },
                "mergeType": "MERGE_ALL"
            }
        })

    def __update_text_styles(self, requests):
        # Update the text & cell style
        requests.append({
            "repeatCell": {
                "range": {
                    "sheetId": self.sheet_id,
                    "startRowIndex": 0,
                    "endRowIndex": 1,
                    "startColumnIndex": 0,
                    "endColumnIndex": 7
                },
                "cell": {
                    "userEnteredFormat": {
                        "backgroundColor": {
                            "red": 0.79,
                            "green": 0.85,
                            "blue": 0.97
                        },
                        "textFormat": {
                            "bold": True
                        }
                    }
                },
                "fields": "userEnteredFormat(backgroundColor,textFormat)"
            }
        })

    def __add_conditional_format_rules(self, requests):
        requests.extend([{
            "addConditionalFormatRule": {
                "rule": {
                    "ranges": [
                        {
                            "sheetId": self.sheet_id,
                            "startRowIndex": 0,
                            "endRowIndex": 100,
                            "startColumnIndex": 6,
                            "endColumnIndex": 7
                        }
                    ],
                    "booleanRule": {
                        "condition": {
                            "type": "NUMBER_GREATER",
                            "values": [
                                {
                                    "userEnteredValue": "12"
                                }
                            ]
                        },
                        "format": {
                            "backgroundColor": {
                                "red": 0.96,
                                "green": 0.80,
                                "blue": 0.80,
                            }
                        }
                    }
                },
                "index": 0
            }
        },
            {
                "addConditionalFormatRule": {
                    "rule": {
                        "ranges": [
                            {
                                "sheetId": self.sheet_id,
                                "startRowIndex": 0,
                                "endRowIndex": 100,
                                "startColumnIndex": 6,
                                "endColumnIndex": 7
                            }
                        ],
                        "booleanRule": {
                            "condition": {
                                "type": "NUMBER_GREATER",
                                "values": [
                                    {
                                        "userEnteredValue": "6"
                                    }
                                ]
                            },
                            "format": {
                                "backgroundColor": {
                                    "red": 0.99,
                                    "green": 0.90,
                                    "blue": 0.80,
                                }
                            }
                        }
                    },
                    "index": 1
                }
            },
            {
                "addConditionalFormatRule": {
                    "rule": {
                        "ranges": [
                            {
                                "sheetId": self.sheet_id,
                                "startRowIndex": 0,
                                "endRowIndex": 100,
                                "startColumnIndex": 6,
                                "endColumnIndex": 7
                            }
                        ],
                        "booleanRule": {
                            "condition": {
                                "type": "NUMBER_LESS_THAN_EQ",
                                "values": [
                                    {
                                        "userEnteredValue": "6"
                                    }
                                ]
                            },
                            "format": {
                                "backgroundColor": {
                                    "red": 0.72,
                                    "green": 0.88,
                                    "blue": 0.80,
                                }
                            }
                        }
                    },
                    "index": 2
                }
            }])

    def __delete_conditional_format_rule(self, requests):
        requests.append([
            {
                "deleteConditionalFormatRule": {
                    "sheetId": self.sheet_id,
                    "index": 0
                }
            },
            {
                "deleteConditionalFormatRule": {
                    "sheetId": self.sheet_id,
                    "index": 0
                }
            },
            {
                "deleteConditionalFormatRule": {
                    "sheetId": self.sheet_id,
                    "index": 0
                }
            }
        ])

    def print_header(self):
        requests = []

        self.__merge_cells(requests)
        self.__update_text_styles(requests)
        self.__add_conditional_format_rules(requests)

        body = {
            'requests': requests
        }

        self.gsheet_client.batchUpdate(spreadsheetId=self.SPREADSHEET_ID, body=body).execute()

        self.__print(self.sheet_name + "!A1", ["Title"])
        self.__print(self.sheet_name + "!F1", ["Last Update"])
        self.__print(self.sheet_name + "!G1", ["Outdated(month)"])

        self.__move_to_next_row()

    def clear_formating(self):
        # clear formating
        requests = []

        self.__delete_conditional_format_rule(requests)

        body = {
            'requests': requests
        }

        try:
            result = self.gsheet_client.batchUpdate(spreadsheetId=self.SPREADSHEET_ID, body=body).execute()
        except googleapiclient.errors.HttpError as e:
            if e.status_code == 400:
                print(e.error_details)

    def clear(self):
        result = self.gsheet_client.values().clear(spreadsheetId=self.SPREADSHEET_ID, range=self.sheet_name).execute()
        print('{0} cleared.'.format(result.get('clearedRange')))

    def __print(self, range, row_data):
        values = [
            row_data
        ]

        body = {
            'values': values
        }

        result = self.gsheet_client.values().update(
            spreadsheetId=self.SPREADSHEET_ID, range=range, valueInputOption="USER_ENTERED",
            body=body).execute()
        # print('{0} cells updated.'.format(result.get('updatedCells')))

    def print(self, row_data):
        row_data.append('=DATEDIF(F%d, NOW(), "M")' % self.row)

        values = [
            row_data
        ]

        body = {
            'values': values
        }

        result = self.gsheet_client.values().update(
            spreadsheetId=self.SPREADSHEET_ID, range=self.range_name, valueInputOption="USER_ENTERED",
            body=body).execute()
        # print('{0} cells updated.'.format(result.get('updatedCells')))

        self.__move_to_next_row()

    def __move_to_next_row(self):
        self.row += 1
        self.range_name = self.sheet_name + "!A" + str(self.row)
