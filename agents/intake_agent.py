from rdkit import Chem
from rdkit.Chem.SaltRemover import SaltRemover

class IntakeAgent:
    def __init__(self):
        self.remover = SaltRemover()

    def process(self, smiles_list):
        """Processes a list of SMILES strings, returning standardized canonical SMILES."""
        valid_compounds = []
        errors = []
        seen = set()

        for idx, sm in enumerate(smiles_list):
            mol = Chem.MolFromSmiles(sm)
            if mol is None:
                errors.append({"index": idx, "smiles": sm, "error": "Invalid SMILES"})
                continue
            
            # Remove salts
            mol = self.remover.StripMol(mol, dontRemoveEverything=True)
            
            # Standardize to canonical SMILES
            canonical_smiles = Chem.MolToSmiles(mol, isomericSmiles=True)
            
            # Deduplicate
            if canonical_smiles in seen:
                continue
                
            seen.add(canonical_smiles)
            valid_compounds.append({"smiles": canonical_smiles, "mol_obj": mol})
            
        return valid_compounds, errors
