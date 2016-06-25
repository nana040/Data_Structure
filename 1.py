# Data structure


class UNode:
    def __init__(self):
        self.n = 0
        self.name = None
        self.fcnt = 0
        self.wcnt = 0
        self.f = None
        self.ff = []

    def set(self, n, name):
        self.n = n
        self.name = name

    def Fadd(self, node):
        if self.f is None:
            self.f = node
        else:
            node.next = self.f
            self.f = node
            node.next.prev = node
        self.fcnt = self.fcnt + 1

    def Fdel(self, n):
        x = self.f
        while x:
            if x == n:
                x.next.prev = x.prev
                x.prev.next = x.next
            else:
                x = x.next

    def FFadd(self, n):  # ?
        self.ff.append(n)

    def FFdel(self, n):
        self.ff.remove(n)


class UTNode(UNode):
    def __init__(self):
        super().__init__()
        self.p = None
        self.left = None
        self.right = None


class UTree:
    def __init__(self):
        self.root = None

    def search(self, z):
        x = self.root
        while x:
            if z == x.n:
                return x
            elif z < x.n:
                x = x.left
            else:
                x = x.right
        return -1

    def insert(self, z):
        y = None
        x = self.root
        while x:
            y = x
            if z.n < x.n:
                x = x.left
            else:
                x = x.right
        z.p = y
        if y == None:
            self.root = z
        elif z.n < y.n:
            y.left = z
        else:
            y.right = z

    def find_min(self, node):
        x = node
        while x.left:
            x = x.left
        return x

    def transplant(self, u, v):
        if u.p == None:
            self.root = v
        elif u == u.p.left:
            u.p.left = v
        else:
            u.p.right = v
        if v != None:
            v.p = u.p

    def delete(self, z):
        a = self.search(z)
        if a.left == None:
            self.transplant(a, a.right)
        elif a.right == None:
            self.transplant(a, a.left)
        else:
            b = self.find_min(a.right)
            if b.p != a:
                self.transplant(b, b.right)
                b.right = a.right
                b.right.p = b
            self.transplant(a, b)
            b.left = a.right
            b.left.p = b


class FNode:
    def __init__(self):
        self.n = 0
        self.v = 0
        self.prev = None
        self.next = None

    def set(self, n, v): # n is an user ID, v is a friend ID
        self.n = n
        self.v = v


class WNode:
    def __init__(self):
        self.v = ""
        self.hash = 0
        self.user = 0
        self.next = None
        self.prev = None
        self.down = None

    def set(self, v, user):
        self.v = v
        m = 0
        for c in v:
            m = m + ord(c)
        self.hash = m % 100
        self.user = user


class WHT:
    def __init__(self):
        self.list = []
        for i in range(0, 100):
            node = WNode()
            self.list.append(node)

    def search(self, v):
        m = 0
        for c in v :
            m = m + ord(c)
        m = m % 100
        a = self.list[m].next
        while a :
            if a.v == v :
                return a
            else :
                a = a.next
        return -1

    def add(self, node):
        a = self.list[node.hash]
        while (a) and (node.v == a.v) :
            a = a.next
        if a.v == node.v :
            b = a.down
            while b :
                b = b.down
            b = node # order correct?
        else :
            a.next = node
            node.prev = a

    def delete(self, v):
        a = self.search(v)
        a.next.prev = a.prev
        a.prev.next = a.next


# Interface
while True:
    print(str("Interface\n").center(20))
    print("0. Read data files")
    print("1. Display statistics")
    print("2. Top 5 most tweeted words")
    print("3. Top 5 most tweeted users")
    print("4. Find users who tweeted a word")
    print("5. Find all people who are friends of the above users")
    print("6. Delete users who mentioned a word")
    print("7. Delete all users who mentioned a word")
    print("8. Find strongly connected components")
    print("9. Find shortest path from a given user")
    print("99. Quit")

    Menu_Input = int(input("\nSelect Menu : "))

    # Read data files
    if Menu_Input == 0:
        cnt_u = 0
        cnt_f = 0
        cnt_w = 0

        Datadir1 = input("\nInput your 'User' text file name with its directory : ")
        with open(Datadir1) as Data_user:
            A = UTree()
            lines = Data_user.readlines()
            for line in lines :
                line = line[0:-1]
            for i in range(0, len(lines)-1, 4):
                node = UTNode()
                node.set(lines[i], lines[i+2])
                A.insert(node)
                cnt_u = cnt_u + 1

        Datadir2 = input("\nInput your 'Friend' text file name with its directory : ")
        with open(Datadir2) as Data_friend:
            lines = Data_friend.readlines()
            for line in lines:
                line = line[0:-1]
            for i in range(0, len(lines)-1, 3):
                node = FNode()
                node.set(lines[i], lines[i+1])
                a = A.search(node.n)
                a.Fadd(node)
                b = A.search(node.v)
                b.FFadd(node)
                cnt_f = cnt_f + 1

        Datadir3 = input("\nInput your 'Word' text file name with its directory : ")
        with open(Datadir3) as Data_word:
            B = WHT()
            lines = Data_word.readlines()
            for line in lines:
                line = line[0:-1]
            for i in range(0, len(lines)-1, 4) :
                node = WNode()
                node.set(lines[i+2], int(lines[i]))
                B.add(node)
                cnt_w = cnt_w + 1

        print("Total users : ", int(cnt_u))
        print("Total friendships records ", int(cnt_f))
        print("Total tweets : ", int(cnt_w))

    elif Menu_Input == 1 :
        