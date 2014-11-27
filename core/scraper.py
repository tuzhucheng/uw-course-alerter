from bs4 import BeautifulSoup


def extract_sections(page):
    soup = BeautifulSoup(page)
    table_rows = soup.find_all('tr')
    sections = []
    for row in table_rows[4:-2]:
        table_cells = row.find_all('td')
        if 'LEC' in table_cells[1].get_text():
            section = {'section': table_cells[1].get_text(),
                       'enroll_cap': table_cells[6].get_text(),
                       'enroll_total': table_cells[7].get_text(),
                       'time': table_cells[10].get_text(),
                       'room': table_cells[11].get_text(),
                       'prof': table_cells[12].get_text()}
            sections.append(section)
    return sections

