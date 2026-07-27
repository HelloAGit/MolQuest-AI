import numpy as np

class ReportAgent:
    def _pareto_rank(self, compounds):
        """Simple Non-Dominated Sorting for Pareto Ranking"""
        # We want to MINIMIZE Toxicity, MINIMIZE Lipinski Violations, MAXIMIZE Similarity
        # Convert to a cost matrix where lower is better
        costs = []
        for c in compounds:
            tox = c["admet"]["Toxicity_Risk"]
            lip = c["drug_likeness"]["Lipinski_Violations"]
            sim = 1.0 - c["similarity"].get("Max_Tanimoto", 0) # 1 - sim so lower is better
            costs.append([tox, lip, sim])
            
        costs = np.array(costs)
        ranks = np.zeros(len(costs), dtype=int)
        
        # O(N^2) naive pareto ranking for demonstration
        for i, c_i in enumerate(costs):
            for j, c_j in enumerate(costs):
                if i == j:
                    continue
                # If j dominates i (j is strictly better or equal in all, better in at least one)
                if np.all(c_j <= c_i) and np.any(c_j < c_i):
                    ranks[i] += 1 
                    
        for idx, comp in enumerate(compounds):
            comp["Pareto_Rank"] = int(ranks[idx])
            
        # Sort by rank
        compounds.sort(key=lambda x: x["Pareto_Rank"])
        return compounds

    def generate_report(self, compounds, errors):
        ranked_compounds = self._pareto_rank(compounds)
        
        report = {
            "Summary": {
                "Total_Submitted": len(compounds) + len(errors),
                "Valid_Processed": len(compounds),
                "Failed_Intake": len(errors)
            },
            "Ranked_Candidates": [],
            "Errors": errors
        }
        
        for c in ranked_compounds:
            report["Ranked_Candidates"].append({
                "SMILES": c["smiles"],
                "Pareto_Rank": c["Pareto_Rank"],
                "Drug_Likeness": c["drug_likeness"],
                "ADMET_Profile": c["admet"],
                "Literature_Evidence": c["evidence"]
            })
            
        return report
