import requests
from pathlib import Path
import csv
import time
from datetime import datetime

def Timer(func):
    def wrapper(*args,**kwargs):
        print(f"Start:  {datetime.now():%H:%M:%S}")
        start = time.time()
        wynik = func(*args,**kwargs)
        print(f"Koniec: {datetime.now():%H:%M:%S}")
        print(f"{func.__name__} - czas: {time.time() - start} sec")
        return wynik
    return wrapper

class DownloadError(Exception):
     pass

class NotFoundError(DownloadError):
     print('File has not been found')


class AccessDeniedError(DownloadError):
     print('Url is not available')

class ETL:
    def __init__(self, folder='data', plik='latest.txt'):
        self.folder = Path(folder)
        self.plik = self.folder / plik
    @Timer
    def Laduj(self):
            with open(self.plik, encoding='utf-8') as f:
                 for line in f:
                     yield line.strip()   
    @Timer
    def Transform(self,wiersze):
        for wiersz in wiersze:
            numer,*wartosci = wiersz.split(',')
            liczby = [float(w) for w in wartosci if w != '-']
            brakujace = [i for i, w in enumerate(wartosci, start=1) if w == "-"]
            suma = sum(liczby)
            srednia = suma / len(liczby) if liczby else None

            yield {
                 "numer":int(numer),
                 "brakujace":brakujace,
                 "suma": round(suma,3),
                 "srednia": round(srednia, 3) if srednia is not None else "",
                  }
    @Timer
    def Zapisz(self,wiersze):
         with (
                     open(self.folder / "values.csv", "w", newline="", encoding="utf-8") as f_val,
                     open(self.folder / "missing_values.csv", "w", newline="", encoding="utf-8") as f_miss,
               ):
              values = csv.writer(f_val)
              missing = csv.writer(f_miss)

              for w in wiersze:
                    values.writerow([w["numer"], w["suma"], w["srednia"]])
                    missing.writerow([w["numer"], ";".join(map(str, w["brakujace"]))])

    @Timer
    def Odpalaj(self):
         self.Zapisz(self.Transform(self.Laduj()))




@Timer
def pobierz_plik(url,nazwa_pliku="latest.txt"):
    odp = requests.get(url,timeout=20)
    
    sciezka = Path("data") / nazwa_pliku


    if odp.status_code == 404:
         raise NotFoundError(f'Brak pliku :{url}')
    if odp.status_code == 403:
         raise AccessDeniedError(f'Brak dostępu do :{url}')

    odp.raise_for_status()

    with open(sciezka,'wb') as f:
        f.write(odp.content)

    print(f'Plik Zapisano W {sciezka}')    



if __name__ == "__main__":
    adresy = [
        "https://oleksandr-fedoruk.com/sggw/podyplomowe/file",
        "http://oleksandr-fedoruk.com/sggw/podyplomowe/404",
        "http://oleksandr-fedoruk.com/sggw/podyplomowe/403",
    ]
    for url in adresy:
            try:
                pobierz_plik(url)
            except NotFoundError as e:
                print(f"NotFoundError: {e}")
            except AccessDeniedError as e:
                print(f"AccessDeniedError: {e}")


    ETL().Odpalaj()       



