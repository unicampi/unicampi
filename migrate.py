from kinto_http import Client
import dacParser

client = Client(server_url="http://localhost:8888/v1",
                auth=('aaa', 'aaa'))
 

class DefaultParserService(object):

    def __init__(self):
        self.client = Client(server_url="http://localhost:8888/v1",
                             auth=('aaa', 'aaa'))

    def create(self):
        raise NotImplemented

    def update(self):
        raise NotImplemented


class DacService(DefaultParserSetup):
  
    COLLECTIONS = [
        'institutos',
        'disciplinas',
        'oferecimentos',
    ] 
    PERIODS = [
        (2016,2),
    ]

    def __init__(self):
        super(DacService, self).__init__()

    def create(self):
        
        # Create DAC bucket
        self.client.update_bucket('dac')
        self.client.patch_bucket('dac', permissions={'read': ['system.Everyone']})
        
        # Move client to bucket
        self.client = self.client.clone(bucket='dac')

        # Create main collections
        for collection in self.COLLECTIONS:
            self.client.update_collection(collection=collection)
        
        # Fetch collection records
        for collection in self.COLLECTIONS:
            records = getattr(self, '_%s' % collection)()
            for record in records:
                self.client.update_record(record, collection=collection)

    def update(self):

        # Move client to bucket
        self.client = self.client.clone(bucket='dac')
        
        # Fetch and patch collection records
        for collection in self.COLLECTIONS:
            records = getattr(self, '_%s' % collection)()
            for record in records:
                self.client.patch_record(record, collection=collection)

    def _institutos(self):

        data = dacParser.getAllInstitutes()

        for record in data:
            record['id'] = record['sigla'].lower()

        return data
    
    def _disciplinas(self):

        institutes = self._institutos()

        data = []
        for inst in institutes:
            subs = dacParser.getAllSubjects(inst['sigla'])

            for sub in subs:
                sub['unidade'] = inst['sigla']

            data += subs

        for record in data:
            record['id'] = record['sigla'].lower()

        return data
    
    def _oferecimentos(self):

        subjects = self._disciplinas()

        data = []
        
        for sub in subjects:
            for year, sem in self.PERIODS:
                for of_id in sub['turmas']:
                    # XXX:
                    off = dacParser.getOffering(sub['sigla'],
                                                of_id,
                                                year,
                                                sem)
                          

                    off['unidade'] = sub['unidade']
                    data.append(off)

        for record in data:
            record['id'] = "%s%s" % (record['sigla'].lower(),
                                     record['turma'].lower())

        return data
