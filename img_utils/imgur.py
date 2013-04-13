import os.path

CLIENT_ID = 'd968b2b8df7f127'


def upload(image):
    try:
        import requests
    except ImportError:
        print "moudle requests not found"
        print "try 'pip install requests' to install"
        raise ImportError
    url = "https://api.imgur.com/3/upload"
    headers = {'Authorization': 'Client-ID %s' % CLIENT_ID}
    files = {'image': open(image, 'rb').read()}

    response = requests.post(url, headers=headers, files=files, verify=False)
    result = response.json()
    if result.get('status'):
        link = result.get('data').get('link')
        base, ext = os.path.splitext(link)
        return {
            'origin': link,
            'small': base + 's' + ext,
            'large': base + 'l' + ext,
        }


if __name__ == "__main__":
    import optparse
    parser = optparse.OptionParser()
    parser.add_option('-u', '--upload', dest='upload', metavar='FILE',
                      help="upload file to imgur.com")

    opts, args = parser.parse_args()
    if opts.upload:
        print upload(opts.upload)
    else:
        parser.print_help()
