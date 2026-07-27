from rdkit.Chem import AllChem, DataStructs

class SimilarityAgent:
    def __init__(self, reference_smiles_list=[]):
        self.refs = []
        for sm in reference_smiles_list:
            mol = Chem.MolFromSmiles(sm)
            if mol:
                fp = AllChem.GetMorganFingerprintAsBitVect(mol, 2, nBits=2048)
                self.refs.append({"smiles": sm, "fp": fp})

    def process(self, compounds):
        for comp in compounds:
            mol = comp["mol_obj"]
            query_fp = AllChem.GetMorganFingerprintAsBitVect(mol, 2, nBits=2048)
            
            max_sim = 0
            best_match = None
            
            for ref in self.refs:
                sim = DataStructs.TanimotoSimilarity(query_fp, ref["fp"])
                if sim > max_sim:
                    max_sim = sim
                    best_match = ref["smiles"]
                    
            comp["similarity"] = {
                "Max_Tanimoto": max_sim,
                "Best_Reference_Match": best_match
            }
        return compounds
