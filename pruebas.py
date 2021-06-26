from hashlib import blake2b
h = blake2b(key=b'pseudorandom key', digest_size=16)
a = 'perro'
d = '¡moa'
o = h.update(str.encode(a+d))
p = o.hexdigest()
print (h)