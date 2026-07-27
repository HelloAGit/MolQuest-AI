import json
from agents.intake_agent import IntakeAgent
from agents.descriptor_agent import DescriptorAgent
from agents.admet_agent import ADMETAgent
from agents.similarity_agent import SimilarityAgent
from agents.evidence_agent import EvidenceAgent
from agents.report_agent import ReportAgent

def main():
    # 1. Initialize Agents
    print("Initializing Agents...")
    intake = IntakeAgent()
    descriptor = DescriptorAgent()
    admet = ADMETAgent()
    # Provide a known drug for similarity benchmarking (e.g., Aspirin)
    similarity = SimilarityAgent(reference_smiles_list=["CC(=O)OC1=CC=CC=C1C(=O)O"]) 
    evidence = EvidenceAgent()
    report = ReportAgent()

    # 2. Input Data (Raw SMILES, some valid, some invalid, some dirty)
    raw_smiles = [
        "CC(=O)OC1=CC=CC=C1C(=O)O.[Na+]",  # Aspirin Sodium Salt (needs desalting)
        "CN1C=NC2=C1C(=O)N(C(=O)N2C)C",    # Caffeine
        "INVALID_SMILES_STRING",           # Will fail intake
        "CC1=C(C=C(C=C1)NC(=O)C2=CC=C(C=C2)CN3CCN(CC3)C)NC4=NC=CC(=N4)C5=CN=CC=C5" # Imatinib
    ]

    # 3. Execute Pipeline
    print("Running Intake Agent...")
    compounds, errors = intake.process(raw_smiles)

    print("Running Descriptor Agent...")
    compounds = descriptor.process(compounds)

    print("Running ADMET Agent...")
    compounds = admet.process(compounds)

    print("Running Similarity Agent...")
    compounds = similarity.process(compounds)

    print("Running Evidence Agent...")
    compounds = evidence.process(compounds)

    print("Running Report Agent...")
    final_report = report.generate_report(compounds, errors)

    # 4. Output Results
    print("\n=== FINAL DRUG SCREENING REPORT ===")
    print(json.dumps(final_report, indent=4))

if __name__ == "__main__":
    main()
