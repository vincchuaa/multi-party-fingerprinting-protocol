#This class is for fingerprinting comparison and authentication
class FingerprintUtil:
  
  #Basic byte sequences comparison
  def compare_group_fingerprint(fp1,fp2):
    if fp1 == fp2:
      return True
    if (fp1 in fp2) or (fp2 in fp1):
      return True
    
    byte_list1 = [bytes([fp1[i]]) for i in range(len(fp1))]
    byte_list2 = [bytes([fp2[i]]) for i in range(len(fp2))]

    if set(byte_list1).issubset(set(byte_list2)) or set(byte_list2).issubset(set(byte_list1)):
      return True
    
    return False
  
  def compare_identifiers(group1,group2):
    ids1 = [user.identifier for user in group1.users]
    ids2 = [user.identifier for user in group2.users]
    
    sorted_ids1 = sorted(ids1, key=lambda x: int.from_bytes(x, 'big'))
    sorted_ids2 = sorted(ids2, key=lambda x: int.from_bytes(x, 'big'))
    
    if sorted_ids1 == sorted_ids2:
      return True
    return False
  
  def compare_identity_keys(group1,group2):
    idks1 = [user.identityKey for user in group1.users]
    idks2 = [user.identityKey for user in group2.users]
    
    sorted_idks1 = sorted(idks1, key=lambda x: int.from_bytes(x, 'big'))
    sorted_idks2 = sorted(idks2, key=lambda x: int.from_bytes(x, 'big'))
    
    if sorted_idks1 == sorted_idks2:
      return True
    return False
