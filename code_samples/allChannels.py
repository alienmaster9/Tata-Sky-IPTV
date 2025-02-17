### Script to get all channels from tata sky
import threading
API_BASE_URL = "https://kong-tatasky.videoready.tv/"
import requests
import json as json

channel_list = []


def getChannelInfo(channelId):
    url = API_BASE_URL + "content-detail/pub/api/v1/channels/" + channelId
    x = requests.get(url)
    channel_meta = x.json()['data']['meta'][0]
    channel_detail_dict = x.json()['data']['detail']
    onechannl = {
        "channel_id": str(channelId),
        "channel_name": channel_meta['channelName'],
        "channel_license_url": channel_detail_dict['dashWidewineLicenseUrl'],
        "channel_url": channel_detail_dict['dashWidewinePlayUrl'],
        "channel_entitlements": channel_detail_dict['entitlements'],
        "channel_logo": channel_meta['channelLogo'],
    }
    channel_list.append(onechannl)


def saveChannelsToFile():
    print(len(channel_list))
    with open("allchannels.json", "w") as channel_list_file:
        json.dump(channel_list, channel_list_file)


def processChnuks(channel_lists):
    for channel in channel_lists:
        print("Getting channelId:" ,channel['id'])
        channel_id = str(channel['id'])
        getChannelInfo(channel_id)


def getAllChannels():
    ts = []
    url = API_BASE_URL + "content-detail/pub/api/v1/channels?limit=443"
    x = requests.get(url)
    channel_list = x.json()['data']['list']
    print("Total Channels fetched:", len(channel_list))
    print("Fetching channel info..........")
    for i in range(0, len(channel_list), 5):
        t = threading.Thread(target=processChnuks, args=([channel_list[i:i + 5]]))
        ts.append(t)
        t.start()
    for t in ts:
        t.join()
    print("Saving all to a file.... " + str(len(channel_list)))
    saveChannelsToFile()


if __name__ == '__main__':
    getAllChannels()
