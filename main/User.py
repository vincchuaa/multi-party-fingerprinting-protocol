import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
import numpy as np
import random

# This class represent a user in a group messaging setting
class User:
  FIXED_KEY_SIZE = 32
  FIXED_SALT_SIZE = 16
  
  def __init__(self,id,identifier,identityKey,fingerprint):
    self.id = id
    self.identifier = identifier
    self.identityKey = identityKey
    self.fingerprint = fingerprint

  # Generates a random ID where in this instance ID denotes a 10 digit phone number
  def generate_ID(self):
    self.id = [random.randint(0,9) for _ in range(10)]
    
  # Generates an identifier for a user using their id
  def generate_identifier(self,length,info):
    salt = bytes(info)
    hkdf = HKDF(algorithm=hashes.SHA256(),length=length,salt=salt,info=None)
    self.identifier = hkdf.derive(bytearray(self.id))
  
  # Generates a fingerprint by hashing user's credentials over number of iterations
  def generate_fingerprint(self):
    hash = self.identifier + self.identityKey
    digest = hashes.Hash(hashes.SHA512())
    for i in range(7200):
      digest.update(hash)
    self.fingerprint = digest.finalize()
  
  # Helper function to initialize a user
  def user_init(self):
    self.generate_ID()
    self.generate_identifier(User.FIXED_KEY_SIZE, self.id)
    self.identityKey = os.urandom(32)
    self.generate_fingerprint()
