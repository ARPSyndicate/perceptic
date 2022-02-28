import optparse
import sys
import os
import concurrent.futures

from PIL import Image
from hashlib import blake2b

BLUE='\033[94m'
RED='\033[91m'
GREEN='\033[92m'
YELLOW='\033[93m'
CLEAR='\x1b[0m'

print(BLUE + "Perceptic[1.0] by ARPSyndicate" + CLEAR)
print(YELLOW + "perceptual image hashing" + CLEAR)

if len(sys.argv)<2:
	print(RED + "[!] ./perceptic --help" + CLEAR)
	sys.exit()

else:
	parser = optparse.OptionParser()
	parser.add_option('-d', '--directory', action="store", dest="directory", help="path to the directory of images")
	parser.add_option('-o', '--output', action="store", dest="output", help="output file")
	parser.add_option('-t', '--threads', action="store", dest="threads", help="maximum threads [default=20]", default=20)
	
inputs,args  = parser.parse_args()
if not inputs.directory:
	parser.error(RED + "[!] path to the directory of images not given" + CLEAR)

ilist = str(inputs.directory)
output = str(inputs.output)
threads = int(inputs.threads)
result = []

try:
    files = os.listdir(ilist)
except:
    print(RED + "[!] invalid input" + CLEAR)
    sys.exit()

def hashify(fil):
    try:
        with open(ilist+"/"+fil, 'rb') as f:
                image = Image.open(f).resize((32, 32), Image.ANTIALIAS).convert('L')
                pls = list(image.getdata())
        bits = "".join(map(lambda q: '1' if q > (sum(pls)/len(pls)) else '0', pls))
        persh = blake2b(bytes(int(bits, 2).__format__('16x'),'utf-8'), digest_size=7).hexdigest()
        result.append("[{0}] {1}".format(persh, fil))
        print(GREEN + "[{0}] {1}".format(persh, fil) + CLEAR)
    except:
        print(RED + "[INVALID] "+fil + CLEAR)
with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
    try:
    	executor.map(hashify, files)
    except(KeyboardInterrupt, SystemExit):
        print(RED + "[!] interrupted" + CLEAR)
        executor.shutdown(wait=False)
        sys.exit()

if inputs.output:
	result.sort()
	with open(output, 'a') as f:
		f.writelines("%s\n" % line for line in result)
print(YELLOW + "done"+ CLEAR)        