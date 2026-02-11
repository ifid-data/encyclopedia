# Encyclopedia of Indian Food Ingredients (v0.1.0)
## As part of Indian Food ID Project

**DOI:** [10.13140/RG.2.2.27821.55529](https://doi.org/10.13140/RG.2.2.27821.55529)

**Documentation:** [ifid.readthedocs.io](https://ifid.readthedocs.io/en/latest/)

**Updates:** [ifid.substack.com](https://ifid.substack.com)

---

## Overview

The Encyclopedia of Indian Food Ingredients is a core component of the **Indian Food Informatics Data (IFID)** project. It provides a standardized taxonomy and high-density metadata for over 600 food components found within the Indian ecosystem.

This repository bridges the gap between traditional Indian culinary knowledge, Ayurvedic botanicals, and modern industrial FMCG standards. By providing machine-readable formats (JSON and Markdown), IFID serves as a foundational layer for food-tech applications, nutritional AI, and academic research.

## Structure
```json
{
  "metadata": {
    "title": "Encyclopedia of Indian Food Ingredients",
    "project": "Indian Food Informatics Data (IFID)",
    "version": "0.1.0-alpha",
    "release_date": "2026-02-11",
    "doi": "https://doi.org/10.13140/RG.2.2.27821.55529",
    "license": "Open Data Commons Attribution License (ODC-By)",
    "author": "Lalitha A R",
    "institution": "Interdisciplinary Systems Research Lab",
    "documentation": "https://ifid.readthedocs.io/en/latest/",
    "journal": "https://ifid.substack.com",
    "contact": "https://ifid.substack.com/about",
    "description": "A standardized taxonomy of 600+ food components..."
  },
  "statistics": {
    "total_categories": 8,
    "total_ingredients": 661
  },
  "data": {
    "Additives & Functional": {
      "2'-Fucosyllactose": {
        "slug": "2'-fucosyllactose",
        "json": {
          "ingredient_name": "2'-Fucosyllactose",
          "category": "Additives & Functional",
          "keywords": ["2'-FL", "HMO", "Prebiotic"]
        }
      }
    }
  }
}
```

## Key Features

* **Standardized Taxonomy:** Normalized nomenclature for 661+ ingredients across various categories.
* **Multi-Format Distribution:** Available in JSON (for developers), Markdown (for RAG/LLM applications), and LaTeX (for academic publishing).
* **Cross-Referenced Metadata:** Data points include historical sourcing, traditional culinary usage, industrial applications, and common consumer distinctions.
* **Graph-Ready:** Features over 4,000 internal links between ingredients to support knowledge graph construction.

## Project Status: v0.1.0 (Alpha)

This is the inaugural "Alpha" release. As part of our commitment to the **Release Early, Iterate Often** philosophy of public digital goods, this version focuses on establishing a baseline nomenclature.

Users should note:

1. This version is a work-in-progress and may contain errors or omissions.
2. Subsequent versions (v0.2.0+) will introduce formalized contribution templates for community-driven refinement.

## Usage for AI and LLM Developers

This dataset is specifically structured for **Retrieval-Augmented Generation (RAG)** and **Knowledge Graph** development.

* **JSON Master:** Located in `/data/ifid_encyclopedia_v010.json`, this file includes a root metadata block and a flattened ingredient dictionary for easy parsing.
* **Markdown Files:** Individual ingredient files are optimized for vector database ingestion, providing clear headings that LLMs can use for precise context retrieval.

## Citation

If you use this dataset in your research or applications, please cite it as follows:

### APA 7th Edition
```
Lalitha, A. R. (2026). Encyclopedia of Indian Food Ingredients (v0.1.0): A Standardized Taxonomy for Indian Food Informatics. Interdisciplinary Systems Research Lab. [https://doi.org/10.13140/RG.2.2.27821.55529](https://doi.org/10.13140/RG.2.2.27821.55529)
```

### BibTeX

```bibtex
@misc{Lalitha2026IFID,
  author       = {Lalitha, A. R.},
  title        = {Encyclopedia of Indian Food Ingredients (v0.1.0)},
  year         = {2026},
  publisher    = {Interdisciplinary Systems Research Lab},
  doi          = {10.13140/RG.2.2.27821.55529},
  url          = {https://doi.org/10.13140/RG.2.2.27821.55529}
}

```

## License

This dataset is made available under the **Open Data Commons Attribution License (ODC-By)**. You are free to share, create, and adapt the data, provided that you maintain attribution to the original author and the IFID project.

## Contact and Contributions

The IFID project is maintained by the **Interdisciplinary Systems Research Lab (ISRL)**.

* **Substack:** [ifid.substack.com](https://ifid.substack.com) for methodological updates.
* **Issues:** Please use the GitHub issue tracker to report errors or suggest taxonomic refinements.
