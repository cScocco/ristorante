import random
import threading
import time
from queue import Queue
from threading import Thread


class Ristorante(object):
    # accesso esclusivo a print su schermo
    printer = threading.Lock()

    # stampa di messaggi sullo schermo
    def stampa(self, messaggio):
        with self.printer:
            print(f'{self.nome_ristorante} : {messaggio}')
            print()

    # costruttore del ristorante
    def __init__(self,
                 nome_ristorante,
                 menu,
                 tavoli,
                 nome_cuochi,
                 gruppi_clienti):
        self.nome_ristorante = nome_ristorante
        self.menu = menu

        # coda dove veranno accodate le comande (ordini dei clienti)
        self.comande = Queue()

        # i tavoli vengono messi nella coda dei tavoli disponibili
        # per ogni tavolo viene creata una coda dentro un dizionario
        self.tavoli_disponibili = Queue()
        self.piatti_preparati = dict()
        for tavolo in tavoli:
            self.tavoli_disponibili.put(tavolo)
            self.piatti_preparati[tavolo] = Queue()

            # attivazione dei gruppi clienti
        for gruppo_cliente in gruppi_clienti:
            thread = Thread(target=self.cliente, kwargs=dict(gruppo_cliente=gruppo_cliente))
            thread.start()
            time.sleep(10 * random.random())

        # attivazione dei cuochi
        for nome_cuoco in nome_cuochi:
            thread = Thread(target=self.cuoco, kwargs=dict(nome_cuoco=nome_cuoco))
            thread.start()
            time.sleep(1 * random.random())

    # il processo del cuoco
    def cuoco(self, nome_cuoco):

        self.stampa(f'{nome_cuoco} va in cucina')

        # finchè ci sono comande da evadere
        while self.comande.qsize() > 0:
            # si prende una comanda
            tavolo, piatti = self.comande.get()

            self.stampa(f'{nome_cuoco} prepara {piatti} per il tavolo {tavolo}')

            # si prepara la comanda
            time.sleep(20 * random.random())

            # si porta il piatto al tavolo
            self.piatti_preparati[tavolo].put(piatti)

        self.stampa(f'{nome_cuoco} ha finito')

    # il processo del gruppo cliente
    def cliente(self, gruppo_cliente):

        # si attende un tavolo disponibile
        tavolo = self.tavoli_disponibili.get()

        # le persone del gruppo si siedono
        for persona in gruppo_cliente:
            self.stampa(f'{persona} si siede al tavolo {tavolo}')

        # le persone del gruppo ordinano
        for tipo_di_piatti in self.menu:
            piatti_scelti = random.choices(tipo_di_piatti, k=len(gruppo_cliente))
            self.stampa(f'ordinazione per tavolo {tavolo} : {piatti_scelti}')
            self.comande.put((tavolo, piatti_scelti))
            time.sleep(10 * random.random())

        # le persone del gruppo attendono i piatti e poi li consumano
        for tipo_di_piatti in self.menu:
            piatti_preparati = self.piatti_preparati[tavolo].get()
            self.stampa(f'al tavolo {tavolo} si consumano : {piatti_preparati}')
            time.sleep(10 * random.random())

        # a fine pasto, le persone del gruppo si alzano
        for persona in gruppo_cliente:
            self.stampa(f'{persona} si alza dal tavolo {tavolo}')

        # il tavolo viene reso disponibile per altri gruppi
        self.tavoli_disponibili.put(tavolo)


def main():
    # ristorante
    antipasti = ('prosciutto e melone', 'cocktail di gamberi', 'caprese')
    primi = ('lasagne', "tagliatelle al ragù", "risotto ai funghi", "bucatini alla amatriciana")
    secondi = ("arrosto con patate", "salmone in bella vista", "Ceasar salad")
    dolci = ("tiramisù", "gelato", "macedonia")
    menu = (antipasti, primi, secondi, dolci)
    clienti = (("Gianni",), ("Paolo", "Teresa"), ("Maria", "Marco"), ("Pino", "Filippo", "Franco"))
    Ristorante(nome_ristorante='Alla pergola',
               menu=menu,
               tavoli=('interno 1', 'esterno 1', 'esterno 2'),
               nome_cuochi=("Chef Mario", "Cuoca Anna", "Grand Chef Gianni"),
               gruppi_clienti=clienti)

    # bar
    bevande = ('caffè', 'cappuccino', 'cioccolata calda', 'caffè_macchiato')
    tavoli = ('saletta', 'sala bar')
    baristi = ('Franco', 'Giulia')
    clienti = (('Roberto',), ('Massimo', 'Elena'), ('Max', 'Laura', 'Jenny'), ('Tom',), ('Jennifer', 'Fred'))
    Ristorante(nome_ristorante='Caffè Roma',
               menu=(bevande,),
               tavoli=tavoli,
               nome_cuochi=baristi,
               gruppi_clienti=clienti)


main()
