# importing modules
import requests
import json

# initiate a list to write the desired output on in
output = []

# api key for the google project
api_key = "" # Enter your API Key

# the playlist ID from the url on the browser
playlist_id = "PLLasX02E8BPArtrhIH0FP8bJU2odUbNR7"

def get_playlist_data(api_key, playlist_id):
    '''
    this function is used for calling the api of youtube data to get the data from the playlist
    and fill the output list with a dictionary for each comment in each video in the playlist

    Args:
    api_key <str> : a string with your api key from google api project
    playlist_id <str> : a string with the playlist unique id from the url on the browser
    '''
    # the url that will be called using the script to get the playlist data
    url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId={playlist_id}&key={api_key}"

    # get the response from the url get request as json format
    res = requests.get(url).json()
    
    # get the items key data from the json overall result
    items_list = res['items']

    # function excution to fill the output list with videos and its comments retrieved data
    append_playlist_data(items_list)

    # iterate the pages of videos in the playlist as the maximum result can be retrieved is 50
    while 'nextPageToken' in res.keys():
        
        # get the next page token to paginate
        page_token = res['nextPageToken']

        # the new url to call after adding the page token
        url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId={playlist_id}&pageToken={page_token}&key={api_key}"

        # get the response from the url get request as json format
        res = requests.get(url).json()

        # get the items key data from the json overall result
        items_list = res['items']

        # function excution to fill the output list with videos and its comments retrieved data
        append_playlist_data(items_list)

def append_playlist_data(page_items_list):
    '''
    this function iterate through playlist videos and comments of the videos to append the data to the output variable
    with the proper structure that required

    Args:
    page_items_list <list<dir>> : list of items for the playlist JSON response from the API
    '''
    # iterate through each item in the list of items and get [video unique id - video number in the playlist - video title]
    for i in range(len(page_items_list)):
        video_id = page_items_list[i]['snippet']['resourceId']['videoId']
        video_number = page_items_list[i]['snippet']['position']+1
        video_title = page_items_list[i]['snippet']['title']

        # function excution to iterate through the comments thread of a video and get the data for all comments as list of objects
        comments_list = get_comments_data(api_key, video_id)

        # if there are comments append data as described in the requirements in output list
        if len(comments_list):
            
            # iterate through the comments to append the data per comment not by video as described in the requirements
            for j in range(len(comments_list)):
                output.append({
                    'Video Number': video_number,
                    'Video ID': video_id,
                    'Video Title': video_title,
                    'Comment Text': comments_list[j]['Comment Text'],
                    'Comment Author': comments_list[j]['Comment Author'],
                    'Comment Date': comments_list[j]['Comment Date']
                })

        # if there aren't comments append data as described in the requirements in output list
        else:
            output.append({
                'Video Number': video_number,
                'Video ID': video_id,
                'Video Title': video_title,
                'Comment Text': '',
                'Comment Author': '',
                'Comment Date': ''
                })

def get_comments_data(api_key, video_id):
    '''
    this function call the api to get the comment threads and iterate through it to create a list of all comments on a video

    Args:
    api_key <str> : a string with your api key from google api project
    video_id <str> : a string with the video unique id

    Returns:
    <list<dic>> : list with each comment as index with 3 required data [Text - Author - Date]
    '''
    # declare the maximum value for the api  to retrieve comments results
    max_res = 100

    # comments list to append the comments on it
    comments_list = []

    # the url that will be called using the script to get the comment threads data
    url = f"https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId={video_id}&maxResult={max_res}&key={api_key}"

    # get the response from the url get request as json format
    res = requests.get(url).json()

    # get the items key data from the json overall result
    comment_items_list = res['items']

    # iterate through the comment threads to append the data as required for each comment
    for i in range(len(comment_items_list)):
        comment_txt = comment_items_list[i]['snippet']['topLevelComment']['snippet']['textDisplay']
        comment_author = comment_items_list[i]['snippet']['topLevelComment']['snippet']['authorDisplayName']
        comment_date = comment_items_list[i]['snippet']['topLevelComment']['snippet']['publishedAt']
        comments_list.append({  
            'Comment Text': comment_txt,
            'Comment Author': comment_author,
            'Comment Date': comment_date
        })  

    # return the list
    return comments_list


# the excuted code to generate the output file when run `python .` inside the directory of this script
if __name__ == "__main__":
    # function excution to change output list value to the desired value
    get_playlist_data(api_key, playlist_id)

    # open a JSON file wit write permission and dump the output list of directory into it as JSON string and close the file
    with open('Output.json','w') as file:
        file.write(json.dumps(output))
        
