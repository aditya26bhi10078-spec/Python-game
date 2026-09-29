seed = [0]


def rnd():
    seed[0] = (1103515245 * seed[0] + 12345) % 2147483648
    return seed[0] // 65536


def randint(a, b):
    return a + rnd() % (b - a + 1)


def isnum(s):
    if len(s) == 0:
        return False
    for c in s:
        if c not in "0123456789":
            return False
    return True


def getnum(msg, lo, hi):
    while True:
        s = input(msg)
        if isnum(s):
            n = int(s)
            if n >= lo and n <= hi:
                return n
        print("enter a number between", lo, "and", hi)


def getbet(bal):
    return getnum("bet (1-" + str(bal) + "): ", 1, bal)


def slots(bal):
    print("\n--- SLOTS ---")
    print("3 same = win, 2 same = get bet back")
    print("CHERRY x5, LEMON x8, BELL x12, STAR x20, SEVEN x50")
    pay = {"CHERRY": 5, "LEMON": 8, "BELL": 12, "STAR": 20, "SEVEN": 50}
    sym = ["CHERRY", "LEMON", "BELL", "STAR", "SEVEN"]
    bet = getbet(bal)
    r = []
    for i in range(3):
        r.append(sym[randint(0, 4)])
    print(r[0], "|", r[1], "|", r[2])
    if r[0] == r[1] and r[1] == r[2]:
        w = bet * pay[r[0]]
        print("jackpot! you won", w)
        bal = bal + w
    elif r[0] == r[1] or r[1] == r[2] or r[0] == r[2]:
        print("pair, bet returned")
    else:
        print("you lost", bet)
        bal = bal - bet
    return bal


def roulette(bal):
    print("\n--- ROULETTE ---")
    print("1. red/black (1:1)")
    print("2. odd/even (1:1)")
    print("3. single number (35:1)")
    red = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
    t = getnum("type (1-3): ", 1, 3)
    if t == 1:
        p = getnum("1 red, 2 black: ", 1, 2)
    elif t == 2:
        p = getnum("1 odd, 2 even: ", 1, 2)
    else:
        p = getnum("number (0-36): ", 0, 36)
    bet = getbet(bal)
    n = randint(0, 36)
    if n == 0:
        col = "green"
    elif n in red:
        col = "red"
    else:
        col = "black"
    print("ball landed on", n, col)
    win = False
    mult = 1
    if t == 1:
        if p == 1 and col == "red":
            win = True
        if p == 2 and col == "black":
            win = True
    elif t == 2:
        if n != 0:
            if p == 1 and n % 2 == 1:
                win = True
            if p == 2 and n % 2 == 0:
                win = True
    else:
        mult = 35
        if p == n:
            win = True
    if win:
        print("you won", bet * mult)
        bal = bal + bet * mult
    else:
        print("you lost", bet)
        bal = bal - bet
    return bal


def total(hand, val):
    t = 0
    aces = 0
    for c in hand:
        t = t + val[c]
        if c == "A":
            aces = aces + 1
    while t > 21 and aces > 0:
        t = t - 10
        aces = aces - 1
    return t


def blackjack(bal):
    print("\n--- BLACKJACK ---")
    print("beat the dealer without going over 21")
    ranks = ("2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A")
    val = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8,
           "9": 9, "10": 10, "J": 10, "Q": 10, "K": 10, "A": 11}
    deck = []
    for i in range(4):
        for r in ranks:
            deck.append(r)
    for i in range(len(deck) - 1, 0, -1):
        j = randint(0, i)
        deck[i], deck[j] = deck[j], deck[i]
    bet = getbet(bal)
    me = [deck.pop(), deck.pop()]
    dealer = [deck.pop(), deck.pop()]
    print("dealer has", dealer[0], "and ?")
    print("you have", me, "=", total(me, val))
    if total(me, val) == 21:
        w = bet * 3 // 2
        print("blackjack! you won", w)
        return bal + w
    while total(me, val) <= 21:
        c = input("hit or stand (h/s): ")
        if c == "h" or c == "H":
            me.append(deck.pop())
            print("you have", me, "=", total(me, val))
        elif c == "s" or c == "S":
            break
        else:
            print("type h or s")
    mt = total(me, val)
    if mt > 21:
        print("bust, you lost", bet)
        return bal - bet
    print("dealer has", dealer, "=", total(dealer, val))
    while total(dealer, val) < 17:
        dealer.append(deck.pop())
        print("dealer draws", dealer, "=", total(dealer, val))
    dt = total(dealer, val)
    if dt > 21:
        print("dealer bust, you won", bet)
        bal = bal + bet
    elif mt > dt:
        print("you won", bet)
        bal = bal + bet
    elif mt < dt:
        print("dealer wins, you lost", bet)
        bal = bal - bet
    else:
        print("tie, bet returned")
    return bal


def dice(bal):
    print("\n--- DICE ---")
    print("1. under 7 (1:1)")
    print("2. exactly 7 (4:1)")
    print("3. over 7 (1:1)")
    p = getnum("your pick (1-3): ", 1, 3)
    bet = getbet(bal)
    a = randint(1, 6)
    b = randint(1, 6)
    s = a + b
    print("rolled", a, "and", b, "=", s)
    if s < 7:
        res = 1
    elif s == 7:
        res = 2
    else:
        res = 3
    if p == res:
        w = bet
        if res == 2:
            w = bet * 4
        print("you won", w)
        bal = bal + w
    else:
        print("you lost", bet)
        bal = bal - bet
    return bal


def cardname(n):
    names = {11: "Jack", 12: "Queen", 13: "King", 14: "Ace"}
    if n in names:
        return names[n]
    return str(n)


def highlow(bal):
    print("\n--- HIGH LOW ---")
    print("guess if next card is higher or lower")
    print("every right guess doubles your pot, wrong guess loses the bet")
    bet = getbet(bal)
    pot = bet
    cur = randint(2, 14)
    streak = 0
    while True:
        print("\ncard:", cardname(cur), " pot:", pot)
        g = getnum("1 higher, 2 lower: ", 1, 2)
        nxt = randint(2, 14)
        print("next card:", cardname(nxt))
        if nxt == cur:
            print("same card, try again")
            continue
        ok = False
        if g == 1 and nxt > cur:
            ok = True
        if g == 2 and nxt < cur:
            ok = True
        if ok:
            streak = streak + 1
            pot = pot * 2
            cur = nxt
            print("correct! pot is", pot)
            if streak == 5:
                print("max streak, cashing out")
                break
            if getnum("1 continue, 2 cash out: ", 1, 2) == 2:
                break
        else:
            print("wrong, you lost", bet)
            return bal - bet
    print("you cashed out and won", pot - bet)
    return bal + pot - bet


def stats(st, bal, start):
    print("\nplayed:", st["played"])
    print("won:", st["won"])
    print("lost:", st["lost"])
    print("biggest win:", st["best"])
    print("chips:", bal, "(started with", start, ")")


def main():
    print("===== PYTHON CASINO =====")
    name = input("your name: ")
    lucky = getnum("lucky number (1-9999): ", 1, 9999)
    s = lucky
    for c in name:
        s = (s * 31 + ord(c)) % 2147483648
    seed[0] = s
    for i in range(10):
        rnd()

    start = 1000
    bal = start
    st = {"played": 0, "won": 0, "lost": 0, "best": 0}
    names = {1: "slots", 2: "roulette", 3: "blackjack", 4: "dice", 5: "high low"}
    print("hello", name, "you have", start, "chips")

    while bal > 0:
        print("\nchips:", bal)
        print("1. slots")
        print("2. roulette")
        print("3. blackjack")
        print("4. dice")
        print("5. high low")
        print("6. stats")
        print("0. leave")
        ch = getnum("choice: ", 0, 6)
        if ch == 0:
            break
        if ch == 6:
            stats(st, bal, start)
            continue
        while bal > 0:
            old = bal
            if ch == 1:
                bal = slots(bal)
            elif ch == 2:
                bal = roulette(bal)
            elif ch == 3:
                bal = blackjack(bal)
            elif ch == 4:
                bal = dice(bal)
            else:
                bal = highlow(bal)
            st["played"] = st["played"] + 1
            diff = bal - old
            if diff > 0:
                st["won"] = st["won"] + 1
                if diff > st["best"]:
                    st["best"] = diff
            elif diff < 0:
                st["lost"] = st["lost"] + 1
            print("chips:", bal)
            if bal <= 0:
                break
            if getnum("play " + names[ch] + " again? 1 yes, 0 no: ", 0, 1) == 0:
                break

    if bal <= 0:
        print("\nyou ran out of chips")
    stats(st, bal, start)
    if bal > start:
        print("you made a profit of", bal - start)
    elif bal < start:
        print("you lost", start - bal)
    else:
        print("you broke even")
    print("thanks for playing", name)


main()
