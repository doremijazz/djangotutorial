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