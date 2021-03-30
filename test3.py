import json
import libraryUtils

# print(libraryUtils.checkAdmin('1B4CDA49ECF4477CB7C7290A241EB14C'))
#
# print(libraryUtils.checkUserByToken('1B4CDA49ECF4477CB7C7290A241EB14C'))
#
# print(libraryUtils.checkUserById(1800130836))
#
# print(libraryUtils.autoSign('1B4CDA49ECF4477CB7C7290A241EB14C'))
#
# print(libraryUtils.sign('1B4CDA49ECF4477CB7C7290A241EB14C','HHXYTSG20620027'))

grabUser = {
    '1': {
        'token': '123',
        'pass': '123'
    },
    '2': {
        'token': '123',
        'pass': '123'
    }
}

for i in grabUser.values():
    if i['pass']=='123':
        print(i)

# print('123' in grabUser.values()['pass'])

# with open('./config.json','r') as f:
#     config = json.load(f)
#     print(json.loads(config['users']['1800130937']))

# with open('./config.json','w') as f:
#     config['users']['1800130935']['token'] = 't'
#     config['users']['1800130935']['password'] = '1800130935'
#     f.write(json.dumps(config))


# results={}
# for i in range(58):
#     info={}
#     info['token']=''
#     info['password'] = ''
#     info['userInfo']={}
#     results['18001309'+str(i).zfill(2)]=info
#
# print(json.dumps(results))
