import re
phone= "+553 838-1525"
phone = re.sub(r"[a-zA-Z . +-]+", "" ,phone)

print(phone)