"""
HTS App 07 emulator
Usage:
    Make sure both flag1 and flag2 are
    set to 'y' and run
"""

enc = []

def encode(flag):
    if flag == 'y':
        """fill with values found from IDA"""
        input_str = "aaaaa"
        xor_sum_str = ["0","1DE","380","556","730","90C"]
        """stop filling"""
        xor_sum = []
        sum_chars = 0
        
        for i in range(len(input_str)):
                sum_chars += ord(input_str[i])
        #+ carriage retutn
        sum_chars += 10
        print "[+] Sum of chars: 0x%02x\n" % sum_chars

        for i in range(len(xor_sum_str)):
                xor_sum.append(int("0x"+xor_sum_str[i],0))

        for i in range(0,len(xor_sum_str)-1):
                enc.append((xor_sum[i+1]-xor_sum[i]) ^ sum_chars)
                
        print "[+] encrypted.enc: " + \
        ' '.join([str("0x%02x" % enc_char) for enc_char in enc])
        return 0
    else:
        print "[*] Calculation of encrypted chars aborted."
        return 1

def decode():
    """fill with the text string I tried on IDA
    already know its length must be 5"""
    input_str = "aaaaa"
    """stop filling"""
    enc_str = [str(enc[0]),str(enc[1]),str(enc[2]),str(enc[3]),str(enc[4])]
    checksum = 0
    sum_chars = 0

    for i in range(len(input_str)):
            sum_chars += ord(input_str[i])
    sum_chars += 10
    sum_chars = int("0x2F1",0)
    print "[+] Sum of chars: %d\n" % sum_chars
    
    for i in range(len(enc_str)):
        enc.append(int("0x"+enc_str[i],0))
    
    for i in range(len(input_str)):
        checksum += enc[i] ^ sum_chars
        print "[+] Checksum: 0x%02x" % checksum
    return 0


def test_sum_chars(low,high,flag):
    if flag == 'y':
        checksum_test = 0
        for sum_chars in range(low,high):
            # 5 enc chars so
            for i in range(5):
                checksum_test += enc[i] ^ sum_chars
            if checksum_test == int("0xDCA",0):
                print "\n[+] Required sum of input chars "+\
                "(excl. carriage return) found: 0x%02x or %d"\
                % (sum_chars-10,sum_chars-10)
                break
            checksum_test = 0
        return 0
    else:
        print "\n[*] Sum of chars testing aborted."
        return 1

def main():
    flag1, flag2 = 'y', 'y'
    encode(flag1)
    decode()
    test_sum_chars(500,900,flag2)
main()
