## This is a project for Machine Learning in the City - group 1

### members: Henry Lin, Ian Wright and Claire Haung

Breif introduction from the slides:
[presentation file](https://docs.google.com/presentation/d/13e1Vv3CQgJleHh3dKkhnSlQrbPs8xMHEBZC0rHEMYj8/edit?usp=sharing)


#### Structure of the repo

 
``  .  
├── data
│   ├── 311_complaint.csv
│   ├── clean_bz.csv
│   ├── spatial_merged_2.csv
│   ├── spatial_merged_3_fs_features.csv
│   ├── spatial_merged.csv
│   ├── spatial_merged_solid.csv
│   ├── topic_output.csv
│   ├── uniq_biz_fs.csv
│   ├── uniq_biz_with_gg.csv
│   └── uniq_biz_yelp_geo.csv
├── figs
│   ├── Decision Tree ROC curve.png
│   ├── GaussianNB ROC curve.png
│   ├── Random Forest ROC curve.png
│   └── SVM ROC curve.png
├── notebooks
│   ├── 311_scrape.ipynb
│   ├── basic_intro.ipynb
│   ├── Data Exploratory Analysis - restaurant categories.ipynb
│   ├── dbscan.ipynb
│   ├── decision_tree.ipynb
│   ├── logit_reg.ipynb
│   ├── p-value and classifiers.ipynb
│   ├── sjoin.ipynb
│   ├── spatial join with pluto data.ipynb
│   ├── visuals.ipynb
│   └── yelp_data.ipynb
├── README.md
└── src
    ├── foursquare_data.py
    ├── fs_data_lat_lon.py
    ├── fs_ETL.py
    ├── get_name.py
    ├── keys.py
    ├── open311SNSL.py
    ├── read_file.py
    ├── test.py
    └── util.py
``    
    
#### Data source:

Foursquare API

Google Place API

Open NYC