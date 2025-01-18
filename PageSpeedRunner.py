import json
import requests
import pandas as pd
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox
import threading

# API Key
api_key = "AIzaSyCzd4hGQ3B0uKtZVpoebtN0Kqf14CkTrMo"

# Tkinter Input Handling (Main Thread Only)
def get_user_inputs():
    root = tk.Tk()
    root.withdraw()

    # Prompt for .txt file with URLs
    messagebox.showinfo("Select the .txt", "Please select the .txt file with URLs")
    file_path = filedialog.askopenfilename(filetypes=[("txt files", "*.txt")])
    if not file_path:
        print("No file selected. Exiting program.")
        sys.exit()

    # Prompt for mobile CSV directory
    messagebox.showinfo("Select Mobile CSV Directory", "Please select the directory to save the mobile CSV file")
    mobile_csv_directory = filedialog.askdirectory()
    if not mobile_csv_directory:
        print("No mobile directory selected. Exiting program.")
        sys.exit()

    # Prompt for desktop CSV directory
    messagebox.showinfo("Select Desktop CSV Directory", "Please select the directory to save the desktop CSV file")
    desktop_csv_directory = filedialog.askdirectory()
    if not desktop_csv_directory:
        print("No desktop directory selected. Exiting program.")
        sys.exit()

    return file_path, mobile_csv_directory, desktop_csv_directory

# Worker Function for Mobile Processing
def process_mobile(file_path, mobile_csv_directory):
    df_mobile = pd.DataFrame([], columns=['URL', 'Mobile Performance', 'Accessibility', 'Best Practices', 'SEO','Server Response Time (ms)', 'Redirects (ms)',
                                          'Offscreen Images (ms)', 'Unused Javascript (ms)', 'Uses Optimized Images (ms)'])
    name = "MobilePageSpeed"
    getdate = datetime.now().strftime("%m-%d-%y-%H-%M")

    with open(file_path) as pagespeedurls:
        content = pagespeedurls.readlines()
        content = [line.rstrip('\n') for line in content]

    for line in content:
        try:
            print(f"Running Mobile for {line}")
            api_url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
            params = {
                "url": line,
                "key": api_key,
                "strategy": "mobile",
                "category": ['performance','seo','best-practices','accessibility']
            }
            req = requests.get(api_url, params=params)

            if req.status_code == 200:
                json_data = req.json()

                # Extract relevant metrics
                performance = str(round(json_data["lighthouseResult"]["categories"]["performance"]["score"] * 100))
                accessibility = str(round(json_data["lighthouseResult"]["categories"]["accessibility"]["score"] * 100))
                best_practices = str(round(json_data["lighthouseResult"]["categories"]["best-practices"]["score"] * 100))
                seo = str(round(json_data["lighthouseResult"]["categories"]["seo"]["score"] * 100))
                server_response = str(json_data["lighthouseResult"]["audits"]["server-response-time"]["numericValue"])
                redirects = str(json_data["lighthouseResult"]["audits"]["redirects"]["numericValue"])
                offscreen_images = str(json_data["lighthouseResult"]["audits"]["offscreen-images"]["numericValue"])
                unused_javascript = str(json_data["lighthouseResult"]["audits"]["unused-javascript"]["numericValue"])
                use_optimized_images = str(json_data["lighthouseResult"]["audits"]["uses-optimized-images"]["numericValue"])

                # Add data to the DataFrame
                dict_mobile = {
                    "URL": line,
                    "Mobile Performance": performance,
                    "Accessibility": accessibility,
                    "Best Practices": best_practices,
                    "SEO": seo,
                    "Server Response Time (ms)": server_response,
                    "Redirects (ms)": redirects,
                    "Offscreen Images (ms)": offscreen_images,
                    "Unused Javascript (ms)": unused_javascript,
                    "Uses Optimized Images (ms)": use_optimized_images
                }
                df_mobile = df_mobile._append(dict_mobile, ignore_index=True)
            else:
                print(f"Error {req.status_code} for {line}: {req.reason}")

        except Exception as e:
            print(f"Error processing mobile for {line}: {e}")
            continue

    df_mobile.to_csv(f"{mobile_csv_directory}/{name}_{getdate}.csv", index=False)
    print("All mobile data saved to CSV.")

# Worker Function for Desktop Processing
def process_desktop(file_path, desktop_csv_directory):
    df_desktop = pd.DataFrame([], columns=['URL', 'Desktop Performance', 'Accessibility', 'Best Practices', 'SEO', 'Server Response Time (ms)', 'Redirects (ms)',
                                           'Offscreen Images (ms)', 'Unused Javascript (ms)', 'Uses Optimized Images (ms)'])
    name = "DesktopPageSpeed"
    getdate = datetime.now().strftime("%m-%d-%y-%H-%M")

    with open(file_path) as pagespeedurls:
        content = pagespeedurls.readlines()
        content = [line.rstrip('\n') for line in content]

    for line in content:
        try:
            print(f"Running Desktop for {line}")
            api_url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
            params = {
                "url": line,
                "key": api_key,
                "strategy": "desktop",
                "category": ['performance','seo','best-practices','accessibility']
            }
            req = requests.get(api_url, params=params)

            if req.status_code == 200:
                json_data = req.json()

                # Extract relevant metrics
                performance = str(round(json_data["lighthouseResult"]["categories"]["performance"]["score"] * 100))
                accessibility = str(round(json_data["lighthouseResult"]["categories"]["accessibility"]["score"] * 100))
                best_practices = str(round(json_data["lighthouseResult"]["categories"]["best-practices"]["score"] * 100))
                seo = str(round(json_data["lighthouseResult"]["categories"]["seo"]["score"] * 100))
                server_response = str(json_data["lighthouseResult"]["audits"]["server-response-time"]["numericValue"])
                redirects = str(json_data["lighthouseResult"]["audits"]["redirects"]["numericValue"])
                offscreen_images = str(json_data["lighthouseResult"]["audits"]["offscreen-images"]["numericValue"])
                unused_javascript = str(json_data["lighthouseResult"]["audits"]["unused-javascript"]["numericValue"])
                use_optimized_images = str(json_data["lighthouseResult"]["audits"]["uses-optimized-images"]["numericValue"])

                # Add data to the DataFrame
                dict_desktop = {
                    "URL": line,
                    "Desktop Performance": performance,
                    "Accessibility": accessibility,
                    "Best Practices": best_practices,
                    "SEO": seo,
                    "Server Response Time (ms)": server_response,
                    "Redirects (ms)": redirects,
                    "Offscreen Images (ms)": offscreen_images,
                    "Unused Javascript (ms)": unused_javascript,
                    "Uses Optimized Images (ms)": use_optimized_images
                }
                df_desktop = df_desktop._append(dict_desktop, ignore_index=True)
            else:
                print(f"Error {req.status_code} for {line}: {req.reason}")

        except Exception as e:
            print(f"Error processing desktop for {line}: {e}")
            continue

    df_desktop.to_csv(f"{desktop_csv_directory}/{name}_{getdate}.csv", index=False)
    print("All desktop data saved to CSV.")

# Main Script
file_path, mobile_csv_directory, desktop_csv_directory = get_user_inputs()

# Start threads for mobile and desktop processing
mobile_thread = threading.Thread(target=process_mobile, args=(file_path, mobile_csv_directory))
desktop_thread = threading.Thread(target=process_desktop, args=(file_path, desktop_csv_directory))

mobile_thread.start()
desktop_thread.start()

mobile_thread.join()
desktop_thread.join()

print("Processing completed for both mobile and desktop!")
messagebox.showinfo("Runs Complete!", "Runs Complete")
