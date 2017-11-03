import requests
import pprint
import json
import sys

class JudoBaseSearchFailed(Exception):
    def __init__(self):
        pass

class JudoBase:
    def __init__(self):
        self._baseuri = 'https://data.ijf.org/api/get_json?access_token='
        pass

    def sendrequest(self):
        self._request = requests.get(self._uri)

    def getresponse(self):
        if self._request.text == '[]':
            raise JudoBaseSearchFailed
        return (self._request.status_code,self._request.text)

    def search(self,query):
        self._uri =(
                '%s'
                '&params[q]=%s'
                '&params[action]=general.search_all'
                % (self._baseuri,query)
                )
        self.sendrequest()

    def searchbydate(self,day,month,year):
        self._uri = (
                '%s'
                '&params[action]=competitor.get_list'
                '&params[__ust]='
                '&params[year]=2012'
                '&params[month]=4'
                '&params[rank_group]='
                '&params[sort]=-1'
                % (self._baseuri)
                )

    def searchbycompetitor(self,weight,country):
        self._uri = (
                '%s'
                '&params[action]=competitor.get_list'
                '&params[__ust]='
                '&params[weight]='
                '&params[country]=%s'
                '&params[q]'
                % (self._baseuri)
                )

    def getcontests(self,id):
        self._uri = (
                '%s'
                '&params[action]=contest.find'
                '&params[__ust]='
                '&params[id_person]=%s'
                '&params[limit]=5000'
                % (self._baseuri, id)
                )
        self.sendrequest()

    def getcontest(self,id):
        self._uri = (
                '%s'
                '&params[action]=contest.find'
                '&params[__ust]='
                '&params[contest_code]=%s'
                '&params[part]=info,score_list,media,events'
                % (self._baseuri,id)
                )
        self.sendrequest()

    def getcompetitions(self,query):
        self._uri = (
                '%s'
                '&params[action]=competition.get_list'
                '&params[__ust]='
                '&params[year]=2017'
                '&params[month]='
                '&params[rank_group]='
                '&params[sort]=-1'
                % (self._baseuri)
                )
        self.sendrequest()

    def getcompetition_results(self,id):
        self._uri = (
                '%s'
                '&params[action]=competition.results'
                '&params[__ust]='
                '&params[id_competition]=%s'
                % (self._baseuri,id)
                )
        self.sendrequest()

def getcompetitions(judobase):
    judobase.getcompetitions('q')
    competitions = json.loads(judobase.getresponse()[1])
    for item in competitions:
        print '%s %s %s' % (item['name'],item['has_results'],item['id_competition'])
        judobase.getcompetition_results(item['id_competition'])
        print judobase.getresponse()[1]
        results = json.loads(judobase.getresponse()[1])
        print results

def main():
    query = JudoBase()
    query.search('mckenzie ashley')
    try:
        print query.getresponse()[1]
    except JudoBaseSearchFailed:
        print 'Search failed\n'
        sys.exit(1)
    player =  json.loads(query.getresponse()[1])
    print query.getresponse()[0]
    id =  player[0]['id']
    query.getcontests(id)
    contests = json.loads(query.getresponse()[1])
    num_contests = 0
    num_wins = 0
    fullcontest = []
    for contest in contests['contests']:
        if contest['id_winner'] == id:
            num_wins += 1

        num_contests += 1
        fullcontest.append(contest['contest_code_long'])

    print "%d %d %f\n" % (num_wins, num_contests,
            (float(num_wins)/float(num_contests)) * 100)

    getcompetitions(query)
#    for c in fullcontest:
#        query.getcontest(c)
#        fc =  json.loads(query.getresponse()i[1])
#        for key in fc['contests']:
#            pprint.pprint(key)

main()
