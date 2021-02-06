import sys
import hashlib
class Node(object):
    def __init__(self, letter,frequency,left,right):
        self.letter = letter
        self.left = left
        self.right = right
        self.frequency = frequency

#Parse dictionary or map as a parameter 
#   {alphabet(char) : frequency (int)}
#return a tree (root node)
def generateTree(letter_dict): 
    #** Only Use THIS algorithm to generate a tree, otherwise your final result may be incorrect!
    Node_list=[]

    #iterate to each charactor in dictionary
    #create a node for each charactor including alphabet(char) and frequency
    #*APPEND* all nodes to Node_list (insert to the end of the list)
    for i in letter_dict:
        if (letter_dict[i] != 0):
            Node_list.append(Node(i,letter_dict[i],None,None))

    #pop 2 nodes as node1,node2 that has *SMALLEST FREQUENCY* from the list
    #Create a new node that has the previous 2 node as a left and right child
    #Set frequency of the new node = node1.frequency + node2.frequency
    #***node1 MUST be the left child and node2 MUST be the right child***(node1.frequency <= node2.frequency)
    #insert the new node back *IN FRONT OF* the list
    #Repeat... until the list contains only 1 node (root node)
    #return the root node
    while(len(Node_list)>1): 
        temp_node1 = Node_list.pop(Node_list.index(min(Node_list,key = lambda node:node.frequency)))
        temp_node2 = Node_list.pop(Node_list.index(min(Node_list,key = lambda node:node.frequency)))
        Node_list.insert(len(Node_list),Node(None,temp_node1.frequency+
            temp_node2.frequency,temp_node1,temp_node2))
    return Node_list[0]

#for the first call, parse the prefix parameter with string = ""
#return as a 2 dimension list value [(alphabet,traversed bits),(...,...) ....]
def make_code(node, prefix):
    if node is None:
        return []
    if node.letter is not None:
        return [(prefix, node.letter)]
    else:
        result = []
        result.extend(make_code(node.left, prefix + '0'))
        result.extend(make_code(node.right, prefix + '1'))
        return result

def hashh(file):
    BLOCK_SIZE = 10 # The size of each read from the file

    file_hash = hashlib.sha256() # Create the hash object, can use something other than `.sha256()` if you wish
    with open(file, 'rb') as f: # Open the file to read it's bytes
        fb = f.read(BLOCK_SIZE) # Read from the file. Take in the amount declared above
        while len(fb) > 0: # While there is still data being read from the file
            file_hash.update(fb) # Update the hash
            fb = f.read(BLOCK_SIZE) # Read the next block from the file

    print ("hash : "+ file_hash.hexdigest()+"\n") # Get the hexadecimal digest of the hash
#Example
letter_dict = {i:0 for i in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz \n !@#$%^&*()_+=-0987654321+/\"\':;.,<>{}[]|"}
#This loop read and write multiple files at once
for i in range (1,2,1):
    si = str(i)
    if(len(si) == 1):
        si = '0'+si;
    #Read a file
    print(sys.argv[1])
    sample = open(sys.argv[1],"r")
    sample_text = sample.read()

    print("\n\n**************************************************")
    print("*             NTT  Challennge 2020               *")
    print("*              Huffman Code Guide                *")
    print("*                                                *")
    print("**************************************************")

    print("\nStep : ")
    #Count all alphabet and map its frequency in dictionary
    for k in sample_text:
        letter_dict[k] +=1
    print("1. Map all characters in text file....\n")
    le = letter_dict.copy()
    for p in le:
        if letter_dict[p] == 0:
            del letter_dict[p];
    print("FREQUENCY : "+str(letter_dict)+"\n")
    #Call generate Tree function, return Root Node
    root_node = generateTree(letter_dict)

    #Call code extraction function (parse root node as a parameter), return a list of [(alphabet, binary),[(..,..)], ....]
    result = make_code(root_node,"")

    #Map the previous list to dictionary [(alphabet : binary)]
    result_dict = {k[1]:k[0] for k in result}
    print("2. Make a Huffman tree, traverse to all of leaf nodes and map binary codes to each character...\n")
    print("BINARY LOOK UP TABLE : "+str(result_dict)+"\n")
    #Make a huffman code binary string
    string_bits = ""
    for j in sample_text:
        string_bits += str(result_dict[j])
    print("3. Then make a code...\n")
    print("code : "+string_bits+"\n")
    #Write binary file from binary string
    print("4. Write a *RAW BYTES* file from above binary code, then make a hash from the file...")
    byte_array = bytearray([int(string_bits[i:i+8], 2) for i in range(0, len(string_bits), 8)])
    f = open(sys.argv[2], 'w+b')
    f.write(byte_array)
    f.close()



