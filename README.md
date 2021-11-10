# doc-health-checker
This is a document health checker tool for the Atlassian Confluence


# How to use
## Option 1
1. Rename the `_credential.json` to `confluence_credential.json` and update the credential accordingly.
2. Excute the the main `get_pages_last_update.py`.
3. By running the script, a `pages.csv` will be generated.
4. Use GoogleSheet to import the `pages.csv`. (See Illustration 1.)

## Option 2
1. Rename the `_credential.json` to `confluence_credential.json` and update the credential accordingly.
2. Add the `google_credential.json` under the `google` package. (See [Authenticating as a service account](https://cloud.google.com/docs/authentication/production#manually))
3. Update the values of the fields.
```
        self.SPREADSHEET_ID = 'xxxxxx'
        self.sheet_id = "123456"
        self.sheet_name = "sheet1"
```
5. Excute the the main `get_pages_last_update.py`.
6. By running the script, the result will output to the spreadsheet you just specified. (See Illustration 1.)


### Illustration 1
![Illustration 1](https://user-images.githubusercontent.com/4138501/141038961-96736866-bfe5-4200-bdf1-d4e4feab522a.png)
