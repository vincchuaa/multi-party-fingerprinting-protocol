from Group import *
from pyzbar.pyzbar import decode
from PIL import Image
from FingerprintUtil import *

import qrcode

#This class is for constructing the fingerprint verification representations.
class Fingerprint:
  
  def create_scannable_fingerprint(group):
    qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
    )
    
    qr.add_data(str(group.groupFingerprint))
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(group.groupName + ".png")
    
  def retrieve_scannable_fingerprint(fileName):
    image = Image.open(fileName)
    decoded_data = decode(image)
    for data in decoded_data:
        # Extract the decoded data as a string
        decoded_data_str = data.data.decode('utf-8')
    return decoded_data_str

  def create_comparable_fingerprint(hash1, hash2):
    status = FingerprintUtil.compare_group_fingerprint(hash1,hash2) 
    if not status:
      return "The security code has changed."
    else:
      byte_list1 = [bytes([byte]) for byte in hash1]
      byte_list2 = [bytes([byte]) for byte in hash2]
      common_bytes = np.intersect1d(byte_list1,byte_list2)
      fingerprint = b''.join(common_bytes)
      return (Fingerprint.get_encoded_chunk(fingerprint, 0) + " " +
            Fingerprint.get_encoded_chunk(fingerprint, 5) + " " +
              Fingerprint.get_encoded_chunk(fingerprint, 10) + " " +
              Fingerprint.get_encoded_chunk(fingerprint, 15) + " " +
              Fingerprint.get_encoded_chunk(fingerprint, 20) + " " +
              Fingerprint.get_encoded_chunk(fingerprint, 25))
    
  def byte_to_long(bytes, offset):
    return ((bytes[offset]     & 0xff) << 32) | \
           ((bytes[offset + 1] & 0xff) << 24) | \
           ((bytes[offset + 2] & 0xff) << 16) | \
           ((bytes[offset + 3] & 0xff) << 8)  | \
           ((bytes[offset + 4] & 0xff))
  
  def get_encoded_chunk(fingerprint, offset):
    chunk = Fingerprint.byte_to_long(fingerprint, offset) % 100000
    return "{:05d}".format(chunk)
  