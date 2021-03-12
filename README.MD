# AWS Resources

Get all EC2 instances details from all regions in csv file

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


