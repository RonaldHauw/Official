from bitarray import *

#### set variables ####
r = 384
l = 4
c = 128
t = 128
b = 512
nbits = 32
w = nbits
p = 1
r0, r1, r2, r3 = 8, 11, 16, 31

one = bitarray(nbits)
one.setall(False)
one[nbits-1] = 1 # one is an nbits-bit variable with value 1

def bitstr_to_bitarray(x,b=32):
    return bitarray(x.zfill(b))

def int_to_bitarray(x,b=32):
    return bitarray(str(bin(x))[2:].zfill(b))

def bitarray_to_bitstr(x):
    x.tolist()
    bin = ''
    for item in x:
        if item: # true (-> 1)
            bin += '1'
        else: # false (-> 0)
            bin += '0'
    return bin

def bitarray_to_dec(x):
    x = bitarray_to_bitstr(x)
    return int(x, 2)

def bitarray_to_hex(x):
    x = bitarray_to_bitstr(x)
    x = x.zfill(len(x)+(4-(len(x)%4))%4) # adds zero's in front of x so len(x) == 4
    return hex(int(x, 2))

# Initialisation constants
u0 = int_to_bitarray(0x0454EDAB)
u1 = int_to_bitarray(0xAC6851CC)
u2 = int_to_bitarray(0xB707322F)
u3 = int_to_bitarray(0xA0C7C90D)
u4 = int_to_bitarray(0x99AB09AC)
u5 = int_to_bitarray(0xA643466D)
u6 = int_to_bitarray(0x21C22362)
u7 = int_to_bitarray(0x1230C950)
u8 = int_to_bitarray(0xA3D8D930)
u9 = int_to_bitarray(0x3FA8B72C)
u10 = int_to_bitarray(0xED84EB49)
u11 = int_to_bitarray(0xEDCA4787)
u12 = int_to_bitarray(0x335463EB)
u13 = int_to_bitarray(0xF994220B)
u14 = int_to_bitarray(0xBE0BF5C9)
u15 = int_to_bitarray(0xD7C49104)

#### bitarray hulpfuncties ####
def message_to_bitarray(message):
    """
    Takes the message and converts it to binary, each character will be saved in 8 bits
    """
    bin_message = bitarray()
    for letter in message:
        bin_message += str(bin(ord(letter)))[2:].zfill(8)
    return bin_message

def bitarray_to_message(bin_message):
    """
    Takes the bitarray in slices of 8 and converts it to ASCII
    """
    message = ""
    for i in range(len(bin_message)/8):
        slice = bin_message[i*8:(i+1)*8]
        dec_int = bitarray_to_dec(slice)
        message += chr(dec_int)
    return message


def bitshift(var,n):
    """
    var = a bitarray
    n = the amount of bits the bitarray has to be shifted
        n > 0: bitshift(var,n) = var >> n
        n < 0: bitshift(var,n) = var << n
    """
    if n > 0: # shift to the right
        new_var = bitarray([0 for i in range(n)])
        new_var.extend(var[:-n])
        return new_var
    else: # (n < 0) shift to the left
        n = -n
        new_var = var[n:]
        new_var.extend([0 for i in range(n)])
        return new_var

def minus_one(bitstr):
    """
    Function to substract 1 from any bitstring
    e.g.: minus_one(0B101) = 0B100, 5-1 = 4
    """
    bitstring = bitarray(bitstr)
    pos = -1
    while bitstring[pos] != 1 and len(bitstring) != -pos:
        pos -= 1
    if len(bitstring) == -pos and bitstring[pos] == 0:
        print "[ERROR] minus_one() used on all zero bitarray"
        return None
    bitstring[pos] = 0
    for j in range(pos+1,0,+1):
        bitstring[j] = 1
    return bitstring

def rotronce(x):
    """
    does one right rotation
    assumes x is a bitarray
    """
    bit = x.pop()
    x.insert(0,bit)
    return x

def rotr(x,n):
    """
    rotates the 32-bit variable n-bits to the right
    IMPORTANT: the input of this function should be a 32-bit bitarray
    """
    output = bitarray(x)
    for i in range(n):
        output = bitarray(rotronce(output))
    return output

def rotl(x,n):
    """
    rotates the 32-bit variable to the right
    IMPORTANT: the input of this function should be a 32-bit bitarray
    """
    mask = minus_one(bitshift(one,-(nbits - n))) # mask = (one << (nbits-n)) - one
    return bitshift(x,(nbits - n)) | bitshift((x & mask), -n) # (x >> (nbits - n)) | ((x & mask) << n)

#### NORX-functions ####
def H(x,y):
    """
    x and y are bitarrays
    """
    return (x^y)^(bitshift((x&y),-1))

def G(a,b,c,d):
    """
    computes the G-function for 32-bit variables a, b, c and d
    """
    a = H(a,b)
    d = rotr(a^d,r0)
    c = H(c,d)
    b = rotr(b^c,r1)
    a = H(a,b)
    d = rotr(a^d,r2)
    c = H(c,d)
    b = rotr(b^c,r3)
    return a, b, c, d

def col(S):
    """
    Applies the G function to the columns
    """
    S = list(S) # creates local memory for the items of S

    S[0], S[4], S[8],  S[12] = G(S[0], S[4], S[8],  S[12])
    S[1], S[5], S[9],  S[13] = G(S[1], S[5], S[9],  S[13])
    S[2], S[6], S[10], S[14] = G(S[2], S[6], S[10], S[14])
    S[3], S[7], S[11], S[15] = G(S[3], S[7], S[11], S[15])
    return S

def diag(S):
    """
    applies the G function diagonally on S
    """
    S = list(S) # creates local memory for the items of S
    S[0], S[5], S[10], S[15] = G(S[0], S[5], S[10], S[15])
    S[1], S[6], S[11], S[12] = G(S[1], S[6], S[11], S[12])
    S[2], S[7], S[8],  S[13] = G(S[2], S[7], S[8],  S[13])
    S[3], S[4], S[9],  S[14] = G(S[3], S[4], S[9],  S[14])
    return S

def F(S,amount=None):
    """
    Applies the G function to the columns and diagonally of S
    Parameter l shows which iteration of F
    """
    S = list(S)
    if amount == None:
        amount = l
    for i in range(amount):
        S = list(diag(list(col(S))))
    return S

def pad(X):
    """
    Pads X so its length (in bits) is a multiple of r
    """
    len_Xm = len(X)%r
    new_X = bitarray(X) # creates a local var so X doesn't change outside of the function
    if len_Xm%8 == 0: # use BYTES
        u = (-(len_Xm/8)-2)%(r/8)
        if u > 0:
            new_X.extend([0,0,0,0,0,0,0,1])
            for i in range(u):
                new_X.extend([0,0,0,0,0,0,0,0])
            new_X.extend([1,0,0,0,0,0,0,0])
        if u == 0:
            new_X.extend([1,0,0,0,0,0,0,1])
    else: # use BITS
        u = (-len_Xm-2)%r
        new_X.append(1)
        for i in range(u):
            new_X.append(0)
        new_X.append(1)
    assert len(new_X)%r == 0
    return new_X

def absorb_slice(S, slice, v):
    """
    absorbs slice with tag v into S
    """
    v = int_to_bitarray(v)
    S = list(S) # create local S
    S[15] = S[15]^v # absorb tag
    S = F(S)
    slice.extend([0 for i in range(c)]) # extend slice so len = b
    for i in range(16): # 16 items of 32 bits
        S[i] = S[i]^slice[i*nbits:(i+1)*nbits]
    return S

def absorb(S,X,v):
    """
    absorbs X with tag v into S
    S = state (list of bitarrays)
    X = A (= header) or Z (= trailer) (one long bitarray)
    v = 01 (if X = header) or 04 (if X = trailer) (decimal number)
    """
    if len(X) == 0: # skips the function if X is empty
        return S
    S = list(S) # create local
    X = pad(X) # X becomes a multiple of r
    for i in range(len(X)/r):
        Xi = X[i:i+r]
        S = absorb_slice(S,Xi,v)
    return S

def encrypt_slice(S,Mi,v):
    S = list(S)
    S[15] = S[15]^v
    S = F(S)
    left_r = S[0] + S[1] + S[2] + S[3] + \
             S[4] + S[5] + S[6] + S[7] + \
             S[8] + S[9] + S[10]+ S[11] # r leftmost bits of S
    assert len(left_r) == r
    Ci = left_r^Mi
    for i in range(12):
        S[i] = Ci[i*32:(i+1)*32]
    return S, Ci

def encrypt(S,M,v):
    """
    assumes the contents of S and M are bitarrays and v is an integer
    """
    v = int_to_bitarray(v)
    C = bitarray()
    M_len = len(M)
    S = list(S) # creates local var of S
    if not(M_len > 0):
        return S, C

    # for-loop
    for i in range(M_len/r): # loops for every part of M except the last one
        Mi = M[r*i:r*(i+1)] # M is the message
        S, Ci = encrypt_slice(S,Mi,v)
        C.extend(Ci)

    # Mm = the last slice of M (with 0 <= len(Mm) < r)
    Mm = M[M_len-(M_len%r):]
    if len(Mm) > 382:
        print "ERROR len(Mm) > 382"
    S[15] = S[15]^v
    S = F(S)

    # len(Mm) = n_slices*nbits + rest
    len_Mm = len(Mm)
    n_slices = len_Mm/nbits
    rest = len_Mm%nbits

    # left = the len(Mm) leftmost bits of S
    left = bitarray()
    if n_slices == 0:
        left += S[0][:rest]
    else:
        for i in range(n_slices):
            left += S[i]
        left += S[i+1][:rest]
    assert len(left) == len(Mm)
    Cm = left^Mm
    C.extend(Cm)

    # XOR S with the padded version of Mm
    Mm = pad(Mm) + (c*'0')
    assert len(Mm) == 512
    for i in range(16):
        S[i] = S[i]^Mm[i*32:(i+1)*32]

    return S, C

def decrypt_slice(S,Ci,v):
    S = list(S)
    S[15] = S[15]^v
    S = F(S)
    left_r = S[0] + S[1] + S[2] + S[3] + \
             S[4] + S[5] + S[6] + S[7] + \
             S[8] + S[9] + S[10]+ S[11] # r leftmost bits of S
    assert len(left_r) == r
    Mi = left_r^Ci
    for i in range(12):
        S[i] = Ci[i*32:(i+1)*32]
    return S, Mi

def decrypt(S,C,v):
    """
    assumes the contents of S and C are bitarrays and v is an integer
    """
    v = int_to_bitarray(v)
    M = bitarray()
    C_len = len(C)
    S = list(S) # creates local memory for the items of S
    if not(C_len > 0):
        return S, M

    # for-loop
    for i in range(C_len/r): # loops for every part of M except the last one
        Ci = C[r*i:r*(i+1)] # C is the cyphertext
        S, Mi = decrypt_slice(S,Ci,v)
        M.extend(Mi)

    # Cm = the last part of C (with 0 <= len(Cm) < r)
    Cm = C[C_len-(C_len%r):]
    if len(Cm) > 382:
        print "ERROR len(Cm) > 382"
    S[15] = S[15]^v
    S = F(S)

    # len(Cm) = n_slices*nbits + rest
    len_Cm = len(Cm)
    n_slices = len_Cm/nbits
    rest = len_Cm%nbits

    # left = the len(Cm) leftmost bits of S
    left = bitarray()
    if n_slices == 0:
        left += S[0][:rest]
    else:
        for i in range(n_slices):
            left += S[i]
        left += S[i+1][:rest]
    assert len(left) == len(Cm)
    Mm = left^Cm
    M.extend(Mm)

    # XOR S with the padded version of Mm
    Mm = pad(Mm) + (c*'0')
    assert len(Mm) == 512
    for i in range(16):
        S[i] = S[i]^Mm[i*32:(i+1)*32]

    return S, M

def initialise(K,N):
    """
    initialises the state matrix S.
    S consists of the key, the nonce and 8 constants. In this application the nonce is a set of four ascending numbers
    """
    N = bitarray(N) # create local variable N
    K = bitarray(K) # create local variable K
    assert len(N) == len(K) == 128
    # n0, n1, n2, n3 = [N[i*nbits:(i+1)*nbits] for i in range(4)]
    # k0, k1, k2, k3 = [K[i*nbits:(i+1)*nbits] for i in range(4)]
    n0, n1, n2, n3 = N[0:32], N[32:64], N[64:96], N[96:128]
    k0, k1, k2, k3 = K[0:32], K[32:64], K[64:96], K[96:128]
    S = [n0, n1, n2, n3,
         k0, k1, k2, k3,
         u8, u9, u10,u11,
         u12,u13,u14,u15]
    S[12], S[13], S[14], S[15] = S[12]^int_to_bitarray(w), S[13]^int_to_bitarray(l), S[14]^int_to_bitarray(p), S[15]^int_to_bitarray(t)
    S = F(S)
    S[12], S[13], S[14], S[15] =  S[12]^k0, S[13]^k1, S[14]^k2, S[15]^k3
    return S

def finalise(S,K,v):
    S = list(S)
    k0, k1, k2, k3 = K[0:32], K[32:64], K[64:96], K[96:128]
    v = int_to_bitarray(v)
    S[15]=S[15]^v
    S=F(S)
    S[12], S[13], S[14], S[15] =  S[12]^k0, S[13]^k1, S[14]^k2, S[15]^k3
    S=F(S)
    S[12], S[13], S[14], S[15] =  S[12]^k0, S[13]^k1, S[14]^k2, S[15]^k3
    for item in S:
        assert len(item) == nbits
    T = bitarray()
    for i in range(-(t/nbits),0,1):
        T += S[i]
    return S,T

def AEADEnc(K, N, A, M, Z):
    S = initialise(K, N)
    S = absorb(S, A, 1)
    S, C = encrypt(S, M, 2)
    S = absorb(S, Z, 4)
    S, T = finalise(S,K,8)
    return C, T

def AEDDec(K, N, A, C, Z):
    S = initialise(K, N)
    S = absorb(S, A, 1)
    S, M = decrypt(S, C, 2)
    S = absorb(S, Z, 4)
    S, T = finalise(S,K,8)
    return M, T

def encrypt_text(message):
    """
    returns the tag and ciphertext as bitstrings
    assumes message is an ASCII string
    """
    key = 0x000102030405060708090A0B0C0D0E0F
    nonce = 0x202122232425262728292A2B2C2D2E2F
    header = 0x0123456789ABCDEF0123456789ABCDEF
    trailer = 0xFEDCBA9876543210FEDCBA9876543210
    K = bitarray(str(bin(key))[2:].zfill(128))
    N = bitarray(str(bin(nonce))[2:].zfill(128))
    A = bitarray(str(bin(header))[2:].zfill(128))
    M = message_to_bitarray(message)
    Z = bitarray(str(bin(trailer))[2:].zfill(128))
    C, T = AEADEnc(K, N, A, M, Z)
    C, T = str(bitarray_to_hex(C))[2:].replace("L", ""), bitarray_to_bitstr(T)
    return C, T

def decrypt_ciphertext(ciphertext):
    """
    returns the tag as a bitstring and the message as an ASCII string
    ciphertext is assumed a bitstring
    """
    key = 0x000102030405060708090A0B0C0D0E0F
    nonce = 0x202122232425262728292A2B2C2D2E2F
    header = 0x0123456789ABCDEF0123456789ABCDEF
    trailer = 0xFEDCBA9876543210FEDCBA9876543210
    K = bitarray(str(bin(key))[2:].zfill(128))
    N = bitarray(str(bin(nonce))[2:].zfill(128))
    A = bitarray(str(bin(header))[2:].zfill(128))
    C = bitarray(str(bin(int(ciphertext,16)))[2:])
    Z = bitarray(str(bin(trailer))[2:].zfill(128))
    M, T = AEDDec(K, N, A, C, Z)
    M, T = bitarray_to_message(M), bitarray_to_bitstr(T)
    return M, T