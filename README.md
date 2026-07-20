# AirVT-15k Project Page

This directory contains the GitHub Pages project site for AirVT-15k.

## Contents

```text
AirVT-15k-site/
├── index.html                         # Project homepage
├── assets/
│   ├── demos/                         # Compressed curated demo videos for visualization
│   ├── posters/                       # Poster images for the curated demos
│   └── figures/                       # Optional figures
├── downloads/
│   ├── evaluation/                    # Evaluation script and submission examples
│   ├── splits/                        # Train/val/test split id files
│   └── split_summary.json             # Split statistics
├── samples/
│   └── annotation_sample.json          # One annotation example
├── CITATION.cff                       # Citation metadata
├── LICENSE.md                         # License information
└── README.md                          # This file
```

## Local Server

```bash
cd /data/chenxi/rs-video/AirVT-15k-site
python3 -m http.server 8000
```

Then open:

```text
http://localhost:8000
```

## GitHub Pages Deployment

1. Create a GitHub repository, for example `AirVT-15k-site`.
2. Push the contents of this directory to the repository.
3. In GitHub, open `Settings -> Pages`.
4. Set `Build and deployment` to `Deploy from a branch`.
5. Select branch `main` and folder `/root`.
6. Update `index.html` after the repository URL, paper URL, full dataset URL, and license are finalized.

## Data Hosting

The homepage organizes curated demo cards into three showcase rows:

- Multi-scenario coverage
- Application-oriented design
- Diverse event semantics

The complete videos and annotations can be linked from the project page after the public release channel is finalized.
