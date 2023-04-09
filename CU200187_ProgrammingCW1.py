import hashlib
import string
import random

"""
    Node class is to represent a node in a binary search tree.

    Attributes:
        key (str): The key value of the node.
        value (str): The value stored in the node.
        left (Node): The left child of the node.
        right (Node): The right child of the node.
    """
class Node:
    def __init__(self, key, value=None):
        self.key = key
        self.value = value
        self.left = None
        self.right = None

"""
    insert_node function to insert a node into a binary search tree.

    Args:
        root (Node): The root of the binary search tree.
        key (str): The key value of the node to be inserted.
        value (str): The value to be stored in the node.

    Returns:
        Node: The root of the binary search tree after the node has been inserted.
    """
#This function inserts a new node with the given key and value into the binary search tree (BST) rooted at root.
def insert_node(root, key, value):
    if root is None:
        return Node(key, value)
    if key < root.key:
        root.left = insert_node(root.left, key, value)
    elif key > root.key:
        root.right = insert_node(root.right, key, value)
    else:
        root.value = value
    return root

# Generate a list of 1000 random passwords, each consisting of 6 lowercase letters
def generate_passwords(count, length):
    passwords = []
    for i in range(count):
        password = ''.join(random.choices(list(string.ascii_lowercase), k=length))
        passwords.append(password)
    return passwords

# Hash each password using the MD5 hash function.
def hash_passwords(passwords):
    hashes = [hashlib.md5(password.encode('utf-8')).hexdigest() for password in passwords]
    return hashes

"""
    A function to reduce a hash value to a password.

    Args:
        hash_string (str): The hash value to be reduced.
        iteration (int): The iteration number.
        alphabet (str): The alphabet to be used for the password.
        word_length (int): The length of the password.

    Returns:
        str: The password obtained by reducing the hash value.
    """
# Define the reduction function used to generate the chains in the rainbow table.
# Reduce a hash value to a password of fixed length using the given alphabet.
# and produces a password of length 6 using the lowercase alphabet
def reduce_hash(hash_string, iteration, alphabet=None, word_length=6):
    if alphabet is None:
        alphabet = list(string.ascii_lowercase)
    # Compute the next value in the chain using the current hash value and iteration number.
    value = (int(hash_string, 16) + iteration) % (2 ** 40)

    # Map each digit in the value to a letter in the alphabet to generate the password.
    result = []
    for i in range(word_length):
        mod = value % len(alphabet)
        value //= len(alphabet)
        result.append(alphabet[mod])
    return "".join(result)

# Build the rainbow table by inserting nodes into the BST
def construct_rainbow_table(passwords, chain_length):
    root_node = None
    hashes = hash_passwords(passwords)
    for i in range(len(passwords)):
        hash_val = hashes[i]
        password = passwords[i]
        for j in range(chain_length):
            password = reduce_hash(hash_val, j)
            hash_val = hashlib.md5(password.encode('utf-8')).hexdigest()
        root_node = insert_node(root_node, hash_val, password)
    return root_node
# Print the rainbow table.
def print_rainbow_table(root, chain_length):
    print("{:<10} {:<34} {:<10}".format("First Password", "Last password", "Hashed"))
    print("-" * 80)

    """
         A function to print the contents of a binary search tree in sorted order.

         Args:
             root (Node): The root of the binary search tree.
        """
    #Traverse the BST rooted at root and print the key-value pairs.
    def print_tree(root):
        if root:
            print_tree(root.left)
            print("{:<10} {:<34} {:<10}".format(root.value, reduce_hash(root.key, chain_length - 1), root.key))
            print_tree(root.right)

    print_tree(root)

# a function to search for a hash value in the rainbow table and return the original password.
def crack_password(rainbow_table, hash_val_to_find, chain_length):
    current_node = rainbow_table
    while current_node is not None:
        if current_node.key == hash_val_to_find:
            return current_node.value
        elif current_node.key < hash_val_to_find:
            current_node = current_node.right
        else:
            current_node = current_node.left
    return None

if __name__ == "__main__":
    passwords = generate_passwords(1000, 6)
    print("Generating passwords...")
    hashes = hash_passwords(passwords)
    print("Hashing passwords...")
    rainbow_table = construct_rainbow_table(passwords, 10000)
    print("Rainbow table:")
    print_rainbow_table(rainbow_table, 10000)
    # Ask the user for a hash value to search for and print the original password if found.
    hash_val_to_find = input("Enter the hashed to get the first password: ")
    password = crack_password(rainbow_table, hash_val_to_find, 10000)
    if password is None:
        print("This hash is not found in the rainbow table. :(")
    else:
        last_value = reduce_hash(hash_val_to_find, 9999)
        print('The first password for this hash is ', password, )