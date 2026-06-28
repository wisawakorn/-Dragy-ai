import json
import urllib.request
import urllib.error

for path, data in [('/', None), ('/api/chat', {'message': 'test message'})]:
    url = 'http://127.0.0.1:8000' + path
    print('REQUEST', path)
    try:
        if data is None:
            with urllib.request.urlopen(url, timeout=10) as resp:
                body = resp.read().decode('utf-8', 'ignore')
                print('STATUS', resp.status)
                print(body[:1200])
        else:
            req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})
            with urllib.request.urlopen(req, timeout=10) as resp:
                body = resp.read().decode('utf-8', 'ignore')
                print('STATUS', resp.status)
                print(body)
    except urllib.error.HTTPError as e:
        print('HTTP ERROR', e.code)
        print(e.read().decode('utf-8', 'ignore'))
    except Exception as e:
        import traceback
        traceback.print_exc()
