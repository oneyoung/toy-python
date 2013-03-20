import json
import urllib2
import base64

CLIENT_ID = 'd968b2b8df7f127'


def upload(image):
    f = open(image, 'rb')
    img_data = base64.b64encode(f.read())
    img_data.strip()
    data = 'image=%s&type=base64' % img_data

    url = "https://api.imgur.com/3/upload"
    req = urllib2.Request(url)
    req.add_header('Authorization', 'Client-ID %s' % CLIENT_ID)
    req.add_data(data)

    response = urllib2.urlopen(req)
    result = json.loads(response.read())
    if result.get('status'):
        link = result.get('data').get('link')
        return link


if __name__ == "__main__":
    print upload('/tmp/img.jpg')
