# Scientific Search
#### Репозиторий для разработки алгоритмов поиска научной информации.

В данные момен проект развивается в двух направлениях: 

1)Классификация текстов на основании абстракта (или полного текста), и далее расчет метрик схожести и релевантности статье.
- Первым шагом на вход подается список rss рассылок, из которого получается списко статей.
```
main/rss.py -> rssParser.py
```
- Далее в полученных статьях необходимо дозаполнить информацию о метаданных, где возможно вытащить текст. 
```
main/findDOI.py ->
-> main/findJournal.py
-> main/ALT.py
-> main/Elsevier_plumX.py (в данный момент недоработана, так как нет четкого понимания, на каких условиях работает API elsevier)
-> main/parse_scihub.py (перед использованием нужно заполнить куки - просто один раз зайти на sci-hub через клинета (e.g. браузер) и пройти капчу) (NB: law issues)
```
- Далее на заполненных данных необходимо определить тему текста (oncology, infection, autoimmune, ophthalmology, chemical, genetic). Для этого используется фреймворк gensim, а также реализованная в нем модель LSI (см. дальнейшие предложения по улучшению main/prepData.py). Для этого мы используем вручную подготовленные стоп-слова, а также memory-friendly подход к тренировке, предложенный gensim. Модели тренируются по скаченной с PubMed выборки 75 000 текстов, которые были выкачены c ресурса по запросу соответствующему какой-либо теме (рак, генетические заболевания и пр.). [Паша напиши плиз пример запроса в pubmed для реплицируемости].
```
{$texts} -> main/stoplist.py -> main/prepData.py -> main/train_model.py -> Scientific_Search/models_lsi
```
- На данный момент заключительный этап -- применить модели к скаченной информации с рассылки rss. Так как, в нашем распоряжении не всегда полные тексты, в алгоритме заложена логика проверки на длину текста. Если,он меньше 40 знаков, определние топика идет по названию. Кроме этого, в скрипте заложен расчет ряда евристик, которые помогают понять какие-либо сведения о статье (подробнее см. скрипт). 
```
main/scores.py
```
Как итог, на выходе мы получсем таблицу, в которой строки -- это отдельная статья, у которой в следующих столбцах расчитаны эвристики, схожести, тема и пр. Подобная подход, помогает визуализировать каждую и статей в n-мерном пространстве.   
Певый черновой вариант отрисовки скаттер плота: (TODO: добавить div окно для составления библиографии)
```
scatter/scatterPLot.ipynb
```
2) 

Оснвоное тело алгоритма прописано в файле main.py (main.ipynb). 
Кастомные фукнции разнесены по отдельным файлам .py (e.g. ALT.py, findDOI.py)
