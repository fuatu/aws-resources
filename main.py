# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import boto3
import yaml
from collections import defaultdict

def read_yaml(filename=None):
    """ read yaml file """
    try:
        stream = open(filename, 'r')
        file_details = yaml.safe_load(stream)
    except (yaml.YAMLError, FileNotFoundError):
        print("Not yaml file...")
        return None
    return file_details

def get_session():
    filename = 'credentials.yaml'
    file_details = read_yaml(filename=filename)
    l_region = file_details['credentials']['default_region']

    session = boto3.Session(
        aws_access_key_id=file_details['credentials']['access_key'],
        aws_secret_access_key=file_details['credentials']['secret_key'],
        region_name=l_region,
    )
    return session

def get_regions(session: boto3.session):
    ec2 = session.client('ec2')
    response = ec2.describe_regions()
    regions = None
    if 'Regions' in response:
        regions = [x['RegionName'] for x in response['Regions']]
    return regions

def get_instance_type_memory(session: boto3.session, instance_type: str):
    instance_types = session.client('ec2').describe_instance_types(InstanceTypes=[instance_type])
    if 'InstanceTypes' in instance_types:
        memory = instance_types['InstanceTypes'][0]['MemoryInfo']['SizeInMiB']
    return memory


def get_ec2(session: boto3.session, regions: []):
    ec2s = []
    for r in regions:
        ec2 = session.resource('ec2', region_name=r)
        print("Checking region: {}".format(r))
        for instance in ec2.instances.all():
            line = defaultdict(lambda: "")
            line['id'] = instance.id
            line['instance_type'] = instance.instance_type
            line['cpus'] = instance.cpu_options['CoreCount'] * instance.cpu_options['ThreadsPerCore']
            line['memory'] = get_instance_type_memory(session, line['instance_type'])
            size = 0
            for v in instance.volumes.all():
                size += v.size
            line['storage'] = size
            line['platform'] = instance.image.platform_details
            line['image_description'] = instance.image.description
            line['region'] = r
            ec2s.append(line)
    return ec2s

def write_to_csv(ec2s: []):
    f = open("ec2s.csv", "w")
    f.write("id,instance_type,cpus,memory,storage,platform,image_description,region\n")
    for e in ec2s:
        line = '{},{},{},{},{},{},{},{}\n'.format(
            e['id'], e['instance_type'], e['cpus'], e['memory'], e['storage'], e['platform'], e['image_description'], e['region'])
        f.write(line)
    f.close()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    session = get_session()
    regions = get_regions(session)
    ec2s = get_ec2(session, regions)
    print('Completed')
    write_to_csv(ec2s)

