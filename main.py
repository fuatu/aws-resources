"""
Get all EC2s from all l_regions and export details as a csv file
"""
from collections import defaultdict
import boto3
import yaml


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
    """
    get aws l_session
    """
    filename = 'credentials.yaml'
    file_details = read_yaml(filename=filename)
    l_region = file_details['credentials']['default_region']

    l_session = boto3.Session(
        aws_access_key_id=file_details['credentials']['access_key'],
        aws_secret_access_key=file_details['credentials']['secret_key'],
        region_name=l_region,
    )
    return l_session


def get_regions(l_session: boto3.session):
    """
    get all aws l_regions
    """
    ec2 = l_session.client('ec2')
    response = ec2.describe_regions()
    l_regions = None
    if 'Regions' in response:
        l_regions = [x['RegionName'] for x in response['Regions']]
    return l_regions


def get_instance_type_memory(l_session: boto3.session, instance_type: str):
    """
    get memory of the instance type in MBs
    """
    memory = 0
    instance_types = l_session.client('ec2').describe_instance_types(InstanceTypes=[instance_type])
    if 'InstanceTypes' in instance_types:
        memory = instance_types['InstanceTypes'][0]['MemoryInfo']['SizeInMiB']
    return memory


def get_ec2(l_session: boto3.session, l_regions: []):
    """
    get all ec2s from all regions
    """
    l_ec2s = []
    for region in l_regions:
        ec2 = l_session.resource('ec2', region_name=region)
        print("Checking region: {}".format(region))
        for instance in ec2.instances.all():
            line = defaultdict(lambda: "")
            line['id'] = instance.id
            line['instance_type'] = instance.instance_type
            line['cpus'] = instance.cpu_options['CoreCount'] * \
                instance.cpu_options['ThreadsPerCore']
            line['memory'] = get_instance_type_memory(l_session, line['instance_type'])
            size = 0
            for volume in instance.volumes.all():
                size += volume.size
            line['storage'] = size
            try:
                line['platform'] = instance.image.platform_details
                line['image_description'] = instance.image.description
            except:
                pass

            line['state'] = instance.state['Name']
            line['region'] = region
            l_ec2s.append(line)
    return l_ec2s


def write_to_csv(l_ec2s: []):
    """
    write ec2 details to csv file
    """
    l_file = open("ec2s.csv", "w")
    l_header = "id,instance_type,cpus,memory_MBs,storage_GBs,"
    l_header += "platform,image_description,state,region\n"
    l_file.write(l_header)
    for ec2 in l_ec2s:
        line = '{},{},{},{},{},{},{},{},{}\n'.format(
            ec2['id'], ec2['instance_type'], ec2['cpus'], ec2['memory'],
            ec2['storage'], ec2['platform'],
            ec2['image_description'], ec2['state'], ec2['region'])
        l_file.write(line)
    l_file.close()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    session = get_session()
    regions = get_regions(session)
    ec2s = get_ec2(session, regions)
    print('Completed')
    write_to_csv(ec2s)
