import igraph as ig
import random
import string
from datetime import datetime

def sim_bo(n_person_owners,n_entity_owners,format):
    g = ig.Graph(directed = True)
    g.add_vertices(n_person_owners+n_entity_owners+1)
    col = []
    statements = []
    nams = []

    for i in range(n_entity_owners+n_person_owners+1):
        d = {}
        d['statementID'] = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(32))
        if i == 0:
            col.append('grey')
            nams.append('Company ' + str(i+1))
            d['statementType'] = 'entityStatement'
            d['isComponent'] = False
            d['statementDate'] = datetime.today().strftime('%Y-%m-%d')
            d['entityType'] = 'registeredEntity'
            d['name'] = 'Company ' + str(i+1)
            d['identifiers'] = [{'scheme': 'GB-COH','id': ''.join(random.choice(string.digits) for _ in range(8))}]
            d['publicationDetails'] = {
            'publicationDate': datetime.today().strftime('%Y-%m-%d'),
            'bodsVersion': '0.2',
            'publisher': {
                'name': 'Company 1'}}
        else:
            if n_entity_owners == 0:
                g.add_edge(i,0)
                col.append('blue')
                nams.append('Person McPerson '+str(i+1))
                d['statementType'] = 'personStatement'
                d['isComponent'] = False
                d['statementDate'] = datetime.today().strftime('%Y-%m-%d')
                d['personType'] = 'knownPerson'
                d['nationalities'] = [{'code': 'GB'}]
                d['names'] = [{ 'type': 'individual','fullName': 'Person McPerson '+str(i+1),'givenName': 'Person','familyName': 'McPerson '+str(i+1)}]
                d['publicationDetails'] = {
                'publicationDate': datetime.today().strftime('%Y-%m-%d'),
                'bodsVersion': '0.2',
                'publisher': {
                    'name': 'Company 1'}}
            else:
                if format == 'wide':
                    if i <= n_entity_owners:
                        g.add_edge(i,0)
                        col.append('red')
                        nams.append('Company ' + str(i+1))
                        d['statementType'] = 'entityStatement'
                        d['isComponent'] = True
                        d['statementDate'] = datetime.today().strftime('%Y-%m-%d')
                        d['entityType'] = 'registeredEntity'
                        d['name'] = 'Company ' + str(i+1)
                        d['identifiers'] = [{'scheme': 'GB-COH','id': ''.join(random.choice(string.digits) for _ in range(8))}]
                        d['publicationDetails'] = {
                        'publicationDate': datetime.today().strftime('%Y-%m-%d'),
                        'bodsVersion': '0.2',
                        'publisher': {
                            'name': 'Company 1'}}
                    else:
                        g.add_edge(i,random.sample(range(n_entity_owners+1),1)[0])
                        col.append('blue')
                        nams.append('Person McPerson '+str(i+1))
                        d['statementType'] = 'personStatement'
                        d['isComponent'] = False
                        d['statementDate'] = datetime.today().strftime('%Y-%m-%d')
                        d['personType'] = 'knownPerson'
                        d['nationalities'] = [{'code': 'GB'}]
                        d['names'] = [{ 'type': 'individual','fullName': 'Person McPerson '+str(i+1),'givenName': 'Person','familyName': 'McPerson '+str(i+1)}]
                        d['publicationDetails'] = {
                        'publicationDate': datetime.today().strftime('%Y-%m-%d'),
                        'bodsVersion': '0.2',
                        'publisher': {
                            'name': 'Company 1'}}
                if format == 'long':
                    if i <= n_entity_owners:
                        g.add_edge(i,i-1)
                        col.append('red')
                        nams.append('Company ' + str(i+1))
                        d['statementType'] = 'entityStatement'
                        d['isComponent'] = True
                        d['statementDate'] = datetime.today().strftime('%Y-%m-%d')
                        d['entityType'] = 'registeredEntity'
                        d['name'] = 'Company ' + str(i+1)
                        d['identifiers'] = [{'scheme': 'GB-COH','id': ''.join(random.choice(string.digits) for _ in range(8))}]
                        d['publicationDetails'] = {
                        'publicationDate': datetime.today().strftime('%Y-%m-%d'),
                        'bodsVersion': '0.2',
                        'publisher': {
                            'name': 'Company 1'}}
                    else:
                        g.add_edge(i,n_entity_owners)
                        col.append('blue')
                        nams.append('Person McPerson '+str(i+1))
                        d['statementType'] = 'personStatement'
                        d['isComponent'] = False
                        d['statementDate'] = datetime.today().strftime('%Y-%m-%d')
                        d['personType'] = 'knownPerson'
                        d['nationalities'] = [{'code': 'GB'}]
                        d['names'] = [{ 'type': 'individual','fullName': 'Person McPerson '+str(i+1),'givenName': 'Person','familyName': 'McPerson '+str(i+1)}]
                        d['publicationDetails'] = {
                        'publicationDate': datetime.today().strftime('%Y-%m-%d'),
                        'bodsVersion': '0.2',
                        'publisher': {
                            'name': 'Company 1'}}
        statements.append(d)
    
    g.vs['color'] = col
    g.vs['label'] = nams
    #Now loop over edges to do ownership or control statements
    ooc = []
    el = g.get_edgelist()
    for edge in el:
        d = {}
        d['statementID'] = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(32))
        d['statementType'] = 'ownershipOrControlStatement'
        d['isComponent'] = statements[edge[1]]['statementType'] == 'entityStatement'
        d['statementDate'] = datetime.today().strftime('%Y-%m-%d')
        d['subject'] = {'describedByEntityStatement' if statements[edge[1]]['statementType'] == 'entityStatement' else 'describedByPersonStatement': statements[edge[1]]['statementID']}
        d['interestedParty'] = {'describedByEntityStatement' if statements[edge[0]]['statementType'] == 'entityStatement' else 'describedByPersonStatement': statements[edge[0]]['statementID']}
        d['interests'] = [
            {'type': 'shareholding',
            'interestLevel': 'direct',
            'beneficialOwnershipOrControl': statements[edge[1]]['statementType'] == 'personStatement',
            'startDate': '2016-01-01',
            'share': { 'exact': 100/sum([i[1] == edge[1] for i in el]),
            'minimum': 100/sum([i[1] == edge[1] for i in el]),
            'maximum': 100/sum([i[1] == edge[1] for i in el])}
            }
            ]
        d['publicationDetails'] = {
        'publicationDate': datetime.today().strftime('%Y-%m-%d'),
        'bodsVersion': '0.2',
        'publisher': {
            'name': 'Company 1'
        }
        }
        ooc.append(d)
    
    statements = statements + ooc

    return g, statements