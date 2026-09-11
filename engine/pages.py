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
    pages.append(_conv("yards-to-meters", "Yards to Meters", "yards", "meters", 0.9144, "length",
                       "Yards rule American football fields, golf courses and fabric counters; meters rule everything else. One yard is exactly 0.9144 meters — so a 100-yard football field is 91.44 meters of pure metric confusion.",
                       "Handy anchors: 1 yd = 0.91 m, 10 yd = 9.14 m, 100 yd = 91.44 m, 1 m = 1.09 yd (slightly more than a yard)."))
    pages.append(_conv("pints-to-liters", "Pints to Liters", "pints (US)", "liters", 0.473176473, "volume",
                       "The pint is the unit of pub culture — but it depends where you drink. A US pint is 473 ml; an imperial (UK) pint is a heftier 568 ml. This converter uses the US pint, the one on American labels and beer taps.",
                       "Handy anchors: 1 US pint = 0.47 L, 2 pints = 0.95 L (a quart), 8 pints = 3.79 L (a gallon). UK drinkers: 1 imperial pint = 0.57 L."))
    pages.append(_conv("inches-to-mm", "Inches to MM", "inches", "millimeters", 25.4, "length",
                       "Precision work — drill bits, camera mounts, 3D printing, jewelry — lives in millimeters, while US tools and hardware still speak inches. One inch is officially exactly 25.4 millimeters, so this conversion is precise to any decimal place.",
                       "Handy anchors: 1 in = 25.4 mm, 1/2 in = 12.7 mm, 1/4 in = 6.35 mm, 2 in = 50.8 mm. Woodworkers: 3/4 in stock = 19.05 mm."))

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
