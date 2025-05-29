This project allows users to input molecular data using a ChEMBL ID. You can obtain this ID by entering the molecular formula into PubChem, which will return the corresponding identifier.

The model predicts pIC50, the negative logarithm (base 10) of the IC50 value measured in micromolar concentration (log₁₀(IC50 in µM)). This logarithmic transformation was applied to enhance the interpretability and comparability of the results.

At the outset, we deliberated between using Lipinski or PubChem descriptors, ultimately choosing the latter for its structural richness. We then translated the molecular structure into machine-readable numerical data, allowing the model to process and learn from molecular patterns.

Each PubChemFP# represents a specific chemical substructure. For a given molecule, each descriptor is encoded as either 1 or 0, indicating the presence or absence of that substructure.

Initially, the dataset contained 882 molecular descriptors. Through feature selection, we refined the input to 218 of the most informative descriptors, thereby improving model performance and interpretability.
