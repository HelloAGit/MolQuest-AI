import requests
import urllib.parse

class EvidenceAgent:
    def process(self, compounds):
        for comp in compounds:
            smiles = comp["smiles"]
            encoded_smiles = urllib.parse.quote(smiles)
            url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/{encoded_smiles}/property/Title/JSON"
            
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    title = data['PropertyTable']['Properties'][0].get('Title', 'Unknown')
                    comp["evidence"] = {"PubChem_Match": True, "Name": title}
                else:
                    comp["evidence"] = {"PubChem_Match": False, "Name": "Novel"}
            except Exception as e:
                comp["evidence"] = {"PubChem_Match": "Error", "Name": str(e)}
        return compounds
