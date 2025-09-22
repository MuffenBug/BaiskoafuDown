# Baiskoafu loagin details
username = "" # <- Enter your email address
password = "" # <- Enter your password

def media_quality(quality='high'):

    q = ['high', 'medium', 'low']  # Reordered with high first

    if quality == q[0]: return q[0]  # high
    if quality == q[1]: return q[1]  # medium  
    if quality == q[2]: return q[2]  # low
    return q[0] # < --- default is now high (highest available)

media_quality('high')  # Force highest quality
ASK_BEFORE_DOWNLOAD = False	# set 'False' for automatic download
IS_PRIMARY_DEVICE   = False	# set 'True' only if you have premium subscription
