import json
import os
import sys
import requests
import urllib.parse
import time
import pandas as pd
from datetime import datetime
#Built by Omi Brown: omiete98@yahoo.com
#API Key and i is used to change betwen desktop and mobile
api_key = "INSERT API KEY"
i = 0


#this while loop helps run the desktop runs immdediately after getting the mobile runs
while i < 2:
#naming of the files and creation of a data frame, it takes what the name is and the current date
    if i == 0:
        df_mobile= pd.DataFrame([], columns=['URL','Mobile Performance','Accessibility','Best Practices', 'SEO','Server Response Time (ms)', 'Redirects (ms)', 'Offscreen Images (ms)','Unused Javascript (ms)','Uses Optimized Images (ms)'])
        name = "INSERT MOBILE FILE NAME" 
        getdate = datetime.now().strftime("%m-%d-%y-%H-%M")
    else:
        df_desktop= pd.DataFrame([], columns=['URL','Desktop Performance','Accessibility','Best Practices','SEO','Server Response Time (ms)', 'Redirects (ms)', 'Offscreen Images (ms)','Unused Javascript (ms)','Uses Optimized Images (ms)'])
        name = "INSERT DESKTOP FILE NAME"
        getdate = datetime.now().strftime("%m-%d-%y-%H-%M")

#Opening and reading the URLs from a .txt file
    with open('INSER FILE PATH/urls.txt') as pagespeedurls:
        content = pagespeedurls.readlines()
        content = [line.rstrip('\n') for line in content]
#For every URL in the .txt file we will run this bit of code
    for line in content:
        #Stripping the url of it's www. components and accounts for if the url doesn't have www. within it
        if "www." in line:
            filename = line.replace('https://www.','').split(".com")
        else:
            filename = line.replace('https://','').split(".com")
        #If i is 0 then we are running for Mobile
        if i == 0:
            try:
                print("Running Mobile for " + line)
                api_url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
                params = {"url": line, "key": api_key,'strategy':'mobile','category':['performance','seo','best-practices','accessibility']}
                req = requests.get(api_url, params=params)
                #We are running a request from the pagespeed api, the code 200 means it's successful so we continue
                if (req.status_code == 200):
                    json_data = json.loads(req.text)
                    json_filenamemobile = 'INSERT FILE PATH FOR MOBILE JSONs' + name + filename[0] + '_' + getdate + '.report.json'
                    #Build a JSON file for URL and channel
                    with open(json_filenamemobile, "w") as outfile:
                        json.dump(json_data, outfile)
                    print("Mobile Report complete for: " + line)
                    with open(json_filenamemobile) as json_data_mobile:
                        loaded_json_mobile = json.load(json_data_mobile)
                    performance = str(round(loaded_json_mobile["lighthouseResult"]["categories"]["performance"]["score"] * 100))
                    accessibility = str(round(loaded_json_mobile["lighthouseResult"]["categories"]["accessibility"]["score"] * 100))
                    best_practices = str(round(loaded_json_mobile["lighthouseResult"]["categories"]["best-practices"]["score"] * 100))
                    seo = str(round(loaded_json_mobile["lighthouseResult"]["categories"]["seo"]["score"] * 100))
                    server_response = str(loaded_json_mobile["lighthouseResult"]["audits"]["server-response-time"]["numericValue"])
                    redirects = str(loaded_json_mobile["lighthouseResult"]["audits"]["redirects"]["numericValue"])
                    offscreen_images = str(loaded_json_mobile["lighthouseResult"]["audits"]["offscreen-images"]["numericValue"])
                    unused_javascript = str(loaded_json_mobile["lighthouseResult"]["audits"]["unused-javascript"]["numericValue"])
                    use_optimized_images = str(loaded_json_mobile["lighthouseResult"]["audits"]["uses-optimized-images"]["numericValue"])
                    dict_mobile = {"URL":line,"Mobile Performance":performance, "Accessibility":accessibility, "Best Practices":best_practices,"SEO":seo, "Server Response Time (ms)":server_response, "Redirects (ms)":redirects, "Offscreen Images (ms)":offscreen_images,"Unused Javascript (ms)":unused_javascript,"Uses Optimized Images (ms)":use_optimized_images}
                    df_mobile = df_mobile._append(dict_mobile, ignore_index=True)
                    print("Data added to Mobile DataFrame")
                #In the event the PageSpeed Insight API doesn't return a succesful status code, we will show the url and error code and fill data frame with null for values
                else:
                    print("PageSpeed Insights failed to successfully run the mobile webpage URL: " + line + "\nError Code: " + str(req.status_code))
                    performance = "null"
                    accessibility = "null"
                    best_practices = "null"
                    seo = "null"
                    server_response = "null"
                    redirects = "null"
                    offscreen_images = "null"
                    unused_javascript = "null"
                    use_optimized_images = "null" 
                    dict_mobile = {"URL":line,"Mobile Performance":performance, "Accessibility":accessibility, "Best Practices":best_practices,"SEO":seo, "Server Response Time (ms)":server_response, "Redirects (ms)":redirects, "Offscreen Images (ms)":offscreen_images,"Unused Javascript (ms)":unused_javascript,"Uses Optimized Images (ms)":use_optimized_images}
                    df_mobile = df_mobile._append(dict_mobile, ignore_index=True)
            #In the event of a Runtime or Type Error we want the script to continue running but place a null for all values and the url attempted
            except RuntimeError or TypeError or KeyError:
                performance = "null"
                accessibility = "null"
                best_practices = "null"
                seo = "null"
                server_response = "null"
                redirects = "null"
                offscreen_images = "null"
                unused_javascript = "null"
                use_optimized_images = "null"
                dict_mobile = {"URL":line,"Mobile Performance":performance, "Accessibility":accessibility, "Best Practices":best_practices,"SEO":seo, "Server Response Time (ms)":server_response, "Redirects (ms)":redirects, "Offscreen Images (ms)":offscreen_images,"Unused Javascript (ms)":unused_javascript,"Uses Optimized Images (ms)":use_optimized_images}
                df_mobile = df_mobile._append(dict_mobile, ignore_index=True)
                continue            
        else:
            #This is the exact same code for except we are now running for desktop
            try:
                print("Running Desktop for " + line)
                api_url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
                params = {"url": line, "key": api_key, "strategy": "desktop","category":["performance","accessibility","best_practices","seo"]}
                req = requests.get(api_url, params=params)
                if (req.status_code == 200):
                    json_data = json.loads(req.text)
                    json_filenamedesktop = 'INSERT FILE PATH FOR DESKTOP JSONS' + name + filename[0] + '_' + getdate + '.report.json'
                    with open(json_filenamedesktop, "w") as outfile:
                        json.dump(json_data, outfile)
                    print("Desktop Report complete for: " + line)
                    with open(json_filenamedesktop) as json_data_desktop:
                        loaded_json_desktop = json.load(json_data_desktop)
                    performance = str(round(loaded_json_desktop["lighthouseResult"]["categories"]["performance"]["score"] * 100))
                    accessibility = str(round(loaded_json_desktop["lighthouseResult"]["categories"]["accessibility"]["score"] * 100))
                    best_practices = str(round(loaded_json_desktop["lighthouseResult"]["categories"]["best-practices"]["score"] * 100))
                    seo = str(round(loaded_json_desktop["lighthouseResult"]["categories"]["seo"]["score"] * 100))
                    server_response = str(loaded_json_desktop["lighthouseResult"]["audits"]["server-response-time"]["numericValue"])
                    redirects = str(loaded_json_desktop["lighthouseResult"]["audits"]["redirects"]["numericValue"])
                    offscreen_images = str(loaded_json_desktop["lighthouseResult"]["audits"]["offscreen-images"]["numericValue"])
                    unused_javascript = str(loaded_json_desktop["lighthouseResult"]["audits"]["unused-javascript"]["numericValue"])
                    use_optimized_images = str(loaded_json_desktop["lighthouseResult"]["audits"]["uses-optimized-images"]["numericValue"])
                    dict_desktop = {"URL":line,"Desktop Performance":performance, "Accessibility":accessibility, "Best Practices":best_practices,"SEO":seo, "Server Response Time (ms)":server_response, "Redirects (ms)":redirects, "Offscreen Images (ms)":offscreen_images,"Unused Javascript (ms)":unused_javascript,"Uses Optimized Images (ms)":use_optimized_images}
                    df_desktop = df_desktop._append(dict_desktop, ignore_index=True)
                    print("Data added to CSV")
                else:
                    print("PageSpeed Insights failed to successfully run the desktop webpage URL: " + line + "\nError Code: " + str(req.status_code))
                    performance = "null"
                    accessibility = "null"
                    best_practices = "null"
                    seo = "null"
                    server_response = "null"
                    redirects = "null"
                    offscreen_images = "null"
                    unused_javascript = "null"
                    use_optimized_images = "null"
                    dict_desktop = {"URL":line,"Desktop Performance":performance, "Accessibility":accessibility, "Best Practices":best_practices,"SEO":seo, "Server Response Time (ms)":server_response, "Redirects (ms)":redirects, "Offscreen Images (ms)":offscreen_images,"Unused Javascript (ms)":unused_javascript,"Uses Optimized Images (ms)":use_optimized_images}
                    df_desktop = df_desktop._append(dict_desktop, ignore_index=True)           
            except RuntimeError or TypeError or KeyError:
                performance = "null"
                accessibility = "null"
                best_practices = "null"
                seo = "null"
                server_response = "null"
                redirects = "null"
                offscreen_images = "null"
                unused_javascript = "null"
                use_optimized_images = "null"
                dict_desktop = {"URL":line,"Desktop Performance":performance, "Accessibility":accessibility, "Best Practices":best_practices,"SEO":seo, "Server Response Time (ms)":server_response, "Redirects (ms)":redirects, "Offscreen Images (ms)":offscreen_images,"Unused Javascript (ms)":unused_javascript,"Uses Optimized Images (ms)":use_optimized_images}
                df_desktop = df_desktop._append(dict_desktop, ignore_index=True)   
                continue 
    #Saves the data frame with all runs as a CSV for later viewing           
    if i == 0:
        df_mobile.to_csv('INSERT FILE PATH FOR MOBILE CSVs' + name + '_' + getdate + '.csv')
        print("All mobile data saved to a .CSV")
    else:
        df_desktop.to_csv('INSERT FILE PATH FOR DESKTOP CSVs' + name + '_' + getdate + '.csv')
        print("All desktop data saved to a .CSV")
    i+=1
print("All done, for all URLs")