## Usage
```
python s3_file_table.py list --s3_metadata --format=tsv | csvsort -c expdate,expmoniker | csvcut -c a,qqfilename | csvlook
```

```
python s3_file_table.py upload --bucket=cytovas-batch-titration-configs --file=config.yaml
```