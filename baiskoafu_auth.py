import requests
import string
import random
import json
import config
import baiskoafu_download_manager


API_VERSION = "v2.04"
login_url   = f"https://admin.baiskoafu.com/api/{API_VERSION}/user/login/"
search_url  = f"https://admin.baiskoafu.com/api/{API_VERSION}/search/"
prmm_url    = f"https://admin.baiskoafu.com/api/{API_VERSION}/user/change-primary-device/"
VIDEO_CDN   = "https://dk4c1mppw2v29.cloudfront.net/"
AUDIO_CDN   = "https://d1g98ytv3fry8t.cloudfront.net/"
KEY_LEN = 32

def chars():
    return (string.ascii_letters+string.digits)  

def gen():
    keylist = [random.choice(chars()) for i in range(KEY_LEN)]
    return ("".join(keylist))

def login(username, password, query=""):
    AUTH = {
        "device_token": f"{gen()}",
        "device_type": "ios",
        "email": f"{username}",
        "password": f"{password}",
        "unique_device_id": f"{gen()}"
        }

    resp = requests.session()
    resp.post(login_url, data=AUTH)
    r = resp.post(login_url, data=AUTH)

    userinfo    = json.loads(r.text)
    
    if "The password you entered is incorrect." in str(userinfo['message']):
        print("The password you entered is incorrect.")
        baiskoafu_download_manager.wait(3)
        exit()
    
    if "Login Successful" in userinfo['message']:

        FIRST_NAME  = userinfo['user']['first_name']
        LAST_NAME   = userinfo['user']['last_name']
        TOKEN	    = userinfo['user']['access_token']
        DEVICE_ID	= userinfo['user']['device_id']
        PRIMARY	    = userinfo['user']['subscription']
        ID_AUTH     = {"Authorization": f"JWT {TOKEN}"}

        print(f"Hi, {FIRST_NAME} {LAST_NAME}")

        if config.IS_PRIMARY_DEVICE and  str(PRIMARY) == "Premium":

            primary = resp.patch(prmm_url, data={"device_id" : f"{DEVICE_ID}"}, headers=ID_AUTH)

        def search_engine():

            if query == "":
                search_query = input("Search for songs, movies, series to download\nSEARCH :  ")
            else: search_query = query
            baiskoafu_download_manager.clear()
            if search_query.lower() == "return 0":
                exit()
            if search_query == "" or None:
                search_engine()
            
            SEARCH_DATA = {
            "category_name": "All",
            "device_id": f"{DEVICE_ID}",
            "search_keyword": f"{search_query}"
            }

            ids = resp.post(search_url, data=SEARCH_DATA, headers=ID_AUTH)
            dummy = json.loads(ids.text)
            
            I = ['ID', 'TYPE', 'CATEGORY', 'EPISODE', 'SERIES/FILM', 'FILE NAME', 'STATUS']
            print(f'{I[0]:<5} | {I[1]:<15} | {I[2]:<15} | {I[3]:<15} | {I[4]:<20} | {I[5]:<25} | {I[6]:<15}')
            print('_' * 160)
            search_result = 0

            # Print the raw response for debugging purposes
            with open("raw_response.txt", "w") as file:
                file.write(json.dumps(dummy, indent=4))

            for i in dummy['data']:

                try:
                    for i in i['items']:

                        ITEM_ID         = i['item_id']
                        ITEM_TITLE      = i['item_title'][0:30]
                        CONTENT_TYPE    = i['content_type']
                        ITEM_CONTENT_M	= i['item_content_url']
                        
                        # Get the first category name if available
                        try:
                            ITEM_CATEGORY = i['categories'][0]['name'] if i.get('categories') and len(i['categories']) > 0 else 'Unknown'
                        except (IndexError, KeyError, TypeError):
                            ITEM_CATEGORY = 'Unknown'
                        
                        # Get episode information
                        try:
                            # Extract episode number from title if it starts with "Episode"
                            if i['item_title'].lower().startswith('episode'):
                                episode_parts = i['item_title'].split()
                                if len(episode_parts) > 1:
                                    ITEM_EPISODE = episode_parts[1].rstrip(':')
                                else:
                                    ITEM_EPISODE = 'N/A'
                            else:
                                ITEM_EPISODE = 'N/A'
                        except:
                            ITEM_EPISODE = 'N/A'
                        
                        # Get series/film name
                        try:
                            # Try to get series name first
                            if 'series' in i and i['series'] and 'series_name' in i['series']:
                                ITEM_SERIES = i['series']['series_name'][0:20]
                            # Fallback to album_id or other identifier
                            elif 'album_id' in i and i['album_id']:
                                ITEM_SERIES = f"Album {i['album_id']}"
                            else:
                                ITEM_SERIES = 'N/A'
                        except:
                            ITEM_SERIES = 'N/A'
                        
                        # Check encryption and premium status
                        try:
                            is_encrypted = i.get('is_encrypted', False)
                            is_verimatrix = i.get('is_verimatrix_encrypted', False)
                            premium_status = i.get('premium_status', 'Free')
                            android_url = i.get('android_content_url', '')
                            
                            # Determine status
                            if is_encrypted or is_verimatrix:
                                if premium_status == 'Premium':
                                    ITEM_STATUS = 'ENCRYPTED+PREM'
                                else:
                                    ITEM_STATUS = 'ENCRYPTED'
                            elif premium_status == 'Premium':
                                ITEM_STATUS = 'PREMIUM'
                            else:
                                ITEM_STATUS = 'FREE'
                        except:
                            ITEM_STATUS = 'UNKNOWN'
                            is_encrypted = False
                            is_verimatrix = False
                            android_url = ''
                        
                        # Truncate URL for display

                        if CONTENT_TYPE == "audio":
                            CONTENT_URL_DISPLAY = AUDIO_CDN+ITEM_CONTENT_M
                        else:
                            CONTENT_URL_DISPLAY = VIDEO_CDN+ITEM_CONTENT_M
                        
                        ITEM_TITLE = ITEM_TITLE if len(ITEM_TITLE) < 25 else ITEM_TITLE[:25] + "..."
                        print(f'{ITEM_ID :<5} | {CONTENT_TYPE :<15} | {ITEM_CATEGORY :<15} | {ITEM_EPISODE :<15} | {ITEM_SERIES :<20} | {ITEM_TITLE :<25} | {ITEM_STATUS :<15}')
                        
                        # Show warning for encrypted content
                        # if is_encrypted or is_verimatrix:
                        #     print(f'      ⚠️  WARNING: This content is encrypted - download quality will be very poor (2-sec clips, ~20kbps)')
                        #     if android_url:
                        #         print(f'      📱 DASH URL available: {android_url[:60]}...')
                        
                        search_result += 1

                except IndexError: pass
                except KeyError: pass

            if search_result == 0:

                print("\nNo results :(\nSearching for series? try with episode name.\n")
                search_engine()
        
            def user_choice():

                choice_list = []
                print('_' * 100)
                try:
                    choice = int(input("Enter ID number to download or Enter 1 to Search again: "))
                    baiskoafu_download_manager.clear()
                    if choice == 0:
                        exit()
                    if choice == 1:
                        search_engine()
                except ValueError:
                    print("INVALID ID NUMBER! TRY AGAIN")
                    user_choice()

                for i in dummy['data']:

                    try:
                        for i in i['items']:
                            ITEM_ID         = i['item_id']
                            ITEM_TITLE      = i['item_title']
                            CONTENT_TYPE    = i['content_type']
                            ITEM_CONTENT_M	= i['item_content_url']

                            if choice == int(ITEM_ID):
                                
                                # Check if content is encrypted before downloading
                                is_encrypted = i.get('is_encrypted', False)
                                is_verimatrix = i.get('is_verimatrix_encrypted', False)
                                premium_status = i.get('premium_status', 'Free')
                                
                                if is_encrypted or is_verimatrix:
                                    print(f"\n⚠️  WARNING: '{ITEM_TITLE}' is ENCRYPTED!")
                                    print("   This will result in very poor quality:")
                                    print("   • Video duration: ~2 seconds only")
                                    print("   • Bitrate: ~20kbps (extremely low)")
                                    print("   • Content may be unwatchable")
                                    if premium_status == 'Premium':
                                        print("   • Requires Premium subscription")
                                    
                                    confirm = input("\nDo you still want to download this encrypted content? (y/N): ")
                                    if confirm.lower() != 'y':
                                        print("Download cancelled. Choose a different item.")
                                        user_choice()
                                        return

                                if CONTENT_TYPE == "audio":
                                    choice_list.append(str(ITEM_TITLE)+'.mp3')
                                else: choice_list.append(str(ITEM_TITLE)+'.mp4')    # index 0 -- > Title
                                choice_list.append(CONTENT_TYPE)
                                choice_list.append(ITEM_CONTENT_M)
  

                    except IndexError: pass
                    except KeyError: pass
                
                if len(choice_list) == 3:

                    if choice_list[2] == "": # empty links
                        print("URL not found!")
                        baiskoafu_download_manager.wait(5)
                        search_engine() # TODO go to main

                    filename = choice_list[0]
                    if choice_list[1] == 'audio':
                        cdn_url = f"{AUDIO_CDN}{choice_list[2]}"
                    else:
                        cdn_url = f"{VIDEO_CDN}{choice_list[2]}"
                    
                    try:
                        resp_cdn = requests.get(cdn_url)
                        resp_cdn.raise_for_status()  # Raise exception for bad status codes
                        resp_cdn_data = resp_cdn.text.split('\n')
                    except requests.RequestException as e:
                        print(f"Error accessing content URL: {e}")
                        print("This might be encrypted content or require special authentication.")
                        user_choice()
                        return
                    
                    high_med_low = []
                    base_url = cdn_url.split('/')
                    base_url.pop(-1)
                    base_url = "/".join(base_url) + "/"
                    
                    for m3 in resp_cdn_data:
                        if m3.endswith('m3u8'):
                            high_med_low.append(m3)

                    if len(high_med_low) == 0:
                        print("⚠️  No downloadable streams found!")
                        print("This content might be encrypted or require special decryption.")
                        print("Try selecting non-encrypted content instead.")
                        user_choice()
                        return

                    # Always try to get the highest quality available
                    if len(high_med_low) > 0:
                        if config.media_quality() == 'high' and len(high_med_low) >= 1:
                            base_url += high_med_low[0]         #  -- > highest available
                        elif config.media_quality() == 'medium' and len(high_med_low) >= 2:
                            base_url += high_med_low[1]         #  -- > medium
                        elif config.media_quality() == 'low' and len(high_med_low) >= 3:
                            base_url += high_med_low[2]         #  -- > low
                        else:
                            # Fallback to highest available if requested quality not found
                            base_url += high_med_low[0]         #  -- > fallback to highest

                    print(f"Downloading from: {base_url}")
                    baiskoafu_download_manager.get_ts_files(base_url)
                    baiskoafu_download_manager.download()
                    baiskoafu_download_manager.combine(filename)
                else:
                    print("❌ Invalid selection or item not found!")
                    print("Please check the ID and try again.")
                    user_choice()

            user_choice()

        search_engine()