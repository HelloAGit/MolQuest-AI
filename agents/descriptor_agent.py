from rdkit.Chem import Descriptors, rdMolDescriptors

class DescriptorAgent:
    def process(self, compounds):
        for comp in compounds:
            mol = comp["mol_obj"]
            
            # Calculate base descriptors
            mw = Descriptors.MolWt(mol)
            logp = Descriptors.MolLogP(mol)
            hbd = rdMolDescriptors.CalcNumLipinskiHDonors(mol)
            hba = rdMolDescriptors.CalcNumLipinskiHAcceptors(mol)
            tpsa = Descriptors.TPSA(mol)
            rotb = rdMolDescriptors.CalcNumRotatableBonds(mol)
            
            # Lipinski & Veber Filters
            lipinski_violations = sum([mw > 500, logp > 5, hbd > 5, hba > 10])
            veber_pass = (tpsa <= 140) and (rotb <= 10)
            
            comp["descriptors"] = {
                "MW": mw,
                "LogP": logp,
                "HBD": hbd,
                "HBA": hba,
                "TPSA": tpsa,
                "RotatableBonds": rotb
            }
            comp["drug_likeness"] = {
                "Lipinski_Violations": lipinski_violations,
                "Veber_Pass": veber_pass,
                "Status": "Pass" if (lipinski_violations <= 1 and veber_pass) else "Fail"
            }
        return compounds
