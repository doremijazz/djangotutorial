# Compte rendu exercice django

## 2.2.2 Exercice Shell

### 2.2.2.1 PRéambule


### 2.2.2.2 Questions

1. Afficher toutes les questions

```
>>> for q in Question.objects.all():
...     print(q)
...
Comment s'appelle mon chien ?
Quel est le plus grand océan du monde ?
Quel langage est utilisé pour structurer une page web ?
Quelle planète est surnommée la planète rouge ?
Combien font 8 × 7 ?
```

2. Lister certaines question en fonction de la date

```
>>> for q in Question.objects.all():
...     if q.pub_date.day == 4 or q.pub_date.day == 5:
...             print(q)
...
Quel langage est utilisé pour structurer une page web ?
Quelle planète est surnommée la planète rouge ?
```

3. Lister les choix de la question id=2

```
>>> Question.objects.get(id=2)
<Question: Quel est le plus grand océan du monde ?>
>>> q = Question.objects.get(id=2)
>>> for choice in Choice.objects.all():
...     if choice.question_id == q.id:
...             print(choice)
...
Océan Pacifique
Océan Atlantique
Océan indien
```

4. Afficher le details des questions et les choix possibles

```
>>> for q in Question.objects.all():
...     print(q.id)
...     print(q.question_text)
...     print(q.pub_date)
...     for choice in Choice.objects.all():
...         if choice.question_id == q.id:
...             print(choice)
...
...
1
Comment s'appelle mon chien ?
2026-11-02 13:08:23+00:00
Tsuki
Ariane
Julia
2
Quel est le plus grand océan du monde ?
2026-11-03 13:20:37+00:00
Océan Pacifique
Océan Atlantique
Océan indien
3
Quel langage est utilisé pour structurer une page web ?
2026-11-04 13:22:04+00:00
CSS
HTML
SQL
4
Quelle planète est surnommée la planète rouge ?
2026-11-05 13:22:04+00:00
Vénus
Jupiter
Mars
5
Combien font 8 × 7 ?
2026-11-06 13:22:04+00:00
54
56
64
>>>
```

5. Afficher le nombre de choix par questions

```
>>> for q in Question.objects.all():
...     cpt =0
...     for choice in Choice.objects.all():
...         if choice.question_id == q.id:
...             cpt+=1
...     print(f"Question {q.id} : {cpt} choix")
...     cpt =0
...
Question 1 : 3 choix
Question 2 : 3 choix
Question 3 : 3 choix
Question 4 : 3 choix
Question 5 : 3 choix
>>>
```

6. Optionel

7. Tirer par date décroissante
```
>>> for q in Question.objects.order_by("-pub_date"):
...     print (f"Questions : {q} / publié {q.pub_date}")
...
Questions : Combien font 8 × 7 ? / publié 2026-11-06 13:22:04+00:00
Questions : Quelle planète est surnommée la planète rouge ? / publié 2026-11-05 13:22:04+00:00
Questions : Quel langage est utilisé pour structurer une page web ? / publié 2026-11-04 13:22:04+00:00
Questions : Quel est le plus grand océan du monde ? / publié 2026-11-03 13:20:37+00:00
Questions : Comment s'appelle mon chien ? / publié 2026-11-02 13:08:23+00:00
```

8. Optionnel

9. Ajouter uen question avec le shell 10. Puis 3 choix

```
>>> from django.utils import timezone
>>> q= Question(question_text="Quel est le plus grans désert chaud du monde ?", pub_date=timezone.now())
>>> q.save()
>>> q.choice_set.create(choice_text="Gobi", votes=0)
<Choice: Gobi>
>>> q.choice_set.create(choice_text="Sahara", votes=0)
<Choice: Sahara>
>>> q.choice_set.create(choice_text="Kalahari", votes=0)
<Choice: Kalahari>
>>> q.choice_set.all()
<QuerySet [<Choice: Gobi>, <Choice: Sahara>, <Choice: Kalahari>]>
```

```
>>> for q in Question.objects.all():
...     print(q.id)
...     print(q.question_text)
...     print(q.pub_date)
...     for choice in Choice.objects.all():
...             if choice.question_id == q.id:
...                     print(choice)
...
1
Comment s'appelle mon chien ?
2026-11-02 13:08:23+00:00
Tsuki
Ariane
Julia
2
Quel est le plus grand océan du monde ?
2026-11-03 13:20:37+00:00
Océan Pacifique
Océan Atlantique
Océan indien
3
Quel langage est utilisé pour structurer une page web ?
2026-11-04 13:22:04+00:00
CSS
HTML
SQL
4
Quelle planète est surnommée la planète rouge ?
2026-11-05 13:22:04+00:00
Vénus
Jupiter
Mars
5
Combien font 8 × 7 ?
2026-11-06 13:22:04+00:00
54
56
64
6
Quel est le plus grans désert chaud du monde ?
2026-11-03 08:16:00.126720+00:00
Gobi
Sahara
Kalahari
```

11. Listez les questions publiées récemment.
```
Question.objects.order_by("-pub_date")[:2]
<QuerySet [<Question: Combien font 8 × 7 ?>, <Question: Quelle planète est surnommée la planète rouge ?>]>
>>>
```

12. Optionnel