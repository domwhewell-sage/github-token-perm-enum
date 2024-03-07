import requests
import argparse

HEADERS = {
    'Accept': 'application/vnd.github.v3+json',
    'X-Github-Api-Version': '2022-11-28'
}

def getUser():
    url = 'https://api.github.com/user'
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        print('[-] Error: ' + str(response.status_code) + ' ' + response.json()['message'])
        return None

def getRepos():
    i=1
    while True:
        url = 'https://api.github.com/user/repos?per_page=100&page=' + str(i)
        response = requests.get(url, headers=HEADERS)
        response_json = response.json()
        if response.status_code != 200:
            print('[-] Error: ' + str(response.status_code) + ' ' + response.json()['message'] + ' When trying to access user repos')
            break
        if not response_json:
            break
        for repo in response_json:
            if repo['private']:
                permissions = []
                for key, value in repo['permissions'].items():
                    if value == True:
                        permissions.append(key.capitalize())
                print("%s permissions on %s" % (", ".join(permissions), repo['html_url']))
        i+=1

def getOrgs():
    orgs = []
    url = 'https://api.github.com/user/orgs'
    response = requests.get(url, headers=HEADERS)
    response_json = response.json()
    for org in response_json:
        orgs.append(org['login'])
    return orgs

def getPrivateOrgRepos(orgs):
    for org in orgs:
        i=1
        while True:
            url = 'https://api.github.com/orgs/' + org + '/repos?per_page=100&page=' + str(i)
            response = requests.get(url, headers=HEADERS)
            response_json = response.json()
            if response.status_code != 200:
                print('[-] Error: ' + str(response.status_code) + ' ' + response.json()['message'] + ' When trying to access the organization ' + org)
                break
            if not response_json:
                break
            for repo in response_json:
                if repo['private']:
                    permissions = []
                    for key, value in repo['permissions'].items():
                        if value == True:
                            permissions.append(key.capitalize())
                    print("%s permissions on %s" % (", ".join(permissions), repo['html_url']))
            i+=1

def parse_arguments():
    parser = argparse.ArgumentParser(description='Supply a github personal access token to check what private repositories it has access to.')

    parser.add_argument('--token', '-t', metavar='ghp_xxxx', type=str, required=True, help='The github personal access token to use in requests to the github api.' ) 

    args = parser.parse_args()

    HEADERS.update({'Authorization': 'Bearer ' + args.token})

def main():
    user = getUser()
    if user:
        print('[+] User: ' + user['login'])
        print('[+] Enumerating private user and org repos...')
        getRepos()
        orgs = getOrgs()
        getPrivateOrgRepos(orgs)

if __name__== "__main__":
    parse_arguments()
    main()
