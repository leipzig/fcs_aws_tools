## Setup
```
conda create -n aws_tools_env --file conda_requirements.txt
source activate aws_tools_env
python setup.py install
```

## Usage

```
aws_tools list --s3_metadata --format=tsv | csvsort -c expdate,expmoniker | csvcut -c a,qqfilename | csvlook
```

```
aws_tools upload --bucket=cytovas-batch-titration-configs --file=config.yaml
```