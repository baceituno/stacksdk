import requests
import openai

class stack_client:
    def _init_(self,key='none') -> None:
        self.key = key
        self.url = 'https://stackend.vercel.app/'
        self.dataset = []
        self.logging = True
    
    def post(self, req, data=None):
        headers = {'Authorization': f'Bearer {self.key}', "Content-Type": "application/json"}
        res = requests.post(url=self.url+req, json=data, headers=headers)
        return res.json()
    
    def get(self, req, data=None):
        headers = {'Authorization': f'Bearer {self.key}', "Content-Type": "application/json"}
        res = requests.post(url=self.url+req, json=data, headers=headers)
        return res.json()
    
    def call_model(self, model="text-davinci-003", prompt="Say this is a test", params={'temperature': 0, 'stop': [], 'max_tokens': 10}, local=True):
        if local:
            res = openai.Completion.create(model=model, prompt=prompt, temperature=params['temperature'], max_tokens=['max_tokens'])
            completion = {'res': res.choices[0].text}
        else:
            completion = self.post('run_model', data={'model': model, 'prompt': prompt, 'params': params})        
        
        if self.logging:
            self.dataset.append({'prompt': prompt, 'completion': completion['res']})
        
        return completion['res']

    def call_chain(self, chain, inputs=[]):
        completion = self.post('run_chain', data={'chain': chain, 'inputs': inputs})        
        
        if self.logging:
            self.dataset.append(completion['dataset'])
    
        return completion['res']
    
    def upload_data(self, dataset='api'):
        self.post(req=f'add_data_to_dataset?dataset={dataset}', data=self.dataset)
    
    def create_dataset(self, dataset='api', type='gpt'):
        self.post(req='dataset', data={'name': dataset, 'type': type})