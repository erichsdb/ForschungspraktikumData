import ckanapi
import json
import time

def ckan_exporter():
    """
    This doesn't work, because it's not properly maintained and I don't want
    to use open forks and workarounds for a simple task.
    --> Issue: https://github.com/ckan/ckanapi-exporter/issues/7
    --> Depency issue: https://github.com/ckan/losser/pull/14
    """
    import ckanapi_exporter.exporter as exporter
    csv_string = exporter.export('https://www.govdata.de/ckan', 'columns.json')
    print(csv_string)


def write_example_output():
    agent = ckanapi.RemoteCKAN('https://www.govdata.de/ckan')
    results = agent.action.package_search(rows=1000)

    if 'results' not in results:
        print("No results found")
        return

    with open('example.json', 'w', encoding='utf-8') as f:
        json.dump(results['results'], f, ensure_ascii=False, indent=4)

    print("Example output written to example.json")


def get_all_packages():
    agent = ckanapi.RemoteCKAN('https://www.govdata.de/ckan')
    results = agent.action.package_search(rows=1000)

    if 'results' not in results:
        print("No results found")
        return

    count = results['count']
    print(f"Found {count} packages")

    # safe the first 1000 results
    full_data = results['results']

    # get the rest of the data
    number_requests = count // 1000
    for i in range(2, number_requests + 1):
        results = agent.action.package_search(rows=1000, start=i * 1000)
        full_data += results['results']
        print(f"Request {i} done. Length of data: {len(full_data)}")
        time.sleep(1)

    with open('all_packages.json', 'w', encoding='utf-8') as f:
        json.dump(full_data, f, ensure_ascii=False, indent=4)

    print("Example output written to all_packages.json")


def read_example_output():
    with open('example.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def read_full_data():
    with open('all_packages.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f"Loaded {len(data)} packages")
    return data


def do_stuff():
    data = read_full_data()

    tags = set()
    resource_tags = set()
    descriptions = {}
    urls = set()

    # parse the data
    for package in data:
        for tag in package:
            tags.add(tag)
        for resource in package['resources']:
            for tag in resource:
                resource_tags.add(tag)

                if tag == 'url':
                    urls.add(resource['url'])

            if 'description' in resource and resource['description'] is not None:
                if package['title'] not in descriptions:
                    descriptions[package['title']] = []
                descriptions[package['title']].append(resource['description'])
    print(tags)
    # github_links = [url for url in urls if 'github' in url]
    # print(github_links)

    # get base urls
    base_urls = set()
    for url in urls:
        base_url = url.split('/')
        if len(base_url) > 2:
            base_urls.add(base_url[2])

    print(base_urls)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Do this first, if no example is available
    # write_example_output()
    do_stuff()
    # get_all_packages()

    # PATH FROM LOCAL TO EU DATA PORTAL
    # HEIDELBERG: https://ckan.datenplattform.heidelberg.de/en/api/3/action/package_search
    # BADEN-WÜRTTEMBERG: https://www.daten-bw.de/ckan/api/3/action/package_search
    # DEUTSCHLAND: https://www.govdata.de/ckan/api/3/action/package_search?rows=1000&start=1000
    # EU: https://data.europa.eu/api/hub/search/ckan/package_search


