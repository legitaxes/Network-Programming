### import modules
import sys
import math
import random
import zlib


### functions
def qn1():
    txt = 'ABC abc'
    byte_arr_text = bytearray(txt, 'utf-8')
    print(len(txt))
    print(len(byte_arr_text))
    print(f'A corresponds to {byte_arr_text[0]}')
    print(f'B corresponds to {byte_arr_text[1]}')
    print(f'C corresponds to {byte_arr_text[2]}')
    print(f'space corresponds to {byte_arr_text[3]}')
    print(f'a corresponds to {byte_arr_text[4]}')
    print(f'b corresponds to {byte_arr_text[5]}')
    print(f'c corresponds to {byte_arr_text[6]}')
    print()


def qn2():
    print('Does ASCII encoding include swedish characters?')
    print('Many manufacturers devised 8-bit character sets consisting of ASCII plus up to 128 of the unused codes: encodings which covered all the more used Western European (and Latin American) languages, such as Danish, Dutch, French, German, Portuguese, Spanish, Swedish and more could be made')
    print("The ASCII encoding always starts with 195 [\\xc3] then followed by the character's ASCII code")
    print()

def qn3_and_4():
    txt = 'ÅÄÖ'
    byte_arr_text = bytearray(txt, 'utf-8')
    print(len(txt))
    print(len(byte_arr_text))
    print(byte_arr_text)
    print(f'Å corresponds to {byte_arr_text[0], byte_arr_text[1]}')
    print(f'Ä corresponds to {byte_arr_text[2], byte_arr_text[3]}')
    print(f'Ö corresponds to {byte_arr_text[4], byte_arr_text[5]}')
    print()

def read_exempeltext():
    ### REQUIRES AN ANSWER ###
    with open('lab-deliverables\exempeltext.txt') as f:
        txt = f.read()
        byte_arr_text = bytearray(txt, 'utf-8')
        # print(byte_arr_text)
        # find number of symbols in the text by counting how many times '0xc3' appears
        print(f'number of symbols in the text: {byte_arr_text.count(195)}')
        # find how many bytes the byte array contains
        print(f'number of bytes in the text: {len(byte_arr_text)}')
        print()
        return byte_arr_text


def makeHisto(byte_arr_text):
    """
    Functions that returns a histogram list of length 256 
    which indicates how many times each number/bit-pattern (0-255) 
    ccurs in byte_arr_text
    """
    hist = [0]*256
    for i in byte_arr_text:
        hist[i] += 1
    print(hist)
    return hist


def makeProb(histo):
    """
    Function that returns a probability distribution based on the histogram distribution
    Same list length as histogram but except its normalised such that all numbers in the list should total up to 1.0
    """
    total = 0
    prob = [0]*256
    for i in range(len(histo)):
        total += histo[i]
        
    for i in range(len(histo)):
        prob[i] = histo[i]/total

    # check if total prob = 1
    sum = 0
    for i in range(len(prob)):
        sum += prob[i]
    
    print(prob)
    # print(sum)
    print()
    return prob


def entropi(prob):
    """
    Function that calculates and returns the probability distribution's entropy
    H = Summation of P(i) log 1/P(i)
    """
    entropy_total = 0
    for i in range(len(prob)):
        if prob[i] != 0:
            entropy_total += prob[i] * math.log2(1/prob[i])
    print(f'entropy total: {entropy_total}')
    print()


def qn2d(prob):
    print()
    print("Q2d: How many bytes should it be possible to compress the byte array variable if we treat it as memory-free source but use an optimal encoding?")
    print(f'we can compress byte-array variable to {entropi(prob)} bytes if we treat it as a memory-free source')


def qn4e():
    print()
    print("Q4e: Which one is the smallest number?")
    print("the zlib-encoded copy of the text is the smaller number because it has been compressed")
    print("the data source's entropy is the highest as it has not been modified at all and is the original file")


def qn5a():
    print()
    t1 = """I hope this lab never ends because it is so incredibly thrilling!"""
    t10 = 10*t1
    compressed_t1 = zlib.compress(bytearray(t1,"utf-8"))
    compressed_t10 = zlib.compress(bytearray(t10,"utf-8"))

    print(f'length of t1: {len(compressed_t1)}')
    print(f'length of t10: {len(compressed_t10)}')
    print("The reason why t10 is not 10 times longer than t1 is because zlib uses techniques to reduce redundancy in data. When a string is repeated multiple times, the compression algorithm can represent the repeated parts more efficiently. Although t10 contains 10 times more symbols than t1, its compressed length is not 10 times longer since there are ten repeated patterns in t10 allowing the compression algorithm to achieve a higher compression ratio.")


### main function
def main():
    # qn1()
    # qn2()
    # qn3_and_4()
    byte_arr_text = read_exempeltext()
    histo = makeHisto(read_exempeltext())
    prob = makeProb(histo)
    entropi(prob)
    qn2d(prob)
    
    # make a copy of byte_arr_text
    theCopy = byte_arr_text[:]
    random.shuffle(theCopy)
    # print(byte_arr_text)
    print()
    # print(theCopy)
    # compress the copy and return the zip-code as a new-byte array
    code = zlib.compress(theCopy)
    
    ### zip-code of theCopy measured in bytes
    print(f'size measured in bytes: {len(code)}')

    ### zip-code of theCopy measured in bits
    print(f'size measured in bits: {len(code)*8}')

    ### count source symbols of theCopy by counting uni-code 195
    print(f'number of source symbol: {code.count(195)}')
    print('the source symbol is reduced by close to half of the original size')


    ### zip-code of byte_arr_text measured in bytes
    print(f'size measured in bytes: {len(byte_arr_text)}')

    ### zip-code of byte_arr_text measured in bits
    print(f'size measured in bits: {len(byte_arr_text * 8)}')

    ### count source symbols of byte_arr_text by counting number of unicode 195
    print(f'number of source symbol: {byte_arr_text.count(195)}')

    qn4e()

    qn5a()

### run main function
if __name__ == "__main__":
    main()