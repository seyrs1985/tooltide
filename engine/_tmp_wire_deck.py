# -*- coding: utf-8 -*-
"""One-shot: wire DECKSTAIN (tt-dst deck page) via full-string replaces. Idempotent."""
import io

P = "tools.py"
s = io.open(P, encoding="utf-8").read()
n_total = 0

PAIRS = [
 ('<label for="dst-a">Deck floor area (sq ft)</label>',
  '<label for="dst-a" data-i18n="deck.area">Deck floor area (sq ft)</label>', "deck.area"),
 ('<label for="dst-r">Railing linear feet</label>',
  '<label for="dst-r" data-i18n="deck.railing">Railing linear feet</label>', "deck.railing"),
 ('<label for="dst-c">Coats</label>',
  '<label for="dst-c" data-i18n="deck.coats">Coats</label>', "deck.coats"),
 ('<label for="dst-p">Price per gallon</label>',
  '<label for="dst-p" data-i18n="deck.price">Price per gallon</label>', "deck.price"),
 ('<span class="result-unit">gallons of stain</span>',
  '<span class="result-unit" data-i18n="deck.gallons">gallons of stain</span>', "deck.gallons"),
 ('<span>total cost</span>',
  '<span data-i18n="deck.totalcost">total cost</span>', "deck.totalcost"),
 ('<span>brushing hours</span>',
  '<span data-i18n="deck.brushing">brushing hours</span>', "deck.brushing"),
 ('<span>redo cycle</span>',
  '<span data-i18n="deck.redocycle">redo cycle</span>', "deck.redocycle"),
 ('<button type="button" class="tool-btn" id="dst-share">Share my stain math</button>',
  '<button type="button" class="tool-btn" id="dst-share" data-i18n="share.share-my-stainmath">Share my stain math</button>',
  "share.share-my-stainmath"),
]
for before, after, key in PAIRS:
    n = s.count(before)
    if n:
        s = s.replace(before, after)
        n_total += n
    else:
        print("MISS:", key)

io.open(P, "w", encoding="utf-8", newline="").write(s)
print("deck_wired_total", n_total)
