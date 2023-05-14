import sys
sys.path.insert(0, 'main')
import timeit
import csv

from Group import *
from Fingerprint import *

#Benchmark tests
with open('benchmarking.csv', mode='w') as file:
  writer = csv.writer(file)
  
  #Benchmarking on fingerprint computation time
  group1 = Group(groupName="test",groupSize=0,users=[],usersFingerprints=[],groupFingerprint=None)
  group1.generate_group(10)
  fingerprint_time = timeit.timeit(group1.generate_group_fingerprint,number=10000)
  writer.writerow(['Fingerprint computation time for 10 users', fingerprint_time])
  
  group1 = Group(groupName="test",groupSize=0,users=[],usersFingerprints=[],groupFingerprint=None)
  group1.generate_group(100)
  fingerprint_time = timeit.timeit(group1.generate_group_fingerprint,number=10000)
  writer.writerow(['Fingerprint computation time for 100 users', fingerprint_time])

  group1 = Group(groupName="test",groupSize=0,users=[],usersFingerprints=[],groupFingerprint=None)
  group1.generate_group(200)
  fingerprint_time = timeit.timeit(group1.generate_group_fingerprint,number=10000)
  writer.writerow(['Fingerprint computation time for 200 users', fingerprint_time])

  group1 = Group(groupName="test",groupSize=0,users=[],usersFingerprints=[],groupFingerprint=None)
  group1.generate_group(256)
  fingerprint_time = timeit.timeit(group1.generate_group_fingerprint,number=10000)
  writer.writerow(['Fingerprint computation time for 256 users', fingerprint_time])

  #Pushing the limit of group size 
  group1 = Group(groupName="test",groupSize=0,users=[],usersFingerprints=[],groupFingerprint=None)
  group1.generate_group(512)
  fingerprint_time = timeit.timeit(group1.generate_group_fingerprint,number=10000)
  writer.writerow(['Fingerprint computation time for 512 users', fingerprint_time])

  #Pushing the limit of group size
  group1 = Group(groupName="test",groupSize=0,users=[],usersFingerprints=[],groupFingerprint=None)
  group1.generate_group(1024)
  fingerprint_time = timeit.timeit(group1.generate_group_fingerprint,number=10000)
  writer.writerow(['Fingerprint computation time for 1024 users', fingerprint_time])

  #Benchmarking on fingerprint storage
  group2 = Group(groupName="test",groupSize=0,users=[],usersFingerprints=[],groupFingerprint=None)
  group2.generate_group(10)
  group2.generate_group_fingerprint()
  writer.writerow(['Size of group fingerprint in a group of 10 users', len(group2.groupFingerprint)])

  group3 = Group(groupName="test",groupSize=0,users=[],usersFingerprints=[],groupFingerprint=None)
  group3.generate_group(1024)
  group3.generate_group_fingerprint()

  #Example user data
  user1 = User(id= [1, 0, 2, 6, 6, 2, 1, 7, 9, 5],
              identifier=b'\x98\xf2\x1e\x9c\x9fEE~\x84\x87\x16\x81\x82\x16\n|\x8a\x10\xd9PP\x0cr\x10\x9a\xf5\x04Db\xa4\x7f\x92',
              identityKey= b'p\xa7\xc4\xaff(\xd3\xf5\xf7\x90\xd0\xe26\xc1\xe5go{If\x062\x84\x97\x1b\xde&\xd3\x8d\x87\n\xcc',
              fingerprint= b'\xf0t\xd9\xf5\xc7\x8fA\x9f^7a\x816\xfc\x85\xb6\xc0;\xc4\xb6\xb9O\xeaB\xb0\xcb\n\x86\x13\xaf0\x02\xe4\xa5p\xfc\xe70\x08\x8f\xa6\xbf\xbc8hV\x8c\xf7\x9f\x1e~i\x14\xed\xff+?\x0b\xb8\x8b\xf1\xad\n\xe7')

  #Benchmarking on recomputation of fingerprint due to adding members
  code = """group2.add_user(user1)
group2.generate_group_fingerprint()"""
  adding_member_time = timeit.timeit(code, globals=globals(),number=10000)
  writer.writerow(['Fingerprint recomputation time for adding members in a group of 10 ', adding_member_time])

  code = """group3.add_user(user1)
group3.generate_group_fingerprint()"""
  adding_member_time = timeit.timeit(code, globals=globals(),number=10000)
  writer.writerow(['Fingerprint recomputation time for adding members in a group of 1024 ', adding_member_time])

  #Benchmarking on recomputation of fingerprint due to removing members
  code = """group2.remove_user(user1)
group2.generate_group_fingerprint()"""
  removing_member_time = timeit.timeit(code, globals=globals(),number=10000)
  writer.writerow(['Fingerprint recomputation time for removing members in a group of 10 ', removing_member_time]) 

  code = """group3.remove_user(user1)
group3.generate_group_fingerprint()"""
  removing_member_time = timeit.timeit(code, globals=globals(),number=10000)
  writer.writerow(['Fingerprint recomputation time for removing members in a group of 1024 ', removing_member_time]) 


  #Benchmarking on time taken to construct QR Code
  group4 = Group(groupName="test",groupSize=0,users=[],usersFingerprints=[],groupFingerprint=None)
  group4.generate_group(10)

  qrcode_time = timeit.timeit(lambda: Fingerprint.create_scannable_fingerprint(group4),number=10000)
  writer.writerow(['QR-Code computation time: ', qrcode_time])