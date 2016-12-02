from bs4 import BeautifulSoup


def extract_blocks(page):
    soup = BeautifulSoup(page)
    table_rows = soup.find_all('tr')
    blocks = []
    for i, row in enumerate(table_rows[4:-2]):
        table_cells = row.find_all('td')
        if table_cells:
            component_and_section = table_cells[1].get_text().rstrip()
            if 'LEC' in component_and_section or 'LAB' in component_and_section:
                component, section = component_and_section.split(' ')
                block = {'component': component,
                         'section': section,
                         'enroll_cap': int(table_cells[6].get_text().rstrip()),
                         'enroll_total': int(table_cells[7].get_text().rstrip()),
                         'time': table_cells[10].get_text().rstrip(),
                         'room': table_cells[11].get_text().rstrip(),
                         'prof': table_cells[12].get_text().rstrip() if len(table_cells) > 12 else ''}
                blocks.append(block)
    return blocks

