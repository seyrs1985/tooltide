# -*- coding: utf-8 -*-
"""ToolTide page definitions.

Every page = one long-tail keyword + one real working tool + original content
(intro paragraphs, how-to steps, FAQ). Built by build.py into static HTML.
Helpers below generate families of pages (countdowns, converters) so new
variants are one-line additions — that is the programmatic-SEO lever.
"""


def _cd(slug, event, month, day, keyword, facts, seasonal, emoji):
    """Countdown page: fixed month/day, recurs yearly (JS computes next occurrence)."""
    return {
        "slug": f"days-until-{slug}",
        "title": f"How Many Days Until {event}? Live {event} Countdown",
        "h1": f"How Many Days Until {event}?",
        "desc": f"See exactly how many days, hours and minutes until {event}. Free live countdown timer, updated every second — no sign-up, works on any device.",
        "category": "countdown",
        "keyword": keyword,
        "tool": "countdown",
        "args": {"event": event, "month": month, "day": day, "emoji": emoji},
        "intro": [
            f"This live countdown shows exactly how long until {event} — down to the second. "
            f"The timer works out the next occurrence of {event} automatically, so this page is always accurate, "
            "whether you are checking months ahead or counting down the final hours.",
            seasonal,
        ],
        "howto": [
            f"Open this page any time — the countdown to {event} starts updating immediately.",
            "Read the big number for whole days remaining, or watch the timer for days, hours, minutes and seconds.",
            "Check the facts panel below the timer for the exact date, day of the week, and weeks remaining.",
        ],
        "faqs": [
            (f"How many days until {event}?",
             f"The timer at the top of this page shows the exact number of days until {event}, calculated from your device's clock right now. It updates every second, so the answer you see is always current."),
            (f"What day of the week is {event}?",
             "The countdown's facts panel shows the day of the week for the upcoming date, so you can plan time off, travel or celebrations around it."),
            (f"How many weeks until {event}?",
             "Divide the days shown by 7 — or just read the weeks figure directly under the timer. We show days, weeks, hours and minutes so you can plan at whatever scale you need."),
            (f"Does the countdown work for {event} next year too?",
             "Yes. Once the date passes, the timer automatically rolls over to next year's date, so this page is a permanent, always-correct countdown."),
        ],
        "facts": facts,
    }


def _conv(slug, title_kw, a_name, b_name, factor, category_label, about, tip, dec=2):
    """Two-way unit converter page. factor = how many `b_name` in one `a_name`.
    factor=None means offset-type conversion (temperature) — args carry that flag."""
    is_temp = factor is None
    if is_temp:
        formula_line = (f"Temperature conversion is offset-based, not a simple multiplication: "
                        f"the converter applies the exact formula rather than a rough factor.")
        how_many_answer = ("Temperature scales don't convert by multiplication — °C to °F is °F = °C × 9/5 + 32, "
                           "with an offset for the different zero points. The converter applies the exact formula for you.")
    else:
        formula_line = (f"The conversion uses the exact relationship 1 {a_name} = {factor:g} {b_name}, "
                        "the same formula used in textbooks and engineering references.")
        how_many_answer = (f"Exactly {factor:g} {b_name}. This is a fixed definition, not an approximation, "
                           "so the conversion is exact at any scale.")
    return {
        "slug": slug,
        "title": f"{title_kw} Converter — Instant, Accurate, Free",
        "h1": f"{a_name} to {b_name} Converter",
        "desc": f"Convert {a_name} to {b_name} instantly. Exact formula, quick reference table, and a free two-way converter — no ads walls, no sign-up.",
        "category": "converter",
        "keyword": f"{title_kw.lower()} conversion",
        "tool": "unitconv",
        "args": {"a": a_name, "b": b_name, "factor": factor, "dec": dec, "label": category_label},
        "intro": [
            f"Type a value in {a_name} and get the answer in {b_name} instantly — or convert the other way. "
            + formula_line,
            about,
        ],
        "howto": [
            f"Type your value into the {a_name} box — the {b_name} result updates as you type.",
            f"To go the other direction, type into the {b_name} box instead and read the {a_name} result.",
            "Copy the result with one tap, or scan the reference table below for common values.",
        ],
        "faqs": [
            (f"How do you convert {a_name} to {b_name}?",
             (f"Multiply the number of {a_name} by {factor:g}. For example, 10 {a_name} = {10 * factor:g} {b_name}. "
              "The converter above does this for you and shows more decimal places than you will ever need.")
             if not is_temp else
             (f"For {a_name} to {b_name}, use °F = °C × 9/5 + 32" if "Celsius" in a_name else "For Fahrenheit to Celsius, use °C = (°F − 32) × 5/9")
             + ". The converter above applies it exactly as you type."),
            (f"How many {b_name} are in one {a_name}?",
             how_many_answer),
            (f"Is this converter accurate for professional use?",
             f"Yes — it uses full double-precision arithmetic and the official {a_name}-to-{b_name} factor, so results are reliable for schoolwork, cooking, fitness, travel and technical work."),
            (f"Can I convert {b_name} back to {a_name}?",
             "Yes. The converter is two-way: just type in the second box and the first box updates instantly with the reverse conversion."),
        ],
        "tip": tip,
    }


def PAGES():
    pages = []

    # ---------- Countdown family ----------
    xmas = _cd("christmas", "Christmas", 12, 25, "how many days until christmas",
               "Christmas Day is a public holiday in more than 160 countries. In the US and UK it is the biggest gift-giving and family-reunion day of the year.",
               "Whether you are planning gifts, booking travel, or just excited for the holidays, a precise countdown keeps the anticipation fun. Bookmark this page and check back anytime — the timer rolls over automatically after Christmas to count down to the next one.",
               "🎄")
    pages.append(xmas)

    ny = _cd("new-year", "New Year", 1, 1, "days until new year",
             "New Year's Day marks the first day of the calendar year. New Year's Eve — the night before — is one of the most celebrated nights on Earth.",
             "Planning resolutions, parties or fireworks? The countdown below targets January 1st of the next upcoming year, automatically updating after the ball drops.",
             "🎆")
    pages.append(ny)

    hw = _cd("halloween", "Halloween", 10, 31, "days until halloween",
             "Halloween is celebrated on October 31st with costumes, trick-or-treating and horror movies. It is the second-biggest commercial holiday in the US after Christmas.",
             "Use the timer to plan costumes, parties and pumpkin carving. Fun fact: searching for Halloween countdowns spikes every September as the spooky season kicks off.",
             "🎃")
    pages.append(hw)

    vd = _cd("valentines-day", "Valentine's Day", 2, 14, "days until valentines day",
             "Valentine's Day is on February 14th every year. It is the busiest day of the year for florists and one of the top days for restaurant reservations.",
             "Whether you are planning a surprise, booking a table, or ordering flowers in advance, the countdown below helps you avoid the last-minute rush.",
               "💝")
    pages.append(vd)

    bf = _cd("black-friday", "Black Friday", 11, 29, "days until black friday",
             "Black Friday is the fourth Friday of November — the day after US Thanksgiving — and the biggest online shopping day of the year. The timer below computes the exact date automatically, including years when the date shifts.",
             "Shoppers use Black Friday countdowns to plan big purchases, compare deals early, and set budget targets before the sales begin.",
               "🛒")
    bf["args"]["rule"] = {"week": 4, "weekday": 5}  # 4th Friday of November
    pages.append(bf)

    tg = _cd("thanksgiving", "Thanksgiving", 11, 26, "days until thanksgiving",
             "US Thanksgiving falls on the fourth Thursday of November. The timer computes the exact Thursday for the upcoming year automatically — including the shift between early and late Novembers.",
             "Planning the turkey, travel or the family football game? A live countdown keeps the cooking schedule on track.",
             "🦃")
    tg["args"]["rule"] = {"week": 4, "weekday": 4}  # 4th Thursday of November
    pages.append(tg)

    j4 = _cd("july-4th", "the 4th of July", 7, 4, "days until july 4th",
             "Independence Day — the 4th of July — is the United States' national holiday, marked by fireworks, barbecues and parades. It is the biggest summer holiday in the US calendar.",
             "Planning fireworks, a lake trip or a backyard party? The countdown below always targets the upcoming July 4th and rolls over automatically after the holiday.",
             "🇺🇸")
    pages.append(j4)

    md = _cd("mothers-day", "Mother's Day", 5, 10, "days until mothers day",
             "In the United States and many other countries, Mother's Day falls on the second Sunday of May. It is the busiest day of the year for restaurants and one of the top days for flower deliveries.",
             "The timer below computes the exact date of the second Sunday in May for the upcoming year automatically — no need to check a calendar. Planning flowers, brunch or a card in advance starts here.",
             "💐")
    md["args"]["rule"] = {"week": 2, "weekday": 0}  # 2nd Sunday of May
    pages.append(md)

    ea = _cd("easter", "Easter", 4, 20, "days until easter",
             "Easter Sunday is the highlight of the Christian calendar — and its date moves every year, falling on the first Sunday after the first full moon following the spring equinox, anywhere between March 22 and April 25.",
             "The timer below computes the moving date automatically for every year, so you never need to look it up. Planning the egg hunt, family lunch or the school-holiday trip starts here.",
             "🐣")
    ea["args"]["rule"] = {"easter": True}
    pages.append(ea)

    xme = _cd("christmas-eve", "Christmas Eve", 12, 24, "days until christmas eve",
              "Christmas Eve — December 24th — is when much of the world opens presents, attends midnight mass, and sits down to the main festive dinner. In many countries it is the emotional peak of the season, bigger than Christmas Day itself.",
              "Counting down to the 24th rather than the 25th? This timer targets Christmas Eve exactly, and rolls over to next year automatically after the holiday.",
              "🎅")
    pages.append(xme)

    sp = _cd("st-patricks-day", "St Patrick's Day", 3, 17, "days until st patricks day",
             "St Patrick's Day — March 17th — celebrates Ireland's patron saint with parades, shamrocks and (in quite a few cities) green beer. It is one of the most widely celebrated national days on Earth.",
             "Planning parade outfits, a pub crawl or a proper Irish breakfast? The countdown below always targets the upcoming March 17th.",
             "☘️")
    pages.append(sp)

    bd = _cd("boxing-day", "Boxing Day", 12, 26, "days until boxing day",
             "Boxing Day — December 26th — is a public holiday across the UK, Canada, Australia and much of the Commonwealth: a day of leftover sandwiches, Boxing Day sales, and full football fixtures.",
             "Counting down to the sales, the fixtures or the family visit? The timer targets December 26th and rolls over to next year automatically after the day passes.",
             "📦")
    pages.append(bd)

    fd = _cd("fathers-day", "Father's Day", 6, 21, "days until fathers day",
             "Father's Day falls on the third Sunday of June in the US, UK and dozens of other countries — the barbecue-and-tools holiday, and the third-biggest day for restaurant bookings after Mother's Day and Valentine's.",
             "The timer computes the third Sunday of June for the upcoming year automatically. Planning the gift, the grill or the visit starts here.",
             "👨")
    fd["args"]["rule"] = {"week": 3, "weekday": 0}  # 3rd Sunday of June
    pages.append(fd)

    nye = _cd("new-years-eve", "New Year's Eve", 12, 31, "days until new years eve",
              "New Year's Eve — December 31st — is the year's last party: countdowns, fireworks at midnight, Auld Lang Syne, and resolutions you will keep for at least a week. For hosts it is also the most demanding night of the year.",
              "Planning the party, the outfits or the midnight toast? This timer targets December 31st exactly — the countdown to the party, not just the calendar year.",
              "🥂")
    pages.append(nye)

    ed = _cd("earth-day", "Earth Day", 4, 22, "days until earth day",
             "Earth Day — April 22nd — is the world's largest environmental movement event: school projects, tree plantings, cleanups and climate campaigns in more than 190 countries.",
             "Teachers, students and organizers use this countdown to plan events and project deadlines. It always targets the upcoming April 22nd and rolls over automatically.",
             "🌍")
    pages.append(ed)

    cd = _cd("cinco-de-mayo", "Cinco de Mayo", 5, 5, "days until cinco de mayo",
             "Cinco de Mayo — May 5th — celebrates the Mexican victory at the Battle of Puebla in 1862. In the United States it has become a nationwide celebration of Mexican food, music and culture — bigger, ironically, than in most of Mexico itself.",
             "Planning the tacos, the playlist or the fiesta? The countdown always targets the upcoming May 5th and rolls over automatically after the day.",
             "🌮")
    pages.append(cd)

    ctd = _cd("thanksgiving-canada", "Canadian Thanksgiving", 10, 12, "canadian thanksgiving countdown",
              "Canadian Thanksgiving falls on the second Monday of October — six weeks before the American holiday, timed to the earlier harvest. It is a quieter affair: turkey, stuffing, and a long weekend with family.",
              "The timer computes the second Monday of October for the upcoming year automatically — handy for planning the drive home or the dinner menu.",
              "🍁")
    ctd["args"]["rule"] = {"week": 2, "weekday": 1}  # 2nd Monday of October
    pages.append(ctd)

    rd = _cd("remembrance-day", "Remembrance Day", 11, 11, "days until remembrance day",
             "Remembrance Day — the 11th of November — honours the fallen of the World Wars: the two-minute silence at the 11th hour, poppies on lapels, and ceremonies at every war memorial in Britain and the Commonwealth.",
             "The Poppy Appeal and school remembrance projects ramp up from October. The countdown always targets the upcoming 11th of November.",
             "🌹")
    pages.append(rd)

    sm = _cd("summer", "Summer", 6, 21, "how many days until summer",
             "Summer — the season of school holidays, beach days and long evenings — begins with the summer solstice, around June 21st in the Northern Hemisphere (the date can shift by a day from year to year).",
             "Whether you are counting down to the last day of school, a booked vacation or just the return of barbecue weather, this timer always targets the upcoming June 21st and rolls over automatically.",
             "☀️")
    pages.append(sm)

    at = _cd("autumn", "Autumn", 9, 22, "how many days until fall",
             "Autumn — or fall, if you are American — arrives with the autumnal equinox around September 22nd: sweater weather, pumpkin everything, and the best sleeping temperatures of the year.",
             "Counting down to hoodie season, the leaves changing, or the holiday run that starts right after it? This timer always targets the upcoming equinox date.",
             "🍂")
    pages.append(at)

    wt = _cd("winter", "Winter", 12, 21, "how many days until winter",
             "Winter begins with the winter solstice around December 21st — the shortest day of the year in the Northern Hemisphere, and the official start of ski season, hot chocolate season and early nights.",
             "Whether you want snow, skiing or just an excuse to stay in, the countdown always targets the upcoming solstice date and rolls over automatically.",
             "❄️")
    pages.append(wt)

    sp = _cd("spring", "Spring", 3, 20, "how many days until spring",
             "Spring begins with the vernal equinox around March 20th — the day daylight finally overtakes night, gardens wake up, and everyone remembers what warm air feels like.",
             "Counting down to lighter evenings, the first picnic or allergy season (sorry)? The timer always targets the upcoming equinox and rolls over automatically.",
             "🌸")
    pages.append(sp)

    jn = _cd("june", "June", 6, 1, "how many days until june",
             "June is the finish line month: finals end, school lets out, and the summer holidays officially begin. 'How many days until June' spikes every spring as students count down to freedom.",
             "This timer targets the upcoming June 1st and rolls over automatically — the moment June arrives, it quietly starts counting to next year.",
             "🎓")
    pages.append(jn)

    dc = _cd("december", "December", 12, 1, "how many days until december",
             "December is the month everything fun piles into: advent calendars, Christmas markets, Hanukkah nights, office parties and the first proper snow in half the world. It also happens to be the month most budgets die.",
             "Whether you are planning gifts, travel or the work party rota, this timer targets the upcoming December 1st and rolls over automatically.",
             "🎄")
    pages.append(dc)

    my = _cd("may", "May", 5, 1, "how many days until may",
             "May is the doorway to summer: Memorial Day weekend, Cinco de Mayo, Mother's Day in most of the world, and the last school month before the holidays. Gardens are planted, barbecues come out of the garage, and everyone's mood improves.",
             "This timer targets the upcoming May 1st and rolls over automatically — the moment May arrives, it starts counting to next year.",
             "🌼")
    pages.append(my)

    jl = _cd("july", "July", 7, 1, "how many days until july",
             "July is peak summer: the longest days of the year, school fully out, Independence Day fireworks and the year's biggest beach and lake weekends. It is also the month people realize the year is half gone.",
             "This timer targets the upcoming July 1st and rolls over automatically — when July arrives, it starts counting to the next one.",
             "🎆")
    pages.append(jl)

    sb = _cd("september", "September", 9, 1, "how many days until september",
             "September is the other new year: back to school, back to routine, autumn clothes in the shops and the last warm weekends. 'How many days until September' is the sound of summer ending — and of students dreading or welcoming it.",
             "This timer targets the upcoming September 1st and rolls over automatically after the month begins.",
             "🎒")
    pages.append(sb)

    pages.append({
        "slug": "strip-html",
        "title": "Strip HTML Tags Online — Convert HTML to Plain Text",
        "h1": "Strip HTML Tags",
        "desc": "Remove HTML tags from any text instantly — convert markup to clean plain text, decode entities, and see how many tags were stripped. 100% in-browser.",
        "category": "text",
        "keyword": "strip html tags",
        "tool": "striphtml",
        "args": {},
        "intro": [
            "Paste HTML — an email template, a scraped page, a CMS export — and get clean plain text with every tag removed: no divs, no spans, no inline styles, no surprise &nbsp; characters. The tag count shows how much markup was hiding in there.",
            "It exists for the moment every developer, marketer and data analyst has: text arrives full of markup and something downstream needs it naked. Everything runs locally in your browser, so it is safe for confidential content.",
        ],
        "howto": [
            "Paste your HTML into the input box — a fragment or a full document both work.",
            "The plain-text version appears instantly, with HTML entities like &amp; decoded to real characters.",
            "Check how many tags were stripped, then copy the clean text with one click.",
        ],
        "faqs": [
            ("How does HTML stripping work?",
             "Every <tag> is removed with a pattern match, then common HTML entities (&amp;, &lt;, &gt; and friends) are decoded into their real characters. What remains is the human-readable text content."),
            ("Is it safe to paste confidential HTML here?",
             "Yes — stripping runs entirely in your browser with JavaScript. Nothing is transmitted, logged or stored; you can disconnect from the internet and it still works."),
            ("Does it handle script and style tags?",
             "Yes — their entire contents are removed, not just the tags, so no stray CSS rules or JavaScript survive into the output."),
            ("Will the formatting survive?",
             "Plain text has no formatting by definition — headings become lines, links become their visible text, bold becomes normal. Line breaks between blocks are preserved so paragraphs stay readable."),
        ],
    })

    pages.append({
        "slug": "inch-fraction-calculator",
        "title": "Inch Fraction Calculator — Fractions ⇄ Decimals ⇄ MM",
        "h1": "Inch Fraction Calculator",
        "desc": "Convert fractional inches (like 3/8 or 1-3/4) to decimal inches and millimeters — and back. Rounded to the nearest 1/16. Built for woodworkers, DIY and hardware shopping.",
        "category": "calculator",
        "keyword": "inch fraction calculator",
        "tool": "inchfrac",
        "args": {},
        "intro": [
            "The tape measure speaks fractions — 3/8, 7/16, 1-3/4 — while plans, 3D printers and product pages speak decimals and millimeters. This calculator translates both ways: type a fraction and get the decimal and millimeter value, or type a decimal and get the nearest fraction to the 1/16th of an inch.",
            "It also knows mixed fractions: 1-3/4 inches is one entry, not two fields. Everything updates as you type, so you can check 'is 14 mm closer to 9/16 or 5/8?' without leaving the page.",
        ],
        "howto": [
            "Type a fraction like 3/8 or a mixed one like 1-3/4 — decimal inches and millimeters appear instantly.",
            "Type a decimal like 0.375 to get the nearest fraction to the 1/16th of an inch.",
            "Check the nearest-16th table below for the tape-measure reading you need.",
        ],
        "faqs": [
            ("What is 3/8 of an inch in decimals and mm?",
             "3/8 inch = 0.375 inches = 9.525 mm. Type it into the converter to confirm, and check neighboring fractions (11/32 = 0.344, 13/32 = 0.406) when a measurement sits between marks."),
            ("How do I read fractions on a tape measure?",
             "Between each inch mark, a tape divides into 16ths: the longest halfway mark is 1/2, quarter marks are 1/4 and 3/4, eighths next, and the shortest lines are 1/16 steps. Count lines from the inch mark and read top-down."),
            ("What is 0.375 inches as a fraction?",
             "0.375 = 3/8 exactly. Multiply the decimal by 16: 0.375 × 16 = 6, so it is 6/16, which simplifies to 3/8. The calculator does this rounding automatically."),
            ("Why do my digital calipers disagree with the tape?",
             "Calipers show decimal inches (or mm) to three places; tapes show fractions to the nearest 1/16 (0.0625). A tape reading of 9/16 (0.5625) and a caliper reading of 0.567 are the same measurement, rounded differently."),
        ],
    })


    pages.append({
        "slug": "percentage-increase",
        "title": "Percentage Increase Calculator — Percent Change Between Two Numbers",
        "h1": "Percentage Increase Calculator",
        "desc": "Calculate percentage increase (or decrease) between two numbers instantly: salary raises, price changes, growth rates. Formula shown, decrease detected automatically.",
        "category": "calculator",
        "keyword": "percentage increase calculator",
        "tool": "percent",
        "args": {"default": 2},
        "intro": [
            "Enter the old value and the new value to get the percentage change between them — the number behind salary negotiations ('a 5% raise'), price tracking ('eggs up 30%'), fitness PRs and revenue reports. If the value went down instead of up, the calculator says so automatically: the answer becomes a percentage decrease.",
            "The formula is (new − old) ÷ old × 100. A raise from $50,000 to $55,000 is (55,000 − 50,000) ÷ 50,000 × 100 = 10%. Enter any two numbers below and the working is shown line by line, so you can sanity-check the math.",
        ],
        "howto": [
            "Type the original (old) value in the first box.",
            "Type the new value in the second — the percentage change appears instantly.",
            "Read whether it is an increase or decrease; check the formula line to verify the working.",
        ],
        "faqs": [
            ("How do I calculate percentage increase?",
             "Subtract the old value from the new value, divide by the old value, and multiply by 100. From 40 to 50: (50 − 40) ÷ 40 × 100 = 25% increase."),
            ("What is the difference between percentage increase and percentage points?",
             "Percentage points compare two percentages directly (from 10% to 15% is 5 percentage points), while percentage increase is relative (10% to 15% is a 50% increase). News headlines mix them up constantly."),
            ("Why is my percentage decrease bigger than the matching increase?",
             "Because the base changes direction: going from 100 to 80 is a 20% decrease, but 80 back to 100 is a 25% increase — the second step divides by the smaller number. This asymmetry is normal, not a bug."),
            ("Can the result be more than 100%?",
             "Yes. A value that doubles (50 to 100) is a 100% increase; tripling is 200%. Anything over 100% simply means the value more than doubled."),
        ],
    })

    pages.append({
        "slug": "average-calculator",
        "title": "Average Calculator — Mean of Any Number List",
        "h1": "Average Calculator",
        "desc": "Paste a list of numbers and get the average (mean), plus sum and count. Handles comma, space or line-separated values. Instant and private.",
        "category": "calculator",
        "keyword": "average calculator",
        "tool": "average",
        "args": {},
        "intro": [
            "Paste any list of numbers — test scores, monthly bills, race times, sales figures — and get the average instantly, along with the sum and how many numbers you entered. Values can be separated by commas, spaces or new lines, in any mix.",
            "The average (strictly, the arithmetic mean) is the single most useful summary of a list: one number that represents the typical value. It also shows the sum, because half the time the follow-up question is 'so what was the total?'",
        ],
        "howto": [
            "Paste or type your numbers into the box — commas, spaces and line breaks all work.",
            "The average, sum and count update as you type.",
            "Fix any typos in place; the result recalculates on every keystroke.",
        ],
        "faqs": [
            ("How do I calculate the average?",
             "Add all the numbers together, then divide by how many there are. The average of 4, 8 and 12 is (4 + 8 + 12) ÷ 3 = 8. This calculator does the arithmetic and tolerates messy formatting."),
            ("What is the difference between mean, median and mode?",
             "The mean is the sum divided by the count (what this tool computes); the median is the middle value when sorted; the mode is the most frequent value. Mean is best for well-behaved data; median resists outliers like one huge salary skewing an average."),
            ("Does it handle negative numbers and decimals?",
             "Yes — any numeric values work: negatives, decimals, even scientific notation like 1.5e3. Non-numeric text between numbers is ignored."),
            ("Is my data uploaded?",
             "No — the calculation runs entirely in your browser with JavaScript. Nothing is sent or stored anywhere."),
        ],
    })



    ja = _cd("january", "January", 1, 1, "how many days until january",
             "January is the reset button: new year resolutions, gym memberships, dry January and the long, quiet walk back to work. 'How many days until January' is usually someone planning a fresh start — or bracing for the credit card bill.",
             "This timer targets the upcoming January 1st and rolls over automatically — the moment the new year begins, it starts counting to the next one.",
             "🎊")
    pages.append(ja)

    fb = _cd("february", "February", 2, 1, "how many days until february",
             "February is the short month with the biggest romantic deadline: Valentine's Day lands on the 14th, and the whole month is either a countdown to romance or to discount chocolate on the 15th. It is also, thanks to leap years, the only month that occasionally refuses to end.",
             "This timer targets the upcoming February 1st and rolls over automatically — leap years included.",
             "💘")
    pages.append(fb)

    ap = _cd("april", "April", 4, 1, "how many days until april",
             "April brings spring properly: cherry blossoms, Easter weekend most years, spring break trips, and (for Americans) the tax deadline on the 15th looming like a storm cloud over the tulips.",
             "This timer targets the upcoming April 1st and rolls over automatically — spring planners and filers alike.",
             "🌱")
    pages.append(ap)

    au = _cd("august", "August", 8, 1, "how many days until august",
             "August is summer's last stand: the big family holiday, the county fair, back-to-school sales creeping in, and evenings that start noticeably earlier by the end of the month.",
             "This timer targets the upcoming August 1st and rolls over automatically — holiday countdowns and school-supply triage both start here.",
             "🏖️")
    pages.append(au)

    nv = _cd("november", "November", 11, 1, "how many days until november",
             "November is the gateway to the holiday season: No Shave November, Thanksgiving travel chaos, Black Friday countdowns and the first Christmas ads of the year. The clocks have changed, the mornings are dark, and online carts are filling up.",
             "This timer targets the upcoming November 1st and rolls over automatically — shoppers use it to plan Black Friday budgets and holiday shipping deadlines.",
             "🗓️")
    pages.append(nv)

    mr = _cd("march", "March", 3, 1, "how many days until march",
             "March is the month winter loses its grip: the equinox brings spring, the clocks jump forward, March Madness tips off, and St Patrick's Day gives everyone a Tuesday excuse. 'How many days until March' is usually about one of those four things.",
             "This timer targets the upcoming March 1st and rolls over automatically — when March arrives, it starts counting to the next one.",
             "🌈")
    pages.append(mr)

    oc = _cd("october", "October", 10, 1, "how many days until october",
             "October is the month of flannel, pumpkin patches, horror movie marathons and the year's most important child-planning question: how many days until Halloween. It also holds the trick for retailers — Q4 begins here.",
             "This timer targets the upcoming October 1st and rolls over automatically — costume planners and deal hunters alike.",
             "🎃")
    pages.append(oc)

    af = _cd("april-fools-day", "April Fools' Day", 4, 1, "days until april fools day",
             "April Fools' Day — April 1st — is the worldwide day of practical jokes and hoaxes, from office pranks to brand marketing stunts. Media outlets and companies compete for the most believable fake product.",
             "Planning a prank that lands (and doesn't go too far)? The countdown below always targets the upcoming April 1st, rolling over automatically after the day is done.",
             "🤡")
    pages.append(af)

    ld = _cd("labor-day", "Labor Day", 9, 1, "days until labor day",
             "Labor Day — the first Monday of September — is the American tribute to workers, and the unofficial end of summer: barbecues, one last lake weekend, and the biggest back-to-school sales of the year.",
             "The timer computes the first Monday of September for the upcoming year automatically, including years when the date shifts. Planning the weekend trip or the sale shopping starts here.",
             "🛠️")
    ld["args"]["rule"] = {"week": 1, "weekday": 1}  # 1st Monday of September
    pages.append(ld)

    # ---------- Calculator family ----------
    pages.append({
        "slug": "percentage-calculator",
        "title": "Percentage Calculator — 3 Tools in One, Instant Answers",
        "h1": "Percentage Calculator",
        "desc": "Calculate X% of a number, what percent X is of Y, and percentage increase or decrease. Free instant percentage calculator with formulas shown.",
        "category": "calculator",
        "keyword": "percentage calculator",
        "tool": "percent",
        "args": {},
        "intro": [
            "Three percentage problems cover almost everything people ask: what is X% of Y, what percent is X of Y, and how much did something change in percent. This page does all three — type any two numbers and the answer appears instantly, with the formula shown so you can check the working.",
            "Percentages trip people up because the same words mean different operations. '20% of 150' is a multiplication; '15 is what percent of 60' is a division; 'price went from 80 to 100' is a change calculation. Instead of remembering which formula fits, just pick the tab that matches your question.",
        ],
        "howto": [
            "Pick the tab that matches your question: 'X% of Y', 'X is what % of Y', or '% change from X to Y'.",
            "Type your two numbers — the answer appears instantly as you type, no button needed.",
            "Read the formula line under the result to see exactly how the answer was calculated.",
        ],
        "faqs": [
            ("How do I calculate a percentage of a number?",
             "Multiply the number by the percentage and divide by 100. For example, 20% of 150 = 150 × 20 ÷ 100 = 30. The first tab of this calculator does it instantly."),
            ("How do I work out percentage increase?",
             "Subtract the old value from the new value, divide by the old value, and multiply by 100. Going from 80 to 100 is (100 − 80) ÷ 80 × 100 = 25% increase. Use the third tab."),
            ("What is the formula for percentage change?",
             "Percentage change = (new − old) ÷ |old| × 100. A positive result is an increase, a negative result is a decrease. The calculator shows the sign automatically."),
            ("How do I calculate a discount percent?",
             "Divide the amount saved by the original price and multiply by 100. For example, saving $12 on a $60 item is 12 ÷ 60 × 100 = 20% off."),
        ],
    })

    pages.append({
        "slug": "days-between-dates",
        "title": "Days Between Dates Calculator — With Weekdays & Weeks",
        "h1": "Days Between Two Dates",
        "desc": "Free calculator for the number of days between two dates. Shows weeks, weekdays (business days) and total hours. Instant, accurate, no sign-up.",
        "category": "calculator",
        "keyword": "days between dates",
        "tool": "datediff",
        "args": {},
        "intro": [
            "Pick any two dates and this calculator tells you exactly how many days separate them — plus weeks, business days (Monday–Friday) and total hours. Useful for project deadlines, contract notice periods, pregnancy estimates, rental periods, or simple curiosity.",
            "The calculator counts calendar days the way you expect: from a start date to an end date, swapping them automatically if you enter them in reverse. The business-day count excludes Saturdays and Sundays but does not account for public holidays, which vary by country.",
        ],
        "howto": [
            "Set the start date using the date picker (or type it).",
            "Set the end date — the results update instantly.",
            "Read total days first; check weeks, weekdays and hours below for planning detail.",
        ],
        "faqs": [
            ("How do I count days between two dates?",
             "Subtract the start date from the end date. Each date is a day number on the calendar, so the difference is exact — 2026-01-01 to 2026-03-01 is 59 days. The calculator handles leap years for you."),
            ("Does the count include both the start and end day?",
             "The standard convention counts the difference (end minus start), so the start day itself is not counted. If you need both endpoints included, add one day to the result."),
            ("How are business days calculated?",
             "We count Mondays through Fridays between the two dates and skip weekends. Public holidays are not excluded because they differ by country and year."),
            ("Can I calculate days since a past date?",
             "Yes — enter the past date as the start and today as the end. It works for birthdays, anniversaries, or 'days since' counters of any kind."),
        ],
    })

    pages.append({
        "slug": "age-calculator",
        "title": "Age Calculator — Exact Years, Months & Days",
        "h1": "Age Calculator",
        "desc": "Calculate your exact age in years, months and days from your date of birth. Also shows days lived and a countdown to your next birthday.",
        "category": "calculator",
        "keyword": "age calculator",
        "tool": "age",
        "args": {},
        "intro": [
            "Enter a date of birth and get the exact age in years, months and days — the way humans count age, not just a decimal number of years. You also get totals (days lived, hours lived) and a live countdown to the next birthday.",
            "This is handy for official forms that ask age in years/months/days, for parents tracking little kids' ages, or for the timeless question of exactly how old you really are today.",
        ],
        "howto": [
            "Enter the date of birth in the date picker.",
            "The 'as of' date defaults to today; change it to calculate age at any past or future date.",
            "Read the exact age breakdown, then check the next-birthday countdown below.",
        ],
        "faqs": [
            ("How is age calculated exactly?",
             "We count full years first, then full months since the last birthday, then leftover days — exactly how ages are stated on official documents."),
            ("Why do months in an age differ from calendar subtraction?",
             "A 'month' varies from 28 to 31 days. Standard age counting advances the month only on the same day-of-month, which is what this calculator does — the same convention used legally in most countries."),
            ("Does the calculator handle leap-year birthdays (Feb 29)?",
             "Yes. Feb 29 birthdays are treated as Feb 28 in non-leap years for the 'reached next age' date, which matches common legal conventions."),
            ("Can I calculate age at a date in the past or future?",
             "Yes — change the 'as of' date. Age at any historical date (or a future one, which becomes a countdown) works the same way."),
        ],
    })

    pages.append({
        "slug": "tip-calculator",
        "title": "Tip Calculator — Split the Bill, Round Nicely",
        "h1": "Tip Calculator & Bill Splitter",
        "desc": "Calculate the tip and split the bill between friends in seconds. Preset percentages, round-up options and per-person amounts.",
        "category": "calculator",
        "keyword": "tip calculator",
        "tool": "tip",
        "args": {},
        "intro": [
            "Enter the bill, tap a tip percentage, and see the total instantly — then split it across any number of people. The quick buttons cover the customary 15%, 18% and 20%, and you can type any custom percentage.",
            "Tipping customs vary: 15–20% is standard for table service in the US, 10–12.5% is common in the UK where service is sometimes included, and in many countries service is already on the bill. When in doubt, check whether a 'service charge' line already appears on your receipt.",
        ],
        "howto": [
            "Type the bill amount — ignore the tip line if a service charge is already included.",
            "Tap 15%, 18% or 20%, or type a custom tip percentage.",
            "Set the number of people to split; read the per-person amount below.",
        ],
        "faqs": [
            ("How much should I tip?",
             "In the US, 15–20% of the pre-tax bill is customary for good table service. 18% is a safe middle ground. For bars, $1–2 per drink is common."),
            ("Should I tip on the pre-tax or post-tax amount?",
             "Traditional etiquette says tip on the pre-tax total, though many people simply tip on the final number for simplicity. Either is acceptable."),
            ("How do I split a bill including tip?",
             "Add the tip to the total, then divide by the number of people. This calculator does it automatically — just set the people count."),
            ("Is 20% tipping too much?",
             "20% is on the generous end in the US and considered excellent service; 15% is the baseline for acceptable service. Outside the US, check local norms — many cultures tip far less or not at all."),
        ],
    })

    pages.append({
        "slug": "discount-calculator",
        "title": "Percent Off Calculator — Sale Price & Savings",
        "h1": "Percent Off Calculator",
        "desc": "Work out the sale price after any discount, see exactly how much you save, and compare stacked discounts. Instant results.",
        "category": "calculator",
        "keyword": "percent off calculator",
        "tool": "discount",
        "args": {},
        "intro": [
            "See the final price after any percentage discount — and exactly how much you save — before you get to the checkout. Add a second, stacked discount (like 'extra 20% off sale items') to reveal the true final price, because two discounts in a row are not the same as adding them together.",
            "This is the Black Friday and clearance-season companion: type the tag price and the advertised percent off, and know within a second whether the deal is real.",
        ],
        "howto": [
            "Type the original price of the item.",
            "Enter the discount percentage — the sale price and savings appear instantly.",
            "For stacked sales, enter the extra discount to get the true combined final price.",
        ],
        "faqs": [
            ("How do I calculate 20% off a price?",
             "Multiply the price by 0.8 (that keeps 80% of it). For example, 20% off $50 = $50 × 0.8 = $40. The calculator shows the same result with the savings spelled out."),
            ("Is 30% off then 20% off the same as 50% off?",
             "No. Sequential discounts multiply: 30% off then 20% off leaves 0.7 × 0.8 = 56% of the price — effectively a 44% total discount, not 50%."),
            ("How do I find the original price from a sale price?",
             "Divide the sale price by (1 − discount). A $40 item sold at 20% off came from $40 ÷ 0.8 = $50."),
            ("Does the calculator include sales tax?",
             "You can add the tax rate to see the final out-the-door price. Tax normally applies to the discounted price, not the original."),
        ],
    })

    pages.append({
        "slug": "reading-time-calculator",
        "title": "Reading Time Calculator — Words to Minutes",
        "h1": "Reading Time Calculator",
        "desc": "Paste any text and see how long it takes to read or speak. Uses the standard 225 words-per-minute reading speed. Free and instant.",
        "category": "calculator",
        "keyword": "reading time calculator",
        "tool": "readingtime",
        "args": {},
        "intro": [
            "Paste an article, script, essay or email and this calculator estimates how long it takes to read aloud or silently. Silent reading is estimated at 225 words per minute (the adult average for non-fiction); speaking pace is estimated at 140 words per minute, the common rate for presentations.",
            "Writers use it to put accurate '5 min read' labels on articles; students use it to rehearse presentation lengths; speakers use it to check whether a toast will take two minutes or ten.",
        ],
        "howto": [
            "Paste or type your text into the box — the estimate updates as you type.",
            "Read the silent-reading time for article labels, or the speaking time for scripts and speeches.",
            "Adjust with the speed dropdown if you read faster or slower than average.",
        ],
        "faqs": [
            ("How long does it take to read 1000 words?",
             "At the average adult rate of 225 words per minute, 1000 words takes about 4.5 minutes silently. Read aloud at 140 wpm it takes about 7 minutes."),
            ("What is the average reading speed?",
             "Most adults read 200–250 words per minute silently with good comprehension. Slow readers are around 150 wpm; skilled speed readers claim 400+ wpm with reduced comprehension."),
            ("How is speaking time different from reading time?",
             "Speaking is slower — about 130–150 words per minute for a comfortable presentation pace. Use the speaking estimate for scripts, toasts and talks."),
            ("Does this work for essays with a word limit read aloud?",
             "Yes — it is commonly used to check that a class presentation or recorded essay fits an assigned time slot before recording."),
        ],
    })

    pages.append({
        "slug": "typing-speed-test",
        "title": "Typing Speed Test — WPM & Accuracy in 60 Seconds",
        "h1": "Typing Speed Test",
        "desc": "Take a free 60-second typing test and get your WPM and accuracy instantly. No sign-up, works on desktop and mobile keyboards.",
        "category": "calculator",
        "keyword": "typing speed test",
        "tool": "typing",
        "args": {},
        "intro": [
            "One minute, one passage, one honest number: your typing speed in WPM (words per minute) with accuracy. The test starts the moment you begin typing and scores standard WPM — 5 characters per word — the same measure used by professional typing certifications.",
            "Average typists land around 40 WPM; professional roles often want 50–60+; competitive typists exceed 100. Whatever your number, retaking the test weekly is one of the simplest measurable skills to improve.",
        ],
        "howto": [
            "Choose a test length (30 or 60 seconds) and click into the text box.",
            "Type the passage exactly — the timer starts with your first keystroke.",
            "See your WPM and accuracy when the timer ends, then retake to beat your score.",
        ],
        "faqs": [
            ("What is a good typing speed?",
             "40 WPM is average, 50–60 WPM is comfortable for most office jobs, and 70+ WPM puts you in the top tier. Accuracy matters as much as raw speed."),
            ("How is WPM calculated?",
             "Standard WPM counts every 5 typed characters as one word, divided by the time in minutes. Uncorrected errors reduce your accuracy score but gross WPM still counts them — net WPM subtracts errors."),
            ("How can I type faster?",
             "Focus on accuracy first at a slightly lower speed; speed follows accuracy. Keep your eyes on the text, not the keyboard, and practice 10 minutes daily rather than an hour weekly."),
            ("Does keyboard layout matter?",
             "The test works with any layout, including Dvorak and non-US layouts. Mobile on-screen keyboards work too, though thumb typing usually scores lower than full-keyboard touch typing."),
        ],
    })

    # ---------- Converter family ----------
    pages.append(_conv("cm-to-inches", "CM to Inches", "centimeters", "inches", 1 / 2.54, "length",
                       "Centimeters are part of the metric system used almost everywhere in the world; inches are the imperial unit still standard in the United States, and common in the UK and Canada for height and screen sizes. Because 1 inch is officially defined as exactly 2.54 cm, this conversion is precise, not estimated.",
                       "Handy anchors: 30 cm ≈ 11.81 in (a school ruler), 180 cm = 70.87 in (a tall adult height), 2.54 cm = 1 in."))
    pages.append(_conv("inches-to-cm", "Inches to CM", "inches", "centimeters", 2.54, "length",
                       "Inches are used in the US for height, screens and construction; centimeters are the metric standard everywhere else. One inch is officially exactly 2.54 centimeters, so converting is a simple multiplication.",
                       "Handy anchors: 5 ft 6 in = 66 in = 167.64 cm; a 13-inch laptop screen is 33.02 cm diagonal."))
    pages.append(_conv("kg-to-lbs", "KG to LBS", "kilograms", "pounds", 2.2046226218, "weight",
                       "Kilograms are the metric unit of mass used worldwide; pounds remain the everyday unit in the United States. The exact factor is 1 kg = 2.2046226218 lb, defined via the international avoirdupois pound.",
                       "Handy anchors: 70 kg = 154.32 lb (average adult male weight), 1 kg ≈ 2.2 lb for quick mental math."))
    pages.append(_conv("lbs-to-kg", "LBS to KG", "pounds", "kilograms", 1 / 2.2046226218, "weight",
                       "Pounds are the everyday weight unit in the US; kilograms are the scientific and international standard. Divide pounds by 2.2046 to get kilograms — or just type it in below.",
                       "Handy anchors: 150 lb = 68.04 kg; 200 lb = 90.72 kg. For quick estimates, halve your pounds and knock off 10%."))
    pages.append(_conv("celsius-to-fahrenheit", "Celsius to Fahrenheit", "Celsius", "Fahrenheit", None, "temperature",
                       "The US uses Fahrenheit for weather and cooking; most of the world uses Celsius. The formula is °F = °C × 9/5 + 32 — a multiplication plus an offset, which is why the converter (not mental math) is the reliable path.",
                       "Handy anchors: 0 °C = 32 °F (freezing), 20 °C = 68 °F (room temperature), 37 °C = 98.6 °F (body temperature), 100 °C = 212 °F (boiling).", dec=1))
    pages.append(_conv("fahrenheit-to-celsius", "Fahrenheit to Celsius", "Fahrenheit", "Celsius", None, "temperature",
                       "Convert US temperatures to the metric scale used by the rest of the world. The exact formula is °C = (°F − 32) × 5/9. Subtract first, then multiply — doing it in the wrong order is the classic mistake.",
                       "Handy anchors: 32 °F = 0 °C (freezing), 68 °F = 20 °C (room), 98.6 °F = 37 °C (body), 212 °F = 100 °C (boiling).", dec=1))
    pages.append(_conv("miles-to-km", "Miles to KM", "miles", "kilometers", 1.609344, "distance",
                       "Miles are used for road distances in the US and UK; kilometers almost everywhere else. The international mile is defined as exactly 1.609344 kilometers, so this conversion is exact.",
                       "Handy anchors: 5K run = 3.11 mi, 10K = 6.21 mi, a marathon = 26.2 mi = 42.16 km, 60 mph ≈ 97 km/h."))
    pages.append(_conv("km-to-miles", "KM to Miles", "kilometers", "miles", 1 / 1.609344, "distance",
                       "Convert kilometers to miles for road trips, running distances and speed limits. One kilometer is exactly 1/1.609344 miles ≈ 0.6214 miles.",
                       "Handy anchors: 100 km = 62.14 mi, 10 km = 6.21 mi, 1 km ≈ 0.62 mi — so 'km × 0.62' is a decent mental shortcut."))
    pages.append(_conv("mm-to-inches", "MM to Inches", "millimeters", "inches", 1 / 25.4, "length",
                       "Millimeters are the metric unit for small precision measurements — jewelry, tools, camera gear, 3D printing; inches remain the everyday small-length unit in the US. Because one inch is officially exactly 25.4 millimeters, this conversion is precise to any number of decimal places.",
                       "Handy anchors: 25.4 mm = 1 in, 10 mm = 0.39 in (about 4/10 of an inch), 100 mm = 3.94 in, 6.35 mm = exactly 1/4 inch (the common drill-bit size)."))
    pages.append(_conv("meters-to-feet", "Meters to Feet", "meters", "feet", 3.280839895, "length",
                       "Meters are the metric standard for height and room dimensions; feet remain the everyday unit in the US. One meter is exactly 3.280839895 feet, so converting is a single multiplication — and the reverse uses the clean factor 0.3048.",
                       "Handy anchors: 1 m = 3.28 ft, 2 m = 6.56 ft (tall doorway height), 100 m = 328.08 ft (a short city block)."))
    pages.append(_conv("feet-to-meters", "Feet to Meters", "feet", "meters", 0.3048, "length",
                       "Feet are the US unit for height, rooms and real estate; meters are the global metric standard. One foot is officially exactly 0.3048 meters, making this conversion precise at any scale.",
                       "Handy anchors: 5 ft = 1.52 m, 6 ft = 1.83 m (average adult heights), 10 ft = 3.05 m (basketball rim)."))
    pages.append(_conv("ounces-to-grams", "Ounces to Grams", "ounces", "grams", 28.349523125, "weight",
                       "Ounces are the US unit for food portions, ingredients and precious metals (technically troy ounces for metals); grams are the metric standard used on nutrition labels worldwide. One avoirdupois ounce is exactly 28.349523125 grams.",
                       "Handy anchors: 1 oz = 28.35 g, 4 oz = 113.40 g (a burger patty), 8 oz = 226.80 g (half a pound)."))
    pages.append(_conv("grams-to-ounces", "Grams to Ounces", "grams", "ounces", 1 / 28.349523125, "weight",
                       "Convert grams — the metric unit on every nutrition label — to ounces, the US kitchen and grocery unit. Divide grams by 28.3495 or just type it below for full precision.",
                       "Handy anchors: 100 g = 3.53 oz (a chocolate bar), 250 g = 8.82 oz (a cup of butter), 500 g = 17.64 oz (just over a pound).", dec=3))
    pages.append(_conv("liters-to-gallons", "Liters to Gallons", "liters", "gallons (US)", 0.2641720524, "volume",
                       "Liters are the metric unit for fuel and drinks; US gallons remain the standard at American pumps and supermarkets. One US gallon is exactly 3.785411784 liters, so a liter is about a quarter of a gallon.",
                       "Handy anchors: 1 L = 0.26 gal, 10 L = 2.64 gal, 55 L = 14.53 gal (a car fuel tank). Note: UK (imperial) gallons are bigger — 4.546 L."))
    pages.append(_conv("gallons-to-liters", "Gallons to Liters", "gallons (US)", "liters", 3.785411784, "volume",
                       "Convert US gallons to liters for fuel economy comparisons, recipes and aquarium sizes. One US gallon is exactly 3.785411784 liters — multiply and done.",
                       "Handy anchors: 1 gal = 3.79 L, 5 gal = 18.93 L (a water-cooler jug), 15 gal = 56.78 L. UK imperial gallons differ: 1 imp gal = 4.55 L."))
    pages.append(_conv("sqft-to-sqm", "Square Feet to Square Meters", "square feet", "square meters", 0.09290304, "area",
                       "Square feet dominate US real-estate listings; square meters are the international standard for apartments and offices. One square foot is exactly 0.09290304 square meters — roughly a tenth.",
                       "Handy anchors: 100 sq ft = 9.29 sq m (a small bedroom), 500 sq ft = 46.45 sq m (a studio), 1,000 sq ft = 92.90 sq m (a two-bed apartment)."))
    pages.append(_conv("sqm-to-sqft", "Square Meters to Square Feet", "square meters", "square feet", 10.76391042, "area",
                       "Convert square meters — the global real-estate unit — to square feet for US listings and floor plans. One square meter is 10.7639 square feet, so a handy mental shortcut is '×10 then add a bit'.",
                       "Handy anchors: 10 sq m = 107.64 sq ft, 50 sq m = 538.20 sq ft (a one-bed flat), 100 sq m = 1,076.39 sq ft."))
    pages.append(_conv("stone-to-kg", "Stone to KG", "stone", "kilograms", 6.35029318, "weight",
                       "The stone is the traditional British unit for body weight — Brits say they weigh '11 stone', never '154 pounds'. One stone is exactly 6.35029318 kilograms (14 pounds), so converting is a single multiplication.",
                       "Handy anchors: 10 st = 63.50 kg, 11 st = 69.85 kg (UK average adult male), 12 st = 76.20 kg, 1 st = 14 lb = 6.35 kg."))
    pages.append(_conv("kg-to-stone", "KG to Stone", "kilograms", "stone", 1 / 6.35029318, "weight",
                       "Convert your weight in kilograms to the British stone unit — the way UK scales, GP charts and newspaper height-and-weight columns actually read. Divide kilograms by 6.35029318, or just type it below.",
                       "Handy anchors: 60 kg = 9.45 st, 70 kg = 11.02 st, 80 kg = 12.60 st, 100 kg = 15.75 st. For quick mental math: divide kg by 6.35."))
    pages.append(_conv("ml-to-oz", "ML to OZ", "milliliters", "fluid ounces (US)", 1 / 29.5735295625, "volume",
                       "Nutrition labels outside the US print milliliters; American labels and recipe cards use fluid ounces. One US fluid ounce is 29.5735 milliliters, so 30 ml is a hair more than an ounce — close enough for the kitchen, not for chemistry.",
                       "Handy anchors: 30 ml ≈ 1 fl oz, 250 ml ≈ 8.45 fl oz (a standard glass), 355 ml = 12 fl oz (a soda can), 750 ml = 25.36 fl oz (a wine bottle).", dec=2))
    pages.append(_conv("minutes-to-hours", "Minutes to Hours", "minutes", "hours", 1 / 60, "time",
                       "Payroll systems, timesheets and invoices want hours in decimals — 7 hours 30 minutes must be entered as 7.5, not 7:30. Divide minutes by 60 for the decimal form; the converter handles any value including awkward ones like 17 minutes.",
                       "Handy anchors: 30 min = 0.50 hr, 15 min = 0.25 hr, 45 min = 0.75 hr, 90 min = 1.50 hr. Multiply hours by 60 to go back.", dec=3))
    pages.append(_conv("inches-to-feet", "Inches to Feet", "inches", "feet", 1 / 12, "length",
                       "Both are US customary units, but they answer different questions: inches for screens, tools and small measurements; feet for height, rooms and lumber. Divide inches by 12 to get feet — 60 inches is 5 feet exactly.",
                       "Handy anchors: 12 in = 1 ft, 60 in = 5 ft, 66 in = 5 ft 6 in, 72 in = 6 ft. For mixed units like 5 ft 7 in, convert the leftover inches separately.", dec=3))
    pages.append(_conv("kmh-to-mph", "KMH to MPH", "kilometers per hour", "miles per hour", 0.6213711922, "speed",
                       "Speed limits and car dashboards use km/h almost everywhere; the US and UK still speak in mph. One km/h is 0.6214 mph, so 100 km/h on a European motorway is a legal 62 mph — and 60 mph is a ticket-prone 96.6 km/h.",
                       "Handy anchors: 30 km/h = 18.6 mph (city), 50 km/h = 31.1 mph, 100 km/h = 62.1 mph (motorway), 120 km/h = 74.6 mph. Quick trick: km/h × 0.62.", dec=1))
    pages.append(_conv("mph-to-kmh", "MPH to KMH", "miles per hour", "kilometers per hour", 1.609344, "speed",
                       "Driving from the US or UK into a km/h country? The numbers on the dashboard and the signs suddenly disagree. One mph is exactly 1.609344 km/h — multiply by 1.6 for a road-safe estimate.",
                       "Handy anchors: 30 mph = 48.3 km/h, 60 mph = 96.6 km/h, 70 mph = 112.7 km/h (UK motorway), 80 mph = 128.7 km/h. Quick trick: mph × 1.6."))
    pages.append(_conv("cups-to-ml", "Cups to ML", "cups (US)", "milliliters", 236.5882365, "volume",
                       "US recipes measure by cups; nearly every other country — and every scale — uses milliliters. One US customary cup is 236.588 milliliters, which is why American and metric recipes never quite line up without a converter.",
                       "Handy anchors: 1 cup = 236.6 ml (round to 240 when eyeballing), 2 cups = 473 ml (a pint), 4 cups = 946 ml (a quart), half a cup = 118 ml.", dec=1))
    pages.append(_conv("tablespoons-to-teaspoons", "Tablespoons to Teaspoons", "tablespoons", "teaspoons", 3, "volume",
                       "The most common baking substitution there is: 1 tablespoon (tbsp) equals exactly 3 teaspoons (tsp). When you are out of one spoon size mid-recipe, the conversion saves the batch — no scale, no math beyond ×3.",
                       "Handy anchors: 1 tbsp = 3 tsp, 2 tbsp = 6 tsp, 1 tbsp = 15 ml, 1 tsp = 5 ml. Four tablespoons = a quarter cup."))
    pages.append(_conv("ounces-to-cups", "Ounces to Cups", "fluid ounces", "cups (US)", 1 / 8, "volume",
                       "American recipes bounce between fluid ounces and cups mid-ingredient-list — a can says 12 fl oz, the recipe asks for 1½ cups. Since one US cup is exactly 8 fluid ounces, the conversion is a simple divide by 8.",
                       "Handy anchors: 8 fl oz = 1 cup, 12 fl oz = 1.5 cups (a soda can), 16 fl oz = 2 cups (a pint), 32 fl oz = 4 cups (a quart).", dec=2))
    pages.append(_conv("liters-to-pints", "Liters to Pints", "liters", "pints (US)", 1 / 0.473176473, "volume",
                       "Convert liters — on every bottle outside the US — into American pints for recipes, brewing and bar orders. One liter is just over 2.11 US pints, so a liter of beer is two pints plus a generous head.",
                       "Handy anchors: 1 L = 2.11 pt, 2 L = 4.23 pt (a big bottle), 0.5 L = 1.06 pt. UK pints are bigger: 1 L = 1.76 imperial pints."))
    pages.append(_conv("kilograms-to-stones", "KG to Stone", "kilograms", "stone", 1 / 6.35029318, "weight",
                       "Reading a UK gym programme or a British boxing weigh-in with metric numbers? Kilograms convert to stone by dividing by 6.35029318 — the unit Brits use for body weight in everyday speech.",
                       "Handy anchors: 50 kg = 7.87 st, 70 kg = 11.02 st, 90 kg = 14.17 st, 100 kg = 15.75 st."))
    pages.append(_conv("tablespoons-to-cups", "Tablespoons to Cups", "tablespoons", "cups (US)", 1 / 16, "volume",
                       "Scaling recipes up or down means hopping between tablespoons and cups — and 16 tablespoons per cup is not mental math anyone enjoys mid-recipe. Type the tablespoons, get the cups, get back to the oven.",
                       "Handy anchors: 4 tbsp = 1/4 cup, 8 tbsp = 1/2 cup (a stick of butter), 12 tbsp = 3/4 cup, 16 tbsp = 1 cup.", dec=3))
    pages.append(_conv("quarts-to-liters", "Quarts to Liters", "quarts (US)", "liters", 0.946352946, "volume",
                       "Engine oil, stock pots and paint cans are measured in quarts in the US and liters everywhere else — and they are annoyingly close in size, which is exactly why guessing goes wrong. One US quart is 0.946353 liters, just shy of a liter.",
                       "Handy anchors: 1 qt = 0.95 L (an oil change), 4 qt = 3.79 L (a gallon), 6 qt = 5.68 L (an Instant Pot)."))
    pages.append(_conv("quarts-to-gallons", "Quarts to Gallons", "quarts (US)", "gallons (US)", 1 / 4, "volume",
                       "The last hop on the US volume ladder: 4 quarts make a gallon, so divide by 4 — or let the converter handle the awkward numbers like 5 quarts of soup for a party of twelve.",
                       "Handy anchors: 4 qt = 1 gal, 8 qt = 2 gal, 6 qt = 1.5 gal. Oil changes: most cars take 4–6 quarts, roughly 1–1.5 gallons."))
    pages.append(_conv("liters-to-quarts", "Liters to Quarts", "liters", "quarts (US)", 1 / 0.946352946, "volume",
                       "Recipes and engine capacities in liters need to become quarts for US kitchens and garages. One liter is 1.05669 US quarts — slightly bigger, which is why a 5.7-liter V8 is a 6-quart oil change territory.",
                       "Handy anchors: 1 L = 1.06 qt, 2 L = 2.11 qt, 4 L = 4.23 qt (just over a gallon), 6 L = 6.34 qt."))
    pages.append(_conv("gallons-to-pints", "Gallons to Pints", "gallons (US)", "pints (US)", 8, "volume",
                       "The US volume ladder is delightfully odd — 8 pints to a gallon, 2 pints to a quart, 4 quarts to a gallon — and milk comes in all of them. One US gallon is exactly 8 US pints, so multiply by 8 and pour.",
                       "Handy anchors: 1 gal = 8 pt, 0.5 gal = 4 pt (half-gallon of milk), 2 gal = 16 pt. UK imperial pints are bigger: 1 imperial gallon = 8 imperial pints but 20% more liquid."))
    pages.append(_conv("pounds-to-ounces", "Pounds to Ounces", "pounds", "ounces", 16, "weight",
                       "US kitchens and post offices both live in pounds and ounces — 16 ounces to the pound, always. Convert a 2.5-pound flour bag into ounces, or a newborn's weight from pounds into ounces for the baby book.",
                       "Handy anchors: 1 lb = 16 oz, 0.5 lb = 8 oz, 2 lb = 32 oz. Baby weights: 7 lb 8 oz = 120 oz."))
    pages.append(_conv("grams-to-pounds", "Grams to Pounds", "grams", "pounds", 1 / 453.59237, "weight",
                       "Convert grams — the unit on every packaged-food label — to pounds, the unit on every American bathroom scale. One pound is exactly 453.59237 grams, so 500 g is just over a pound and 1,000 g (a kilo) is 2.2 pounds.",
                       "Handy anchors: 250 g = 0.55 lb, 454 g = 1 lb (a butter block), 1,000 g = 2.20 lb. Quick trick: grams ÷ 454."))
    pages.append(_conv("stones-to-pounds", "Stone to Pounds", "stone", "pounds", 14, "weight",
                       "Within the British weight system you often need both: someone weighs '11 and a half stone', a US form wants pounds. One stone is exactly 14 pounds — the one conversion in this family that is pure mental math, but this one's faster and shows decimals.",
                       "Handy anchors: 1 st = 14 lb, 10 st = 140 lb, 12 st = 168 lb, 15 st = 210 lb. Halve the stone figure and add a tenth for rough pounds."))
    pages.append(_conv("ml-to-l", "ML to Liters", "milliliters", "liters", 1 / 1000, "volume",
                       "Milliliters handle drinks, doses and recipes; liters handle bottles, tanks and fuel. The conversion is a clean divide by 1,000 — but doing it while pouring is how people end up with 10x the cordial in the glass. This one keeps it straight.",
                       "Handy anchors: 100 ml = 0.1 L, 330 ml = 0.33 L (a can), 500 ml = 0.5 L (a water bottle), 1,500 ml = 1.5 L (a big soda bottle)."))
    pages.append(_conv("cups-to-fluid-ounces", "Cups to Fluid Ounces", "cups (US)", "fluid ounces", 8, "volume",
                       "The reverse of the classic: your recipe asks for 2 cups, the measuring jug only shows fluid ounces. One US cup is exactly 8 fluid ounces, so multiply by 8 — and stop doing it in your head while holding a whisk.",
                       "Handy anchors: 1 cup = 8 fl oz, 1.5 cups = 12 fl oz, 2 cups = 16 fl oz (a pint), 4 cups = 32 fl oz (a quart)."))
    pages.append(_conv("yards-to-meters", "Yards to Meters", "yards", "meters", 0.9144, "length",
                       "Yards rule American football fields, golf courses and fabric counters; meters rule everything else. One yard is exactly 0.9144 meters — so a 100-yard football field is 91.44 meters of pure metric confusion.",
                       "Handy anchors: 1 yd = 0.91 m, 10 yd = 9.14 m, 100 yd = 91.44 m, 1 m = 1.09 yd (slightly more than a yard)."))
    pages.append(_conv("pints-to-liters", "Pints to Liters", "pints (US)", "liters", 0.473176473, "volume",
                       "The pint is the unit of pub culture — but it depends where you drink. A US pint is 473 ml; an imperial (UK) pint is a heftier 568 ml. This converter uses the US pint, the one on American labels and beer taps.",
                       "Handy anchors: 1 US pint = 0.47 L, 2 pints = 0.95 L (a quart), 8 pints = 3.79 L (a gallon). UK drinkers: 1 imperial pint = 0.57 L."))
    pages.append(_conv("inches-to-mm", "Inches to MM", "inches", "millimeters", 25.4, "length",
                       "Precision work — drill bits, camera mounts, 3D printing, jewelry — lives in millimeters, while US tools and hardware still speak inches. One inch is officially exactly 25.4 millimeters, so this conversion is precise to any decimal place.",
                       "Handy anchors: 1 in = 25.4 mm, 1/2 in = 12.7 mm, 1/4 in = 6.35 mm, 2 in = 50.8 mm. Woodworkers: 3/4 in stock = 19.05 mm."))
    pages.append(_conv("feet-to-cm", "Feet to CM", "feet", "centimeters", 30.48, "length",
                       "Convert US height and furniture measurements straight into centimeters in one hop — no inches in between. One foot is exactly 30.48 centimeters, so 6 feet is 182.88 cm and a 5-foot sofa is 152.4 cm.",
                       "Handy anchors: 1 ft = 30.48 cm, 5 ft = 152.4 cm, 6 ft = 182.88 cm, 7 ft = 213.36 cm (a door is 6 ft 8 in = 203 cm)."))

    # ---------- Text & generator family ----------
    pages.append({
        "slug": "word-counter",
        "title": "Word Counter — Words, Characters, Sentences & Reading Time",
        "h1": "Word Counter",
        "desc": "Count words, characters (with and without spaces), sentences and paragraphs instantly. Live statistics with estimated reading time.",
        "category": "text",
        "keyword": "word counter",
        "tool": "wordcounter",
        "args": {},
        "intro": [
            "Type or paste text and get a live count of words, characters, sentences and paragraphs — everything updates as you type, entirely in your browser (nothing is uploaded). Reading-time estimate included, using the standard 225 words per minute.",
            "Essay word limits, tweet and meta-description character limits, abstract minimums, cover-letter lengths — every writing context has a number attached. This counter gives you that number without the clutter of a full editor.",
        ],
        "howto": [
            "Paste your text into the box — statistics update on every keystroke.",
            "Check words against your limit; check characters-with-spaces for platforms that count them.",
            "Clear the box to start over; your text never leaves your device.",
        ],
        "faqs": [
            ("How do you count words?",
             "Words are sequences of characters separated by whitespace. 'Don't' is one word; 'state-of-the-art' is one word; numbers count as words. This matches how Word and Google Docs count."),
            ("Do characters include spaces?",
             "We show both: characters with spaces (used by most platforms like Twitter/X) and without spaces (used in some academic contexts). Check which one your limit refers to."),
            ("How many words is a 5 minute speech?",
             "About 700 words at the standard speaking pace of 140 words per minute. Use the reading-time figure on this page with the speaking rate for rehearsal."),
            ("Is my text uploaded anywhere?",
             "No. The counting runs entirely in your browser with JavaScript — nothing is transmitted, stored or logged. You can disconnect from the internet and it still works."),
        ],
    })

    pages.append({
        "slug": "case-converter",
        "title": "Case Converter — UPPERCASE, lowercase, Title Case & More",
        "h1": "Case Converter",
        "desc": "Convert text to UPPERCASE, lowercase, Title Case, Sentence case, camelCase, snake_case and kebab-case. One click, instant, private.",
        "category": "text",
        "keyword": "case converter",
        "tool": "case",
        "args": {},
        "intro": [
            "Paste text, click a case, copy the result. Beyond the basics (UPPERCASE, lowercase, Title Case, Sentence case), it also outputs camelCase, snake_case and kebab-case — the formats developers and writers constantly need for variable names, URLs, filenames and hashtags.",
            "Everything runs locally in your browser, so it is safe for private or sensitive text. There is no length limit — convert a headline or an entire chapter.",
        ],
        "howto": [
            "Paste or type your text into the input box.",
            "Click the case style you need — the output box updates instantly.",
            "Use the copy button to grab the converted text.",
        ],
        "faqs": [
            ("What is Title Case?",
             "Title Case capitalizes the first letter of each major word ('The Quick Brown Fox'). Minor words like 'a', 'of', 'the' are traditionally lowercase unless they start the title."),
            ("What is the difference between camelCase and snake_case?",
             "camelCase removes spaces and capitalizes each word after the first ('myVariableName'). snake_case replaces spaces with underscores and lowercases everything ('my_variable_name'). kebab-case uses hyphens ('my-variable-name')."),
            ("How do I fix text that's ALL IN CAPS?",
             "Click 'Sentence case' — it lowercases everything except the first letter of each sentence. Or 'Title Case' if it is a heading."),
            ("Is my text sent to a server?",
             "No. All conversion happens in your browser with JavaScript. Nothing is uploaded, logged or stored — refresh the page and it is gone."),
        ],
    })

    pages.append({
        "slug": "random-name-generator",
        "title": "Random Name Generator — Fantasy, Team & Character Names",
        "h1": "Random Name Generator",
        "desc": "Generate random names for fantasy characters, game teams, babies' name inspiration, or username ideas. Click for fresh names, tap to copy.",
        "category": "generator",
        "keyword": "random name generator",
        "tool": "names",
        "args": {},
        "intro": [
            "Stuck naming a D&D character, a fantasy football team, a game guild, or a fictional town? Hit generate for a fresh batch of twelve names, drawn from curated syllable sets that produce plausible, pronounceable names — not keyboard mash. Click any name to copy it.",
            "Switch between styles: fantasy names with elvish and heroic flavors, punchy team names for leagues and offices, and character names for fiction. Every batch is different; there are millions of combinations.",
        ],
        "howto": [
            "Pick a style: fantasy, team, or character names.",
            "Click Generate for a new batch of twelve; click any name to copy it to your clipboard.",
            "Keep generating until one sticks — or mix a generated first name with your own surname.",
        ],
        "faqs": [
            ("Are the names unique?",
             "Each batch is randomly drawn from millions of combinations, so exact repeats are rare but possible. Names are generated, not checked against trademarks — do your own search before using one commercially."),
            ("Can I use these names for my novel or game?",
             "Yes — generated names are yours to use. They are assembled from syllable patterns, not taken from any existing name list of real people."),
            ("How do I get better fantasy names?",
             "Try the fantasy style for a few batches, then customize: swap endings (-iel, -or, -yn) or shorten to two syllables. Shorter names read as more grounded; flowing endings read as elvish."),
            ("Does it work offline?",
             "Yes. Generation runs in your browser with JavaScript — no network needed after the page loads, and nothing you generate is recorded."),
        ],
    })

    pages.append({
        "slug": "password-generator",
        "title": "Strong Password Generator — Random & Secure, 100% Offline",
        "h1": "Random Password Generator",
        "desc": "Generate strong random passwords with one click. Choose length and character sets. Runs entirely in your browser — passwords never leave your device.",
        "category": "generator",
        "keyword": "random password generator",
        "tool": "password",
        "args": {},
        "intro": [
            "Generate cryptographically strong random passwords using your browser's built-in secure random number generator (WebCrypto). Choose length and character sets; every password is created locally on your device and is never transmitted, logged or stored — you can even disconnect from the internet and it keeps working.",
            "For most accounts, a 16-character password with mixed character types is the sweet spot of strength and memorability-with-a-manager. For high-value accounts (email, banking, password manager master key), go 20+ characters.",
        ],
        "howto": [
            "Set the length (16 is a good default; 20+ for critical accounts).",
            "Toggle character types — keep symbols off only if the site rejects them.",
            "Click Generate, then use the copy button and paste directly into your password manager.",
        ],
        "faqs": [
            ("What makes a password strong?",
             "Length and randomness. A password's strength against guessing grows exponentially with length — each extra character multiplies the work. Random 16-character passwords are beyond practical brute-force; human-chosen passwords are not."),
            ("Are these passwords safe to use?",
             "Yes. They are generated with the browser's WebCrypto API (a cryptographically secure random source) and never leave your device — there is no server involved in generation at all."),
            ("Should I use a passphrase instead?",
             "Passphrases of 4–5 random words are as strong as long random passwords and easier to type manually. For accounts you type daily, a passphrase is a great choice; for everything else, generate and store in a password manager."),
            ("Why shouldn't I reuse passwords?",
             "Data breaches leak passwords constantly; reused passwords let one leak compromise every account that shares it. Unique passwords (stored in a manager) contain the damage to a single site."),
        ],
    })

    pages.append({
        "slug": "random-number-generator",
        "title": "Random Number Generator — Truly Random, Cryptographically Secure",
        "h1": "Random Number Generator",
        "desc": "Generate random numbers in any range, with or without duplicates. Uses your browser's cryptographic random source — perfect for draws, games and picking winners.",
        "category": "generator",
        "keyword": "random number generator",
        "tool": "randomnum",
        "args": {},
        "intro": [
            "Pick random numbers in any range — for prize draws, raffle winners, picking who goes first, sampling, or games. Choose whole numbers or decimals, allow or ban duplicates, and generate up to 100 at once. Results come from your browser's WebCrypto cryptographically secure random source, not a predictable pseudo-random shortcut.",
            "Fairness matters when a draw has real consequences. Cryptographic randomness is the same class of generator used for security keys, so every number in the range is equally likely and impossible to predict in advance — even by this page.",
        ],
        "howto": [
            "Set the minimum and maximum of your range — anything from -1,000,000 to 1,000,000.",
            "Choose how many numbers you need, and toggle whole-numbers-only or no-duplicates as you prefer.",
            "Hit Generate — results appear instantly; generate again for a fresh set.",
        ],
        "faqs": [
            ("Is this random number generator truly random?",
             "It uses the browser's WebCrypto API — a cryptographically secure random source seeded by your operating system. This is the same quality of randomness used for encryption keys, which is far stronger than typical Math.random() generators."),
            ("Can I use it for a raffle or prize draw?",
             "Yes. Set the range to your number of entries, turn on 'no duplicates' if you are picking multiple winners, and generate. The cryptographic source makes the draw fair and verifiable."),
            ("How do I generate a number between 1 and 100?",
             "Set minimum to 1, maximum to 100, count to 1, keep 'whole numbers only' on, and press Generate. Both endpoints of the range are included."),
            ("What happens if duplicates are off and the range is too small?",
             "You cannot pick 50 unique numbers from a 10-number range, so the tool shows a clear message instead of looping forever. Turn duplicates on or widen the range."),
        ],
    })

    pages.append({
        "slug": "words-to-pages",
        "title": "Words to Pages Converter — Essays, Reports & Assignments",
        "h1": "Words to Pages Converter",
        "desc": "Convert word counts to page estimates for essays and reports: 250 words per page single-spaced, 500 double-spaced. Handles 300, 500, 1000, 2500 words and more.",
        "category": "calculator",
        "keyword": "words to pages",
        "tool": "wordspages",
        "args": {},
        "intro": [
            "Convert any word count into an estimated page count for an essay, report or assignment. The calculation uses the academic standard: 12-point Times New Roman, one-inch margins, ~250 words per single-spaced page or ~500 words per double-spaced page.",
            "It answers the question behind every assignment brief: 'how long is 500 words?', 'is 1000 words a lot?' (about two double-spaced pages — not much), and 'how many pages is my 3000-word dissertation chapter?' (six single-spaced). Exact layout varies with fonts and headings, so treat the result as a solid estimate.",
        ],
        "howto": [
            "Type your word count — or paste text and let the counter fill it in.",
            "Pick single or double spacing to match your assignment's formatting rules.",
            "Read the estimated page count; check the handwriting note if your school counts handwritten pages.",
        ],
        "faqs": [
            ("How many pages is 500 words?",
             "About 1 page single-spaced or 2 pages double-spaced, using the standard 12-point font with one-inch margins. Handwritten, it is roughly 2 pages."),
            ("How many pages is 1000 words?",
             "About 2 pages single-spaced or 4 pages double-spaced. Most 'short essay' assignments of 1000 words are a 4-page double-spaced document."),
            ("How many words fit on one page?",
             "Single-spaced: about 500–550 words. Double-spaced: about 250–275 words. Headings, quotes and paragraph breaks reduce the count, which is why estimates use the lower numbers."),
            ("Does font size change the answer?",
             "Yes — this converter assumes 12-point Times New Roman (or Arial, similar metrics) with 1-inch margins. A larger 14-point font adds roughly 20% more pages; tighter layouts fit more."),
        ],
    })

    pages.append({
        "slug": "roman-numerals-converter",
        "title": "Roman Numerals Converter — Numbers ⇄ Roman (1–3999)",
        "h1": "Roman Numerals Converter",
        "desc": "Convert numbers to Roman numerals and back instantly: 2026 = MMXXVI. Full 1–3999 range, bidirectional, with the subtraction rules explained. Great for dates, tattoos and homework.",
        "category": "converter",
        "keyword": "roman numerals converter",
        "tool": "roman",
        "args": {},
        "intro": [
            "Type a number to see it in Roman numerals — or type Roman numerals to see the number. The full classic range 1–3999 is supported, both directions, instantly. Wedding dates, tattoo ideas, movie credits, chapter numbers and homework all land here eventually.",
            "Roman numerals obey a small set of rules: I, X, C and M repeat; V, L and D never do; and a smaller symbol before a larger one subtracts (IV = 4, CM = 900). The converter produces the standard modern form and rejects invalid strings like IIIV rather than guessing.",
        ],
        "howto": [
            "Type an ordinary number (1–3999) in the first box — the Roman form appears as you type.",
            "Type Roman numerals in the second box (like MMXXVI) — the number appears instantly.",
            "Both boxes stay in sync, so you can flip direction at any time without pressing anything.",
        ],
        "faqs": [
            ("What is 2026 in Roman numerals?",
             "2026 is MMXXVI: MM (2000) + XX (20) + VI (6). Type any year into the converter to see it instantly — 2025 is MMXXV, 2027 will be MMXXVII."),
            ("Why is 4 written IV and not IIII?",
             "The modern standard uses subtraction: a smaller numeral before a larger one means 'take it away', so IV = 5 − 1 = 4. Old clock faces often show IIII for visual balance, but IV is the correct written form."),
            ("What is the biggest number in Roman numerals?",
             "With the standard seven symbols and no overline notation, the largest is 3999 (MMMCMXCIX). Larger numbers historically used a bar over a symbol to multiply by 1,000 — the converter sticks to the standard 1–3999 range."),
            ("Are zero and negative numbers possible in Roman numerals?",
             "No. The Romans had no symbol for zero and no negative numbers, which is one reason the system was eventually replaced by Arabic numerals for mathematics."),
        ],
    })

    pages.append({
        "slug": "sales-tax-calculator",
        "title": "Sales Tax Calculator — Add or Remove Tax From Any Price",
        "h1": "Sales Tax Calculator",
        "desc": "Add sales tax to a price, or remove tax to find the pre-tax amount. Two-direction calculator for US shoppers, freelancers and small businesses. Instant results.",
        "category": "calculator",
        "keyword": "sales tax calculator",
        "tool": "salestax",
        "args": {},
        "intro": [
            "Two directions, one tool: type a price and a tax rate to see the total at checkout, or type a tax-inclusive total and strip the tax back out to find the pre-tax amount — the thing freelancers need when an invoice total includes VAT or sales tax and the books need it separate.",
            "US sales tax rates vary by state, county and even city, from 0% to over 10%, which is why the rate is always an input here, never a guess. Enter the rate printed on your receipt or your state's published rate and everything calculates instantly.",
        ],
        "howto": [
            "To add tax: type the pre-tax price and your tax rate — the tax amount and total appear instantly.",
            "To remove tax: switch to the reverse tab, type the tax-inclusive total and the rate — the pre-tax price appears.",
            "Check the breakdown line for the exact tax amount to record in your books.",
        ],
        "faqs": [
            ("How do I calculate sales tax backwards from a total?",
             "Divide the total by (1 + rate). A $110 total at 10% tax contains $10 of tax: 110 ÷ 1.10 = $100 pre-tax. The reverse tab does this instantly — subtracting 10% directly would give the wrong answer ($99)."),
            ("How much is sales tax in the US?",
             "There is no federal sales tax. State rates run from 0% (Oregon, Montana, New Hampshire) to 7.25%+ in California, and local additions can push combined rates past 9–10% in some cities. Use the combined rate for your address."),
            ("Is sales tax charged on top of shipping?",
             "Increasingly yes — most states now require tax on shipping when the shipped item is taxable. The rules are state-specific, so check your state's department of revenue page."),
            ("Why can't I just subtract the tax percentage from the total?",
             "Because the tax was calculated on the smaller pre-tax amount. Subtracting 10% from $110 gives $99, but the true pre-tax price is $100. Division by (1 + rate) is the correct reversal — this calculator handles it."),
        ],
    })

    pages.append({
        "slug": "grade-calculator",
        "title": "Grade Calculator — Test Score to Percentage & Letter Grade",
        "h1": "Grade Calculator",
        "desc": "Turn any test score into a percentage and letter grade instantly. Enter points earned and points possible — see the grade, plus what you'd need on the final.",
        "category": "calculator",
        "keyword": "grade calculator",
        "tool": "grade",
        "args": {},
        "intro": [
            "Enter the points you earned and the points possible, and get your percentage and letter grade instantly — A through F on the standard US scale. Built for the post-exam ritual of every student: 'what did 42 out of 50 actually get me?' (84% — a solid B).",
            "It also answers the forward-looking question: what do you need on the final to hit your target grade? Enter what you have so far plus the final's weight, and the target box shows the exact score required — sometimes reassuring, sometimes a wake-up call.",
        ],
        "howto": [
            "Type the points you earned and the total points possible for the test or class.",
            "Read your percentage and letter grade — the scale is shown below for reference.",
            "For finals planning, enter your current grade and the final's weight to see the score you need.",
        ],
        "faqs": [
            ("What percentage is an A?",
             "On the standard US scale, an A is 90% or above, B is 80–89%, C is 70–79%, D is 60–69%, and F is below 60%. Some schools use plus/minus cutoffs (93% = A, 90% = A−); check your syllabus for the exact scheme."),
            ("How do I calculate my grade percentage?",
             "Divide points earned by points possible and multiply by 100. Scoring 85 out of 100 points is 85%; scoring 17 out of 20 is also 85% — the ratio is what matters, not the raw numbers."),
            ("What do I need on the final to pass?",
             "Use the target-grade box: enter your current average and the final's share of the total grade, and it shows the exact final-exam percentage required. If the number is over 100%, the target is mathematically out of reach — talk to your teacher about extra credit."),

            ("Does it work for weighted grading categories?",
             "Yes for a single category: enter your average within that category and its weight in the target section. For multiple weighted categories, average each category first, then combine by weight before entering it."),
        ],
    })

    pages.append({
        "slug": "duplicate-line-remover",
        "title": "Remove Duplicate Lines Online — Keep Order, Instant Results",
        "h1": "Duplicate Line Remover",
        "desc": "Paste any list or text and remove duplicate lines instantly — original order preserved. Shows exactly how many lines were removed. 100% in-browser, nothing uploaded.",
        "category": "text",
        "keyword": "remove duplicate lines",
        "tool": "dedupe",
        "args": {},
        "intro": [
            "Paste a list — keywords, emails, log lines, CSV rows, URLs — and strip out every duplicate while keeping the first-seen order. Cleaned output appears instantly with a count of what was removed, and one click copies the result.",
            "This is the everyday data-cleaning chore: deduplicating keyword exports before analysis, merging mailing lists, tidying SQL results, or trimming a wordlist. Everything runs locally in your browser — your data never touches a server, which matters when the list contains something private.",
        ],
        "howto": [
            "Paste your text or list into the input box.",
            "The cleaned output appears instantly — duplicates removed, first-seen order kept.",
            "Check the removed-lines count, then hit Copy to take the result.",
        ],
        "faqs": [
            ("How does it decide which duplicate to keep?",
             "It keeps the first occurrence and drops every later repeat — so the order of your original list is preserved. This matters for ranked lists, logs and timelines."),
            ("Does it treat lines that differ only by spaces as duplicates?",
             "Each line is compared exactly, including leading and trailing spaces. If your data has messy whitespace, trim the lines first — case is also preserved (Apple and apple are different)."),
            ("Is there a size limit?",
             "The practical limit is your browser tab's memory — lists of hundreds of thousands of lines process in a second or two. Everything runs locally, so there is no upload bottleneck."),
            ("Is my data uploaded anywhere?",
             "No. The deduplication runs entirely in your browser with JavaScript. Nothing is transmitted or logged — you can disconnect from the internet and it still works."),
        ],
    })

    pages.append({
        "slug": "slug-generator",
        "title": "URL Slug Generator — Clean, SEO-Friendly Slugs Instantly",
        "h1": "URL Slug Generator",
        "desc": "Turn any title into a clean URL slug: lowercase, accents stripped, spaces to hyphens. Perfect for blog posts, product pages and SEO. Runs entirely in your browser.",
        "category": "text",
        "keyword": "url slug generator",
        "tool": "slug",
        "args": {},
        "intro": [
            "Paste a headline and get the URL slug a search engine would want: lowercase, spaces and punctuation converted to hyphens, accents folded to their plain equivalents (café → cafe), and no stray dashes. The slug is the part of the URL that humans and Google both read — 'my-ultimate-cold-brew-guide' beats '/post?id=4171' every time.",
            "It also reports slug length, because best practice keeps slugs short: 3–5 meaningful words, under about 60 characters. Edit the input live and the slug updates as you type; everything runs in your browser.",
        ],
        "howto": [
            "Paste or type your page title into the box.",
            "The clean slug appears instantly — accents folded, symbols stripped, words joined by hyphens.",
            "Check the length readout, copy the slug, and paste it into your CMS or router.",
        ],
        "faqs": [
            ("What makes a good URL slug?",
             "Lowercase, hyphens between words, no punctuation, no filler words like 'a' or 'the', and 3–6 words that describe the content. Keywords near the front help slightly; readability matters more."),
            ("Should slugs use hyphens or underscores?",
             "Hyphens. Google treats hyphens as word separators but treats underscores as word joiners — 'cold-brew-guide' reads as three words, 'cold_brew_guide' reads as one."),
            ("Do accented characters hurt SEO?",
             "Modern browsers handle them, but they turn into ugly percent-encoded strings when shared (caf%C3%A9). Folding accents to plain letters keeps URLs clean and shareable."),
            ("Can I change a slug after publishing?",
             "Only with a redirect. Changing a published URL breaks any links pointing to it — set up a 301 redirect from the old slug to the new one, then update internal links."),
        ],
    })

    pages.append({
        "slug": "upside-down-text",
        "title": "Upside Down Text Generator — Flip Text for Bios & Messages",
        "h1": "Upside Down Text",
        "desc": "Flip your text upside down with real Unicode characters — works in Instagram bios, WhatsApp, TikTok and anywhere you paste it. Free, instant, nothing uploaded.",
        "category": "generator",
        "keyword": "upside down text",
        "tool": "upside",
        "args": {},
        "intro": [
            "Type any text and get it flipped upside down — sᴉɥʇ ǝʞᴉl — using genuine Unicode characters, not an image. The flipped text copies and pastes anywhere: Instagram and TikTok bios, WhatsApp messages, Twitter/X posts, Discord names and game chat.",
            "It also reverses the reading order automatically, so the result reads (upside down) from left to right the way you typed it. Everything runs locally in your browser; the flipped text is just characters, so it survives copy-paste across every app.",
        ],
        "howto": [
            "Type or paste your text into the first box.",
            "The upside-down version appears instantly in the output box.",
            "Hit Copy and paste it into your bio, chat or post — it flips right side up when readers turn their phone.",
        ],
        "faqs": [
            ("How does upside-down text work?",
             "It swaps each letter for a Unicode character that looks like the original rotated 180 degrees (a becomes ɐ, e becomes ǝ), then reverses the order. The result is ordinary text — just written with strange letters."),
            ("Will it work in my Instagram bio?",
             "Yes — the characters are standard Unicode, supported by Instagram, TikTok, WhatsApp, Twitter/X, Discord, and virtually every modern app. A few rare fonts may render odd shapes."),
            ("Is it readable by screen readers?",
             "Poorly — screen readers may read the substitute letters strangely or skip them. It is fun decoration, not accessible text; keep important information in normal characters."),
            ("Does the flipped text count as different characters?",
             "It counts the same number of characters, but they are different ones — some platforms with strict username rules may reject exotic characters in usernames. Bios and messages are fine."),
        ],
    })

    pages.append({
        "slug": "hours-calculator",
        "title": "Hours Calculator — Time Between Start and End Times",
        "h1": "Hours Calculator",
        "desc": "Calculate hours and minutes between a start and end time — handles overnight shifts and gives decimal hours for timesheets. Free and instant.",
        "category": "calculator",
        "keyword": "hours calculator",
        "tool": "hoursdiff",
        "args": {},
        "intro": [
            "Enter a start time and an end time and get the duration in hours and minutes — plus the decimal form (8 hours 30 minutes = 8.5) that timesheet systems actually want. Shifts that cross midnight are handled automatically: 10 PM to 6 AM is a clean 8 hours, not a negative number.",
            "It exists because 'hours calculator' is secretly a payroll question. Hourly workers checking a paycheck, freelancers logging billable time, managers building rotas — everyone needs the same boring subtraction, done reliably, with the decimal version ready to paste into whatever system the company uses.",
        ],
        "howto": [
            "Set the start time (your time picker uses 24-hour format; 22:00 is 10 PM).",
            "Set the end time — if it is earlier than the start, the shift is treated as crossing midnight.",
            "Read the duration in hours:minutes, and copy the decimal hours into your timesheet.",
        ],
        "faqs": [
            ("How do I calculate hours between two times?",
             "Convert both to minutes since midnight, subtract the start from the end, and divide by 60. From 9:00 AM (540) to 5:00 PM (1,020): 1020 − 540 = 480 minutes = 8 hours. This calculator does the subtraction and shows both formats."),
            ("How do I calculate a night shift that crosses midnight?",
             "If the end time is earlier than the start time, add 24 hours to the end before subtracting. 10 PM to 6 AM becomes 22:00 to 30:00 — exactly 8 hours. The calculator detects this automatically."),
            ("What is 8 hours 30 minutes in decimal hours?",
             "8.5 hours — divide the minutes by 60 and add to the hours. Timesheet and payroll systems almost always want the decimal form, which this calculator shows alongside the hours:minutes version."),
            ("Does it include breaks?",
             "Not automatically — enter your break as a separate calculation, or subtract it yourself from the duration. Some employers round breaks to 15 minutes; check your workplace rules."),
        ],
    })

    pages.append({
        "slug": "aspect-ratio-calculator",
        "title": "Aspect Ratio Calculator — Resize Without Distortion",
        "h1": "Aspect Ratio Calculator",
        "desc": "Calculate missing dimensions while keeping the aspect ratio. Presets for 16:9, 4:3, 1:1, 21:9 and more. Perfect for video, images and design.",
        "category": "calculator",
        "keyword": "aspect ratio calculator",
        "tool": "aspect",
        "args": {},
        "intro": [
            "Enter a width or height, and this calculator gives you the matching dimension for any aspect ratio — so images and videos resize without stretching. The presets cover the ratios you meet constantly: 16:9 video, 4:3 classic displays, 1:1 social posts, 21:9 ultrawide, 9:16 vertical video.",
            "It also detects the ratio from dimensions you type (say, 1920×1080) and simplifies it (16:9), which is handy when you need to describe a source file or check whether two images share proportions.",
        ],
        "howto": [
            "Choose a preset ratio, or type your own ratio like 3:2.",
            "Enter the width to get the height, or the height to get the width.",
            "Or type both dimensions to detect and simplify the ratio you already have.",
        ],
        "faqs": [
            ("What aspect ratio is 1920×1080?",
             "16:9. Both numbers divide by 120: 1920÷120 = 16 and 1080÷120 = 9. This is the standard HD video and monitor ratio."),
            ("How do I keep aspect ratio when resizing?",
             "Scale both dimensions by the same factor. To halve the width of a 16:9 image, halve the height too — this calculator computes the exact partner dimension for any input."),
            ("What ratio is vertical video (TikTok/Reels/Shorts)?",
             "9:16 — the vertical flip of widescreen. Record at 1080×1920 for full-quality vertical video on all major platforms."),
            ("Why does my photo look stretched?",
             "Its width-to-height proportion was changed during resize. If an image is displayed at a different ratio than its native one, circles become ovals and faces widen — lock the ratio to fix it."),
        ],
    })

    pages.append(_conv("liters-to-ml", "Liters to ML", "liters", "milliliters", 1000, "volume",
                       "The cleanest conversion in the metric system: one liter is exactly 1,000 milliliters, always, everywhere. Multiply by 1,000 for bottles, doses and recipes — the converter keeps the zeros straight when the number gets long.",
                       "Handy anchors: 0.5 L = 500 ml (a water bottle), 1.5 L = 1,500 ml (a big soda bottle), 2 L = 2,000 ml, 5 L = 5,000 ml (a water cooler jug)."))

    pages.append({
        "slug": "text-to-binary",
        "title": "Text to Binary Converter — Text ⇄ Binary Code, Instant",
        "h1": "Text to Binary Converter",
        "desc": "Convert text to binary code and binary back to text instantly. Every character becomes 8 bits (UTF-8). Great for CS homework, puzzles and understanding how computers store text.",
        "category": "converter",
        "keyword": "text to binary",
        "tool": "binary",
        "args": {},
        "intro": [
            "Type any text and see exactly how a computer stores it: every character becomes a byte of 8 binary digits (UTF-8 encoding), with spaces between bytes so you can read the pattern. Paste binary code — space-separated bytes — and it decodes back into text in the other direction.",
            "This is the classic computer-science exercise: seeing that 'Hi' is 01001000 01101001 makes abstract bits concrete. It works for emoji too (they take more than one byte, which is the lesson hiding in plain sight).",
        ],
        "howto": [
            "Type text in the first box — the binary (UTF-8) appears instantly, one group of 8 bits per character.",
            "Paste binary code into the second box to decode it back into readable text.",
            "Note how many bytes emoji take compared to plain letters — that is UTF-8 in action.",
        ],
        "faqs": [
            ("How does text become binary?",
             "Each character is mapped to a number by the UTF-8 standard, and that number is written in base 2 (binary). The letter H is number 72, which is 01001000 in binary — one byte per character for plain English text."),
            ("Why do emoji take more bits than letters?",
             "Emoji are characters outside the basic ASCII range, so UTF-8 encodes them as multiple bytes — often 4, or 32 binary digits. The converter shows this live: type one letter, then one emoji, and compare."),
            ("Can I decode binary I found online?",
             "Yes, if it is standard space-separated 8-bit UTF-8 bytes like 01001000 01101001. The decoder is strict about grouping so partial bytes fail loudly instead of decoding to nonsense."),
            ("Is this the same as encryption?",
             "No — binary is an encoding, not a cipher. Anyone can decode it. Encryption transforms data with a secret key; this simply shows the same text in a different notation."),
        ],
    })

    pages.append({
        "slug": "grams-to-cups",
        "title": "Grams to Cups Converter — By Ingredient (Flour, Sugar, Butter)",
        "h1": "Grams to Cups Converter",
        "desc": "Convert grams to cups by ingredient: flour, sugar, butter, oats, cocoa and more. Ingredient density matters — 200 g of flour is not 200 g of sugar in cups.",
        "category": "converter",
        "keyword": "grams to cups",
        "tool": "gramscups",
        "args": {},
        "intro": [
            "Converting grams to cups is the one baking conversion where the ingredient itself matters: a cup of flour weighs 125 g, but a cup of sugar weighs 200 g and a cup of honey nearly 340 g. Pick the ingredient from the list and both directions convert with the right density.",
            "Results include a friendly fraction estimate (like \u2154 cup) because nobody measures 0.67 cups. For best baking results, grams win — a scale removes the packing-error that makes cup measurements unreliable — but when only cups exist, this converter keeps the recipe honest.",
        ],
        "howto": [
            "Choose the ingredient from the dropdown — density differs for every one.",
            "Type grams to see cups, or type cups to see grams; both directions update live.",
            "Use the fraction shown as the practical measuring-cup answer.",
        ],
        "faqs": [
            ("How many grams is a cup of flour?",
             "About 125 g for all-purpose flour spooned and leveled. Scooping directly from the bag compresses it and can reach 150 g+ — which is why weight recipes beat cup recipes."),
            ("How many grams is a cup of sugar?",
             "Granulated sugar: about 200 g per cup. Brown sugar (packed): about 213 g. Powdered sugar is much lighter: about 120 g per cup."),
            ("Why do grams and cups disagree between websites?",
             "Because cups measure volume, not weight — the answer depends on how densely the ingredient is packed. Reputable sources agree closely on standard weights (flour 120–130 g per cup), and this converter uses the widely accepted values."),
            ("Should I switch my recipes to grams?",
             "If you bake regularly, yes: a scale costs little and removes the single biggest source of baking failure. Use this converter to translate your existing cup recipes once, then weigh forever after."),
        ],
    })

    pages.append({
        "slug": "day-of-week",
        "title": "What Day of the Week Was I Born? — Day of Week Calculator",
        "h1": "Day of the Week Calculator",
        "desc": "Find the day of the week for any date in history — birthdays, historical events, or the date of your next anniversary. Instant, with the day-of-year and week number.",
        "category": "calculator",
        "keyword": "what day of the week was i born",
        "tool": "dayofweek",
        "args": {},
        "intro": [
            "Pick any date and see the day of the week it fell on — or will fall on. It answers the classic 'what day was I born on?' (and whether your birthday lands on a weekend next year), plus historical curiosity: moon landings, royal weddings, and that concert you remember being at.",
            "Alongside the weekday you get the day-of-year number and the ISO week number, which is the detail project plans and European calendars quietly rely on.",
        ],
        "howto": [
            "Pick any date — past or future — from the date picker.",
            "Read the weekday instantly, plus the day-of-year and ISO week number.",
            "Change the year to plan birthdays: see whether yours falls on a weekend next time.",
        ],
        "faqs": [
            ("What day of the week was I born?",
             "Enter your date of birth and the weekday appears instantly. The pattern repeats every 28 years (the solar cycle), so your birth date falls on the same weekday as it did 28 years ago."),
            ("Does the calculator work for any year in history?",
             "It uses your browser's proleptic Gregorian calendar, accurate across a huge historical range. For dates before 1582 (when the Gregorian calendar was introduced) historians use the Julian calendar, so results may differ from historical records."),
            ("Why do dates fall on different weekdays each year?",
             "A year is 365 days — one day longer than 52 weeks — so each year's dates shift one weekday later (two after a leap year). That is why your birthday keeps moving."),
            ("What is the ISO week number?",
             "A standard way of numbering weeks (1–52/53) used in European business calendars: week 1 is the week containing the first Thursday of January."),
        ],
    })

    pages.append(_conv("liters-to-quarts-uk", "Liters to Quarts", "liters", "quarts (US)", 1.0566882094, "volume",
                       "Forward direction for the liters-to-quarts family: multiply liters by 1.05669 to get US quarts. Engine capacities, stock pots and paint tins all land on this conversion.",
                       "Handy anchors: 1 L = 1.06 qt, 3 L = 3.17 qt, 5 L = 5.28 qt, 10 L = 10.57 qt."))

    pages.append({
        "slug": "litres-per-100km-to-mpg",
        "title": "L/100km to MPG Converter — Fuel Economy, Both Directions",
        "h1": "L/100km to MPG Calculator",
        "desc": "Convert liters per 100 km to US MPG (and back). The two fuel-economy scales run in opposite directions — this converter handles the inverted math and flags which number is better.",
        "category": "converter",
        "keyword": "litres per 100km to mpg",
        "tool": "fuel",
        "args": {},
        "intro": [
            "Europe measures fuel economy in liters per 100 km; America uses miles per gallon. They are not just different units — they run in opposite directions: lower L/100km is better, higher MPG is better. The conversion is MPG = 235.215 ÷ (L/100km), and this calculator handles the inversion both ways.",
            "So a European-spec car at 6.5 L/100km is a 36 MPG car; an American 30 MPG sedan is a 7.8 L/100km car. Useful when importing, comparing spec sheets, or decoding a rental car dashboard on holiday.",
        ],
        "howto": [
            "Type your figure in liters per 100 km — the MPG equivalent appears instantly.",
            "Or type MPG in the second box to get L/100km in the first.",
            "The better-worse hint updates automatically, so the inverted scales never catch you out.",
        ],
        "faqs": [
            ("How do you convert L/100km to MPG?",
             "Divide 235.215 by the L/100km figure. 8 L/100km = 235.215 ÷ 8 = 29.4 MPG (US). For UK imperial MPG, use 282.481 instead — imperial gallons are 20% bigger."),
            ("Why do the two scales run in opposite directions?",
             "L/100km measures fuel used per distance (lower = efficient); MPG measures distance per fuel (higher = efficient). One is consumption, the other is efficiency — the same idea from opposite ends."),
            ("What is a good L/100km?",
             "For petrol cars: under 6 L/100km is efficient, 6–8 is typical, over 10 is thirsty. Hybrids reach 4–5; large SUVs can exceed 12. Electric cars leave the scale entirely (they use kWh/100km)."),
            ("Is this US MPG or UK MPG?",
             "This converter uses US MPG (the standard in the US). UK MPG uses the larger imperial gallon, so a car rated 40 MPG (UK) is only 33 MPG (US) — check which scale the brochure means."),
        ],
    })

    pages.append({
        "slug": "cups-to-grams",
        "title": "Cups to Grams Converter — By Ingredient (Flour, Sugar, Butter)",
        "h1": "Cups to Grams Converter",
        "desc": "Convert cups to grams by ingredient: flour 125 g/cup, sugar 200 g, butter 227 g and more. The accurate way to translate US recipes onto a kitchen scale.",
        "category": "converter",
        "keyword": "cups to grams",
        "tool": "gramscups",
        "args": {},
        "intro": [
            "Translating an American cup recipe onto a kitchen scale is the single best upgrade a baker can make — and the trick is that the answer depends on the ingredient: a cup of flour is 125 g, a cup of sugar 200 g, a cup of butter 227 g. Choose the ingredient and both directions convert with the correct density.",
            "Cup measurements vary by up to 20% depending on how firmly you scoop; grams never vary. Translate the recipe once with this converter, weigh after that, and your bakes stop varying with them.",
        ],
        "howto": [
            "Choose the ingredient from the dropdown list.",
            "Type the number of cups — the gram weight appears instantly (or go the other way).",
            "Weigh to the gram on your scale; note the translation on the recipe card for next time.",
        ],
        "faqs": [
            ("How many grams is 2 cups of flour?",
             "About 250 g, at the standard 125 g per leveled cup. If the original recipe scooped heavily, the author may have meant closer to 280 g — one more reason weight recipes win."),
            ("How many grams is a cup of butter?",
             "227 g — which is exactly one US stick-based convenience: a 1-pound butter pack is 2 cups. Most butter wrappers print tablespoon and cup markings on the side."),
            ("Is 1 cup always 240 grams?",
             "Only for water and milk. Dense ingredients (sugar 200 g, honey 340 g) and light ones (oats 90 g, powdered sugar 120 g) differ wildly — always convert by ingredient."),
            ("What is 250 grams in cups?",
             "Depends entirely on the ingredient: 2 cups of flour, 1.25 cups of granulated sugar, about 1.1 cups of butter. Pick the ingredient in the converter above."),
        ],
    })

    pages.append({
        "slug": "salary-to-hourly",
        "title": "Salary to Hourly Calculator — Annual Pay to Hourly Wage",
        "h1": "Salary to Hourly Calculator",
        "desc": "Convert your annual salary to an hourly wage (and back). Uses the standard 2,080-hour work year, with custom hours-per-week support. Know what your time is worth.",
        "category": "calculator",
        "keyword": "salary to hourly",
        "tool": "salary",
        "args": {},
        "intro": [
            "Enter an annual salary and see the equivalent hourly wage — or type an hourly rate and get the yearly figure. The default assumes the American standard of 2,080 work hours per year (40 hours × 52 weeks); adjust hours per week and weeks per year for your reality, including part-time schedules and unpaid leave.",
            "It matters for job comparisons (a $65,000 salary against a $35/hour contract is not obvious until both are on the same scale), for freelancers setting rates, and for anyone working out whether overtime at time-and-a-half actually pays better than the salaried offer.",
        ],
        "howto": [
            "Type your annual salary — the hourly, monthly and weekly equivalents appear instantly.",
            "Adjust hours per week and weeks per year if your schedule differs from 40 × 52.",
            "Or enter an hourly rate to convert upward to yearly pay.",
        ],
        "faqs": [
            ("How do I convert salary to hourly wage?",
             "Divide the annual salary by the hours worked per year. The standard assumption is 2,080 hours (40 hours × 52 weeks), so $52,000 a year is $25 per hour. Adjust the hours if you work part-time or take unpaid leave."),
            ("What is $50,000 a year per hour?",
             "About $24.04 per hour at 2,080 hours a year — roughly $961 a week or $4,167 a month before taxes. Enter it above to see the breakdown at your actual hours."),
            ("Should I compare jobs by hourly or annual pay?",
             "Convert both to the same scale first, then account for benefits: salaried roles often include paid leave and health insurance that hourly rates exclude. A slightly lower salary with paid time off can beat a higher hourly contract."),
            ("How many hours is full-time?",
             "The US standard is 40 hours a week for 52 weeks = 2,080 hours a year. If you take 2 weeks unpaid leave, use 2,000; many contractors bill 1,800–1,900 billable hours a year after non-billable time."),
        ],
    })

    pages.append({
        "slug": "coin-flip",
        "title": "Coin Flip Online — Fair, Cryptographically Random Heads or Tails",
        "h1": "Coin Flip",
        "desc": "Flip a coin online: cryptographically fair heads or tails with a running tally. Can't decide? Let 256 bits of entropy do it. Free, instant, nothing recorded.",
        "category": "generator",
        "keyword": "coin flip",
        "tool": "coinflip",
        "args": {},
        "intro": [
            "Flip a fair coin as many times as you like — each result comes from your browser's cryptographically secure random source, so heads and tails are equally likely every single time, with no hidden patterns. The tally keeps count across flips so you can settle best-of-three, best-of-five, or a best-of-nineteen argument.",
            "The classic use is the decision you already know the answer to: flip the coin and notice which side you were hoping for while it spins. For group decisions, the tally doubles as a neutral referee.",
        ],
        "howto": [
            "Press Flip — the coin lands heads or tails instantly.",
            "Keep flipping for best-of series; the running tally tracks heads, tails and total flips.",
            "Hit Reset to clear the tally for the next decision.",
        ],
        "faqs": [
            ("Is this online coin flip fair?",
             "Yes — each flip uses the browser's WebCrypto secure random source, the same class of generator used for encryption. Every flip is independent and exactly 50/50 in expectation."),
            ("Can I use this for a sports coin toss?",
             "You can, but a physical coin is more ceremonial. This version is handy for remote games, online debates and quick decisions where nobody has a coin."),
            ("What are the odds of flipping 5 heads in a row?",
             "1 in 32 (2 to the power of 5, about 3.1%). The tally makes it easy to spot streaks — which appear more often than intuition expects, a famous quirk of true randomness."),
            ("Does the coin remember previous flips?",
             "No — every flip is independent. The tally is just for record-keeping; past results have zero influence on the next flip."),
        ],
    })

    pages.append({
        "slug": "square-footage-calculator",
        "title": "Square Footage Calculator — Length × Width in Feet or Meters",
        "h1": "Square Footage Calculator",
        "desc": "Calculate square footage (or square meters) from length and width. Works in feet or meters, converts between them, and totals multiple rooms. For flooring, paint and real estate.",
        "category": "calculator",
        "keyword": "square footage calculator",
        "tool": "sqft",
        "args": {},
        "intro": [
            "Enter the length and width of a room, house or garden and get the area in square feet or square meters — the number behind flooring orders, paint estimates, rent-per-square-foot comparisons and 'is this apartment actually big?' checks. It works in either unit and converts automatically.",
            "For irregular spaces, measure section by section and add the areas together — the running total box keeps the math honest. An L-shaped living room is just two rectangles that happen to share a wall.",
        ],
        "howto": [
            "Choose feet or meters, then enter the length and width.",
            "Read the area in square feet and square meters side by side.",
            "For multi-room projects, add each room's area to the running total.",
        ],
        "faqs": [
            ("How do I calculate square footage of a room?",
             "Measure the length and width in feet and multiply them: a 12 ft × 15 ft room is 180 square feet. For closets and alcoves, measure separately and add the areas."),
            ("How many square feet is 12x12?",
             "12 ft × 12 ft = 144 square feet — a standard bedroom size, and conveniently exactly the amount of flooring in one box quote territory (most boxes cover 18–25 sq ft, so order 6–8 boxes plus 10% waste)."),
            ("How do I convert square feet to square meters?",
             "Multiply by 0.0929. A 1,000 sq ft apartment is about 92.9 square meters. The calculator shows both units side by side automatically."),
            ("How much extra flooring should I buy?",
             "Add 10% for straight layouts and 15% for diagonal patterns or lots of cuts — waste is real, and dye lots mean buying more later may not match. Use the running total to plan the order."),
        ],
    })

    pages.append({
        "slug": "seconds-converter",
        "title": "Seconds to Hours, Minutes & Seconds Converter — h:m:s",
        "h1": "Seconds Converter",
        "desc": "Convert a raw number of seconds into hours, minutes and seconds (h:m:s) — perfect for video lengths, run times and logs. Two-way: type a duration too.",
        "category": "converter",
        "keyword": "seconds to hours",
        "tool": "secondsconv",
        "args": {},
        "intro": [
            "Type a raw number of seconds — 3725, 86,400, whatever a log file, API response or stopwatch hands you — and see it as readable hours, minutes and seconds. Go the other way too: type 1:02:05 and get the total seconds, which is what video timestamps and countdowns actually expect.",
            "It is a small tool with an outsized number of uses: run splits (a marathon in seconds), podcast chapters, benchmark timings, game speedruns, and every timestamp that was clearly never meant for human eyes.",
        ],
        "howto": [
            "Type a number of seconds — the h:m:s breakdown appears instantly.",
            "Or type a duration like 1:02:05 in the second box to get total seconds.",
            "Both boxes stay in sync — edit either side at any time.",
        ],
        "faqs": [
            ("How many seconds are in an hour?",
             "3,600 — 60 seconds × 60 minutes. A day is 86,400 seconds, which is the number behind most computer clock internals."),
            ("How do I convert seconds to h:mm:ss?",
             "Divide by 3,600 for hours, take the remainder and divide by 60 for minutes, and what is left is seconds. 7,325 seconds = 2:02:05. The converter does this and shows the padding."),
            ("How many seconds is a 4 minute mile?",
             "A 4-minute mile is 240 seconds — or 0.066 hours. Elite marathoners cover the same distance in under 4:35 per mile for two hours straight."),
            ("Why do APIs return seconds instead of hh:mm:ss?",
             "Because plain integer seconds are unambiguous, sortable and easy to add — no 60-based carrying. Humans get readability; machines get seconds, and this converter translates between them."),
        ],
    })

    pages.append(_conv("gb-to-mb", "GB to MB", "gigabytes", "megabytes", 1000, "storage",
                       "Storage makers use decimal gigabytes: 1 GB = 1,000 MB. Your operating system may display binary gibibytes (1 GiB = 1,024 MiB), which is why a '256 GB' drive shows as about 238 GiB in Windows — the drive is not lying, the units are different.",
                       "Handy anchors: 1 GB = 1,000 MB, 5 GB = 5,000 MB (a phone plan), 64 GB = 64,000 MB (a flash drive), 500 GB = 500,000 MB (a laptop SSD)."))
    pages.append(_conv("mb-to-gb", "MB to GB", "megabytes", "gigabytes", 1 / 1000, "storage",
                       "Convert megabytes to gigabytes by dividing by 1,000 — the decimal definition storage and telecom companies use. A 5,000 MB photo collection is 5 GB of cloud storage you did not know you needed.",
                       "Handy anchors: 100 MB = 0.1 GB (an app), 700 MB = 0.7 GB (a CD), 4,700 MB = 4.7 GB (a DVD), 50,000 MB = 50 GB (a video game)."))

    pages.append({
        "slug": "pixels-to-inches",
        "title": "Pixels to Inches Calculator — Print Size at Any DPI",
        "h1": "Pixels to Inches Calculator",
        "desc": "Convert pixels to inches for print or screen: enter pixel dimensions and DPI/PPI to get exact physical size. Includes print-quality DPI guidance.",
        "category": "calculator",
        "keyword": "pixels to inches",
        "tool": "pxin",
        "args": {},
        "intro": [
            "Pixels have no physical size until you give them a density: the same 3,000-pixel image is 10 inches wide at 300 DPI (print quality) or 31 inches at 96 DPI (a screen). Enter pixel dimensions and the DPI, and this calculator gives the exact physical width and height in inches and centimeters.",
            "The print rule of thumb: 300 DPI for photos in the hand, 150 DPI acceptable for posters viewed at arm's length, 96–72 DPI is screen territory. Work backwards from a target print size and the calculator tells you the pixel dimensions your camera or export needs.",
        ],
        "howto": [
            "Enter the pixel width and height of your image.",
            "Enter the DPI/PPI — 300 for photo prints, 150 for posters, 96 for screens.",
            "Read the physical size in inches and centimeters; adjust DPI to fit a target print size.",
        ],
        "faqs": [
            ("How do I convert pixels to inches?",
             "Divide the pixel count by the DPI (dots per inch). A 1,200-pixel-wide image at 300 DPI prints 4 inches wide: 1,200 ÷ 300 = 4. The calculator does this for width and height together."),
            ("What DPI should I use for printing photos?",
             "300 DPI is the photo-lab standard viewed at reading distance. 150 DPI works for posters and wall art viewed from a meter or more; large-format banners can go as low as 100 DPI."),
            ("How many pixels is an 8x10 print at 300 DPI?",
             "2,400 × 3,000 pixels — 7.2 megapixels. Any modern phone camera exceeds this, which is why phone photos generally print beautifully at ordinary sizes."),
            ("Why does my 4000-pixel image look blurry when printed?",
             "Because it was stretched beyond its pixel budget: at 4,000 pixels and 300 DPI the sharp size is 13.3 inches. Printing it at 20 inches means 200 DPI, and the softness you see is interpolation filling in pixels that were never captured."),
        ],
    })

    pages.append(_conv("ounces-to-ml", "Ounces to ML", "fluid ounces (US)", "milliliters", 29.5735295625, "volume",
                       "US recipes and nutrition labels speak in fluid ounces; the rest of the world pours in milliliters. One US fluid ounce is 29.5735 ml — about 30, which is why the two units feel like near-twins even though they are not twins.",
                       "Handy anchors: 1 fl oz = 29.57 ml, 8 fl oz = 236.6 ml (a cup), 12 fl oz = 354.9 ml (a can), 16 fl oz = 473.2 ml (a pint).", dec=1))

    pages.append({
        "slug": "dice-roller",
        "title": "Online Dice Roller — D6, D20 & Any Dice, Cryptographically Fair",
        "h1": "Dice Roller",
        "desc": "Roll virtual dice online: pick how many dice and how many faces (D6, D20, anything). Cryptographically fair results with per-die outcomes and totals. Perfect for board games and D&D.",
        "category": "generator",
        "keyword": "dice roller",
        "tool": "dice",
        "args": {},
        "intro": [
            "Roll up to 12 dice with any number of faces — the classic D6, the D20 that decides dungeons, or an exotic D7 if your board game demands it. Each die's result is shown individually plus the total, and every roll comes from your browser's cryptographically secure random source.",
            "No physical dice to lose under the sofa, no suspicious thumb techniques, no arguments about whether the roll was fair. The randomness is the same quality used for encryption keys — the fairest dice you will ever throw.",
        ],
        "howto": [
            "Choose the number of dice (1–12) and the number of faces per die (2–100).",
            "Hit Roll — each die shows its result, and the total appears underneath.",
            "Roll again for another set; the table shows the last roll's individual outcomes.",
        ],
        "faqs": [
            ("What is a D20?",
             "A 20-sided die, the signature die of Dungeons & Dragons — a natural 20 (rolling a 20) is the legendary critical success. This roller supports D20 and every other face count from 2 to 100."),
            ("Are online dice rolls actually random?",
             "This one uses the browser's WebCrypto secure random source — cryptographically stronger than most physical dice, which can be slightly unbalanced by weight and shape. Each roll is independent."),
            ("How do I roll 2d6?",
             "Set dice count to 2 and faces to 6 — that is the standard 2d6 notation used in Monopoly, Catan and backgammon. The roller shows each die plus the total."),
            ("Can I use this for a classroom or raffle?",
             "Yes — assign numbers to participants and roll one die with the matching face count. The cryptographic randomness makes it demonstrably fair if anyone questions the result."),
        ],
    })

    pages.append({
        "slug": "roman-numeral-date-converter",
        "title": "Roman Numeral Date Converter — Weddings, Tattoos & Anniversaries",
        "h1": "Roman Numeral Date Converter",
        "desc": "Convert any date into Roman numerals — the classic wedding date and tattoo format (like XII·XXV·MMXXIV). Type a date, get the numerals, copy the style you want.",
        "category": "converter",
        "keyword": "roman numeral date converter",
        "tool": "roman",
        "args": {},
        "intro": [
            "Turn any date — a wedding day, an anniversary, a child's birth — into Roman numerals in the classic engraved format: 12·25·2024 becomes XII·XXV·MMXXIV. Roman numeral dates appear on invitation suites, wedding bands, tattoos and family wall art precisely because they look timeless.",
            "Type your date below and the numerals render instantly. The separator dot (·) is the traditional engraved style, but hyphens or plain spacing are equally correct — the numerals themselves are what matter.",
        ],
        "howto": [
            "Set the month, day and year of your date — the Roman numeral form renders instantly.",
            "Read the result in the engraved style: month · day · year in Roman numerals.",
            "Copy the numerals for your invitation, engraving or design mockup.",
        ],
        "faqs": [
            ("How do you write a date in Roman numerals?",
             "Convert each part of the date separately: the month, the day, and the year each become Roman numerals, traditionally joined by dots. June 15, 2025 becomes VI·XV·MMXXV."),
            ("What is my wedding date in Roman numerals?",
             "Type the date into the converter — for example, September 12, 2026 becomes IX·XII·MMXXVI. Couples usually engrave it with raised dots between the groups."),
            ("Are Roman numeral date tattoos done in a specific order?",
             "Most common is month·day·year (the American order), but day·month·year (European) is equally valid — choose the order that matches how you say the date, and keep it consistent across the design."),
            ("Do Roman numerals have a year zero problem?",
             "No — the calendar simply counts years forward, and every year from 1 to 3999 converts cleanly. All modern dates fit comfortably."),
        ],
    })

    pages.append(_conv("mm-to-cm", "MM to CM", "millimeters", "centimeters", 1 / 10, "length",
                       "The metric system's two everyday small units differ by exactly one factor of ten: 1 centimeter is 10 millimeters. Divide by 10 to go from mm to cm — or slide the decimal point one place left, which is all this converter is really doing.",
                       "Handy anchors: 10 mm = 1 cm, 45 mm = 4.5 cm (a golf ball), 100 mm = 10 cm, 250 mm = 25 cm (a ruler's length)."))

    # ---------- Index metadata used by build ----------
    CATEGORY_INFO = {
        "countdown": ("Countdowns", "Live countdown timers for the dates people care about — always accurate, automatically rolling over to the next year."),
        "calculator": ("Calculators", "Instant answers for the everyday math people actually search for — percentages, dates, tips and discounts."),
        "converter": ("Converters", "Two-way unit conversions with the exact formulas and reference tables — length, weight, temperature and distance."),
        "text": ("Text Tools", "Word counting and case conversion that run entirely in your browser — private by design."),
        "generator": ("Generators", "Random names and strong passwords, generated locally with cryptographically secure randomness."),
    }

    return pages, CATEGORY_INFO


def get_pages():
    return PAGES()
