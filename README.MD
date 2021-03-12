# AWS Resources

Get all EC2 instances details from all AWS regions in a csv file.

## Prerequisites
Python 3.x installed

## Installation and running the script
- clone the repo or download it
- go inside the folder
- install required packages
- copy credentails.yaml.example to credentails.yaml
- you need an AWS user with programmatic access, relevant permissions to read ec2 instance details. The user keys
- Update credentails.yaml with your aws key and secret
- run the script
- the ec2 details from all regions will be written to file ec2s.csv in the same folder

## install requirements
```
$ pip install -r requirements.txt
```

## run script
```
$ python main.py
```

## Sample CSV file content
|id                 |instance_type|cpus|memory_MBs|storage_GBs|platform  |image_description     |state  |region   |
|-------------------|-------------|----|----------|-----------|----------|----------------------|-------|---------|
|i-0dxxxxxxxxxxxxx  |t4g.micro    |2   |1024      |14         |Linux/UNIX|Fedora AMI Description|stopped|eu-west-1|
|i-00xxxxxxxxxxxxx  |t4g.micro    |2   |1024      |14         |Linux/UNIX|Fedora AMI Description|stopped|eu-west-1|
|i-05xxxxxxxxxxxxx  |t4g.micro    |2   |1024      |14         |Linux/UNIX|Fedora AMI Description|stopped|eu-west-1|
|i-0exxxxxxxxxxxxx  |t4g.micro    |2   |1024      |14         |Linux/UNIX|Fedora AMI Description|stopped|eu-west-1|

