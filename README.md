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
- Indexul se poate descarca de la aceasta adresa: [index](https://we.tl/t-Zan9tYYWGb). Se dezarhiveaza in folderul proiectului.
- Se ruleaza urmatoarea comanda pentru a descarca stopwords-urile:
```python
  nltk.download('stopwords')
```
- Este nevoie si de un API KEY pentru ChatGPT. Acesta se pune in ```CHAT_GPT_API_KEY``` din fisierul ```utils/Constants```.
- Dupa aceea se ruleaza metoda ```main``` din fisierul ```main.py```. Executia acestei metode dureaza aproximativ 20 de minute. Daca fisierul index lipseste,
acesta se genereaza pe baza fisierelor Wikipedia, iar timpul de executie creste considerabil(in cazul nostru a durat 40 de minute generarea acestuia). 
