from ...abc_base import PlayerBase
import json
import requests
from lxml.html.soupparser import fromstring

"""
    Class for loading players from ghin.
    The existing list of players is in a variable named player_list
    You can use it or call super().mergePlayers(new_player_list)
        the new_player_list param in mergePlayers is {club_member_number, name=name, handicap_index=handicap_index, data=data}
    You also need to call super().storePlayers() in order to update the database
    TODO: Activate, Inactivate, Delete
"""
class GHINPlayers(PlayerBase):

    def __init__(self):
        pass

    def loadPlayers(self, data):
        jsondata = json.loads(data)

        url = "http://ghp.ghin.com/GHPOnline/Club/LogonClub.aspx"

        payload = {
            '__ASYNCPOST':'true',
            '__EVENTARGUMENT':'',
            '__EVENTTARGET':'',
            '__EVENTVALIDATION':'/wEdAAlFBaqAugheNTMpDpyyDO2NcU6hUdNh6dvOB/8vCL+/AAkpGIC4ZRfvvF5vTc20DcCeRB2s5jI6AOXLEARhsW5eJmignBl2EqCZ+zHvdFHEpzn/bVwSjZqljFAqY2CQFEaPRZEuc0g4470jcP/IwC6TL0kG5Vt3hK8vgSqiH7DsXgmz9wCNPqpuDOHcORVb9HHFVa1rWrclV36BVcExYzloSCJcKQ==',
            '__LASTFOCUS':'',
            '__VIEWSTATE':'/wEPZwUPOGQ0ZGI0NTAwYTQ0YjZllSagtgMikVRXMYAIveXV3WTD/dw=',
            '__VIEWSTATEGENERATOR':'9B52B84B',
            'ctl00$cph$btnLogin':'Log In',
            'ctl00$cph$chkRememberMe':'on',
            'ctl00$cph$txtAssociation': jsondata['assn_number'],
            'ctl00$cph$txtClub':jsondata['club_number'],
            'ctl00$cph$txtPassword':jsondata['password'],
            'ctl00$sm':'ctl00$cph$upLogin|ctl00$cph$btnLogin'
        }
        headers = {
            'x-newrelic-id': "Ug8AVlJRGwcHVFlQDgA=",
            'origin': "http://ghp.ghin.com",
            'user-agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
            'content-type': "application/x-www-form-urlencoded",
            'cache-control': "no-cache",
            'x-microsoftajax': "Delta=true",
            'x-devtools-emulate-network-conditions-client-id': "26e639d7-2ec8-49fb-aba2-65a83facd2d7",
            'x-requested-with': "XMLHttpRequest",
            'x-devtools-request-id': "10196.4200",
            'accept': "*/*",
            'referer': "http://ghp.ghin.com/GHPOnline/Club/LogonClub.aspx",
            'accept-encoding': "gzip, deflate",
            'accept-language': "en-US,en;q=0.8",
            'postman-token': "b04e0930-5e41-4055-fce7-a83aeb0705b4"
        }

        response = requests.request("POST", url, data=payload, headers=headers)
        
        url = "http://ghp.ghin.com/GHPOnline/Club/GolferSearch.aspx"

        querystring = {"Assoc":jsondata['assn_number'],"Club":jsondata['club_number'],"Svc":"1","Status":"1"}

        cookie = response.headers['Set-Cookie'].split(" ")[0] + ' '
        cookie += response.headers['Set-Cookie'].split(" ")[3] + ' '
        cookie += 'HomeCourses.aspx:ctl00$cph$gvCourse$trPager$cboPagerSize=25; ScoreMaintenance.aspx:ctl00$cph$gvScores$trPager$cboPagerSize=25; GolferSearch.aspx:ctl00$cph$gvGolfer$trPager$cboPagerSize=500; '
        cookie += '__utma=229584714.2112325690.1501258985.1501259883.1501259882.1; __utmc=229584714; __utmz=229584714.1501259883.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); '
        cookie += '__gads=ID=fe2715360cb75e78:T=1501259882:S=ALNI_MbHHKFF1rqvNO4cCn_YBKez5-pqpA; _ga=GA1.2.2112325690.1501258985; _gid=GA1.2.1432345712.1501865813'

        headers = {
            'x-devtools-request-id': "10196.3884",
            'x-devtools-emulate-network-conditions-client-id': "26e639d7-2ec8-49fb-aba2-65a83facd2d7",
            'upgrade-insecure-requests': "1",
            'user-agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
            'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            'referer': "http://ghp.ghin.com/GHPOnline/Club/default.aspx",
            'accept-encoding': "gzip, deflate",
            'accept-language': "en-US,en;q=0.8",
            'cookie': cookie,
            'cache-control': "no-cache",
            'postman-token': "dfb94adf-1253-6fd7-f7c6-c2eb94530018"
            }

        response = requests.request("GET", url, headers=headers, params=querystring)

        tree = fromstring(response.text)
        new_player_list = []
        for tr in tree.xpath('//*[@id="cph_gvGolfer"]/tbody/tr'):
            name = tr.xpath('td[3]/a')[0].text
            ghin_number = tr.xpath('td[2]')[0].text
            handicap_index = ''.join(i for i in tr.xpath('td[4]')[0].text if i in '0123456789.')
            if (handicap_index == ''):
                handicap_index = 1
            new_player_list.append({'club_member_number': ghin_number, 'name': name, 'handicap_index': handicap_index, 'player_type__id': 1, 'data': {}})
        super(GHINPlayers, self).mergePlayers(new_player_list)
        super(GHINPlayers, self).storePlayers()
