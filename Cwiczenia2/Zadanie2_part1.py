
class Logger:
    def __enter__(self):
        print("Start sekcji logowania")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Koniec sekcji logowania")
        return False


with Logger():
    print("Jakiś Komentarz")


class FileWriter:
    def __init__(self, path):
        self.path = path
        self.plik = None

    def __enter__(self):
        self.plik = open(self.path, "w", encoding="utf-8")
        return self.plik

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.plik:
            self.plik.close()
        if exc_type is not None:
            print(f"Błąd podczas zapisu: {exc_val}")
        return False



with FileWriter("test.txt") as f:
    f.write("Pierwsza linia\n")
    f.write("Druga linia\n")

print(f.closed)  

with open("test.txt", encoding="utf-8") as f:
    print(f.read())



try:
    with FileWriter("test2.txt") as f:
        f.write("Pierwsza linia\n")
        raise ValueError("Nieprawidłowe dane")
except ValueError as e:
    print("Wyjątek przeszedł dalej:", e)



class SafeDivision:
    def __enter__(self):
        return self

    def divide(self, a, b):
        return a / b

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None and issubclass(exc_type, ZeroDivisionError):
            print("Nie można dzielić przez zero")
            return True
        return False


with SafeDivision() as sd:
    print(sd.divide(10, 2))

with SafeDivision() as sd:
    print(sd.divide(5, 0))

print("Dalej")

try:
    with SafeDivision() as sd:
        sd.divide("10", 2)
except TypeError as e:
    print("TypeError nie został stłumiony:", e)





