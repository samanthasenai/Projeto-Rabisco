class Animal:
    def __init__(self, nome):
        self.nome = nome

    def fazer_som(self):
        pass

class Cachorro(Animal):
    def fazer_som(self):
        return "Latido"

class Gato(Animal):
    def fazer_som(self):
        return "Miau"

cachorro = Cachorro("Rex")
gato = Gato("Mimi")

print(cachorro.nome)  # Output: Rex
print(cachorro.fazer_som())  # Output: Latido
print(gato.nome)  # Output: Mimi
print(gato.fazer_som())  # Output: Miau