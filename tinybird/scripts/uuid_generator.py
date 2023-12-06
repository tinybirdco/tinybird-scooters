from uuid import uuid4

def generate_uuids(file_path):
    uuids = set()
    while len(uuids) < 5000:
        uuids.add(uuid4())

    with open(file_path, 'w') as file:
        for uuid in uuids:
            file.write(str(uuid) + '\n')

generate_uuids('uuids.txt')