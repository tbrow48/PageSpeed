import requests

# Documentation: https://developers.google.com/speed/docs/insights/v5/get-started

# JSON paths: https://developers.google.com/speed/docs/insights/v4/reference/pagespeedapi/runpagespeed

# Populate 'pagespeed.txt' file with URLs to query against API.


with open('pagespeed.txt') as pagespeedurls:
    download_dir = 'pagespeed-results.csv'
    file = open(download_dir, 'w')
    content = pagespeedurls.readlines()
    content = [line.rstrip('\n') for line in content]

    columnTitleRow = "URL, Desktop Page Speed Index Score\n"
    file.write(columnTitleRow)

    # This is the google pagespeed api url structure, using for loop to insert each url in .txt file
    for line in content:
        # If no "strategy" parameter is included, the query by default returns desktop data.
        x = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={line}&key=AIzaSyCzd4hGQ3B0uKtZVpoebtN0Kqf14CkTrMo" 
        print(f'Requesting {x}...')
        r = requests.get(x)
        final = r.json()
        
        try:
            urlid = final['id']
            split = urlid.split('?') # This splits the absolute url from the api key parameter
            urlid = split[0] # This reassigns urlid to the absolute url
            ID = f'URL ~ {urlid}'
            ID2 = str(urlid)
            urlfcp = final['lighthouseResult']['categories']['performance']['score']*100
            FCP = f'Page Speed Index ~ {str(urlfcp)}'
            FCP2 = str(urlfcp)
        except KeyError:
            print(f'<KeyError> One or more keys not found {line}.')
        
        try:
            row = f'{ID2},{FCP2}\n'
            file.write(row)
        except NameError:
            print(f'<NameError> Failing because of KeyError {line}.')
            file.write(f'<KeyError> & <NameError> Failing because of nonexistant Key ~ {line}.' + '\n')
    print("Desktop Done")
    file.close()

with open('pagespeed.txt') as pagespeedurls:
    download_dir = 'pagespeed-mobile-results.csv'
    file = open(download_dir, 'w')
    content = pagespeedurls.readlines()
    content = [line.rstrip('\n') for line in content]

    columnTitleRow = "URL, Mobile Page Speed Index Score\n"
    file.write(columnTitleRow)

    # This is the google pagespeed api url structure, using for loop to insert each url in .txt file
    for line in content:
        # If no "strategy" parameter is included, the query by default returns desktop data.
        x = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={line}&strategy=mobile&key=AIzaSyCzd4hGQ3B0uKtZVpoebtN0Kqf14CkTrMo" 
        print(f'Requesting {x}...')
        r = requests.get(x)
        final = r.json()
        
        try:
            urlid = final['id']
            split = urlid.split('?') # This splits the absolute url from the api key parameter
            urlid = split[0] # This reassigns urlid to the absolute url
            ID = f'URL ~ {urlid}'
            ID2 = str(urlid)
            urlfcp = final['lighthouseResult']['categories']['performance']['score']*100
            FCP = f'Page Speed Index ~ {str(urlfcp)}'
            FCP2 = str(urlfcp)
        except KeyError:
            print(f'<KeyError> One or more keys not found {line}.')
        
        try:
            row = f'{ID2},{FCP2}\n'
            file.write(row)
        except NameError:
            print(f'<NameError> Failing because of KeyError {line}.')
            file.write(f'<KeyError> & <NameError> Failing because of nonexistant Key ~ {line}.' + '\n')

    print("Mobile Done")
    file.close()
