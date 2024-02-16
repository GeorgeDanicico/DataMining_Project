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
- Se descarca fisierele wikipedia de pe urmatorul link: [wikipedia](https://www.dropbox.com/s/nzlb96ejt3lhd7g/wiki-subset-20140602.tar.gz?dl=0)
- Se ruleaza urmatoarea comanda pentru a descarca stopwords-urile:
```python
  nltk.download('stopwords')
```
- Dupa aceea se ruleaza metoda ```test_index```. Executia acestei metode dureaza aproximativ 20 de minute.
