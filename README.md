# Data Mining Project

## Prerequisites:
- Python 3.6

## Instalare:
- Se instaleaza urmatoarele dependinte:
```bash
  pip install openai
  pip install whoosh
  pip install nltk
```
- Se descarca fisierele wikipedia de pe urmatorul link: [wikipedia](https://www.dropbox.com/s/nzlb96ejt3lhd7g/wiki-subset-20140602.tar.gz?dl=0).
- Se creeaza un folder numit ```FileExample``` in folderul proiectului.
- Se copiaza fisierele descarcate in folderul ```FileExample```
- Indexul se poate descarca de la aceasta adresa: [index](https://we.tl/t-Zan9tYYWGb). Se dezarhiveaza in folderul proiectului.
- Se ruleaza urmatoarea comanda pentru a descarca stopwords-urile:
```python
  nltk.download('stopwords')
```
- Dupa aceea se ruleaza metoda ```test_index```. Executia acestei metode dureaza aproximativ 20 de minute. Daca fisierul index lipseste,
acesta se genereaza pe baza fisierelor Wikipedia, iar timpul de executie creste considerabil(in cazul nostru a durat 40 de minute generarea acestuia). 
