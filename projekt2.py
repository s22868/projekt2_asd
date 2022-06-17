def write_file(string, file_name):
    with open(file_name, 'w') as f:
        f.write(string)


def read_file(filename):
    with open(filename, 'r') as f:
        return f.read()


string = read_file('input.txt')

# stworzenie dicta z litera i iloscia wystapien
def create_dict(string):
    my_dict = {}
    for i in string:
        if i in my_dict:
            my_dict[i] += 1
        else:
            my_dict[i] = 1
    return my_dict


class Node:
    def __init__(self, freq, symbol, left=None, right=None):
        # ilosc wystapien
        self.freq = freq
        # nazwa węzła (symbol)
        self.symbol = symbol
        # lewy dolny węzeł połączony z obecnym
        self.left = left
        # prawy dolny węzeł połączony z obecnym
        self.right = right
        # 'kierunek' obecnego węzła 0/1 - lewy/prawy i potrzebne do generowania kodów
        self.huff = ''

    # do testowania
    def __repr__(self):
        return "|| symbol: " + self.symbol + ', freq: ' + str(self.freq) + " || "


# kody huffmana trzymane w tablicy - np. a:0, b:1, c:10, d:11
huffman_codes = []


def generateCodes(node, val=''):
    # kod obecnego wezla zostaje generowany wg. 'kierunku' węzła 0/1
    newVal = val + str(node.huff)

    # jezeli wezel nie jest na krawedzi(ostatni w drzewie) to przechodzimy w dol
    if(node.left):
        generateCodes(node.left, newVal)
    if(node.right):
        generateCodes(node.right, newVal)

    # jezeli wezel jest na krawedzi(ostatni w drzewie) to zapisujemy kod do tablicy
    if(not node.left and not node.right):
        huffman_codes.append((node.symbol, newVal))


# wczytywanie pliku i utworzenie dict z iloscia wystapien liter
dc = create_dict(string)
dc = [x for x in dc.items()]
#
# print(dc)
#[('B', 1), ('a', 7), ('r', 5), ('b', 3), (' ', 2), ('m', 1)]
#
# x[0] to tablica znakow w pliku input.txt i x[1] to tablica ilosci wystapien
chars = [x[0] for x in dc]
freq = [x[1] for x in dc]
# znaki
# chars = ['B', 'a', 'r', 'b', ' ', 'm']
#
# ilosc wystapien
# freq = [ 1, 3, 5, 10, 2, 1]

# lista wezlow
nodes = []

# zamiana znakow i ilosci wystapien na wezly w drzewie
for x in range(len(chars)):
    nodes.append(Node(freq[x], chars[x]))


# print(nodes)
# [|| symbol: B, freq: 1 || , || symbol: a, freq: 7 || , || symbol: r, freq: 5 || , || symbol: b, freq: 3 || , || symbol:  , freq: 2 || , || symbol: m, freq: 1 || ]

# wyciaganie pierwszego wezla z kopca (najmniejszy) i zamiana miejscami pierwszy na ostatni i wyrzucenie ostatniego
def heap_extract_min(Q):
    min = Q[0]
    Q[0] = Q[-1]
    Q.pop()
    #ponowne utworzenie kopca po wyciagnieciu
    heapify_min(Q, 0)
    return min

# tworzenie kopca (najmniejszy na poczatku) z wezlow wedlug ilosci wystapien
def heapify_min(nodes, i):
    left = 2*i + 1
    right = 2*i + 2
    if left < len(nodes) and nodes[left].freq < nodes[i].freq:
        smallest = left
    else:
        smallest = i
    if right < len(nodes) and nodes[right].freq < nodes[smallest].freq:
        smallest = right
    if smallest != i:
        nodes[i], nodes[smallest] = nodes[smallest], nodes[i]
        heapify_min(nodes, smallest)


for i in range(len(nodes)//2, -1, -1):
    heapify_min(nodes, i)

# wyswietlanie drzewka huffmana z symbolami i czestotliwoscia -- poczatkowa lista
# print(nodes)

#zbudowanie drzewa
while len(nodes) > 1:
    # wybranie 2ch najmniejszych wezlow wedlug ilosci wystapien
    x = heap_extract_min(nodes)
    y = heap_extract_min(nodes)
    # ustawienie kierunku wybranych wezlow - potrzebne do generowania kodow huffmana
    x.huff = 0
    y.huff = 1
    # tworzenie nowego wezla z suma wystapien dwoch wezlow
    z = Node(x.freq + y.freq, x.symbol+y.symbol, x, y)
    # dodanie nowego wezla do listy wezlow
    nodes.append(z)
    # ponowne utworzenie kopca z nowym wezlem
    heapify_min(nodes, len(nodes)-1)


# wypelnienie tablicy huffman_codes
generateCodes(nodes[0])
# huffman_codes == [('a', '0'), ('r', '10'), ('b', '110'), (' ', '1110'), ('B', '11110'), ('m', '11111')]

# print("kody kuffmana: ", huffman_codes)


# zakodowanie pliku
def huffman_encode(string):
    encoded = ''
    # iterowanie po znakakch w pliku
    for i in string:
        for j in huffman_codes:
            # jezeli znak jest znakiem z tablicy huffman_codes to dodaje kod do encoded np. jezeli to a to dodaje 0 a jezeli m to dodaje 11111
            if i == j[0]:
                encoded += j[1]
    # zamkniecie pliku
    return encoded


# print("Po zakodowaniu: ", huffman_encode(string))


huffman_1011 = huffman_encode(string)
# print(huffman_1011)


# stworzenie tablicy bitow zakodowanego pliku   - 01001010 = 74 (74 = J)
byte_array = []
for i in range(0, len(huffman_1011), 8):
    byte_array.append(int(huffman_1011[i:i+8], 2))
    
# print(byte_array)

with open('output_bin.txt', 'wb') as bin_file:
    bin_file.write(bytes(str(huffman_codes), 'utf-8') + b"\n")
    bin_file.write(bytearray(byte_array))


# print(nodes[0].right.right.right.right.left.symbol)
