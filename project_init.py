import os

def create_file_if_not_exists(path):
    if not os.path.exists(path):
        open(path, 'a').close()
        print(f'File created: {path}')
    else:
        print(f'File already exists: {path}')

####################################
##      Environment Structure     ##
####################################

FOLDER_LIST = [
    'airflow',
    'conf',
    'datanode',
    'historyserver',
    'namenode',
    'nodemanager',
    'resourcemanager',
    'spark',
]

FILE_LIST = [
    'Dockerfile',
    'docker-compose.yml',
    'start-cluster.sh'
]

CURRENT_DIRECOTRY = os.getcwd()


for folder in FOLDER_LIST:
    if not os.path.exists(os.path.join(CURRENT_DIRECOTRY, folder)):
        os.mkdir(os.path.join(CURRENT_DIRECOTRY, folder))
        print(f'Folder created: {os.path.join(CURRENT_DIRECOTRY, folder)}')
    else:
        print(f'Folder already exists: {os.path.join(CURRENT_DIRECOTRY, folder)}')

for file in FILE_LIST:
    create_file_if_not_exists(os.path.join(CURRENT_DIRECOTRY, file))


#########################
##      Name Node      ##
#########################

NAMENODE_DIR = os.path.join(CURRENT_DIRECOTRY, 'namenode')

if os.path.exists(NAMENODE_DIR):
    # Create Dockerfile
    NAMENODE_FILE_LIST = [
        'Dockerfile',
        'run.sh'
    ]
    
    for file in NAMENODE_FILE_LIST:
        create_file_if_not_exists(os.path.join(CURRENT_DIRECOTRY, file))
else:
    print(f'Folder not present: {os.path.join(CURRENT_DIRECOTRY, file)}')


#########################
##      Data Node      ##
#########################

DATANODE_DIR = os.path.join(CURRENT_DIRECOTRY, 'datanode')

if os.path.exists(DATANODE_DIR):
    # Create Dockerfile
    DATANODE_FILE_LIST = [
        'Dockerfile',
        'run.sh'
    ]
    
    for file in DATANODE_FILE_LIST:
        create_file_if_not_exists(os.path.join(CURRENT_DIRECOTRY, file))
else:
    print(f'Folder not present: {os.path.join(DATANODE_DIR, file)}')


#############################
##      Histry Server      ##
#############################

HISTORYSERVER_DIR = os.path.join(CURRENT_DIRECOTRY, 'historyserver')

if os.path.exists(DATANODE_DIR):
    # Create Dockerfile
    HISTORYSERVERE_FILE_LIST = [
        'Dockerfile',
        'run.sh'
    ]
    
    for file in HISTORYSERVERE_FILE_LIST:
        create_file_if_not_exists(os.path.join(CURRENT_DIRECOTRY, file))
else:
    print(f'Folder not present: {os.path.join(HISTORYSERVER_DIR, file)}')



