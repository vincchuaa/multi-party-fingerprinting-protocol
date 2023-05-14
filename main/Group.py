from User import *
from FingerprintUtil import *
from Fingerprint import *
import numpy as np
import ast 

#This class represents a group in a group messaging setting.
class Group:
  def __init__(self,groupName,groupSize,users,usersFingerprints,groupFingerprint):
    if groupSize !=len(users):
      raise ValueError("Group size must be equivalent to the number of users")
    self.groupName = groupName
    self.groupSize = groupSize
    self.users = users
    self.usersFingerprints = usersFingerprints
    self.groupFingerprint = groupFingerprint

  # Create a group of users and initialize them with info
  def generate_group(self, number_of_users):
    self.groupSize = number_of_users
    for x in range(number_of_users):
      user = User(id = None, identifier = None, identityKey = None, fingerprint = None)
      user.generate_ID()
      user.generate_identifier(length=User.FIXED_KEY_SIZE,info=user.id)
      user.identityKey = os.urandom(User.FIXED_KEY_SIZE)
      user.generate_fingerprint()
      self.users = np.concatenate((self.users,[user]),axis=None)
      self.usersFingerprints = np.concatenate((self.usersFingerprints,[user.fingerprint]),axis=None)

  # Generates a group fingerprint
  def generate_group_fingerprint(self):
    sortedGroupFingerprint = sorted(self.usersFingerprints, key=lambda x: int.from_bytes(x, 'big'))
    self.groupFingerprint = b''.join(sortedGroupFingerprint)
  
  # Add a user to the group
  def add_user(self, user):
    self.groupSize = self.groupSize+1
    self.users = np.append(self.users,user)
    self.usersFingerprints = np.append(self.usersFingerprints,user.fingerprint)
    
  # Remove a user from the group
  def remove_user(self, user):
    self.groupSize = self.groupSize-1
    #Remove relevant user and user fingerprint into the group object
    self.users = np.array(self.users)
    self.users = self.users[~np.isin(self.users, user)]
    self.usersFingerprints = self.usersFingerprints[~np.isin(self.usersFingerprints, user.fingerprint)]
    
  # Adding users 
  def add_users(self, users):
    self.groupSize = self.groupSize+len(users)
    self.users = np.concatenate((self.users,users),axis=None)
    for user in users: 
      self.usersFingerprints = np.concatenate((self.usersFingerprints,[user.fingerprint]),axis=None)
      
  # Removing users
  def remove_users(self, users):
    self.groupSize = self.groupSize-len(users)
    self.users = np.array(self.users)
    self.users = self.users[~np.isin(self.users, users)]
    for user in users:
      self.usersFingerprints = np.setdiff1d(self.usersFingerprints, user.fingerprint)
    
  def qrcode_verification(self,fileName):
    local_fp = self.groupFingerprint
    remote_fp = ast.literal_eval(Fingerprint.retrieve_scannable_fingerprint(fileName))
    status = FingerprintUtil.compare_group_fingerprint(local_fp, remote_fp)
    if status:
      print("QR Code Status: Group verified!")
    else:
      print("QR Code Status: Warning, the security code has been changed!")
