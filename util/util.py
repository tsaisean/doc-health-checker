def generate_cvs_row(indents, page_title, link, last_updated, author):
    last_updated = last_updated.strftime("%m/%d/%Y")
    page_title_double_quoted = page_title.replace('"', '""')
    row = [""] * indents
    row.append('=HYPERLINK("%s", "%s")' % (link, page_title_double_quoted))
    row += [""] * (5 - len(row))
    row.append(last_updated)
    row.append(author)
    return row
