# -*- coding: utf-8 -*-
"""ToolDune page definitions.

Every page = one long-tail keyword + one real working tool + original content
(intro paragraphs, how-to steps, FAQ). Built by build.py into static HTML.
Helpers below generate families of pages (countdowns, converters) so new
variants are one-line additions — that is the programmatic-SEO lever.
"""


def _cd(slug, event, month, day, keyword, facts, seasonal, emoji,
        unit=None, unit_label=None, title=None, h1=None, desc=None, faqs=None, slug_out=None):
    """Countdown page: fixed month/day, recurs yearly (JS computes next occurrence).
    Optional unit/unit_label render the big number as weeks/sleeps instead of days;
    slug_out overrides the default days-until-{slug} URL."""
    page = {
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
    if slug_out:
        page["slug"] = slug_out
    if unit:
        page["args"]["unit"] = unit
    if unit_label:
        page["args"]["unit_label"] = unit_label
    if title:
        page["title"] = title
    if h1:
        page["h1"] = h1
    if desc:
        page["desc"] = desc
    if faqs:
        page["faqs"] = faqs
    return page


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

    # Christmas unit variants — "sleeps" (kid/family ritual) and "weeks" (planner) are
    # distinct high-volume query angles with their own SERPs, same countdown engine.
    sleeps = _cd("sleeps", "Christmas", 12, 25, "how many sleeps until christmas",
                 "One sleep means one night. Kids have used the sleep count for generations because it turns an abstract number of days into something you can feel at bedtime: on December 24th there is exactly one sleep left.",
                 "Ask \"how many sleeps\" at bedtime and let the page answer. The count follows your device's clock and rolls over automatically to next Christmas after the big day, so the bookmark never goes stale.",
                 "🛏️",
                 unit="sleeps", unit_label="sleeps to go", slug_out="sleeps-until-christmas",
                 title="How Many Sleeps Until Christmas? Live Sleeps Countdown for Kids",
                 h1="How Many Sleeps Until Christmas?",
                 desc="Count the sleeps until Christmas — one sleep per night, made for kids and families. Live countdown, always correct, works on any device, no sign-up.",
                 faqs=[
                     ("How many sleeps until Christmas?",
                      "The big number counts the nights between tonight and Christmas morning. Each bedtime that passes takes one sleep off the total, so on Christmas Eve you will see exactly one sleep left."),
                     ("Is a sleep the same as a day?",
                      "Almost — the number of sleeps matches the number of days on a regular countdown until the final stretch. The difference is the ritual: sleeps are counted at bedtime, which is why kids (and honestly, adults) find them easier to feel."),
                     ("When does the count change to one sleep?",
                      "It follows your device's calendar. When your date shows December 24th, one sleep remains; on December 25th the page switches to celebrate that it's Christmas today."),
                     ("Does it work next year too?",
                      "Yes. After Christmas the page automatically starts counting the sleeps until next Christmas, so you can keep it bookmarked all year."),
                 ])
    pages.append(sleeps)

    weeks = _cd("weeks", "Christmas", 12, 25, "how many weeks until christmas",
                 "Planning in weeks matches how the run-up to Christmas actually works: Advent is four weeks long, most shoppers spread costs week by week, and travel and parcel deadlines are quoted in weeks ahead.",
                 "Use the weeks figure for planning and the live timer for precision — the page also shows exact days, hours and minutes underneath, plus the date Christmas falls on this year.",
                 "🗓️",
                 unit="weeks", unit_label="weeks to go", slug_out="weeks-until-christmas",
                 title="How Many Weeks Until Christmas? Live Weeks Countdown & Planner",
                 h1="How Many Weeks Until Christmas?",
                 desc="See how many weeks until Christmas, with a live timer showing exact days, hours and minutes too. Plan gifts, travel and Advent week by week — free, no sign-up.",
                 faqs=[
                     ("How many weeks until Christmas?",
                      "The big number shows the full weeks remaining, counted from your device's clock right now — the same live calculation as a days countdown, scaled to weeks so it matches how most people plan December."),
                     ("Is the weeks figure rounded?",
                      "It is rounded up to the next whole week, so a part-week still counts as one. If you need precision, the timer below shows the exact days, hours, minutes and seconds remaining."),
                     ("Why plan Christmas in weeks instead of days?",
                      "Weeks line up with real deadlines: Advent calendars, weekly shopping budgets, school terms and flight price windows are all quoted in weeks. Days feel endless in September; weeks give you a workable plan."),
                     ("Does the countdown work after Christmas?",
                      "Yes — it rolls over automatically to next year's Christmas, so the weeks figure stays correct all year round."),
                 ])
    pages.append(weeks)

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

    pages.append({
        "slug": "half-calculator",
        "title": "Half Calculator — Half of Any Number, Fraction or Amount",
        "h1": "Half Calculator",
        "desc": "What is half of 3/4 cup, half of 150, or half of 2-1/2? Split any number, fraction or mixed amount in half — exact fractional answers for recipes and math homework.",
        "category": "calculator",
        "keyword": "half calculator",
        "tool": "half",
        "args": {},
        "intro": [
            "Halving sounds trivial until the number is 3/4 cup of cocoa and you are making a half batch. This calculator halves anything: whole numbers, decimals, fractions (3/4), and mixed amounts (2-1/2) — giving the exact fractional answer (3/8) alongside the decimal, so the reduced recipe stays correct.",
            "It is the quiet hero of batch cooking, scaling down for two, dividing bills between two people, and every math worksheet with the word 'half' in it.",
        ],
        "howto": [
            "Type any amount — whole number, decimal, fraction like 3/4, or mixed like 2-1/2.",
            "Read the exact half as a fraction and as a decimal.",
            "Halve several ingredients in a row while scaling a recipe down.",
        ],
        "faqs": [
            ("What is half of 3/4?",
             "3/8. Dividing a fraction by 2 doubles its bottom number: 3/4 becomes 3/8. In cups, 3/8 cup is 6 tablespoons — a common half-batch conversion."),
            ("What is half of 2/3?",
             "2/3 halved is 1/3 (double the bottom number: 2/3 → 2/6 = 1/3). This trips people up because the decimal form, 0.333, looks nothing like 0.666 halved — but it is exactly half."),
            ("What is half of 1 and 3/4 cups?",
             "7/8 cup. Convert 1-3/4 to 7/4 first, halve it to 7/8 — just under a full cup. Practically: a scant cup."),
            ("How do I halve an odd number?",
             "Odd whole numbers halve to .5 — half of 7 is 3.5. For fractions with odd denominators (like 1/2), double the denominator instead: half of 1/2 is 1/4."),
        ],
    })

    pages.append({
        "slug": "random-letter-generator",
        "title": "Random Letter Generator — Pick Letters A to Z Instantly",
        "h1": "Random Letter Generator",
        "desc": "Generate random letters A–Z for classroom games, giveaways and puzzles. Cryptographically fair, no repeats option, instant results.",
        "category": "generator",
        "keyword": "random letter generator",
        "tool": "letter",
        "args": {},
        "intro": [
            "Generate random letters from A to Z — for classroom activities, drinking-game safe editions, brainstorming ('name a fruit starting with…'), giveaways, or word games. Cryptographically fair, so every letter is equally likely and nobody can predict the pick.",
            "Generate one letter at a time or a batch, with an optional no-repeats mode for letter-bingo style games. Everything runs locally — nothing is recorded anywhere.",
        ],
        "howto": [
            "Set how many letters you need (1–26).",
            "Toggle no-repeats for bingo-style draws, or leave it off for independent picks.",
            "Hit Generate — letters appear instantly; generate again for a fresh set.",
        ],
        "faqs": [
            ("Is the letter pick truly random?",
             "Yes — letters are drawn from your browser's WebCrypto secure random source, the cryptographic-grade generator. Every letter has exactly a 1-in-26 chance."),
            ("Can I generate the whole alphabet in random order?",
             "Set count to 26 with no-repeats on — you get all 26 letters in a random order, ready for letter-bingo or alphabet challenge games."),
            ("What can I use a random letter for?",
             "Classroom games (name a country starting with M), art prompts, assigning fair letter grades to presentations, passwords, brainstorming constraints, and board game substitutes for lost letter tiles."),
            ("Does it work offline?",
             "Yes — generation runs in your browser. Once the page is loaded, no connection is needed."),
        ],
    })

    pages.append({
        "slug": "cubic-feet-calculator",
        "title": "Cubic Feet Calculator — Volume from Length, Width & Height",
        "h1": "Cubic Feet Calculator",
        "desc": "Calculate cubic feet from length, width and height — for moving trucks, storage units, fridges and shipping. Works in feet or cm and converts to cubic meters.",
        "category": "calculator",
        "keyword": "cubic feet calculator",
        "tool": "cubicft",
        "args": {},
        "intro": [
            "Enter length, width and height to get the volume in cubic feet — the number that decides which moving truck to book, whether the fridge fits the alcove, and what the shipping company will charge. It works in feet or centimeters and shows cubic meters alongside, because the rest of the world quotes volumes that way.",
            "Everything updates as you type, and the cm mode means European appliance specs and American shelf measurements can finally be compared on one screen.",
        ],
        "howto": [
            "Choose feet or centimeters, then enter length, width and height.",
            "Read the volume in cubic feet and cubic meters side by side.",
            "Add a margin for packing — moving boxes never pack at 100% density.",
        ],
        "faqs": [
            ("How do I calculate cubic feet?",
             "Multiply length × width × height, all in feet. A box measuring 2 ft × 2 ft × 1 ft is 4 cubic feet. Measure the largest points (including handles and feet on appliances) to be safe."),
            ("How many cubic feet is a standard fridge?",
             "A typical fridge-freezer holds 18–25 cubic feet; a compact dorm fridge around 3–4. Check the interior capacity spec, not the exterior size — walls and compressors eat space."),
            ("What size moving truck do I need?",
             "A studio flat fits in a 10–12 ft truck (about 350–450 cu ft), a one-bedroom in a 15–16 ft truck, and a 3-bedroom house usually needs a 20–26 ft truck (1,400+ cu ft). Measure your largest furniture first."),
            ("How do I convert cubic feet to cubic meters?",
             "Multiply by 0.0283. A 40 cu ft storage crate is about 1.13 cubic meters. The calculator shows both units automatically."),
        ],
    })

    pages.append({
        "slug": "line-sorter",
        "title": "Line Sorter — Alphabetize Text Lists Online (A-Z or Z-A)",
        "h1": "Line Sorter",
        "desc": "Sort text lines alphabetically A-Z or Z-A instantly. Case-insensitive option, duplicate and blank line cleanup, live line counts. 100% in your browser.",
        "category": "text",
        "keyword": "alphabetize lines",
        "tool": "sorter",
        "args": {},
        "intro": [
            "Paste any list — names, keywords, URLs, tasks — and sort the lines alphabetically in one pass. A-Z or Z-A, with case-insensitive comparison so 'apple' and 'Apple' sort together instead of by capital letter. Blank lines can be dropped, duplicates collapsed, and the line count updates live.",
            "It pairs naturally with the duplicate remover for list cleaning: dedupe first, sort second, copy the result. Like every ToolDune text tool, it runs entirely in your browser — private by architecture.",
        ],
        "howto": [
            "Paste your list into the input box.",
            "Choose A-Z or Z-A; toggle case-insensitive, remove blanks or dedupe as needed.",
            "The sorted list and line count update live — copy when it looks right.",
        ],
        "faqs": [
            ("How do I alphabetize a list of names?",
             "Paste the names one per line and click A-Z. Case-insensitive sorting keeps 'smith' and 'Smith' together instead of putting all lowercase names after all uppercase ones."),
            ("Does sorting change my original text?",
             "No — the sorted output appears in its own box. Your input stays untouched until you clear or edit it."),
            ("What does case-insensitive mean here?",
             "The sort compares letters without caring about capitalization, which is what humans expect: 'banana' sorts between 'Apple' and 'Cherry' rather than at the end."),
            ("Is there a line limit?",
             "The practical limit is browser memory — tens of thousands of lines sort instantly. Nothing is uploaded; sorting is local JavaScript."),
        ],
    })

    pages.append({
        "slug": "unit-price-calculator",
        "title": "Unit Price Calculator — Which Pack Is Actually Cheaper?",
        "h1": "Unit Price Calculator",
        "desc": "Compare two packs by unit price: price ÷ quantity for A and B, winner highlighted. Works with any unit — per 100g, per liter, per sheet. Stop falling for bulk illusions.",
        "category": "calculator",
        "keyword": "unit price calculator",
        "tool": "unitprice",
        "args": {},
        "intro": [
            "The shelf price lies by omission: the 900 ml bottle at $3.40 versus the 1.5 L jug at $5.10 — which is cheaper per drink? Enter price and quantity for each pack, and the calculator computes the unit price of both and names the winner instantly.",
            "Bulk is usually cheaper per unit — but not always, and supermarkets know shoppers assume it is. Ten seconds with this calculator pays for itself the first time it catches a 'family size' that costs more per gram than the regular box.",
        ],
        "howto": [
            "Enter pack A's price and quantity, then pack B's.",
            "Read both unit prices — the cheaper one is highlighted automatically.",
            "Use any quantity unit you like (grams, ml, sheets, tablets); just use the same unit for both packs.",
        ],
        "faqs": [
            ("How do I calculate unit price?",
             "Divide the price by the quantity: $3.40 for 900 ml is 3.40 ÷ 900 = $0.00378 per ml (or 37.8 cents per 100 ml). Do the same for the other pack and compare — the calculator does both divisions at once."),
            ("Is bigger always cheaper per unit?",
             "Usually, but not always. Discount lines sometimes cost more per gram than the standard size, and sale prices can invert the rule. That is exactly why shelf tags saying 'value size' deserve a quick unit-price check."),
            ("What unit should I compare in?",
             "Any unit, as long as both packs use the same one. Per 100 g or per liter reads most naturally; for paper goods, per sheet or per 100 sheets is the honest comparison."),
            ("Does it work for three or more packs?",
             "Compare in pairs — A against B, then the winner against C. Two rounds settle a three-way comparison."),
        ],
    })

    pages.append({
        "slug": "word-frequency-counter",
        "title": "Word Frequency Counter — Top Words in Any Text",
        "h1": "Word Frequency Counter",
        "desc": "Paste text and see which words appear most often, ranked by count with percentages. Live TOP table, stopwords toggle, 100% in-browser.",
        "category": "text",
        "keyword": "word frequency counter",
        "tool": "wordfreq",
        "args": {},
        "intro": [
            "Paste an article, essay or transcript and instantly see which words you use most: a ranked table of every word with its count and percentage of the text. Toggle small function words (the, a, of…) off to reveal the words that actually carry your meaning — writers use this to catch overused words; SEO folks, to check keyword balance.",
            "The analysis runs entirely in your browser: nothing you paste is uploaded anywhere. Case is folded (The and the count together), punctuation is ignored, and the table re-ranks live as you edit.",
        ],
        "howto": [
            "Paste your text into the box — the frequency table builds instantly.",
            "Toggle 'ignore common words' to hide the/a/of-style fillers and see content words.",
            "Scan the top of the table for accidental repetition, then copy or re-edit your text.",
        ],
        "faqs": [
            ("What is word frequency analysis used for?",
             "Writers catch overused words; students check vocabulary variety in essays; SEO writers verify keyword balance; linguists and teachers study text style. It is the fastest way to see what a text is really made of."),
            ("How are words counted?",
             "Text is split on anything that is not a letter or number, and case is folded — 'Dog', 'dog' and 'DOG!' all count as the same word. Numbers count as words too."),
            ("What are stopwords?",
             "High-frequency function words (the, and, of, to…) that carry grammar but little meaning. Hiding them lets the content words rise to the top of the table — usually where the insight is."),
            ("Is my text private?",
             "Completely — counting happens in your browser's JavaScript. Nothing is transmitted, stored or logged, so confidential drafts are safe here."),
        ],
    })

    pages.append(_conv("mb-to-kb", "MB to KB", "megabytes", "kilobytes", 1000, "storage",
                       "On the decimal scale storage vendors use, 1 MB = 1,000 KB exactly. (Operating systems sometimes count in binary kibibytes — 1 MiB = 1,024 KiB — which is where the classic 'my file is bigger than it should be' confusion comes from.)",
                       "Handy anchors: 1 MB = 1,000 KB, 5 MB = 5,000 KB (a photo), 25 MB = 25,000 KB (an email attachment limit)."))
    pages.append(_conv("kb-to-mb", "KB to MB", "kilobytes", "megabytes", 1 / 1000, "storage",
                       "Divide kilobytes by 1,000 to get megabytes on the decimal scale — the one storage and telecom pricing actually uses. A 2,000 KB attachment is a 2 MB upload.",
                       "Handy anchors: 500 KB = 0.5 MB (a heavy photo), 1,000 KB = 1 MB, 10,000 KB = 10 MB (a short video clip)."))

    pages.append({
        "slug": "degrees-to-radians",
        "title": "Degrees to Radians Converter — ° to rad and Back",
        "h1": "Degrees to Radians Converter",
        "desc": "Convert degrees to radians and back instantly: 180° = π rad. Exact π forms for common angles plus decimal values. The trigonometry homework companion.",
        "category": "calculator",
        "keyword": "degrees to radians",
        "tool": "degrad",
        "args": {},
        "intro": [
            "Type an angle in degrees and get it in radians instantly — including the exact form in terms of π when one exists (90° is π/2, not 1.5708). Go the other way too: paste a radian value like 3π/4 or a decimal, and the degrees appear.",
            "Trigonometry, physics and every graphing calculator live in radians, while every compass and protractor lives in degrees — this converter is the bridge between the two worlds, with the π-based exact answers math teachers want to see.",
        ],
        "howto": [
            "Type an angle in degrees — the radian value appears instantly, exact π form when available.",
            "Or type radians (decimals like 1.5708, or π-forms like 3pi/4) to get degrees.",
            "Check the common-angle table below for the values worth memorizing.",
        ],
        "faqs": [
            ("How do you convert degrees to radians?",
             "Multiply by π and divide by 180: radians = degrees × π/180. So 90° = 90 × π/180 = π/2 radians. The converter shows both the exact π-form and the decimal."),
            ("Why does math use radians instead of degrees?",
             "Radians make calculus and trig identities clean: sin(x) Derivative works only in radians, and arc length is simply radius × angle. Degrees are human convention; radians are mathematical nature."),
            ("What is 1 radian in degrees?",
             "About 57.2958°. One radian is the angle where the arc length equals the radius — a full circle is 2π radians, which is why π shows up everywhere in circle math."),
            ("How do I type π into the converter?",
             "Just write pi or 3pi/4 — the converter understands pi as π. Decimals like 1.5708 work equally well."),
        ],
    })

    pages.append({
        "slug": "roman-numerals-1-100",
        "title": "Roman Numerals 1-100 — Complete Chart (I to C)",
        "h1": "Roman Numerals 1–100 Chart",
        "desc": "The complete Roman numerals chart from 1 to 100 (I to C): every number with its Roman numeral, plus the rules for reading them. Free printable reference table.",
        "category": "converter",
        "keyword": "roman numerals 1-100",
        "tool": "romantable",
        "args": {},
        "intro": [
            "The full Roman numerals chart from 1 to 100 — every number with its Roman numeral in a clean four-column table, ready to read at a glance or print for homework. The pattern becomes obvious after 10 rows: tens build on X, XX, XXX, and units repeat I through IX inside each decade.",
            "Below the chart you will find the seven symbols and the one rule that generates the whole system: subtract when a smaller numeral stands before a larger one (IV = 4, XC = 90), otherwise add. That single rule plus seven letters covers every number from 1 to 3,999.",
        ],
        "howto": [
            "Scan the table for your number — rows run 1–25, 26–50, 51–75 and 76–100.",
            "Check the symbols box below to learn the seven letters and their values.",
            "Need a number outside 1–100? Use the full Roman numeral converter linked below the chart.",
        ],
        "faqs": [
            ("What is the Roman numeral for 100?",
             "100 is C (from the Latin centum). Numbers 100–399 then build with C, CC, CCC, and 400 is CD (100 before 500)."),
            ("What are the seven Roman numeral symbols?",
             "I (1), V (5), X (10), L (50), C (100), D (500) and M (1,000). Every Roman number is written with combinations of only these seven letters."),
            ("How do you write 99 in Roman numerals?",
             "XCIX: XC is 90 (100 minus 10) and IX is 9 (10 minus 1). The subtract-before rule applies at both ends of the number."),
            ("Is IIII a valid Roman numeral?",
             "On clocks, traditionally yes (clock faces often show IIII for visual symmetry). In standard written Roman numerals, 4 is always IV."),
        ],
    })

    pages.append({
        "slug": "yes-or-no",
        "title": "Yes or No Decision Maker — Random Answer, Cryptographically Fair",
        "h1": "Yes or No?",
        "desc": "Can't decide? Get a random Yes or No answer instantly. Cryptographically fair 50/50, with a running tally. The fastest decision tool on the internet.",
        "category": "generator",
        "keyword": "yes or no",
        "tool": "yesno",
        "args": {},
        "intro": [
            "Ask a yes/no question, press the button, get an answer. It uses the browser's cryptographically secure random source, so the 50/50 is genuinely fair — no hidden bias toward the answer you were hoping for (that part is still on you).",
            "The tally tracks your session so you can spot when luck keeps saying no. Decisions with real consequences deserve more than a coin toss — but for pizza-or-pasta, this is the tool.",
        ],
        "howto": [
            "Think of your yes/no question.",
            "Press the big button — the answer appears instantly.",
            "Keep asking for best-of series; the tally tracks yes and no counts.",
        ],
        "faqs": [
            ("Is the yes or no answer really random?",
             "Yes — each answer draws from the browser's WebCrypto secure random source, the same generator class used for encryption. Exactly 50/50 in expectation, no patterns."),
            ("Should I make real decisions with this?",
             "For pizza toppings and movie picks, absolutely. For anything with lasting consequences, use it as a tiebreaker after real deliberation, not instead of it."),
            ("Does it remember my questions?",
             "No — the tool sees nothing you are deciding about; it only produces the answer. The tally resets when you leave the page."),
            ("Can I ask more than once?",
             "As many times as you like — the tally counts each answer so you can run best-of-three or spot a suspicious streak."),
        ],
    })

    pages.append({
        "slug": "prime-checker",
        "title": "Prime Number Checker — Is It Prime? Instant Test",
        "h1": "Prime Number Checker",
        "desc": "Check if any number is prime instantly, with the first factor shown when it is not. Handles numbers up to 15 digits using fast trial division and Miller-Rabin.",
        "category": "calculator",
        "keyword": "prime number checker",
        "tool": "prime",
        "args": {},
        "intro": [
            "Type any whole number and find out whether it is prime — and if it is not, one of its factors is shown, so you can see exactly why. Numbers up to 15 digits are checked with deterministic Miller-Rabin plus trial division, which is instant for homework numbers and fast well beyond them.",
            "Prime numbers are the atoms of arithmetic: divisible only by 1 and themselves. They drive cryptography, appear in nature (cicada life cycles), and are the endless fascination of number theory — this checker settles any 'is 1,009 prime?' argument in a keystroke.",
        ],
        "howto": [
            "Type any whole number (2 or greater).",
            "Read the verdict instantly — prime, or composite with a factor shown.",
            "Try famous cases: Mersenne suspects like 2,147,483,647, or your phone number.",
        ],
        "faqs": [
            ("What is a prime number?",
             "A whole number greater than 1 whose only divisors are 1 and itself: 2, 3, 5, 7, 11, 13… Every other number (composites) breaks into prime factors, which is why primes are called the atoms of arithmetic."),
            ("Is 1 a prime number?",
             "No — by definition primes need exactly two distinct divisors, and 1 has only one (itself). Mathematicians agreed on this convention precisely so that unique factorization works."),
            ("What is the largest known prime number?",
             "The largest known primes are Mersenne primes of the form 2^p − 1 — the record has millions of digits and is found by distributed GIMPS projects. This checker handles everyday numbers up to 15 digits instantly."),
            ("Why do primes matter outside math class?",
             "Internet encryption (RSA, Diffie-Hellman) is built on the difficulty of factoring huge composite numbers made of two large primes. Every HTTPS connection starts with prime number mathematics."),
        ],
    })

    pages.append({
        "slug": "factorial-calculator",
        "title": "Factorial Calculator — n! up to 1000, Exact Digits",
        "h1": "Factorial Calculator",
        "desc": "Calculate n! for any n up to 1,000 with full precision — every digit, not scientific notation. Shows the multiplication chain and digit count.",
        "category": "calculator",
        "keyword": "factorial calculator",
        "tool": "factorial",
        "args": {},
        "intro": [
            "Enter n and get n! — the product of every whole number from 1 to n — computed exactly, with all digits shown. Factorials explode fast (10! already has 7 digits, 100! has 158), and most calculators quietly switch to scientific notation and lose the digits. This one keeps every single one.",
            "Factorials count arrangements: 5! is the number of ways to order five things (120), which makes it the backbone of probability, combinatorics, and the permutation formulas behind shuffles, rankings and lottery odds.",
        ],
        "howto": [
            "Type a whole number n between 0 and 1,000.",
            "Read n! with every digit displayed — 0! is defined as 1.",
            "Check the digit count to appreciate how fast factorials grow.",
        ],
        "faqs": [
            ("What is 5 factorial?",
             "5! = 5 × 4 × 3 × 2 × 1 = 120. It counts the ways to arrange 5 items in order — five books on a shelf have 120 possible orders."),
            ("Why is 0 factorial equal to 1?",
             "By definition: there is exactly one way to arrange zero items (do nothing). The convention also makes formulas like n! = n × (n−1)! work for n = 1."),
            ("How big is 100 factorial?",
             "158 digits long — roughly 9.33 × 10^157. It exceeds the number of atoms in the observable universe by a wide margin, which is why exact-digit display matters."),
            ("Where are factorials used?",
             "Counting permutations and combinations, probability (card shuffles, lottery odds), Taylor series in calculus, and algorithm analysis. Anywhere 'how many orderings' appears, factorials are hiding."),
        ],
    })

    pages.append({
        "slug": "random-country-generator",
        "title": "Random Country Generator — Pick a Country, Any Continent",
        "h1": "Random Country Generator",
        "desc": "Get a random country with its flag — filter by continent if you like. For geography class, travel dice, quiz nights and picking where to eat next. Free and instant.",
        "category": "generator",
        "keyword": "random country generator",
        "tool": "country",
        "args": {},
        "intro": [
            "Spin the globe: get a random country with its flag, optionally filtered to one continent. Teachers use it for geography quizzes ('find this country on the map'), travelers use it as a destination dice, quiz teams use it to settle 'name a country starting with K' disputes.",
            "All 195 UN-recognized countries are in the pot, each with equal probability, drawn from your browser's secure random source. Nothing is recorded — your dream (or dreaded) destination stays between you and the button.",
        ],
        "howto": [
            "Optionally pick a continent to narrow the pool.",
            "Press Generate — a country and its flag appear instantly.",
            "Keep rolling for travel inspiration or classroom quizzes.",
        ],
        "faqs": [
            ("How many countries are in the generator?",
             "All 195 UN-recognized countries — 193 member states plus the two observer states (Vatican City and Palestine). Dependencies and territories are excluded to keep the list standard."),
            ("Can I limit it to one continent?",
             "Yes — pick Africa, Americas, Asia, Europe or Oceania from the filter, and draws come from that continent only."),
            ("Is each country equally likely?",
             "Yes — the draw is uniform over the current pool using the browser's WebCrypto secure random source. Small countries are not weighted by size or population."),
            ("Does it show which continent the country is in?",
             "Yes — the result includes the continent and the flag, so it doubles as a flashcard for geography revision."),
        ],
    })

    pages.append({
        "slug": "stones-and-pounds-to-kg",
        "title": "Stone and Pounds to KG — British Weight, Metric Answer",
        "h1": "Stones and Pounds to Kilograms",
        "desc": "Convert the British double-unit weight (like 11 st 7 lb) into kilograms in one step — and back. The way UK bathroom scales and US forms finally agree.",
        "category": "converter",
        "keyword": "stones and pounds to kg",
        "tool": "stlb",
        "args": {},
        "intro": [
            "British weight comes in two parts — 'eleven stone seven' — and converting that to kilograms normally means two steps. This converter takes stones and pounds together (11 st + 7 lb) and returns the exact kilogram value, or runs in reverse from kilograms to the stone-and-pounds split.",
            "One stone is 14 pounds and 6.35029318 kilograms, so the math is simple twice over — but doing it while standing on a scale is exactly the wrong time for arithmetic. Type, read, done.",
        ],
        "howto": [
            "Enter the stones and the extra pounds separately — 11 st 7 lb, not 11.5 st.",
            "The kilogram answer updates instantly; switch to enter kg and get the split back.",
            "Check the pounds-only equivalent below for US-style comparisons.",
        ],
        "faqs": [
            ("How many kg is 11 stone 7 pounds?",
             "11 stone = 69.85 kg; 7 pounds = 3.18 kg; total is about 73.03 kg. The converter does the two-part arithmetic in one step."),
            ("How do I convert stones and pounds to kilograms?",
             "Multiply stones by 6.35029318, multiply pounds by 0.45359237, and add the two. Or just enter both numbers above — same answer, no arithmetic."),
            ("Why do Brits use two units for one weight?",
             "History: the stone was the traditional trade weight for centuries and survived metrication for body weight specifically. So a person is '11 stone 7', never '161 pounds' — even though it is the same thing."),
            ("What is 70 kg in stones and pounds?",
             "About 11 stone and 0.2 pounds (70 kg is 11.02 stone, which is 11 st plus a fraction of a pound). Enter 70 kg in the reverse direction to see the exact split."),
        ],
    })

    pages.append({
        "slug": "feet-and-inches-to-cm",
        "title": "Feet and Inches to CM — Height Converter (5'7\u2033 and Beyond)",
        "h1": "Feet and Inches to Centimeters",
        "desc": "Convert height in feet and inches (like 5'7\u2033) to centimeters in one step — and back. The two-unit height Americans use, translated for the metric world.",
        "category": "converter",
        "keyword": "feet and inches to cm",
        "tool": "ftincm",
        "args": {},
        "intro": [
            "American height comes as two numbers — 5 feet 7 inches — and translating that to centimeters normally means two conversions plus an addition. Enter the feet and inches separately and get the exact centimeter value in one step; enter centimeters to get the feet-and-inches split back.",
            "One foot is exactly 30.48 cm and one inch 2.54 cm, so 5'7\u2033 becomes 170.18 cm. Medical forms, dating profiles and driver's licences finally speak the same language.",
        ],
        "howto": [
            "Enter feet and inches separately — 5 and 7, not 5.7.",
            "The centimeter answer updates instantly (or type cm to get the split back).",
            "Round down or up depending on whether you are filling a form or flattering a profile.",
        ],
        "faqs": [
            ("How many cm is 5 feet 7 inches?",
             "5 ft 7 in = 67 inches total = 170.18 cm. Multiply feet by 30.48, inches by 2.54, and add — or let the converter do both steps."),
            ("How many cm is 6 feet?",
             "Exactly 182.88 cm. Six feet is the classic 'tall' threshold in the US — in most of Europe that is a comfortably above-average 1 m 83."),
            ("Why do Americans use feet and inches for height?",
             "Tradition: the imperial system survived metrication in the US, and height stuck as its stronghold — two units for one measurement, the same way the UK weighs people in stones and pounds."),
            ("Is 170 cm 5 feet 7?",
             "Almost — 170 cm is 5 feet 6.93 inches, which rounds to 5'7\u2033. The reverse converter shows the exact split so forms match precisely."),
        ],
    })

    pages.append({
        "slug": "random-emoji-generator",
        "title": "Random Emoji Generator — Spin the Unicode Wheel",
        "h1": "Random Emoji Generator",
        "desc": "Get random emoji instantly — one at a time or batches, with category filters for faces, animals, food and more. Cryptographically fair, nothing recorded.",
        "category": "generator",
        "keyword": "random emoji generator",
        "tool": "emoji",
        "args": {},
        "intro": [
            "One button, one emoji: draw from a hand-picked pool of hundreds, filtered by category if you want faces, animals, food, objects or symbols only. Generate batches for Slack reactions, creative prompts, social media games and 'describe your day in three emoji' challenges.",
            "Every draw uses the browser's cryptographically secure random source — each emoji is equally likely, and nothing you generate is recorded anywhere.",
        ],
        "howto": [
            "Pick a category or leave it on All.",
            "Set how many emoji you want (1–12) and hit Generate.",
            "Copy the batch with one tap for your bio, message or game.",
        ],
        "faqs": [
            ("How many emoji are in the generator?",
             "Hundreds, spanning faces, animals, food, activities, objects, symbols and travel — curated for ones that display reliably across platforms."),
            ("Why do emoji look different on iPhone vs Android?",
             "Each platform draws its own emoji artwork from the same Unicode standard — same character, different art. The character you copy is identical everywhere; only the picture varies."),
            ("Can I use these commercially?",
             "Emoji characters themselves are just Unicode text and free to use. Platform-specific artwork is copyrighted by its creator, so design your own graphics for commercial artwork."),
            ("Is the draw random?",
             "Yes — powered by the browser's WebCrypto secure random source, so every emoji in the pool is equally likely on every draw."),
        ],
    })

    pages.append({
        "slug": "cm-to-feet-and-inches",
        "title": "CM to Feet and Inches — Height Converter (170 cm and Beyond)",
        "h1": "Centimeters to Feet and Inches",
        "desc": "Convert centimeters to feet and inches in one step — 170 cm is 5 ft 6.9 in. Exact splits for medical forms, dating profiles and US-size clothing.",
        "category": "converter",
        "keyword": "cm to feet and inches",
        "tool": "ftincm",
        "args": {},
        "intro": [
            "Metric height in centimeters translates into the American two-part format — 170 cm becomes 5 feet 6.9 inches — with one division and one remainder. Enter centimeters and get the exact feet-and-inches split, or type feet and inches to go the other way.",
            "This is the conversion behind international paperwork: US medical forms, dating profiles and clothing sizes all want imperial height, while passports and metric countries use centimeters. One converter, both formats, no guessing whether 1.7 m counts as 5'7″.",
        ],
        "howto": [
            "Type your height in centimeters — the feet-and-inches split appears instantly.",
            "Check the inches-only total too, since some US forms ask height purely in inches.",
            "Go the other direction by typing feet and inches into the top fields.",
        ],
        "faqs": [
            ("How many feet and inches is 170 cm?",
             "170 cm is 5 feet 6.93 inches — which everyone rounds to 5'7″. The converter shows the exact decimal so forms can be filled precisely."),
            ("How do I convert cm to feet and inches manually?",
             "Divide centimeters by 2.54 to get total inches (170 ÷ 2.54 = 66.93). That is 5 whole feet (60 inches) plus 6.93 inches — so 170 cm is 5 feet 6.93 inches. The converter removes the two-step risk."),
            ("Is 180 cm 6 feet?",
             "Close but not exact: 180 cm is 70.87 inches = 5 feet 10.87 inches. Six feet is 182.88 cm — nearly 3 cm more than 180."),
            ("What height is 160 cm?",
             "160 cm is 5 feet 2.99 inches — commonly rounded to 5'3″. Enter it above to see the exact figure with the inches-only total."),
        ],
    })

    pages.append(_conv("cubic-meters-to-liters", "Cubic Meters to Liters", "cubic meters", "liters", 1000, "volume",
                       "One cubic meter is exactly 1,000 liters — a neat 1:1,000 that makes aquariums, concrete pours and hot tub sizing straightforward. A 60-liter tank is 0.06 cubic meters; a 2-cubic-meter concrete order is 2,000 liters of the mix.",
                       "Handy anchors: 0.1 m³ = 100 L (a big aquarium), 1 m³ = 1,000 L, 4 m³ = 4,000 L (a small hot tub), 30 m³ = 30,000 L (a garden pond)."))

    pages.append({
        "slug": "hex-to-rgb",
        "title": "Hex to RGB Converter — Color Codes Both Ways, Live Preview",
        "h1": "Hex to RGB Converter",
        "desc": "Convert HEX color codes to RGB and back instantly, with a live color preview. For designers, front-end developers and anyone stuck reading #1A73E8 in a spec.",
        "category": "converter",
        "keyword": "hex to rgb",
        "tool": "hexrgb",
        "args": {},
        "intro": [
            "Paste a hex code like #1A73E8 and get its RGB equivalent (26, 115, 232) instantly — or paste RGB values and get the hex. A live swatch shows the actual color, so you can confirm you have the right shade before it goes into CSS, Figma or a brand guide.",
            "Both notations describe the same color: hex is just RGB written in base 16 (1A hex = 26). The converter accepts 3-digit shorthand too (#F00 = #FF0000) and outputs the 6-digit canonical form.",
        ],
        "howto": [
            "Type a hex code (with or without the #) — RGB values and the color swatch appear instantly.",
            "Or type R, G, B numbers (0–255) to get the hex code.",
            "Copy either format straight into CSS, design tools or documentation.",
        ],
        "faqs": [
            ("How do I convert HEX to RGB?",
             "Split the hex code into three pairs and convert each from base 16 to base 10. #1A73E8: 1A = 26, 73 = 115, E8 = 232 — so RGB(26, 115, 232). The converter does both pairs live."),
            ("What is the difference between HEX and RGB?",
             "None in color — they are two notations for the same values. HEX is compact and universal in design handoffs; RGB(A) supports alpha transparency and reads more explicitly in CSS."),
            ("What are 3-digit hex codes?",
             "Shorthand where each digit is doubled: #F00 expands to #FF0000 (red). It exists for brevity; the converter accepts it and outputs the full 6-digit form."),
            ("What is RGBA?",
             "RGB plus an alpha channel for opacity (0–1). This converter handles opaque colors; add the alpha in CSS separately, e.g. rgba(26, 115, 232, 0.5)."),
        ],
    })

    pages.append(_conv("gallons-to-quarts", "Gallons to Quarts", "gallons (US)", "quarts (US)", 4, "volume",
                       "The US volume ladder's final step: 1 gallon is exactly 4 quarts. Milk jugs, engine oil and soup pots all speak this language — multiply gallons by 4 and the recipe or oil change is settled.",
                       "Handy anchors: 1 gal = 4 qt, 2 gal = 8 qt, 0.5 gal = 2 qt (those half-gallon milk cartons)."))

    pages.append(_conv("kb-to-gb", "KB to GB", "kilobytes", "gigabytes", 1 / 1000000, "storage",
                       "The long jump of the storage ladder: divide kilobytes by 1,000,000 to reach gigabytes (decimal scale). A 500,000 KB photo library is 0.5 GB of cloud space; a 2,000,000 KB video is 2 GB.",
                       "Handy anchors: 100,000 KB = 0.1 GB, 500,000 KB = 0.5 GB, 1,000,000 KB = 1 GB, 10,000,000 KB = 10 GB (a movie download)."))

    pages.append({
        "slug": "age-on-other-planets",
        "title": "Age on Other Planets — Your Age on Mars, Jupiter & More",
        "h1": "Your Age on Other Planets",
        "desc": "Enter your Earth age and see how old you would be on Mercury, Venus, Mars, Jupiter and the rest — each planet's year is a different length. Space science made personal.",
        "category": "calculator",
        "keyword": "age on other planets",
        "tool": "planets",
        "args": {},
        "intro": [
            "A year is one trip around the Sun — but every planet takes a different time to make that trip. Enter your age in Earth years and this calculator shows your age on all eight planets: a 30-year-old is 124 on Mercury (its year is 88 days), just 12 on Uranus, and hasn't even finished one Neptune year.",
            "It is the friendliest possible introduction to orbital periods: the numbers stick because they are about you. Teachers use it for solar system units; everyone else uses it to feel young again (Mercury birthdays come around four times an Earth year).",
        ],
        "howto": [
            "Enter your age in Earth years.",
            "Read your age on all eight planets — each converted by that planet's orbital period.",
            "Note Mercury: you would celebrate a birthday roughly every 88 Earth days.",
        ],
        "faqs": [
            ("How old would I be on Mars?",
             "Divide your Earth age by 1.881 (Mars's year is 1.881 Earth years). A 30-year-old is about 16 on Mars — teenagers on the red planet are in their forties on Earth."),
            ("Why is my age different on other planets?",
             "Age in years counts orbits around the Sun. Mercury orbits in 88 Earth days, Neptune in nearly 165 Earth years — same you, different number of laps completed."),
            ("How old would I be on Mercury?",
             "Multiply your Earth age by about 4.15 — Mercury's year is only 88 days. A 1-year-old baby has already celebrated four Mercury birthdays."),
            ("Which planet makes you oldest?",
             "Mercury, by far — its short orbit means the most birthdays. Neptune is the opposite: no human has completed a single Neptune year since it was discovered in 1846."),
        ],
    })

    pages.append(_conv("km-to-feet", "KM to Feet", "kilometers", "feet", 3280.839895, "distance",
                       "Aviation altitudes, hiking trails and running elevation are quoted in feet even when the distances underneath are metric. One kilometer is 3,280.84 feet — so a 5 km trail climb chart in feet needs this exact factor, not the rough 3,280.",
                       "Handy anchors: 1 km = 3,280.84 ft, 3 km = 9,842 ft (a park loop), 10 km = 32,808 ft, 42 km = 137,795 ft (marathon distance)."))

    pages.append({
        "slug": "name-combiner",
        "title": "Name Combiner — Merge Two Names into One",
        "h1": "Name Combiner",
        "desc": "Blend two names into one: couple names, ship names, baby names, team names or brand ideas. Multiple merge styles, click to copy, everything local.",
        "category": "generator",
        "keyword": "name combiner",
        "tool": "combiner",
        "args": {},
        "intro": [
            "Type two names and get a list of blended possibilities — the classic couple-name game (Brad + Angelina), ship names for fandoms, baby-name brainstorming, or company and product name ideas from two founder names. Several merge styles run at once: front-half + back-half, overlapping sounds, and alternating letters.",
            "Every combination is generated locally in your browser from the two names you type — nothing is sent anywhere, and nothing is recorded. Copy the ones you like and ignore the rest; half the fun is the terrible ones.",
        ],
        "howto": [
            "Type the two names you want to blend.",
            "Read the merged candidates — different splice points produce different styles.",
            "Click any result to copy it; regenerate with different spellings for fresh options.",
        ],
        "faqs": [
            ("How does name blending work?",
             "Each name is split at every syllable-ish boundary, and the front half of one is joined to the back half of the other — both directions. Overlaps where the ending of one name matches the start of the other produce the smoothest blends."),
            ("What is a ship name?",
             "Fandom shorthand for a fictional (or real) couple: Brad + Angelina became 'Brangelina'. Ship names work the same way for TV characters, K-pop pairings and book couples."),
            ("Can I use a blended name for my business?",
             "Blends make memorable brand names (think Pinterest = pin + interest). Before committing, search trademark databases and domain availability — the generator cannot check those for you."),
            ("Does it work with any language?",
             "It works best with Latin-alphabet names. Accented characters are kept as-is, so Spanish, French and Nordic names blend fine."),
        ],
    })

    pages.append(_conv("miles-to-feet", "Miles to Feet", "miles", "feet", 5280, "distance",
                       "The most American conversion there is: one mile is exactly 5,280 feet — a number everyone in the US has memorized and nobody outside can explain. Runners, pilots and real estate listings all hop between these units.",
                       "Handy anchors: 1 mi = 5,280 ft, 3 mi = 15,840 ft (a 5K in feet), 26.2 mi = 138,336 ft (marathon), 100 mi = 528,000 ft (century ride)."))
    pages.append(_conv("yards-to-miles", "Yards to Miles", "yards", "miles", 1 / 1760, "distance",
                       "Football fields are measured in yards, road trips in miles — and 1,760 yards make a mile. Divide yards by 1,760, or remember that 10 football fields (including end zones) is just about a mile.",
                       "Handy anchors: 1,760 yd = 1 mi, 880 yd = 0.5 mi (half-mile track), 100 yd = 0.057 mi (a football field), 1,500 yd = 0.85 mi."))

    pages.append(_conv("inches-to-meters", "Inches to Meters", "inches", "meters", 0.0254, "length",
                       "One inch is exactly 0.0254 meters — a small number that trips mental math constantly. The converter keeps all the decimals straight for TV sizes, tool specs and any spec sheet that mixes the two systems.",
                       "Handy anchors: 1 in = 0.0254 m, 10 in = 0.254 m, 39.37 in = 1 m (the memorable reverse), 70 in = 1.778 m (a tall TV diagonal).", dec=4))

    pages.append({
        "slug": "whitespace-cleaner",
        "title": "Whitespace Cleaner — Trim Lines & Collapse Extra Spaces",
        "h1": "Whitespace Cleaner",
        "desc": "Clean messy text instantly: trim leading and trailing spaces on every line, collapse double spaces, and remove blank lines. Live stats and one-click copy.",
        "category": "text",
        "keyword": "remove extra spaces",
        "tool": "whitespace",
        "args": {},
        "intro": [
            "Copied-from-PDF text, CSV exports and pasted emails all carry the same disease: stray leading spaces, doubled spaces and random blank lines. This cleaner trims every line, squeezes space runs down to a single space, and optionally drops blank lines — with a live count of what was removed.",
            "It pairs with the duplicate remover and line sorter as the list-cleaning toolkit: dedupe, sort, strip whitespace, done. All processing is local JavaScript — nothing you paste leaves your browser.",
        ],
        "howto": [
            "Paste the messy text into the input box.",
            "Toggle trims on or off — trim line edges, collapse inner space runs, drop blank lines.",
            "Read the removal stats, then copy the cleaned result.",
        ],
        "faqs": [
            ("What is whitespace?",
             "Any invisible spacing character: regular spaces, tabs, and the line breaks themselves. Cleaner text with tidy whitespace compiles better, sorts better, and pastes into spreadsheets without phantom columns."),
            ("Does it remove spaces inside sentences?",
             "Only the extra ones: 'hello    world' becomes 'hello world' with one space kept, when collapse mode is on. You choose which cleanups run."),
            ("Is my text uploaded anywhere?",
             "No — cleaning is pure JavaScript in your browser. Disconnect from the internet and it still works; nothing is logged anywhere."),
            ("Can it clean tabs too?",
             "Yes — tab characters are treated as whitespace and handled by the trims and collapsing, alongside regular spaces."),
        ],
    })

    pages.append({
        "slug": "binary-to-hex",
        "title": "Binary to Hex Converter — Binary ⇄ Hexadecimal, Instant",
        "h1": "Binary to Hex Converter",
        "desc": "Convert binary to hexadecimal and back instantly. Byte-grouped, standard notation, with the 4-bit nibble trick explained. Computer science homework solved.",
        "category": "converter",
        "keyword": "binary to hex",
        "tool": "binhex",
        "args": {},
        "intro": [
            "Paste binary code (space-separated bytes like 01001000 01101001) and get clean hexadecimal — 48 69 — or paste hex and get the binary. The conversion works in groups of four bits: each binary nibble maps to exactly one hex digit, which is why programmers write memory dumps in hex.",
            "Both directions update live and strict validation rejects malformed groups instead of guessing. It pairs with the text-to-binary converter for the full journey from human text to machine notation.",
        ],
        "howto": [
            "Paste binary in the first box — space-separated groups of up to 8 bits.",
            "Read the hexadecimal in the second box, one or two hex digits per group.",
            "Paste hex (like 48 69) in the second box to convert back to binary.",
        ],
        "faqs": [
            ("How do you convert binary to hex?",
             "Group the bits in fours from the right, then convert each group: 0100 = 4, 1001 = 9, so 01001001 = 49 in hex. Four bits (a nibble) cover exactly 0–15, the range of one hex digit."),
            ("Why do programmers use hexadecimal?",
             "It is readable shorthand for binary: every byte is exactly two hex digits instead of eight bits. Memory dumps, color codes and MAC addresses all use hex for this reason."),
            ("What is 11111111 in hex?",
             "FF — the maximum value of one byte, 255 in decimal. Eight 1-bits map to two F digits, one per nibble."),
            ("Does the converter handle values longer than a byte?",
             "Yes — groups are converted independently, so 16-bit, 32-bit and arbitrary-length binary strings all work. Keep the groups separated with spaces for reliable parsing."),
        ],
    })

    pages.append({
        "slug": "number-to-words",
        "title": "Number to Words Converter — Numbers in English Text",
        "h1": "Number to Words Converter",
        "desc": "Convert any number to English words instantly: 1234 becomes one thousand two hundred thirty-four. For checks, contracts, invoices and formal documents.",
        "category": "converter",
        "keyword": "number to words",
        "tool": "numwords",
        "args": {},
        "intro": [
            "Type any whole number from 0 to 999 trillion and see it written out in English words — the format legal documents, checks and formal contracts require. Handles hyphenated compound numbers (forty-two), the word 'and' conventions, and the full scale ladder from thousand up to trillion.",
            "Writing amounts in words is not decoration: banks and legal systems require the word form precisely because digits are easy to alter. This converter produces the standard American wording, instantly and without the spelling anxiety.",
        ],
        "howto": [
            "Type your number — digits only, no commas needed.",
            "Read the word form; hyphens and scale words (thousand, million, trillion) are handled automatically.",
            "Copy the result into your document, check or contract.",
        ],
        "faqs": [
            ("How do you write 1234 in words?",
             "One thousand two hundred thirty-four. American convention omits 'and' before the tens (British style would say 'one thousand two hundred and thirty-four') — both are understood."),
            ("How do you write amounts on a check?",
             "Write the cents as a fraction: 'One thousand two hundred thirty-four and 56/100 dollars'. The word form controls the legal amount, which is why it must match the digits exactly."),
            ("What is the biggest number this converts?",
             "Up to 999,999,999,999,999 — the trillions scale. Beyond that, scientific notation is the clearer choice for everyone involved."),
            ("Why do hyphens appear in some numbers?",
             "Compound numbers from twenty-one to ninety-nine take a hyphen (forty-two, seventy-five). It is standard English orthography, and the converter applies it automatically."),
        ],
    })

    pages.append(_conv("gallons-to-cups", "Gallons to Cups", "gallons (US)", "cups (US)", 16, "volume",
                       "The extreme ends of the US volume ladder meet here: 1 gallon is exactly 16 cups. Punch recipes, beverage dispensers and big-batch cooking are where this conversion actually happens.",
                       "Handy anchors: 1 gal = 16 cups, 0.5 gal = 8 cups, 2 gal = 32 cups (a party dispenser), 1 cup = 1/16 gal."))

    pages.append(_conv("mm-to-feet", "MM to Feet", "millimeters", "feet", 0.003280839895, "length",
                       "Metric engineering drawings meet American construction: convert millimeters to feet by dividing by 304.8. A 1,000 mm meter stick is 3.28 feet; a 2,438 mm sheet of plywood is exactly 8 feet.",
                       "Handy anchors: 300 mm = 0.98 ft (about a foot), 1,000 mm = 3.28 ft, 2,438 mm = 8 ft (a plywood sheet), 5,000 mm = 16.4 ft (a parking space)."))

    pages.append({
        "slug": "volume-of-cylinder",
        "title": "Volume of a Cylinder Calculator — pi x r2 x Height",
        "h1": "Volume of a Cylinder Calculator",
        "desc": "Calculate cylinder volume from radius and height: V = pi x r2 x h. Results in cubic units and liters/gallons for tanks, pipes and cans. Instant, with formula shown.",
        "category": "calculator",
        "keyword": "volume of a cylinder",
        "tool": "cylinder",
        "args": {},
        "intro": [
            "Enter the radius and height of a cylinder and get its volume instantly — in cubic units plus liters and US gallons, which is what water tanks, propane cylinders and rain barrels are actually sold in. The formula V = πr²h is shown with your numbers in place, so the homework answer and the intuition both arrive together.",
            "Cylinders are everywhere once you look: cans, pipes, wells, engines, candles. One formula covers them all.",
        ],
        "howto": [
            "Enter the radius of the circular base and the height of the cylinder.",
            "Read the volume in cubic units, then in liters and US gallons for real-world capacity.",
            "Use diameter instead of radius by halving it first — the calculator works in radius.",
        ],
        "faqs": [
            ("What is the formula for the volume of a cylinder?",
             "V = πr²h: pi times the radius squared, times the height. A cylinder with a 5 cm radius and 10 cm height holds about 785 cubic centimeters (0.785 liters)."),
            ("How many gallons is a 24-inch by 48-inch tank?",
             "Radius 12 in, height 48 in: V = π \u00d7 144 \u00d7 48 \u2248 21,715 cubic inches \u2248 94 gallons. The calculator handles the cubic-inch-to-gallon hop when you work in inches."),
            ("Does diameter work instead of radius?",
             "Yes, if you halve it first: a 20 cm diameter cylinder has a 10 cm radius. Entering the diameter as the radius overstates the volume by 4x - the most common mistake with this formula."),
            ("What is the volume of a cylinder in liters per cm of height?",
             "That is the cross-sectional area: πr² cubic centimeters per centimeter of height. A 5 cm radius cylinder holds π \u00d7 25 \u2248 78.5 ml per centimeter - handy for rain gauges and graduations."),
        ],
    })

    pages.append(_conv("ounces-to-tablespoons", "Ounces to Tablespoons", "fluid ounces", "tablespoons", 2, "volume",
                       "The kitchen's smallest ladder: one US fluid ounce is exactly 2 tablespoons. Syrup doses, cocktail recipes and half-recipe scaling all land on this conversion — and since it is a clean 2:1, the only real risk is using the weight ounce instead of the fluid ounce.",
                       "Handy anchors: 1 fl oz = 2 tbsp, 2 fl oz = 4 tbsp (a quarter cup), 4 fl oz = 8 tbsp (half a cup), 8 fl oz = 16 tbsp (a full cup)."))

    pages.append({
        "slug": "days-until-tax-day",
        "title": "How Many Days Until Tax Day? April 15 Countdown",
        "h1": "How Many Days Until Tax Day?",
        "desc": "Live countdown to Tax Day - April 15. Track the filing deadline for federal taxes, extensions and quarterly estimated payments. Updates every second.",
        "category": "countdown",
        "keyword": "days until tax day",
        "tool": "countdown",
        "args": {"event": "Tax Day", "month": 4, "day": 15, "emoji": "💰"},
        "intro": [
            "This live countdown shows exactly how long until Tax Day - April 15, the federal income tax filing deadline in the United States. The timer computes the next April 15 automatically and rolls over the moment it passes, so you always know the real number of filing days left.",
            "Procrastinators, extension filers and quarterly estimated-payment taxpayers all share the same April anxiety. Bookmark the page and check the honest number instead of guessing.",
        ],
        "howto": [
            "Open the page - the countdown to April 15 starts immediately.",
            "Read days remaining for filing planning, or watch the final-hours timer in April.",
            "After Tax Day passes, the timer rolls to next year automatically.",
        ],
        "faqs": [
            ("When is Tax Day?",
             "April 15 in most years - the federal individual income tax filing deadline. When April 15 falls on a weekend or a DC holiday, the deadline shifts to the next business day (in 2026 it is Wednesday, April 15)."),
            ("What happens if I miss Tax Day?",
             "File as fast as possible: the late-filing penalty is 5% of unpaid taxes per month, capped at 25%. Filing an extension by the deadline moves the paperwork deadline to October - but not the payment deadline."),
            ("When are quarterly estimated taxes due?",
             "For self-employed taxpayers: April 15, June 15, September 15 and January 15 of the following year. The countdown above tracks the April one; the others follow the same quarterly rhythm."),
            ("Does the countdown include state tax deadlines?",
             "Most states align their deadline with the federal April 15 date, but a few differ. Check your state revenue department for local deadlines - the federal countdown above is the one almost everyone shares."),
        ],
    })

    pages.append(_conv("quarts-to-pints", "Quarts to Pints", "quarts (US)", "pints (US)", 2, "volume",
                       "The middle rung of the US volume ladder: 1 quart is exactly 2 pints. Soup recipes say quarts, milk cartons say pints, and this converter keeps the conversation going without a calculator.",
                       "Handy anchors: 1 qt = 2 pt, 4 qt = 8 pt (a gallon), 0.5 qt = 1 pt (a big soda), 3 qt = 6 pt (an ice cream haul)."))
    pages.append(_conv("cups-to-quarts", "Cups to Quarts", "cups (US)", "quarts (US)", 1 / 4, "volume",
                       "Big-batch cooking jumps from cups straight to quarts — 16 cups to a quart, so halving a 50-serving punch recipe is division the recipe never warns you about. Type the cups, get the quarts, get back to the kitchen.",
                       "Handy anchors: 4 cups = 1 qt, 8 cups = 2 qt, 12 cups = 3 qt, 16 cups = 4 qt (a full gallon)."))

    pages.append(_conv("gb-to-kb", "GB to KB", "gigabytes", "kilobytes", 1000000, "storage",
                       "The full storage ladder in one hop: multiply gigabytes by 1,000,000 (a million) to reach kilobytes on the decimal scale. Useful when a system asks for KB and all you know is the GB figure.",
                       "Handy anchors: 1 GB = 1,000,000 KB, 16 GB = 16,000,000 KB (a phone plan), 64 GB = 64,000,000 KB (a flash drive), 1 TB = 1,000,000,000 KB."))
    pages.append(_conv("liters-to-cups", "Liters to Cups", "liters", "cups (US)", 4.1666667, "volume",
                       "Convert liter-bottle recipes into American cup measurements: one liter is about 4.17 cups (4 cups plus a splash). Metric recipe in hand, US measuring cups in the drawer - this is the bridge.",
                       "Handy anchors: 0.5 L = 2.11 cups, 1 L = 4.17 cups, 2 L = 8.45 cups, 4 L = 16.9 cups (roughly a gallon)."))

    pages.append(_conv("cups-to-pints", "Cups to Pints", "cups (US)", "pints (US)", 1 / 2, "volume",
                       "Two cups make a pint - the conversion hiding in every 'a pint is a pound the world around' saying (for water, close enough). Ice cream pints, pub glasses and recipe halvings all cross this line.",
                       "Handy anchors: 2 cups = 1 pt, 4 cups = 2 pt, 6 cups = 3 pt, 1 pt = 2 cups (remember it by the pint of ice cream you finished alone)."))
    pages.append(_conv("pints-to-cups", "Pints to Cups", "pints (US)", "cups (US)", 2, "volume",
                       "Multiply pints by 2 and you have cups - the friendliest member of the US volume family. A pint of blueberries is 2 cups; a pint of cream is 2 cups; the pattern is mercifully simple.",
                       "Handy anchors: 1 pt = 2 cups, 2 pt = 4 cups, 3 pt = 6 cups, 4 pt = 8 cups (half a gallon)."))

    pages.append(_conv("cm-to-feet", "CM to Feet", "centimeters", "feet", 0.03280839895, "length",
                       "Convert centimeters straight to feet - skipping the inches detour. One centimeter is 0.0328 feet, so 170 cm is 5.58 feet (5 feet 6.9 inches if you want the split). Room dimensions, TV sizes and European furniture specs all need this hop.",
                       "Handy anchors: 100 cm = 3.28 ft, 180 cm = 5.91 ft, 200 cm = 6.56 ft, 250 cm = 8.20 ft (a large sofa length)."))
    pages.append(_conv("meters-to-inches", "Meters to Inches", "meters", "inches", 39.37007874, "length",
                       "One meter is 39.37007874 inches - a number engineers memorize as 'about 39.37'. Television diagonals, lumber lengths and fabric bolts bounce between the two, and this converter keeps every decimal place honest.",
                       "Handy anchors: 1 m = 39.37 in, 2 m = 78.74 in, 0.5 m = 19.69 in, 3 m = 118.11 in (a large TV is 75 in diagonal)."))

    pages.append(_conv("yards-to-inches", "Yards to Inches", "yards", "inches", 36, "length",
                       "Fabric stores sell by the yard; pattern pieces are marked in inches. One yard is exactly 36 inches, so the math is a clean multiply by 36 - two yards of fabric is 72 inches of material.",
                       "Handy anchors: 1 yd = 36 in, 2 yd = 72 in (fabric length), 10 yd = 360 in, 100 yd = 3,600 in (a football field minus end zones)."))
    pages.append(_conv("grams-to-kilograms", "Grams to Kilograms", "grams", "kilograms", 1 / 1000, "weight",
                       "The metric system at its simplest: 1,000 grams make a kilogram, so divide by 1,000. Kitchen scales read grams, bathroom scales read kilograms - this converter keeps recipes, parcels and fitness tracking on the same page.",
                       "Handy anchors: 500 g = 0.5 kg (a bottle of water), 750 g = 0.75 kg (a pack of flour), 1,000 g = 1 kg (a kilo of sugar), 2,500 g = 2.5 kg (a bag of rice)."))

    pages.append(_conv("kilograms-to-ounces", "KG to Ounces", "kilograms", "ounces", 35.27396195, "weight",
                       "The cross-system kitchen conversion: metric recipes in kilograms, American packaging in ounces. One kilogram is 35.27 ounces (just over 2.2 pounds of ounces), so a 1 kg bag of flour is 35 and a bit ounces.",
                       "Handy anchors: 0.5 kg = 17.64 oz, 1 kg = 35.27 oz, 2 kg = 70.55 oz, 5 kg = 176.37 oz (a big bag of rice)."))
    pages.append(_conv("ounces-to-kilograms", "Ounces to Kilograms", "ounces", "kilograms", 1 / 35.27396195, "weight",
                       "Convert ounces to kilograms when American package sizes meet metric recipes or shipping forms. Divide ounces by 35.274 - or remember an ounce is about 28 grams and work in two hops. This converter skips the hops.",
                       "Handy anchors: 8 oz = 0.23 kg (a block of cream cheese), 16 oz = 0.45 kg (a pound), 32 oz = 0.91 kg (a quart of liquid), 100 oz = 2.83 kg."))

    pages.append({
        "slug": "text-to-morse",
        "title": "Text to Morse Code Converter — Letters ⇄ Dots and Dashes",
        "h1": "Text to Morse Code Converter",
        "desc": "Convert text to Morse code and back instantly. Standard International Morse with letters, numbers and punctuation. Learn, practice or send secret messages.",
        "category": "converter",
        "keyword": "text to morse code",
        "tool": "morse",
        "args": {},
        "intro": [
            "Type any message and read it in International Morse code - dots and dashes with proper letter spacing - or paste Morse and decode it back into readable text. Numbers and common punctuation are supported alongside the full alphabet.",
            "Morse is the original text compression: SOS (\u00b7\u00b7\u00b7 \u2013 \u2013 \u2013 \u00b7\u00b7\u00b7) has been saving lives since 1906. Whether you are learning for a radio license, building an escape-room puzzle, or just want to tap messages on a desk, this is the two-way bridge.",
        ],
        "howto": [
            "Type your message in the first box - Morse appears instantly with letters separated by spaces.",
            "Paste Morse code in the second box (dots, dashes, spaces between letters) to decode it.",
            "Use the SOS example to check the spacing convention works as expected.",
        ],
        "faqs": [
            ("How does Morse code encode letters?",
             "Each letter is a unique sequence of dots (short marks) and dashes (long marks): A is \u00b7\u2013, B is \u2013\u00b7\u00b7\u00b7, and the most common letters get the shortest codes - E is a single dot. Spaces separate letters; a slash or wider gap separates words."),
            ("What is SOS in Morse code?",
             "SOS is \u00b7\u00b7\u00b7 \u2013 \u2013 \u2013 \u00b7\u00b7\u00b7. It was chosen for its unmistakable pattern, not as an abbreviation - it is not actually 'Save Our Souls'."),
            ("Is Morse code still used today?",
             "Yes - amateur radio operators, aviation navigation beacons, assistive technology for people with limited mobility, and a surprising number of escape rooms and puzzles. It is no longer required for maritime licenses, retired in 1999."),
            ("Can I decode Morse without spaces between letters?",
             "Not reliably - letter spacing is part of the code. ...-.. could be many things. The decoder needs spaces between letters (and slashes or extra gaps between words) to parse honestly."),
        ],
    })

    pages.append(_conv("feet-to-yards", "Feet to Yards", "feet", "yards", 1 / 3, "length",
                       "Three feet make a yard - the tailoring, football and landscaping conversion. Divide feet by 3, or count yards in threes: a 6-foot person is exactly 2 yards tall.",
                       "Handy anchors: 3 ft = 1 yd, 6 ft = 2 yd, 30 ft = 10 yd (first-down marker), 100 ft = 33.33 yd."))

    pages.append({
        "slug": "epoch-timestamp",
        "title": "Epoch Timestamp Converter — Unix Time to Date and Back",
        "h1": "Epoch Timestamp Converter",
        "desc": "Convert Unix epoch timestamps to human dates and back, live. Shows the current timestamp ticking, accepts seconds or milliseconds, all local JavaScript.",
        "category": "converter",
        "keyword": "epoch timestamp converter",
        "tool": "epoch",
        "args": {},
        "intro": [
            "Every API response, database row and log line stores time as a Unix timestamp - seconds since January 1, 1970, UTC. This converter turns those numbers back into dates humans can read, and turns dates into timestamps for the query you are about to write. It also shows the current timestamp ticking live, which is the fastest way to check whether a mystery number is in seconds or milliseconds.",
            "Developers live in this conversion daily; everyone else meets it once and never forgets it. Paste, read, move on - all locally in your browser.",
        ],
        "howto": [
            "Paste a Unix timestamp (seconds) - the UTC and local date appear instantly.",
            "Toggle the milliseconds switch if your number is 13 digits.",
            "Or pick a date and time to get its timestamp for your API call.",
        ],
        "faqs": [
            ("What is a Unix timestamp?",
             "The number of seconds elapsed since 00:00:00 UTC on January 1, 1970 - the moment computers agreed to call zero. Right now it is a 10-digit number; in 2038 the 32-bit version overflows, which is the Y2K of embedded systems."),
            ("Why is my timestamp 13 digits?",
             "It is in milliseconds, not seconds - common in JavaScript (Date.now()). Divide by 1,000 or use the milliseconds toggle to convert honestly."),
            ("Does the timestamp depend on my time zone?",
             "The number itself is always UTC-based. The converter shows it both as UTC and in your local time zone, so the same timestamp reads differently but means identically."),
            ("What happens at timestamp 0?",
             "That is the Unix epoch: January 1, 1970, 00:00:00 UTC. Negative timestamps count backwards from it - historical dates before 1970 work fine."),
        ],
    })

    pages.append(_conv("inches-to-yards", "Inches to Yards", "inches", "yards", 1 / 36, "length",
                       "Fabric and flooring measurements collapse from inches into yards by dividing by 36. A 54-inch-wide bolt of fabric is 1.5 yards wide - the number the cutting table actually works with.",
                       "Handy anchors: 36 in = 1 yd, 18 in = 0.5 yd, 54 in = 1.5 yd (fabric width), 72 in = 2 yd (a tall person in yards)."))
    pages.append(_conv("miles-to-meters", "Miles to Meters", "miles", "meters", 1609.344, "distance",
                       "One mile is exactly 1,609.344 meters - the conversion that makes American race distances readable to the metric world. A mile of running is 1,609 meters of track laps.",
                       "Handy anchors: 1 mi = 1,609 m, 2 mi = 3,219 m, 5 mi = 8,047 m, 10 mi = 16,093 m (a 10-miler)."))

    pages.append(_conv("km-to-yards", "KM to Yards", "kilometers", "yards", 1093.6132983, "distance",
                       "Golf courses, athletic tracks and cross-country courses mix kilometers and yards more often than any sane person expects. One kilometer is 1,093.61 yards - just over a kilometer of fairway per thousand yards on the card.",
                       "Handy anchors: 1 km = 1,093.61 yd, 2 km = 2,187.23 yd, 5 km = 5,468 yd (a parkrun), 10 km = 10,936 yd."))
    pages.append(_conv("minutes-to-days", "Minutes to Days", "minutes", "days", 1 / 1440, "time",
                       "Uptime logs, billing records and binge-watching tallies all end up in minutes - and humans think in days. Divide minutes by 1,440 (60 x 24) and the number finally means something: 10,080 minutes is exactly one week.",
                       "Handy anchors: 60 min = 1 hr, 1,440 min = 1 day, 10,080 min = 1 week, 43,200 min = 30 days."))

    pages.append(_conv("km-to-inches", "KM to Inches", "kilometers", "inches", 39370.07874, "distance",
                       "The longest leap on the length ladder: one kilometer is 39,370.08 inches. rarely needed by hand, constantly needed by spreadsheets - map scales, pacing charts and model railroading all hit it eventually.",
                       "Handy anchors: 1 km = 39,370 in, 0.5 km = 19,685 in, 2 km = 78,740 in, 42.2 km = 1,661,457 in (a marathon, in inches)."))
    pages.append(_conv("inches-to-km", "Inches to KM", "inches", "kilometers", 1 / 39370.07874, "distance",
                       "Divide inches by 39,370.08 to reach kilometers - the reverse of the most lopsided conversion on the length ladder. Odometer discrepancies, model scales and printable map bars all produce inches that reports want in kilometers.",
                       "Handy anchors: 39,370 in = 1 km, 19,685 in = 0.5 km, 3,937 in = 0.1 km, 787 in = 0.02 km."))

    pages.append({
        "slug": "days-until-friday",
        "title": "How Many Days Until Friday? Live Weekly Countdown",
        "h1": "How Many Days Until Friday?",
        "desc": "Live countdown to the next Friday - updates every second and rolls over automatically every week. The weekend countdown that never lies.",
        "category": "countdown",
        "keyword": "how many days until friday",
        "tool": "countdown",
        "args": {"event": "Friday", "titleUnit": "days to Friday", "emoji": "🏭", "rule": {"weekly": True, "weekday": 5}},
        "intro": [
            "The honest answer to the most-asked workplace question on Earth, refreshed every second. This countdown targets the upcoming Friday automatically - once Friday arrives it rolls to the next one, so it never shows a stale number or counts down to a Friday months away.",
            "Fridays recur every seven days, which makes this the only countdown with a guaranteed next date forever. Bookmark it: the tab title keeps the days-remaining visible even when you are buried in seventeen other tabs.",
        ],
        "howto": [
            "Open the page any day of the week - the countdown targets the upcoming Friday automatically.",
            "Watch the timer through Friday itself; after midnight it rolls to next week.",
            "Keep the tab open - the browser tab title shows the days remaining at all times.",
        ],
        "faqs": [
            ("How many days until Friday?",
             "Between 0 and 6, depending on today. The countdown shows the exact days, hours and minutes to midnight of the upcoming Friday, updating live."),
            ("Does the countdown roll over after Friday?",
             "Yes - the moment Friday ends it starts counting to the next one. There is always a Friday coming, which is the quiet beauty of this page."),
            ("What about Saturday - is it 6 or 7 days until Friday?",
             "On Saturday the countdown reads 6 days (the next Friday). Counting Saturday-to-Friday as 6 matches how calendars and every other countdown handle weekly recurrences."),
            ("Why do people search for days until Friday?",
             "Because the weekend is the finish line of the working week - search interest for Friday countdowns spikes every Sunday evening and Monday morning worldwide. This page is the answer, permanently accurate."),
        ],
    })

    pages.append({
        "slug": "business-days-calculator",
        "title": "Business Days Calculator — Working Days Between Two Dates",
        "h1": "Business Days Calculator",
        "desc": "Count working days (Monday-Friday) between two dates instantly, with weekend days shown separately. For deadlines, SLA clocks, lead times and notice periods.",
        "category": "calculator",
        "keyword": "business days calculator",
        "tool": "datediff",
        "args": {},
        "intro": [
            "Pick two dates and see the working days between them - the count that actually matters for SLA clocks, shipping lead times, contract notice periods and 'we need it by Friday' promises. Weekend days are counted separately so both numbers are on screen.",
            "The weekday count excludes Saturdays and Sundays automatically; public holidays vary by country, so add those on top of this number for your region. Your last inputs are remembered on the page between visits.",
        ],
        "howto": [
            "Set the start date - your inputs are remembered for next visit.",
            "Set the end date - weekdays, weeks and total days update instantly.",
            "Add public holidays manually if your deadline logic counts them as non-working.",
        ],
        "faqs": [
            ("How do I calculate business days between two dates?",
             "Count every Monday-Friday between the dates and skip weekends. A Monday-to-Friday span is 4 business days (or 5 if you count the end date). This calculator shows the count automatically."),
            ("How long is 10 business days?",
             "Exactly two calendar weeks, when no public holidays interfere. 'Ships in 10 business days' from a Wednesday means roughly two and a half calendar weeks."),
            ("Does the count include public holidays?",
             "No - holidays differ by country and year. Add them manually on top of the weekday count for your region's calendar."),
            ("Can I count business days since a past date?",
             "Yes - set the past date as start and today as end. Useful for SLA breach checks, invoice aging and probation periods."),
        ],
    })

    pages.append({
        "slug": "days-until-the-weekend",
        "title": "How Many Days Until the Weekend? Live Saturday Countdown",
        "h1": "How Many Days Until the Weekend?",
        "desc": "Live countdown to the weekend - Saturday, 00:00, updating every second and rolling over every week. The tab title keeps the count visible all week long.",
        "category": "countdown",
        "keyword": "how many days until the weekend",
        "tool": "countdown",
        "args": {"event": "the Weekend", "titleUnit": "days to Weekend", "emoji": "🏖️", "rule": {"weekly": True, "weekday": 6}},
        "intro": [
            "The weekend officially starts at midnight on Saturday - and this countdown counts down to that exact moment, every week, forever. If you count Friday night as the weekend too, our Friday countdown is one tab away; this one is for the purists.",
            "The browser tab title carries the days remaining at all times, so the number follows you across your seventeen open work tabs - a little reminder that Saturday is mathematically approaching.",
        ],
        "howto": [
            "Open the page any day - it locks onto the upcoming Saturday midnight automatically.",
            "Watch the final Saturday countdown in hours; after midnight it rolls to next week.",
            "Keep the tab pinned - the title keeps the countdown visible from any other tab.",
        ],
        "faqs": [
            ("How many days until the weekend?",
             "Between 0 and 6 depending on today - Saturday morning counts as arrived (0 days), Sunday night is 6 days away. The countdown targets Saturday 00:00 exactly."),
            ("Does Friday night count as the weekend?",
             "Culturally yes, technically no - the calendar weekend is Saturday-Sunday, so this page counts to Saturday 00:00. If your weekend starts Friday evening, the Friday countdown is the one for you."),
            ("Does it work all week?",
             "Yes - it rolls over automatically every Saturday midnight to the next one. There is always another weekend coming."),
            ("Why keep it in a tab all week?",
             "The tab title shows the live days-remaining, so the weekend follows you across every tab - half motivation, half countdown clock."),
        ],
    })

    pages.append(_conv("hours-to-days", "Hours to Days", "hours", "days", 1 / 24, "time",
                       "Shift logs, hospital rotas, battery life and marathon streams all produce hours that only make sense as days. Divide hours by 24 - a 72-hour fast is exactly 3 days, a 8,760-hour year is 365.",
                       "Handy anchors: 24 hr = 1 day, 48 hr = 2 days, 72 hr = 3 days (the classic movie title), 168 hr = 1 week."))

    pages.append({
        "slug": "words-to-number",
        "title": "Words to Number Converter — English Number Words to Digits",
        "h1": "Words to Number Converter",
        "desc": "Convert English number words to digits: 'two thousand three hundred forty-two' becomes 2,342. Handles negatives, hyphens, 'and', up to trillions.",
        "category": "converter",
        "keyword": "words to number",
        "tool": "wordstonum",
        "args": {},
        "intro": [
            "Paste an amount written out in words - from a check, a contract clause, or an old legal document - and get the digits: 'two thousand three hundred forty-two' becomes 2,342. Handles negatives, hyphenated compounds, the British 'and', and scale words up to trillion.",
            "It is the exact reverse of our number-to-words converter, and together the pair verifies legal amounts in both directions: write it in words, convert it back to digits, and confirm the numbers match before anyone signs anything.",
        ],
        "howto": [
            "Type or paste the number in words - capitalization does not matter.",
            "The digits appear instantly, formatted with thousand separators.",
            "Check the negative and scale handling on tricky inputs like 'minus twelve billion'.",
        ],
        "faqs": [
            ("How do you convert number words to digits?",
             "Small words map to values (twenty = 20, hundred = 100), scale words multiply (thousand, million), and everything adds up left to right - 'forty-two hundred' is 42 x 100 = 4,200. The parser handles the whole grammar."),
            ("Does it understand the word 'and'?",
             "Yes - 'one hundred and five' parses the same as 'one hundred five'. Both British and American conventions are accepted."),
            ("What about hyphenated numbers?",
             "Hyphens are handled natively: 'forty-two' and 'forty two' both parse to 42, matching how the number-to-words converter writes them back."),
            ("How large can the number be?",
             "Up to the trillions scale - the same ceiling as legal and financial documents actually use. Beyond that, scientific notation serves better than words anyway."),
        ],
    })

    pages.append({
        "slug": "speed-distance-time",
        "title": "Speed Distance Time Calculator — Find the Missing Value",
        "h1": "Speed, Distance & Time Calculator",
        "desc": "Enter any two of speed, distance or time and get the third - in km/h, mph, or your own units. With h:mm:ss output for runs, drives and deliveries.",
        "category": "calculator",
        "keyword": "speed distance time calculator",
        "tool": "sdt",
        "args": {},
        "intro": [
            "The triangle every driving instructor, runner and dispatcher draws on a napkin: speed = distance / time. Enter any two of the three values and this calculator solves the third - a 120 km trip at 80 km/h takes exactly 1.5 hours, shown as 1:30:00 for the trip computer.",
            "Distance and speed default to kilometers and km/h but accept any consistent units - miles with mph, meters with seconds - because the formula does not care as long as the units agree. The time field accepts h:mm:ss, which is how GPS watches and delivery apps actually report durations.",
        ],
        "howto": [
            "Fill in any two fields: distance, speed, or time.",
            "The third value solves instantly - time appears in both decimal and h:mm:ss form.",
            "Leave the field blank for the value you want to find; changing inputs re-solves live.",
        ],
        "faqs": [
            ("How do you calculate speed, distance and time?",
             "The triangle: speed = distance / time, distance = speed x time, time = distance / speed. Cover the value you want and the formula remains. Fill any two fields above and the third solves itself."),
            ("How long does it take to drive 100 km at 80 km/h?",
             "100 / 80 = 1.25 hours = 1 hour 15 minutes. The calculator shows both forms so the answer drops straight into a log or trip plan."),
            ("How do I calculate average speed from a journey?",
             "Enter the total distance and the total duration (in h:mm:ss) - the speed field solves as the true average, including stops. Note it is average speed, not the maximum shown on the dashboard."),
            ("Does it work for running pace?",
             "Yes - enter the race distance and your finishing time, and the speed field gives your average speed; divide further for pace per kilometer if you think in minutes-per-km."),
        ],
    })

    pages.append({
        "slug": "reverse-text",
        "title": "Reverse Text Generator — Flip Words & Characters Backwards",
        "h1": "Reverse Text Generator",
        "desc": "Reverse text two ways: flip the whole string character-by-character, or reverse word order only. Live output, one-tap copy, everything local.",
        "category": "text",
        "keyword": "reverse text",
        "tool": "reverser",
        "args": {},
        "intro": [
            "Paste text and read it backwards - either character-by-character (esrever) or with the word order reversed (backwards the in order word). Puzzle makers, bio stylers and anyone playing with palindromes use both modes constantly.",
            "The output updates live and copies in one tap. Unlike the upside-down generator (which substitutes look-alike Unicode letters), reversing keeps your exact original characters in a new order - so it survives every platform perfectly.",
        ],
        "howto": [
            "Paste or type your text into the input box.",
            "Toggle between reversing characters and reversing word order.",
            "Copy the result with one tap - it pastes as plain text everywhere.",
        ],
        "faqs": [
            ("How do I reverse text?",
             "Paste it and switch to character mode - the whole string flips end-to-end. Word mode keeps each word intact but reverses their order, which is handy for lists."),
            ("What is a palindrome checker trick?",
             "Reverse a word in character mode: if the output reads identically (like racecar), it is a palindrome. The visual match is the fastest palindrome test there is."),
            ("Does reversed text work on social media?",
             "Yes - unlike upside-down text, reversed characters are your own ordinary letters, so they paste cleanly everywhere including strict platforms."),
            ("Is my text uploaded?",
             "No - reversing runs entirely in your browser. Nothing is transmitted or stored."),
        ],
    })

    pages.append({
        "slug": "weight-on-moon",
        "title": "Weight on the Moon Calculator — Your Moon Weight in Seconds",
        "h1": "Weight on the Moon",
        "desc": "Enter your Earth weight and see what you would weigh on the Moon (x0.165), Mars, Jupiter and every planet. Same body, different gravity - science class made personal.",
        "category": "calculator",
        "keyword": "weight on the moon",
        "tool": "moonweight",
        "args": {},
        "intro": [
            "Your weight is your mass times local gravity - and lunar gravity is one-sixth of Earth's. Enter your Earth weight and see your Moon weight instantly, plus Mars, Jupiter and the rest of the solar system, because the scale reading is a local opinion.",
            "Important distinction for science class: your mass never changes anywhere in the universe; weight is just the force your mass experiences under local gravity. On the Moon you would weigh 16% of Earth - but you would still be exactly you.",
        ],
        "howto": [
            "Enter your weight on Earth (kg or lb - the ratio works the same in any unit).",
            "Read your weight on the Moon, Mars, Jupiter and the other planets.",
            "Note Jupiter: heavier gravity means the same you weighs 2.5 times more there.",
        ],
        "faqs": [
            ("How much would I weigh on the Moon?",
             "Multiply your Earth weight by 0.165 (lunar gravity is 1.62 m/s2 versus Earth's 9.81). A 60 kg person weighs about 9.9 kg-force on the Moon - light enough to jump over a car, in theory."),
            ("Why is weight different but mass the same?",
             "Mass is the amount of matter in you - constant everywhere. Weight is mass times local gravitational acceleration, so it changes with location while you stay the same size."),
            ("Where would I weigh the most in the solar system?",
             "Jupiter: its gravity is 2.53 times Earth's, so a 70 kg person weighs 177 kg there. You could not stand, breathe or survive - but the scale reading would be impressive."),
            ("Is this calculation scientifically accurate?",
             "The gravity ratios are the standard values used in physics education. Real weight also varies slightly with altitude and latitude even on Earth, by about 0.5% - far less than the planetary differences shown here."),
        ],
    })

    pages.append({
        "slug": "binary-to-decimal",
        "title": "Binary to Decimal Converter — Base 2 to Base 10 and Back",
        "h1": "Binary to Decimal Converter",
        "desc": "Convert binary to decimal and decimal to binary instantly. Positional values explained (128 64 32 16 8 4 2 1), strict validation, CS homework solved.",
        "category": "converter",
        "keyword": "binary to decimal",
        "tool": "bindec",
        "args": {},
        "intro": [
            "Type a binary number (only 0s and 1s) and get its decimal value instantly - or type a decimal and get the binary form. The positional logic is what makes it click: each bit is worth double the one to its right, so 1010 is 8+0+2+0 = 10.",
            "This is the foundation under every hex conversion and every bit of computer memory. The converter validates strictly - a stray 2 or a malformed group is flagged rather than silently misread, because in base-2 arithmetic there is no almost.",
        ],
        "howto": [
            "Type a binary number (0s and 1s only) in the first box - the decimal appears instantly.",
            "Type a decimal number in the second box to get its binary form.",
            "Try 11111111 and watch it become 255 - the biggest number one byte can hold.",
        ],
        "faqs": [
            ("How do you convert binary to decimal?",
             "Each bit is worth a power of 2, doubling right to left: 1, 2, 4, 8, 16... Add the values of the 1-bits. 1101 = 8 + 4 + 0 + 1 = 13. The converter does the sum as you type."),
            ("How do you convert decimal to binary?",
             "Divide by 2 repeatedly and read the remainders bottom-up - or subtract the largest power of 2 at each step. The converter uses the same algorithm internally and shows the binary padded to full bytes."),
            ("Why do computers use binary?",
             "Two states (on/off, high/low voltage) are physically reliable; ten states are not. Every number, letter and pixel ends up as patterns of bits, which is why binary conversion is CS 101."),
            ("What is 2 to the power of 10 in binary terms?",
             "1 followed by ten zeros: 10000000000 binary = 1,024 decimal. That near-thousand is why 'kilo' in computing historically meant 1,024 - the kilobyte that was secretly 1,024 bytes."),
        ],
    })

    pages.append(_conv("tablespoons-to-ml", "Tablespoons to ML", "tablespoons", "milliliters", 14.7867648, "volume",
                       "US recipes say tablespoons, metric jugs say milliliters - and one US tablespoon is 14.7868 ml (15 in the rounded convention most kitchens use). The converter shows both the precise and the practical answer, because pancakes forgive rounding but chemistry does not.",
                       "Handy anchors: 1 tbsp = 14.79 ml, 2 tbsp = 29.57 ml (one fluid ounce), 4 tbsp = 59.15 ml (a quarter cup), 16 tbsp = 236.6 ml (a full cup)."))

    pages.append({
        "slug": "kelvin-converter",
        "title": "Kelvin Converter — Kelvin, Celsius & Fahrenheit Together",
        "h1": "Kelvin Converter",
        "desc": "Convert Kelvin to Celsius and Fahrenheit in one view - type in any of the three scales and the others update live. Physics and chemistry homework, solved with the exact offsets shown.",
        "category": "calculator",
        "keyword": "kelvin converter",
        "tool": "kelvin",
        "args": {},
        "intro": [
            "Three temperature scales, one converter: type a value into Kelvin, Celsius or Fahrenheit and the other two update instantly. Kelvin is Celsius shifted by exactly 273.15 - same degree size, different zero - while Fahrenheit needs both an offset and a fraction. The formulas are displayed with your numbers in place.",
            "Kelvin matters because it is absolute: 0 K is the temperature where molecular motion stops, which is why gas laws and thermodynamics refuse to work in degrees. This converter is the bridge between the physics classroom and the weather report.",
        ],
        "howto": [
            "Type a value into any of the three boxes - Kelvin, Celsius or Fahrenheit.",
            "The other two scales update instantly, with the conversion formulas shown below.",
            "Note 0 K (absolute zero) equals -273.15 C: the coldest anything can ever be.",
        ],
        "faqs": [
            ("How do you convert Kelvin to Celsius?",
             "Subtract 273.15. 300 K is 26.85 C. To go back, add 273.15 - the degree sizes are identical, only the zero points differ."),
            ("What is absolute zero in Celsius and Fahrenheit?",
             "0 K = -273.15 C = -459.67 F. It is the theoretical floor of temperature: no colder state exists because molecular motion cannot go below zero."),
            ("Why does science use Kelvin instead of Celsius?",
             "Because formulas need a true zero. Gas laws like PV = nRT only work when temperature is proportional to molecular energy - in Celsius, doubling 10 C to 20 C would absurdly claim double the energy."),
            ("Can temperature be negative in Kelvin?",
             "No - there is no temperature below absolute zero. (Physics classes may mention exotic 'negative temperature' systems, but those are stranger than simple coldness and not what a thermometer measures.)"),
        ],
    })

    pages.append({
        "slug": "savings-goal-calculator",
        "title": "Savings Goal Calculator — The Exact Date You'll Hit Your Target",
        "h1": "Savings Goal Calculator",
        "desc": "Enter a savings goal, what you have saved and your monthly deposit — get the exact month and year you'll reach it, with interest and a progress bar. Free, no sign-up.",
        "category": "calculator",
        "keyword": "savings goal calculator",
        "tool": "savings",
        "args": {},
        "intro": [
            "Most savings calculators show a chart and ask you to sign up for a bank account. This one answers the only question that actually motivates saving: \"when will I get there?\" Type your goal, what you already have, and your monthly deposit — the answer is a calendar date, not an abstraction.",
            "Add an optional APY to see what interest contributes — for many goals the interest line is small at first and becomes the fast lane later, which is exactly the part cash savers underestimate. Your inputs are remembered on this device and the share button produces a link that reopens the plan with your numbers filled in, so you can text the plan to an accountability partner.",
        ],
        "howto": [
            "Type your savings goal, what you already have, and your monthly deposit — the target month and year appear instantly.",
            "Optionally add your account's APY to see the interest contribution; the progress bar shows how far you already are.",
            "Tap Share to send the plan as a link — it reopens with your numbers pre-filled, ready for the group chat.",
        ],
        "faqs": [
            ("How long will it take to save my goal?",
             "The big result gives the exact month and year based on your monthly deposit and optional interest rate, computed month by month. Change any input and the date recalculates instantly — shaving the timeline by raising deposits is the fastest experiment you can run."),
            ("Does the calculator include compound interest?",
             "Yes — if you enter an APY, balances grow monthly at that rate, and the detail line splits your timeline into deposits versus interest earned. At 4% APY a $10,000 goal with $500 monthly deposits arrives about a month earlier than under the mattress."),
            ("What monthly deposit do I need to save $10,000 in a year?",
             "About $815 a month without interest, or roughly $800 with a 4% APY. Set the goal and adjust the deposit until the date matches your deadline — the recalculation is live."),
            ("Are my numbers stored or uploaded?",
             "No. Everything runs in your browser; the inputs are kept only in your own device's local storage so the page remembers them next visit, and nothing is ever sent to a server."),
        ],
    })

    pages.append({
        "slug": "compound-interest-calculator",
        "title": "Compound Interest Calculator — Future Value With Yearly Breakdown",
        "h1": "Compound Interest Calculator",
        "desc": "See what your money grows to with monthly compounding — starting amount, optional monthly contributions, a yearly balance table and the rule-of-72 doubling time. Free, instant, no sign-up.",
        "category": "calculator",
        "keyword": "compound interest calculator",
        "tool": "compound",
        "args": {},
        "intro": [
            "Compound interest is interest earning interest: every month your balance grows, and the growth itself starts growing. Enter a starting amount, an optional monthly contribution, a rate and a time horizon — you get the future value plus a year-by-year table that shows exactly when compounding starts doing the heavy lifting.",
            "The detail line also applies the rule of 72 — the classic mental math that divides 72 by your rate to estimate the doubling time. At 7%, money doubles roughly every decade; the yearly table lets you watch that doubling happen. Pair this with the savings goal calculator when you have a target date instead of a horizon.",
        ],
        "howto": [
            "Enter your starting amount, annual rate and time in years — the future value updates as you type.",
            "Add an optional monthly contribution to model regular investing; the table breaks the growth down year by year.",
            "Share the projection with one tap — the link carries your inputs so the recipient sees the same numbers.",
        ],
        "faqs": [
            ("How is compound interest calculated monthly?",
             "Each month the balance grows by rate/12, then contributions are added — the same order banks use. Over a year that lands within a fraction of a percent of the true annual-compounding figure, and it matches how savings accounts and index plans actually post interest."),
            ("What is the rule of 72?",
             "Divide 72 by your annual rate to estimate how many years it takes money to double: 72 / 7 ≈ 10 years at 7%, 72 / 4 = 18 years at 4%. The calculator applies it for you and the yearly table shows the real curve behind the shortcut."),
            ("How much is $5,000 at 7% for 10 years?",
             "About $10,040 left alone — the classic doubling. Add $200 monthly and the same decade grows to roughly $44,700, because contributions feed the compounding engine every month. Try it above and check the year-by-year table."),
            ("Is this calculator free and private?",
             "Completely free with no sign-up, and the math runs entirely in your browser. Inputs are remembered locally on your device only — nothing is transmitted or stored on a server."),
        ],
    })

    pages.append({
        "slug": "double-discount-calculator",
        "title": "Double Discount Calculator — What 30% + 20% Off Is Really Worth",
        "h1": "Double Discount Calculator",
        "desc": "Two discounts in a row? Enter both and get the true combined percentage, the final price, and a verdict against the flat single-discount deal. Instant, free, no sign-up.",
        "category": "calculator",
        "keyword": "double discount calculator",
        "tool": "doubledisc",
        "args": {},
        "intro": [
            "\"30% off, then an extra 20% at checkout\" is not 50% off — it is 44%, because the second discount applies to the already-reduced price. Retailers know most shoppers add the numbers, which is exactly why stacked discounts look juicier than they are. This calculator applies the discounts in order, shows the true combined percentage, and prices the deal honestly.",
            "The flat-alternative field answers the question deal hunters actually face: is \"30% + extra 20%\" better than the competitor's flat 45%? Enter both offers and the verdict line tells you which one wins and by how many dollars — the math most coupon threads argue about for pages, settled in one glance.",
        ],
        "howto": [
            "Enter the original price and the two stacked discounts — the true combined percentage and final price appear instantly.",
            "Type the flat single discount you're comparing against to get the verdict: stacked wins, flat wins, or identical.",
            "Share the result with one tap — the link carries your numbers so the group chat sees the same math.",
        ],
        "faqs": [
            ("What is 30% off then 20% off combined?",
             "44% off, not 50%. The second discount multiplies what remains: 0.70 × 0.80 = 0.56, so you pay 56% of the original price. The calculator shows this multiplication chain step by step so the number is never a guess."),
            ("Why isn't adding two discounts correct?",
             "Because percentages apply to different bases. The 20% comes off the post-30% price, not the original — each extra discount is worth less than the last. A 30%+20% stack equals a flat 44%; the same stack advertised as \"50% off\" overstates it by 6 points."),
            ("Is a stacked discount ever better than one big discount?",
             "Yes — 30% + 20% (true 44%) beats a flat 40%. But 30% + 10% (true 37%) loses to a flat 40%. The comparison depends entirely on the numbers, which is why the verdict field exists: enter both offers and it names the winner in dollars."),
            ("Does this work for three or more discounts?",
             "Keep multiplying: each discount leaves (100% − discount) of the price, so chain them — 0.9 × 0.8 × 0.7 for a 10%+20%+30% stack (true 49.6%). For the common two-discount case this page does the whole chain, the comparison and the share link for you."),
        ],
    })

    pages.append({
        "slug": "simple-interest-calculator",
        "title": "Simple Interest Calculator — SI = P×r×t With Compound Comparison",
        "h1": "Simple Interest Calculator",
        "desc": "Calculate simple interest instantly: interest earned, monthly interest, total at maturity — plus what the same money would earn compounded monthly. Free, no sign-up.",
        "category": "calculator",
        "keyword": "simple interest calculator",
        "tool": "simpleint",
        "args": {},
        "intro": [
            "Simple interest is the flat-rent version of money growth: interest = principal × rate × time, always computed on the original principal, never on accumulated interest. It is how most car loans, short-term notes and textbook problems work — and the formula fits on one line, which is exactly why it belongs in every financial toolkit.",
            "The third stat answers the question every learner eventually asks: \"what would compounding have done instead?\" The calculator runs the same principal at the same rate compounded monthly and shows the difference in dollars. When the gap matters, head to the compound interest calculator; when you have a target date instead of a fixed term, the savings goal calculator works backwards from it.",
        ],
        "howto": [
            "Enter the principal, annual rate and time in years (decimals fine for months, e.g. 0.5 for six months).",
            "Read the interest earned, the per-month figure, and the total at maturity — all update live as you type.",
            "Compare the compounded-monthly stat to see what the same principal earns under compound growth.",
        ],
        "faqs": [
            ("What is the formula for simple interest?",
             "SI = P × r × t: principal times annual rate times time in years. $5,000 at 6% for 3 years = 5,000 × 0.06 × 3 = $900 interest, $5,900 total at maturity. The calculator applies the formula exactly and shows the work."),
            ("How is simple interest different from compound interest?",
             "Simple interest always computes on the original principal, so growth is linear — the same dollars of interest every year. Compound interest computes on the running balance, so growth accelerates. The stat row shows both for your numbers so the difference is concrete, not theoretical."),
            ("When is simple interest used in real life?",
             "Auto loans and many personal loans amortize on simple interest, bonds pay fixed coupons on face value, and short-term notes between 30 days and 5 years often specify it. It is also the standard model in school math and finance exams."),
            ("Does partial-year time work?",
             "Yes — time is in years and accepts decimals: 0.5 for half a year, 1.75 for 21 months. Interest scales proportionally, and the per-month stat divides the total interest evenly across the term."),
        ],
    })

    pages.append({
        "slug": "gpa-calculator",
        "title": "GPA Calculator — Credit-Weighted 4.0 Scale, Semester or Cumulative",
        "h1": "GPA Calculator",
        "desc": "Enter courses, credits and letter grades — get your semester GPA on the 4.0 scale, or fold in prior credits for your cumulative GPA. Instant, private, no sign-up.",
        "category": "calculator",
        "keyword": "gpa calculator",
        "tool": "gpa",
        "args": {},
        "intro": [
            "GPA is a credit-weighted average, not a plain average of grades — a 4-credit A outweighs a 3-credit B+, and that weighting is where most hand calculations go wrong. Enter each course with its credit hours and letter grade; the calculator applies the standard 4.0 scale (A=4.0, A−=3.7, B+=3.3, and so on) and does the weighting for you.",
            "Added your prior cumulative GPA and graded credits below? The headline result switches to your cumulative GPA — the number scholarships, internships and grad schools actually ask for. Everything runs in your browser: courses are remembered on this device between visits and never sent anywhere.",
        ],
        "howto": [
            "Fill in credit hours and a letter grade for each course — course names are optional and blank rows are ignored.",
            "Read the semester GPA in the big result; add prior GPA and prior credits to switch it to your cumulative GPA.",
            "Share the result with one tap — a clean summary text, with no grades attached unless you add them yourself.",
        ],
        "faqs": [
            ("How is GPA calculated on a 4.0 scale?",
             "Multiply each course's grade points (A=4.0, A−=3.7, B+=3.3, B=3.0, B−=2.7, C+=2.3, C=2.0, C−=1.7, D+=1.3, D=1.0, F=0) by its credit hours, add them up, and divide by total credits. The calculator runs that weighting live as you type."),
            ("How do I calculate my cumulative GPA?",
             "Fold your history in: enter your prior cumulative GPA and the graded credits it covered in the two optional fields. The result becomes (this semester's points + prior points) ÷ (this semester's credits + prior credits) — the same formula registrar offices use."),
            ("Do Pass/Fail or withdrawn courses count?",
             "No — P/F, W and incomplete courses carry no grade points, so leave those rows blank and only count courses with a letter grade. The credit total shown reflects exactly what you include."),
            ("Is a 3.5 GPA good?",
             "On the 4.0 scale, 3.5 is an A− average — above the typical cum laude line (often 3.5-3.6) and competitive for most internships and graduate programs. Context matters: the cumulative fields let you track how this semester moves your overall number."),
        ],
    })

    pages.append({
        "slug": "sleep-cycle-calculator",
        "title": "Sleep Cycle Calculator — Best Wake-Up Times & Bedtimes by 90-Min Cycles",
        "h1": "Sleep Cycle Calculator",
        "desc": "Waking mid-cycle is why mornings feel brutal. See the best wake-up times if you sleep now — or the bedtime that gets you up on time — in 90-minute sleep cycles. Free, no sign-up.",
        "category": "calculator",
        "keyword": "sleep cycle calculator",
        "tool": "sleepcycle",
        "args": {},
        "intro": [
            "Sleep moves in roughly 90-minute cycles, and the groggiest mornings come from an alarm landing mid-cycle rather than at its end. This planner works in both directions: sleep right now and it lists the four best wake-up windows over the next nine hours; entering a target wake-up time lists the four bedtimes that line up with a cycle boundary.",
            "Fifteen minutes of fall-asleep time is built in, because \"in bed at 11:00\" and \"asleep at 11:15\" are different plans. Six cycles (about 9 hours) is the generous pick, five (7.5 hours) suits most adults, and three cycles (4.5 hours) is the short-night floor — the times update live, are remembered on this device, and the share button packages your plan for whoever needs to be up with you.",
        ],
        "howto": [
            "Choose \"sleep now\" to see wake-up times from 6 down to 3 cycles, each with its hours of sleep.",
            "Or switch to \"bedtime\" mode and enter the time you must wake up — the four cycle-aligned bedtimes appear instantly.",
            "Share the plan with one tap; the link reopens the same mode and time on the other person's phone.",
        ],
        "faqs": [
            ("What time should I wake up if I sleep now?",
             "Take the current time, add about 15 minutes to fall asleep, then add 90-minute cycles: the planner shows wake-ups at roughly 9, 7.5, 6 and 4.5 hours out. Waking at any of those boundaries — especially 5-6 cycles — feels noticeably lighter than waking mid-cycle."),
            ("How many sleep cycles do you need?",
             "Most adults do best on 5-6 cycles (7.5-9 hours); 4 cycles (6 hours) works occasionally, and 3 cycles (4.5 hours) is the short-night minimum, not a routine. The planner lists all four so you can pick honestly for tonight."),
            ("Why add 15 minutes to fall asleep?",
             "Sleep latency — the average time it takes to drift off once lights are out. Bedtimes here are lights-out times, so the planner subtracts latency from your target wake-up to keep the cycle math honest. If you typically fall asleep faster or slower, mentally shift the results the same way."),
            ("Does the 90-minute cycle rule actually work?",
             "It is a useful average, not a biological law — individual cycles run 80-100 minutes and vary night to night. Used as a planning heuristic (which is all this calculator claims), aligning alarms with cycle boundaries reliably reduces grogginess from sleep inertia."),
        ],
    })

    pages.append({
        "slug": "final-grade-calculator",
        "title": "Final Grade Calculator — What Do I Need on My Final?",
        "h1": "Final Grade Calculator",
        "desc": "Enter your current grade and the final's weight — see exactly what score you need for your target course grade, plus where 100%, 80% and 60% outcomes land. Free, instant, no sign-up.",
        "category": "calculator",
        "keyword": "final grade calculator",
        "tool": "finalgrade",
        "args": {},
        "intro": [
            "\"What do I need on the final to get an 80?\" is the most searched question of exam season, and the answer is one weighted-average formula away: needed = (target − current × (1 − final weight)) ÷ final weight. Enter three numbers — current grade, the final's worth, your target — and the big result is the exact score to aim for.",
            "The scenario row answers the better question: what actually happens. It shows the course grade you'd land with 100%, 80% or 60% on the final, so you can see whether your target is safe, stretchy or gone — and decide where the study hours go. If the needed score is above 100%, the result says so honestly and shows the ceiling instead; if it's below 0%, your target is already locked even with a zero. Pair it with the GPA calculator to see what the outcome does to your semester.",
        ],
        "howto": [
            "Enter your current grade, the final exam's weight (from the syllabus), and the course grade you're aiming for.",
            "Read the required final score in the big result — the formula line shows the exact calculation.",
            "Check the scenario row for 100%/80%/60% outcomes to decide how much this final is really worth to your week.",
        ],
        "faqs": [
            ("What do I need on the final to get an 80?",
             "With a 78 average and a 30% final: (80 − 78 × 0.70) ÷ 0.30 = 84.7%, so an 85 rounds to safe. The formula shifts fast with the final's weight — a 40% final needs only 82, a 20% final needs 96 — which is why the weight field matters more than intuition suggests."),
            ("How do I calculate my weighted final grade?",
             "Course grade = current × (1 − final weight) + final score × final weight. The three scenario stats apply that formula at 100%, 80% and 60% so you can see the whole outcome range without retyping anything."),
            ("What if the needed score is over 100%?",
             "Then the target is mathematically out of reach with your current average — the calculator shows the maximum course grade instead (a perfect final score). Lower the target one letter grade and the required score usually drops into reach; the recalculation is instant."),
            ("Does this work for points-based grading?",
             "Yes — convert to percentages first: divide your earned points by possible points so far, and use the final's share of total points as its weight. After that the math is identical."),
        ],
    })

    pages.append({
        "slug": "water-intake-calculator",
        "title": "Water Intake Calculator — Your Daily Hydration Target in Liters",
        "h1": "Water Intake Calculator",
        "desc": "How much water should you drink a day? Get a personalized daily target from your body weight, today's exercise and the heat — shown in liters, bottles and cups. Free, no sign-up.",
        "category": "calculator",
        "keyword": "water intake calculator",
        "tool": "water",
        "args": {},
        "intro": [
            "Generic \"8 glasses a day\" advice ignores the two things that change everything: body size and the day you're actually having. This calculator starts from ~33 ml per kilo of body weight, then adds roughly 400 ml per 30 minutes of exercise and half a liter for hot weather — the same adjustments sports-nutrition guidelines use, minus the guesswork.",
            "The result lands in the units that matter at the fridge: liters, 500 ml bottles and 8 oz cups, so \"2.9 liters\" becomes \"6 bottles\" and an actual plan. The note line includes a realistic spread-it-through-the-day schedule, because hitting a target is about distribution, not chugging. Bookmark it — the page remembers your weight and adjusts in one tap when the workout or the heat changes tomorrow.",
        ],
        "howto": [
            "Enter your weight and today's exercise minutes — the daily target updates instantly in liters.",
            "Toggle hot weather if it's over 30°C / 86°F, then read the same target in bottles and cups.",
            "Follow the distribution note across the day, and share the target with one tap on workout days.",
        ],
        "faqs": [
            ("How much water should I drink a day?",
             "A common baseline is 30-35 ml per kilogram of body weight — roughly 2.3 L for a 70 kg adult — before exercise and heat. This calculator uses 33 ml/kg as the baseline and then adds for today's activity and temperature, which is why the number changes day to day rather than staying fixed."),
            ("Does coffee and food count toward water intake?",
             "Yes. All beverages count (caffeinated drinks are mildly diuretic but still net-positive), and food — especially fruit, vegetables and soup — typically supplies 20% of daily fluid. Aim most of the remaining 80% at water rather than sugary drinks."),
            ("Can I drink too much water?",
             "Rarely, but it is real: drinking multiple liters per hour can dilute blood sodium (hyponatremia), seen mostly in endurance events. Spreading intake through the day as the schedule suggests keeps you far from that zone — thirst plus pale-yellow urine is a good practical compass."),
            ("How much extra water should I drink when exercising?",
             "Roughly 400 ml (13 oz) per half hour of activity, more in heat or for heavy sweating — the calculator adds this automatically from your exercise minutes. For sessions beyond 90 minutes, an electrolyte drink replaces the sodium that plain water alone doesn't."),
        ],
    })

    pages.append({
        "slug": "tdee-calculator",
        "title": "TDEE Calculator — Daily Calorie Needs (BMR + Activity)",
        "h1": "TDEE & Calorie Calculator",
        "desc": "Find your total daily energy expenditure: BMR from the Mifflin-St Jeor equation times your real activity level — plus steady-loss and lean-gain reference lines. Free, no sign-up.",
        "category": "calculator",
        "keyword": "tdee calculator",
        "tool": "tdee",
        "args": {},
        "intro": [
            "TDEE — total daily energy expenditure — is the number of calories you burn in 24 hours including everything from digestion to workouts. It is the anchor every sensible plan hangs from: eat below it to lose weight, above it to gain. This calculator computes your BMR with the Mifflin-St Jeor equation (the formula most dietitians start from), then applies an honest activity multiplier you pick from five plain-language levels.",
            "Two reference lines sit next to the maintenance number: a 500 kcal deficit for steady loss (about half a kilo a week) and a +300 kcal surplus for lean gain, because eating wildly past your TDEE mostly buys fat, not muscle. Your inputs are remembered on this device — recheck after your activity level changes and the whole picture updates in one tap.",
        ],
        "howto": [
            "Enter sex, age, height and weight — your BMR appears immediately in the stats row.",
            "Pick the activity level that matches your real week, not your aspirational one — the big number is your maintenance calories.",
            "Use the −500 and +300 reference lines for loss or lean-gain plans, and share the estimate with one tap.",
        ],
        "faqs": [
            ("How is TDEE calculated?",
             "BMR × activity multiplier. BMR comes from the Mifflin-St Jeor equation (10 × weight kg + 6.25 × height cm − 5 × age + 5 for men, −161 for women); the multiplier runs from 1.2 for sedentary to 1.9 for athletes. The result is an estimate — treat it as a starting point and adjust against real weight trends."),
            ("Should I eat below my TDEE to lose weight?",
             "A deficit is what produces fat loss, and 500 kcal below maintenance is the standard steady pace (≈0.5 kg/week). Going far below BMR is where diets backfire — energy, training and adherence all crumble. The loss line shows the moderate starting point, not a hard limit."),
            ("Why is my TDEE different from my friend's?",
             "Body size, muscle mass, age and sex move BMR substantially — a heavier, younger, taller body burns more at rest. Two people with identical lifestyles can differ by 400+ kcal a day, which is exactly why shared diet numbers fail and personal calculators work."),
            ("How accurate is the Mifflin-St Jeor equation?",
             "It lands within about 10% of measured resting metabolism for most adults and outperforms older equations in validation studies. Use the estimate to set a starting intake, then trust the scale trend over two weeks — if weight isn't moving as predicted, adjust intake by 100-200 kcal."),
        ],
    })

    pages.append({
        "slug": "tip-split-calculator",
        "title": "Tip Split Calculator — Per-Person Share With Round-Up Option",
        "h1": "Tip Split Calculator",
        "desc": "Split the dinner bill fairly: bill + tip ÷ people, each person's exact share, and a round-up option that fattens the tip instead of shortchanging the server. Free, instant.",
        "category": "calculator",
        "keyword": "tip split calculator",
        "tool": "tipsplit",
        "args": {},
        "intro": [
            "End-of-meal math is the worst kind: done on a phone, under peer pressure, twice. This calculator takes the bill, your tip percentage and the headcount, then shows each person's exact share, the grand total, and — the part everyone actually wants — a round-up figure where each person throws in to the next whole dollar and the surplus becomes a better tip rather than an argument.",
            "It complements the plain tip calculator for the \"one check, many wallets\" situation: the note line spells out what the round-up collection totals and how much extra the server receives, so the table can decide between exact fairness and clean cash. Every input is remembered and the share button packages the split for the group chat before the dessert menus arrive.",
        ],
        "howto": [
            "Enter the bill total, tip percentage and number of people — each person's share appears instantly.",
            "Compare the round-up figure: everyone pays to the next whole dollar and the difference tops up the tip.",
            "Tap Share to send the per-person amount to the group chat with the math attached.",
        ],
        "faqs": [
            ("How do you split a bill with tip?",
             "Add the tip to the bill first, then divide by people: (bill × (1 + tip%)) ÷ heads. For a $184.50 bill with an 18% tip across 4 people: grand total $217.71, so $54.43 each. The calculator shows both the exact figure and the round-up version."),
            ("How much should I tip for dinner?",
             "US table service convention is 18-20% for good service, 15% for adequate, 20%+ for exceptional; the tip applies to the pre-discount bill. The percentage field accepts any value so the table can decide collectively — the math stays honest either way."),
            ("Is it fair to split the bill equally?",
             "Equal splits are fair when orders are comparable; they quietly break when one person's steak funds another's side salad. This calculator gives the equal-split answer (what most tables do) with clean round-up cash — for order-by-order fairness, itemized apps are the alternative."),
            ("What does the round-up option actually do?",
             "Each person rounds their share up to the next whole dollar. The note line totals the collection and shows the surplus — for the example above, four people paying $55 collect $220 on a $217.71 bill, handing the server an effective 19.3% tip without anyone doing mental math at the table."),
        ],
    })

    pages.append({
        "slug": "heat-index-calculator",
        "title": "Heat Index Calculator — What It Really Feels Like (NOAA Formula)",
        "h1": "Heat Index Calculator",
        "desc": "Enter temperature and humidity to get the heat index — what your body actually feels in the shade — with the official NOAA risk bands for caution, danger and heat stroke. Free, instant.",
        "category": "calculator",
        "keyword": "heat index calculator",
        "tool": "heatindex",
        "args": {},
        "intro": [
            "Humidity is why 95°F in Phoenix feels survivable and 95°F in Houston feels hostile: sweat evaporates slower in moist air, so your body's cooling system underperforms exactly when it matters. The heat index puts one number on that — and this calculator runs the full NOAA Rothfusz regression, the same formula the National Weather Service publishes, not the rough doubling shortcuts.",
            "The risk band under the result translates the number into what to actually do: caution means hydrate and pace yourself, extreme caution means cut midday effort, danger and extreme danger mean heat illness becomes likely without intervention. The delta stat shows how many degrees humidity added — the number most people find genuinely surprising. Note the figure is for shade with light wind; full sun can push the effective temperature up another 15°F.",
        ],
        "howto": [
            "Pick °F or °C, then enter the air temperature and relative humidity from any weather report.",
            "Read the feels-like heat index in the big result, with the official NOAA risk band spelled out below it.",
            "Check the delta to see what humidity added, and share the figure in one tap for the group chat.",
        ],
        "faqs": [
            ("What is the heat index?",
             "The temperature a body perceives when humidity is combined with air temperature, because reduced sweat evaporation impairs cooling. 95°F at 60% humidity computes to a heat index of about 114°F — the air is 95, but your cooling system is working as if it were 114."),
            ("How is the heat index calculated?",
             "This page uses the NOAA Rothfusz regression — a multi-term polynomial of temperature and relative humidity — plus the official corrections for very dry (RH<13%) and very humid (RH>85%) conditions. It applies only above 80°F (27°C); below that the air temperature itself is the standard feels-like figure."),
            ("What heat index is dangerous?",
             "NOAA bands: 80-90°F caution (fatigue with prolonged exposure), 90-102°F extreme caution (heat cramps and heat stroke possible), 103-124°F danger (likely without precautions), 125°F+ extreme danger (heat stroke imminent). The calculator prints your band with the result."),
            ("Why does the heat index assume shade?",
             "The NOAA formula models a shaded, lightly-winded person so forecasts are comparable across locations. Direct sun adds up to 15°F (8°C) to the effective load — treat the shaded figure as the floor, not the worst case, and plan outdoor effort accordingly."),
        ],
    })

    pages.append({
        "slug": "bmi-calculator",
        "title": "BMI Calculator — Metric & Imperial With WHO Categories",
        "h1": "BMI Calculator",
        "desc": "Calculate your Body Mass Index in metric or imperial units — with the WHO category and the healthy weight range for your height. Free, private, no sign-up.",
        "category": "calculator",
        "keyword": "bmi calculator",
        "tool": "bmi",
        "args": {},
        "intro": [
            "BMI is one division — weight over height squared — and yet it is the first number most doctors, insurers and sports programs ask for. This calculator handles both metric and imperial input, prints your BMI with the official WHO category, and converts the healthy range (18.5-24.9) back into an actual weight window for your height, which is the part that turns a score into a target.",
            "The honest framing matters: BMI is a population screening tool, not a body composition scan. Muscle-heavy athletes read overweight; older adults with low muscle read healthy. Use the number as a checkpoint — if it sits outside the range and you don't know why, that's the moment to look at waist measurement or body fat rather than panic. The page remembers your inputs on this device for quick rechecks.",
        ],
        "howto": [
            "Choose metric (cm, kg) or imperial (in, lb) — the placeholders follow your choice.",
            "Enter height and weight: BMI appears instantly with its WHO category and your healthy weight window.",
            "Share the number in one tap, or bookmark the page — inputs are remembered for next visit.",
        ],
        "faqs": [
            ("How is BMI calculated?",
             "BMI = weight (kg) ÷ height (m)². In imperial units, BMI = 703 × pounds ÷ inches². A 175 cm, 70 kg person lands at 22.9 — mid-range healthy. The calculator applies the formula exactly and shows both the score and its category."),
            ("What is a healthy BMI range?",
             "The WHO defines 18.5-24.9 as healthy, below 18.5 underweight, 25-29.9 overweight and 30+ obese (classes I-III at 30/35/40). The healthy-weight stat converts that range into the actual weight window for your height — more actionable than the score alone."),
            ("Is BMI accurate for athletes and older adults?",
             "Not by itself. BMI cannot tell muscle from fat, so muscular athletes often score overweight despite low body fat, and adults losing muscle with age can score healthy while carrying risk. Treat BMI as the cheap first screen; waist circumference or a body-fat measurement refines it."),
            ("Does BMI differ for men and women?",
             "The formula and WHO cut-offs are identical for adult men and women — that is both its simplicity and its weakness. Body composition differs meaningfully by sex and age, which is why the healthy range here is the standard one and individual judgment (or a clinician) fills the gap."),
        ],
    })

    pages.append({
        "slug": "wind-chill-calculator",
        "title": "Wind Chill Calculator — How Cold It Really Feels (NOAA Formula)",
        "h1": "Wind Chill Calculator",
        "desc": "Enter temperature and wind speed to get the wind chill — how cold exposed skin actually feels — plus official frostbite time estimates. Free, instant, °F/mph or °C/km/h.",
        "category": "calculator",
        "keyword": "wind chill calculator",
        "tool": "windchill",
        "args": {},
        "intro": [
            "Wind doesn't lower the air temperature — it strips away the thin layer of warm air your body heats around itself, so exposed skin loses heat faster and the cold bites deeper. Wind chill is the temperature calm air would have to be for that same rate of heat loss, and this calculator applies the official NOAA formula used in every winter weather bulletin.",
            "The frostbite stat is the one worth knowing before a winter run or a scraped windshield: at a wind chill of −19°F exposed skin can freeze in 30 minutes, at −32°F in 10, and at −48°F in 5. The figure assumes night shade per NOAA — sunshine softens it a little, wet skin and clothing harden it a lot. It is the winter twin of the heat index: one formula, the whole story of what the weather will do to you.",
        ],
        "howto": [
            "Pick your units (°F/mph or °C/km/h), then enter the air temperature and wind speed from any forecast.",
            "Read the feels-like wind chill in the big result, with the frostbite time estimate beside it.",
            "Share the figure in one tap — useful before commutes, dog walks and winter training sessions.",
        ],
        "faqs": [
            ("How is wind chill calculated?",
             "NOAA's formula: 35.74 + 0.6215T − 35.75V^0.16 + 0.4275T·V^0.16, with T in °F and V in mph — a model of heat loss from a bare face in shade at night. It is defined for 50°F (10°C) and below with wind above 3 mph; outside that range, air temperature is the standard figure."),
            ("What wind chill causes frostbite?",
             "Roughly −19°F wind chill freezes exposed skin in 30 minutes, −32°F in 10 minutes, and −48°F in 5. The calculator shows the estimate for your exact combination — cover extremities well before those thresholds, since fingers, toes and ears freeze first."),
            ("Can wind chill be lower than the actual temperature?",
             "It always is, by definition — wind chill represents an equivalent temperature for heat loss, not the air itself. At 20°F with a 20 mph wind the calculator gives about 4°F: the air stays 20°F, your skin loses heat as if it were 4°F."),
            ("Why does calm air feel warmer than the wind chill number?",
             "Below 3 mph the formula stops applying — your body's warm boundary layer stays mostly intact, and the air temperature is the honest figure. Indoors or behind a windbreak, dress for the thermometer; outside, dress for the wind chill."),
        ],
    })

    pages.append({
        "slug": "pace-calculator",
        "title": "Running Pace Calculator — Pace per KM/Mile + Race Finish Times",
        "h1": "Running Pace Calculator",
        "desc": "Enter a distance and finish time to get your running pace per kilometer and per mile, your speed, and predicted 5K, 10K, half and marathon times at the same effort. Free, no sign-up.",
        "category": "calculator",
        "keyword": "running pace calculator",
        "tool": "pace",
        "args": {},
        "intro": [
            "Pace is the runner's shared language — \"5-minute Ks\" says more than any speed number. Enter any distance and finish time (h:mm:ss, the format GPS watches report) and this calculator returns pace per kilometer and per mile in that same clock format, plus your speed in km/h and mph for treadmill cross-checks.",
            "The prediction row is the training payoff: it scales your current pace across the classic race distances — 5K, 10K, half and full marathon — so a single hard 10K instantly becomes a realistic marathon target conversation. It assumes the same pace holds (not a fatigue-adjusted projection, which elite tools model), making it most accurate from threshold work up to about the half marathon. Logs pair well with the sleep cycle calculator, because recovery is the other half of pace.",
        ],
        "howto": [
            "Choose kilometers or miles, enter your distance and finish time — pace per km and per mile appear instantly.",
            "Read the predicted finish times for 5K, 10K, half and marathon at that same pace.",
            "Share the result with one tap — the link carries your run so training buddies see identical numbers.",
        ],
        "faqs": [
            ("How do I calculate my running pace?",
             "Divide your finish time by the distance: a 52:30 10K is 3150 seconds ÷ 10 km = 5:15 per kilometer (about 8:26 per mile). The calculator does the division in both units at once and works for any distance you enter, from a track mile to an ultramarathon."),
            ("What is a good running pace?",
             "Recreational 5K paces commonly fall between 5:00 and 7:30 per kilometer (8:00-12:00 per mile), while sub-20-minute 5K racing means holding 4:00/km or faster. \"Good\" is trajectory, not a table — compare against your own last month, and the prediction row shows what your current pace already buys at longer distances."),
            ("How accurate are race predictions from pace?",
             "Same-pace scaling is solid up to about the half marathon; beyond that, fatigue, fueling and heat push real times slower than linear math. Treat the marathon row as a fit-runner's floor, then adjust for course, weather and long-run experience."),
            ("What pace should I train at?",
             "Most weekly mileage should be conversational — typically 60-90 seconds per kilometer slower than your 5K race pace — with one or two quality sessions faster. Enter a recent race above, then run easy days about 1:30/km slower than the pace shown."),
        ],
    })

    pages.append({
        "slug": "macro-calculator",
        "title": "Macro Calculator — Protein, Carb & Fat Grams From Your Calories",
        "h1": "Macro Calculator",
        "desc": "Turn a daily calorie target into grams of protein, carbs and fat — with four goal presets and full custom control. Free, instant, no sign-up.",
        "category": "calculator",
        "keyword": "macro calculator",
        "tool": "macros",
        "args": {},
        "intro": [
            "Calories decide weight change; macros decide where those calories take your body. This calculator converts any daily calorie target into grams of protein, carbohydrate and fat using the standard energy factors — 4 kcal per gram of protein or carbs, 9 per gram of fat — so a 2,400 kcal day at 30/40/30 becomes 180 g protein, 240 g carbs and 80 g fat you can actually put on a plate.",
            "Four goal presets cover the common splits (balanced, high-protein, endurance, low-carb), and switching to Custom unlocks the three percentage fields directly — the note line warns when a split doesn't sum to 100. Feed it your maintenance number from the TDEE calculator and the pair gives you a complete, no-app subscription nutrition plan; both pages remember your numbers locally for daily rechecks.",
        ],
        "howto": [
            "Enter your daily calorie target — or take it from the TDEE calculator's loss or gain line.",
            "Pick a goal preset or choose Custom and set your own protein/carb/fat percentages.",
            "Read the gram targets, then share them with one tap for the training group or coach.",
        ],
        "faqs": [
            ("How do I calculate macros from calories?",
             "Multiply calories by each macro's percentage share, then divide by its energy density: protein and carbs carry 4 kcal per gram, fat carries 9. At 2,400 kcal with a 30/40/30 split that is 2400×0.30÷4 = 180 g protein, 240 g carbs and 80 g fat — the calculator runs it live."),
            ("What macro split is best for fat loss?",
             "Protein matters most: 30-40% preserves muscle in a deficit. A 35/30/35 or 40/35/25 split suits most cuts, with carbs timed around training. Fat below about 20% tends to backfire on hormones and adherence — the presets all stay above that floor."),
            ("How many grams of protein do I need per day?",
             "Evidence for active people clusters around 1.6-2.2 g per kilogram of body weight. Rather than a flat rule, set protein to 30-40% of calories at a deficit and check the gram output against your weight — both numbers should roughly agree."),
            ("Do the percentages need to add up to 100?",
             "Yes for a mathematically exact plan — the note line flags any drift. The gram outputs are proportional regardless, so a 95% split simply under-allocates 5% of your calories; nudge one field until the note clears."),
        ],
    })

    pages.append({
        "slug": "electricity-cost-calculator",
        "title": "Electricity Cost Calculator — What Any Appliance Costs to Run",
        "h1": "Electricity Cost Calculator",
        "desc": "Enter an appliance's watts, hours used per day and your rate per kWh — get the daily, monthly and yearly running cost instantly. Free, no sign-up.",
        "category": "calculator",
        "keyword": "electricity cost calculator",
        "tool": "electricity",
        "args": {},
        "intro": [
            "Every appliance has a wattage printed on its label or spec sheet, and your utility bill states a price per kWh — multiply through the hours and you know exactly what anything costs to run. A 1,500 W space heater for 3 hours a day at $0.17/kWh is about $23 a month; a gaming PC for 5 hours is similar. This calculator does that arithmetic for any device, any rate, any country's billing unit.",
            "The yearly figure is where decisions live: that old second fridge, the dehumidifier in the basement, the always-on server — each line item is one entry away from a number you can act on. The note adds the standby-power reality check (1-2 W around the clock for anything left plugged in), and the share button sends the cost to whoever in the house needs convincing.",
        ],
        "howto": [
            "Enter the device's wattage (check the label), hours per day, and your rate per kWh from the bill.",
            "Read the monthly cost in the big result, with daily, yearly and kWh figures alongside.",
            "Share or bookmark — inputs are remembered so you can price out the whole house one device at a time.",
        ],
        "faqs": [
            ("How do I calculate the cost of running an appliance?",
             "Watts × hours ÷ 1000 = kWh; kWh × your rate per kWh = cost. A 1500 W heater for 3 h/day at $0.17/kWh: 1.5 × 3 = 4.5 kWh/day → $0.77/day → about $23/month. The calculator shows each step of the math."),
            ("How do I find my electricity rate?",
             "It's on the utility bill, stated in ¢ or $ per kWh — often several line items (energy, delivery, taxes) that you can sum. European bills quote the same figure in €/kWh; enter it the same way after converting to your local currency."),
            ("How much does it cost to leave something plugged in?",
             "Standby draw is typically 1-2 W around the clock: roughly 9-17 kWh a year, or $1.50-$3 at typical rates — small per device, meaningful across a house full of chargers and set-top boxes. The calculator's yearly line makes each one concrete."),
            ("Do space heaters really cost that much to run?",
             "Yes — resistance heating is the most expensive comfort per kWh. A 1500 W heater at 3 h/day runs $20-25/month at US average rates, which is why the calculator's yearly figure surprises people. Compare against the yearly cost of insulation, a heat pump or simply closing doors."),
        ],
    })

    pages.append({
        "slug": "body-fat-calculator",
        "title": "Body Fat Calculator — US Navy Method (Tape Measurements)",
        "h1": "Body Fat Calculator",
        "desc": "Estimate body fat percentage with the US Navy tape method — just height, neck and waist (plus hip for women), with fat mass, lean mass and fitness category. Free, private.",
        "category": "calculator",
        "keyword": "body fat calculator",
        "tool": "bodyfat",
        "args": {},
        "intro": [
            "The scale can't tell muscle from fat; a tape measure gets surprisingly close. The US Navy developed this circumference formula to field-assess recruits without lab equipment — neck and waist for men, plus hips for women — and validation studies put it within roughly ±3% of DEXA scans for most people. Enter four numbers and you get a body fat percentage, a fitness category, and the fat-versus-lean split of your current weight.",
            "That lean-mass number is the one worth tracking: at a constant body weight, falling body fat means you are recomposing — gaining muscle while losing fat — something the scale alone would hide. Re-measure with the same tape at the same time of day, and the page remembers your measurements locally so the monthly comparison takes thirty seconds.",
        ],
        "howto": [
            "Measure per the method: neck below the larynx, waist at the navel (men) or narrowest point (women), hips at the widest point for women.",
            "Enter height, circumference measurements and your weight — the estimate, category and mass split appear instantly.",
            "Share the estimate in one tap, or bookmark the page — measurements are remembered for your monthly recheck.",
        ],
        "faqs": [
            ("How does the Navy body fat formula work?",
             "It models the body as cylinders and logs: for men, 495 ÷ (1.0324 − 0.19077×log10(waist−neck) + 0.15456×log10(height)) − 450; women add hip circumference to the equation. The log terms capture how fat is distributed — exactly what a scale cannot see."),
            ("What is a healthy body fat percentage?",
             "For men, roughly 14-18% is athletic-fitness range and 18-25% average; for women, 21-25% athletic-fitness and 25-32% average — women carry essential fat the male formula never sees. Below the essential floor is a health risk, not an achievement."),
            ("How accurate is the tape method?",
             "Within about ±3% of DEXA for most body types when measured carefully, which is enough to track trends. Consistency beats precision: same tape tension, same time of day, same hydration state — the direction of change is the signal."),
            ("Why track body fat instead of just weight?",
             "Weight cannot distinguish recomposition from stagnation. Two people at 80 kg can hold 15% or 30% body fat with opposite health profiles — and during a training block, stable weight with falling body fat is the win the scale would misread as failure."),
        ],
    })

    pages.append({
        "slug": "oven-temperature-converter",
        "title": "Oven Temperature Converter — °F, °C and Gas Marks With Reference Table",
        "h1": "Oven Temperature Converter",
        "desc": "Convert any oven setting between Fahrenheit, Celsius and UK gas marks — plus a full reference table from meringues to pizza. Never misread a recipe again. Free, instant.",
        "category": "calculator",
        "keyword": "oven temperature converter",
        "tool": "oven",
        "args": {},
        "intro": [
            "The internet's recipes travel, but ovens don't: American recipes speak Fahrenheit, European ones Celsius, and British vintage cookery writes gas marks. Enter any setting in one system and this converter gives the equivalent in both others — plus the full reference table from 275°F meringue-land to 500°F pizza-blast, so you can sanity-check any recipe at a glance.",
            "The table's fourth column is the practical one: what each temperature is actually used for, from slow-roasting to fast browning. One warning is built into the page: fan (convection) ovens run about 20°C hotter than these conventional settings — subtract 20°C or one gas mark equivalent when the manual says fan-assisted.",
        ],
        "howto": [
            "Pick the unit your recipe uses — °F, °C or gas mark — and type the temperature.",
            "Read the equivalent in both other systems in the big result, with the nearest gas mark named.",
            "Scan the reference table for the typical use at each setting, and share the conversion with one tap.",
        ],
        "faqs": [
            ("What is 350°F in Celsius and gas mark?",
             "350°F is 175°C — gas mark 4, the workhorse of baking (cookies, cakes, most roasting). It is the single most common oven setting in American recipes, which is why it anchors the middle of the reference table."),
            ("How do gas marks convert to Celsius?",
             "Gas mark 1 is about 140°C and each mark adds roughly 13-15°C (250°F + 25°F per mark in Fahrenheit). The converter rounds to the nearest mark because dials are that imprecise anyway — anything within a quarter-mark is the same oven reality."),
            ("Do I need to adjust for a fan oven?",
             "Yes — fan-assisted ovens circulate heat and effectively cook 20°C (25°F) hotter than conventional settings. Reduce the temperature by 20°C (or one gas mark equivalent) or shorten the time; when a recipe says 180°C conventional, run a fan oven at 160°C."),
            ("Why do recipes disagree about temperatures?",
             "Ovens lie: a dial reading 180°C can sit 15°C off true, and hot spots vary by rack. The converter gives you the correct target — after that, an oven thermometer is the cheapest baking upgrade there is, because you calibrate your oven against the number the recipe means."),
        ],
    })

    pages.append({
        "slug": "cgpa-to-percentage",
        "title": "CGPA to Percentage Calculator — 10-Point Scale, Both Directions",
        "h1": "CGPA to Percentage Calculator",
        "desc": "Convert CGPA to percentage (×9.5, the CBSE formula) or percentage back to CGPA — with typical class bands and a certificate caveat. Free, instant, no sign-up.",
        "category": "calculator",
        "keyword": "cgpa to percentage",
        "tool": "cgpa",
        "args": {},
        "intro": [
            "Indian application forms ask for percentages; transcripts report CGPA out of 10. The standard bridge is the CBSE formula — percentage = CGPA × 9.5 — and this converter runs it in both directions: enter your CGPA for the percentage, or your percentage for the CGPA equivalent, with the typical class band (first class, distinction territory) shown alongside so you know how the number reads.",
            "The caveat matters enough to print on the tool itself: some universities use factors from 9.0 to 10.0, and a few issue their own conversion certificates. Treat the ×9.5 result as the widely-accepted default, check your institution's rule before writing it on a form, and use the share button to send the exact conversion to whoever asked for it.",
        ],
        "howto": [
            "Pick the direction — CGPA → percentage, or percentage → CGPA.",
            "Enter your value: 8.6 CGPA becomes 81.7%, and 82% becomes 8.63 CGPA.",
            "Check the class band, then share the result with one tap for application forms.",
        ],
        "faqs": [
            ("How do you convert CGPA to percentage?",
             "Multiply by 9.5 — the official CBSE conversion, so an 8.6 CGPA is 81.7%. The formula exists because CBSE computed the average ratio between marks and CGPA across its datasets and published the factor; most Indian universities accept it as the default bridge."),
            ("How do I convert percentage to CGPA?",
             "Divide by 9.5: 82% ÷ 9.5 ≈ 8.63 CGPA. The second mode of this calculator does the reverse conversion, useful when a form asks for CGPA on a 10-point scale but your marksheet only shows percentages."),
            ("Do all universities use the 9.5 factor?",
             "No — factors range from 9.0 to 10.0 and some institutions publish their own equivalence certificates. The 9.5 multiplier is the safe default for applications that don't specify; when a university states its own formula, theirs wins."),
            ("Is 8.0 CGPA a good score?",
             "8.0 CGPA converts to 76% — comfortably first-class and above the common 75% distinction line at many institutions. For competitive programs the cut-offs run higher, which is why the class band next to the result is worth a glance before you quote the number."),
        ],
    })

    pages.append({
        "slug": "caffeine-calculator",
        "title": "Caffeine Calculator — Daily Total vs the 400 mg Guideline",
        "h1": "Caffeine Calculator",
        "desc": "Count your day's caffeine from coffee, tea, cola and energy drinks — see the total against the 400 mg adult guideline and the last safe cup time before bed. Free, no sign-up.",
        "category": "calculator",
        "keyword": "caffeine calculator",
        "tool": "caffeine",
        "args": {},
        "intro": [
            "Caffeine sneaks up in sums: two filter coffees, an afternoon cola and a pre-workout energy drink land you at 284 mg before anything with a shot count. This calculator lists the nine most common sources with their typical milligrams — pick how many of each you've had and the total appears against the 400 mg daily guideline for healthy adults.",
            "The second stat answers the sleep question: caffeine's half-life is roughly 5-6 hours, so the tool prints a last-safe-cup time for an 11 PM bedtime. The countdown logic pairs naturally with the sleep cycle calculator — and because the page remembers your usual picks, tomorrow's tally is two taps instead of a memory test.",
        ],
        "howto": [
            "Select how many of each drink you've had today — the total updates against the 400 mg guideline.",
            "Check the cutoff stat for the last cup that won't fight your 11 PM bedtime.",
            "Share the tally with one tap, or bookmark it — the page remembers your picks.",
        ],
        "faqs": [
            ("How much caffeine is safe per day?",
             "Up to 400 mg daily is the guideline for healthy adults — about four filter coffees — and single doses stay under 200 mg. Pregnancy, some medications and heart conditions lower the ceiling substantially; the calculator's remaining-total stat assumes the standard 400 mg."),
            ("How long does caffeine stay in your system?",
             "Half-life averages 5-6 hours: 100 mg at 4 PM leaves about 50 mg at 10 PM and 25 mg at 4 AM. That residual is enough to lighten sleep even when you fall asleep normally, which is why the cutoff stat works backwards from bedtime."),
            ("How much caffeine is in a cup of coffee?",
             "A filter or drip cup runs ~95 mg, an espresso shot ~63 mg, instant ~66 mg, black tea ~47 mg, green tea ~28 mg, cola ~34 mg per 330 ml, and a 250 ml energy drink ~80 mg. Actual figures vary by bean, brew and brand — the calculator uses these widely-cited averages."),
            ("Does decaf or matcha count?",
             "Decaf is not zero — about 7 mg per cup, worth counting if you drink several. Matcha and green tea carry meaningful caffeine with a slower ramp from L-theanine; the calculator includes both so tea drinkers get an honest total too."),
        ],
    })

    pages.append({
        "slug": "gst-calculator",
        "title": "GST Calculator — Add or Extract GST at India's Standard Slabs",
        "h1": "GST Calculator",
        "desc": "Add 5/12/18/28% GST to a net price, or extract it from a GST-inclusive price — with CGST/SGST split for intra-state invoices. Free, instant, no sign-up.",
        "category": "calculator",
        "keyword": "gst calculator",
        "tool": "gst",
        "args": {},
        "intro": [
            "Two GST questions cover almost every real situation: \"what will this cost with GST added?\" and \"how much of this GST-inclusive price was tax?\" This calculator handles both — add mode applies the slab to a net price, extract mode backs the tax out of a MRP-style inclusive price — using India's four standard slabs (5, 12, 18, 28%) with one tap each.",
            "The CGST/SGST line is the invoice detail most calculators skip: intra-state sales split the tax equally between Central and State GST, while inter-state bills carry the full amount as IGST. Whether you are checking a restaurant bill, pricing a product or filing a reimbursement, the split is shown in rupees, and the share button packages the whole breakdown for the accounts chat.",
        ],
        "howto": [
            "Enter the price and tap the slab — 5, 12, 18 or 28%.",
            "Choose \"add GST\" for net prices or \"extract GST\" when the price already includes tax.",
            "Read the GST amount, net/gross figures and the CGST/SGST split, then share the breakdown in one tap.",
        ],
        "faqs": [
            ("How do I calculate GST on a price?",
             "GST = net price × rate ÷ 100 — a ₹2,499 item at 18% carries ₹449.82 GST for a gross of ₹2,948.82. For GST-inclusive prices, reverse it: tax = price × rate ÷ (100 + rate), because the sticker price already contains the tax."),
            ("How do I remove GST from a total price?",
             "Divide by (1 + rate/100): a ₹1,180 bill at 18% inclusive has a net of 1,180 ÷ 1.18 = ₹1,000 and ₹180 GST. The extract mode applies exactly this, which is the calculation most people get wrong by simply subtracting 18% of the total."),
            ("What is the difference between CGST, SGST and IGST?",
             "Intra-state sales split the GST equally between Central and State GST (CGST + SGST); inter-state sales levy it once as IGST. The amounts are identical — only the split changes, and the calculator shows both views."),
            ("Which GST slab applies to my item?",
             "India's main slabs are 5% (essentials), 12% and 18% (most goods and services), and 28% (luxury and sin goods). The rate is set per HSN/SAC code rather than by product type alone — when in doubt, the invoice of a comparable product is the fastest reference."),
        ],
    })

    pages.append({
        "slug": "overtime-pay-calculator",
        "title": "Overtime Pay Calculator — Regular + OT Split for Your Week",
        "h1": "Overtime Pay Calculator",
        "desc": "Enter your hourly rate and weekly hours — see regular pay, overtime pay at 1.5× past 40, and the exact dollar value of every OT hour. Free, no sign-up.",
        "category": "calculator",
        "keyword": "overtime pay calculator",
        "tool": "overtime",
        "args": {},
        "intro": [
            "Overtime is where paychecks get quietly wrong: 47 hours at $25/hour is not $1,175 — the 7 extra hours earn time-and-a-half, bringing the week to $1,337.50. Enter your rate and hours and this calculator splits the week into regular and overtime pay using the FLSA baseline (1.5× past 40 in a workweek), with the threshold and multiplier adjustable for state daily-OT rules or contract double time.",
            "The note line translates the math into negotiating terms: how many OT hours you worked, and the exact dollar premium they earned over plain time — the number that makes the case for (or against) that extra shift. Inputs are remembered on this device, so next week is a one-field update, and the share button packages the split for payroll questions.",
        ],
        "howto": [
            "Enter your hourly rate and total hours for the week — regular and OT pay split instantly.",
            "Adjust the OT threshold or multiplier if your state or contract uses different rules.",
            "Share the weekly total with one tap, or bookmark it — your rates are remembered.",
        ],
        "faqs": [
            ("How is overtime pay calculated?",
             "Under the US FLSA: hours past 40 in a workweek earn at least 1.5× your regular rate. At $25/hour working 47 hours: 40 × $25 + 7 × $37.50 = $1,000 + $262.50 = $1,362.50 gross. The calculator shows the regular and OT halves separately."),
            ("Is overtime always 1.5×?",
             "Federal law sets 1.5× as the floor past 40 hours, but some states (California most notably) add daily overtime past 8 hours and double time past 12, and union contracts often negotiate richer terms. Set the threshold and multiplier fields to match whichever rule governs your week."),
            ("Do bonuses count toward the overtime rate?",
             "Non-discretionary bonuses must be folded into the regular rate before computing OT — which raises the 1.5× base. Purely discretionary gifts don't count. Payroll math gets subtle here; this calculator uses your actual hourly rate as the base."),
            ("What if I'm salaried — do I get overtime?",
             "Possibly: the FLSA exempts only salaried employees who also pass a duties test and a salary threshold (updated periodically). Non-exempt salaried staff earn OT like hourly workers. Enter your effective hourly rate (salary ÷ expected hours) to estimate what OT would be worth."),
        ],
    })

    pages.append({
        "slug": "rent-affordability-calculator",
        "title": "Rent Affordability Calculator — What Should You Pay for Rent?",
        "h1": "Rent Affordability Calculator",
        "desc": "Enter your income and monthly debts — get the maximum rent by the 30% rule, adjusted for a 36% debt-to-income ceiling, with what's left for everything else. Free, no sign-up.",
        "category": "calculator",
        "keyword": "rent affordability calculator",
        "tool": "rent",
        "args": {},
        "intro": [
            "The 30% rule — spend no more than 30% of gross income on housing — is the landlord's screen and the budget's oldest guardrail. This calculator applies it instantly, then adds the check that matters when you actually have debts: a 36% debt-to-income ceiling that lowers the honest ceiling by exactly what your car loan, student loan and cards already eat.",
            "The \"left for everything else\" stat is the reality check most rent calculators skip: rent is the largest line, but groceries, transport and savings still have to fit underneath it. Three budget rules are on offer — 25% for aggressive saving, 30% classic, 35% for high-cost cities — and the page remembers your numbers so re-budgeting after a raise takes one field.",
        ],
        "howto": [
            "Enter gross monthly income and any monthly debt payments — the rent ceiling appears instantly.",
            "Pick the budget rule that fits your city and goals; the DTI line shows the lender's view.",
            "Read what's left for the rest of life, then share the budget in one tap.",
        ],
        "faqs": [
            ("How much rent can I afford on my salary?",
             "The classic rule caps rent at 30% of gross monthly income — $4,800 income means a $1,440 ceiling. If you carry debts, lenders count them against a 36% DTI instead, and that line becomes the honest number. The calculator shows both and takes the lower one."),
            ("Is the 30% rule still realistic?",
             "In high-cost metros, 35-40% of gross is increasingly common — which is why the rule selector includes 35%. Treat it as a pressure gauge rather than law: above 30%, the \"left for everything else\" stat tells you exactly how thin the rest of the budget runs."),
            ("Does the 30% rule use gross or net income?",
             "Traditionally gross (before tax), which is also how landlords screen applicants. Budgeting on net pay feels stricter but survives contact with reality better — if your gross-based ceiling feels heavy, run the same rent against take-home and see what remains."),
            ("What counts as monthly debt for the DTI check?",
             "Minimum payments on loans, credit cards, car notes and child support — not utilities, subscriptions or the balance itself. Enter the payment amounts, not the balances, and the DTI ceiling adjusts accordingly."),
        ],
    })

    pages.append({
        "slug": "fuel-cost-calculator",
        "title": "Fuel Cost Calculator — Trip Cost From Distance, MPG & Gas Price",
        "h1": "Fuel Cost Calculator",
        "desc": "Enter trip distance, your car's consumption and local fuel price — get the one-way cost, round trip and per-person split. Works in MPG or L/100km. Free, no sign-up.",
        "category": "calculator",
        "keyword": "fuel cost calculator",
        "tool": "fuelcost",
        "args": {},
        "intro": [
            "Road-trip budgets live or die on the fuel line, and the mental math is always optimistic. This calculator takes distance, your car's real consumption and the pump price, and returns the one-way cost, the round trip, and the per-person split when four riders divide the tank — the three numbers every trip planning conversation actually needs.",
            "Both unit worlds ship in one tool: miles/MPG/dollars-per-gallon for the US, kilometers/liters-per-100km for everyone else — switch and the placeholders follow. The note adds the 10-15% real-world buffer (AC, hills, luggage) that factory figures ignore, and pairs naturally with the speed-distance-time calculator for the arrival side of the plan. Inputs are remembered, and the share button sends the cost split to the group chat.",
        ],
        "howto": [
            "Pick your unit system, then enter distance, consumption and fuel price — the cost updates live.",
            "Read fuel needed, the four-rider split, and the round-trip figure for return planning.",
            "Share the trip cost with one tap — the link carries all three inputs.",
        ],
        "faqs": [
            ("How do I calculate the fuel cost of a trip?",
             "Distance ÷ consumption = fuel needed, × price per unit = cost. A 480-mile trip at 30 MPG with $3.45 gas: 480 ÷ 30 = 16 gallons × $3.45 = $55.20 one-way. The calculator runs it in miles/MPG or km/L-per-100km and doubles it for round trips."),
            ("How do I convert MPG to L/100km?",
             "235.215 ÷ MPG = L/100km (and 235.215 ÷ (L/100km) = MPG). The unit switch converts your inputs' frame automatically — the underlying math adapts so the cost answer is identical either way."),
            ("Should I use my car's rated MPG?",
             "Use your real average from the trip computer if it shows one — rated figures assume gentle highway cruising, and city legs, AC and roof racks commonly push consumption 10-15% higher. The note builds that buffer into the planning advice."),
            ("How do we split fuel cost fairly?",
             "Divide the round-trip cost by occupants — the per-person stat does it for four riders on the one-way figure's basis, and the round-trip line doubles the total for the honest pool. Tolls and wear are separate lines; fuel is just the start of the split conversation."),
        ],
    })

    pages.append({
        "slug": "commission-calculator",
        "title": "Commission Calculator — Base + Rate × Revenue, With Quota Tracking",
        "h1": "Commission Calculator",
        "desc": "Enter base pay, commission rate and revenue — see the total paycheck, quota attainment and how much of your pay is commission. Free, instant, no sign-up.",
        "category": "calculator",
        "keyword": "commission calculator",
        "tool": "commission",
        "args": {},
        "intro": [
            "Commission plans are quoted in percentages but lived in dollars: 8% of $45,000 on top of a $2,000 base is $5,600 — and whether that's a good month depends entirely on where the quota sits. Enter base, rate, revenue and an optional quota; the calculator returns the total, the commission share of pay, and your attainment percentage in one line.",
            "The note line does the part sales reps actually need mid-month: how many dollars of revenue stand between you and quota, and what each additional 10% of revenue is worth at your current rate. Inputs are remembered on this device, so updating after every closed deal takes seconds — and the share button packages the math for the manager conversation.",
        ],
        "howto": [
            "Enter your base pay per period, commission rate and revenue booked — the total updates live.",
            "Add your quota to see attainment percentage and the dollar gap to 100%.",
            "Share the paycheck math with one tap, or bookmark it — your plan numbers are remembered.",
        ],
        "faqs": [
            ("How is commission calculated?",
             "Commission = revenue × rate. A $45,000 month at 8% earns $3,600, which stacks on your base: $2,000 + $3,600 = $5,600 total. The calculator keeps base and commission separate so you always see which half is doing the work."),
            ("How much of my pay should be commission?",
             "Common splits run 50/50 to 60/40 (base/commission) in B2B sales and 30/70 or higher in transactional roles. The commission-share stat shows your actual mix — the number to compare against your plan's target and against what you can stomach in a slow month."),
            ("What does quota attainment mean for pay?",
             "Quota is the revenue floor your plan expects; attainment is revenue ÷ quota. Many plans add accelerators — a higher rate past 100% — so crossing the line can raise the rate on every additional dollar. The attainment stat keeps that checkpoint visible all month."),
            ("Do commissions get taxed differently?",
             "No — commission is ordinary supplemental wage income and is taxed as it's paid, often at flat withholding rates that trues up at filing. The calculator shows gross pay; your actual take-home depends on your withholding elections."),
        ],
    })

    pages.append({
        "slug": "air-fryer-converter",
        "title": "Air Fryer Converter — Oven Recipe to Fryer Temp & Time",
        "h1": "Air Fryer Converter",
        "desc": "Turn any oven recipe into an air fryer setting: about 25°F (15°C) cooler and 20% faster, with a check-early warning and expert tips. Free, instant, no sign-up.",
        "category": "calculator",
        "keyword": "air fryer conversion",
        "tool": "airfryer",
        "args": {},
        "intro": [
            "An air fryer is a compact convection oven, and the internet's recipes were mostly written for big conventional ones. The conversion rule of thumb is reliable: drop the temperature about 25°F (15°C), cut the cooking time to roughly 80%, and start checking early — the concentrated fan heat does its crisping fast in the final minutes.",
            "Enter the recipe's oven temperature and time, and the converter returns the fryer setting plus the minutes you save. The built-in tips cover the three things that actually cause air-fryer failures: crowding the basket, skipping the halfway shake, and trusting the timer over your eyes for the last two minutes. It pairs with the oven temperature converter when the recipe itself is in a foreign unit.",
        ],
        "howto": [
            "Choose °F or °C, then enter the recipe's oven temperature and cooking time.",
            "Read the air fryer setting — lower temperature, ~80% of the time — and the minutes saved.",
            "Share the setting with one tap, or bookmark it — last recipe's numbers are remembered.",
        ],
        "faqs": [
            ("How do I convert oven recipes to an air fryer?",
             "Reduce the temperature by about 25°F (15°C) and the time to roughly 80% of the original. A 400°F, 25-minute oven bake becomes about 375°F for 20 minutes in the fryer — the calculator applies both adjustments and rounds the time sensibly."),
            ("Why does an air fryer cook faster?",
             "It is a small chamber with a powerful fan: hot air reaches every surface constantly, so heat transfer is far more efficient than a big oven's static air. Same physics as convection mode — just concentrated into a basket-sized volume."),
            ("Do I need to preheat my air fryer?",
             "Usually only 2-3 minutes, if at all — the small chamber reaches temperature fast. For frozen foods and thin items start from cold and add a minute; for battered or delicate bakes, a short preheat keeps the first minute from being soggy."),
            ("What foods don't convert well to the air fryer?",
             "Wet batters (they drip before setting), leafy greens (they fly into the element), cheese-only dishes (they melt through the basket) and large roasts (the outside overcooks before the center is done). Everything breaded, frozen or vegetable-ish converts beautifully."),
        ],
    })

    pages.append({
        "slug": "loan-payment-calculator",
        "title": "Loan Payment Calculator — Monthly Payment, Total Interest & Cost",
        "h1": "Loan Payment Calculator",
        "desc": "Enter amount, rate and term to see the amortized monthly payment, total interest and what share of every payment is interest. Free, instant, no sign-up.",
        "category": "calculator",
        "keyword": "loan payment calculator",
        "tool": "loanpay",
        "args": {},
        "intro": [
            "Every loan quote hides the same three numbers inside one monthly figure: a $25,000 car loan at 7.5% for five years is about $501 a month — which quietly becomes $30,056 of payments and roughly $5,000 of pure interest over the term. Enter amount, annual rate and term; the calculator returns the payment, the total interest, and the share of every payment that never touches your balance.",
            "That interest share is the number to shop with: a shorter term or a single-point rate cut moves it more than most people expect. The note line keeps the payoff logic visible — extra principal each month skips every future month's interest on that money — and your numbers stay on this device, so comparing dealer quotes takes seconds. It pairs with the compound interest calculator for the other side of the ledger: what that same money earns when you invest it instead.",
        ],
        "howto": [
            "Enter the loan amount, annual interest rate and term in years.",
            "Read the monthly payment, total interest and interest share of all payments.",
            "Share the payment with one tap, or bookmark it — your quote numbers are remembered.",
        ],
        "faqs": [
            ("What is the loan payment formula?",
             "For an amortized loan with monthly compounding: payment = P × r × (1+r)^n ÷ ((1+r)^n − 1), where P is the principal, r the monthly rate (annual ÷ 12) and n the number of payments. At 0% interest it collapses to the simple split: principal ÷ months."),
            ("How much does a shorter term save?",
             "A lot, because interest has fewer months to accumulate. The same $25,000 at 7.5% costs about $5,056 over 60 months but roughly $3,268 over 48 — the payment rises about $100 while the interest drops nearly a fifth. The calculator makes that trade explicit in the interest-share stat."),
            ("Does paying extra principal change the payment?",
             "No — extra principal shortens the term instead. Your required monthly payment stays fixed; each extra dollar reduces the balance, so subsequent months accrue less interest and the loan ends sooner. Lenders apply extra to principal only if you say so; otherwise some treat it as an early next payment."),
            ("What's missing from this calculator?",
             "Fees, taxes, insurance and balloon structures. APR wraps some fees into the rate, so comparing APRs — not headline rates — is the honest basis. For a lease or balloon note the amortization differs; treat this tool as the standard fixed-payment case."),
        ],
    })

    pages.append({
        "slug": "vat-calculator",
        "title": "VAT Calculator — Add or Remove VAT (UK 20% & EU Rates)",
        "h1": "VAT Calculator",
        "desc": "Add VAT to a net price or strip it from a gross price — UK 20%, Germany 19%, Ireland 23% and more, with the divide-don't-subtract method shown. Free, no sign-up.",
        "category": "calculator",
        "keyword": "vat calculator",
        "tool": "vatcalc",
        "args": {},
        "intro": [
            "Two VAT jobs account for almost every search: a business prices up — £100 net becomes £120 gross at the UK's 20% standard rate — and an accountant digs the tax back out of a receipt, where the right move is dividing by 1.2, never subtracting 20% (that gives £96, not the true £100 net). This calculator does both directions from one amount box, with quick-pick rates for the UK, Germany, the Netherlands, Spain, Italy and Ireland.",
            "The net / VAT / gross trio updates live so the breakdown is always in view, and the note line shows the exact arithmetic — the multiplier or divisor used — so the method transfers to your own spreadsheet. Fractions of a penny are kept to two decimals the way invoices round, and your last rate stays on this device for the next receipt. It sits alongside the sales tax calculator for US prices and the GST calculator for Indian ones.",
        ],
        "howto": [
            "Pick Add VAT (net to gross) or Remove VAT (gross to net), then enter the amount.",
            "Type a rate or quick-pick one — UK 20% is the default placeholder.",
            "Read net, VAT and gross at once; share or bookmark it — the rate is remembered.",
        ],
        "faqs": [
            ("How do I remove 20% VAT from a price?",
             "Divide the gross by 1.2. A £120 receipt holds £100 of net and £20 of VAT; subtracting 20% instead gives £96 and understates the net by £4. General rule: net = gross ÷ (1 + rate), which the calculator applies and shows in the note line."),
            ("How do I add VAT to a net price?",
             "Multiply net by (1 + rate): £100 × 1.2 = £120 gross, of which £20 is VAT payable to HMRC after your input credit. The calculator's add mode does exactly this and keeps all three figures visible at once."),
            ("What are the standard VAT rates in Europe?",
             "UK 20%, Germany 19%, Netherlands and Spain 21%, Italy 22%, Ireland 23%, France 20%. Most countries also run reduced rates (UK 5% for energy, 0% for food and children's clothes) — the quick-rate list carries the common ones and the rate box accepts any number a special case needs."),
            ("Is VAT the same as sales tax?",
             "Mechanically similar — a percentage on consumption — but VAT is charged at each stage of production with credits for tax already paid, while US sales tax is collected once at the final sale. For arithmetic on a price they behave the same, which is why the sales tax, VAT and GST calculators here share one shape."),
        ],
    })

    pages.append({
        "slug": "fraction-calculator",
        "title": "Fraction Calculator — Add, Subtract, Multiply & Divide, Simplified",
        "h1": "Fraction Calculator",
        "desc": "Add, subtract, multiply or divide two fractions — exact simplified answer with mixed number, decimal and the common-denominator steps shown. Free, no sign-up.",
        "category": "calculator",
        "keyword": "fraction calculator",
        "tool": "fraction",
        "args": {},
        "intro": [
            "Fraction homework fails on the same step every time: 3/4 + 5/6 needs a common denominator before anything else can happen. This calculator works with whole-number numerators and denominators in both fractions, then returns the exact simplified answer — 19/12 — alongside the mixed number (1 7/12), the decimal, and the worked line that shows the common denominator it used, so the answer teaches the method instead of replacing it.",
            "Division gets the same treatment with its own trick — flip and multiply — and every result is reduced by the greatest common divisor, with the divisor named in the note. Negative numerators work for subtracting-below-zero cases. Inputs are remembered on this device, which makes checking a whole worksheet's worth of problems a matter of editing two numbers between questions. It pairs with the roman numeral and prime factorization tools in the study corner of the site.",
        ],
        "howto": [
            "Enter the numerator and denominator of each fraction as whole numbers.",
            "Choose add, subtract, multiply or divide — the answer updates live.",
            "Read the simplified fraction, mixed number and decimal; the note shows the steps.",
        ],
        "faqs": [
            ("How do you add fractions with different denominators?",
             "Rewrite both over the least common denominator, then add the numerators: 3/4 + 5/6 becomes 9/12 + 10/12 = 19/12. The calculator shows exactly this line, including the common denominator it chose, then simplifies the result by the GCD."),
            ("How do you divide fractions?",
             "Multiply by the reciprocal: 3/4 ÷ 5/6 = 3/4 × 6/5 = 18/20 = 9/10. No common denominator needed — flip the second fraction and multiply. The note line writes out the flip so the habit sticks."),
            ("How do I simplify a fraction?",
             "Divide numerator and denominator by their greatest common divisor. 18/20 share a GCD of 2, giving 9/10; the note names the divisor it used so you can check the work by hand. A fraction is fully simplified when nothing above 1 divides both parts."),
            ("Can this handle mixed numbers like 1 3/4?",
             "Enter them as improper fractions — 1 3/4 is 7/4 — and the calculator returns the answer both ways: simplified improper and mixed. To convert by hand, multiply the whole by the denominator and add the numerator (1×4+3=7) over the original denominator."),
        ],
    })

    pages.append({
        "slug": "pregnancy-due-date-calculator",
        "title": "Pregnancy Due Date Calculator — EDD, Gestational Age & Trimester",
        "h1": "Pregnancy Due Date Calculator",
        "desc": "Estimate your due date from your last period, conception date or an ultrasound reading — plus gestational age today, days to go and trimester. Free, no sign-up.",
        "category": "calculator",
        "keyword": "pregnancy due date calculator",
        "tool": "pregnancy",
        "args": {},
        "intro": [
            "Due dates are arithmetic with a disclaimer: Naegele's rule adds 280 days to the first day of your last period, because the average pregnancy runs 40 weeks from that anchor. Enter an LMP date, a conception date (266 days), or an ultrasound reading with its gestational age and the calculator returns the estimated due date with its weekday, how far along you are today in weeks and days, the countdown, and which trimester you're in.",
            "The date is remembered on this device, so each visit shows the current week without re-entering anything — the kind of page people genuinely come back to weekly. Two honest caveats travel with the answer: only about 5% of babies arrive on the due date itself (most come within two weeks of it), and first-trimester ultrasound dating beats LMP when cycles are irregular. This tool does the math your midwife will recognize; it doesn't replace them.",
        ],
        "howto": [
            "Choose your method: last period, conception date, or ultrasound with gestational age.",
            "Enter the reference date (plus weeks and days for ultrasound).",
            "Read the due date, current gestational age, days remaining and trimester - it updates weekly on return visits.",
        ],
        "faqs": [
            ("How is a due date calculated?",
             "Naegele's rule: first day of the last menstrual period + 280 days, assuming a 28-day cycle with ovulation on day 14. From a known conception date it's 266 days; from a first-trimester ultrasound, the measured gestational age is subtracted from 280 to project the due date. All three methods are built in."),
            ("How accurate is a due date?",
             "As a deadline, not very — roughly 5% of babies arrive on it, though most deliver between 37 and 42 weeks. As the midpoint that anchors every appointment, test and milestone, it works well, which is why clinicians redated pregnancies from early ultrasound when the two disagree by more than a week."),
            ("What gestational age am I today?",
             "Weeks and days since the LMP date — 32w 3d means 32 weeks and 3 days of the 40-week term. The calculator computes this fresh on every visit against today's date, along with the trimester split at 13 and 27 completed weeks."),
            ("Does an irregular cycle change the due date?",
             "Yes — Naegele assumes ovulation on day 14, so long or irregular cycles push the real conception date later and the LMP-based estimate early. If you know ovulation or conception, use those methods here, or trust a dating ultrasound over the calendar."),
        ],
    })

    pages.append({
        "slug": "time-zone-converter",
        "title": "Time Zone Converter — DST-Aware Meeting Times Across Cities",
        "h1": "Time Zone Converter",
        "desc": "Convert any date and time between 20+ world zones with daylight saving handled automatically - see the local time, hour difference and date shift. Free, no sign-up.",
        "category": "converter",
        "keyword": "time zone converter",
        "tool": "tzconvert",
        "args": {},
        "intro": [
            "Every international call scheduling failure is the same three traps: the raw hour difference, the date rolling over, and daylight saving moving one city but not the other. Enter a date and time in one zone and this converter answers all three for the zone on the other end — the local wall-clock time, the signed difference including half-hours, and whether the result lands next day or the day before.",
            "The zone list covers the world's business hubs from New York to Auckland, and your device's own zone appears first so the common case is one dropdown. Conversions use your browser's built-in IANA timezone database, so DST transitions are computed exactly — a July date and a January date between London and New York genuinely differ by an hour, and the converter knows it. Your pairing is remembered for the next call.",
        ],
        "howto": [
            "Pick the from-zone (your device zone is listed first) and enter a date and time.",
            "Choose the to-zone - the local time, hour difference and date shift appear instantly.",
            "Share the meeting time with one tap; the pairing is remembered on this device.",
        ],
        "faqs": [
            ("How do I convert time between two zones?",
             "Take the wall-clock time in the first zone, find its UTC instant, then re-express that instant in the second zone's rules. The calculator does this using the browser's IANA database - the same one servers use - rather than fixed offsets, so the answer is right on the exact date you enter."),
            ("Why does the time difference between two cities change through the year?",
             "Daylight saving: zones shift on different dates (US and Europe differ by weeks) and not all zones observe it at all. London-New York is 5 hours in January but 4 in midsummer for the gap weeks. DST is handled automatically here - enter the real meeting date and you get the real answer."),
            ("What about half-hour and 45-minute offsets?",
             "India sits at UTC+5:30, Nepal at +5:45, and parts of Australia at +9:30 - all in the list, and the difference line shows the minutes when they matter. This is a common failure of quick mental math that a converter never makes."),
            ("Does this work offline?",
             "Yes - everything runs locally in your browser using its built-in timezone data, with no network calls or accounts. Save it to your home screen and it keeps working on a plane, which is exactly when you need it."),
        ],
    })

    pages.append({
        "slug": "week-number-calculator",
        "title": "Week Number Calculator — ISO Week, Quarter & Day of Year",
        "h1": "Week Number Calculator",
        "desc": "Find the ISO-8601 week number for any date - with Monday-Sunday boundaries, quarter and day of year, and the first-Thursday rule explained. Free, no sign-up.",
        "category": "calculator",
        "keyword": "week number calculator",
        "tool": "weeknum",
        "args": {},
        "intro": [
            "What week is it? The question sounds trivial until ISO-8601's answer bites: weeks run Monday to Sunday, and week 1 of a year is the one containing the first Thursday — so 1 January can belong to week 52 of the previous year, and some years legitimately have 53 weeks. Pick any date and this calculator returns the ISO week number, the exact Monday-Sunday span it covers, the quarter, and the day-of-year out of 365 or 366.",
            "It defaults to today, which makes it a handy weekly reference: planners, sprint cadences, manufacturing date codes and European calendars all speak ISO weeks. The note explains the first-Thursday rule because that's the part that breaks expectations — a date and its week number can disagree about the year, and the calculator shows which ISO year each week actually belongs to. Your last date is remembered between visits.",
        ],
        "howto": [
            "Enter any date - it starts on today's date for a quick answer.",
            "Read the ISO week number, the Monday-Sunday span, quarter and day of year.",
            "Share the week with one tap, or bookmark it - the date is remembered.",
        ],
        "faqs": [
            ("What ISO week is it right now?",
             "Open the page and it's calculated instantly from today's date - no input needed. The ISO-8601 system numbers weeks from the week containing the year's first Thursday, with weeks starting Monday, so the number matches what European calendars and most project tools show."),
            ("Why can January 1st be in week 52 or 53?",
             "Because week 1 needs the first Thursday. If New Year falls on a Friday, Saturday or Sunday, those days belong to the final week of the old year - and conversely a December 29-31 can already be week 1 of the next. The Monday-Sunday span shown for your date makes the boundary visible."),
            ("When does a year have 53 weeks?",
             "When it either starts on a Thursday or is a leap year starting on a Wednesday - 71 of every 400 years qualify, most recently spaced irregularly (2020 had 53 weeks; so will 2026). The day-of-year stat alongside helps you sanity-check where you stand."),
            ("Is the ISO week the same everywhere?",
             "No - the US convention often numbers weeks from January 1 regardless of weekdays, and Sunday-start calendars (Middle East, parts of North America) shift every boundary. This calculator follows ISO-8601, the standard used by Europe, most software and international business."),
        ],
    })

    pages.append({
        "slug": "time-card-calculator",
        "title": "Time Card Calculator — Weekly Hours, Lunch Deduction & Overtime",
        "h1": "Time Card Calculator",
        "desc": "Add up a full week of clock-ins and clock-outs - lunch deducted, overnight shifts handled, overtime over 40 hours flagged. Free, no sign-up.",
        "category": "calculator",
        "keyword": "time card calculator",
        "tool": "timecard",
        "args": {},
        "intro": [
            "Timesheet math has three traps that a calculator removes: subtracting lunch twice (or never), overnight shifts where the clock-out is a smaller number than the clock-in, and the hour-and-minute to decimal conversion payroll actually wants. Fill in the week's in/out pairs, set one unpaid-lunch figure, and this time card returns total hours in h m format, the decimal total for the payroll system, hours past the 40-hour overtime line, and the average day.",
            "Empty days are simply skipped, so part-time weeks and mid-week starts work without zero-filling. Overnight shifts roll past midnight automatically, and the whole week is remembered on your device — next week you edit the days that changed instead of retyping the roster. It pairs with the hours calculator for single spans and the overtime pay calculator once the hours become money.",
        ],
        "howto": [
            "Enter clock-in and clock-out for each day worked - leave days blank.",
            "Set the unpaid lunch minutes deducted per day (0 if none).",
            "Read the weekly total in hours-minutes and decimal, plus overtime over 40h.",
        ],
        "faqs": [
            ("How do I calculate hours worked from clock times?",
             "Convert both times to minutes since midnight and subtract: 09:00 is 540, 17:00 is 1020, and 1020 - 540 = 480 minutes = 8 hours. Overnight shifts add 24 hours to the out-time when it is smaller than the in-time; the calculator applies both rules and deducts lunch once per worked day."),
            ("Why does payroll want decimal hours?",
             "Payroll systems multiply wage by hours as a plain number, and 7h 30m breaks that arithmetic — it must become 7.5. The decimal total here is rounded to two places, which matches typical payroll exports; the h m display stays for humans."),
            ("When does overtime start?",
             "In the US, FLSA overtime runs past 40 hours in a workweek — daily overtime rules in states like California differ. The calculator flags everything past 40 weekly hours; multiply that figure by your 1.5x rate in the overtime pay calculator for the dollar amount."),
            ("What about breaks - are they paid?",
             "Short rest breaks (5-20 minutes) are paid working time under FLSA; bona fide meal periods (typically 30+ minutes) are unpaid only if you are fully relieved of duty. The lunch deduction here models the unpaid meal break; paid breaks need no deduction at all."),
        ],
    })

    pages.append({
        "slug": "one-rep-max-calculator",
        "title": "One Rep Max Calculator — Epley, Brzycki & Lander 1RM",
        "h1": "One Rep Max Calculator",
        "desc": "Estimate your one rep max from any set - Epley, Brzycki and Lander formulas averaged, with percentage working weights for your program. Free, no sign-up.",
        "category": "calculator",
        "keyword": "one rep max calculator",
        "tool": "onerepmax",
        "args": {},
        "intro": [
            "Nobody should test a true 1RM every week - it beats up the joints and stalls the program - so lifters estimate it from heavy sets instead. Enter the weight and reps you actually moved, and this calculator runs the three standard formulas at once: Epley (the classic, generous at high reps), Brzycki (accurate under 10 reps), and Lander, then averages them into the working number your percentages come from.",
            "Alongside the max you get the practical translation: the 80% weight for 5x5 strength blocks, and the note reminds you where the estimates live honestly - tight under 10 reps, drifting beyond. Your last lift is remembered on the device, so week-to-week progression means editing one number. It pairs with the macro calculator for the kitchen half of the training equation.",
        ],
        "howto": [
            "Enter the weight you lifted and the reps you completed with good form.",
            "Read your estimated 1RM - three formulas plus their average.",
            "Use the percentage working weights (80% for 5x5) to set your program.",
        ],
        "faqs": [
            ("What is a one rep max?",
             "The heaviest weight you can lift for a single clean repetition. It anchors strength programming: a 5x5 squat block at 80% of 1RM, a peaking block walking 90-95%. Testing it directly is exhausting and risky, which is why formulas estimate it from sets of 1-10 reps."),
            ("Which 1RM formula is most accurate?",
             "For under 10 reps, Brzycki and Epley land within a couple of percent of each other; above that, Epley runs high because rep endurance inflates it. Averaging Epley, Brzycki and Lander - what this calculator does - hedges the extremes and matches how most programs publish their percentages."),
            ("How do I use percentages of my 1RM?",
             "Strength blocks cluster at 80-90% (reps drop to 3-5), hypertrophy at 65-80% (reps 6-12), and technique or deload work sits around 60%. The 80% figure shown is the classic 5x5 working weight - heavy enough to force adaptation, light enough to accumulate volume."),
            ("Do these formulas work for women and for all lifts?",
             "They were built mostly on male squat/bench/deadlift data and hold well there; for upper-body lifts and female lifters they tend to read slightly low at higher reps. Treat the output as a training anchor - a number to round your programming against - rather than a laboratory measurement."),
        ],
    })

    pages.append({
        "slug": "standard-deviation-calculator",
        "title": "Standard Deviation Calculator — Sample & Population SD, Mean",
        "h1": "Standard Deviation Calculator",
        "desc": "Paste any dataset to get sample and population standard deviation, variance, mean, n and range - with the n-1 vs n rule explained. Free, no sign-up.",
        "category": "calculator",
        "keyword": "standard deviation calculator",
        "tool": "stddev",
        "args": {},
        "intro": [
            "Standard deviation answers the question averages hide: how spread out is the data? Two classes can both average 75 while one has everyone at 74-76 and the other ranges from 40 to 100 - the mean is identical, the standard deviations are worlds apart. Paste numbers separated by spaces, commas or new lines and this calculator returns the sample SD (the n-1 figure for data drawn from a bigger population), the population SD (when your data is everyone), the variance both ways, the mean, and the range.",
            "The n-1 versus n choice is where most homework loses marks, so the note line states which divisor produced each number and when to use it: sample data reports n-1, a complete population reports n. Results are rounded to six decimals, datasets are remembered between visits, and it pairs with the average calculator for the rest of the summary statistics.",
        ],
        "howto": [
            "Paste or type your numbers - any mix of spaces, commas and line breaks.",
            "Read sample SD, population SD, mean, variance and range instantly.",
            "Check the note for which divisor applies to your data before reporting.",
        ],
        "faqs": [
            ("What is standard deviation?",
             "The typical distance of data points from the mean. It is calculated as the square root of variance - the average of squared deviations - which restores the original units. Low SD means values cluster tight; high SD means they spread wide. For the dataset 2, 4, 4, 4, 5, 5, 7, 9 the sample SD is about 2.138."),
            ("When do I use sample (n-1) versus population (n)?",
             "Use n-1 when your numbers are a sample estimating a larger population - Bessel's correction compensates for the sample mean underestimating spread. Use n only when you truly have every member: all of a class, a complete production run. When unsure with sampled data, the n-1 sample SD is the defensible default."),
            ("What is variance and how does it relate?",
             "Variance is standard deviation squared - the same spread measured in squared units. The calculator shows both: variance feeds other statistics (tests, ANOVA), while SD is the one you quote because its units match the data - centimeters, dollars, points."),
            ("Does this handle negative and decimal numbers?",
             "Yes - any finite numbers parse, including negatives and decimals, in any order. Tokens that are not numbers are ignored rather than breaking the run, so a stray label in pasted spreadsheet data will not sabotage the calculation."),
        ],
    })

    pages.append({
        "slug": "concrete-calculator",
        "title": "Concrete Calculator — Cubic Yards, Bags & Slab Estimates",
        "h1": "Concrete Calculator",
        "desc": "Enter slab length, width and thickness to get cubic yards for the ready-mix order plus 80 lb and 60 lb bag counts. Free, instant, no sign-up.",
        "category": "calculator",
        "keyword": "concrete calculator",
        "tool": "concrete",
        "args": {},
        "intro": [
            "Concrete is ordered in cubic yards but planned in feet and inches, and the arithmetic between them is where budgets leak: a 10 × 10 ft patio at 4 inches deep is 33.3 cubic feet, which is 1.23 cubic yards — order one yard and you are short, order two and you paid for a third of a truck you didn't need. Enter the slab's length, width and thickness and this calculator converts straight to yards, with the 80 lb and 60 lb bag counts for the small-job alternative.",
            "The note carries the two rules that separate a clean pour from a cold joint: add 5-10% for spillage and uneven subgrade, and cross the bags-versus-truck threshold honestly — below roughly a cubic yard, mixing bags makes sense; above it, ready-mix wins on both cost and consistency. Metric mode computes in cubic meters with the yard equivalent alongside. Your slab numbers stay on this device for the next stage of planning.",
        ],
        "howto": [
            "Enter the slab length and width, then pick the thickness - 4 in for patios, 6 in for driveways.",
            "Read cubic yards for the ready-mix order and bag counts for small jobs.",
            "Add 5-10% waste per the note, then share or bookmark - dimensions are remembered.",
        ],
        "faqs": [
            ("How many bags of concrete per cubic yard?",
             "A cubic yard is 27 cubic feet, and an 80 lb bag yields about 0.60 cubic feet - so 45 bags per yard. Sixty-pound bags yield 0.45 cubic feet, needing 60 per yard. The calculator shows exact counts for your volume; just add the 10% waste margin before checkout."),
            ("How much concrete for a 10x10 slab?",
             "It depends entirely on thickness: 4 inches deep is 1.23 cubic yards, 6 inches is 1.85. This is why thickness is a dropdown rather than an afterthought - the difference between patio spec and driveway spec is half a truck."),
            ("Should I order extra concrete?",
             "Yes - 5-10% covers spillage, uneven subgrade, and the edge of the form that always seems deeper than measured. Coming up short mid-pour means a cold joint and a weakened slab, which costs far more than the extra quarter yard."),
            ("Bags or ready-mix truck - which is cheaper?",
             "Below about one cubic yard, bags win once you factor the short-load fees trucks charge for small pours. Above a yard, ready-mix wins decisively on labor and consistency - hand-mixing 45 bags is a full, miserable day, and the result is only as uniform as your mixing."),
        ],
    })

    pages.append({
        "slug": "slope-calculator",
        "title": "Slope Calculator — Two Points to m, Fraction, Angle & Intercept",
        "h1": "Slope Calculator",
        "desc": "Find the slope between two points - decimal and exact fraction, inclination angle, y-intercept and the perpendicular slope, with steps shown. Free, no sign-up.",
        "category": "calculator",
        "keyword": "slope calculator",
        "tool": "slopecalc",
        "args": {},
        "intro": [
            "Slope is rise over run, and the fraction is where the understanding lives: from (2, 3) to (7, 8) the line rises 5 over a run of 5 - slope 1, a 45° line, clean and exact. Enter any two points and this calculator returns the slope as both decimal and reduced fraction, the inclination angle in degrees, the y-intercept, and the slope any perpendicular line would need - the four numbers algebra homework and roof-pitch questions actually ask for.",
            "The worked note shows the rise-over-run division with your numbers substituted, so the answer demonstrates its own method. Vertical lines are handled as the special case they are - undefined slope, 90°, no intercept - rather than crashing into a division by zero. Points are remembered between visits for multi-part problems, and the page sits with the fraction and degrees-radians tools in the study corner.",
        ],
        "howto": [
            "Enter the x and y of both points.",
            "Read the slope as decimal and fraction, plus angle and y-intercept.",
            "Use the perpendicular slope in the note for parallel/perpendicular questions.",
        ],
        "faqs": [
            ("What is the slope formula?",
             "m = (y₂ - y₁) / (x₂ - x₁) - the vertical change between the points divided by the horizontal change. From (2, 3) to (7, 8): (8-3)/(7-2) = 5/5 = 1. The note line reproduces exactly this substitution with your values."),
            ("What does a negative slope mean?",
             "The line falls as it moves left to right - downhill in standard reading order. Positive slopes rise, zero slopes run horizontally (both y values equal), and undefined slopes are vertical (both x values equal). The direction is named in the result note."),
            ("How do I find the y-intercept from two points?",
             "Solve y = mx + b with one of your points: b = y₁ - m·x₁. The calculator does this and hands you the full line equation, which is usually the second half of the same homework problem."),
            ("How are slope and angle related?",
             "The inclination angle is the arctangent of the slope: slope 1 is 45°, slope √3 ≈ 1.732 is 60°, and roofers flip the relationship - a 6:12 pitch means slope 0.5, about 26.57°. The angle stat connects the algebra view with the physical one."),
        ],
    })

    pages.append({
        "slug": "random-team-generator",
        "title": "Random Team Generator — Shuffle Names into Fair Teams",
        "h1": "Random Team Generator",
        "desc": "Paste a list of names and split them into any number of fair, random teams with one click - crypto-grade shuffle, re-draw anytime. Free, no sign-up.",
        "category": "generator",
        "keyword": "random team generator",
        "tool": "teamgen",
        "args": {},
        "intro": [
            "Every teacher, coach and facilitator knows the ritual: 24 names, 4 teams, and the suspicion that the draw wasn't quite random. Paste the list - one name per line - choose how many teams, press Shuffle, and this generator deals everyone out using cryptographically secure randomness from your own device, with team sizes balanced to within one person and the roster preserved for the next session.",
            "The balance line shows the exact distribution (2 teams of 7 and 2 of 5, for instance), and re-shuffling costs one click - no recutting strips of paper. The share button packages the full draw as text for the group chat, with a link that carries the name list so colleagues can re-run it on their side. It joins the coin flip, dice roller and random number tools for every decision that should not be yours to make.",
        ],
        "howto": [
            "Paste or type the names, one per line.",
            "Set the number of teams and press Shuffle.",
            "Read the teams, re-shuffle if needed, or share the draw to the group chat.",
        ],
        "faqs": [
            ("How does the team generator stay fair?",
             "Two parts: the shuffle uses the browser's cryptographic random source - the same one that guards web security - so every arrangement is equally likely, and the dealing round-robins the shuffled names so team sizes differ by at most one. No weighting, no seeding, no favorites."),
            ("Can I make uneven teams on purpose?",
             "Not directly here - balance is the point. If you need a 5-and-2 split for a scrimmage, run two draws or move one name by hand after shuffling; the honest randomness has already done its job by that point."),
            ("Are my names sent anywhere?",
             "No - the list never leaves the browser. Names are stored only in your own device's local storage so the next session starts where this one ended, and clearing the browser clears them."),
            ("Can it pick one winner instead of teams?",
             "For single draws use the random name generator; for yes/no decisions the coin flip; for order-of-play questions shuffle here and read the first team as the order. Same cryptographic engine underneath all of them."),
        ],
    })

    pages.append({
        "slug": "paint-calculator",
        "title": "Paint Calculator — How Much Paint per Room, Doors & Windows Off",
        "h1": "Paint Calculator",
        "desc": "Work out gallons or liters for any room - wall area minus doors and windows, coats included, with the buy-extra rule built in. Free, no sign-up.",
        "category": "calculator",
        "keyword": "paint calculator",
        "tool": "paintcalc",
        "args": {},
        "intro": [
            "The paint aisle mistake runs in one direction: buying one gallon for a job that needs two, because wall area hides inside room length and width. A 12 × 10 ft room with 8 ft ceilings carries 352 square feet of wall before openings - minus two doors and two windows, times two coats, that's roughly 1.6 gallons, which means buy two. This calculator walks the same steps: room dimensions in, doors and windows subtracted, coats multiplied, coverage divided, purchase rounded up.",
            "Coverage runs 350-400 sq ft per gallon on primed, smooth walls - the calculator uses the conservative 350 so the estimate errs toward enough. The note carries the trade's batch-matching rule: paint is tinted per batch, so finishing a wall from a second, unmatched can is the visible mistake the rounding-up prevents. Metric mode computes liters at 10 m² per liter. Room numbers are remembered for the next room in the same house.",
        ],
        "howto": [
            "Enter room length, width and wall height.",
            "Set doors and windows - standard 21 and 12 sq ft openings subtract automatically.",
            "Pick coats (2 is default) and read gallons or liters, rounded up for touch-ups.",
        ],
        "faqs": [
            ("How much paint do I need per room?",
             "Wall area = (length + width) × 2 × height, minus openings (21 sq ft per door, 12 per window), times coats, divided by 350 per gallon. A 12x10x8 room with two doors and two windows needs about 1.6 gallons for two coats - buy two, because partial gallons cannot be matched later."),
            ("Does 2 coats double the paint?",
             "Nearly - the second coat uses slightly less because the primed first coat seals the surface, but planning at double is the safe budget. Dark over light or light over dark colors may want three; the calculator's coats dropdown covers both."),
            ("How do I account for doors and windows?",
             "Subtract 21 sq ft per standard door and 12 per standard window from wall area before dividing by coverage - or enter exact counts and let the calculator do it. Painting the doors themselves? Add one door's worth back per door painted."),
            ("What about primer and ceiling?",
             "Primer covers more per gallon (roughly 400-500 sq ft) but budget it the same way per coat. Ceilings are their own area: length × width, same coverage math - and ceilings drink paint on textured finishes, so round up harder there."),
        ],
    })

    pages.append({
        "slug": "tile-calculator",
        "title": "Tile Calculator — Tiles, Boxes & 10% Waste for Any Area",
        "h1": "Tile Calculator",
        "desc": "Enter area and tile size to get the tile count, boxes to buy and the 10% cutting waste already included. Works in inches/feet or cm/meters. Free, no sign-up.",
        "category": "calculator",
        "keyword": "tile calculator",
        "tool": "tilecalc",
        "args": {},
        "intro": [
            "Tile math looks like simple division and then bites at the edges: a 12 × 10 ft floor takes 120 one-foot tiles on paper, but real floors have cuts, breakages, and the half-tile that shatters on the nipper - the trade's answer is 10% overage, and the tile shop's unit is the box, not the tile. This calculator does the full chain: area and tile size in, exact tile count, the 10% waste margin applied, and boxes rounded up to whole cartons.",
            "Both unit systems work - inches over feet, centimeters over meters - so imported tile specs and local room measurements coexist. The note keeps the spare-tile doctrine visible: dye lots change between production runs, so the leftovers from the 10% are your repair stock for the next decade. Dimensions are remembered on your device for comparing rooms and layouts.",
        ],
        "howto": [
            "Enter the area's length and width, then the tile's length and width.",
            "Set tiles per box as printed on the carton.",
            "Read tiles to buy, boxes, and the spare count from the 10% waste.",
        ],
        "faqs": [
            ("How many tiles do I need with waste?",
             "Compute area ÷ tile size for the exact count, then multiply by 1.10 for cuts and breakage - a 120-tile floor buys 132. Diagonal layouts and large-format tiles want 15% instead; straight grid layouts can live with 10%. The calculator applies 10% automatically."),
            ("How do I calculate tiles per box?",
             "Cartons print their coverage or piece count - commonly 12 one-foot tiles per box, but it varies by manufacturer and tile size. Enter the printed number and the calculator converts your waste-included count into whole boxes, because nobody sells you 7 tiles."),
            ("What about grout joints and pattern layouts?",
             "Grout spacing (typically 1/8 to 3/16 in) slightly reduces effective tile coverage, which the 10% waste comfortably absorbs. Herringbone and other offset patterns increase cutting waste - move to 15% by adding a box rather than trusting a tighter margin."),
            ("Should I keep leftover tiles?",
             "Yes - dye lots change, and a future repair with a mismatched lot shows forever. Store spares flat in conditioned space; they are your cheapest insurance on the floor you just paid for."),
        ],
    })

    pages.append({
        "slug": "half-birthday-calculator",
        "title": "Half Birthday Calculator — Date, Countdown & Exact Age",
        "h1": "Half Birthday Calculator",
        "desc": "Find your half birthday - the six-month mirror of your birth date - with the exact date, days until it, and your precise age today. Free, no sign-up.",
        "category": "calculator",
        "keyword": "half birthday calculator",
        "tool": "halfbday",
        "args": {},
        "intro": [
            "A half birthday is exactly what it sounds like: the calendar day six months after yours, when you turn X-and-a-half. Parents throw them for summer-born kids whose real birthdays collide with school holidays; leap-year and December 31 folks use them as the sane alternative; and everyone else enjoys a perfectly good excuse for cake in the off-season. Enter your birthday and this calculator names the exact date with its weekday, counts down the days to the next one, and states your precise age in years, months and days today.",
            "The arithmetic has one trap worth doing properly: six months after August 31 lands on a date that doesn't exist in February, so the calculator clamps to the month's last day and says so in the note. Your birthday is remembered on the device, which quietly turns the page into a little countdown you can revisit - and the share button packages the date for whoever needs to start planning.",
        ],
        "howto": [
            "Enter your date of birth.",
            "Read your half birthday's exact date and weekday, with a live day countdown.",
            "Share it, or bookmark - the countdown updates every visit.",
        ],
        "faqs": [
            ("What is a half birthday?",
             "The date exactly six months from your birth date - June 15's half birthday is December 15. It marks the X-and-a-half milestone between birthdays, celebrated mostly for kids with holiday-adjacent birthdays and by anyone who enjoys two cakes a year."),
            ("How do you calculate a half birthday?",
             "Add six months to the birth month and keep the day. When the day doesn't exist in the target month - August 31 to February - clamp to the last day of that month (February 28, or 29 in leap years). The calculator does both rules and explains which it applied."),
            ("Why celebrate a half birthday instead?",
             "Three common reasons: school-age kids born in summer never get the in-class party; December babies are drowned by the holidays; and leap-day birthdays (February 29) get a real calendar date every year instead of a borrowed one."),
            ("Is a half birthday the same as a half-birthday cake day for babies?",
             "Close - the six-month mark is also the traditional half-birthday photo shoot for babies, usually with a smash cake and a 6 sign. Same math, more frosting; this calculator gives parents the exact date and the countdown to book the photographer."),
        ],
    })

    pages.append({
        "slug": "ratio-calculator",
        "title": "Ratio Calculator — Solve A:B = C:x, Simplify & Scale",
        "h1": "Ratio Calculator",
        "desc": "Solve the missing value in any proportion - A is to B as C is to what? - with the simplified ratio, decimal and percentage alongside. Free, no sign-up.",
        "category": "calculator",
        "keyword": "ratio calculator",
        "tool": "ratiocalc",
        "args": {},
        "intro": [
            "Proportions are the workhorse of everyday math: scale a recipe from 4 servings to 6, convert a map distance, mix paint at 3:2, work out screen aspect. All of it is one sentence - A is to B as C is to x - and one move: x = C × B ÷ A. Enter the three known values and this calculator fills in the fourth, then shows the ratio simplified, as a decimal and as a percentage, with the cross-multiplication check written out so the answer verifies itself.",
            "The worked line is the point: 3:4 = 15:x resolves to x = 20 with the cross-products shown (3 × 20 = 60, 4 × 15 = 60), which is exactly the check a teacher wants to see. Values persist on your device for multi-step scaling sessions, and the page sits naturally beside the fraction calculator for the same students.",
        ],
        "howto": [
            "Enter the three known values of your proportion - A, B and C.",
            "Read x, plus the ratio simplified, decimal and percentage views.",
            "Check the cross-multiplication line, then share or keep the values for the next step.",
        ],
        "faqs": [
            ("How do I solve a proportion?",
             "Cross-multiply and divide: A:B = C:x means A·x = B·C, so x = B·C ÷ A. For 3:4 = 15:x: x = 15 × 4 ÷ 3 = 20. The note line shows this arithmetic - and its reverse check - with your numbers."),
            ("How do I simplify a ratio?",
             "Divide both sides by their greatest common divisor: 12:18 shares a GCD of 6, so the ratio is 2:3. The calculator reduces whatever you enter, including decimals (scaled to integers first), so 1.5:2 becomes 3:4."),
            ("How do I scale a recipe with ratios?",
             "Treat servings as one side of the proportion. A recipe serving 4 with 2 cups of rice scales to 6 servings via 4:6 = 2:x - x = 3 cups. Enter recipe servings, target servings and the known quantity in the A, B, C slots in that order."),
            ("What's the difference between a ratio and a rate?",
             "A ratio compares like quantities (3 cups to 2 cups); a rate compares unlike ones with units kept (60 miles per hour). The math here solves both, but keep units explicit for rates - mixing numerators and denominators is the classic proportion error."),
        ],
    })

    pages.append({
        "slug": "calories-burned-calculator",
        "title": "Calories Burned Calculator — MET-Based by Activity & Weight",
        "h1": "Calories Burned Calculator",
        "desc": "Estimate calories burned for walking, running, swimming, HIIT and more - MET values by activity, your body weight and duration. Free, no sign-up.",
        "category": "calculator",
        "keyword": "calories burned calculator",
        "tool": "calburn",
        "args": {},
        "intro": [
            "Calorie burn is three numbers multiplied: the activity's MET value (its metabolic cost), your body weight in kilograms, and the hours you do it. Walking at 3 mph is 3.5 METs, so a 70 kg person on a one-hour walk burns 3.5 × 70 ≈ 245 kcal; the same person running at 8 mph burns nearly 700. Pick an activity, enter weight and duration, and this calculator returns the burn along with the per-10-minute rate and a food-equivalent for honest perspective.",
            "The MET table here covers twelve common activities from housework to HIIT, with a custom slot for anything the Compendium of Physical Activities lists. The note keeps the honesty: MET figures are population averages, and real burn moves 10-20% with intensity, fitness and terrain - a range that matters more the longer the session. Your last activity and weight persist on the device for daily logging, and the page pairs with the TDEE and macro calculators for the intake side of the equation.",
        ],
        "howto": [
            "Pick your activity - or enter a custom MET value.",
            "Enter body weight (kg or lb) and the duration in minutes.",
            "Read the calories burned, per-10-minute rate and food equivalent.",
        ],
        "faqs": [
            ("How are calories burned calculated?",
             "kcal = MET × weight in kg × hours. MET (metabolic equivalent of task) expresses energy cost as a multiple of rest - 1 MET is roughly 1 kcal per kg per hour. The calculator applies exactly this formula and shows the substituted arithmetic in the note."),
            ("How accurate are MET-based estimates?",
             "Within 10-20% for most people - MET values are lab averages, and individual burn varies with fitness, effort and terrain. Treat the output as a planning figure, not a receipt; consistency across activities matters more than absolute precision."),
            ("Why does body weight matter so much?",
             "Moving more mass costs more energy at the same pace - the kg term multiplies directly. A 100 kg runner burns about 40% more than a 70 kg runner over the same 5k at the same speed, which is also why heavier runners see faster initial burn as weight drops."),
            ("Do I burn calories differently than my fitness watch says?",
             "Watches add heart-rate data, which captures effort but carries its own error - studies find commercial trackers range widely on burn (some off by 30%+). The MET method is the transparent baseline: no black box, reproducible arithmetic, easy to sanity-check any device against."),
        ],
    })

    pages.append({
        "slug": "debt-payoff-calculator",
        "title": "Debt Payoff Calculator — Months to Debt-Free & Total Interest",
        "h1": "Debt Payoff Calculator",
        "desc": "See exactly when a balance dies: months to debt-free, total interest, the minimum-payment trap - and what paying a little more saves. Free, no sign-up.",
        "category": "calculator",
        "keyword": "debt payoff calculator",
        "tool": "debtpayoff",
        "args": {},
        "intro": [
            "Debt math hides its own cruelty inside the interest line: a $5,000 balance at 18% APR accrues $75 a month before you pay a cent, and minimum payments engineered just above that number stretch the payoff past a decade. Enter balance, APR and the payment you actually make, and this calculator simulates every month until the balance hits zero - then shows the months, the total interest, and the total that left your account.",
            "The note does the motivational arithmetic automatically: the same simulation at a 10% higher payment shows how many months disappear and how much interest survives - usually a startling ratio, which is precisely the point. Payments below the monthly interest trigger a plain-language warning instead of a bogus answer, and the strategy one-liner (snowball vs avalanche) closes it out. It pairs with the loan payment calculator for the borrowing side.",
        ],
        "howto": [
            "Enter the balance, the APR and your monthly payment.",
            "Read months to debt-free, total interest and total paid.",
            "Check the note for what a slightly bigger payment saves you.",
        ],
        "faqs": [
            ("How long will it take to pay off my debt?",
             "Depends on the gap between payment and interest: $5,000 at 18% APR with $200/month takes about 32 months and roughly $1,230 in interest; at $150/month it stretches to 43 months and over $1,900. The calculator simulates month by month rather than trusting a closed formula, so irregular inputs still get honest answers."),
            ("What is the minimum payment trap?",
             "Minimums are typically 1-2% of the balance plus interest - at 2%, most of the payment is interest, and the payoff stretches toward decades. This calculator flags it directly: if your payment doesn't clear the monthly interest, it says so and states the minimum payment that actually makes progress."),
            ("Snowball or avalanche - which is better?",
             "Avalanche (highest APR first) is mathematically optimal; snowball (smallest balance first) wins on psychology because closing an account builds momentum. The interest difference is usually modest - pick the one you'll sustain, and let the extra-payment note show what consistency buys."),
            ("Should I pay extra or invest the difference?",
             "Compare guaranteed vs expected: extra payments return the APR risk-free (18% card payoff beats almost any investment), while low-APR debt (sub-5%) against long-horizon investing is a genuine coin toss. Run your numbers here, then decide with the loan payment calculator as the counterweight."),
        ],
    })

    pages.append({
        "slug": "json-formatter",
        "title": "JSON Formatter & Validator — Pretty Print, Minify, Locally",
        "h1": "JSON Formatter",
        "desc": "Format, validate and minify JSON in your browser - pretty print with 2-space or tab indent, exact parse-error position, nothing uploaded. Free, no sign-up.",
        "category": "text",
        "keyword": "json formatter",
        "tool": "jsontool",
        "args": {},
        "intro": [
            "Half of all JSON errors are the same three culprits: a trailing comma after the last item, single quotes standing in for double, and an unquoted key. Paste any JSON here and the formatter validates it with the browser's native parser, pretty-prints it at your chosen indent, and when something is wrong it names the character position and the likely offender instead of just saying 'unexpected token'.",
            "The stats line sizes the payload (bytes, keys plus values, nesting depth) - handy for spotting the 200 KB config that grew quietly. Minify collapses it back for transport. Everything runs locally in your browser: API responses with tokens, customer data, draft payloads - none of it leaves the page, which is exactly why a local formatter beats a random web one.",
        ],
        "howto": [
            "Paste your JSON - validation and pretty print happen instantly.",
            "Pick 2-space, 4-space or tab indent; Minify collapses for transport.",
            "Fix errors by their reported position, then copy or re-check.",
        ],
        "faqs": [
            ("Is my JSON uploaded anywhere?",
             "No - parsing and formatting use the browser's own JSON engine on this page, with zero network calls. That matters for API responses and config files containing tokens; a local formatter is the one that cannot leak them."),
            ("Why is my JSON invalid with a trailing comma?",
             "Strict JSON forbids a comma after the final element - {\"a\":1,} fails. The error usually points just past the real spot. JavaScript objects allow it, which is why code pasted into a JSON context breaks; remove the last comma and it parses."),
            ("What's the difference between JSON and a JavaScript object?",
             "JSON is a text format: keys must be double-quoted, no comments, no single quotes, no undefined, and numbers have rules. A JS object literal is looser on all of those. Formatting here validates against strict JSON, so it catches the looseness a browser would silently accept in code."),
            ("Does it handle large files?",
             "Comfortably into the megabytes on a normal machine - the limit is your browser's textarea, not a server. For very large payloads the stats line (bytes, node count, depth) gives you the shape before you expand it."),
        ],
    })

    pages.append({
        "slug": "base64-encode-decode",
        "title": "Base64 Encode & Decode — UTF-8 Safe, Runs in Your Browser",
        "h1": "Base64 Encode & Decode",
        "desc": "Convert text to Base64 and back with full UTF-8 support - emoji and non-Latin scripts round-trip perfectly, invalid input flagged clearly. Free, no sign-up.",
        "category": "text",
        "keyword": "base64 encode",
        "tool": "base64",
        "args": {},
        "intro": [
            "Base64 turns arbitrary bytes into a safe alphabet of 64 characters - the encoding behind data URLs, Basic auth headers, JWT payloads and email attachments. The classic tool trap is UTF-8: naive encoders mangle emoji and non-Latin text. This one round-trips every character correctly in both directions, shows input and output lengths with the 3-bytes-to-4-chars math, and flags genuinely invalid Base64 instead of silently producing garbage.",
            "Decode mode is also a reader: JWT middle sections, data-URI payloads and mystery strings from logs become readable text in one paste. Everything runs locally - credentials in Basic auth strings or tokens inside JWTs never leave the page. Your last input is remembered for iterative work, and the copy button puts the result straight on the clipboard.",
        ],
        "howto": [
            "Choose encode or decode, then paste your input.",
            "Read the result - lengths, byte counts and the padding math update live.",
            "Copy the output with one tap; errors explain what made the input invalid.",
        ],
        "faqs": [
            ("What is Base64 used for?",
             "Moving binary-safe data through text-only channels: embedding images as data URLs, HTTP Basic authentication headers, the parts of a JWT, and email's MIME attachments. It is not encryption - it is a reversible encoding anyone can read, so never treat Base64 as hiding anything."),
            ("Why does Base64 make data bigger?",
             "Every 3 bytes (24 bits) become 4 Base64 characters - a fixed 33% overhead, plus = padding to a multiple of 4. A 300-byte input encodes to 400 characters exactly; the stats here show the arithmetic on your own input."),
            ("Why do emoji break some Base64 tools?",
             "The naive btoa() works on 16-bit characters, but emoji and many scripts need proper UTF-8 byte conversion first. This tool encodes text → UTF-8 bytes → Base64 and reverses exactly that path, so every character round-trips."),
            ("Is my input sent to a server?",
             "No. Encoding and decoding run entirely in your browser - which is the right property for a tool you might paste auth headers into. Local-only by design, like every text tool on this site."),
        ],
    })

    pages.append({
        "slug": "url-encoder-decoder",
        "title": "URL Encoder & Decoder — Component vs Full URL, Explained",
        "h1": "URL Encoder & Decoder",
        "desc": "Encode and decode URLs and query values correctly - component mode for ?q= parameters, full-URL mode that keeps structure characters. Free, local, no sign-up.",
        "category": "text",
        "keyword": "url encoder",
        "tool": "urlcod",
        "args": {},
        "intro": [
            "URL encoding is why 'café & croissants' survives a query string: spaces become %20, the ampersand becomes %26 so it can't be misread as a separator, é becomes %C3%A9. This tool does both directions with the distinction most tools skip - component mode (for values inside ?a=1&b=2, escaping & = ? /) versus full-URL mode (keeping the :// and separators that make a URL work), with the difference explained in the note as you type.",
            "Decode mode is the reader for mystery links: paste a tracking URL or an encoded API parameter and see the human version instantly, with malformed sequences (% not followed by two hex digits) flagged precisely rather than decoding to garbage. The stats count the % sequences for you, and everything runs locally - your URLs, with their tokens and tracking parameters, stay on your device.",
        ],
        "howto": [
            "Pick encode or decode, then component or full-URL scope.",
            "Paste your text or URL - the result updates live with a length diff.",
            "Copy the output; malformed decodes explain exactly what broke.",
        ],
        "faqs": [
            ("When should I use %20 versus + for spaces?",
             "%20 is the encoding of a space in URLs and query strings (encodeURIComponent style, what this tool produces); + is the legacy application/x-www-form-urlencoded style from HTML form posts. Both decode to a space in practice, but %20 is the modern, always-safe choice - and what well-behaved APIs expect."),
            ("What is the difference between component and full-URL encoding?",
             "Component encoding escapes structure characters (& = ? /) so a value cannot be mistaken for URL syntax - right for ?q=... values. Full-URL encoding (encodeURI) keeps :// ? & intact because they ARE the syntax - right when encoding a complete URL to embed as a parameter."),
            ("Why did my decode fail with a lone % sign?",
             "Every % must be followed by exactly two hexadecimal digits. A bare percent - '50% off' pasted raw - is malformed; encode it first (%25) or remove it. The error note here pinpoints the rule rather than guessing."),
            ("Is URL encoding a form of encryption?",
             "Not at all - it is reversible transport encoding, readable by anyone. It makes text safe to carry in a URL; it hides nothing. For secrecy you need TLS (automatic on https) and proper encryption, not percent-encoding."),
        ],
    })

    pages.append({
        "slug": "jwt-decoder",
        "title": "JWT Decoder — Read Header, Payload & Expiry Locally",
        "h1": "JWT Decoder",
        "desc": "Paste a JWT to read its header and payload as JSON, with alg, claim count and expiry timing - exp, iat and nbf in plain language. Local only, no sign-up.",
        "category": "text",
        "keyword": "jwt decoder",
        "tool": "jwtdecode",
        "args": {},
        "intro": [
            "A JWT is three base64url parts separated by dots - header, payload, signature - and almost every debugging session starts with 'what's actually in this token?'. Paste it here and the decoder unpacks the first two parts into clean JSON, names the algorithm, counts the claims, and translates the unix timestamps into plain language: expired 3 hours ago, issued in 2 days, not yet valid for 40 minutes.",
            "Two boundaries are stated up front: signatures are never verified (decoding proves readability, not authenticity), and the token never leaves the browser - by design there is no URL state, so a pasted token can't leak into a shared link. This makes it safe for the tokens you actually debug: session JWTs, OIDC id_tokens, service-account tokens from cloud consoles.",
        ],
        "howto": [
            "Paste the full token - all three dot-separated parts.",
            "Read the header and payload as JSON, with alg and claim count.",
            "Check the expiry line - exp, iat and nbf in relative and absolute terms.",
        ],
        "faqs": [
            ("What are the three parts of a JWT?",
             "Header (algorithm and type), payload (the claims - subject, expiry, roles, whatever the issuer put in), and signature (the cryptographic proof over the first two). The first two are base64url-encoded JSON and readable by anyone; this decoder unpacks exactly those."),
            ("Can a JWT be read without the secret?",
             "Yes - the header and payload are encoded, not encrypted. Anyone holding the token can read every claim; the secret only matters for changing them, which the signature prevents. Treat JWTs like postcards, not sealed letters."),
            ("How do I know if a JWT is expired?",
             "The exp claim is a unix timestamp; expired means exp is in the past. This decoder states it in both relative (3h ago) and absolute (2026-09-13 21:00) terms, and also honors nbf (not-before) for tokens that activate later."),
            ("Is my token safe pasted here?",
             "Everything runs in your browser with zero network calls, and unlike other tools on this site, this one deliberately has no share-with-data URL state - a token must never travel inside a link. That said, pasted tokens are still tokens: revoke anything sensitive you wouldn't paste into your own terminal."),
        ],
    })

    pages.append({
        "slug": "amortization-schedule",
        "title": "Amortization Schedule Calculator — Payment Split Month by Month",
        "h1": "Amortization Schedule",
        "desc": "See every payment's interest/principal split and running balance - first year in full, anniversaries after, with extra-payment savings. Free, no sign-up.",
        "category": "calculator",
        "keyword": "amortization schedule",
        "tool": "amortize",
        "args": {},
        "intro": [
            "Early loan payments are mostly interest wearing a payment's clothing: on a $25,000, 7.5%, 5-year loan, payment one sends $156 to interest and $345 to principal - only in month 153 would a 30-year mortgage's split cross to majority principal. This schedule shows the whole march: each payment, its interest and principal pieces, and the running balance, with the first twelve months itemized and every anniversary after.",
            "The extra-payment field is where the table becomes a decision tool: add $100 a month and the schedule recomputes the payoff - months saved, interest saved, and the crossover month where your dollars start beating the bank's. The numbers are remembered for scenario comparing, and it pairs with the loan payment and debt payoff calculators on either side of the borrowing journey.",
        ],
        "howto": [
            "Enter loan amount, annual rate and term - the payment appears first.",
            "Read the schedule: month-by-month for year one, anniversaries after.",
            "Add an extra monthly amount to see months and interest saved instantly.",
        ],
        "faqs": [
            ("What is an amortization schedule?",
             "The table splitting every scheduled payment into interest (rate on the remaining balance) and principal (the rest), with the running balance until zero. Because interest rides the balance, early payments are interest-heavy and the principal share grows every month - the table makes that visible row by row."),
            ("Why do early payments barely reduce the balance?",
             "Interest is charged on the full remaining balance - at the start that's the whole loan. On a 30-year mortgage, payment one can be two-thirds interest; the principal snowball only dominates in the final years. The schedule shows exactly when your payment's split crosses over."),
            ("How do extra payments change the schedule?",
             "Extra dollars skip ahead: they apply entirely to principal, which shrinks every future month's interest charge. $100 extra on the sample loan saves around 10 months and hundreds in interest - the calculator computes it live rather than estimating."),
            ("Does this schedule match my bank's exactly?",
             "To the formula, yes - same standard amortization math. Bank statements can differ by pennies from rounding conventions, payment-date interest, or fees; treat this as the clean model of your loan, and the bank's as the noisy reality of it."),
        ],
    })

    pages.append({
        "slug": "csv-to-json",
        "title": "CSV to JSON Converter — Header Row to Keys, Quoted Cells Safe",
        "h1": "CSV to JSON",
        "desc": "Convert CSV to a JSON array instantly - headers become keys, quoted commas survive, numbers auto-typed, delimiter sniffed. Local, free, no sign-up.",
        "category": "text",
        "keyword": "csv to json",
        "tool": "csv2json",
        "args": {},
        "intro": [
            "CSV is what spreadsheets export and JSON is what APIs and code want, and the conversion breaks on the same details every time: commas hiding inside quoted cells, semicolon delimiters from European exports, and numbers that arrive as strings. This converter handles all three - quoted values are parsed properly, the delimiter is sniffed from the header row, numeric cells are typed as JSON numbers - and shows the result as clean, copyable JSON.",
            "The first row becomes object keys, so 'name,role' headers yield {\"name\":..., \"role\":...} records. Everything runs locally in your browser: customer exports and spreadsheet data never leave the page. Your last CSV is remembered for iteration, and the tool sits between the JSON formatter and Base64 decoder in the data-tools corner of the site.",
        ],
        "howto": [
            "Paste CSV with headers in the first row - commas, semicolons or tabs.",
            "Read the JSON array - records, columns, delimiter and numeric-cell count update live.",
            "Copy the output, or tweak the CSV and watch it reconvert.",
        ],
        "faqs": [
            ("How are commas inside values handled?",
             "Properly - cells wrapped in double quotes keep their commas, and doubled quotes inside quoted cells become literal quotes (the CSV escaping rule). Only unquoted commas split cells, which is exactly how standards-compliant CSV parsers behave."),
            ("How do numbers become JSON numbers?",
             "Cells matching a numeric pattern (optional sign, digits, decimal, scientific notation) are emitted unquoted and become real JSON numbers; everything else stays a string. Need '123' as a string? Quote it in the CSV or fix it after - the note line counts what was typed."),
            ("Does it detect semicolon or tab delimiters?",
             "Yes - the header row is scanned for commas, semicolons and tabs, and the most frequent wins. European Excel exports (semicolon CSVs) and TSVs paste straight in; the delimiter stat shows what was detected."),
            ("Is my data uploaded anywhere?",
             "No - parsing happens in your browser with zero network calls, the same guarantee as every text tool here. For customer lists and financial exports, local-only is not a feature, it is the requirement."),
        ],
    })

    pages.append({
        "slug": "online-timer",
        "title": "Online Timer — Free Countdown Timer Minutes:Seconds with Beep",
        "h1": "Online Timer",
        "desc": "Free online countdown timer with presets (1-60 min), tab-title live countdown and a three-beep alarm at zero. Accurate wall-clock timing, no sign-up.",
        "category": "countdown",
        "keyword": "online timer",
        "tool": "onlinetimer",
        "args": {},
        "intro": [
            "A web timer should do three things well: start instantly, keep perfect time in a background tab, and get your attention when it ends. This one measures elapsed time from the system clock rather than counting ticks, so tab throttling cannot drift it - a 25-minute pomodoro finishes in 25 real minutes. At zero it plays three beeps and flips the tab title to an alarm, so you notice it even from another window.",
            "Type minutes and seconds or hit a preset chip (1, 3, 5, 10, 15, 25, 45, 60), press Start, and glance at the tab title anytime - the remaining time lives there, which is the whole point of a timer you are not watching. Your last duration is remembered for the next session, and a share link carries the exact time you configured, so 'start a 10 minute timer' is one message to a friend or a class.",
        ],
        "howto": [
            "Set minutes and seconds, or tap a preset chip for common durations.",
            "Press Start - the tab title becomes a live countdown you can watch from any window; Pause and Reset are one keypress away.",
            "At zero: three beeps sound and the title switches to an alarm. Share button sends the exact timer as a link.",
        ],
        "faqs": [
            ("Is the timer accurate in a background tab?",
             "Yes - each refresh recomputes remaining time as end-time minus the system clock, instead of trusting that setInterval fired on schedule. Background tabs throttle timers to roughly once per minute, but wall-clock math is immune: the display might refresh late, the finish moment never moves."),
            ("Does it make a sound at zero?",
             "Three 880 Hz beeps via the Web Audio API - no audio files, no autoplay restrictions to fight because sound only plays after you clicked Start. The tab title also flips to an alarm message, covering muted devices and silent mode."),
            ("Can I use it for pomodoro or workout intervals?",
             "Presets cover the classics - 25 minutes for pomodoro focus blocks, 45 for long sessions, 5 for short breaks, 3 and 1 for planks and rest intervals between sets. The remembered-last-duration feature means repeat intervals are two clicks: preset, Start."),
            ("Does it work offline or without an account?",
             "No account, no install - it is a plain page that runs entirely in your browser, and once loaded it keeps working with no network at all. Bookmark it and your duration settings follow you on this device."),
        ],
    })

    pages.append({
        "slug": "stopwatch",
        "title": "Online Stopwatch with Laps — Free, Accurate to 10ms",
        "h1": "Stopwatch",
        "desc": "Free online stopwatch with lap splits, 10ms precision and a live tab-title display. Keeps running through reloads - no sign-up, no install.",
        "category": "countdown",
        "keyword": "online stopwatch, lap timer",
        "tool": "stopwatch",
        "args": {},
        "intro": [
            "Stopwatches fail in two familiar ways: they drift in background tabs, and they reset when the page reloads. This one fixes both - elapsed time comes from timestamp arithmetic (start time plus accumulated time, never tick counting), and the running state persists to local storage, so an accidental refresh mid-run restores the stopwatch still running with its laps intact.",
            "Lap records both the split and the cumulative total, which is what you actually need for interval training, brewing timers, lab work or timing speakers. While running, the tab title shows elapsed time, letting you monitor a run from another window. Precision is 10 milliseconds - honest, since browser rendering rarely justifies more.",
        ],
        "howto": [
            "Press Start; the display and the tab title begin counting immediately.",
            "Press Lap at each split - laps list both split time and running total; Stop freezes, Start resumes without zeroing.",
            "Reset clears everything. Reload the page mid-run and the stopwatch comes back still running.",
        ],
        "faqs": [
            ("How precise is it?",
             "10 milliseconds, shown as hundredths. Under the hood it uses millisecond timestamps, so timing is accurate to the clock; the display simply rounds to hundredths - the same resolution physical stopwatches advertise."),
            ("What happens if I reload or close the tab?",
             "Reload mid-run: state restores and timing continues seamlessly, because elapsed time is computed from the saved start timestamp. Close the tab entirely: the frozen total is remembered, and reopening the page shows the stopped stopwatch where you left it."),
            ("How do lap splits work?",
             "Each Lap press stores the time since the previous lap (the split) and since Start (the total). For a 4x400 workout that means you see each lap's own time and the session total - no manual subtraction."),
            ("Can I time something while using other apps?",
             "Yes - that is the tab-title feature. Switch windows and the running time stays visible in the browser tab; throttling may refresh it at one-second steps in the background, but the underlying timestamp math stays exact."),
        ],
    })

    pages.append({
        "slug": "stock-average-calculator",
        "title": "Stock Average Calculator — Average Down Cost Basis Instantly",
        "h1": "Stock Average Down Calculator",
        "desc": "Add shares at a new price and see your blended average cost, total invested and how far the break-even bar moved. Free, instant, no sign-up.",
        "category": "calculator",
        "keyword": "stock average calculator",
        "tool": "stockavg",
        "args": {},
        "intro": [
            "Averaging down is the most common trade in investing and the least often computed: you own 100 shares at $50, the stock drops to $35, and buying another 100 lands your break-even at $42.50 - not $35, and not the midpoint either. This calculator does that blend instantly, plus the totals that decide whether the add is wise: combined shares, combined capital in the position, and how much the average actually moved.",
            "The honest number here is break-even. Averaging down does not un-buy your expensive shares - it re-weights them - so the note under the result states the new bar plainly and what it does and does not fix. Your inputs are remembered for scenario testing, results land in the tab title, and one tap shares the full position via a link that carries the numbers.",
        ],
        "howto": [
            "Enter the shares you own and the average price you paid.",
            "Enter the size and price of the new buy.",
            "Read the blended average, total invested and the new break-even - tweak numbers to compare scenarios.",
        ],
        "faqs": [
            ("How is the new average cost calculated?",
             "Total dollars invested divided by total shares owned: (old shares × old price + new shares × new price) ÷ total shares. On 100 @ $50 plus 100 @ $35 that is $8,500 ÷ 200 = $42.50. The weighted blend is always between the two prices, closer to whichever buy was bigger."),
            ("Does averaging down lower my break-even?",
             "It lowers it toward the new price, never to it. Each add pulls the average closer to that add's price in proportion to its size - which is why the calculator shows 'average lowered by' as a percentage: the move from $50 to $42.50 is real relief, but the shares bought at $50 are still underwater until the stock passes $42.50."),
            ("Is averaging down a good idea?",
             "It is a bet that the thesis is intact and the drop is noise - the math is neutral, the judgment is yours. What the numbers do show is position sizing: the second buy raises your capital at risk to $8,500 in the example. Decide the total you are willing to own before the first buy, not after the drop."),
            ("Does it work for averaging up or crypto/forex?",
             "Yes - the formula only cares about shares and prices, so averaging up into strength works identically, and units of any asset (coins, lots, ETFs) calculate the same. Fees are not modeled; add them mentally to the new buy's price if they are material."),
        ],
    })

    pages.append({
        "slug": "position-size-calculator",
        "title": "Position Size Calculator — Risk %, Stop Loss & R:R for Any Trade",
        "h1": "Position Size Calculator",
        "desc": "Enter account size, risk %, entry and stop to get your exact position size, stop distance, position value and reward:risk. Free, no sign-up.",
        "category": "calculator",
        "keyword": "position size calculator",
        "tool": "possize",
        "args": {},
        "intro": [
            "The first question of every trade is not what to buy but how much: a $10,000 account risking 1% on a stock at $50 with a stop at $47.50 can buy 40 shares - not 41, because 41 would risk $1,025 and break the rule. This calculator runs that arithmetic live: risk dollars from your percentage, stop distance from entry to stop, shares rounded down so reality stays inside the plan.",
            "Add an optional target and it completes the trade plan with reward:risk - the one number that tells you whether the setup is worth taking at all. Inputs are remembered between visits, results show in the tab title while you work, and the share link carries every field so a trading buddy can check your sizing.",
        ],
        "howto": [
            "Enter your account size and the percent you are willing to lose on the trade.",
            "Enter entry price and stop loss - the position size appears immediately.",
            "Optionally add a target price to see the reward:risk before you commit.",
        ],
        "faqs": [
            ("How is position size calculated?",
             "Risk dollars ÷ per-share risk: ($10,000 × 1%) ÷ ($50 − $47.50) = $100 ÷ $2.50 = 40 shares. Position value is those shares × entry ($2,000 here) - notice it can dwarf your risk: you control $2,000 to risk $100, which is exactly why the stop must exist before the size is computed."),
            ("Why are shares rounded down?",
             "Fractional risk compounds: 41 shares at a $2.50 stop risks $102.50, breaking a 1% rule on a $10,000 account. Rounding down keeps actual risk at or under your chosen percentage - the note states the rounding explicitly rather than hiding it in a decimal."),
            ("What risk percentage should I use?",
             "Most systematic traders use 0.5-2% per trade: at 1%, ten straight losses cost about 9.6% of the account and survivable; at 10%, the same streak is a 65% drawdown. The percentage is a business decision, not a math constant - the calculator just enforces whatever you pick."),
            ("Does it work for forex, futures or crypto?",
             "Yes - 'shares' means units of whatever you trade: crypto coins work directly per-unit; for forex lots or futures contracts, compute per-unit risk from your tick value first, or divide the position value by your broker's contract size. The risk-first order of operations is identical in every market."),
        ],
    })

    pages.append({
        "slug": "lottery-odds-calculator",
        "title": "Lottery Odds Calculator — Jackpot Odds, EV & Break-even Jackpot",
        "h1": "Lottery Odds Calculator",
        "desc": "Exact jackpot odds for Powerball, Mega Millions and EuroMillions, plus expected value per ticket and the jackpot that would break even. Free, no sign-up.",
        "category": "calculator",
        "keyword": "lottery odds calculator",
        "tool": "lotto",
        "args": {},
        "intro": [
            "Every lottery advertisement quotes the jackpot; none quotes what the ticket is mathematically worth. This calculator does: pick a game and a jackpot, and it computes the exact jackpot odds from the combinatorics (Powerball's 1 in 292,201,338 is not a marketing number - it is 69-choose-5 times 26), the expected value per $2 ticket, and the jackpot at which the ticket would stop being a guaranteed loss.",
            "That break-even number is the punchline: with only jackpot dollars counted, Powerball's ticket price is not covered until the jackpot reaches roughly $584 million - and taxes, the lump-sum discount and shared jackpots push the true bar far higher. The note under the result keeps score honestly, which is exactly what makes this a better answer than a bare odds table.",
        ],
        "howto": [
            "Pick a game - or choose Custom and enter your local lottery's number format.",
            "Enter the current jackpot; odds and per-ticket EV update instantly.",
            "Read the break-even jackpot - the headline number your ticket is actually competing against.",
        ],
        "faqs": [
            ("How are the jackpot odds computed?",
             "Combinatorics, live: the chance of matching 5 main numbers from 69 is 69-choose-5 = 11,238,513, multiplied by 26 bonus balls = 292,201,338. Mega Millions and EuroMillions use their own pools, and EuroMillions draws two lucky stars, so its bonus term is 12-choose-2 = 66. Custom mode runs the same formula on your numbers."),
            ("What is expected value per ticket?",
             "Jackpot ÷ odds - the average the jackpot line alone pays per ticket. A $500M Powerball jackpot pays about $1.71 per $2 ticket from the top prize; smaller tiers add roughly $0.20-0.35 more. Until the jackpot crosses the break-even, every ticket is mathematically underwater before a ball is drawn."),
            ("Why is the real break-even even higher?",
             "Three haircuts: federal (and state) taxes take roughly half, the advertised jackpot is an annuity whose lump-sum option is about 60% of the headline, and jackpots that big are commonly split. The calculator shows the no-haircut bar because it is the honest floor - reality is meaningfully worse."),
            ("Doesn't buying more tickets improve my odds?",
             "Linearly and uselessly: 2 tickets halve the odds to 1 in 146 million - a rounding error on a number that size. The only strategy the math rewards is picking unpopular numbers to avoid splitting a won jackpot, and even that cannot push expected value positive at normal jackpots."),
        ],
    })

    pages.append({
        "slug": "pomodoro-timer",
        "title": "Pomodoro Timer Online — 25/5 Focus Cycles with Tab Countdown",
        "h1": "Pomodoro Timer",
        "desc": "Free online pomodoro timer: 25/5 focus cycles, long break every fourth round, live tab-title countdown and a daily focus-streak counter. No sign-up.",
        "category": "countdown",
        "keyword": "pomodoro timer",
        "tool": "pomodoro",
        "args": {},
        "intro": [
            "The pomodoro method is 25 minutes of focus, 5 minutes off, and a longer break every fourth cycle - simple to describe, easy to abandon, because most timers make you babysit them. This one runs the whole protocol: it cycles through focus and break phases automatically, beeps at each transition, and keeps the countdown in the browser tab title so it stays visible while you work in other windows.",
            "It also keeps score: completed focus blocks and focus minutes accrue per day, survive a reload mid-session, and are there when you come back tomorrow - the counter that quietly asks whether today was a zero-focus day. Durations are adjustable, and the timing math runs on wall-clock timestamps, so background-tab throttling cannot make your 25 minutes drift.",
        ],
        "howto": [
            "Set your focus and break lengths (25/5/15 works; 50/10 also has fans).",
            "Press Start - work until the beep, rest when it says break, repeat.",
            "Come back tomorrow: today's focus-block count is waiting, reset to zero.",
        ],
        "faqs": [
            ("What is the pomodoro technique?",
             "A time-boxing method by Francesco Cirillo: 25-minute focus blocks separated by 5-minute breaks, with a 15-30 minute break after every fourth block. The box is the point - a hard edge makes starting easy and makes 'one more scroll' a visible violation of your own timer."),
            ("Does it keep running if I switch tabs?",
             "Yes - elapsed time is computed from wall-clock timestamps, not counted ticks, so browser throttling of background tabs cannot slow it. The tab title carries a live countdown, which is how most people keep it visible from another window."),
            ("What happens if I close the page mid-session?",
             "The phase in progress is lost, but your day is not: completed focus blocks and minutes are stored per date and reappear when you reload. Rigid timers punish real life; this one only asks that the daily count stay honest."),
            ("Can I change 25/5 to something else?",
             "Yes - focus, short break and long break are all adjustable, and the long break fires automatically after every fourth focus block. Common variants: 50/10 for deep work, 15/3 for rough days. The method serves you, not the reverse."),
        ],
    })

    pages.append({
        "slug": "password-strength-checker",
        "title": "Password Strength Checker — Entropy Bits & Crack Time, Nothing Stored",
        "h1": "Password Strength Checker",
        "desc": "Test a password's entropy and realistic crack times against online, GPU and datacenter attacks - computed locally, never stored or sent. Free, no sign-up.",
        "category": "calculator",
        "keyword": "password strength checker",
        "tool": "passstrength",
        "args": {},
        "intro": [
            "'Strong password' is useless advice without a number. This checker gives two: entropy in bits (length × log₂ of the character pool you actually used) and what those bits mean in practice - how long the password survives a throttled online attack, a single gaming GPU, or a well-funded datacenter. Dictionary words, keyboard patterns, repeats and date-shaped tails are detected and deducted, because crackers try them first and brute-force math flatters them.",
            "The privacy bar is absolute: nothing you type is stored, remembered or sent anywhere - there is deliberately no URL state and no input memory on this tool, because a password must never persist. The note under the result explains why length beats symbol soup and why reuse is the real breach multiplier.",
        ],
        "howto": [
            "Type (not paste from your manager, for this test) a candidate password.",
            "Read the entropy bits, the verdict and the three attack-scenario times.",
            "Adjust: doubling length beats adding a symbol every time - test and see.",
        ],
        "faqs": [
            ("How is password strength measured?",
             "Entropy: each character adds log₂(pool size) bits - lowercase-only adds 4.7 bits per character, mixed case+digits+symbols adds about 6.5. A 12-character random lowercase password (~56 bits) beats 'P@ss1!' (~33 bits) comfortably, which is why the verdict follows the math and not the aesthetics."),
            ("What do the crack-time estimates assume?",
             "Three honest rates: ~100 guesses/second against a rate-limited login form, 10^10/s for an offline GPU cracking a stolen hash, and 10^14/s for warehouse-scale hardware. Real cracking is dictionary-guided and uneven, which is exactly why the pattern deductions exist."),
            ("Why does 'Password1!' score badly when it's complex?",
             "Complexity rules check character classes, crackers check dictionaries first - and 'password' with a suffix is the most-guessed pattern in every breach dump. The checker normalizes leetspeak (0→o, 3→e, @→a) before its word list, so cosmetic substitutions do not buy back security."),
            ("Does this tool store or transmit what I type?",
             "No - deliberately. The entropy math runs in your browser; there is no input memory, no share-with-data link and no network call on this page, and the share button sends only your score. The one habit no checker can fix is reuse, so rotate passwords between sites or use a manager."),
        ],
    })

    pages.append({
        "slug": "crypto-profit-calculator",
        "title": "Crypto Profit Calculator — Net P/L, ROI & Break-even After Fees",
        "h1": "Crypto Profit Calculator",
        "desc": "Calculate real crypto profit after exchange fees on both sides: net P/L, ROI, total invested and the exact break-even sell price. Free, no sign-up.",
        "category": "calculator",
        "keyword": "crypto profit calculator",
        "tool": "cryptoprofit",
        "args": {},
        "intro": [
            "Most crypto profit calculators subtract entry from exit and call it done - which quietly ignores the fee that both sides of every trade pay. Buy $30,000 of Bitcoin at 0.1% and you received $29,970 of exposure; sell at 'break-even' and the exit fee closes the round trip $60 in the hole. This calculator fees both sides explicitly and derives the number that actually matters: the sell price at which you are truly flat.",
            "From there it is honest P/L: net profit, ROI on capital-at-risk including the buy-side fee, and a note that keeps the long-run picture visible - fees compound with trade frequency, which is how active traders silently give back double-digit percentages a year. Inputs are remembered, results land in the tab title, and the share link carries the whole scenario.",
        ],
        "howto": [
            "Enter buy price, sell price and quantity - profit appears with default fees.",
            "Set your exchange's per-side fee (0.1-0.5% is typical for spot).",
            "Read net P/L, ROI and break-even - then try the fee the spread really costs you.",
        ],
        "faqs": [
            ("How is break-even calculated?",
             "Break-even sell price = buy price × (1 + fee) ÷ (1 − fee). At 0.1% per side that is 0.2% above your entry: buy at $60,000 and the trade is only whole at $60,120.1. The formula compounds both fee directions, which is why it is slightly larger than the naive entry × (1 + 2×fee)."),
            ("Do the fees include spread and slippage?",
             "No - the fee field models the exchange's commission only. The spread on illiquid pairs and slippage on market orders are real costs too; many traders fold them in by raising the fee percent until it matches their all-in cost, and the calculator updates break-even live."),
            ("Does it work for any coin or only Bitcoin?",
             "Any asset priced per unit: ETH, SOL, DOGE, gold ounces, or fractional coins - quantity takes decimals, so 0.5 BTC works exactly like 500 DOGE. Leverage, funding rates and tax lots are out of scope; this is the spot round-trip, modeled precisely."),
            ("Is profit before or after tax?",
             "Before - crypto disposals are taxable events in most jurisdictions, and short-term rates apply to trades held under a year. The note keeps the trading-cost picture honest; for the tax picture, your jurisdiction's rules on cost basis and holding periods apply on top."),
        ],
    })

    pages.append({
        "slug": "dog-age-calculator",
        "title": "Dog Age Calculator — Real Human Years by Breed Size, Not ×7",
        "h1": "Dog Age Calculator",
        "desc": "Convert your dog's age to human years with the size-aware veterinary table - and see why the ×7 rule fails. Free, instant, no sign-up.",
        "category": "calculator",
        "keyword": "dog age calculator",
        "tool": "petagedog",
        "args": {},
        "intro": [
            "The 'one dog year equals seven human years' line falls apart the moment you look at a one-year-old lab: no seven-year-old child has finished growing, run a full heat cycle, or trained up to off-leash reliability. Veterinary growth tables tell the real story - dogs burn through roughly 15 human years in their first year, hit their mid-twenties by two, then add about four to five human years per calendar year, with large breeds aging measurably faster than small ones.",
            "This calculator applies those tables with the size correction your dog needs, then adds the two numbers that make it useful: a life-stage label and an estimate of how much of a typical lifespan your dog has lived - the number that quietly decides when senior screening bloodwork should start. Save your dog's age once and the next check is a two-tap affair.",
        ],
        "howto": [
            "Enter your dog's age in years and months.",
            "Pick the size bucket - small, medium or large - since big dogs age faster.",
            "Read the human-equivalent age, life stage and lifespan estimate.",
        ],
        "faqs": [
            ("Why isn't multiplying by 7 accurate?",
             "Because dogs don't age linearly. Year one delivers about 15 human years of development (a 1-year-old dog can reproduce and is skeletally mature), year two adds ~9 more, and each later year is worth roughly 4-5 human years - more for large breeds. The ×7 rule averages that curve into a straight line and misses both ends."),
            ("Why does breed size change the answer?",
             "Large dogs age faster and die younger - a Great Dane is a senior at 6 while a Chihuahua is middle-aged at 10, roughly inverted from the usual body-size rule in mammals. The calculator's three size buckets adjust both the yearly aging rate and the lifespan estimate accordingly."),
            ("Is the '16 × ln(age) + 31' formula better?",
             "It comes from a 2020 epigenetic study of Labradors' DNA methylation, and it's a lovely single-line approximation for adult dogs - but it knows nothing of breed size and gets the first year wrong. The veterinary growth tables used here stay close to it for adults while handling puppies and size classes honestly."),
            ("When should my dog be considered a senior?",
             "Small dogs around 10-11, medium around 8-9, large around 6-7 calendar years - which is why the human-equivalent number matters more than the calendar one: screenings (bloodwork, joint checks) should start when your dog is roughly human mid-40s to 50s, not when an arbitrary label flips."),
        ],
    })

    pages.append({
        "slug": "cat-age-calculator",
        "title": "Cat Age Calculator — Calendar Age to Human Years, Life Stage",
        "h1": "Cat Age Calculator",
        "desc": "Convert your cat's age to human years with the veterinary table, plus life stage and lifespan context. Free, instant, no sign-up.",
        "category": "calculator",
        "keyword": "cat age calculator",
        "tool": "petagecat",
        "args": {},
        "intro": [
            "Cats compress a whole childhood into their first year: a 1-year-old cat is roughly a 15-year-old human - sexually mature, fully mobile and confident about it. Year two brings them to their mid-twenties, and from there the pace settles to about four human years per calendar year, slower than dogs and far slower than the mythic ×7.",
            "This calculator runs the veterinary association table for any age down to the month, labels the life stage, and estimates the share of a typical 15-year lifespan your cat has lived - useful mostly as a nudge about the other end of the curve: from about age 10, twice-yearly vet visits are the single highest-yield habit an indoor cat's human can keep.",
        ],
        "howto": [
            "Enter your cat's age in years and months (kittens included).",
            "Read the human-equivalent age and life stage instantly.",
            "Check the lifespan bar - then ask your vet when senior screening should start.",
        ],
        "faqs": [
            ("How old is 1 year in cat years?",
             "About 15 human years: by their first birthday, cats are the equivalent of a developed teenager - grown, fertile and coordinated. Two calendar years reach roughly 24 human years, and every year after adds about 4. There is no good origin for the ×7 myth; it fails for cats exactly as it does for dogs."),
            ("Do indoor cats really live longer?",
             "Meaningfully - indoor cats commonly reach 12-18, and quite a few pass 20, while outdoor cats average far lower due to traffic, fights and disease. The calculator uses 15 as the reference lifespan; a protected indoor lifestyle plus weight control is the two biggest levers an owner holds."),
            ("When is a cat a senior?",
             "Around 10-11 calendar years, which lands near a human's late 50s. Cats are champions at hiding illness - weight loss, thirst changes and litter-habit shifts are the tells - so from age 10 the standard advice shifts to twice-yearly checkups with bloodwork."),
            ("Does the same chart work for kittens and big cats?",
             "The table covers kittens from birth (months included) through geriatric housecats; big cats - lions, tigers - mature on different curves and don't belong on a housecat chart. For the first six months the calculator falls back to a simple growth approximation, since even vet tables are coarse there."),
        ],
    })

    pages.append({
        "slug": "flesch-reading-ease-calculator",
        "title": "Flesch Reading Ease Calculator — Score Text, Grade Level, Live",
        "h1": "Flesch Reading Ease Calculator",
        "desc": "Paste text and get its Flesch Reading Ease score, grade level, sentence stats and what they mean - computed locally as you type. Free, no sign-up.",
        "category": "text",
        "keyword": "flesch reading ease calculator",
        "tool": "flesch",
        "args": {},
        "intro": [
            "The Flesch Reading Ease score is the number behind 'write for an 8th-grade reading level': 206.835 minus 1.015 times average sentence length minus 84.6 times average syllables per word. It powers readability checks in Word, in SEO tools and in government plain-language laws - and this calculator computes it live as you type, with the grade level beside it, so you can watch a rewrite push the number up in real time.",
            "The stat that moves the score most surprises people: words per sentence is weighted 1.015 while syllables per word gets 84.6 ÷ (words × words) - practically, cutting a sentence in half moves the needle more than swapping every long word. Your text stays in the browser (nothing is uploaded), is remembered between visits up to a cap, and the share button sends the score, not the essay.",
        ],
        "howto": [
            "Paste a paragraph, email, essay or article intro into the box.",
            "Read the score, grade level and words-per-sentence as you type.",
            "Rewrite a sentence shorter and watch the score move - then aim for 60-70.",
        ],
        "faqs": [
            ("What is a good Flesch Reading Ease score?",
             "60-70 is the standard target - 'plain English', roughly 8th-9th grade - and most mass-audience publications sit between 50 and 70. Reader's Digest famously runs in the 60s-80s, academic and legal writing falls below 30, and that's appropriate there: the score measures effort to read, not quality of thought."),
            ("How is the score calculated?",
             "Flesch Reading Ease = 206.835 − 1.015 × (words ÷ sentences) − 84.6 × (syllables ÷ words). This tool counts sentences by terminal punctuation and syllables with a standard vowel-group heuristic (silent 'e' dropped, 'y' as a vowel), the same approach classroom calculators use; scores can differ by a point or two from Word's tokenizer."),
            ("How do I raise my score?",
             "Cut sentences first - splitting a 40-word sentence into two 20-word sentences is worth about 10 points, more than de-syllabifying the same text. Then prefer the short word where it exists naturally. What not to do: pad sentences with 'and' to lower average length; the grade-level check will catch the fraud."),
            ("Is my text uploaded or stored anywhere?",
             "No network calls happen - scoring runs entirely in your browser. Your text is kept in this browser's local storage (capped at 20,000 characters) so a revision session survives a reload; clear the box and it's gone, and the share button transmits only the score."),
        ],
    })

    pages.append({
        "slug": "dew-point-calculator",
        "title": "Dew Point Calculator — Real Mugginess from Temperature & Humidity",
        "h1": "Dew Point Calculator",
        "desc": "Turn temperature and relative humidity into dew point with a comfort verdict - the honest 'it's not the heat' number. Free, instant, no sign-up.",
        "category": "calculator",
        "keyword": "dew point calculator",
        "tool": "dewpoint",
        "args": {},
        "intro": [
            "Relative humidity is the most misleading number in the weather app: 70% humidity at 15°C is a crisp autumn day, while 70% at 30°C is a swamp - the same percentage, completely different air. The dew point cuts through it by stating the actual water vapor content: the temperature at which that air would saturate. Meteorologists read comfort straight off it, and this calculator runs the Magnus formula the moment you type.",
            "The comfort bands under the result are the ones forecasters actually use - below 10°C dry, 10-16 comfortable, 16-21 noticeable, 21-24 muggy, and past 24 oppressive - plus a stat most tools skip: the temp-dew-point spread, which tells you how close fog or overnight dew is. Your last inputs are remembered, the result lands in the tab title, and the share link carries the whole reading.",
        ],
        "howto": [
            "Pick °C or °F, then enter air temperature and relative humidity.",
            "Read the dew point and its comfort verdict instantly.",
            "Watch the temp-dew-point spread - when it nears zero, fog and dew are close.",
        ],
        "faqs": [
            ("Why is dew point better than relative humidity?",
             "Relative humidity is water vapor relative to what the air could hold at its current temperature - so it changes with temperature even when the moisture doesn't. Dew point measures the moisture itself: a 20°C dew point means the same sticky air in Dallas or Delhi. That's why pilots and meteorologists track dew point, not RH."),
            ("What dew point feels muggy?",
             "Most people: below 10°C dry, 10-16 comfortable, 16-21 noticeable, 21-24 muggy, 24+ oppressive. Past about 26-28°C even resting in shade is miserable, because sweat stops evaporating efficiently once the dew point nears skin temperature - evaporation is the only cooling your body has."),
            ("How is dew point calculated?",
             "The Magnus approximation, the same one in most weather station firmware: dew point = 243.12·γ ÷ (17.62 − γ), where γ = ln(RH/100) + 17.62·T ÷ (243.12 + T). Accurate to a fraction of a degree across normal weather; the calculator also converts the result to absolute humidity in g/m³."),
            ("What does it mean when dew point equals air temperature?",
             "The air is saturated - 100% relative humidity - and any further cooling forces water out: dew on grass, fog in the air, clouds in the sky. The 'spread' stat shows how close you are; pilots use the same spread to predict morning fog at their destination."),
        ],
    })

    pages.append({
        "slug": "btu-calculator",
        "title": "BTU Calculator — AC Size by Room, Insulation, Sun & Occupancy",
        "h1": "BTU Calculator",
        "desc": "Size your air conditioner properly: room area, ceiling, insulation, sun, people and kitchen adjustments give BTU, kW and tons of cooling. Free, no sign-up.",
        "category": "calculator",
        "keyword": "btu calculator",
        "tool": "btucalc",
        "args": {},
        "intro": [
            "Air conditioner sizing is the classic 'bigger must be better' trap - and it's wrong in both directions. An undersized unit runs flat-out on hot afternoons and never pulls humidity down; an oversized one cools the air in five minutes, shuts off before it dehumidified anything, and leaves the room cold-but-clammy while short-cycling the compressor to death. The right number comes from area, ceiling height, insulation, sun, people and what appliances share the room.",
            "This calculator starts from the 20 BTU per square foot rule of thumb, scales it for ceiling volume, then applies honest adjustments - poor insulation +15%, heavy sun +10%, +600 BTU per person past the second, +4,000 for kitchens - and reports the result three ways: BTU, kW and tons, so it matches whatever label your local seller uses. Inputs are remembered for the next room in the house.",
        ],
        "howto": [
            "Enter room area and ceiling height.",
            "Set insulation, sun exposure, usual occupancy and whether it's a kitchen.",
            "Match the BTU (or kW / tons) figure to the unit's cooling rating, not its size.",
        ],
        "faqs": [
            ("How many BTU do I need per square meter?",
             "About 215 BTU per m² (20 per sq ft) with a standard 2.7 m ceiling as the starting point - then adjust up for sun, poor insulation, many occupants or kitchen heat, and down for shade and tight modern construction. A 20 m² bedroom lands near 5,000-6,000 BTU; a sunny 40 m² living room near 12,000-14,000."),
            ("What happens if the AC is too big?",
             "It short-cycles: the compressor satisfies the thermostat before it has run long enough to dehumidify, leaving a cold, clammy room and doubling on/off wear. Humidity removal - half of comfort - happens in the long, steady runs that oversized units never get. Oversizing wastes money twice: at purchase and in lifetime."),
            ("Are kW and tons different from BTU?",
             "Same quantity, different labels: 12,000 BTU/h = 1 ton = about 3.5 kW of cooling. Regions differ in habit - the US sells by BTU, much of Asia by 'HP' or kW, HVAC pros by tons - which is why the calculator shows all three for the same sized unit."),
            ("Does this work for heating with a heat pump?",
             "The room-loss logic transfers, but heating loads are usually quoted separately and depend more on climate and insulation than cooling does. Size for whichever season dominates your bill, and remember heat pump ratings list cooling and heating capacities separately - match the right column."),
        ],
    })

    pages.append({
        "slug": "tire-size-comparison",
        "title": "Tire Size Comparison — Speedometer Error, Diameter & Fit Check",
        "h1": "Tire Size Comparison",
        "desc": "Compare two tire sizes before you buy: diameter change, speedometer error at 100 km/h, revs per mile and a ±3% fitment verdict. Free, no sign-up.",
        "category": "calculator",
        "keyword": "tire size comparison calculator",
        "tool": "tire",
        "args": {},
        "intro": [
            "A tire size like 225/45-17 is a formula, not a name: 225 mm of width, a sidewall that is 45% of that width, on a 17-inch rim. Put those three numbers in the diameter equation and you can predict everything that matters before the tires are mounted - how much taller the new setup sits, what your speedometer will read when you're actually doing 100, and whether the odometer just started lying to you.",
            "This calculator runs the comparison live and adds the verdict that tire shops argue about: the ±3% rule. Stay inside it and gearing, ABS, ESP and rub clearances stay within what your car was engineered for; drift outside and the note explains exactly which problems you've signed up for. It's the math behind why plus-sizing pairs a bigger rim with a smaller aspect ratio - and why some swaps simply don't work.",
        ],
        "howto": [
            "Enter your current size from the sidewall (e.g. 225/45-17) as the baseline.",
            "Enter the size you're considering.",
            "Check the diameter change, speedometer reading and the ±3% fitment verdict.",
        ],
        "faqs": [
            ("How do I calculate tire diameter from the size?",
             "Diameter in mm = rim inches × 25.4 + 2 × (width × aspect ÷ 100). For 225/45-17: sidewall is 225 × 0.45 = 101 mm, so diameter = 431.8 + 202.5 ≈ 634 mm. Compare diameters between sizes and everything else - speedo error, clearance, revs per mile - follows from that single ratio."),
            ("Will bigger tires mess up my speedometer?",
             "Yes, proportionally: speedo reads a percentage based on rolling diameter, so a +3% taller tire makes it read 97 when you're doing 100. The calculator shows the exact reading at 100 km/h for your swap. Odometer drifts the same way - enough to matter for leases and fuel logs."),
            ("What is the ±3% rule?",
             "A practical industry guideline: keep total diameter within about ±3% of the factory size so gearing, braking, ABS/ESP calibration, and body or fender clearance stay within design tolerances. Beyond that you're into rub-on-full-lock territory, speedometer correction, or insurance questions - sometimes all three."),
            ("Why do people put bigger rims with thinner tires?",
             "To keep the total diameter constant while filling the arch with more wheel: a plus-one or plus-two swap increases rim inches but steps the aspect ratio down so the sidewall shrinks by the same amount. The math only works if the sum holds steady - which is exactly what this comparison checks before you spend money."),
        ],
    })

    pages.append({
        "slug": "heart-rate-zones-calculator",
        "title": "Heart Rate Zones Calculator — Karvonen & %Max Training Bands",
        "h1": "Heart Rate Zones Calculator",
        "desc": "Get your five training heart rate zones from age and resting HR - Karvonen reserve method or classic % of max, with honest formula caveats. Free.",
        "category": "calculator",
        "keyword": "heart rate zones calculator",
        "tool": "hrzone",
        "args": {},
        "intro": [
            "Training zones turn 'go for a run' into a dosage: Z1 recovery, Z2 aerobic base, Z3 tempo, Z4 threshold, Z5 VO2max - five bands with five different jobs. The catch is that every watch and wall chart computes them differently, and the two mainstream formulas disagree: % of max gives everyone the same bands, while the Karvonen method scales by heart rate reserve (max − resting) and hands trained hearts genuinely higher working zones for the same effort.",
            "This calculator runs both, side by side with your resting heart rate factored in where it belongs, and keeps the honesty column open: 220 − age is a population average with over ±10 bpm of scatter on any individual. Your zones are remembered, shown in the tab title mid-workout, and shareable as a link that carries your settings.",
        ],
        "howto": [
            "Enter your age and, if you know it, your resting heart rate.",
            "Pick Karvonen (reserve-based) or classic % of max.",
            "Train to the bands: most of your week belongs in Z2, and that's the one people skip.",
        ],
        "faqs": [
            ("What are the 5 heart rate zones?",
             "Z1 recovery (50-60%): warm-ups and flush-outs. Z2 aerobic base (60-70%): the conversational mileage that builds mitochondria - most of a training week lives here. Z3 tempo (70-80%): comfortably hard. Z4 threshold (80-90%): the effort you could hold for about an hour. Z5 VO2max (90-100%): intervals, minutes at a time."),
            ("Which formula is better, Karvonen or % of max?",
             "Karvonen is physiologically fairer: it measures intensity relative to your usable range (reserve) rather than to a fixed max, so a fit athlete with a 45 bpm resting rate gets zones that reflect their engine. % of max wins only on convenience - no resting HR needed. Both inherit the 220 − age error."),
            ("How accurate is 220 minus age?",
             "It is a 1971 population regression with no error bars on the wall chart: individual max HR at a given age scatters by more than ±10 bpm, and the formula drifts for older athletes. Tanaka's 208 − 0.7 × age fits modern data better. A field-tested max (hard finish to a race) beats any formula - use the formula until you have one."),
            ("Should I train by heart rate or pace?",
             "Heart rate on hills, heat and tired days; pace on the flat and the track. HR drifts upward during long sessions (cardiac drift) and lags effort on intervals - so use zones to gate easy days and cap steady work, and use feel or pace for the sharp end. The best plan uses both loosely, not either rigidly."),
        ],
    })

    pages.append({
        "slug": "golf-handicap-calculator",
        "title": "Golf Handicap Calculator — WHS Differential & Course Handicap",
        "h1": "Golf Handicap Calculator",
        "desc": "Turn a scorecard into a World Handicap System differential, then into a course handicap for the next tee. Free, instant, no sign-up.",
        "category": "calculator",
        "keyword": "golf handicap calculator",
        "tool": "golf",
        "args": {},
        "intro": [
            "The World Handicap System made one number the currency of amateur golf: the differential, (113 ÷ slope) × (adjusted gross score − course rating). It is the only fair way to compare a 95 at a brute 74.8/140 course with a 95 at a friendly 69.9/113 one - and it is the raw material your index is made of, being the average of your best 8 differentials from the last 20 rounds.",
            "This calculator runs the differential from any scorecard in one line, then answers the question you actually have on the first tee: with your index entered, it gives the course handicap for today's rating and slope, the target score that counts as a 'handicap round', and whether today beat your index. Inputs are remembered for league night, and the share link carries your round.",
        ],
        "howto": [
            "Enter your adjusted gross score plus the course's rating and slope from the card.",
            "Add your handicap index and par to get today's course handicap.",
            "Play to par + course handicap - that's a net-even round on any course on earth.",
        ],
        "faqs": [
            ("How is a handicap differential calculated?",
             "Differential = (113 ÷ slope rating) × (adjusted gross score − course rating). The 113 is the baseline slope: shoot 95 from a 72.4 rating on a 128-slope course and your differential is (113/128) × 22.6 ≈ 19.9. Harder courses shrink the number, which is exactly the point."),
            ("How does my handicap index come from differentials?",
             "Your index is the average of your lowest 8 differentials from the most recent 20 acceptable rounds (fewer rounds use a scaled table), multiplied by 0.96 - a small nod toward your potential rather than your average. It updates as new scores post, which is why a great day shows up in your index within days."),
            ("What is a course handicap and why does it differ from my index?",
             "Course handicap = index × (slope ÷ 113) + (course rating − par). It converts your portable index into strokes for one specific set of tees on one specific course - more strokes on a harder-than-average layout, fewer on an easy one. It's the number you play with, not the number on your profile."),
            ("Does a disaster hole ruin the round's differential?",
             "No - the system caps every hole at net double bogey for handicap purposes ('adjusted gross score'), which is why the input says adjusted: pick up, take the cap, and one triple-quadruple costs you almost nothing in differential terms. The best-8-of-20 averaging handles the rest."),
        ],
    })

    pages.append({
        "slug": "bpm-delay-calculator",
        "title": "BPM Delay & Reverb Time Calculator — Synced Note Values in ms",
        "h1": "BPM Delay Calculator",
        "desc": "Convert any tempo into delay and reverb times: 1/4 note, dotted 1/8, triplets, bar length and LFO Hz - the producer's tempo-sync cheat sheet. Free.",
        "category": "calculator",
        "keyword": "bpm delay calculator",
        "tool": "bpmdelay",
        "args": {},
        "intro": [
            "Tempo-synced delay is one note of arithmetic: a quarter-note delay lasts 60,000 ÷ BPM milliseconds, and every other subdivision is a multiple of it. Set a plugin's time manually to those milliseconds and echoes land exactly between the notes - the dotted eighth that defines U2-style edge-of-chaos ambience, the triplet that swings, the one-bar wash that turns a vocal into a stadium. This calculator shows the whole family at once, live, from one field.",
            "It also answers the questions the delay table doesn't: how long a bar lasts (for reverb tails and loop lengths), and the modulation rate in Hz producers need when a plugin's LFO syncs by frequency instead of tempo - one LFO cycle per bar at your tempo, to three decimals. Your last tempo is remembered for the session, and the share link carries the BPM.",
        ],
        "howto": [
            "Enter your track's BPM.",
            "Read the delay time you need - quarter for on-beat echoes, dotted 1/8 for the classic push.",
            "Use the bar length for reverb tail decisions and the Hz value for LFO sync.",
        ],
        "faqs": [
            ("How do I calculate delay time from BPM?",
             "Quarter note in ms = 60,000 ÷ BPM. At 120 BPM that's 500 ms; a dotted eighth is 1.5× = 750 ms; an eighth triplet is ⅔ = 333 ms. Every subdivision is just a fraction or multiple of the quarter - the calculator lays them out so you can dial a number in instead of trusting tap tempo."),
            ("Why do producers love dotted eighth delays?",
             "Because echoes fall between the subdivisions, creating a rhythm that's locked to the track but sounds like it's floating - the Edge's guitar sound and half of ambient techno are dotted-eighth ping-pong delays. It reads as complexity while being mathematically perfectly in time."),
            ("What about reverb times - how long should a tail be?",
             "A workable rule: tail roughly equal to one bar (or one phrase) so washes resolve on the downbeat; for vocals, keep predelay at 10-30 ms so the dry signal stays in front, and use the bar-length stat to decide whether the tail fits the groove or blurs it. Ballads tolerate longer; anything uptight and fast wants shorter."),
            ("My plugin syncs by Hz, not tempo - what value do I use?",
             "Hz = BPM ÷ 60 ÷ (beats per cycle). One LFO cycle per bar of 4/4 is BPM ÷ 240 - at 120 BPM, 0.5 Hz. The calculator shows that figure to three decimals, which matters because tremolo and auto-pan drift becomes audible when the cycle slips even a few hundredths against the grid."),
        ],
    })

    pages.append({
        "slug": "ev-charging-cost-calculator",
        "title": "EV Charging Cost Calculator — Per Mile & vs Gas, Charging-Loss Aware",
        "h1": "EV Charging Cost Calculator",
        "desc": "Work out what your EV really costs per mile or km: battery, efficiency and your electricity rate - with an honest gas-car comparison. Free, no sign-up.",
        "category": "calculator",
        "keyword": "ev charging cost calculator",
        "tool": "evcharge",
        "args": {},
        "intro": [
            "The promise of cheap electric driving hides in three numbers: your battery's usable kWh, your real-world efficiency, and what your utility actually charges per kWh - and the difference between a 0.10 off-peak rate and a 0.40 public rapid is the difference between driving for pennies and paying more than a diesel. This calculator runs the honest per-mile figure from your own numbers, plus the full-charge cost that decides whether topping up at home beats the pump.",
            "The comparison column is where it gets satisfying: add a gas price and consumption and the note converts the per-unit saving into a yearly number at 12,000 units - the figure that actually wins arguments. The note also keeps one awkward truth visible: wall-to-battery charging losses run about 10% on Level 2 and worse on rapids, so the meter number and the battery number are not the same.",
        ],
        "howto": [
            "Enter your battery's usable kWh and efficiency (mi/kWh or kWh/100km).",
            "Enter your electricity rate - check your off-peak tariff, it changes everything.",
            "Optionally add gas price and consumption for the per-mile showdown.",
        ],
        "faqs": [
            ("How do I calculate EV cost per mile?",
             "Electricity rate ÷ efficiency: at $0.15/kWh and 4 mi/kWh, that is 3.75 cents per mile - about $450 a year at 12,000 miles. The same formula works in metric (rate × kWh/100km gives cost per km), and the calculator switches units cleanly so you can compare with what your gas car burns."),
            ("Why is my real charging bill higher than this?",
             "Charging losses: roughly 10% of the energy you pay for never reaches the battery on Level 2 (conversion heat, battery management), and DC fast charging wastes even more on top of costing 2-3× per kWh. The calculator shows the battery-math price; mentally add a tenth for home charging, more for rapids."),
            ("What efficiency number should I use?",
             "The EPA or WLTP figure is a lab best case; most drivers see 10-20% less in mixed driving, less again in winter when cold batteries and cabin heating bite. Check your car's trip computer lifetime average - that honest number beats any spec sheet for cost math."),
            ("Is public rapid charging still cheaper than gas?",
             "Often, barely - and sometimes not. At $0.40/kWh and 4 mi/kWh you pay 10 cents a mile; a 30 mpg car at $3.50 gas pays 11.7. Home charging at $0.15 halves that. The calculator makes the trade visible: the EV's economics depend less on the car than on where and when you charge."),
        ],
    })

    pages.append({
        "slug": "golden-hour-calculator",
        "title": "Golden Hour Calculator — Sunrise, Sunset & Best Photo Light Today",
        "h1": "Golden Hour Calculator",
        "desc": "Find today's golden hour windows from any location: sunrise, morning light, evening light and sunset - computed with real solar math. Free, no sign-up.",
        "category": "calculator",
        "keyword": "golden hour calculator",
        "tool": "goldenhour",
        "args": {},
        "intro": [
            "Golden hour is the hour-ish window when the sun sits within about 6° of the horizon and light turns warm, directional and forgiving - portraits glow, cities turn amber, and every photographer's feed gets better. It is not a fixed time: it shifts with latitude and season, from a reliable hour at mid-latitudes to most of the nightless summer day up north. This calculator computes it from solar position, not from a lookup table.",
            "Enter a date and coordinates and it gives the full light plan: sunrise, when the morning window closes, when the evening window opens, and sunset - all in your device's timezone, with the window length stated so you know whether you're working with 70 minutes or 25. Location and date are remembered for the next scout, and the share link hands the whole schedule to your shooting partner.",
        ],
        "howto": [
            "Pick the date and enter your latitude and longitude.",
            "Read the morning and evening golden windows plus sunrise and sunset.",
            "Arrive 20 minutes early - the first half of the window is the best light.",
        ],
        "faqs": [
            ("What exactly is golden hour?",
             "The period when the sun is low - roughly within 6° of the horizon. Sunlight then travels through much more atmosphere, which scatters away blue light and leaves warm, soft, directional illumination with long shadows. It occurs twice daily, and its length varies hugely with latitude and season - this calculator derives it from solar geometry rather than guessing '60 minutes'."),
            ("How accurate are the times?",
             "The math is the standard NOAA-style solar position model (declination, equation of time, horizon at -0.833° for sunrise/sunset and +6° for the golden edge), typically accurate to a couple of minutes. Local terrain matters more than formula error: mountains and tall buildings end the window early, so treat the times as your plan, not a guarantee."),
            ("What's the difference between golden hour and blue hour?",
             "Golden hour is before sunset (sun 6° above horizon to setting); blue hour is just after, when the sun is below the horizon and remaining light is deep blue - the cityscape and twilight-buildings window. The note under tonight's plan reminds you blue hour follows immediately if you're shooting skylines."),
            ("Why does golden hour last longer in summer or up north?",
             "The sun's path meets the horizon at a shallower angle when the days are long, so it crawls through the 6° band instead of diving through it. At mid-latitudes the evening window runs 30-60 minutes; near the Arctic in midsummer the sun can graze the horizon all night. The window-length stat shows your number for the date."),
        ],
    })

    pages.append({
        "slug": "pizza-dough-calculator",
        "title": "Pizza Dough Calculator — Flour, Water, Salt & Yeast in Grams",
        "h1": "Pizza Dough Calculator",
        "desc": "Scale pizza dough precisely: choose ball count, weight and hydration, get flour, water, salt and yeast in grams - with cold-ferment guidance. Free.",
        "category": "calculator",
        "keyword": "pizza dough calculator",
        "tool": "pizza",
        "args": {},
        "intro": [
            "Every good pizza dough is the same four numbers in different clothes: flour, water at 60-70% of flour weight, salt near 3%, and just enough yeast for the time you're giving the dough. Recipes written in cups betray you at every scale - this calculator works in baker's percentages, so '4 balls at 250g and 65% hydration' comes back as exact grams of everything, whether you're making two pizzas or twenty.",
            "The yeast field is the piece most calculators skip: yeast quantity depends on fermentation time and temperature, so the selector separates a room-temp day from a 24-hour cold ferment and adjusts the dose accordingly - because the single biggest upgrade in home pizza is not a 450°C oven, it's tomorrow's dough tonight. Your usual recipe is remembered, results show in the tab title, and the share link carries the full spec.",
        ],
        "howto": [
            "Enter how many pizzas and how heavy each ball should be (250g is typical for a 12-inch).",
            "Set hydration: 60% for beginner-friendly NY style, 65-70% for Neapolitan.",
            "Get your grams - then try the 24-hour cold ferment option this weekend.",
        ],
        "faqs": [
            ("What does hydration percentage mean?",
             "Water weight as a percentage of flour weight - 65% hydration means 650g water per kilo of flour. Higher hydration means wetter dough, more open airy crumb and harder handling; lower means easier shaping and denser chew. Start at 60-63% for your first bakes; go up only as your confidence with sticky dough does."),
            ("How much yeast should pizza dough have?",
             "Less than you think when time is on your side: a same-day dough wants around 0.4% instant yeast (1% fresh), while a 24-hour cold ferment needs only a quarter of that - the dough rises slowly in the fridge while flavor compounds build. Doubling yeast does not double rise speed linearly; giving the dough more time does."),
            ("How heavy should a pizza dough ball be?",
             "About 250g for a 12-inch (30cm) pizza, scaling roughly with the square of the size: 180-200g for a 10-inch, 300-330g for a 14-inch pan. Neapolitan rules pin it at 180-280g by law of tradition - the calculator just does the arithmetic for whatever you decide."),
            ("Can I scale this recipe for a stand mixer or by hand?",
             "The grams scale to any batch size, which is the point of baker's percentages - an eight-pizza party batch is as exact as a two-pizza Tuesday. Mix, rest 20 minutes (autolyse), add nothing, knead briefly, then ball and ferment; the numbers stay the same no matter which muscles do the work."),
        ],
    })

    pages.append({
        "slug": "inflation-calculator",
        "title": "Inflation Calculator — What $100 From Any Year Is Worth Today",
        "h1": "Inflation Calculator",
        "desc": "Convert money across any years 1913-2025 with BLS CPI-U data: today's buying power, cumulative inflation and average yearly rate. Free, no sign-up.",
        "category": "calculator",
        "keyword": "inflation calculator",
        "tool": "inflation",
        "args": {},
        "intro": [
            "A dollar is not a unit of measurement - it is a share of a shifting basket. $100 in 1990 has the buying power of roughly $240 today; $100 in 1920 had the power of about $1,600. This calculator runs those conversions on the Bureau of Labor Statistics' CPI-U annual averages, from 1913 to the present, and shows not just the headline number but the machinery behind it: cumulative inflation and the compound average rate per year.",
            "That yearly rate is the number worth internalizing: even the 'quiet' 2-3% years halve a dollar's value in 25-35 years, which is why a savings account under inflation is a slow leak with good manners. The note under the result keeps the map honest - CPI tracks an average basket, and your personal basket (housing, health, tuition) has its own weather.",
        ],
        "howto": [
            "Enter an amount and the year it came from.",
            "Enter the year to convert to - today's money is the usual target.",
            "Read the converted value, cumulative inflation and average annual rate.",
        ],
        "faqs": [
            ("How is inflation calculated between two years?",
             "By the Consumer Price Index: value × (CPI of the later year ÷ CPI of the earlier year). The CPI-U series used here is the BLS's standard index (1982-84 = 100), published as annual averages from 1913 onward - the same data behind every 'in today's money' headline you've ever read."),
            ("Why does my number differ slightly from other calculators?",
             "Three honest reasons: some sites use monthly rather than annual CPI (a December-vs-January difference), some use the CPI-Retroactive series the BLS rescaled in 1978, and the current year is always an estimate until the BLS finalizes it. Differences of a percent or two are normal and not a sign anyone is wrong."),
            ("What was the worst inflation in US history?",
             "The 1970s: prices nearly doubled across the decade (about 7-8% a year compounded), and single years hit 13%+ in 1979-1980. The fastest single-year spike in the modern series was 2022's post-pandemic surge; the deflation years of the 1930s cut prices but brought the Depression - falling prices are not a bargain."),
            ("Does this work for salaries and investments?",
             "For comparing purchasing power across time, yes - a $30,000 salary in 2000 equals about $55,000 today, and that's the honest way to judge a raise across years. For investments, subtract inflation from the nominal return to get the real return: 5% gains in a 3% year is only 2% of actual buying power."),
        ],
    })

    pages.append({
        "slug": "sleep-debt-calculator",
        "title": "Sleep Debt Calculator — How Far Behind Your Target You Really Are",
        "h1": "Sleep Debt Calculator",
        "desc": "Add up the hours you owe your body: average sleep vs your target, debt level, and how many nights of catch-up it takes. Free, instant, no sign-up.",
        "category": "calculator",
        "keyword": "sleep debt calculator",
        "tool": "sleepdebt",
        "args": {},
        "intro": [
            "Sleep debt is the gap between what your body asked for and what it got, compounded nightly: sleep 6.5 against an 8-hour target and by Sunday you owe 10.5 hours - which explains why the alarm on Monday morning feels like a court summons. This calculator makes the ledger visible: your average hours, your personal target, and the running balance across however many nights you've been living like this.",
            "The note under the number keeps the science honest, because the popular advice is half-wrong: weekend catch-up restores how awake you feel but not the metabolic and memory costs of the shortfall, and a single 14-hour recovery sleep is not a repayment plan. What works is boringly effective - a 15-minutes-earlier bedtime each week and an extra hour a night until the balance clears.",
        ],
        "howto": [
            "Enter your average hours slept and your personal target (8 is standard, 7 is the floor for most adults).",
            "Enter how many nights you've been running at that pace.",
            "Read your debt total, its level, and the realistic catch-up timeline.",
        ],
        "faqs": [
            ("What is sleep debt?",
             "The cumulative difference between the sleep your body needs and the sleep it received: an hour short per night for a week is a 7-hour debt. The body keeps rough books on this - it's why five bad nights in a row feel dramatically worse than one, even though total hours lost seem manageable."),
            ("Can you pay back sleep debt on the weekend?",
             "Partially. Recovery sleep restores vigilance and reaction time surprisingly well, but studies on metabolic effects (insulin sensitivity, appetite hormones) suggest the costs of short sleep are not fully refunded by binge sleeping - and weekend 12-hour sleeps shift your circadian rhythm later, making Monday harder. Steady extra hours beat heroic ones."),
            ("How much sleep do I actually need?",
             "Most adults need 7-9 hours; your number is the amount where you wake without an alarm feeling functional and don't crash mid-afternoon. If you need an alarm, caffeine before noon, and willpower to stay awake in meetings, the honest entry for 'target' is higher than the one you've been negotiating with."),
            ("Is chronic sleep debt serious or just tiredness?",
             "Serious: chronic 6-hour nights degrade attention comparably to alcohol at the legal limit, and long-term associations include higher risks of hypertension, weight gain, and mood disorders - while feeling 'used to it' is an illusion the impairments don't share. The debt number isn't guilt; it's a maintenance budget like any other."),
        ],
    })

    pages.append({
        "slug": "coffee-ratio-calculator",
        "title": "Coffee Ratio Calculator — Grams of Coffee to Water, Both Ways",
        "h1": "Coffee Ratio Calculator",
        "desc": "Stop guessing your brew: convert water to coffee grams (or back) at any ratio, with strength guidance for pour-over, French press and more. Free.",
        "category": "calculator",
        "keyword": "coffee ratio calculator",
        "tool": "coffee",
        "args": {},
        "intro": [
            "The difference between good coffee and disappointing coffee is usually not the beans, the grind, or the water - it's 3 grams. Brewing is a ratio game: grams of coffee times your ratio equals grams of water, and the whole specialty world lives between 1:15 (bold) and 1:18 (light). This calculator runs the math both directions - 'I have 500ml of water, how many beans?' and 'I weighed out 30g, how much water?' - so the scale becomes the best upgrade your kitchen ever took.",
            "The verdict line reads your ratio back in plain language - strong, balanced, or tea-like - and the note carries the two adjustments that actually fix a cup: grind coarser for bitter, finer for sour. Your recipe is remembered for tomorrow morning, the result rides in the tab title while you pour, and the share link sends the exact recipe to whoever keeps asking why your coffee tastes better.",
        ],
        "howto": [
            "Pick a direction: know your water (most brewing) or know your coffee (pre-weighed).",
            "Enter the amount and a ratio - 1:16 is the universal starting point.",
            "Brew, taste, then move the ratio one notch: 1:15 for more punch, 1:17 for lighter.",
        ],
        "faqs": [
            ("What is the golden ratio for coffee?",
             "The specialty-coffee standard sits at 1:16 to 1:18 coffee to water by weight - about 30-31g of coffee per 500ml. 1:15 and below reads strong and heavy (good for French press with milk), 1:17 is where most pour-over dialed-in cups live, and past 1:19 extraction struggles to keep up with the dilution and the cup turns thin and papery."),
            ("Why weigh coffee instead of using scoops?",
             "A 'tablespoon' of coffee can weigh 4g or 7g depending on grind, roast and how heaped it is - a spread wide enough to change the cup noticeably. Ten dollars of scale removes the biggest variable in brewing, which is why every serious recipe you've ever seen is written in grams: weight is the only honest unit."),
            ("Does the ratio change for espresso or cold brew?",
             "Yes - they're different games: espresso runs near 1:2 in 25-30 seconds (a 18g dose to a 36g shot), and cold brew is a concentrate near 1:8 that gets diluted before serving. This calculator covers the immersion and pour-over family where 1:14-1:18 rules; for espresso, dose and yield are the two numbers to fix first."),
            ("My coffee tastes sour/bitter - is it the ratio?",
             "Probably the grind, and the ratio can compensate: sour-and-thin means under-extraction, so grind finer or use more coffee (lower ratio); bitter-and-dry means over-extraction, so grind coarser or use less (higher ratio). Change one variable at a time by a small step - the calculator keeps the math honest while your palate finds the sweet spot."),
        ],
    })

    pages.append({
        "slug": "break-even-calculator",
        "title": "Break-Even Calculator — Units to Cover Costs, Margin Shown",
        "h1": "Break-Even Calculator",
        "desc": "Find the exact number of sales that covers your monthly costs: fixed costs, price and unit cost in, break-even units, revenue and margin out. Free.",
        "category": "calculator",
        "keyword": "break even calculator",
        "tool": "breakeven",
        "args": {},
        "intro": [
            "Every business has a magic unit number: the sale where the rent stops being your money and becomes profit's. Break-even is fixed costs ÷ (price − variable cost) - the whole discipline of a business plan compressed into one line, and the first number any investor, lender or spouse asks for. This calculator runs it live, plus the two numbers that make it mean something: revenue required at break-even and the contribution margin each sale carries.",
            "The note under the result is where strategy lives: because everything past break-even falls to profit at nearly 100% margin, small levers matter enormously - and a price increase almost always beats a volume chase. Your assumptions are remembered between visits, the result rides in the tab title, and the share link carries the scenario for partners to poke at.",
        ],
        "howto": [
            "Enter monthly fixed costs - rent, salaries, subscriptions, everything that doesn't care about volume.",
            "Enter price per unit and the variable cost of delivering one unit.",
            "Read break-even units, then test: what happens to it if price rises $5?",
        ],
        "faqs": [
            ("How is the break-even point calculated?",
             "Break-even units = fixed costs ÷ (price per unit − variable cost per unit). The denominator is the contribution margin: what each sale adds toward fixed costs after its own direct costs. $3,000 fixed, $49 price, $17 cost gives $32 margin and 94 units a month - unit #94 clears the slate; #95 is profit."),
            ("What counts as a fixed vs variable cost?",
             "Fixed costs stay flat as volume changes: rent, salaries, software, insurance. Variable costs ride with each unit: materials, packaging, payment processing, shipping. The gray zone - your salary as founder, hourly labor - goes where it behaves more like the label says; be consistent rather than perfect."),
            ("Is a lower break-even point always better?",
             "Lower is safer - fewer sales to survive a slow month - but the cheapest ways down (low price, minimal fixed spend) often cap the upside. The interesting move is usually the opposite direction: raising price raises margin, which cuts break-even while raising the ceiling. Run both scenarios above and compare."),
            ("Does break-even work for services or SaaS?",
             "Yes, with honest inputs: a freelancer's variable cost per project might be just software fees and subcontractors; a SaaS has server cost per user and churn eating the 'units'. The formula is identical - what changes is how honestly you split fixed from variable, which this calculator makes you decide out loud."),
        ],
    })

    pages.append({
        "slug": "ideal-weight-calculator",
        "title": "Ideal Weight Calculator — Devine Formula & Healthy BMI Range",
        "h1": "Ideal Weight Calculator",
        "desc": "Get two honest answers for your height: the classic Devine formula and the wider healthy-BMI weight band, in kg or lb. Free, instant, no sign-up.",
        "category": "calculator",
        "keyword": "ideal weight calculator",
        "tool": "idealweight",
        "args": {},
        "intro": [
            "'Ideal weight' sounds like one number, but the two formulas behind the phrase disagree on purpose. The Devine formula - 50 kg for a man plus 2.3 kg per inch over five feet - was built in 1974 to dose medications, and became the classic single answer. The healthy-BMI band (18.5-24.9) is wider because bodies are. This calculator shows both, side by side, in kg or lb, so you can see the range instead of worshipping a point.",
            "The note under the result is the differentiator: no formula knows your frame, muscle mass or history, and an athletic body at the top of the BMI band can be healthier than a sedentary one at the bottom. Treat the band as a range, the trend as the signal, and your doctor as the tiebreaker - that is the honest version of this tool, and it's remembered here for your next check-in.",
        ],
        "howto": [
            "Choose units (cm/kg or ft-in/lb), sex and enter your height.",
            "See the Devine ideal weight and the healthy-BMI range together.",
            "Use the band, not the point - and compare against where you were last month.",
        ],
        "faqs": [
            ("What is the Devine ideal weight formula?",
             "Men: 50 kg + 2.3 kg per inch over 5 feet. Women: 45.5 kg + the same inch allowance. It was published in 1974 to convert height into a medication dose, inherited from insurance tables, and became the 'ideal body weight' in medical texts - useful as a rough midpoint, never as a verdict on a body."),
            ("What is a healthy weight range for my height?",
             "The BMI band 18.5-24.9 applied to your height: for 175 cm that's roughly 57-76 kg (126-168 lb). It's wide because it needs to be - bone structure, muscle and fat distribution vary enormously within one height. The calculator shows both the band and the Devine point so you can see the difference between a range and a myth."),
            ("Why does the calculator show a range instead of one number?",
             "Because single-number ideals do real harm: they ignore frame size, muscle (which is denser than fat) and age. Research consistently finds the lowest mortality in the upper part of the 'normal' BMI band and slightly above it in older adults - the truth is a plateau, not a peak, and pretending otherwise just fuels yo-yo dieting."),
            ("Is BMI itself reliable?",
             "As a population screen, yes; as an individual verdict, it's blunt - muscular people read as overweight, and 'normal BMI' can hide high body fat. Better signals: waist-to-height ratio (under about 0.5), how your clothes fit over months, and bloodwork. This tool starts the conversation; your clinician finishes it."),
        ],
    })

    pages.append({
        "slug": "lorem-ipsum-generator",
        "title": "Lorem Ipsum Generator — Count-Exact Placeholder Text, Instant Copy",
        "h1": "Lorem Ipsum Generator",
        "desc": "Generate placeholder text with exact paragraph and word counts, optional classic start, one-tap copy. Free, instant, nothing tracked.",
        "category": "generator",
        "keyword": "lorem ipsum generator",
        "tool": "lorem",
        "args": {},
        "intro": [
            "Placeholder text is a utility, and utilities should be exact: this generator produces as many paragraphs as you ask, each word-count-true, starting with the canonical 'Lorem ipsum dolor sit amet' when you want the classic look or with fresh random Latin when you don't. One tap copies it to your clipboard - no signup walls, no ads between you and the paste, no nonsense.",
            "Under the hood it draws from the full classical passage plus Cicero's De Finibus roots (the text has been filler since the 1500s, when a printer scrambled it to show a typeface), reshuffling sentence-length fragments every regenerate. Your last settings are remembered for the next mockup, and the word count rides in the tab title so you can size a layout without counting.",
        ],
        "howto": [
            "Set paragraph count and words per paragraph.",
            "Toggle the classic 'Lorem ipsum…' opening on or off.",
            "Copy to clipboard and paste into your design, CMS or CSS demo.",
        ],
        "faqs": [
            ("What is Lorem ipsum, actually?",
             "Scrambled fragments of Cicero's 'De finibus bonorum et malorum' (45 BC), mangled by a 16th-century printer to demonstrate a typeface and adopted by typesetters ever since. It's deliberately readable-as-Latin-but-meaningless: enough like real language to show layout texture, empty enough that nobody proofreads the placeholder."),
            ("Why does word count matter for placeholder text?",
             "Because layouts are weight-sensitive: a 60-word paragraph wraps differently than a 40-word one, and testing with sloppy lengths hides overflow and raggedness that ship with real copy. Exact counts let you stress the worst case - that's the whole point of the tool."),
            ("Can I use it in a real project or publication?",
             "For mockups, wireframes, CMS tests and CSS demos: absolutely, that's its job. For published content: replace it - shipping Lorem ipsum to production is the classic 'nobody checked' tell. The Latin itself is ancient public domain; Cicero won't sue."),
            ("Does it make the same text every time?",
             "No - each regenerate draws fresh random sentences from the word pool, so repeated blocks look natural across a long page. The optional classic opening fixes just the first five words ('Lorem ipsum dolor sit amet') for those traditional-print vibes, then randomizes the rest."),
        ],
    })

    pages.append({
        "slug": "cagr-calculator",
        "title": "CAGR Calculator — Compound Annual Growth Rate of Any Investment",
        "h1": "CAGR Calculator",
        "desc": "Smooth any investment's journey into one honest yearly rate: beginning value, ending value, years - CAGR, total growth and doubling time. Free.",
        "category": "calculator",
        "keyword": "cagr calculator",
        "tool": "cagr",
        "args": {},
        "intro": [
            "An investment that went +40%, then -15%, then +22% over three years didn't grow 47% - it grew at its compound annual growth rate, the single rate that would have taken the same money from the same start to the same finish at steady speed. CAGR = (ending ÷ beginning)^(1/years) − 1, and it is the only fair way to compare a wild ride with a boring one, a fund with a benchmark, or this year's portfolio with your neighbor's boast.",
            "This calculator runs it instantly and adds the two sanity numbers professionals keep handy: the total multiple and the doubling time at that rate (Rule of 72 made precise). The note underneath keeps the recovery trap visible - a 50% loss needs a 100% gain to break even - which is the reason steady compounding beats spectacular swings over any real holding period.",
        ],
        "howto": [
            "Enter the beginning value, the ending value, and the years between them.",
            "Read the annualized rate, total growth and doubling time.",
            "Compare: same CAGR with half the volatility is the better investment, every time.",
        ],
        "faqs": [
            ("What is CAGR in simple terms?",
             "The smoothed yearly rate: the growth percentage that, applied every year with compounding, lands exactly where your investment actually landed. A portfolio that doubled in 6 years has a 12.2% CAGR - even if it never grew exactly 12.2% in any single year. It converts stories into a comparable number."),
            ("How is CAGR different from average return?",
             "The arithmetic average of +50% and −50% is 0%, but the money is down 25% - averages ignore sequencing. CAGR uses the geometric path and tells the truth: √(1.5×0.5)−1 = −13.4%. Any comparison built on averaged yearly returns flatters volatility; CAGR doesn't."),
            ("What is a good CAGR?",
             "Context decides: 7% real has been the long-run equity market's rough song; a business growing revenue 20-30% a year is elite; a 40% CAGR sustained for a decade is almost unheard of. The right question is CAGR versus the risk-free alternative plus the risk you took - the calculator gives you the number; the benchmark gives it meaning."),
            ("Does CAGR account for additional contributions?",
             "No - it assumes one sum in, one sum out. For a portfolio with regular deposits, use the money-weighted return (IRR) instead; running CAGR on the combined deposits will overstate growth. This tool is honest for lump sums and for business metrics like revenue or users, which is where it's most used."),
        ],
    })

    pages.append({
        "slug": "pool-volume-calculator",
        "title": "Pool Volume Calculator — Liters & Gallons by Shape and Depth",
        "h1": "Pool Volume Calculator",
        "desc": "Calculate your pool's water volume from shape and dimensions - liters, US gallons and tonnes, with average-depth guidance for honest dosing. Free.",
        "category": "calculator",
        "keyword": "pool volume calculator",
        "tool": "pool",
        "args": {},
        "intro": [
            "Every pool chemical label, pump spec and heating estimate starts from one number owners routinely get wrong: how much water is actually in the pool. Volume is length × width × average depth for a rectangle, π × radius² × depth for a circle - and 'average depth' is where the honest math happens, because (shallow + deep) ÷ 2 is not what most people eyeball. This calculator runs the geometry for rectangular, oval and round pools in metric or feet.",
            "The outputs come back three ways - liters, US gallons and tonnes of water - because chemical dosing, filtration specs and water bills each speak a different dialect. The note adds the two practical truths: fill level sits near 90% of the coping, and at several thousand liters, evaporation alone is why a pool cover is the highest-ROI accessory you can buy.",
        ],
        "howto": [
            "Pick the pool shape: rectangular, circular or oval.",
            "Enter dimensions and the average depth - (shallow + deep) ÷ 2.",
            "Read liters, gallons and tonnes; dose chemicals to the volume, not to guesswork.",
        ],
        "faqs": [
            ("How do I calculate my pool's volume?",
             "Rectangle: length × width × average depth. Circle: π × (diameter ÷ 2)² × depth. Oval: π × (length ÷ 2) × (width ÷ 2) × depth. Keep every measurement in the same unit; the calculator converts to liters or US gallons and shows both plus cubic meters for filter-flow specs."),
            ("Why is average depth so important?",
             "Because chemicals, heating and pump runtime all scale with true volume, and a wrong average compounds every dose: a pool that's really 60 m³ but treated as 45 gets 25% under-dosed sanitizer - which is how green water happens to tidy people. Measure both ends and split the difference; freeform pools need a honest middle estimate."),
            ("How many liters is a typical backyard pool?",
             "A 8×4 m family pool averaging 1.4 m deep holds about 45,000 liters (12,000 US gallons); a small round above-ground (4.5 m, 1.2 m) around 19,000 liters. knowing your number turns chemical labels from riddles into arithmetic - '100 ml per 10,000 L' finally means something."),
            ("Does the shape of the floor (hopper, slope) change the math?",
             "Averaging handles simple slopes; deep hopper ends in diving pools add volume the flat average misses - if yours has one, estimate the hopper separately and add it. Freeform kidney shapes: measure width at three points and average. The calculator's ±10% honest range beats most owners' ±30% guesses."),
        ],
    })

    pages.append({
        "slug": "time-spent-calculator",
        "title": "Time Spent Calculator — What X Hours a Day Costs Over a Lifetime",
        "h1": "Time Spent Calculator",
        "desc": "Turn 'just an hour a day' into years of your life: daily hours, ages, and the total in years, months and 40-hour work-weeks. Free, no sign-up.",
        "category": "calculator",
        "keyword": "time spent calculator",
        "tool": "timespent",
        "args": {},
        "intro": [
            "Three hours a day doesn't sound like much - it's a commute, a scrolling habit, a series. Run the math across a life and it becomes 8 years: eight years of your one allocation, spent at 3 hours a day from 15 to 80. This calculator makes that arithmetic unavoidable: hours per day, days per week, the age span you choose, and the total in years, months and honest 40-hour work-weeks.",
            "The tool refuses to moralize for you - the same math that indicts a doom-scrolling habit also celebrates a craft: 90 minutes of guitar a day from age 20 to 70 is nearly two years of deliberate practice, which is what mastery is actually made of. Your inputs are remembered, the total rides in the tab title, and the share link carries the scenario for the group chat that needs to see it.",
        ],
        "howto": [
            "Enter the daily hours and days per week for the habit you're curious about.",
            "Set the age span - from when it started to when you'd like it to end.",
            "Read the total in years and work-weeks; adjust the daily number and watch it move.",
        ],
        "faqs": [
            ("How is time spent calculated over a lifetime?",
             "Hours per day × days per week × 52.14 weeks × the years in your age span, then ÷ 24 to express it as full 24-hour days worth of years. A 3-hour daily habit from 15 to 80 is 3 × 7 × 52.14 × 65 ÷ 24 ÷ 365.25 ≈ 7.7 years. The calculator does it live so you can watch the total react to each input."),
            ("Why does an hour a day feel bigger than it sounds?",
             "Because habits compound like money: an hour is only 4% of a day, but an hour every day for a decade is 365 hours - nine full work-weeks - and 4% of a day is closer to 6% of your waking hours. Small daily choices are where years actually go; the number just removes the camouflage."),
            ("What can I realistically do with recovered time?",
             "The classic benchmarks: a spoken language needs roughly 600-750 hours, a musical instrument's first competent year about 300, a sub-4-hour marathon maybe 500. One reclaimed hour a day pays for any of those inside two years - the calculator turns that from a motivational poster into arithmetic you've personally verified."),
            ("Is some daily 'wasted' time actually fine?",
             "Yes - rest, boredom and unstructured time are where recovery and ideas come from, and optimizing every minute is its own failure mode. The honest use of this number is on the habits you do without deciding to: the app you open on autopilot. Time you chose on purpose was never waste."),
        ],
    })

    pages.append({
        "slug": "meat-cooking-time-calculator",
        "title": "Meat Cooking Time Calculator — Roast Times per Kg with Rest & Core Temps",
        "h1": "Meat Cooking Time Calculator",
        "desc": "Roast times for chicken, turkey, pork, beef and lamb by weight - with safe core temperatures and resting time built in. Free, instant, no sign-up.",
        "category": "calculator",
        "keyword": "meat cooking time calculator",
        "tool": "meattime",
        "args": {},
        "intro": [
            "Every roast dinner panic is the same arithmetic: how long does THIS weight need, and when do I actually put it in the oven. This calculator answers per cut - whole chicken, turkey, pork loin, beef ribs, lamb leg - scaling the classic per-kilogram times to your exact weight, then adding the two things time-only charts forget: the resting period that finishes the carryover cooking, and the target core temperature that decides juicy versus sawdust.",
            "The honest rule the note keeps repeating: minutes are the plan, the probe is the boss. Ovens run hot or cold by 15 degrees, meat shapes fool charts, and only the internal temperature is both safe and delicious - which is why the result pairs every time range with its core target and the reminder to pull the meat a few degrees early and let rest do the rest.",
        ],
        "howto": [
            "Pick the cut and enter the weight (kg or lb).",
            "Read the oven-time range, safe core temperature and resting time.",
            "Pull the meat a few degrees early, rest it, carve - juices stay in the meat, not the board.",
        ],
        "faqs": [
            ("How long do I cook a whole chicken per kg?",
             "About 42-48 minutes per kg at 180°C (350°F), so a 1.5 kg bird runs 60-70 minutes - plus a 15-minute rest. The only verdict that matters is core temperature: 74°C (165°F) in the thickest part of the thigh, with clear juices. A slightly early pull and a proper rest keeps breast meat from turning to chalk."),
            ("Why does meat need to rest after roasting?",
             "Heat drives juices toward the center; resting lets them redistribute so the meat reabsorbs them instead of donating them to the carving board. Five minutes for a loin, 15-30 for a turkey - and carryover heat keeps cooking the core 3-5°C during the rest, which is exactly why you pull the roast early."),
            ("What temperature is pork done at now?",
             "The old 'well-done or else' rule is retired: 63°C (145°F) core with a short rest is the modern standard for pork loin - blush pink is safe and vastly juicier. Ground pork and organ meats remain the exception (72°C+). Poultry stays at 74°C with no exceptions; the pink-versus-safe line differs by animal."),
            ("Do cooking times change with fan (convection) ovens?",
             "Slightly - fan ovens cook roughly 10-20% faster and more evenly, so start checking toward the early end of the range or drop the temperature 15-20°C. But the same principle covers every oven quirk: the recipe time is a schedule for the probe, not a verdict - trust the core temperature over the clock."),
        ],
    })

    pages.append({
        "slug": "car-depreciation-calculator",
        "title": "Car Depreciation Calculator — What Your Car Is Worth After N Years",
        "h1": "Car Depreciation Calculator",
        "desc": "See a car's real cost curve: value after N years at your depreciation rate, total loss, and the per-year cost fuel calculators forget. Free, no sign-up.",
        "category": "calculator",
        "keyword": "car depreciation calculator",
        "tool": "cardep",
        "args": {},
        "intro": [
            "Fuel gets the headlines but depreciation eats the budget: for most owners, the value a car silently loses each year is the single biggest cost of driving - often larger than fuel and insurance combined. This calculator runs the compounding curve from purchase price, years owned and an annual rate, and reports the three numbers that matter: current value, total value lost, and the honest cost per year of ownership.",
            "The default 15% annual rate encodes the industry's uncomfortable shape: cars lose 40-50% of their value in the first three years, then the curve flattens dramatically - which is why the 3-year-old used car is the classic rational purchase (someone else paid the steep part), and why a two-year lease on a new luxury badge is the most expensive way to own anything with wheels.",
        ],
        "howto": [
            "Enter the purchase price and years owned.",
            "Set the annual depreciation rate (15-18% is typical; luxury cars run higher).",
            "Read current value, total loss and per-year cost - then try 3 years versus 8.",
        ],
        "faqs": [
            ("How fast do cars lose value?",
             "New cars typically drop 15-20% the moment they're driven off the forecourt and reach 40-50% cumulative loss by year three, after which depreciation settles to single digits a year. Compounding the classic 15% rate matches real market data for average sedans; luxury marques and heavy EVs have run steeper, while models with cult demand run flatter."),
            ("Why is depreciation the biggest cost of owning a car?",
             "Because it's invisible: fuel, insurance and maintenance announce themselves in bills, while depreciation happens silently in the resale price. A $30,000 car that's worth $18,000 after three years cost you $4,000 a year - likely more than the fuel to drive it. Any honest car budget starts with this line, not the pump."),
            ("What's the cheapest age to buy a used car?",
             "Around 3 years old: the steepest depreciation is done, the car is modern enough for safety tech and reliability, and the remaining curve is gentle. By year 8-10 maintenance costs start climbing to meet the flattened depreciation, which is the other edge of the curve - the sweet spot is between them."),
            ("Do electric cars depreciate differently?",
             "Recently, faster - rapid battery-tech improvements and aggressive new-price cuts on EVs dragged 3-year residuals below comparable petrol cars in many markets, though the gap is narrowing as batteries prove durable. If you're shopping EVs, run this calculator with a steeper early rate (20-25%) and let the used market's shape inform the risk."),
        ],
    })

    pages.append({
        "slug": "jet-lag-calculator",
        "title": "Jet Lag Calculator — Recovery Days & Light Strategy by Time Zones",
        "h1": "Jet Lag Calculator",
        "desc": "Estimate how many days jet lag will last for your flight: zones crossed, east or west, plus the pre-shift and light-exposure plan that shortens it. Free.",
        "category": "calculator",
        "keyword": "jet lag calculator",
        "tool": "jetlag",
        "args": {},
        "intro": [
            "Jet lag is your circadian clock stranded in the wrong time zone - and the recovery bill depends on which way you flew. Eastward (losing hours) costs roughly a day of adjustment per zone crossed; westward (gaining hours) runs about half that, because staying up late fights your biology less than falling asleep early does. This calculator turns your itinerary into a recovery estimate plus the strategy that actually shortens it.",
            "The strategy has two halves the note makes concrete: pre-shifting your sleep and meal times an hour per day toward destination time before departure (the pro move that does most of the work on the ground), and using light as the drug after arrival - morning light to advance eastward, evening light to delay westward - with caffeine before local noon and zero airplane alcohol, which costs more sleep than it buys.",
        ],
        "howto": [
            "Enter how many time zones you're crossing and which direction.",
            "Read the realistic recovery days and the pre-departure shift schedule.",
            "Follow the light rule on arrival - it's the strongest lever you have.",
        ],
        "faqs": [
            ("How long does jet lag last?",
             "The working rule: about one day per time zone crossed flying east, half a day per zone westward - so 7 zones east can genuinely take a week to fully clear, while 7 west feels human in 3-4. Individual recovery varies with age and chronotype, but the direction asymmetry is consistent across studies."),
            ("Why is flying east worse than west?",
             "Eastbound shortens your day, forcing sleep earlier than your body wants - and the human circadian system resists advancing more than delaying. Westbound lengthens the day, and staying up later is something most brains manage happily. Same distance, different bill - the calculator prices it honestly."),
            ("Does light exposure really fix jet lag?",
             "It's the strongest lever that exists - timed bright light is how the circadian clock actually resets. The rule: flying east, seek bright morning light locally and block evening light (sunglasses after dusk) to pull the clock forward; flying west, flood your evening with light and avoid dawn. Get the direction wrong and you can shift the wrong way, doubling the lag."),
            ("Should I pre-shift my sleep before a long flight?",
             "Yes - it's what frequent flyers and sports teams do: move bedtime, wake time and meals one hour per day toward destination time for as many days as you can before departure. Three days of pre-shift before an eastbound flight quietly absorbs half the jet lag before the plane leaves the gate. Combine with morning caffeine and no naps past 20 minutes on arrival day."),
        ],
    })


    pages.append({'slug': 'mulch-calculator', 'title': 'Mulch Calculator — How Many Bags by Area and Depth', 'h1': 'Mulch Calculator', 'desc': 'How many bags of mulch for your beds? Enter area and depth in cm, get bag count, cubic metres and cost. Includes the bulk-vs-bags crossover. Free, no sign-up.', 'category': 'calculator', 'keyword': 'mulch calculator how many bags', 'tool': 'mulch', 'args': {}, 'intro': ['Enter the length and width of your bed, the depth you want in centimetres, and your bag size in litres. The calculator converts everything to cubic metres, rounds up to whole bags, and totals the cost if you enter a price per bag.', 'Garden-centre mulch calculators usually push one brand and one bag size. This one is brand-neutral, metric, and honest about the point where a delivered bulk skip of a cubic metre or two beats carrying dozens of plastic bags home.'], 'howto': ["Measure the bed's length and width in metres — for an odd shape, break it into rectangles and add the areas as a length × width pair.", 'Pick your depth: 5 cm is the standard weed-suppressing layer, 7–8 cm for bare soil or topping up old mulch.', 'Enter the bag size printed on the bag (commonly 50–100 L) and the price if you want a total; the result rounds up to whole bags.'], 'faqs': [('How deep should mulch be?', '5 cm blocks most weeds and holds moisture well. 7–8 cm suits bare, dry soil or a refresh over old mulch. Beyond 10 cm you risk starving roots of air, and never pile mulch against trunks or stems — leave a hand-width clear to avoid rot.'), ('How many 50-litre bags make a cubic metre?', 'Twenty. That is the bulk-vs-bags crossover in practice: once you need roughly a cubic metre or more, delivered bulk mulch is usually cheaper per m³, saves dozens of bags, and can be barrowed straight onto the beds.'), ('Do I need to remove old mulch first?', 'No — loosen it with a fork and top up to the target depth. Only remove it if it has matted into a water-shedding crust or shows fungal growth; otherwise the old layer composts in place and feeds the soil.'), ('Does mulch attract pests?', 'Properly aerated mulch at the right depth attracts worms, not trouble. Problems come from too-deep layers and mulch piled against stems, which create the damp hiding spots slugs and rodents like.')]})

    pages.append({'slug': 'laminate-flooring-calculator', 'title': 'Laminate Flooring Calculator — Packs Needed with Waste %', 'h1': 'Laminate Flooring Calculator', 'desc': 'How many packs of laminate for your room? Area plus a waste allowance for cuts, L-shapes and herringbone, with batch-number advice. Free, no sign-up, works offline.', 'category': 'calculator', 'keyword': 'laminate flooring calculator packs waste', 'tool': 'laminate', 'args': {}, 'intro': ["Enter your room's length and width, the coverage printed on the laminate pack (in m²), and a waste allowance. The calculator works out the real area, adds the waste, and rounds up to full packs — including how many spare metres you are actually buying.", 'Shop calculators often hide the waste allowance or set it too low to make the price look cheaper. This one shows the waste explicitly, defaults to 8% for a straight lay, and tells you when to push it to 12% or 15%.'], 'howto': ['Measure the room at its longest and widest points, into doorways and alcoves — not just between the skirting boards.', 'Read the pack coverage from the box label (typically 1.5–2.7 m²) and enter it exactly; packs vary between thicknesses and ranges.', 'Choose waste: 8% for a plain rectangular room, 10–12% for L-shapes, many doorways or herringbone, 15%+ for a 45° diagonal lay.'], 'faqs': [('How much laminate waste should I add?', '8% covers a straightforward rectangular room with straight-lay boards. Use 10–12% for L-shaped rooms, lots of pipe and doorway cuts, or herringbone patterns, and 15% or more for diagonal (45°) layouts where every board end is a cut.'), ('Why do packs matter more than square metres?', 'Laminate sells in sealed packs and shade lots differ between production runs. Buying full packs from one batch — and keeping the batch number — means future repairs match; buying short mid-job risks a visible mismatch.'), ('What do I do with leftover packs?', 'Keep one opened pack for repairs and return the rest: most retailers accept unopened packs within their return window, which is why keeping receipts and not damaging boxes is part of the job plan.'), ('Should laminate acclimatise before fitting?', "Yes — leave sealed boxes flat in the room for about 48 hours so the boards reach the room's humidity. Skipping this is the classic cause of later gapping and creaking as the boards expand and contract.")]})

    pages.append({'slug': 'wallpaper-calculator', 'title': 'Wallpaper Calculator — Rolls Needed incl. Pattern Repeat', 'h1': 'Wallpaper Calculator', 'desc': 'How many rolls of wallpaper for your room? Perimeter and height with roll size and pattern repeat handled honestly. Free, no sign-up, works offline.', 'category': 'calculator', 'keyword': 'wallpaper calculator how many rolls pattern repeat', 'tool': 'wallp', 'args': {}, 'intro': ['Enter the perimeter of your walls, the height, your roll dimensions and the pattern repeat from the label. The calculator works out strips needed, strips per roll with the repeat applied, and whole rolls to buy — with the trim allowance built in.', 'Shop calculators quietly assume plain paper. This one prices the pattern repeat honestly: with a repeat, every strip cuts to a multiple of the repeat, offcuts stop being reusable, and the roll count jumps — better to know before the till than after.'], 'howto': ['Add up the wall lengths you are papering (perimeter) and subtract only large openings like doors if you prefer to work net.', 'Read roll width and length from the label (standard metric rolls are 0.53 m × 10.05 m) and enter them exactly.', 'Find the pattern repeat on the insert — the distance before the design repeats. Enter 0 for plain paper; the calculator rounds each cut up to the repeat automatically.'], 'faqs': [('How much extra wallpaper should I allow?', 'The built-in 10 cm per strip covers uneven ceilings and skirtings. Beyond that, order one spare roll for bold patterns or long rooms: repairs must come from the same batch number later, and discontinued lines are never reprinted.'), ('Why does pattern repeat change the number of rolls?', 'Each strip must start at the same point of the pattern so the design lines up across the wall. That forces every cut to a multiple of the repeat, wasting a fixed offcut per strip — on a large repeat over a short wall, a 10 m roll can drop from four usable strips to three.'), ('How do I measure the perimeter?', 'Wall length plus wall width, doubled, then subtract nothing for windows and doors — the offcuts and the spare-roll margin cover openings, and working gross is safer than running short mid-wall.'), ('Do I paper behind wardrobes and radiators?', 'Behind a fitted wardrobe you can skip; behind radiators, paper — strips shrunk visibly at a radiator are the classic amateur tell. The pattern match across the radiator matters more than the saving.')]})

    pages.append({'slug': 'diaper-cost-calculator', 'title': 'Diaper Cost Calculator — Real First-Year Total', 'h1': 'Diaper Cost Calculator', 'desc': 'What diapers really cost: per day, per month and over the whole diapering years, with the cloth crossover priced honestly. Free, no sign-up.', 'category': 'calculator', 'keyword': 'diaper cost calculator first year', 'tool': 'diapers', 'args': {}, 'intro': ['Enter how many diapers a day you are actually changing, what you pay per diaper, and how many months of diapering you expect. The calculator totals the spend per day, month, year and overall — the number baby-product sites prefer not to add up.', 'Brand cost calculators quote newborn-stage counts and their own pack prices. This one is brand-neutral, shows the monthly running cost, and tells you when the count drops — because diaper usage halves between month one and year two.'], 'howto': ['Count diapers for two normal days and average them — do not trust memory, parents underestimate by about a third.', 'Work out your real price per diaper from your last receipt including offers; bulk packs usually land 15-25% cheaper per piece.', 'Enter the months you expect (most children are done between 24 and 36 months, later at night) and read the total plus the monthly running cost.'], 'faqs': [('How many diapers a day does a baby use?', 'Newborns average 10-12, infants 7-9, and toddlers 4-6 plus night nappies. The drop is steady: sizing up reduces count per day but raises price per diaper, which is why the total stays flatter than the count suggests.'), ('What is the realistic total cost of diapers?', 'At 8 a day, 0.25 per diaper over 30 months, you are near 1,800-2,000 — wipes, bags and cream push it 15-20% higher. Using budget brands can cut it by half; premium push it up by a third.'), ('When do cloth diapers pay off?', 'A full cloth stash costs roughly one to three months of disposables, so the crossover lands around month two or three — but only if you actually wash at temperature every two to three days. Price your water and electricity before assuming savings.'), ('Should I stockpile diapers before the baby arrives?', 'Buy one box each of size newborn and size 1, no more: growth is unpredictable and half of stockpiled newborn boxes go unused. Lock in the price you like on size 2 and 3, which babies wear longest.')]})

    pages.append({'slug': 'wake-window-calculator', 'title': 'Wake Window Calculator — Ranges by Baby Age in Months', 'h1': 'Wake Window Calculator', 'desc': 'Typical wake windows by age in months: how long a baby can stay up between naps, nap counts and total daily sleep, with cue-reading guidance. Free, no sign-up.', 'category': 'calculator', 'keyword': 'wake windows by age baby months', 'tool': 'wake', 'args': {}, 'intro': ["Enter your baby's age in months and get the typical wake window range, how many naps a day that age usually takes, and total daily sleep expectations — the three numbers sleep schedules are built on.", "Sleep-site tables often present one magic number per age. This one shows honest ranges, because a 4-month-old's comfortable window varies by half an hour baby to baby — and reading cues beats watching the clock anyway."], 'howto': ["Enter your baby's age in months (use the corrected age if born early).", 'Read the wake window range: aim naps at the lower end on busy days, the upper end is a ceiling, not a target.', 'Watch for the cues — eye rubbing, staring, fussing — and put the baby down at the first one rather than waiting out the window.'], 'faqs': [('What happens if I miss the wake window?', 'Overtiredness releases cortisol, which works like caffeine: the baby fights the next nap, sleeps shorter and wakes more at night. An earlier bedtime by 20-30 minutes usually rescues the day.'), ('Do wake windows apply at night?', "They set the last stretch before bed: the final wake window is usually the longest of the day, around 2-3 hours at 6 months. If nights are rough, shorten the day's last window first before changing anything else."), ('What is the 2-3-4 schedule?', 'A simple pattern once naps consolidate to two: wake window of 2 hours before the first nap, 3 before the second, 4 before bedtime. It works for many babies aged roughly 6-14 months and self-adjusts as windows stretch.'), ('Are these ranges rules?', 'No — they are population mid-points. Premature babies run on corrected age, high-need sleepers run short, and some babies comfortably run long. Consistency day to day matters more than hitting a specific number.')]})

    pages.append({'slug': 'formula-feeding-calculator', 'title': 'Formula Feeding Calculator — ml per Feed by Weight', 'h1': 'Formula Feeding Calculator', 'desc': 'How much formula per feed? Enter baby weight and feeds per day for ml per feed using the 150 ml/kg/day rule, with the safe 120-200 range. Free, no sign-up.', 'category': 'calculator', 'keyword': 'formula feeding calculator ml per feed by weight', 'tool': 'formula', 'args': {}, 'intro': ["Enter your baby's weight in kilograms and how many feeds a day you are doing. The calculator applies the standard 150 ml per kg per day rule and shows the typical amount per feed, the accepted range, and the ounce conversion for bottle markings.", "Feeding guides on formula tins give broad bands by age. Weight-based maths is more accurate: a small 3-month-old and a big one have very different needs, and per-feed amounts follow the day's total, not the month on the box."], 'howto': ['Weigh your baby (or use the last clinic weight) and enter it in kilograms.', 'Count the actual number of feeds in the last 24 hours, including night feeds.', 'Read the typical ml per feed and the range — feed to hunger cues within it, not to the line on the bottle.'], 'faqs': [('How much formula should a baby drink per feed?', 'By the 150 ml/kg/day rule, a 5 kg baby over 7 feeds takes about 107 ml per feed. The accepted range is 120-200 ml/kg/day: the same baby might reasonably take 86-143 ml per feed depending on growth and spitting-up.'), ('When do feed amounts stop rising?', 'Around 5-6 months most babies settle near 150-210 ml per feed and the daily total stops climbing as solids start. Do not keep scaling up with weight forever — the per-day total plateaus in the second half of year one.'), ('Should I wake a baby for a scheduled feed?', "In the first weeks, yes if advised for weight gain; after that, night feeds on demand beat the clock. The calculator sets the day's budget, not a timetable — cluster feeding before bedtime is normal and not a sign of underfeeding."), ('Is more than 200 ml per kg per day dangerous?', 'It can indicate overfeeding or simply a growth spurt — one heavy day is fine, a steady pattern above the range is worth a pediatrician check. Never dilute or concentrate formula to adjust amounts.')]})

    pages.append({'slug': 'protein-intake-calculator', 'title': 'Protein Intake Calculator — Grams per Day by Weight and Goal', 'h1': 'Protein Intake Calculator', 'desc': 'How much protein do you need? Grams per day by bodyweight and goal — cutting, building, active or 60+ — with real-food equivalents. Free, no sign-up.', 'category': 'calculator', 'keyword': 'how much protein per day calculator by weight', 'tool': 'protein', 'args': {}, 'intro': ['Enter your bodyweight and pick your goal. The calculator applies the evidence-based g/kg ranges, shows your daily target with its range, splits it into per-meal doses, and translates it into grams of chicken breast so the number means something at dinner.', 'Supplement sites scale everyone up to 2 g/kg and sell powder. The research says needs depend on what you do: 0.8 g/kg holds a sedentary body, training pushes it to 1.2-1.6, muscle building tops out near 2.2, and cutting raises protein because it protects muscle in a deficit.'], 'howto': ['Weigh yourself and enter the figure in kilograms — the ranges are per kg of total bodyweight.', 'Pick the goal that matches your training week, not your aspiration.', 'Aim the per-meal figure at 3-4 meals a day; hitting the daily total with two giant meals works noticeably worse.'], 'faqs': [('Can I eat too much protein?', 'Healthy kidneys handle high intakes fine — the real cost of overshooting is displacement: protein calories crowd out vegetables and carbs that fuel training. Beyond about 2.2 g/kg when building, extra protein is just expensive energy.'), ('Do I need protein powder to hit these numbers?', 'No — 150 g is 500 g of chicken, or four eggs plus 300 g of greek yogurt plus 200 g of lentils. Powder is convenience, not chemistry: milk protein ranks with the best-studied sources anyway.'), ('Why is my cutting target higher than my bulking one?', 'In a calorie deficit the body burns some protein for energy. Raising intake to 1.8-2.4 g/kg forces that burn to come from food instead of muscle — it is muscle insurance, not extra growth.'), ('Does protein timing matter?', 'The per-meal dose matters more than the clock: near 0.4 g/kg per meal maximises the muscle-building response, so 3-4 evenly spaced protein meals beat one feast. The mythical 30-minute anabolic window is generously wider than sold.')]})

    pages.append({'slug': 'creatine-calculator', 'title': 'Creatine Calculator — Loading and Maintenance Dose by Weight', 'h1': 'Creatine Calculator', 'desc': 'Creatine dose by bodyweight: loading week vs maintenance-only, grams per day, how long a 500 g tub lasts, and the no-cycling truth. Free, no sign-up.', 'category': 'calculator', 'keyword': 'creatine calculator loading maintenance dose', 'tool': 'creatine', 'args': {}, 'intro': ['Enter your bodyweight and choose whether you want a loading week. The calculator gives the loading dose (0.3 g/kg/day split over the day), the maintenance range of 3-5 g/day, and how many days a standard 500 g tub will last you.', 'Creatine labels push oversized scoops and cycling phases. The research is refreshingly boring: monohydrate, 3-5 g a day, no cycling — loading just buys you saturation three weeks faster.'], 'howto': ['Enter your bodyweight in kilograms.', 'Choose a loading week if you want results within days, or maintenance-only if you can wait 3-4 weeks — the destination is identical.', 'Take the dose daily, training days or not; creatine saturates muscle, it is not a pre-workout.'], 'faqs': [('Should I load creatine or just take 5 g?', 'Loading (0.3 g/kg/day for 5-7 days) saturates muscles in about a week; 3-5 g daily gets there in 3-4 weeks. Same endpoint, different speed — skipping loading is simply the gentler, stomach-friendlier route.'), ('Do I need to cycle creatine?', 'No. It is not a stimulant and the body does not downregulate it — cycling just drains the stores you paid to refill, then you reload. Continuous low-dose daily use is the studied pattern behind the performance claims.'), ('Why did I gain 1-2 kg in the first week?', 'Water, by design: creatine pulls water into muscle cells, which is part of how it works. It is not fat and it is not bloat to fix — drink normally and let it be.'), ('Which form should I buy?', 'Monohydrate. It is the cheapest and by far the most-studied form — every fancy variant is marketing on top of the same molecule. Check the label says Creapure or just plain creatine monohydrate and save the difference.')]})

    pages.append({'slug': 'data-usage-calculator', 'title': 'Data Usage Calculator — GB per Month from Your Real Hours', 'h1': 'Data Usage Calculator', 'desc': 'How much data do you actually use? Streaming quality, music, video calls and browsing hours turned into GB per day and month, matched against plan caps. Free, no sign-up.', 'category': 'calculator', 'keyword': 'monthly data usage calculator streaming hours', 'tool': 'datausage', 'args': {}, 'intro': ['Enter your daily hours for streaming, music, video calls and ordinary browsing, and pick your streaming quality. The calculator converts honest per-hour figures into GB per day and per month — the number to compare against your plan cap.', 'Plan-checker tools ask what apps you use and never show the maths. This one prices the lever that actually matters: one hour of 4K costs the same as ten hours of SD, so quality choice moves your bill more than any usage habit.'], 'howto': ['Pick your usual streaming quality — SD 0.7, HD 3, 4K about 7 GB per hour.', 'Enter honest average daily hours for each category, weekend-heavy users should include weekends in the average.', 'Compare the monthly figure with your plan cap, keeping 5-10 GB aside for OS updates and background sync.'], 'faqs': [('How much data does Netflix use per hour?', 'About 0.7 GB in SD, 3 GB in HD and 7 GB in 4K. Auto quality quietly picks the highest your line allows — setting Data Saver per profile is the single biggest GB/month cut available.'), ('How much data do video calls use?', "Roughly 1.2 GB per hour in HD group calls, half that one-to-one. Turning your own camera off barely saves data — you still download everyone else's video."), ('Is 100 GB a month a lot?', 'For one person it is comfortable: about an hour of HD streaming plus music and browsing daily. It collapses with a 4K household — two hours of 4K a day alone burns 420 GB a month.'), ('What eats data that people forget?', 'Cloud photo backups, OS updates and game downloads arrive in multi-GB spikes. If your monthly figure looks impossible from streaming alone, check what the phone uploads overnight before blaming the TV.')]})

    pages.append({'slug': 'flight-delay-compensation-calculator', 'title': 'Flight Delay Compensation Calculator — EU261 Fixed Amounts', 'h1': 'Flight Delay Compensation Calculator', 'desc': 'What your delayed flight is worth: EU261/UK261 fixed compensation by distance and arrival delay, plus care and receipt rules. Free, no sign-up.', 'category': 'calculator', 'keyword': 'flight delay compensation calculator eu261', 'tool': 'flightdelay', 'args': {}, 'intro': ['Enter your flight distance in km and how late you arrived, and get the fixed compensation the EU261 (and UK261) rules attach: 250, 400 or 600 by distance band, with the long-haul reduction window handled.', 'Claims-firm sites bury the band table under commission pitches. This one shows the arithmetic plainly, plus the two details that decide real claims: the clock is arrival delay at your final destination, and extraordinary circumstances excuse the fixed sum but never the duty of care.'], 'howto': ['Find the great-circle distance of your flight (any flight-distance site) and enter it in kilometres.', 'Enter how late you actually arrived at the final destination on your ticket, not how late you departed.', 'Read the band amount, then keep every receipt - meals, hotel, taxis and rebooking costs are claimable on top.'], 'faqs': [('Does a 2-hour departure delay count?', 'Not on its own: the 3-hour clock is arrival delay at the final destination. A 2-hour late takeoff that lands 3:15 late qualifies; a 4-hour departure delay made up to a 2:30 arrival does not.'), ('What are extraordinary circumstances?', 'Severe weather, air-traffic control strikes and hidden manufacturing faults can excuse the airline from the fixed compensation - but never from duty of care: meals, communication and hotels during the wait are still owed, with receipts.'), ('How long do I have to claim?', 'Years, not days: six in England and Wales, and similar limitation periods across the EU. Old delays are still worth checking - airlines count on people assuming it is too late.'), ('Do I need a claims company?', 'No. They typically take 25-35% of a fixed amount the airline owes anyway. Write to the airline directly with your booking reference, delay facts and receipts first; escalate to the national enforcement body or aviation ombudsman if refused.')]})

    pages.append({'slug': 'subscription-cost-calculator', 'title': 'Subscription Cost Calculator — The Real Yearly Total', 'h1': 'Subscription Cost Calculator', 'desc': 'Add up what your subscriptions really cost per year: four lines with monthly, quarterly or yearly billing, biggest-cost callout and cut-one savings. Free, no sign-up.', 'category': 'calculator', 'keyword': 'subscription cost calculator yearly total', 'tool': 'subs', 'args': {}, 'intro': ["Enter each subscription's price and how often it bills. The calculator normalises everything to monthly and yearly totals, flags the biggest line, and shows what cutting it actually saves per year.", 'Services price monthly because 12.99 feels small and 155.88 does not. This audit does the multiplication the pricing page hopes you skip - and it never asks which brands you use.'], 'howto': ["List your streaming, software, cloud and app subscriptions - check your phone's subscription page and card statement, most people find one they forgot.", 'Enter each price with its billing cycle; yearly plans get divided, not ignored.', "Look at the biggest-cost line first: pausing or cancelling it saves the yearly figure shown, which is usually a utility bill's worth."], 'faqs': [('How much do people spend on subscriptions on average?', 'Households commonly run 50-220 per month across streaming, cloud, apps and software - the forgotten half of the list is where the money leaks, not the one flagship service you actually use.'), ('Is annual billing worth it?', 'For anything you kept continuously all last year, yes: annual discounts run 15-20%, effectively a month or two free. For anything you pause seasonally, stay monthly - renewing discipline beats the discount.'), ('Is pausing better than cancelling?', 'Often: several streaming services hold your watchlist and profile for 1-3 months on pause, and gym chains freeze memberships for holidays. Cancel outright when the pause is just a way to keep paying.'), ('How do I find subscriptions I forgot?', "Check the subscriptions page on your phone, then search a year of card statements for recurring merchant names. Anything you cannot remember opening last month is the audit's first cut.")]})

    pages.append({'slug': 'silver-value-calculator', 'title': 'Silver Value Calculator — Melt Value by Weight and Purity', 'h1': 'Silver Value Calculator', 'desc': 'What is my silver worth? Weight, purity (999/925/800) and current spot price give the melt value, per-gram figure and a realistic dealer offer range. Free, no sign-up.', 'category': 'calculator', 'keyword': 'silver value calculator melt sterling', 'tool': 'silverval', 'args': {}, 'intro': ["Enter the weight in grams, the purity, and today's spot price per troy ounce. The calculator returns the melt value, the fine-silver content, the per-gram figure, and a realistic dealer-offer estimate - the number scrap buyers actually quote.", 'Silver sites quote spot price and quietly buy at a discount. This tool makes the discount explicit: scrap dealers pay 85-95% of melt, so you can weigh any offer instantly instead of trusting the counter.'], 'howto': ['Weigh the silver in grams on a kitchen scale accurate to a gram - jewellery and cutlery batches first, bullion coins by their stamped weight.', 'Find the purity: 999 on bullion, 925 hallmark for sterling, 800 on older continental silver. Unmarked or plated items are worth near zero by weight.', "Look up today's spot price per troy ounce, enter it, and compare the dealer offer you get against the 88% mid-estimate shown."], 'faqs': [('How much is sterling silver worth per gram?', 'Melt value is purity times spot divided by 31.1035: at 30 per troy ounce, 925 silver runs about 0.89 per gram, 999 bullion about 0.96. Multiply by weight for the melt total.'), ('Why do dealers pay less than spot?', 'They carry refining costs, testing risk and market movement between buying and melting. Fair scrap offers sit at 85-95% of melt; below that, walk - and get quotes from two dealers minimum for anything over a few hundred grams.'), ('Is my old cutlery worth more as silverware?', 'Often yes: full canteens by known makers and antique pieces carry collector value above melt. Check sold listings on two marketplaces before selling anything with a date, portrait or maker mark by weight.'), ('What is the difference between plated and sterling?', 'Sterling is 92.5% silver all the way through; plated ware is a few microns of silver over base metal. A magnet is a quick screen (silver is not magnetic), but the hallmark is the verdict - no 925 or 999 mark, assume plate.')]})

    pages.append({'slug': 'yarn-yardage-calculator', 'title': 'Yarn Yardage Calculator — Metres Needed from Your Swatch', 'h1': 'Yarn Yardage Calculator', 'desc': 'How much yarn does your project need? Swatch area and yarn used scaled to project size, with skein count, 15% buffer and dye-lot advice. Free, no sign-up.', 'category': 'calculator', 'keyword': 'yarn yardage calculator swatch', 'tool': 'yarn', 'args': {}, 'intro': ['Knit and measure a swatch, note how many metres it ate, then enter it with your project dimensions. The calculator scales swatch to project, adds a 15% buffer for tension drift and frogging, and converts to skeins.', 'Pattern databases and yarn-brand sites quote yardage for their gauge, not yours. Your swatch is the only gauge that matters - this tool makes it the yardstick instead of a formality.'], 'howto': ['Knit a swatch at least 10×10 cm in the project stitch, block it, and let it relax before measuring.', 'Find the yarn it used: unpick and measure, or weigh the swatch and convert with grams-per-metre from the ball band.', "Enter both with the project's finished dimensions and your skein size; buy the skein count shown in one dye lot."], 'faqs': [('Why does my swatch need blocking first?', 'Blocking relaxes the stitches to their final geometry - a pre-block swatch can lie by 5-10% in both directions, which compounds to a quarter of your yardage on a big project. Measure what the fabric will be, not what it is on the needle.'), ('What is the 15% buffer for?', 'Tension drifts over a long project, sizing gets adjusted, and the neckline everyone reknits eats yarn twice. Fifteen percent is the quiet difference between finishing on the last skein and shopping for a dye lot that no longer exists.'), ('Can I use grams instead of metres?', 'Yes - run the maths in grams throughout (swatch grams × area ratio) and convert at the end with the ball band. Weighing on a kitchen scale is usually more accurate than estimating unpicked metres.'), ('Why must all skeins come from one dye lot?', 'Dye lots differ subtly in shade, and the difference shows as a visible stripe where the new ball starts. Buy the full count up front, and wind one extra from the same lot as your repair skein for years to come.')]})

    pages.append({'slug': 'knitting-cast-on-calculator', 'title': 'Knitting Cast-On Calculator — Stitches for Hats by Gauge', 'h1': 'Knitting Cast-On Calculator', 'desc': 'How many stitches to cast on for a hat: head circumference, your blocked gauge, negative ease and the pattern multiple handled in one number. Free, no sign-up.', 'category': 'calculator', 'keyword': 'knitting hat cast on stitches calculator', 'tool': 'caston', 'args': {}, 'intro': ["Enter head circumference, your blocked gauge per 10 cm, the negative ease, and your pattern's stitch multiple. The calculator gives the cast-on count adjusted to the multiple, the raw figure, and the finished relaxed width.", 'Ball-band gauges and generic tables create hats that fit nobody. This calculator uses your gauge and the physics of negative ease - the 2-3 cm by which knitted hats are deliberately smaller than the head.'], 'howto': ['Measure the head where the brim will sit, above the ears - not the forehead, and round up half a centimetre for comfort.', "Swatch in the brim stitch, block it, and count stitches per 10 cm; enter that figure, never the band's.", 'Pick your ease (2.5 cm is standard for ribbed brims) and the pattern multiple; knit an inch of brim and try it on before committing.'], 'faqs': [('What is negative ease in knitting?', 'The finished piece is smaller than the body it covers: knitted fabric stretches up to a third of its width and relaxes back, so a hat 2-3 cm under head circumference grips instead of sliding. Ribbed brims can take up to 5 cm; stiff stitch patterns barely 1.'), ('Why did the multiple change my stitch count?', 'Ribbing, cables and lace repeat in fixed block sizes, so the cast-on must be a multiple of that block. The calculator rounds to the nearest multiple - if that shifts you more than 2-3 stitches from raw, change needle size rather than stretching the count.'), ('Do I measure gauge before or after blocking?', 'After, always. Blocking usually widens and shortens stockinette, and the hat gets blocked too - the pre-block gauge is a number for a fabric that will never exist. For stretchy brims, measure the swatch slightly stretched as it will be worn.'), ('How do I adapt this to a cowl or sweater band?', "Same arithmetic, new circumference: measure where the piece sits, subtract the ease, multiply by stitches-per-cm. For pull-on cowls keep at least 2 cm negative ease or they slide; for sweaters follow the pattern's stated ease since it shapes the silhouette.")]})

    pages.append({'slug': 'curtain-fabric-calculator', 'title': 'Curtain Fabric Calculator — Metres by Track Width and Fullness', 'h1': 'Curtain Fabric Calculator', 'desc': 'How much fabric for curtains? Track width, finished drop, fullness ratio and roll width give panels, cut length and total metres, with hem and repeat advice. Free, no sign-up.', 'category': 'calculator', 'keyword': 'curtain fabric calculator metres', 'tool': 'curtain', 'args': {}, 'intro': ['Enter your track or pole width, the finished drop, the fullness your heading style needs, and the fabric roll width. The calculator works out panel count, cut length with hem and heading allowances, and total metres to buy.', 'Fabric-shop calculators assume one window and hide the allowances. This one shows the 30 cm per panel that proper hems eat, and why fullness - not window size - is the number that moves the bill.'], 'howto': ['Measure the track or pole, not the window: pole width plus finials is the working figure, fitted where the curtain will hang.', 'Measure finished drop from ring eye or track to the intended hem line - sill, radiator top or floor, minus 1 cm clearance.', 'Pick fullness by heading: 2× for pencil pleat, 2.5× for pinch pleat, 1.5× for eyelet flats, then read panels and metres.'], 'faqs': [('How much fabric do I need for standard curtains?', 'A 150 cm track at 137 cm drop in pencil pleat takes about 5.2 m across 3 panels of standard 137 cm fabric. The counterintuitive part: doubling the window width less than doubles the fabric when panels already overshoot the roll width.'), ('What is curtain fullness?', 'The ratio of gathered fabric width to track width. Pencil pleat wants twice the track width to fold into crisp columns; pinch pleat needs two and a half for the fixed pleats; eyelet headings manage with one and a half because each wave uses less cloth.'), ('Why add 30 cm per panel?', 'A double-turned 15 cm bottom hem gives the weight that makes curtains hang in folds instead of flapping, and the heading allowance tops the panel. Skimp on both and the curtain looks home-made from across the room, whatever the fabric cost.'), ('How does pattern repeat change the maths?', 'Each drop must start at the same point of the pattern, so add one repeat per panel beyond the first and buy from one dye lot. Solids and tone-on-tone weaves skip this entirely - one reason plain curtain fabric is cheaper to make up than it looks.')]})

    pages.append({'slug': 'commute-cost-calculator', 'title': 'Commute Cost Calculator — Car vs Transit, the Honest Totals', 'h1': 'Commute Cost Calculator', 'desc': 'What does your commute really cost? Car all-in per km versus transit pass, per year and per day, with the fuel-is-a-third truth. Free, no sign-up.', 'category': 'calculator', 'keyword': 'commute cost calculator car vs public transport', 'tool': 'commute', 'args': {}, 'intro': ['Enter your one-way distance, commuting days, the true per-km cost of running your car, annual parking, and your transit pass price. The calculator totals both options per year and per commuting day - the comparison employers never put in the offer letter.', 'Commute comparisons usually stop at fuel versus ticket price. The honest car figure multiplies distance by an all-in rate of 0.35-0.55 per km, because depreciation, maintenance, tyres and insurance ride along with every kilometre - fuel is only about a third of it.'], 'howto': ['Measure one-way door-to-door distance for each mode (maps apps give it per mode - transit is often shorter than driving).', 'Set the per-km figure to an all-in rate, not pump price; 0.45 is a sensible middle for a petrol car.', 'Enter parking and pass prices and read the yearly gap - then weigh it honestly against door-to-door time and what the train time is worth to you.'], 'faqs': [('What is the true cost per km of driving?', 'All-in figures run 0.35-0.55 per km for a typical petrol car: fuel roughly a third, with depreciation the largest single block, then maintenance, tyres and insurance. Using pump price alone understates driving cost by about two-thirds.'), ('Is a monthly transit pass always cheaper?', 'For commutes over about 8 km each way at 4-5 days a week, almost always. Under that, or for hybrid patterns of 2-3 office days, pay-as-you-go fares can beat the pass - price both before committing.'), ('How do I compare when I already own the car?', "Separate fixed from marginal: insurance and depreciation happen regardless, so the commute's marginal cost is km-rate plus parking. But be honest - if commuting is why the household needs the second car, the fixed costs belong in the comparison."), ('Does working from home change the maths?', 'Enormously: one fewer office day a week cuts the annual figure by 20%. Hybrid workers should enter actual commuting days, not a nominal full-time week - most overestimate their office attendance by a day.')]})

    pages.append({'slug': 'mileage-reimbursement-calculator', 'title': 'Mileage Reimbursement Calculator — Total Owed for Your Trips', 'h1': 'Mileage Reimbursement Calculator', 'desc': 'Total mileage reimbursement: distance times rate, in miles or km, with the gap versus your true cost per km and fuel-only warning. Free, no sign-up.', 'category': 'calculator', 'keyword': 'mileage reimbursement calculator total owed', 'tool': 'mileage', 'args': {}, 'intro': ['Enter the distance you drove for work, your reimbursement rate, and optionally what a kilometre actually costs you. The calculator totals what you are owed, shows the per-100 figure, and quantifies the gap if your rate is fuel-only.', 'Mileage tables on HR portals give you a rate and stop there. This one tells you what the rate means: standard rates bundle fuel with maintenance, tyres, insurance and depreciation - and accepting a fuel-only rate quietly donates about two-thirds of the real cost.'], 'howto': ['Total your business distance for the period from your trip log - contemporaneous notes, not reconstruction.', 'Enter the rate your employer, client or national tax authority publishes (rates are set per year - check the current one).', 'Optionally enter your true cost per unit to see whether the rate covers you, and by how much per period.'], 'faqs': [('What rate should I claim per mile or km?', "Use your national tax authority's published standard rate - they exist precisely so you do not have to itemise, and claiming them stays tax-free. The headline figures move yearly, so check the current publication rather than reusing last year's."), ('Why is a fuel-only reimbursement a bad deal?', "Fuel is roughly 30-40% of a car's per-km cost; maintenance, tyres, insurance and depreciation make up the rest. A fuel-only rate pays the petrol and leaves you funding the wear - over a year of typical field work, a four-figure difference."), ('What records do I need for mileage claims?', 'Date, start and end points, purpose, and distance per trip, logged as it happens. Reconstructed logs are the classic audit rejection; a recurring calendar entry per regular route plus occasional photos of the odometer makes the log self-writing.'), ('Do commuting miles count?', 'No - the ordinary home-to-work journey is personal almost everywhere. But a direct business trip from home to a client, or a detour to the office en route to a site visit, qualifies in most systems. The first and last leg home does not.')]})

    pages.append({'slug': 'carpool-savings-calculator', 'title': 'Carpool Savings Calculator — What Sharing the Ride Saves You', 'h1': 'Carpool Savings Calculator', 'desc': 'What carpooling actually saves: shared driving cost per person per year, CO₂ taken off the road, and the schedule rules that keep a pool alive. Free, no sign-up.', 'category': 'calculator', 'keyword': 'carpool savings calculator per year', 'tool': 'carpool', 'args': {}, 'intro': ['Enter the one-way distance, days per week, your driving cost per km, and how many people share the ride. The calculator splits the annual cost per person, shows what each sharer saves against driving alone, and the CO₂ the arrangement removes.', 'Ride-hailing apps price a trip; pool calculators usually stop at fuel. This one splits the honest all-in driving cost, puts a kilogramme figure on the emissions, and - the part apps skip - sets the ground rules that decide whether a pool survives its first late meeting.'], 'howto': ['Enter the one-way distance and days per week you actually commute - 46 working weeks keeps holidays honest.', 'Use an all-in per-km cost (0.45 default), not fuel alone, so the driver is not quietly subsidising passengers.', "Pick the group size and read each person's saving; agree the late-evening rule before the first shared ride, not after."], 'faqs': [('How is carpool cost normally split?', 'By distance-driven cost share: total running cost divided by occupants, sometimes with the driver keeping a larger share for the ownership risk. Fuel-only splits undercharge the driver by about two-thirds of the true cost per km.'), ('Does carpooling affect my insurance?', 'Genuine cost-sharing between commuters is treated as shared expenses, not commercial hire, by mainstream insurers. Charging strangers a profit per seat is different and needs hire-and-reward cover - a pool of colleagues is fine.'), ('How much CO₂ does carpooling save?', 'A typical petrol car emits about 170 g of CO₂ per km, so a 25 km each-way commute driven 5 days a week books roughly 2 tonnes a year. Three sharers in one car remove one whole car - about 1.3 tonnes saved per person, per year.'), ('What kills a carpool in practice?', "Schedule rigidity: one person's late meeting strands the others, twice, and the pool dies. Pools that last agree a written norm - a departure window, a solo-day allowance each month, and a backup driver - before the first missed connection, not after.")]})

    pages.append({'slug': 'ebike-range-calculator', 'title': 'E-Bike Range Calculator — Real km from Your Battery', 'h1': 'E-Bike Range Calculator', 'desc': 'Real e-bike range, not brochure range: battery Wh divided by honest Wh/km for your assist level, with cold-weather and battery-health reality. Free, no sign-up.', 'category': 'calculator', 'keyword': 'e-bike range calculator wh', 'tool': 'ebikerange', 'args': {}, 'intro': ['Enter your battery capacity in Wh, your typical assist level, and the reserve you keep. The calculator gives the realistic range in the middle, plus the eco and high-assist extremes - the numbers to plan a commute or a loop around.', 'Manufacturer range figures assume a light rider, flat terrain and eco mode. Real riding lands 25-40% below the sticker; this calculator starts from usable Wh and honest consumption instead of the brochure.'], 'howto': ['Find the Wh figure on the battery label or spec sheet (voltage × amp-hours).', 'Match the assist style you actually ride - not the one you plan to ride.', 'Keep a 10% reserve in the planning figure and compare the result against your longest regular ride.'], 'faqs': [('How far does a 500 Wh e-bike go?', 'At honest mixed-assist consumption of 15 Wh/km, about 30 km of usable range with a 10% reserve - eco stretches it past 45 km, full assist trims it near 20 km. Winter and hills knock a further 15-25% off.'), ('Why is my real range below the manufacturer figure?', 'The sticker assumes a 70 kg rider, flat ground, no wind, eco assist and a fresh battery. Add cargo, hills, cold and the highest assist level and a 25-40% shortfall is normal, not a fault.'), ('Does cold weather really cut e-bike range?', 'Yes - lithium chemistry slows below 10 °C, costing 15-25%, and denser winter air plus studded tyres add drag. The capacity returns when the battery warms; storing and charging it indoors helps.'), ('How should I charge to protect the battery?', 'Daily rides: charge to 80-90% rather than full, avoid deep discharges, and store around half-charge if the bike rests for weeks. Shallow partial cycles are kind to lithium - the old full-cycle habit belongs to nickel batteries.')]})

    pages.append({'slug': 'bike-saddle-height-calculator', 'title': 'Bike Saddle Height Calculator — by Inseam and Riding Type', 'h1': 'Bike Saddle Height Calculator', 'desc': 'Correct saddle height from your inseam: LeMond factor for road, comfort and MTB variants, plus the knee-pain diagnostics. Free, no sign-up.', 'category': 'calculator', 'keyword': 'bike saddle height calculator inseam', 'tool': 'saddle', 'args': {}, 'intro': ['Measure your inseam and pick your riding style. The calculator applies the LeMond factor (0.883 for road, softened for city and MTB) and gives the saddle height in cm and mm - the single bike-fit number worth more than everything else combined.', 'Shop fits price like a service and generic charts skip the method. This one shows the arithmetic, the measurement that makes it work, and the knee-pain table that tells you which way to nudge it.'], 'howto': ['Measure inseam barefoot against a wall: press a firm book into the crotch and measure floor to book top.', 'Enter the figure and choose the factor for your bike type.', 'Set saddle top to bottom-bracket distance to the result, ride a week, then adjust in 2-3 mm steps by how your knees report.'], 'faqs': [('What is the LeMond formula?', "Saddle height equals inseam × 0.883, measured from saddle top to bottom-bracket axle - popularised by Greg LeMond's coach and still the best one-line fit in cycling. Upright city bikes run 0.87, mountain bikes 0.88 for clearance and control."), ('Is my knee pain from saddle height?', 'Usually: front-of-knee pain points to a saddle too low (compressed angle at the top), back-of-knee or hip rocking to one too high (overreaching at the bottom). Fix height first in 2-3 mm steps before buying insoles or new pedals.'), ('How do I measure inseam correctly?', 'Barefoot, back to a wall, firm book or spirit level pressed into the crotch at sitting-bone level, measured straight down to the floor. Jeans and soft fabric add a centimetre of error - and 1 cm of inseam error becomes 0.9 cm of saddle error.'), ('What is the heel check?', 'A cross-check, not a formula: put your heel on the pedal at the bottom of the stroke - the leg should be perfectly straight without your hip dropping. Then ride on the ball of the foot; if you now point at the bottom, the saddle is a touch high.')]})

    pages.append({'slug': 'ebike-charging-cost-calculator', 'title': 'E-Bike Charging Cost Calculator — Cents per Charge and per 100 km', 'h1': 'E-Bike Charging Cost Calculator', 'desc': 'What an e-bike really costs to run: charge cost from battery Wh and your electricity price, per 100 km and per year, with charger losses counted. Free, no sign-up.', 'category': 'calculator', 'keyword': 'e-bike charging cost per charge', 'tool': 'ebikecharge', 'args': {}, 'intro': ['Enter your battery Wh, electricity price, and how much of the battery a typical charge uses. The calculator prices the charge, the cost per 100 km, and a 3,000 km year - the comparison that makes car-versus-e-bike arithmetic laughable.', 'Cost pages usually quote a full-charge figure and stop. This one counts the 12% charger losses, scales to your actual partial charging habit, and points at where e-bike money really goes: not electrons, but the pack itself.'], 'howto': ['Read battery Wh from the label or spec sheet.', 'Enter your electricity price per kWh from your latest bill - night tariffs can halve it.', 'Set your typical charge use (top-ups count too) and read the per-charge, per-100-km and yearly figures.'], 'faqs': [('How much does it cost to charge an e-bike?', 'A 500 Wh battery from empty costs around one sixth of a kWh-price unit at 0.30 - roughly the price of a text message. Typical partial top-ups cost a fraction of that, losses included.'), ('Do charging losses matter?', "Wall energy runs about 10-15% above the battery's rated Wh because chargers and the battery itself waste heat. At e-bike scale the absolute waste is pennies a year - count it for honesty, not because it changes decisions."), ('Is an e-bike cheaper than a car per km?', 'By two orders of magnitude on energy: 100 km costs cents on an e-bike versus fuel, plus you remove parking, congestion charges and, often, a whole second car. The depreciation you do not pay is the real subsidy.'), ('When does the battery need replacing and what does that cost?', 'Most packs deliver 500-900 full cycles before capacity drops to 80% - for a 3,000 km-year rider, roughly 7-13 years. Spread over the km actually ridden, replacement is a few cents per km; unused, it is the most expensive shed ornament you own.')]})

    pages.append({'slug': 'tv-size-calculator', 'title': 'TV Size Calculator — Right Screen Size for Your Sofa Distance', 'h1': 'TV Size Calculator', 'desc': 'What size TV for your room? Sofa distance and resolution give the right diagonal in inches, with screen width and the too-close limit. Free, no sign-up.', 'category': 'calculator', 'keyword': 'tv size calculator viewing distance', 'tool': 'tvsize', 'args': {}, 'intro': ['Measure or estimate your sofa-to-screen distance and pick the content resolution you actually watch. The calculator gives the right diagonal in inches, the real width in centimetres for stands and walls, and the too-close limit for that size.', 'Retail size guides nudge you up a bracket because bigger sells. The honest rule - distance divided by 1.5 for 4K, 2.2 for 1080p - lands where pixels disappear and the picture fills your view, not the shop floor.'], 'howto': ['Measure from the screen to where you actually sit - the farthest seat if the family spreads out.', 'Pick the resolution you mostly watch: streams and discs in 4K, older broadcast at 1080p.', "Check the width figure against your stand or wall section, and mind the TV's own feet - they are often wider than expected."], 'faqs': [('How big a TV for 2.5 metres?', 'About 65 inches for 4K content (2.5 m ÷ 1.5 ÷ 2.54 ≈ 65). The same seat with 1080p broadcast suits roughly 45 inches - closer to the bigger figure and compression artefacts start showing.'), ('Is a TV ever too big for the room?', 'Functionally yes: past the too-close limit you resolve pixels and scan lines and eyes tire faster. Cosmetically, a screen that dominates the wall is a taste question - the calculator gives the functional ceiling, decoration is yours.'), ('Does 4K really matter at sofa distance?', 'Yes, increasingly so: 4K packs pixels fine enough that you can sit much closer for the same image quality, which is why the 4K divisor is smaller. At 1080p the same closeness resolves the grid - 4K lets big screens work in smaller rooms.'), ('How much space do I need for a 65-inch TV?', 'The panel alone is about 145 × 84 cm; add 10-20 cm if it stands on feet, more for a soundbar. Measure the wall section or console before buying - doorways on delivery day are the other classic discovery.')]})

    pages.append({'slug': 'fish-tank-stocking-calculator', 'title': 'Fish Tank Stocking Calculator — How Many Fish Your Tank Supports', 'h1': 'Fish Tank Stocking Calculator', 'desc': 'How many fish for your tank? Litres and adult fish size with community, cichlid and goldfish stocking rules, plus the nitrogen-cycle reality. Free, no sign-up.', 'category': 'calculator', 'keyword': 'how many fish in a tank calculator litres', 'tool': 'fishtank', 'args': {}, 'intro': ['Enter your tank volume in litres, the adult size of the fish you want, and the stocking type. The calculator applies the centimetre-per-litre rule with the right multiplier, and sizes the weekly water change that keeps the chemistry stable.', 'Fish-shop advice counts the juveniles in the bags. This calculator counts the adults they become - the difference between a thriving tank and the silent ammonia crash that ends most first aquariums.'], 'howto': ['Use the real water volume (tanks hold less than the label once gravel and filters move in - knock off 10%).', 'Look up the ADULT size of your species, not the shop size, and enter it in cm.', 'Pick the stocking type - community, territorial cichlids or waste-heavy goldfish - and cycle the tank before the first fish ever goes in.'], 'faqs': [('What is the 1 cm per litre rule?', 'A rough adult-size budget: total body length of adult fish per litre of water. It works for slim-bodied tropical communities; goldfish need 2.5 L per cm because their waste outruns their size, and territorial cichlids need extra room for behaviour, not just chemistry.'), ('Why does adult size matter so much?', 'Shops sell juveniles, and most aquarium fish grow several times their purchase size within a couple of years. A tank stocked at shop size is overstocked by the time the fish mature - which shows up as persistent ammonia, torn fins and algae.'), ('How long should a tank cycle before adding fish?', 'Four to six weeks without fish: the beneficial bacteria that convert ammonia live on filter media and take weeks to colonise. Fish-in cycling is possible with daily testing and changes, but fishless cycling with a drop of pure ammonia is kinder and surer.'), ('How much water should I change weekly?', 'About 25%, dechlorinated and temperature-matched, vacuuming the gravel as you go. Consistency beats volume: a steady quarter weekly keeps nitrates under control without destabilising the chemistry the fish have adapted to.')]})

    pages.append({'slug': 'laundry-detergent-calculator', 'title': 'Laundry Detergent Calculator — The Right Dose per Wash', 'h1': 'Laundry Detergent Calculator', 'desc': 'How much detergent per wash? Load size, soil level and water hardness give the right liquid or powder dose - and why overdosing makes clothes worse. Free, no sign-up.', 'category': 'calculator', 'keyword': 'laundry detergent amount per load calculator', 'tool': 'laundry', 'args': {}, 'intro': ['Enter your load size, how dirty the wash is, and your water hardness. The calculator gives a right-sized dose in millilitres, the powder equivalent, and what that dose costs per year at your detergent price.', 'Detergent packs print tables that flatter their sales. The honest dose is smaller than most people pour: excess surfactant does not clean better - it deposits on fibres, stiffens towels and feeds the mould behind that washed-but-smelly machine.'], 'howto': ["Check your machine's rated drum size and weigh or estimate a typical load (a full drum of dry clothes runs 4-6 kg for most households).", "Find your water hardness from your water supplier's website - it changes the dose by up to 25%.", 'Dose to the figure, run a wash, and adjust once: clothes smelling of nothing is the target, not a perfume cloud.'], 'faqs': [('How much detergent should I really use?', 'An 8 kg drum at normal soil and medium hardness takes about 50 ml of liquid or a 25-30 g powder scoop. Light washes in soft water run under 40 ml; hard water and sports kit push 65-80 ml. Most people pour one and a half to two times these figures.'), ('What happens if I use too much detergent?', 'The surplus cannot rinse out: it coats fibres as a grey or stiff film, makes towels water-repellent and crunchy, traps odour, and feeds the biofilm that makes machines smell. It also fades colours faster - the classic signs are suds in the rinse and clothes that feel slick when wet.'), ('Does water hardness change the dose?', "Yes - hardness minerals deactivate part of the surfactant, so hard water needs about 25% more and soft water needs 15% less. Soft-water households that keep the packet's default dose are the most overdosed group there is."), ('Are detergent pods correctly dosed?', 'For full loads, roughly; pods are pre-measured for an average drum and cannot flex down for a half load, so small washes come out over-dosed. Two pods for a big or dirty load is fine - three is marketing.')]})

    pages.append({'slug': 'moving-cost-calculator', 'title': 'Moving Cost Calculator — Professional vs DIY, Honestly', 'h1': 'Moving Cost Calculator', 'desc': 'What should your move cost? Professional crew vs DIY van with fuel, pizza wages and boxes - with the access traps that inflate quotes. Free, no sign-up.', 'category': 'calculator', 'keyword': 'moving cost calculator professional vs diy', 'tool': 'movecost', 'args': {}, 'intro': ['Enter your home size, distance, the local hourly rate per mover, call-out fee and van hire price. The calculator totals a professional crew and an honest DIY move side by side - including the pizza, fuel and boxes the DIY column always forgets.', 'Removal-company quote tools take commissions from the companies. This comparison prices both columns the same honest way and tells you when the crew is genuinely worth it - which is more often than DIY pride expects.'], 'howto': ['Pick your home size; the built-in hours-per-size come from typical crew jobs, not brochure minimums.', 'Enter your local hourly mover rate and call-out fee - ask two companies to sanity-check the figures.', 'Read the gap against one day of your salary: under that, the crew is usually the rational buy.'], 'faqs': [('How much do movers cost for a 1-bedroom move?', 'At 40 per mover-hour, a 1-bedroom (4 hours, 2 movers) with a 50 call-out runs about 370. The same move DIY - van, fuel, pizzas, boxes - lands near 230 plus two days of your back.'), ('Why do moving quotes vary so much?', 'Access, not volume: stairs without a lift, long carries, narrow access for the van and waiting time add billed hours. Two quotes for the same flat routinely differ 50% because one estimator walked the route and the other guessed from photos.'), ('When is DIY moving worth it?', "Ground-floor to ground-floor, short distance, a friend with a van, and no piano or heirlooms. Past a day's salary of savings, or up any serious staircase, the professional column wins on money once damaged furniture and your time are priced."), ('What hidden fees should I watch for?', 'Stair surcharges, weekend and end-of-month premiums (20-30%), packing-materials markup, waiting time if keys are delayed, and fuel levies. Ask for the all-in figure in writing - the hourly rate is the ad, the access fees are the invoice.')]})

    pages.append({'slug': 'moving-boxes-calculator', 'title': 'Moving Boxes Calculator — How Many Boxes by Bedrooms', 'h1': 'Moving Boxes Calculator', 'desc': 'How many moving boxes do you need? Bedrooms and packing style give the box count, size mix, tape and bubble wrap - plus the packing pace. Free, no sign-up.', 'category': 'calculator', 'keyword': 'how many moving boxes calculator bedrooms', 'tool': 'boxcalc', 'args': {}, 'intro': ['Enter your bedroom count and how honestly you pack. The calculator gives the box total, the small/medium/large split, tape and bubble wrap counts, and how many solo packing days the job takes at a realistic pace.', 'Box-seller calculators inflate counts because boxes are the product. This one prices the whole packing job - and its real advice is which things go in which size, where most of the damage and back strain is decided.'], 'howto': ["Count bedrooms; be honest about the packing style - the 'everything goes' multiplier exists for a reason.", 'Buy the size mix shown: small for books, medium for kitchen, large only for light bulky things.', 'Start three weeks out at the pace shown, storage rooms first, and pack the first-night box for the car.'], 'faqs': [('How many boxes does a 1-bedroom flat need?', 'About 35 for a normal household - 10 small, 16 medium, 9 large. Minimalists land near 25; collectors of everything should budget 50 and start two weekends earlier than feels necessary.'), ('What goes in which box size?', "Books and dishes in small boxes (20 kg is the lifting limit, not the box's), kitchen and general in medium, and only light bulky items - bedding, lampshades, plastics - in large. Heavy-in-large is how boxes die on staircases."), ('Where can I get free moving boxes?', 'Supermarkets, liquor stores and bookshops - sturdy double-corrugated and free. Refuse anything damp or from produce floors, and flatten-and-store them dry; wet cardboard loses half its strength before it looks weak.'), ('What is the first-night box?', 'One box that rides in your car, not the van: bed sheets, kettle, mugs, chargers, toilet paper, basic tools and a change of clothes. It is the difference between a functioning first evening and excavating a wall of boxes at midnight.')]})

    pages.append({'slug': 'moving-timeline-planner', 'title': 'Moving Timeline Planner — Week-by-Week Plan from Your Moving Date', 'h1': 'Moving Timeline Planner', 'desc': "Enter your moving date and get the week-by-week plan: when to book movers, declutter, change addresses and pack - with this week's task highlighted. Free, no sign-up.", 'category': 'calculator', 'keyword': 'moving timeline checklist weeks before', 'tool': 'movetl', 'args': {}, 'intro': ['Pick your moving day and the planner works backwards: eight weeks for bookings, six for decluttering, four for utilities and address changes, then the packing push - with the current phase highlighted and a boxes-per-day pace to hold.', 'Checklists exist as static PDFs that ignore your date. This one lives on your actual countdown, tells you what this specific week is for, and puts the pace number next to it so the last week is not a collapse.'], 'howto': ['Enter the moving date - the plan regenerates from whatever today is.', 'Read the highlighted phase and do only that; early packing of everyday stuff is how lives get unbearable for a month.', 'Keep the page bookmarked and revisit weekly - the title tab shows the days remaining.'], 'faqs': [('How many weeks before should I start preparing?', 'Eight weeks is the comfortable standard: enough to get three mover quotes, declutter without panic and pack storage rooms early. Compressed to two weeks it still works - but decluttering dies first, and you pay to move things you should have dumped.'), ('When should I book the moving company?', 'As soon as the date is plausible, 4-8 weeks out: end-of-month and weekend dates in busy seasons go first and cost most. Book a flexible window if your completion date can still slip.'), ('What should I pack first and last?', 'First: storage rooms, books, seasonal gear - anything untouched weekly. Last: kitchen essentials, bathroom and the beds. The first-night box never enters the van; it rides in your car.'), ('What do people always forget when moving?', 'Meter photos on both ends, defrosting the freezer, the electronics cabling photo, parking permits for both addresses, and the address change for subscriptions and government services. The timeline schedules all of them early enough to fix.')]})

    pages.append({'slug': 'heating-cost-calculator', 'title': 'Heating Cost Calculator — Season Cost by Area, Insulation and System', 'h1': 'Heating Cost Calculator', 'desc': 'What will this winter cost? Home area, insulation and heating system give the season bill, monthly figure and the 1 °C setback saving. Free, no sign-up.', 'category': 'calculator', 'keyword': 'heating cost calculator per season', 'tool': 'heating', 'args': {}, 'intro': ['Enter your home area, insulation level, heating system and energy price. The calculator estimates the season cost, the monthly figure over a 180-day season, and what every degree off the thermostat saves.', 'Supplier calculators quote their own tariff. This one shows the model - watts per square metre by insulation, system efficiency as a simple factor - so you can argue with it, and points at the fixes in true payback order.'], 'howto': ['Enter living area (heated rooms only - the unheated hallway is not your enemy).', "Be honest about insulation: drafty sash windows are 'poor' no matter what the estate agent said.", 'Set your energy price from the latest bill; heat-pump households keep the price but pick the pump.'], 'faqs': [('How much does it cost to heat 80 m²?', 'Average insulation on gas at 0.15 per kWh lands around 1,500-1,700 per 180-day season at 8 h/day. Poor insulation can nearly double it; a heat pump cuts the same house by roughly two thirds.'), ('How much does 1 degree lower save?', 'About 6% of the heating bill per degree - on a 1,500 season that is 90 per degree, sustained. A night setback to 17 °C costs nothing in comfort under a duvet and books real money over a season.'), ('Is a heat pump cheaper than a gas boiler?', 'Usually yes on running cost: a COP around 3 turns each purchased kWh into three of heat, so even against cheap gas the pump often wins, and always on emissions. Upfront cost is the trade-off - the calculator lets you compare both at your prices.'), ('What is the cheapest way to cut heating costs?', 'In order: draft-proofing and behavioural setbacks (near-free), loft insulation (pays back in years), heating system upgrade (big but slow), windows last. Money spent in that order buys the most degree-hours per unit.')]})

    pages.append({'slug': 'radiator-size-calculator', 'title': 'Radiator Size Calculator — Watts and BTU by Room Volume', 'h1': 'Radiator Size Calculator', 'desc': 'What size radiator does the room need? Area, ceiling height, insulation and window extras give watts, BTU/h and the physical length to look for. Free, no sign-up.', 'category': 'calculator', 'keyword': 'radiator size calculator watts btu room', 'tool': 'radiator', 'args': {}, 'intro': ['Enter the room area, ceiling height, insulation level and whether a big window or external wall leaks on it. The calculator returns the output to look for in watts and BTU/h, plus the physical radiator length at typical double-panel output.', 'Plumbing merchants size by wall length because that is what fits. Rooms are heated by volume through their envelope - this calculator does the volume physics and tells you why oversizing is safe and undersizing never is.'], 'howto': ['Measure floor area and ceiling height honestly - alcoves and bays count.', 'Flag the large window or external wall; 10-20% more output goes there.', "Match the watt figure on the radiator's output chart at your system temperature, not the brochure headline."], 'faqs': [('How many watts per square metre of heating?', "A room with average insulation needs roughly 100 W per m² at 2.5 m ceilings (40 W per cubic metre). Poor insulation pushes 125+, modern builds manage 75. The ceiling-height multiplier is where the 'per square metre' shortcut breaks."), ('Is it bad to oversize a radiator?', 'No - with a thermostatic valve an oversized radiator reaches the setpoint faster then modulates down, quietly and evenly. An undersized one runs flat out on the coldest day and still loses the race: the one mistake behaviour cannot fix.'), ('What does BTU mean for radiators?', 'BTU/h is the same number in imperial clothes: watts times 3.412. UK spec sheets quote BTU, European ones quote watts - this calculator shows both so you can shop either catalogue.'), ('Why is my room cold even with the radiator on?', "Nine times out of ten the radiator is undersized for the room's volume or the valve is set low; the tenth time it is air-locked - bleed it. If it heats fine but the room still feels cold, check draughts and insulation before buying more iron.")]})

    pages.append({'slug': 'insulation-payback-calculator', 'title': 'Insulation Payback Calculator — Years to Recover the Upgrade Cost', 'h1': 'Insulation Payback Calculator', 'desc': 'Which insulation upgrade pays back first? Draft-proofing, loft, walls or windows - annual saving, payback years, 10-year net and CO₂. Free, no sign-up.', 'category': 'calculator', 'keyword': 'insulation payback calculator years', 'tool': 'insulation', 'args': {}, 'intro': ['Enter your yearly heating cost and pick an upgrade. The calculator gives the annual saving, payback period, the 10-year net after costs, and the CO₂ cut - with the true order of operations spelled out.', 'Window-sales pages sell glazing as the insulation king. The honest payback ranking is draft-proofing, loft, walls, then windows - and this calculator prices all four so the sequence is visible instead of sold.'], 'howto': ['Use your actual annual heating spend (the heating cost calculator estimates it if you do not know).', 'Pick the upgrade you are considering; defaults are typical installed costs before any subsidy.', 'Compare payback years across options - then check national grants, which move every figure left.'], 'faqs': [('Which insulation upgrade pays back fastest?', 'Draft-proofing: a weekend and a few hundred units of materials against 8% of the bill - often a one-year payback. Loft insulation is the best professionally-installed job; walls are the biggest absolute saving.'), ('Why do windows rank last for savings?', 'Glass upgrade costs dominate: thousands to install against roughly 10% of heating bills, pushing payback past a decade. People still rightly replace windows - for comfort, noise and resale - but the savings are the alibi, not the reason.'), ('Do subsidies change the ranking?', 'They change the numbers, not the physics: grants on loft and wall schemes can halve payback, and some regions cover draft-proofing entirely. Always price the grant first - the ranking only shifts when a subsidy is that large.'), ('Can insulation cause damp?', 'It can, done badly: walls that stop drying inward without ventilation or breathable materials trap moisture. This is the corner where the cheapest quote becomes the expensive one - ask any installer explicitly how the wall will still dry.')]})

    pages.append({'slug': 'fire-number-calculator', 'title': 'FIRE Number Calculator — Your Financial Independence Target', 'h1': 'FIRE Number Calculator', 'desc': 'Your FIRE number: annual spending divided by an honest withdrawal rate (3.25-4.5%), with the gap, coast years and passive income shown. Free, no sign-up.', 'category': 'calculator', 'keyword': 'fire number calculator 25x rule', 'tool': 'firenum', 'args': {}, 'intro': ['Enter what you actually spend in a year, pick a withdrawal rate, and the calculator gives your FIRE number - the invested sum whose returns fund that spending forever - plus the remaining gap and how many years your current pot needs to coast there untouched.', 'Most FIRE calculators fix the 4% rule and flatter the result. This one exposes the rate choice - 4% is a 30-year US study, early retirees run 3.25-3.5% for 50-year horizons - and prices the trade honestly instead of selling a course.'], 'howto': ["Enter true annual spending from last year's records, not an aspirational budget.", 'Choose the rate for your retirement length: 4% for classic 30-year, 3.25-3.5% if retiring decades early.', 'Read the gap, the coast years (what happens if you never save again), and the passive income at target.'], 'faqs': [('What is the 25x rule?', 'FIRE number equals 25 times annual spending - the inverse of the 4% withdrawal rate from the Trinity study. It is a starting point: long retirements warrant 28-30x (3.5-3.25%), and the number scales with spending, not salary.'), ('Why do early retirees use 3.5% instead of 4%?', 'The 4% rule was tested over 30-year retirements at age 65. A 35-year-old needs the money to last 50+ years, through more market cycles and unknown future costs - the extra margin turns a coin-flip into a robust plan.'), ('Is the FIRE number a guarantee?', 'No - it is a floor built on historical averages. Sequence-of-returns risk means a crash in the first retired years bites hardest; flexible rules (spend 10% less after down years) buy more safety than a bigger number ever did.'), ('What counts as annual expenses?', 'Everything you actually spent last year including the irregular - repairs, insurance, holidays - averaged in. Using your aspirational budget produces a number that funds the person you wish you were, not the one who wakes up on Tuesday.')]})

    pages.append({'slug': 'savings-rate-to-fi-calculator', 'title': 'Savings Rate Calculator — Years of Work Left at Your Rate', 'h1': 'Savings Rate Calculator', 'desc': 'Your savings rate decides when work becomes optional: rate from income and spending, then years to FI on the famous 5%-return table. Free, no sign-up.', 'category': 'calculator', 'keyword': 'savings rate calculator years to retire', 'tool': 'savingsrate', 'args': {}, 'intro': ['Enter your take-home income and what you spend. The calculator gives your savings rate and - the part nobody forgets after seeing it - how many years of work that rate leaves, interpolated on the classic savings-rate-to-retirement table.', 'Retirement calculators demand portfolio guesses before they say anything. This one answers from two numbers you already know, and shows the shock that keeps the table famous: the curve from 51 years at 10% down to 8 at 70% is not linear.'], 'howto': ['Use take-home pay (after tax) - gross income is a number your payslip already ate.', 'Enter real spending from records; be honest, the rate is only as true as the spend line.', 'Read the years figure, then the +10-point row: each extra ten points of rate buys back years of life.'], 'faqs': [('What savings rate do I need to retire in 10 years?', "About 60% of take-home, at 5% real returns with a 4% withdrawal assumption. Every household's answer differs with spending: the rate matters because it is both the speed and the destination size at once."), ('Why is the savings-rate table so nonlinear?', 'Each saved coin does double duty - it grows the fund and shrinks the target it must fund. Saving 10% leaves 51 years of work; saving 70% leaves 8: the last decades fall away because spending fell too, not just because the pot grew.'), ('Does this work on gross or net income?', "Net. Tax is a spending-like leakage your future self never sees; the table's arithmetic lives entirely on take-home pay and real spending. Using gross flatters the rate and hides the truth it exists to tell."), ('Is 5% real return realistic?', "It is the table's long-run assumption for a diversified equity-heavy portfolio after inflation - historically reasonable, never guaranteed. Pessimists can read the table one band up: at 4% real, every duration stretches a few years, not a decade.")]})

    pages.append({'slug': 'coast-fire-calculator', 'title': 'Coast FIRE Calculator — Invested Today, Retired by Compounding', 'h1': 'Coast FIRE Calculator', 'desc': 'How much invested today means retirement at your target age with zero further saving? Coast FIRE number, surplus or deficit, and the return sensitivity. Free, no sign-up.', 'category': 'calculator', 'keyword': 'coast fire calculator by age', 'tool': 'coastfire', 'args': {}, 'intro': ['Enter your target at retirement, your ages, current investments and expected real return. The calculator gives the coast number: the sum that, invested today and left alone, reaches your target purely by compounding - after which new saving becomes optional.', 'Coast calculators usually bury the sensitivity. This one shows the same target at your rate and at 7%, because the gap between them is the real lesson: return assumptions dominate the early decades more than any salary raise.'], 'howto': ['Set the retirement target from your FIRE number, not a round million.', 'Enter current age and retirement age honestly - the multiple shown is what compounding promises at your rate.', 'Compare the figure with what you hold today; the surplus or deficit is the whole conversation.'], 'faqs': [('What is Coast FIRE?', 'The point where invested savings alone, left to compound, reach your retirement target by your target age. Past it, salary only needs to cover living costs - pension contributions become optional, and career decisions get much braver.'), ('How is the coast number calculated?', "Pure discounting: target divided by (1 + real return) to the power of years remaining. A million needed at 65 for a 30-year-old at 5% real is about 209k today - the multiple shown is compounding's whole promise."), ('Why does the return assumption matter so much?', 'Because it is exponentiated over decades: at 35 years to retirement, 5% versus 7% real nearly doubles the required starting sum. Costs, diversification and staying invested move this assumption more than any stock pick.'), ('Is Coast FIRE risky?', 'The risk is front-loaded: you stop saving on a promise about forty future years of returns. Mitigations - keep the target conservative, revisit annually, and treat coast as savings-optional rather than savings-impossible. A crash at 60 hits regardless; coast just changes what you do at 35.')]})

    pages.append({'slug': 'tent-size-calculator', 'title': 'Tent Size Calculator — What Rated Capacity to Actually Buy', 'h1': 'Tent Size Calculator', 'desc': 'What size tent for your group? Sleepers plus the +1 rule, with floor dimensions, packed weight and shoulder room - backpacking vs family. Free, no sign-up.', 'category': 'calculator', 'keyword': 'tent size calculator what size tent', 'tool': 'tent', 'args': {}, 'intro': ['Enter how many people sleep in the tent and whether you carry it. The calculator applies the +1 rule - buy one rated size above your headcount - and shows the floor dimensions, packed weight and shoulder room to expect.', 'Shop pages quote the rating on the label. This one explains why the label lies gently: ratings assume shoulders only, no bags, no dogs - and prices the honest size in kilos you will feel.'], 'howto': ["Count sleepers honestly (including the dog, who takes a person's worth of floor).", 'Pick backpacking or drive-in; weight maths differ by an order of magnitude.', 'Buy the rated size shown and check the floor dimensions against your longest sleeper plus 30 cm.'], 'faqs': [('What does tent capacity actually mean?', 'The number of shoulders that fit wall to wall - a 2-person tent is two 55 cm strips. Real camping wants bags, boots and the dignity of turning over, which is why the +1 rule is the first advice every experienced camper gives.'), ('How much should a backpacking tent weigh?', 'Modern 2-person 3-season designs run 2-3 kg, ultralight under 1.5 at double the price and fragility. Family tents ignore weight entirely - drive-in camping buys comfort, not grams.'), ('Is a 4-season tent worth it?', 'Only above the treeline or in snow: the extra poles and fabric handle wind and loading you rarely meet. A good 3-season tent plus a warm sleep system serves 95% of trips, in all three actual seasons.'), ('Where should I pitch a tent?', 'Higher than the water line, away from dead branches, out of gully wind-funnels, and never with the door into the prevailing weather. The best tent pitch decision costs nothing and saves more nights than any gear upgrade.')]})

    pages.append({'slug': 'backpack-weight-calculator', 'title': 'Backpack Weight Calculator — Total Load and the 20% Rule', 'h1': 'Backpack Weight Calculator', 'desc': 'Weigh your backpack before your shoulders do: base gear, food and water by trip days, total load and the 20% of body weight verdict. Free, no sign-up.', 'category': 'calculator', 'keyword': 'backpack weight calculator percentage body', 'tool': 'backpack', 'args': {}, 'intro': ['Enter your body weight, base gear weight, trip length and luxury allowance. The calculator adds consumables at honest rates, totals the pack, and gives the percentage-of-body-weight verdict that decides whether the trip is a joy or a negotiation.', 'Packing lists count items; this counts what your spine counts. The 20% rule, the consumables swing and the big-three leverage are all laid out instead of sold as an ultralight course.'], 'howto': ['Weigh your packed bag without food and water - that is base gear plus luxuries.', 'Enter trip days; food and water are added at 0.8 kg and 2 litres per standard plan.', 'Read the verdict: under 20% disappears, past 25% every kilometre hurts - trim the big three first.'], 'faqs': [('How heavy should a backpack be?', 'Under 20% of body weight for comfort: a 70 kg hiker carries 14 kg happily, 17.5 kg with fitness, and 21 kg by grit alone. Day hikes run lighter but water alone can take 2-3 kg in summer.'), ('What are the big three in backpacking?', 'Shelter, sleep system and pack - usually over half of base weight between them. Two kilos saved across the big three buys more comfort than a whole drawer of titanium accessories, and usually costs less than one.'), ('How much water should I carry hiking?', 'About half a litre per hour of hot-weather walking, but strategy beats capacity: knowing reliable refill points lets you carry 1 litre instead of 3 - two free kilos. Check sources before relying on them.'), ('Can I bring luxury items backpacking?', 'One, deliberately chosen - a paperback, real coffee, dry camp socks. The morale rule works because it is finite: one defended luxury beats seven accumulated comforts that quietly rebuild the 25% pack you were escaping.')]})

    pages.append({'slug': 'hiking-time-calculator', 'title': "Hiking Time Calculator — Naismith's Rule with Breaks", 'h1': 'Hiking Time Calculator', 'desc': "How long does that hike take? Distance, ascent and pace give walking time by Naismith's rule, plus break allowance and the turnaround point. Free, no sign-up.", 'category': 'calculator', 'keyword': 'hiking time calculator naismith rule', 'tool': 'hiketime', 'args': {}, 'intro': ["Enter the route distance, total ascent, your honest pace and break habits. The calculator applies Naismith's rule - the 1892 formula every routing app still builds on - and shows walking time, the climb penalty and your turnaround point.", "Route apps show kilometres and pretend hills are free. This calculator prices the ascent separately, because the climb is what turns 'just 6 km' into an afternoon - and it hands you the turnaround discipline that keeps afternoons from becoming nights."], 'howto': ['Read distance and cumulative ascent off the route profile (any maps app shows it).', 'Pick your real pace on flat ground - time a 5 km walk if you have never measured.', 'Add breaks honestly, and note the turnaround time before you set out, not at the junction.'], 'faqs': [("What is Naismith's rule?", 'One hour for every 5 km of distance plus one hour for every 600 m of ascent, formulated by Scottish mountaineer W. W. Naismith in 1892. Simple, surprisingly robust, and still the backbone of modern route-time algorithms.'), ('Does descent really take no extra time?', 'Naismith counts only ascent, but steep descents slow most walkers below flat pace - knees shorten strides on rocky ground. Rough or technical descents deserve an extra quarter of the flat-time estimate.'), ('How many kilometres can I hike in a day?', 'A fit walker covers 20-25 km of trail with modest ascent in a day; 15 km with 800 m of climbing feels the same. The ascent penalty in the calculator is why route profiles matter more than distance.'), ('What is the turnaround rule?', 'Turn back at half the total estimated time, whatever the summit looks like and however close it feels. Weather, injuries and dusk all arrive faster than regret - the summit is optional, the descent is mandatory.')]})

    pages.append({'slug': 'exam-study-planner', 'title': 'Exam Study Planner — Week-by-Week Plan from Your Exam Date', 'h1': 'Exam Study Planner', 'desc': 'Enter your exam date and subjects for the week-by-week plan: syllabus audit, past papers, error log drills - with hours per day and the last-new-topic date. Free.', 'category': 'calculator', 'keyword': 'exam study planner weeks before', 'tool': 'examplan', 'args': {}, 'intro': ['Pick your exam date and count your subjects. The planner works backwards: syllabus audit and past papers early, weak-topic passes in the middle, timed papers and the error log late - with the hours per day your remaining time implies.', 'Study guides hand out generic timetables that ignore your date. This planner lives on your countdown, highlights the current phase, and shows the arithmetic that tells you what is no longer possible - before you spend a week discovering it.'], 'howto': ['Enter the exam date and subject count; the plan regenerates from whatever today is.', 'Read the highlighted phase and run only that phase; early green-topic study is comfortable and useless.', 'Bookmark the page - the tab title keeps the days remaining, and the last-new-topic date is the hard deadline inside the deadline.'], 'faqs': [('How many weeks should I study for an exam?', 'Six weeks is the comfortable standard: syllabus audit, two passes on weak topics, two timed past papers and a taper. Two weeks still works - but the plan collapses to papers and error log, and green topics ride on luck.'), ('How many hours a day should I revise?', 'Whatever the remaining days demand - roughly 30 hours per subject spread across your time. Four hours of focused retrieval daily beats ten hours of rereading, and the figure that matters is what survives sleep, not what the timetable says.'), ('Should I study my strong subjects first?', 'Almost never. Red topics get your best hours; green topics get evenings or nothing - they already pay. The exception is confidence: one short green warm-up before hard work is morale, and morale is infrastructure.'), ('When should I stop learning new material?', '48 hours before the exam, hard stop. Late new topics arrive with two reviews at best - recall theatre instead of knowledge - and they displace consolidation sleep that would have made everything else stick.')]})

    pages.append({'slug': 'flashcard-revision-calculator', 'title': 'Flashcard Revision Calculator — New Cards per Day Until the Exam', 'h1': 'Flashcard Revision Calculator', 'desc': 'How many flashcards per day? Deck size and days to exam give the new-card rate, total reviews, peak minutes and the last day to add cards. Free, no sign-up.', 'category': 'calculator', 'keyword': 'flashcard how many new cards per day exam', 'tool': 'flashcard', 'args': {}, 'intro': ['Enter your deck size, days to the exam and seconds per review. The calculator prices spaced repetition honestly: new cards per day, the total review bill with expanding intervals, the peak-day minutes - and the date to stop adding cards.', 'Flashcard apps tell you whether you are due. This one tells you whether the plan is survivable - the 3.6x review multiplier, the mid-deck peak and the cut-off date are the parts apps let you discover at 1 a.m. in April.'], 'howto': ['Count the real deck - the cards that exist, not the ones you intend to write.', 'Enter honest days left and seconds per card (6 is typical; medicine runs longer).', 'Set the daily new-card pace shown and treat the stop date as a subject: no new cards inside ten days.'], 'faqs': [('How many new flashcards per day is reasonable?', 'Whatever divides your deck across your days: 300 cards in 21 days is 15 daily, with review load stacking to roughly 25-40 minutes at peak. Past 30 new cards a day, retention and goodwill both collapse.'), ('Why does the review total exceed the deck size?', 'Spaced repetition reschedules every card at growing intervals - first next-day, then three days, then a week - which costs about 3.6 reviews per card before an exam. That multiplier IS the forgetting curve being beaten.'), ('When should I stop adding new cards?', 'About ten days out. A card added later gets two reviews at best, which feels like studying and performs like rereading. The final days belong to drills on what already failed, plus sleep.'), ('Are flashcards actually better than rereading notes?', 'Yes - retrieval practice outperforms rereading in virtually every controlled comparison, because exams test retrieval and rereading trains recognition. The catch: cards must require real recall, and failed cards must be split, not stared at.')]})

    pages.append({'slug': 'halloween-candy-calculator', 'title': 'Halloween Candy Calculator — How Many Bags to Buy', 'h1': 'Halloween Candy Calculator', 'desc': 'How much Halloween candy for your street? Trick-or-treater count, pieces per kid and bag size give bags, cost and the half-show floor. Free, no sign-up.', 'category': 'calculator', 'keyword': 'how much halloween candy to buy calculator', 'tool': 'candy', 'args': {}, 'intro': ['Estimate your trick-or-treater count, set pieces per kid and your bag size. The calculator adds the rush-hour buffer, totals bags and cost, and shows the half-show floor for the rain scenario.', 'Party stores want you to over-buy; neighbors under-buy and run dark by 7:15. This one prices the 25% rush buffer explicitly - the difference between a legendary house and a porch light off early.'], 'howto': ["Use last year's count or ask the neighbours who have done a decade of Halloweens.", "Two pieces per visitor is the standard; check your bag's piece count - fun-size bags range 40-90.", 'Buy the figure and keep the receipt unopened bags can go back on November 1st sales.'], 'faqs': [('How many pieces of candy per trick-or-treater?', 'Two is the unspoken standard: generous without setting the new street record. One is remembered for years, and not the way hosts hope; full-size bars buy neighbourhood fame at roughly triple the cost per kid.'), ('What if I run out of candy?', 'Lights off means the evening is over - trick-or-treaters read the porch, not the doorbell. The half-show figure is the honest floor for bad weather; if you do run dark early, a sign and the leftover decoration budget beat an empty bowl.'), ('How do I handle allergies on Halloween?', 'A separate bowl of non-candy options - stickers, glow sticks, pencils - and the teal pumpkin that signals it. Allergy kids travel the longest distances for houses that stock them, and word travels through school gates fast.'), ('What do I do with leftover candy?', 'Chocolate freezes perfectly for months - December baking and the advent calendar are covered. Opened mixed bags do not keep well past a few weeks; unopened bags return on the sales cycle if kept for receipts.')]})

    pages.append({'slug': 'party-budget-calculator', 'title': 'Party Budget Calculator — Real Cost per Guest, Food to Extras', 'h1': 'Party Budget Calculator', 'desc': 'What will the party cost? Guests times per-head food and drink plus decorations, with the per-guest figure and the 1.5 invite rule built in. Free, no sign-up.', 'category': 'calculator', 'keyword': 'party budget calculator per guest', 'tool': 'partybudget', 'args': {}, 'intro': ['Enter your expected attendance, what you plan to spend per head on food and drink, and fixed extras. The calculator totals the party, shows the per-guest figure, and hands you the invite-list number that accounts for no-shows.', 'Party-planning sites sell themes. This one prices the arithmetic: the two-thirds food-and-drink share, the 1.5x RSVP rule, and where a potluck moves the money instead of removing it.'], 'howto': ['Enter expected guests - attendees, not invitees; the invite figure is an output.', 'Price food and drink per head honestly from your last shop or venue menu.', 'Add fixed extras - decorations, playlist speakers, a cleaning service - and read the total against your comfort.'], 'faqs': [('How much should a party cost per guest?', "Casual home parties run 15-30 per guest with food and drink; dinner parties 40+. The budget's shape matters more than its size: food and drink take about two-thirds, and everything else is staging."), ('How many people should I invite versus expect?', 'Invite half again as many as you can host for a casual party - about two-thirds accept, and a third of acceptances flake on the day. Seated dinners are the exception: there, every yes claims a chair, so invite exactly the table.'), ('Does a potluck actually save money?', 'It moves the money more than it removes it: guests cover sides and desserts, but the host still owns drinks, the main and coordination - which is the hidden cost. Best value: one made signature dish, one drink, bought everything else.'), ('How far in advance should I plan a party?', 'Three weeks for invitations to breathe and two days for shopping and make-ahead cooking. The prep-time rule: anything cooked doubles its estimate, and nothing new gets cooked the day of - the day belongs to the guests.')]})

    pages.append({'slug': '401k-match-calculator', 'title': '401k Match Calculator — Free Money From Your Employer', 'h1': '401k Match Calculator', 'desc': 'What is your employer match worth? Salary, contribution and match formula give the free annual amount, what you leave on the table, and its 20-year value. Free.', 'category': 'calculator', 'keyword': '401k employer match calculator free money', 'tool': 'match401k', 'args': {}, 'intro': ["Enter your salary, your contribution percentage and your plan's match formula. The calculator shows the free money you collect each year, what contributing less leaves on the table, and what that gap becomes over twenty years of compounding.", 'Payroll pages explain enrollment; this one prices the decision. The match is the only instant 50-100% return in finance with no market risk - and the gap row is what declining it actually costs, in the only units that matter: years.'], 'howto': ['Copy the match formula from your HR page - rate and cap both go in exactly as written.', 'Enter your current contribution percentage; the matched slice is whatever the cap allows.', 'Read the gap row first: if it is not zero, the raise you are declining is your own.'], 'faqs': [('How does an employer 401k match work?', 'The plan pays a percentage of what you contribute, up to a salary cap - the classic pattern matches 50 cents per dollar on your first 6%. Contribute under the cap and the difference is simply not paid; the match rewards presence, not effort.'), ('How much should I contribute to get the full match?', "Exactly the cap: at '50% of first 6%', contributing 6% earns the full 3% extra. Anything below is declining part of your compensation; anything above is fine but unmatched - good for tax reasons, invisible to the match."), ('Is the employer match really free money?', 'Yes, with one condition: vesting. Some plans hand the match over only after 2-3 years of service - leaving early forfeits it. Otherwise it is a 50-100% instant return no investment offers, before any market growth at all.'), ('What does leaving the match on the table really cost?', 'The gap compounds: 1,800 a year declined at 5% real returns is about 60,000 over a 20-year career - the six-figure version of a rounding error. Order of operations: full match first, then high-interest debt, then everything else.')]})

    pages.append({'slug': 'rent-split-calculator', 'title': 'Rent Split Calculator — Fair Share by Room Size', 'h1': 'Rent Split Calculator', 'desc': 'Split rent fairly by room size: private rooms pay their own square metres, shared space splits equally - with the en-suite and couple adjustments explained. Free.', 'category': 'calculator', 'keyword': 'rent split calculator by room size', 'tool': 'rentsplit', 'args': {}, 'intro': ['Enter the total rent and the square metres of each bedroom plus the shared space. The calculator prices every metre once: private rooms cost their own area, common space splits equally - and the bigger room pays more for reasons nobody has to argue about.', 'Split apps ask for your bank details; flatmates argue in feelings. This one shows the arithmetic in one line, then prices the real-world adjustments - en-suites, couples, bills - that the raw metres cannot see.'], 'howto': ['Measure each bedroom and the shared space roughly - a tape and five minutes beat estimates by feel.', 'Enter the total rent and the three areas.', 'Read both shares, agree them in writing the week you move in, and note the renewal date.'], 'faqs': [('How should rent be split between roommates?', 'By square metres with shared space equalised: common area cost splits per tenant, each private room bills its own metres. It is the only split that survives the bigger-room argument without a fight - the maths is the referee.'), ('Should the bigger room cost more?', 'Yes, by exactly its share of square metres - typically 10-20% more than the small room. Premium features worth more than metres (en-suite, double glazing, built-in wardrobes) add a further 5-10% by agreement, not by formula.'), ('How do couples split rent in a shared flat?', "The couple takes one room price plus half a share of the common area, since two people wear the kitchen and bathroom like two tenants but occupy one room. A single roommate should never subsidise a couple's cohabitation discount."), ('How should utility bills be split?', 'Equally - nobody heats half a flat and the meter cannot tell roommates apart. Streaming and personal shopping go by user; anything usage-heavy (a grow-room of computers, an aquarium) bills its owner. Review the split at every renewal, in writing.')]})

    pages.append({'slug': 'gift-budget-calculator', 'title': 'Gift Budget Calculator — Holiday Spending Without the January Bill', 'h1': 'Gift Budget Calculator', 'desc': 'Total your holiday gift spending by tier - partner, kids, family, friends, colleagues - then fund it across three months instead of one credit-card statement. Free.', 'category': 'calculator', 'keyword': 'holiday gift budget calculator total', 'tool': 'giftbudget', 'args': {}, 'intro': ['Enter what you plan to spend on each tier - partner, children, family, friends, colleagues. The calculator totals the season, flags the biggest line, prices the wrapping that everyone forgets, and turns the whole thing into a monthly saving figure.', 'Seasonal guides guilt you about generosity and never show the total. This one does the opposite: the 1%-of-take-home benchmark, the save-across-three-months plan, and permission to stop where the line says stop.'], 'howto': ["List real figures per tier from last year's receipts if you have them - memory rounds down.", 'Read the monthly figure and set up the transfer for October and November.', 'Trim the biggest line, not five small ones - one decision beats a dozen renegotiations.'], 'faqs': [('How much should I budget for Christmas gifts?', 'About 1% of annual take-home pay is the sustainable benchmark - 400 on a 40k net income. Most households spend triple that in December and rediscover it in January; the total row above is the number that changes the pattern.'), ('How do I stop overspending on Christmas presents?', 'Fund the budget in advance - the monthly figure shown - and shop from the list, not the shop. In-store December is engineered to convert warmth into spending; a written number per tier is the only reliable insulation.'), ('What is a reasonable gift budget per child?', "Whatever the household's tier says, consistently - children count gifts, not prices, and four wrapped presents outshine one expensive one. Consistency across siblings and years beats any absolute figure."), ('Are gift cards a lazy gift?', 'They are the correct gift for the person who wants nothing: cash with a constraint, no returns queue. Spend the effort on the card for the people who treasure surprise - the budget row exists precisely so effort goes where it lands.')]})

    pages.append({'slug': 'bbq-charcoal-calculator', 'title': 'BBQ Charcoal Calculator — Briquettes by Guests and Hours', 'h1': 'BBQ Charcoal Calculator', 'desc': 'How much charcoal for the barbecue? Guests times grill hours plus fire-up, in briquettes, chimney starters and kilos - with the two-zone layout. Free, no sign-up.', 'category': 'calculator', 'keyword': 'how much charcoal for bbq guests hours', 'tool': 'charcoal', 'args': {}, 'intro': ['Enter how many people you are feeding and how long the grill runs. The calculator gives briquettes, chimney starters and kilos - plus the two-zone layout that turns raw fire into actual cooking.', 'Bag recommendations assume a grill shaped like their brand. This one prices the real variables - guests and hours - and explains the two-zone fire, the chimney starter and the hand test that no bag label covers.'], 'howto': ['Count guests and estimate honest grill hours (burgers an hour, chicken three).', 'Buy the kilo figure plus one spare bag; leftover charcoal keeps dry for next time.', 'Light in a chimney, bank coals two-thirds/one-third, and cook in the zones, not the flames.'], 'faqs': [('How much charcoal do I need for 6 people?', 'About 170 briquettes - two chimney starters or roughly 1.6 kg - for a three-hour cook: 25 to establish the fire plus 8 per guest-hour. Wind and winter add a quarter; the spare bag is not optional.'), ('What is the two-zone fire?', 'Coals banked two-thirds on one side and one-third on the other: the hot side sears, the safe side finishes without burning. Every flare-up is solved by moving food, never by water - the zone system is what separates grilling from arson.'), ('Is a chimney starter worth it?', 'Yes - coals lit evenly in 15-20 minutes with no fluid taste, for the price of one bag of premium charcoal. Lighter fluid lingers in the first cook of the day and is the reason some burgers taste like a petrol station forecourt.'), ('How do I tell grill temperature without a thermometer?', 'The hand test: hold your palm at grate height - 2 seconds is searing heat, 4 is medium-high, 6 is gentle. It is imprecise and wonderful; a cheap grate thermometer makes it exact, but the hand keeps the instinct sharp.')]})

    pages.append({'slug': 'dog-food-portion-calculator', 'title': 'Dog Food Portion Calculator — Grams per Day by Weight and Stage', 'h1': 'Dog Food Portion Calculator', 'desc': "How much should your dog eat? Weight and life stage give kcal via the vet formula, then grams from the bag's energy - with the measuring-cup trap exposed. Free.", 'category': 'calculator', 'keyword': 'how much should I feed my dog calculator grams', 'tool': 'dogfood', 'args': {}, 'intro': ["Enter your dog's weight, life stage and the energy figure on the food bag. The calculator applies the veterinary RER formula (70 × kg^0.75) with the right stage multiplier, then converts to grams per day and per meal.", 'Feeding guides on bags are biased high - food companies sell food. This one uses the maths vets actually use, exposes the measuring-cup error that quietly overfeeds most dogs, and hands the decision back to the body condition score.'], 'howto': ["Weigh your dog (you - dog - you) rather than guessing; enter the bag's kcal/kg from the analysis panel.", "Pick the honest life stage - 'active' is for working dogs, not enthusiastic ones.", 'Weigh the daily ration on a kitchen scale, feed in two meals, and adjust 10% monthly against the ribs test.'], 'faqs': [('How much should a 20 kg dog eat per day?', 'At 3,600 kcal/kg food, a neutered adult 20 kg dog needs roughly 1,290 kcal - about 360 g a day split in two meals. The bag often says more; the ribs test and monthly weighing say what is true.'), ('Why do bag feeding guides overfeed?', "They are printed to sell food: generous tables assume intact, highly active animals and end at the top of every weight range. Neutered pet dogs typically need 20-30% less than the bag's happy default."), ('Is a measuring cup accurate for dog food?', 'Not really - cup measures of kibble run up to 20% off either way, which is the difference between slim and overweight over a year. A 5-gram kitchen scale is the cheapest pet-health purchase there is.'), ('How do I know if my dog is the right weight?', "Body condition, not the scale alone: ribs findable under a thin layer, waist visible from above, belly tuck from the side. Score monthly and adjust the ration by 10% - the dog's silhouette is the portion calculator that never lies.")]})

    pages.append({'slug': 'cat-food-portion-calculator', 'title': 'Cat Food Portion Calculator — Grams per Day by Weight and Stage', 'h1': 'Cat Food Portion Calculator', 'desc': 'How much should your cat eat? Weight and stage give kcal by the feline RER formula, then grams from the bag - plus the 4-meal rhythm and scale discipline. Free.', 'category': 'calculator', 'keyword': 'how much should I feed my cat calculator grams', 'tool': 'catfood', 'args': {}, 'intro': ["Enter your cat's weight, life stage and the food's energy. The calculator applies the same veterinary formula vets use - 70 × kg^0.75 with a stage factor - and returns grams per day and per small meal.", 'Cat portions live or die by precision: ten grams of overpour is a tenth of the day. This calculator shows that arithmetic, explains the indoor-cat multiplier owners underestimate, and rules by silhouette rather than by bag.'], 'howto': ['Use the last vet-visit weight; enter kcal/kg from the food panel.', 'Pick the honest stage - neutered indoor is the most common and the lowest multiplier.', 'Weigh the daily total once, split into 3-4 small meals, adjust 10% monthly by the ribs-and-waist test.'], 'faqs': [('How much should a 4.5 kg cat eat per day?', 'A neutered indoor 4.5 kg cat needs about 250 kcal - roughly 65 g of 3,800 kcal/kg food. The bag table usually says more; the indoor multiplier and the scale decide the truth.'), ('Why do indoor cats gain weight so easily?', 'The lowest energy multiplier meets the highest feeding optimism: neutered indoor cats burn less and eat by boredom. Measured portions, wet food for volume, and food-puzzle toys close the gap without a diet drama.'), ('How many meals should a cat eat per day?', 'Three or four small meals matches the natural hunt-eat-sleep cycle; two big meals work if that is reality. The 5 a.m. serenade is usually a scheduling bug - shift the last meal later before blaming the cat.'), ('How do I check if my cat is overweight?', 'Ribs findable under slight fat, waist visible from above, no swinging belly flap when walking. Cats should weigh what their frame says, not a breed chart - adjust the ration 10% monthly and let the silhouette vote.')]})

    pages.append({'slug': 'pet-treat-calculator', 'title': 'Pet Treat Calculator — The 10% Rule in Pieces per Day', 'h1': 'Pet Treat Calculator', 'desc': 'How many treats can your pet have? The veterinary 10% rule turns daily food calories into a treat budget, in pieces, with the human-food dangers listed. Free.', 'category': 'calculator', 'keyword': 'how many treats a day dog 10 percent rule', 'tool': 'treats', 'args': {}, 'intro': ["Enter your pet's daily food calories and the energy per treat. The calculator applies the veterinary 10% rule - treats stay under a tenth of daily intake - and answers in pieces per day, with the safety list every household should know.", 'Treat bags never mention the budget they spend from. This one prices the 10% rule in actual pieces, counts the training session and the grandparent from the same ledger, and keeps the poison list one glance away.'], 'howto': ["Take daily kcal from the dog or cat portion calculator, or the bag's worked example.", 'Read kcal per treat from the packet - dental chews hide 30-80 kcal and count double.', 'Count pieces per day, shrink meals on heavy training days, and pin the danger-food list to the fridge.'], 'faqs': [('What is the 10% treat rule?', 'Treats, chews and table scraps together stay under 10% of daily calories. Pet food is nutritionally balanced and snacks are not - past a tenth, you are diluting a designed diet with randomness, and most pet weight gain lives exactly here.'), ('How many calories are in common treats?', "Training treats run 3-10 kcal, biscuits 20-40, dental chews 30-80 - a large chew can be a third of a small dog's daily allowance. The packet's kcal per piece is the number this calculator spends."), ('Which human foods are dangerous for pets?', "Dogs: chocolate, grapes and raisins, xylitol sweetener, onions, macadamias. Cats: onions and garlic in any form, and lilies anywhere in the house. 'Just a little' of the wrong list is an emergency vet visit, not a treat."), ('Should treats come out of meal portions?', "On heavy training days, yes - take the extra calories out of meals rather than off the ledger. Same dog, same daily total, better behaviour at dinner: the budget is the day's, not each bowl's.")]})

    pages.append({'slug': 'dripping-tap-calculator', 'title': 'Dripping Tap Calculator — Litres and Money Down the Drain', 'h1': 'Dripping Tap Calculator', 'desc': 'What does a dripping tap waste? Drips per minute times the clock gives litres per year and cost, hot-tap doubling and the meter leak test. Free, no sign-up.', 'category': 'calculator', 'keyword': 'dripping tap waste water per year calculator', 'tool': 'driptap', 'args': {}, 'intro': ['Count the drips per minute, enter your water price and how long the tap drips each day. The calculator turns a quarter-millilitre nuisance into litres and money per year - and shows the one-drip-per-second scare figure for scale.', 'Plumbing sites quote a washer and van call-out. This one prices the drip first: the bathtub-a-month arithmetic, the hot-tap doubling most calculators skip, and the overnight meter test that finds the leaks you have not met yet.'], 'howto': ['Count drips for 15 seconds, multiply by four - or trust your ears: audible-at-night is around 100 a minute.', 'Enter your water price per cubic metre from the bill; halve the hours if it is a tap you mostly close.', 'Compare the yearly figure with a ten-minute washer fix, then run the overnight meter test for hidden leaks.'], 'faqs': [('How much water does a dripping tap waste?', 'One drip per second is roughly 7,900 litres a year - a bathtub every fortnight. Sixty drips a minute, the audible-at-night class, doubles that; each drip carries about a quarter millilitre and the year multiplies it mercilessly.'), ('Does a hot tap dripping cost more?', 'Yes - you pay for the water and the heating: gas or electric re-warming replaces what escapes, roughly doubling the bill versus a cold drip. Hot taps also scale up faster, so they fail sooner and drip harder.'), ('Can I fix a dripping tap myself?', 'Usually: isolate the supply, and either swap the rubber washer (traditional taps) or the ceramic cartridge (modern mixers) - a five to ten minute job with parts under ten units. Hard water taps may need a descale while open.'), ('How do I check for hidden water leaks?', 'The overnight meter test: read the meter last thing at night with every appliance and tap off, read again before morning use. Any movement means water escapes somewhere - fittings, cisterns, or the supply pipe itself.')]})

    pages.append({'slug': 'shower-vs-bath-calculator', 'title': 'Shower vs Bath Calculator — Real Cost per Wash', 'h1': 'Shower vs Bath Calculator', 'desc': 'Shower or bath - which costs less? Minutes, flow and energy price give the weekly cost of each, the litres saved, and the exact crossover time. Free, no sign-up.', 'category': 'calculator', 'keyword': 'shower vs bath cost water calculator', 'tool': 'showerbath', 'args': {}, 'intro': ["Enter your shower minutes, the head's litres per minute, washes per week and your energy price. The calculator totals water and heating cost for showers versus a standard 80-litre bath - and finds the exact minute your shower becomes a bath.", 'Water-company pages count litres and stop; the bigger half of the bill is heating them. This calculator prices both halves, exposes the ten-minute crossover, and lets the bath keep its honest place as a priced luxury.'], 'howto': ['Time a real shower once - estimates run short by minutes.', 'Check flow: hold a jug under the head for ten seconds and multiply, or use the 8 L/min default for a modern head.', 'Enter washes per week and your energy price; read both weekly bills and the crossover minutes.'], 'faqs': [('Is a shower always cheaper than a bath?', "Only under ten minutes at 8 litres a minute: past 80 litres, a long power shower is a bath with standing. The average seven-minute shower uses about half a bath's water - the crossover, not the label, decides the bill."), ('What does a bath cost in water and energy?', '80 litres heated 35 degrees over mains temperature is about 3.3 kWh plus the water itself - at typical prices, roughly the cost of a nine-minute shower. The energy share is four times the water share, which is the part most comparisons skip.'), ('Do low-flow showerheads really help?', "Yes - 8 down to 6 litres a minute saves a quarter of water and heating with little felt difference on a modern head. Weeks to payback, and it shortens every shower's litres without a timer or an argument."), ('How much does a 10-minute shower cost?', 'At 8 L/min and typical energy prices, about 80 litres and 3.3 kWh heated - the same water as a bath. Five minutes at 6 L/min cuts both by half; the cheapest shower is short, cool-ish and low-flow.')]})

    pages.append({'slug': 'standby-power-calculator', 'title': 'Standby Power Calculator — What Idle Electronics Cost You', 'h1': 'Standby Power Calculator', 'desc': 'The always-on leak: standby watts times hours times price gives the yearly cost of idle electronics - with the warm-when-off hunt and the switchable-lead fix. Free.', 'category': 'calculator', 'keyword': 'standby power cost calculator vampire energy', 'tool': 'standby', 'args': {}, 'intro': ['Enter your always-on standby load in watts, hours per day and your electricity price. The calculator prices the year of idle drain - the set-top boxes, consoles, routers and chargers that never truly sleep.', 'Energy sites warn about vampire power and stop. This one turns it into an annual figure you can feel, lists the usual suspects, and gives the two-minute meter hunt that finds which devices confess by being warm.'], 'howto': ['Guess or measure: a plug-in power meter gives the real household figure in minutes (30-60 W is typical).', 'Enter hours actually left powered - 24 for the always-on cluster, fewer if leads get switched.', 'Read the yearly figure, then the per-day one: that is what the red light on the set-top box really costs.'], 'faqs': [('How much does standby power cost per year?', 'A 45-watt always-on load at typical prices runs near 120 a year - comparable to the entire lighting bill of an LED home. Half the household typically idles at 30-60 watts across boxes, consoles, routers and chargers.'), ('Which devices waste the most standby power?', 'The warm-when-off club: set-top boxes and game consoles in instant-on mode lead, followed by old amplifiers, desktop towers left on, and anything with a brick that hums. The router stays - it earns its idle.'), ('How do I find vampire devices?', 'A plug-in power meter answers per device; the free version is the palm test - anything warm when off is drawing current. The whole-house version is the same overnight meter test used for water leaks, done at the electricity meter.'), ('Do smart plugs stop standby waste?', 'Switchable extension leads and smart plugs work well for switchable clusters - the entertainment centre dies in one gesture. Leave the router, fridge-freezer and anything with recordings or updates on its own schedule.')]})

    pages.append({'slug': 'food-waste-calculator', 'title': 'Food Waste Calculator — What Your Bin Costs Per Year', 'h1': 'Food Waste Calculator', 'desc': 'What does your household bin? Weekly food waste in kg times price gives the yearly total, per-person share and the shopping-list slice. Free, no sign-up.', 'category': 'calculator', 'keyword': 'food waste calculator household cost per year', 'tool': 'foodwaste', 'args': {}, 'intro': ['Weigh or honestly estimate the food your household bins in a week - leftovers, wilted produce, forgotten containers. The calculator scales it to a year of kilos and money, per household and per person.', 'Campaigns recite national averages nobody believes apply to them. This calculator makes your own bin the witness, then prices the three free habits - list, fridge map, cook-the-tired-things-first - that typically remove nearly half of it.'], 'howto': ['Collect one honest week of food waste in a bag and weigh it - include plate scrapings and drinks poured away.', 'Enter your average price per kilo from a real shopping receipt.', 'Read the yearly figure, then run the three-fixes month and weigh again - the drop is the savings column.'], 'faqs': [('How much food does the average household waste?', 'Roughly a fifth to a third of purchased food - several hundred euros a year for a family, mostly fresh produce, bread and leftovers. Almost everyone estimates themselves below average, which is why the week-long weighing exercise lands so hard.'), ('What foods get wasted the most?', 'Salad and leafy vegetables lead, then bread, fruit, milk and cooked leftovers - the fresh-perishable half of the trolley. The freezer is the reset button for everything except lettuce; the salad drawer is a queue, not a museum.'), ('Does meal planning really reduce food waste?', 'Yes - a written list against a planned week typically removes around 40% of waste, because it kills the impulse produce and the duplicate jars. Planning is the cheapest grocery saving available and it compounds weekly.'), ('Are best-before dates the same as expiry dates?', 'No - best-before is about quality and most foods are fine well past it; use-by is about safety and applies to perishables only. The sniff-and-look test governs best-before; use-by on meat and fish is the one date worth treating as law.')]})

    pages.append({'slug': 'christmas-tree-calculator', 'title': 'Real vs Artificial Christmas Tree Calculator — Break-even Christmases', 'h1': 'Real vs Artificial Christmas Tree Calculator', 'desc': 'Real tree every year or artificial once? Price both, find the break-even Christmas count and the carbon verdict - the 10-use rule explained. Free, no sign-up.', 'category': 'calculator', 'keyword': 'real vs artificial christmas tree cost break even', 'tool': 'xmastree', 'args': {}, 'intro': ['Enter your local real-tree price and the artificial tree you are eyeing. The calculator gives the break-even Christmas count, the per-use cost of the plastic one, and the carbon verdict that settles the argument properly.', 'Tree debates run on vibes. This one runs on division - and on the physical rule underneath: the artificial tree wins money and carbon only after its tenth Christmas, which is why the cheap plastic one loses both arguments at once.'], 'howto': ['Price a real tree in your area and the artificial model you would actually keep for years.', 'Enter how long you have owned any artificial tree already - its remaining Christmases are what count.', 'Read the break-even figure honestly: if your tree habit changes sooner, the real one was always right.'], 'faqs': [('Is an artificial tree cheaper than real?', 'After the break-even year, yes: a 90 unit tree against 45 unit real trees pays for itself in two years. Before that, or if it breaks early, the real tree was cheaper all along - longevity is the entire artificial business case.'), ('Which tree is better for the environment?', "An artificial tree carries roughly 40 kg of manufacturing and shipping CO2 and needs ten or more Christmases to beat a real tree's ~3 kg. Local real trees are an annually replanted crop, not deforestation; a kept-alive potted tree beats both."), ('How long do artificial trees last?', 'Decent ones run 10-15 years before the PVC yellows and the hinge boxes fail; cheap ones die by year three - the price gap is really a lifespan bet. Storage matters: dry attic, original box, crushed branches are the killer.'), ('Is a real Christmas tree sustainable?', 'Trees are farmed as a crop - grown 7-10 years per harvest and replanted, absorbing carbon while growing. The footprint lives in transport and disposal; shredding or replanting-with-roots keeps it low, landfill is the bad ending.')]})

    pages.append({'slug': 'carry-on-size-calculator', 'title': 'Carry-On Size Calculator — Does Your Bag Fit Cabin Rules?', 'h1': 'Carry-On Size Calculator', 'desc': 'Will your bag board? Length, width, depth against the four common airline frames give a fits verdict, the spare centimetres and the gate-check risk. Free.', 'category': 'calculator', 'keyword': 'carry on size check calculator cabin bag', 'tool': 'carryon', 'args': {}, 'intro': ["Measure your bag's length, width and depth - wheels and handles included - and pick the airline frame you fly. The calculator returns the fits-or-too-big verdict, your tightest margin, and how likely a gate agent is to disagree.", "Airline tables hide the comparison and their own variation. This one checks the shape against the four common frames at once, explains the sizer's zero-tolerance for one soft centimetre, and prices the soft-versus-hardshell difference."], 'howto': ['Measure the bag fully assembled - wheels, handles and feet are part of every rule.', 'Pick the frame matching your airline, or check the tightest one if you fly mixed carriers.', 'Read the margin: 1 cm passes soft and fails hardshell; 3 cm over is a fee with your name on it.'], 'faqs': [('What are the standard carry-on dimensions?', 'The common frames are 55×40×23 (US majors), 55×35×25 (EU typical), 56×36×23 (IATA guide) and 56×45×25 (larger allowances). Check your specific airline - budget carriers enforce hard, and aircraft type can shrink even that.'), ('Do wheels count in carry-on size?', 'Yes - every dimension includes wheels, handles and feet, which is how advertised cabin bags fail real sizers. Measure the bag standing ready to fly, not the label sewn inside the lining.'), ('What happens if my bag is slightly too big?', 'At the gate: a gate check, usually free on legacy carriers and a fee on budget ones - or the embarrassing frame test. A bag within 1 cm passes if soft and compressible; hardshell needs its full margin in writing.'), ('How strict are airlines about carry-on weight?', 'Varies wildly: EU carriers weigh with 7-10 kg limits and charge for overage; US majors check size, not weight. The trick is wearing the heavy things aboard and letting the bag carry the light ones.')]})

    pages.append({'slug': 'stopping-distance-calculator', 'title': 'Stopping Distance Calculator — Reaction + Braking by Road', 'h1': 'Stopping Distance Calculator', 'desc': 'How far does your car take to stop? Speed times reaction time plus braking physics by road surface - dry, wet, snow, ice - in metres and car lengths. Free.', 'category': 'calculator', 'keyword': 'stopping distance calculator speed braking', 'tool': 'stopdist', 'args': {}, 'intro': ['Enter your speed, the road condition and an honest reaction time. The calculator splits stopping into reaction distance - travelled before your foot moves - and braking distance from the friction physics, in metres and car lengths.', 'Driving-school charts quote one dry number and one wet number. This one shows the arithmetic live: braking grows with the square of speed, ice multiplies it eightfold, and the reaction half is the part your phone stretches.'], 'howto': ['Enter the speed you actually travel, not the limit.', 'Pick the honest road condition - wet means properly wet, not freshly damp.', 'Set reaction time: 1.5 s is the standard alert driver; tired or distracted adds a full second you cannot brake away.'], 'faqs': [('What is the stopping distance at 100 km/h?', 'On dry asphalt with a 1.5 s reaction: about 40 m of reaction plus 50 m of braking - roughly 90 metres, twenty car lengths. The same speed on ice stops in around 340 metres, three football pitches.'), ('Why does braking distance grow with the square of speed?', 'Kinetic energy rises with velocity squared, and every metre of braking must burn it: double from 50 to 100 km/h and the braking part quadruples. The speedometer lies by understatement - the physics is exponential-feeling.'), ('How much does ice increase stopping distance?', 'Roughly eight times versus dry road, because grip falls from a friction factor near 0.8 to about 0.1. Snow sits between at 0.2 - five times dry. Wet compacts the margin before the cold seasons even arrive.'), ('Does ABS make stopping distances shorter?', "Only marginally on dry roads - ABS's gift is steerability while braking, not shorter stops. Shorter stops come from good tyres at correct pressure, honest speeds and an unoccupied reaction window.")]})

    pages.append({'slug': 'following-distance-calculator', 'title': 'Following Distance Calculator — the Two-Second Rule in Metres', 'h1': 'Following Distance Calculator', 'desc': 'How far behind should you follow? Speed and headway seconds give the gap in metres and car lengths, plus the marker method and reaction-gap cost. Free, no sign-up.', 'category': 'calculator', 'keyword': 'following distance calculator two second rule metres', 'tool': 'followdist', 'args': {}, 'intro': ['Enter your speed and your headway in seconds. The calculator converts the two-second rule into metres and car lengths, shows what your reaction window alone consumes, and teaches the marker method that makes it stick.', 'Tailgating feels like progress and prices like a crash. This calculator shows the gap the physics wants - which grows with speed while the bumper-to-bumper illusion grows with courage - and why jams dissolve in the space you leave.'], 'howto': ['Enter your real speed and pick headway: 3 s dry and awake, 4 s in rain or dark, 5 s for snow or towing.', 'Practise the marker method: fixed point, count the seconds as the car ahead passes it.', 'Compare the reaction-gap row with your following distance - the gap must swallow your reaction, not your hopes.'], 'faqs': [('What is the two-second rule?', 'Keep at least two seconds of time between you and the car ahead: pass a fixed roadside marker no sooner than two seconds after they do. Three seconds is the realistic minimum for alert driving; rain, night and towing each add a second.'), ('Why do tailgaters not actually arrive sooner?', 'Traffic moves in waves, and close following amplifies every brake tap into a stop-go oscillation - the space you leave absorbs the wave and smooths your own journey. The queue paradox: gaps move traffic faster, not slower.'), ('How does following distance relate to stopping distance?', "The gap must cover your reaction distance at that speed - about 40 metres at 100 km/h - before your braking even begins, and ideally the car ahead's braking too. Time-based gaps scale with speed automatically; fixed metres do not."), ('What headway should I leave at night or in rain?', 'Add a second per degradation: night costs one for vision, rain one for grip, snow or towing two. Five seconds feels enormous and is merely survivable - the drivers behind can wait for their own safety margin.')]})

    pages.append({'slug': 'winter-tire-calculator', 'title': 'Winter Tire Calculator — the 7°C Rule and Three-Year Cost', 'h1': 'Winter Tire Calculator', 'desc': 'Do you need winter tires? Morning temperature against the 7°C rule gives the grip verdict, plus the two-sets-versus-all-season three-year cost. Free, no sign-up.', 'category': 'calculator', 'keyword': 'winter tires 7 degree rule when to change', 'tool': 'wintertire', 'args': {}, 'intro': ['Enter your typical morning temperature and what is on the car. The calculator gives the grip verdict against the seven-degree rule and totals the three-year cost of two tyre sets plus swaps versus one all-season set.', 'Tire shops sell fear in all four sizes. This one prices the decision: the compound chemistry that makes summer rubber a hockey puck below 7°C, the honest middle ground all-seasons occupy, and the swap calendar that rhymes with the clocks.'], 'howto': ["Use your coldest regular morning temperature, not the day's high.", 'Pick your current setup and the local swap cost - or zero if you change them yourself.', 'Read the verdict and the three-year figure, then book the swap window: under 7°C mornings, or after Easter in spring.'], 'faqs': [('What is the 7°C rule for winter tires?', 'Below about 7°C, summer rubber hardens and grips through its tread pattern alone, while winter compounds stay soft and bite cold tarmac - the crossover is chemistry, not snow. Winter tires also outbrake summers on cold dry roads, which surprises everyone.'), ('Are all-season tires a good compromise?', 'For mild winters and light snow, genuinely yes - one set, no swaps, roughly 70% of each specialist. Where winters are proper - sustained ice, snowfall, mountain grades - they are the compromised choice at the exact moment margin matters.'), ('When should I change to winter tires?', "When regular mornings sit under 7°C - in most temperate climates that is October's second half; spring change waits until after Easter. Regions with mandatory winter-tire laws enforce windows by signage and season, not by feel."), ('How much does running two sets of tires really cost?', "The second set plus two swaps a year against one all-season set's faster wear - typically a few hundred over three years, the price of the shortest stopping distance you will ever buy. Store the off-season set cool, dark and off concrete.")]})

    pages.append({'slug': 'plant-watering-calculator', 'title': 'Plant Watering Calculator — Days Between Waterings', 'h1': 'Plant Watering Calculator', 'desc': 'How often should you water your houseplant? Pot size, plant type, season and light give the interval in days, litres per watering and the finger-test law. Free, no sign-up.', 'category': 'calculator', 'keyword': 'how often to water houseplant calculator', 'tool': 'plantwater', 'args': {}, 'intro': ['Enter the pot diameter, plant type, season and light. The calculator gives the interval between waterings, the litres to pour until it drains through, and the signs that overrule any schedule.', 'Plant apps send notifications on a calendar. This one computes the interval from the physics - pot volume, drink rate, resting season - and then hands authority to the only sensor that never lies: your fingertip.'], 'howto': ["Measure the pot's rim diameter and pick the type honestly - succulents drink a third of a tropical's rate.", 'Winter halves the interval; low light stretches it again.', 'Check at the interval: dry two centimetres down means water until it drains, then empty the saucer.'], 'faqs': [('How often should I water a houseplant?', 'Tropicals in a 15 cm pot run about a week in the growing season, two weeks resting in winter; succulents stretch three times that. The interval is a plan - the top two centimetres of soil, tested by finger, is the decision.'), ('How much water does a plant need per watering?', "Enough to drain from the bottom - roughly a fifth of the pot's volume - then empty the saucer within minutes. The drain-through flushes accumulated salts and wets the whole root ball; the emptied saucer is what saves the roots."), ('What are the signs of overwatering?', 'Yellowing leaves while the soil is still wet, soft brown stems at the base, fungus gnats, and a sour smell. Overwatering kills more houseplants than drought - roots suffocate in the water the schedule insisted on.'), ('Do plants need less water in winter?', 'Yes - growth halts in low light and the drinking halves with it, which is why winter is the overwatering season. Water less, stop feeding, and let the soil dry further between drinks until spring resumes.')]})

    pages.append({'slug': 'repot-size-calculator', 'title': 'Repot Size Calculator — Next Pot Diameter and Soil Needed', 'h1': 'Repot Size Calculator', 'desc': 'What size pot next? Current diameter gives the +2-3 cm upgrade, the litres of potting soil to buy, and the root-bound signals worth checking. Free, no sign-up.', 'category': 'calculator', 'keyword': 'what size pot when repotting calculator', 'tool': 'repot', 'args': {}, 'intro': ["Enter the current pot's diameter and height. The calculator applies the two-to-three-centimetre rule, works out the litres of fresh potting soil, and lists the root-bound signals that say repot rather than refresh.", 'Garden centres upsell pots by enthusiasm. This one prices the root physics: too big a pot holds water the roots cannot drink, which is how overwatering happens to careful people - and the upgrade rule keeps the soil-to-root ratio honest.'], 'howto': ["Measure the current pot's rim diameter and height.", 'Buy the next size shown and roughly the soil litres - one extra bag if the roots are dense.', 'Repot in spring as growth resumes; water lightly for a fortnight while the roots settle.'], 'faqs': [('How much bigger should the new pot be?', 'Two to three centimetres in diameter - enough fresh soil for a season of root growth without a swamp of unused, ever-damp compost. Jumping several sizes is the classic overwatering trap wearing a generous disguise.'), ('How do I know a plant is root-bound?', 'Roots circling the soil surface, escaping the drainage hole, or water racing straight through the pot - the root mass now owns the volume. Slowed growth and quick thirst are the quieter versions of the same message.'), ('How much potting soil do I need?', "The new pot's cylinder minus the root ball - the calculator gives litres, and one spare bag covers the underestimate. Refresh the top five centimetres yearly even without a full repot; it resets nutrition without moving roots."), ('When is the best time to repot?', 'Spring, just as growth resumes - roots colonise fresh soil at their fastest then. Repotting in winter leaves wounded roots sitting in wet, unexplored soil; water lightly for a fortnight after any move.')]})

    pages.append({'slug': 'fertilizer-dilution-calculator', 'title': 'Fertilizer Dilution Calculator — ml per Watering Can', 'h1': 'Fertilizer Dilution Calculator', 'desc': 'How much plant feed per can? Label dose times can size times season gives the ml - with the salt-burn signs and the half-strength default. Free, no sign-up.', 'category': 'calculator', 'keyword': 'plant fertilizer dilution calculator ml per litre', 'tool': 'fertdilute', 'args': {}, 'intro': ["Enter the label's dose, your watering can size and the season. The calculator gives the millilitres of feed per can, the per-plant figure, and the calendar that decides when feeding stops entirely.", 'Labels print greenhouse doses for greenhouses. This one halves them for windowsill winters, explains why overfeeding looks like underwatering at first glance, and gives the flush that fixes the salt crust when enthusiasm won.'], 'howto': ['Read the ml-per-litre dose from the bottle - not the scoop table for outdoor beds.', 'Set the season: half strength from autumn to spring, full only in active growth.', 'Water first if the soil is dry - feed goes into damp soil, never into parched roots.'], 'faqs': [('How much fertilizer should I use for houseplants?', 'The label dose, halved for indoor winter conditions, every two to four waterings in the growing season. Greenhouse labels assume professional light and airflow; a windowsill metabolises a fraction of that.'), ('What happens if I over-fertilize plants?', 'Salt burn: brown leaf tips and margins that mimic underwatering, white mineral crust on the soil, sometimes a fertiliser smell. The fix is a thorough flush with plain water and a month off feeding - then a weaker dose.'), ('Should I fertilize plants in winter?', 'Almost never - resting plants cannot spend nutrients, so the feed becomes the salt crust that burns roots in spring. Resume weakly when new growth starts, and let the calendar, not the bottle, set the rhythm.'), ('Can I add fertilizer to dry soil?', 'No - fertiliser onto parched roots concentrates and burns. Water first, feed second, or feed with the regular watering at half dose: damp soil spreads the salts the way roots can actually take them.')]})

    pages.append({'slug': 'turkey-thaw-calculator', 'title': 'Turkey Thaw Calculator — Start Date, Oven Time and Rest', 'h1': 'Turkey Thaw Calculator', 'desc': 'When to start thawing the turkey? Serving date and weight give the fridge-thaw start date, oven time at 175°C and the rest before carving. Free, no sign-up.', 'category': 'calculator', 'keyword': 'how long to thaw a turkey calculator start date', 'tool': 'turkeythaw', 'args': {}, 'intro': ["Enter the serving date and the bird's weight. The calculator works backwards: fridge-thaw start date at four and a half hours per kilo, oven time at 175°C, and the rest window before carving.", 'Bag instructions and forums disagree by days. This one runs the vetted arithmetic on your actual date - and explains the cold-water rescue, the probe truth over pop-up timers, and why the rest is not optional.'], 'howto': ["Enter the date you serve and the frozen bird's weight from the label.", 'Read the start-thaw date and put it in the calendar - bottom shelf, on a tray.', 'On the day: oven at 175°C, probe to 74°C in the thigh, then rest before the knife.'], 'faqs': [('How long does a turkey take to thaw in the fridge?', "About four and a half hours per kilo - a 6 kg bird needs roughly a day and a half, so start it two days before serving with a day's margin. The fridge thaw is the only one that is safe and hands-off."), ('Can I thaw a turkey in cold water?', 'Yes, in a leak-proof bag, fully submerged, water changed every half hour - about half an hour per kilo. It works on a forgotten bird but owns the whole day; the fridge method never needs rescuing.'), ('How long should I roast the turkey?', 'About 45 minutes per kilo uncovered at 175°C, but the only verdict is 74°C in the inner thigh on your own probe - pop-up timers pop early, and colour lies under skin.'), ('Why rest the turkey before carving?', 'Thirty to forty minutes lets the juices redistribute instead of flooding the board, and buys exactly enough time to roast the vegetables and finish the gravy. Tent it loosely; it will not go cold.')]})

    pages.append({'slug': 'holiday-shipping-calculator', 'title': 'Holiday Shipping Calculator — Last Safe Posting Date', 'h1': 'Holiday Shipping Calculator', 'desc': 'When must holiday parcels be posted? Arrival date and destination give the last safe posting day, peak-season buffer and the online order deadline. Free, no sign-up.', 'category': 'calculator', 'keyword': 'last day to ship for christmas calculator', 'tool': 'shipdead', 'args': {}, 'intro': ['Enter when the parcel must arrive and how far it travels. The calculator works backwards through transit time, a peak-season buffer, and a further week for online ordering - the three dates that keep December deliveries honest.', "Carrier countdown pages publish their own deadlines last. This one computes your personal deadlines from the actual arrival date, explains why December's 'usually three days' becomes four, and prices the buffer that wins the bet."], 'howto': ['Enter the arrival date - the 24th, not the 25th morning, if it must be under the tree.', 'Pick the destination tier honestly; international December is the slow bracket.', 'Post on the date or earlier, and treat the online-order row as the real countdown.'], 'faqs': [('When is the last day to ship for Christmas?', 'Work backwards: domestic parcels want three transit days plus a buffer - roughly a week before; near-international two weeks; slow international four. The calculator turns your arrival date into the exact posting day.'), ("Why add a buffer to the carrier's transit time?", 'December networks run at capacity: sorting hubs overflow, weather compounds, and every delay lands on the last-posted parcels first. Half the transit time again is the stake that survives a bad day.'), ('How much earlier should I order online?', 'About a week before the posting deadline - warehouse handling sits on top of transit, and the advertised order-by date is one everyone else also read. Earlier orders also pick from full stock, not the dented leftovers.'), ('What if the parcel arrives when nobody is home?', 'Plan the landing: a safe spot, a neighbour, or a pickup point beats a redelivery card on the 27th. Digital gifts and hand-delivered ones keep no calendar - everything else is a bet against the network.')]})

    pages.append({'slug': 'leftover-storage-calculator', 'title': 'Leftover Storage Calculator — Eat or Freeze By Date', 'h1': 'Leftover Storage Calculator', 'desc': 'How long are leftovers good? Cook date and food type give the use-or-freeze date, the freezer extension and the one-reheat rule. Free, no sign-up.', 'category': 'calculator', 'keyword': 'how long do leftovers last calculator fridge', 'tool': 'leftover', 'args': {}, 'intro': ['Enter when the food was cooked, what it is, and where it lives. The calculator gives the use-or-freeze date - four fridge days for cooked meats, soups, rice and gravy, three for fish - plus the freezer extension and reheat rule.', 'Smell and sight both fail exactly where they matter most. This calculator runs the food-safety consensus on your actual dates: the four-day rule, the two-hour cooling window, and the one-way door of reheating.'], 'howto': ['Enter the cook date - be honest, the mystery box is always older than memory claims.', 'Pick the food type and storage; the fridge date is the deadline, the freezer is the pause button.', 'Label containers with the cook date so the next calculator is never needed from memory.'], 'faqs': [('How long do leftovers last in the fridge?', 'Three to four days for cooked meats, soups, stews, rice and gravies; cooked fish nearer three. The fridge slows bacterial generations, it never resets the clock - day four is the honest deadline, not the first smell.'), ('Can I freeze cooked leftovers?', 'Yes - freezing pauses the clock for about three months at best quality. Thaw in the fridge over a day, never on the counter, and expect texture changes in anything creamy; taste survives, structure sometimes does not.'), ('How quickly should leftovers be refrigerated?', 'Within two hours of cooking - sooner in summer heat. A shallow container cools fast; the stockpot on the counter keeps the whole depth in the danger zone for hours. The two-hour window is where safety is won.'), ('Is it safe to reheat leftovers twice?', "No - one thorough reheat to steaming is the rule. Each warm-up multiplies exactly the bacterial risk the four-day rule manages, and 'still tastes fine' is not a test anything dangerous agrees to.")]})

    pages.append({'slug': 'ski-trip-cost-calculator', 'title': 'Ski Trip Cost Calculator — Per-Person Budget by Days on Snow', 'h1': 'Ski Trip Cost Calculator', 'desc': 'What does a ski trip cost? Days, lift pass, rental, lessons and mountain food give the per-person total, the lift share and the season-pass crossover. Free, no sign-up.', 'category': 'calculator', 'keyword': 'ski trip cost calculator per person budget', 'tool': 'skicost', 'args': {}, 'intro': ['Enter days on snow, the daily lift price, rental, lessons and mountain food. The calculator totals the trip per person, shows what the lift ticket really contributes, and finds the day count where a season pass wins.', 'Resort calculators quote package magic. This one lays the five lines bare - and the surprise is that food and lodge outspend the lift pass, which the mountain knows and prices accordingly.'], 'howto': ["Enter realistic daily figures from the resort's price page - lift, rental, lesson as applicable.", 'Add the honest mountain-day food cost; the sun-deck coffee is part of the sport.', 'Read the season-pass crossover: past that day count, the pass pays for the rest of the winter.'], 'faqs': [('How much does a ski trip cost per person?', 'A week at mid-range European prices lands near 1,200-1,500 per person: passes around 350, rental 200, food and lodge the largest block, plus travel. The daily figure on this calculator is where that total hides or shrinks.'), ('When is a season pass worth it?', 'Past roughly ten to fifteen days on snow, depending on price - the crossover row computes yours. Early-bird sales in September often cut another third, which moves the crossover down two days for free.'), ('Are ski lessons worth the cost?', 'For beginners and plateaued intermediates, unambiguously: two days of instruction beats seasons of self-taught habit and prevents the injuries that end trips. It is the line item that repays in skill, not in savings.'), ('What costs do ski trip calculators forget?', "Travel to the mountain, parking or airport transfers, lunch on the sun deck, and the apres that starts as one drink. This calculator's food line exists so the fifth column never surprises the card statement.")]})

    pages.append({'slug': 'ski-rental-vs-own-calculator', 'title': 'Ski Rental vs Own Calculator — Break-even Days per Year', 'h1': 'Ski Rental vs Own Calculator', 'desc': 'Rent or buy skis? Days per year against rental price, kit cost and servicing give the break-even years - with the own-skis-rent-boots hybrid. Free, no sign-up.', 'category': 'calculator', 'keyword': 'ski rental vs buying calculator break even', 'tool': 'skirent', 'args': {}, 'intro': ['Enter how many days you ski, rental prices, the kit you would buy and yearly servicing. The calculator gives the break-even years - past which owning wins - and prices the hybrid most regulars actually settle on.', 'Shops sell kits; rental chains sell days. This one runs the honest crossover: owning wins around fifteen to twenty days a year, below that rental wins on money and on hassle - and boots are the exception that proves both.'], 'howto': ['Count your days on snow last season - honesty here decides the answer.', "Price a realistic kit from last season's stock, plus yearly wax and edge servicing.", 'Read the break-even years and consider the hybrid: own skis, rent boots, skip the luggage fees.'], 'faqs': [('Is it cheaper to rent or buy skis?', 'Below about fifteen days a year, renting wins - kit depreciation plus servicing beats the rental counter only for the committed. Above twenty days, owning pays and pays increasingly, especially on last-season stock bought in September.'), ('What does owning skis really cost per year?', 'Kit spread over a six-year life plus wax, edges and the occasional binding service - typically a third of what equivalent rental days would charge. The hidden costs are transport and storage, both real, both yours.'), ('Should I buy my own ski boots?', "Yes, before you buy skis - boots are the fit-critical half of skiing, and a fitted pair outperforms any rental on comfort and control. The locals' hybrid: own boots and skis, rent anything bulky or travel-hostage."), ('When do ski gear sales have the best prices?', "September for early-bird passes and last-season stock, and end-of-season March-April for everything else. The same ski with last year's top sheet is this year's bargain - geometry turns over gently, marketing does not.")]})

    pages.append({'slug': 'ski-length-calculator', 'title': 'Ski Length Calculator — Right Ski Size by Height, Weight and Skill', 'h1': 'Ski Length Calculator', 'desc': 'What length skis do you need? Height, weight and skill give the length in centimetres, the range either side, and the weight caveat shops skip. Free, no sign-up.', 'category': 'calculator', 'keyword': 'what length skis calculator height weight', 'tool': 'skilength', 'args': {}, 'intro': ['Enter your height, weight and skill level. The calculator gives a ski length in centimetres, the range either side worth considering, and the weight adjustment that charts printed on walls keep forgetting.', 'Rental shops size by eyeball and end-of-day patience. This one shows the modern arithmetic - chin to brow, weight bending the ski, skill picking the end of the range - so the shop conversation starts from your numbers, not their stock.'], 'howto': ['Enter height and weight; the weight adjustment is where the chart and the body disagree.', 'Pick your honest skill level - beginners take shorter for forgiveness, advanced longer for stability.', "Treat the result as the shop's starting point: terrain and preferred snow refine the final centimetres."], 'faqs': [('What length skis should I buy for my height?', 'Modern skis run chin to brow - roughly 15 to 25 cm shorter than you are tall, tuned by weight and skill. The old head-height rule belongs to straight skis; sidecut and rocker turned shorter into nimbler.'), ('Does weight matter more than height for ski length?', "For the turn's physics, weight matters: it bends the ski into its edge, so heavy-for-height skiers go longer or stiffer, light skiers shorter. Two same-height skiers of different builds genuinely need different skis."), ('Should beginner skis be shorter?', 'Yes - the shorter end of the range turns easier and forgives the late-weight-shift habits every beginner has. Length rewards skill with stability at speed; shortness rewards learning with control at realistic speeds.'), ('How do I know if my skis are too long?', "The tell is the turn you cannot finish: tips that won't release at low speed, legs exhausted by lunch, edges that wash out on hard snow. Rent one length down for a day before selling - the fix costs a day ticket, not a season.")]})

    pages.append({'slug': 'homework-time-calculator', 'title': 'Homework Time Calculator — the 10-Minutes-Per-Grade Guideline', 'h1': 'Homework Time Calculator', 'desc': 'How much homework is normal? Grade level gives the 10-minutes-per-grade guideline, focus blocks, and the signal that means talk to the teacher. Free, no sign-up.', 'category': 'calculator', 'keyword': 'how much homework by grade calculator', 'tool': 'homework', 'args': {}, 'intro': ["Enter your child's grade. The calculator applies the education establishment's own guideline - ten minutes per grade, capped across high school - and converts it into focus blocks a child can actually run.", 'Homework debates run on anecdotes. This one quotes the rule schools themselves set, declares what counts as abnormal, and explains the teacher conversation that a consistently doubled guideline deserves.'], 'howto': ['Enter the grade and count evening activity days.', 'Run homework in the focus blocks shown - real breaks between, phone in another room.', 'If reality runs double the guideline for weeks, that is diagnostic information for the teacher, not a character verdict.'], 'faqs': [('How much homework should a child have per night?', 'The guideline is ten minutes per grade: 30 minutes in third grade, an hour in sixth, and a 90-120 minute ceiling across high school. Consistently doubling it signals a problem with the assignment or the support, not the child.'), ('What is the ten-minute rule for homework?', "A widely cited education guideline - endorsed by teachers' associations - scaling homework from ten minutes in first grade upward by grade. It is a heuristic for sanity, not a quota for ambition; quality of attention beats duration every week."), ('How long should a homework session run before a break?', 'About 25 minutes for most children, longer for teens - attention has a duty cycle, and structured breaks beat grinding through. Four honest blocks outperform one miserable evening for everyone in the house.'), ('When should parents talk to the teacher about homework?', "When it consistently takes double the guideline, when tears are routine, or when the child cannot start without you. Frame it as data - 'twenty minutes of work takes two hours' - and the conversation is diagnostic, not adversarial.")]})

    pages.append({'slug': 'mattress-lifespan-calculator', 'title': 'Mattress Lifespan Calculator — Replace or Keep Sleeping?', 'h1': 'Mattress Lifespan Calculator', 'desc': 'Should you replace your mattress? Type and age set the expected life, sleep quality casts the vote - verdict plus rotation schedule. Free, no sign-up.', 'category': 'calculator', 'keyword': 'how often replace mattress calculator lifespan', 'tool': 'mattress', 'args': {}, 'intro': ["Pick your mattress type, enter its age and how your mornings have been. The calculator merges the industry lifespan with your body's vote - and gives the verdict: keep sleeping, start shopping, or replace now.", 'Mattress marketing sells by year count and fear. This one prices the alternative honestly: age sets the prior, but a mattress that sleeps well owes nobody a replacement, and one that aches every back has already failed regardless of its warranty.'], 'howto': ['Pick the type and count the years honestly.', 'Answer the sleep-quality question from the last month, not last night.', 'Check the physical tells - a body impression past 5 cm, sagging edges, better sleep anywhere else - and rotate head-to-foot.'], 'faqs': [('How often should you replace a mattress?', 'About eight years for innerspring, foam and hybrids; twelve to fifteen for latex. But the body outranks the calendar - a mattress that sleeps perfectly at year nine owes nobody a purchase, and one that aches at year two has failed.'), ('What are the signs a mattress needs replacing?', 'A body impression deeper than five centimetres, sagging edges, new morning stiffness that eases once you are up, and the quiet test: you sleep better in hotel beds than at home. Three of four means start shopping.'), ('Do mattress warranties cover sagging?', 'Only above a depth threshold - often 3-4 cm - and usually prorated, so year-seven claims refund a fraction. Read the warranty before relying on it; the comfort guarantee window is the part that actually protects you.'), ('How often should I rotate my mattress?', 'Every three to six months, head to foot. Flipping only applies to genuinely two-sided mattresses, which modern ones mostly are not - flipping a one-sided mattress puts the padding underneath where it does nothing.')]})

    pages.append({'slug': 'aquarium-heater-calculator', 'title': 'Aquarium Heater Calculator — Watts for Your Tank Volume', 'h1': 'Aquarium Heater Calculator', 'desc': 'What size aquarium heater? Tank litres and the temperature gap give the wattage, the two-heater threshold and the thermometer rule. Free, no sign-up.', 'category': 'calculator', 'keyword': 'aquarium heater size calculator watts litres', 'tool': 'aquaheat', 'args': {}, 'intro': ['Enter your tank volume, target water temperature and the coldest the room gets. The calculator sizes the heater in watts - about one watt per litre in a cold room - and flags when two heaters beat one.', 'Heater packaging quotes vague litre ranges. This one runs the actual arithmetic on your temperature gap, explains why oversized costs nothing extra to run, and prices the redundancy that turns a failure into a drift.'], 'howto': ["Enter litres and the species' target temperature - tropicals run 24-27°C.", 'Enter the coldest the room genuinely gets at night in winter.', 'Buy the wattage shown, a second for anything over 200 litres, and a glass thermometer that outranks the dial.'], 'faqs': [('What size heater for a 100 litre aquarium?', 'Roughly 75-100 W depending on the room: litres times the temperature gap times 0.09. A cold room with an 8°C gap wants the higher end; a warm flat can run less - but never run a heater flat out at its limit.'), ('Is a bigger aquarium heater wasteful?', 'No - the thermostat governs duty, not wattage, so an oversized heater runs shorter bursts at the same cost and survives cold snaps with margin. Undersized is the expensive mistake: it runs flat out, arrives late, and dies young.'), ('Should a big tank have two heaters?', 'Yes, past about 200 litres: one at each end spreads the heat instead of pooling it, and if one fails the other turns an emergency into a slow drift you will notice on the thermometer first.'), ('How accurate is the dial on an aquarium heater?', 'Treat it as a suggestion with a few degrees of drift - the independent thermometer is the fact. Cheap stick-on strips drift more; a small glass thermometer settles every argument for pocket change.')]})

    pages.append({'slug': 'cost-per-use-calculator', 'title': 'Cost Per Use Calculator — the Only Price Tag That Matters', 'h1': 'Cost Per Use Calculator', 'desc': 'Cost per use (or per wear): price divided by honest uses, against the 1-per-wear bar, with the half-use reality check and the closet audit. Free, no sign-up.', 'category': 'calculator', 'keyword': 'cost per wear calculator clothing value', 'tool': 'costperuse', 'args': {}, 'intro': ['Enter the price and how many times you will honestly use it - wears, rides, runs, brews. The calculator gives the cost per use, tests it against the one-per-wear bar, and runs the double-edge check: what if you use it half as much?', 'Fashion blogs invented cost per wear for clothes. This one works for everything - tools, gadgets, equipment - and adds the two steps the blogs skip: the half-use reality check where optimism lives, and the closet audit that prices your actual history instead of your intentions.'], 'howto': ['Enter the real price and your honest use count - the version of you from the last twelve months, not the aspirational one.', 'Halve the uses and see whether the figure still clears your bar.', 'Run the closet audit yearly: the average price of things barely worn is your personal bar for the next want.'], 'faqs': [('What is the cost per wear rule?', 'Divide price by expected wears; at one per wear or better, the item is earning its keep. The rule generalises to cost per use for anything - tools, bikes, machines - and turns shopping arguments into arithmetic.'), ('Why do cheap items often cost more per use?', 'A 40 jacket worn twice costs 20 a wear; a 300 coat worn all winter costs about one. Durability and love of use are the multipliers - the cheapest price tag routinely hides the most expensive object in the wardrobe.'), ('How do I estimate uses honestly?', 'Use your history, not your plans: how often did you use the last similar thing in the first year? The aspirational user exercises five times a week; the real one the calculator prices shows up on Tuesdays, sometimes.'), ('What is a closet audit?', "Count the garments worn fewer than five times last year, average what they cost, and let that figure - typically hundreds - set your bar. It is the only price index built from your own behaviour rather than a shop's.")]})

    pages.append({'slug': 'wishlist-30-day-calculator', 'title': '30-Day Wish List Calculator — the Cooling-Off Buy-On Date', 'h1': '30-Day Wish List Calculator', 'desc': 'Beat impulse buying: enter when the wanting started and get the buy-on date, the three-question gate and the price-alert trick. Free, no sign-up.', 'category': 'calculator', 'keyword': '30 day rule before buying calculator', 'tool': 'wishlist30', 'args': {}, 'intro': ['Enter when you started wanting it and pick a cooling-off length - thirty days is the classic. The calculator gives the buy-on date: purchase then if you still want it, or let it expire silently if the feeling did.', 'Anti-impulse advice says wait; this one dates the wait. Wanting is a chemical event with a half-life, and the calendar is how you let it decay without willpower - most list items simply stop mattering, and that is the entire saving.'], 'howto': ['Enter the date the wanting started - the day you first opened the tab counts.', 'Read the buy-on date and write the item on a real list; close the tab.', 'On the date, run the gate: still want it, does it fit your life, can you pay without borrowing - all three, then buy guilt-free.'], 'faqs': [('What is the 30-day rule for purchases?', 'Note the want, wait thirty days, and buy only if the want survived. It works because desire decays measurably faster than prices rise: the surge that made the purchase feel inevitable usually expires sometime in week two.'), ('Does the waiting rule work for small purchases?', 'Use shorter cooling-offs - seven days for small wants, fourteen for medium - the decay curve is the same at every price. The habit matters more than the duration: wanting, dating, and deciding instead of tapping.'), ('What if the price rises while I wait?', "Sometimes it does - and sometimes it drops, especially with alerts set on a wish list. The rule's savings come mostly from the items that expire, not the timing; a price alert catches the drops without keeping a tab open."), ('What are the three questions before buying?', 'Still want it after the wait, does it fit your actual life, and can you pay without borrowing or a payment plan. All three yeses make it a decision rather than an impulse - and decisions deserve to happen.')]})

    pages.append({'slug': 'work-hours-price-calculator', 'title': 'Work Hours Price Tag — What Things Cost in Your Hours', 'h1': 'Work Hours Price Tag', 'desc': 'What does it cost in your hours? Price divided by your net hourly gives the work-days figure - the exchange rate that never lies. Free, no sign-up.', 'category': 'calculator', 'keyword': 'how many hours of work to afford calculator', 'tool': 'workhours', 'args': {}, 'intro': ['Enter the price, your monthly take-home and your work hours. The calculator prints the price tag in the only currency that cannot be printed: hours of your life, in work days as well as hours.', 'Everything is priced in money so nobody has to read it in hours. This one does the conversion at your real net rate - tax already took its share - and lets the number decide, because some things are easily worth eight workdays and others never survive the translation.'], 'howto': ['Enter the price and your take-home pay - net, the money that actually reaches you.', 'Count your real monthly hours, commute included if you want the honest rate.', 'Read the days figure and let it vote: the tool never says no, it says know what you paid.'], 'faqs': [('How do I work out what something costs in work hours?', 'Divide the price by your net hourly rate - take-home divided by real work hours. A 600 purchase at 17.50 net hourly is 34 hours, four workdays: the same object, priced in the currency you actually paid.'), ('Why use net pay instead of gross for this?', 'Gross includes the tax share you never hold, so it flatters your hourly and flatters the purchase. The hours you worked for the sticker price are the hours that reached your account - net is the honest exchange rate.'), ('Is the work-hours framing healthy or guilt-inducing?', "It is resolution, not prohibition: some things are obviously worth four workdays - the tool says know, not don't. Used without judgment it kills the forgettable purchases and keeps the meaningful ones, which is the whole point."), ('Should commute time count in my hourly rate?', 'For the truest rate, yes: a job that pays 25 an hour but takes two unpaid commuting hours daily pays something less. Doing the arithmetic twice - with and without the fine print - is the honest version of salary comparison.')]})

    pages.append({'slug': 'moon-phase-calculator', 'title': "Moon Phase Calculator - Tonight's Moon for Any Date", 'h1': 'Moon Phase Calculator', 'desc': 'Pick any date and get the moon phase, illuminated fraction and moon age, computed live from the 29.53-day synodic cycle - plus the next full moon. Honest about the one-day tolerance, instant, free.', 'category': 'calculator', 'keyword': 'moon phase calculator what is the moon phase tonight', 'tool': 'moonphase', 'args': {}, 'intro': ["Type any date - tonight, a wedding, a camping trip, a historical morning - and this calculator returns the moon's phase name, its emoji, the illuminated fraction and its age in days, plus the next full moon after that date. Everything is computed live in your browser from the 29.5306-day synodic cycle, so the answer arrives before a moon-phase site finishes loading its ads.", 'Moon almanac sites freeze one year per page and bury the phase behind article text. This one answers any date at once and tells you the size of its own error - about a day - instead of pretending almanac precision. The result lands in your tab title, so the moon follows you while you open other tabs.'], 'howto': ['Pick a date (today is pre-filled).', 'Read the phase name, emoji and illuminated percentage.', 'Check the next full moon date - or share the result link.'], 'faqs': [('How accurate is this moon phase calculator?', 'It uses the mean synodic cycle of 29.5306 days counted from a reference new moon, which can drift up to about a day from official almanac times. For minute-precise times an observatory table wins; for any-date answers this is faster than looking one up.'), ('What is the moon phase tonight?', "Today's date is pre-filled, so the big emoji shows tonight's phase the moment the page opens, with the illuminated fraction and the next full moon date beside it."), ('Why does the moon age matter?', 'Moon age is how many days past new moon the date sits - day 0 is new, about 14.77 is full, and the count explains why full moons shift about 11 days earlier each calendar year.'), ('Does my location change the moon phase?', 'No - the phase depends only on the date. Where you are changes when the moon rises, not how lit it is.')]})
    pages.append({'slug': 'full-moon-calendar', 'title': 'Full Moon Calendar - Every Full Moon in Any Year', 'h1': 'Full Moon Calendar', 'desc': 'Type any year and get every full moon date in it, computed live from the synodic cycle - twelve or thirteen, first to last, with the blue-moon years flagged. No frozen tables, no ads between dates.', 'category': 'calculator', 'keyword': 'full moon calendar full moons this year dates', 'tool': 'fullmooncal', 'args': {}, 'intro': ['Enter a year and the calendar lists every full moon in it with dates, counts them, and flags the years that get thirteen - the blue moon years. Because the list is computed from the 29.5306-day cycle rather than copied from a printed table, any year from 1900 to 2100 answers instantly, including years no almanac ever bothered to print.', 'Most full moon pages are one frozen year per page, tuned for ads. This one answers the question people actually have - when are the full moons - for any year at once, and says plainly that the simple cycle carries about a day of tolerance, so you know when to trust it for a moonlit walk and when to check an observatory for an eclipse.'], 'howto': ['Type a year (this year is pre-filled).', 'Read the dated list and the count.', 'Watch for the extra-moon flag - that year has a blue moon.'], 'faqs': [('How many full moons are in a year?', 'Usually twelve - one synodic month is 29.53 days versus about 30.4 days per calendar month, so a full moon lands roughly every month. Thirteen arrive when one falls in the first days of January, and those years are marked here.'), ('What is a blue moon?', 'The common modern meaning is the second full moon in one calendar month, which happens in the same years that fit thirteen full moons. The calendar flags those years so you know where to look.'), ('How precise are these full moon dates?', "Within about a day of official almanac times, because the simple synodic cycle ignores the orbit's elliptical speed-ups. For eclipse nights or minute-precise timing, an observatory table is the better tool."), ('Can I see full moons for a past year?', 'Yes - any year from 1900 to 2100 works, which printed calendars never bother covering.')]})
    pages.append({'slug': 'birthday-moon', 'title': 'Birthday Moon - What Was the Moon Phase When You Were Born?', 'h1': 'Birthday Moon', 'desc': 'Enter your birth date and meet the moon you were born under - phase, emoji, illuminated fraction - computed live for any birthday since 1900. One-tap share settles the group chat.', 'category': 'calculator', 'keyword': 'birthday moon phase what moon was i born under', 'tool': 'bdaymoon', 'args': {}, 'intro': ['Type your birth date and the page shows the moon that hung over it: the phase name, its emoji, how lit it was and how old the moon was that night, plus the first full moon that followed you into the world. The answer is computed live for any date in seconds - no paging through archived almanacs.', 'Birthday-moon sites wrap a one-line answer in horoscope copy and signup walls. This one gives the astronomy straight, says plainly that everyone born on your date shares the phase, and hands you the share link - roughly one person in eight carries your lunar emoji, which is the part of astrology that is actually true.'], 'howto': ['Enter your birth date.', "Read your moon's phase, emoji and illumination.", 'Share the result - one in eight friends will match your emoji.'], 'faqs': [('What was the moon phase when I was born?', 'Type your birth date and the phase appears instantly - name, emoji and illuminated fraction, computed from the synodic cycle with about a day of tolerance.'), ('Does my birth time or place change my birthday moon?', 'No - the phase depends only on the date. Your location changes moonrise times, not the fraction lit; everyone born on your date shares the same phase.'), ('Why do people care about birth moons?', 'Mostly for the fun of a concrete, checkable fact - the emoji doubles as a badge, and about one in eight people share yours, which makes it a better icebreaker than a star sign.'), ('How far back does it work?', "Any date from 1900 onward - grandparents' birthdays included.")]})
    pages.append({'slug': 'firewood-calculator', 'title': 'Firewood Calculator - How Many Cords You Need for Winter', 'h1': 'Firewood Calculator', 'desc': 'Enter heated area, climate and species to get cords for the winter, total cost and dollars per million Btu against electric heat - with the labor cost most firewood pages skip. Free, instant.', 'category': 'calculator', 'keyword': 'firewood calculator how many cords of firewood for winter', 'tool': 'firewood', 'args': {}, 'intro': ['Enter your heated square footage, how cold your winters get, the species and the going price per cord, and this calculator returns cords for the winter, the total damage and the number that actually matters: dollars per million Btu, set against electric resistive heat at the same output. The rule of thumb is on the table - roughly 2, 3 or 4.5 cords per 1000 sq ft by climate - so you can argue with it instead of trusting it.', 'Firewood sellers quote cords, not heat, and a softwood cord at half the oak price is not half the deal - it carries roughly half the Btu. This page converts everything to dollars per million Btu, and it also prices the part most pages hide: your labor. Wood wins on fuel cost if your time is cheap to you; the calculator leaves that judgment to you on purpose.'], 'howto': ['Enter heated area and pick your climate.', 'Add species and local price per cord.', 'Read cords, total cost and the per-Btu verdict.'], 'faqs': [('How many cords of firewood do I need for winter?', 'A common rule is 2 cords per 1000 sq ft in mild climates, 3 in moderate and up to 4.5 in cold ones, assuming wood is a main or heavy supplementary heat in a reasonably tight house. Insulation and how much you burn evenings change it more than any formula.'), ('Is softwood firewood worth half the price?', 'Only if it is actually half the price - seasoned softwood carries roughly 15 million Btu per cord versus about 26 for hardwood, so per unit of heat the discount shrinks. The per-million-Btu line in this calculator settles it with your local prices.'), ('What does a cord of firewood cost?', 'Commonly $200-400 delivered depending on region and species - enter your local number. A cord is a stacked stack 4x4x8 ft, 128 cubic feet, which the seasoning calculator uses directly.'), ('Should I heat my whole house with wood?', 'You can, but the calculator prices only the fuel. Add the labor - hauling, stacking, tending the stove at 5 am - and judge honestly; many households land on wood for the rooms that matter and gas or electric for the rest.')]})
    pages.append({'slug': 'fire-pit-vs-patio-heater', 'title': 'Fire Pit vs Patio Heater - Real Cost per Hour Compared', 'h1': 'Fire Pit vs Patio Heater', 'desc': 'Wood fire pit, propane patio heater or electric infrared - enter your local prices and see the honest cost per hour of each, assumptions on the table. The cheapest heat is rarely the one being sold.', 'category': 'calculator', 'keyword': 'fire pit vs patio heater cost per hour propane', 'tool': 'firepitvs', 'args': {}, 'intro': ['Backyard heat has three contenders and sellers quote none of them per hour. This calculator does: a wood bundle burned in a fire pit, a 20-lb propane tank drunk by a 40,000 Btu patio heater, and a 1500-watt electric infrared panel - enter your local prices and read the cost per hour of each, with every assumption written where you can argue with it.', 'Patio heater listings sell BTUs and fire pit blogs sell vibes; neither says what an evening costs. The answer flips the usual sales pitch: electric infrared is roughly twenty times cheaper per hour than wood - but it warms a person, not a party. Propane buys a 12-ft circle, wood buys the smell and the sparks. This page prices the heat and leaves the atmosphere to you.'], 'howto': ['Enter wood bundle, propane refill and electricity prices.', 'Read the per-hour cost of all three.', 'Pick the heat that matches the evening you want.'], 'faqs': [('How much does a fire pit cost per hour to run?', 'A store bundle of wood (about 0.75 cubic feet) burns roughly 1.5 hours in a fire pit, so at $8 a bundle you are paying about $5 per hour - enter your local bundle price for your number.'), ('How long does a 20-lb propane tank last on a patio heater?', 'About 10-11 hours: the tank holds roughly 430,000 Btu and a typical patio heater burns 40,000 Btu per hour. Divide your refill price by that to get the hourly cost.'), ('Are electric patio heaters cheap to run?', 'Per hour, yes - a 1500-watt infrared panel costs about 15-35 cents depending on your rate, far under wood or propane. The catch is coverage: it heats the person in front of it, not the circle.'), ('Which backyard heater should I buy?', 'Match the heater to the evening: cheap reading warmth is electric, a circle of guests is propane, and if you want crackle and smell, wood - now priced honestly per hour.')]})
    pages.append({'slug': 'firewood-seasoning', 'title': 'Firewood Seasoning Calculator - When Is Your Stack Ready to Burn?', 'h1': 'Firewood Seasoning Calculator', 'desc': 'Enter your split date and species to get the seasoning-ready month, plus cords in your stack from its footprint - and the tell-tale signs (crack, clack, hiss) that beat any calendar.', 'category': 'calculator', 'keyword': 'firewood seasoning time how long to season firewood', 'tool': 'seasoning', 'args': {}, 'intro': ['Split wood is a promise the calendar has to keep: oak wants about 12 months, ash and pine are usable near 6, birch sits between. Enter your split date and species and this calculator returns the ready month, plus how many cords your stack holds from its length and height (a row 4 ft deep, the standard cord math of 128 cubic feet).', 'Firewood buying guides pretend seasoning is a detail; it is the whole product - wet wood burns half as hot and coats your stove in creosote. This page gives the species timelines, the stack-to-cord math, and the field tests that beat any date: grey cracked split faces, bark peeling off, a clack instead of a thud when two logs meet, and the hiss that means a wet log is burning your money.'], 'howto': ['Enter your split date and species.', 'Add stack length and height for the cord count.', 'Read the ready month and check the signs before burning.'], 'faqs': [('How long does firewood take to season?', 'Split oak wants about 12 months; ash and pine are near 6; birch around 9. Splitting early matters more than species - a whole round seasons far slower than split pieces, so wood cut this spring burns this winter.'), ('How can I tell if firewood is seasoned?', 'Look for grey, cracked split faces and loosening bark; knock two logs together - seasoned wood clacks, wet wood thuds; and if it hisses while burning, it is still wet and paying twice for the heat.'), ('How many cords are in my stack?', 'One row 4 ft deep: multiply length by height by 4 feet and divide by 128 cubic feet - an 8-ft by 4-ft row is a quarter cord. The calculator does it from your stack measurements.'), ('Should I cover my wood stack?', 'Cover the top only, and leave the sides open - wind pulls the moisture out, a full tarp traps it in. Stack off the ground on pallets or rails so the bottom row seasons too.')]})
    pages.append({'slug': 'pumpkin-pie-calculator', 'title': 'Pumpkin Pie Calculator - How Many Pies for Your Guests', 'h1': 'Pumpkin Pie Calculator', 'desc': 'Enter guests and appetite to get pies, cups of puree, 15-oz cans, eggs and sugar - the full shopping math for one 9-inch pie feeding eight. Free, instant, no signup.', 'category': 'calculator', 'keyword': 'pumpkin pie calculator how many pies per guest thanksgiving', 'tool': 'pumpkinpie', 'args': {}, 'intro': ['Enter how many guests and how generous your slices are, and this calculator converts it to the shopping list: pies, cups of puree, 15-oz cans, eggs and sugar, all from one standard recipe - a 9-inch pie feeds eight polite slices and drinks 2 cups of puree. The slice slider settles the eternal holiday argument between one polite slice and seconds.', 'Most pie pages give one recipe and wish you luck scaling it; the classic failure is eleven guests and two pies where one would do, or one can short on the morning of. This page does the arithmetic both directions and says plainly which pumpkin to buy: baking sugar pumpkins roast down to better flavor, but canned puree has standardized moisture and is the reliable pick for a first crust.'], 'howto': ['Enter your guest count.', 'Pick the slice generosity - the slider is the honesty control.', 'Read pies, cans and the rest of the shopping list.'], 'faqs': [('How many people does a pumpkin pie feed?', 'One 9-inch pie cuts into 8 polite slices; the slider lets you budget 1.5 or 2 slices per guest for holiday appetites, which is usually the safer plan.'), ('How much puree is in a 15-oz can?', 'About 1.75 cups, and one 9-inch pie needs 2 cups - so one can plus a little fresh roasted, or round up cans; leftover puree freezes well for the next batch.'), ('Can I use a carving pumpkin for pie?', 'Technically yes, but flavor and texture lose: buy small baking (sugar) pumpkins, 3-4 lbs each, which roast down to about 2 cups of denser, sweeter flesh than a stringy jack-o-lantern.'), ('Why is my pumpkin pie filling soggy or watery?', 'Usually moisture: canned puree is standardized, fresh roasted varies a lot - strain fresh puree through a cloth, and pre-bake or blind-bake the crust so the filling does not soak it.')]})
    pages.append({'slug': 'pumpkin-carving-timing', 'title': 'Pumpkin Carving Timing - The Right Day for a Fresh Jack-o-Lantern', 'h1': 'Pumpkin Carving Timing', 'desc': 'Carve too early and your Jack-o-lantern sags by Halloween. Pick your preservation method and get the carving date that keeps it fresh for the night that matters.', 'category': 'calculator', 'keyword': 'when to carve pumpkins how early can you carve halloween', 'tool': 'carvetiming', 'args': {}, 'intro': ['A carved pumpkin is produce with a countdown: left alone it holds about four days once cut, petroleum jelly on the cuts stretches it toward six, a bleach-water spray buys five, and the porch-days fridge-nights rhythm is the strongest at about seven. Enter your method and this planner works backward from October 31 to give you the carving date - plus whether carving today is commitment or mistake.', 'The internet says carve whenever; produce says otherwise, and every year the sad ones prove it. This page treats the Jack-o-lantern as what it is - a cut vegetable on a porch - gives each preservation folk method its honest stretch, and answers the question people actually search the week before Halloween: not how to carve, but when.'], 'howto': ['Pick your preservation method - be honest about your discipline.', 'Read your carving date, worked back from Halloween.', 'Carve on the date, keep the lid on between shows.'], 'faqs': [('When should I carve my pumpkin for Halloween?', 'Work backward from your freshness window: with no treatment, carve about 4 days before Halloween; with the fridge-night method, up to a week. The calculator gives your date from the method you will actually keep up.'), ('How do I make a carved pumpkin last longer?', 'The strongest routine is porch days and fridge nights; petroleum jelly seals moisture into cut faces, and a bleach-water spray slows mold but washes off in rain. All methods stretch days, none stop the clock.'), ('Why did my jack-o-lantern rot in three days?', 'Cut faces dry out and mold spores get to work - heat and sun speed it up. Carve later, scoop the walls thinner, and keep the lid on when it is off duty.'), ('How long do uncarved pumpkins last?', 'Weeks on a cool dry porch - which is the real answer: buy late and whole, and carve close to the date instead of preserving a carved one for weeks.')]})
    pages.append({'slug': 'pumpkin-seeds-roast-calculator', 'title': 'Pumpkin Seeds Roast Calculator - Yield, Servings and Roast Time', 'h1': 'Pumpkin Seeds Roast Calculator', 'desc': 'Enter your pumpkin weight to get cups of seeds, snack servings, oil and salt, and the roast time at 300 or 350 F - plus the simmer step most recipes skip that makes them crisp.', 'category': 'calculator', 'keyword': 'pumpkin seeds roast time and temperature how many seeds per pumpkin', 'tool': 'seedroast', 'args': {}, 'intro': ['Enter your pumpkin weight and this calculator returns the seed haul - about a quarter cup per pound - the snack servings it makes, the oil and salt to toss with, and roast minutes for 300 or 350 F. The carving leftovers stop being waste and become the actual snack of the evening, with the math to prove it.', 'Seed recipes assume one mystery pumpkin; this page starts from the weight you actually have and scales everything: yield, servings, seasoning and time. The tip that separates crisp from chewy is in the note - a 10-minute salted simmer before roasting - and the honest closing line is that the pumpkin does not care whether it was bought to carve or to eat.'], 'howto': ['Weigh your pumpkin and enter it.', 'Pick your oven temperament - 300 F for even, 350 F for speed.', 'Read cups, servings and the roast timer.'], 'faqs': [('How many seeds are in a pumpkin?', 'Roughly a quarter cup of cleaned seeds per pound of whole pumpkin - a 5-lb carving pumpkin nets about three quarters of a cup, enough for three snack servings.'), ('What temperature roasts pumpkin seeds best?', '300 F for about 30-35 minutes gives even crisp without scorching; 350 F finishes in 22-28 minutes but watches closer. Stir once mid-roast either way.'), ('Why simmer pumpkin seeds before roasting?', 'A 10-minute simmer in salted water cooks the inside slightly so the oven crisps the shell instead of steaming it - the step most recipes skip and the difference between crisp and chewy.'), ('Do you eat pumpkin seed shells?', 'Yes - roasted shell-on seeds are the classic snack; the shell is where the salt and crunch live. Hulling them is a hobby, not a requirement.')]})
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
