#!/bin/sh
# Rebuilds the guide pages from their Markdown. The .md files are the source,
# and are also served to agents as they are (see _worker.js).
cd "$(dirname "$0")"
page() { python3 -I build.py support.html "$1.md" "$2" "$3" "$4"; }
page guides guides/index.html "Sewing guides" "Plain answers for people who sew: keeping a fabric stash, how much fabric a pattern or dress needs, shrinkage, and what a make costs."
page guides/fabric-stash-inventory guides/fabric-stash-inventory.html "How to keep a fabric stash inventory" "What to record for each fabric in your sewing stash (photo, length, fiber, width, weight, location, price), how to keep it current, and spreadsheet vs app."
page guides/enough-fabric-for-a-pattern guides/enough-fabric-for-a-pattern.html "Do I have enough fabric for this pattern?" "How to read a sewing pattern's yardage chart by size and fabric width, and allow for shrinkage, nap, one-way prints and plaid matching before you cut."
page guides/sewing-project-cost guides/sewing-project-cost.html "How to work out what a sewing project cost" "Add up what a handmade garment cost: fabric by the length used, notions, pattern and your hours, with a worked example and markup vs margin for a sale price."
page guides/how-much-fabric-for-a-dress guides/how-much-fabric-for-a-dress.html "How much fabric do I need for a dress?" "Rough fabric amounts for a dress by style and fabric width, and how to estimate yardage from your own measurements, with a worked example."
page guides/fabric-shrinkage guides/fabric-shrinkage.html "How much does fabric shrink? Cotton, linen, wool, viscose" "Typical first-wash shrinkage for cotton, linen, viscose, wool, silk, synthetics and knits, how to test a piece, and how to prewash before cutting."
page guides/pricing-handmade-clothes guides/pricing-handmade-clothes.html "How to price handmade clothes" "Price handmade clothing to cover materials, your time and overheads: markup, margin or an hourly rate, with a worked example for a linen shirt."
