import urllib
import bs4

prefix = "http://www.elections.ny.gov:8080"


def make_soup(link):
    f = urllib.urlopen(link)
    content = "".join(f.readlines())
    f.close()

    index = content.rfind("<HTML>")
    content = content[index:]
    soup = bs4.BeautifulSoup(content)
    return soup


def number(string):
    return float(string.strip().replace(',', ''))


def get_filer_details(link):
    link = prefix + link
    soup = make_soup(link)

    rows = soup.find_all("tr")[2:-1]
    details = {'contributors': []}
    for row in rows:
        cells = row.find_all("td")
        entry = dict()
        entry['contributor'] = cells[0].text
        entry['amount'] = number(cells[1].text)
        details['contributors'].append(entry)

    total = number(soup.find_all("tr")[-1].find_all("td")[-1].font.b.text)
    details['total'] = total
    return details


def find_details(OFFICE_IN):
    action = "plsql_browser/CONTRIB_PRE_A_COUNTY"

    payload = dict(
        NAME_IN="",
        OFFICE_IN=OFFICE_IN,
        county_IN=28,
        date_from="01/01/1989",
        date_to="09/21/2012",
        CATEGORY_IN="ALL",
        AMOUNT_from=0,
        AMOUNT_to=100000000000000,
        ZIP1="",
        ZIP2="",
        ORDERBY_IN="N",
    )

    query_string = urllib.urlencode(payload)
    url = prefix + "/" + action + "?" + query_string
    soup = make_soup(url)
    table = soup.find_all("table")[0]
    rows = table.find_all("tr")

    all_details = []
    for row in rows[1:]:
        name, committee_type, office, dist, county, municipality, link = \
            row.find_all("td")

        print " * Querying, ", name.font.text, office.text, OFFICE_IN
        details = get_filer_details(link.font.a['href'])
        print "      ", details['total']

        all_details.append(dict(
            name=name.text,
            committee_type=committee_type.text,
            office=office.text,
            dist=dist.text,
            county=county.text,
            municipality=municipality.text,
            link=link.font.a,
            details=details
        ))

    return all_details


def main():

    all_details = []

    for OFFICE_IN in range(256):
        try:
            all_details += find_details(OFFICE_IN)
        except IndexError:
            pass

    all_details.sort(lambda x, y: cmp(x['details']['total'],
                                      y['details']['total']))
    for deets in all_details:
        print deets['name'], deets['details']['total']
if __name__ == '__main__':
    main()
