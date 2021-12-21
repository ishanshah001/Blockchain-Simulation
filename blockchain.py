"""
@author: Ishan Shah

Blockchain simulation
"""

import datetime
import hashlib

class Block:
    blockNo = 0
    data = None
    next = None
    hash = None
    nonce = 0

    # makes block chain immutable
    # if previous data is changed, it changes previous hash code
    # and thereby even current hash code (line 25)
    previous_hash = 0x0
    timestamp = datetime.datetime.now()

    def __init__(self, data):
        self.data = data

    def hash(self):
        #  The concept was subsequently adapted to securing digital money by Hal Finney in 2004 through
        #  the idea of "reusable proof of work" using the SHA-256 hashing algorithm.
        # Proof of work (PoW) is a decentralized consensus mechanism that requires members of a network to expend effort
        # solving an arbitrary mathematical puzzle to prevent anybody from gaming the system.
        h = hashlib.sha256()
        h.update(
        str(self.nonce).encode('utf-8') +
        str(self.data).encode('utf-8') +
        str(self.previous_hash).encode('utf-8') +
        str(self.timestamp).encode('utf-8') +
        str(self.blockNo).encode('utf-8')
        )
        return h.hexdigest()

    def __str__(self):
        return "Block Hash: " + str(self.hash()) + "\nBlockNo: " + str(self.blockNo) + "\nBlock Data: " + str(self.data) + "\nHashes: " + str(self.nonce) + "\nPrevious: " + str(self.previous_hash) + "\n--------------"

class Blockchain:
    # difficulty
    # You have to be the first miner to arrive at the right answer, or closest answer, to a numeric problem.
    # This process is also known as proof of work.
    # The first miner to come up with a 64-digit hexadecimal number (a "hash") that is less than or equal to
    # the target hash. It's basically guesswork.
    # Due to proof of work, Bitcoin and other cryptocurrency transactions can be processed peer-to-peer in a secure
    # manner without the need for a trusted third party.
    diff = 20
    maxNonce = 2**32
    target = 2 ** (256-diff)

    block = Block("Genesis")
    dummy = head = block

    def add(self, block):

        block.previous_hash = self.block.hash()
        block.blockNo = self.block.blockNo + 1

        # points current pointer to next block
        self.block.next = block
        # increments current block, i.e. current block is the next one
        self.block = self.block.next


    def mine(self, block):
        for n in range(self.maxNonce):
            if int(block.hash(), 16) <= self.target:
                self.add(block)
                break
            else:
                block.nonce += 1

blockchain = Blockchain()

# for n in range(10):
#     # generates blocks
#     # whenever a block is mined, we add it to block chain (line 57)
#     blockchain.mine(Block("Block " + str(n+1)))

info=["Hello","I","am","Ishan"]

blocks=[]

for i in info:
    block=Block(i)
    #print(block)
    blocks+=[block]

for i in blocks:
    blockchain.mine(i)
# blockchain.mine(blocks[0])
# blockchain.mine(blocks[2])

data=""

while blockchain.head != None:
    print(blockchain.head)
    data+=str(blockchain.head)
    blockchain.head = blockchain.head.next

file=open("data.txt","w")
file.write(data)
file.close()
