"""task19 names: each person's name and date of birth as each system holds them.

Nationals take Irish and English names; residents from abroad take the names of their origin group, with diacritics
some systems drop, compound surnames some systems shorten, and two or three romanisations of names written in another
script. Each system records the same person its own way: a nickname, a surname changed at marriage, a slip of the
keyboard, a day and month swapped, a date of birth one system only knows as the first of January."""
import unicodedata

import numpy as np
from faker import Faker

import params as PR

NICK = {
    "Catherine": ["Kate", "Cathy"], "Katherine": ["Kate", "Katie"], "Elizabeth": ["Liz", "Beth"], "Margaret": ["Maggie", "Peggy"],
    "Patrick": ["Pat", "Paddy"], "Michael": ["Mick", "Mike"], "James": ["Jim", "Jimmy"], "Thomas": ["Tom"], "Daniel": ["Dan", "Danny"],
    "Joseph": ["Joe"], "Edward": ["Eddie", "Ted"], "Robert": ["Rob", "Bob"], "William": ["Bill", "Will"], "Anthony": ["Tony"],
    "Christopher": ["Chris"], "Matthew": ["Matt"], "Nicholas": ["Nick"], "Stephen": ["Steve"], "Andrew": ["Andy"],
    "Jennifer": ["Jenny"], "Rebecca": ["Becky"], "Samantha": ["Sam"], "Benjamin": ["Ben"], "Alexander": ["Alex"],
    "Deborah": ["Debbie"], "Patricia": ["Trish", "Pat"], "Josephine": ["Josie"], "Bernadette": ["Bernie"], "Gerard": ["Ger"],
    "Kathleen": ["Kathy"], "Eileen": ["Eily"], "Brendan": ["Brenny"], "Francis": ["Frank"], "Frances": ["Fran"],
    "Jonathan": ["Jon"], "Timothy": ["Tim"], "Philip": ["Phil"], "Richard": ["Rich", "Dick"], "Gabriel": ["Gabe"],
    "Siobhan": ["Shiv"], "Dermot": ["Derm"], "Cornelius": ["Con"], "Jeremiah": ["Jerry"], "Bridget": ["Bridie"],
}

# English and Irish forms of the same forename: one system holds one, the other the other
IRISH = {"John": "Sean", "James": "Seamus", "Patrick": "Padraig", "Mary": "Maire", "Owen": "Eoghan", "William": "Liam",
         "Joan": "Siobhan", "Hugh": "Aodh", "Denis": "Donncha", "Jeremiah": "Diarmuid", "Margaret": "Mairead",
         "Bridget": "Brid", "Catherine": "Caitriona", "Peter": "Peadar", "Michael": "Micheal", "Thomas": "Tomas",
         "Helen": "Eibhlin", "Kate": "Cait", "Charles": "Cathal", "Daniel": "Domhnall", "Eugene": "Eoin",
         "Timothy": "Tadhg", "Bernard": "Brian", "Florence": "Finola", "Edward": "Eamonn", "Brigid": "Brid",
         "Joseph": "Seosamh", "Anne": "Aine", "Nora": "Nora", "Martin": "Mairtin", "Stephen": "Steafan", "Gerard": "Gearoid"}
IRISH.update({v: k for k, v in list(IRISH.items())})
GAELIC = {"Murphy": "O Murchu", "Kelly": "O Ceallaigh", "Sullivan": "O Suilleabhain", "Walsh": "Breathnach",
          "Smith": "Mac Gabhann", "O'Brien": "O Briain", "Byrne": "O Broin", "Ryan": "O Riain", "O'Connor": "O Conchuir",
          "O'Neill": "O Neill", "O'Reilly": "O Raghallaigh", "Doyle": "O Dubhghaill", "McCarthy": "Mac Carthaigh",
          "Gallagher": "O Gallchobhair", "O'Doherty": "O Dochartaigh", "Kennedy": "O Cinneide", "Lynch": "O Loingsigh",
          "Murray": "Mac Muireadhaigh", "Quinn": "O Cuinn", "Moore": "O Mordha", "McLoughlin": "Mac Lochlainn",
          "O'Carroll": "O Cearbhaill", "Connolly": "O Conghaile", "Daly": "O Dalaigh", "O'Connell": "O Conaill",
          "Wilson": "Mac Liam", "Dunne": "O Duinn", "Brennan": "O Braonain", "Burke": "de Burca", "Collins": "O Coileain",
          "Campbell": "Mac Cathmhaoil", "Clarke": "O Cleirigh", "Johnston": "Mac Seain", "Hughes": "O hAodha",
          "O'Farrell": "O Fearghail", "Fitzgerald": "Mac Gearailt", "Brown": "de Brun", "Martin": "Mac Mairtin",
          "Maguire": "Mag Uidhir", "Nolan": "O Nuallain", "Flynn": "O Floinn", "Thompson": "Mac Tomais",
          "O'Callaghan": "O Ceallachain", "O'Donnell": "O Domhnaill", "Duffy": "O Dubhthaigh", "O'Mahony": "O Mathuna",
          "Boyle": "O Baoill", "Healy": "O hEalaighthe", "O'Shea": "O Se", "White": "de Faoite", "Sweeney": "Mac Suibhne",
          "Hayes": "O hAodha", "Kavanagh": "Caomhanach", "Power": "de Paor", "McGrath": "Mac Craith", "Moran": "O Morain",
          "Brady": "Mac Bradaigh", "Stewart": "Stiobhard", "Casey": "O Cathasaigh", "Foley": "O Foghlu",
          "Fitzpatrick": "Mac Giolla Phadraig", "O'Leary": "O Laoghaire", "McDonnell": "Mac Domhnaill", "McMahon": "Mac Mathuna",
          "Donnelly": "O Donnghaile", "Regan": "O Riagain", "Donovan": "O Donnabhain", "Burns": "O Broin",
          "Flanagan": "O Flannagain", "Mullan": "O Maolain", "Barry": "de Barra", "Kane": "O Cathain", "Robinson": "Mac Roibin",
          "Cunningham": "O Cuinneagain", "Griffin": "O Griofa", "Kenny": "O Cionaoith", "Sheehan": "O Siochain",
          "Ward": "Mac an Bhaird", "Whelan": "O Faolain", "Lyons": "O Liathain", "Reid": "Mac Riada", "Graham": "Greachan",
          "Higgins": "O hUiginn", "Cullen": "O Cuilinn", "Keane": "O Cathain", "King": "Mac Conraoi", "Maher": "O Meachair",
          "McKenna": "Mac Cionaoith", "Bell": "Mac Giolla Mhaoil", "Scott": "Scot", "Hogan": "O hOgain",
          "O'Keeffe": "O Caoimh", "Magee": "Mag Aoidh", "McNamara": "Mac Conmara", "McDonald": "Mac Domhnaill",
          "McDermott": "Mac Diarmada", "Moloney": "O Maoldhomhnaigh", "O'Rourke": "O Ruairc", "Buckley": "O Buachalla",
          "O'Dwyer": "O Duibhir"}
USED_NAME = {"m": ["Tom", "Alex", "Sam", "Mark", "Adam", "Peter", "Mo", "Ali", "Max", "Dan", "Jack", "Ben"],
             "f": ["Kate", "Anna", "Sara", "Maria", "Lily", "Eva", "Mia", "Nina", "Kasia", "Gosia", "Lucy", "Amy"]}

# Romanisations: each group is one name written several ways
_G = {
    "Mohammed": ["Mohammed", "Muhammad", "Mohamed", "Mohammad"], "Ahmed": ["Ahmed", "Ahmad"],
    "Hussein": ["Hussein", "Hussain", "Husain"], "Hassan": ["Hassan", "Hasan"], "Yusuf": ["Yusuf", "Youssef", "Yousef"],
    "Ibrahim": ["Ibrahim", "Ebrahim"], "Mustafa": ["Mustafa", "Mostafa"], "Karim": ["Karim", "Kareem"], "Omar": ["Omar", "Umar"],
    "Khalid": ["Khalid", "Khaled"], "Abdullah": ["Abdullah", "Abdallah"], "Tariq": ["Tariq", "Tarek", "Tarik"],
    "Walid": ["Walid", "Waleed"], "Samir": ["Samir", "Sameer"], "Rashid": ["Rashid", "Rasheed"], "Faisal": ["Faisal", "Faysal"],
    "Imran": ["Imran", "Emran"], "Rahul": ["Rahul"], "Arjun": ["Arjun"], "Vikram": ["Vikram", "Vikrum"], "Sanjay": ["Sanjay"],
    "Rajesh": ["Rajesh", "Rajes"], "Anil": ["Anil"], "Suresh": ["Suresh"], "Rakib": ["Rakib", "Raqib"], "Shahid": ["Shahid", "Shaheed"],
    "Fatima": ["Fatima", "Fatimah", "Fatma"], "Aisha": ["Aisha", "Ayesha", "Aysha"], "Zainab": ["Zainab", "Zaynab"],
    "Mariam": ["Mariam", "Maryam"], "Nour": ["Nour", "Noor", "Nur"], "Leila": ["Leila", "Layla", "Laila"],
    "Yasmin": ["Yasmin", "Yasmeen"], "Amina": ["Amina", "Aminah"], "Samira": ["Samira", "Sameera"], "Rania": ["Rania", "Raniya"],
    "Hana": ["Hana", "Hanaa"], "Priya": ["Priya"], "Anjali": ["Anjali"], "Sunita": ["Sunita", "Suneeta"],
    "Nasrin": ["Nasrin", "Nasreen"], "Shirin": ["Shirin", "Shireen"], "Rukhsana": ["Rukhsana", "Rokhsana"],
    "Farzana": ["Farzana", "Farjana"], "Sadia": ["Sadia", "Saadia"],
    "Rahman": ["Rahman", "Rehman"], "Hossain": ["Hossain", "Hussain", "Husain"], "Chowdhury": ["Chowdhury", "Choudhury", "Chaudhry"],
    "Islam": ["Islam"], "Uddin": ["Uddin", "Udin"], "Siddiqui": ["Siddiqui", "Siddiqi"], "Qureshi": ["Qureshi", "Kureshi"],
    "Khan": ["Khan"], "Ali": ["Ali"], "Begum": ["Begum"], "Akhtar": ["Akhtar", "Akter"], "Sharma": ["Sharma"], "Patel": ["Patel"],
    "Singh": ["Singh"], "Kumar": ["Kumar"], "Das": ["Das"], "Gupta": ["Gupta"], "Mukherjee": ["Mukherjee", "Mukerji"],
    "Bhattacharya": ["Bhattacharya", "Bhattacharjee"], "Haddad": ["Haddad", "Hadad"], "Mansour": ["Mansour", "Mansur"],
    "Nasser": ["Nasser", "Nasir"], "Saleh": ["Saleh", "Salih"], "Abdallah": ["Abdallah", "Abdullah"],
    "Al-Masri": ["Al-Masri", "Almasri", "El Masri"], "Haidar": ["Haidar", "Haider", "Hyder"], "Yilmaz": ["Yilmaz", "Yilmas"],
    "Karimi": ["Karimi", "Kareemi"], "Hosseini": ["Hosseini", "Husseini"], "Mohammadi": ["Mohammadi", "Muhammadi"],
    "Rezaei": ["Rezaei", "Rezaie"], "Jafari": ["Jafari", "Jaffari"], "Nouri": ["Nouri", "Noori"], "Soltani": ["Soltani", "Sultani"],
    "Reza": ["Reza"], "Mehdi": ["Mehdi", "Mahdi"], "Hamid": ["Hamid", "Hameed"], "Saeed": ["Saeed", "Said", "Saeid"],
    "Zahra": ["Zahra", "Zahraa"], "Nuwan": ["Nuwan"], "Chaminda": ["Chaminda"], "Kasun": ["Kasun"], "Dinesh": ["Dinesh"],
    "Dilani": ["Dilani"], "Kumari": ["Kumari"], "Nadeesha": ["Nadeesha", "Nadisha"], "Sanduni": ["Sanduni"],
    "Perera": ["Perera"], "Fernando": ["Fernando"], "Silva": ["Silva", "De Silva"], "Jayasinghe": ["Jayasinghe"],
    "Wickramasinghe": ["Wickramasinghe", "Wickremasinghe"], "Bandara": ["Bandara"], "Rajapaksa": ["Rajapaksa", "Rajapakse"],
}
TRANS = {
    "SA": {"m": ["Mohammed", "Imran", "Rahul", "Arjun", "Vikram", "Sanjay", "Rajesh", "Anil", "Suresh", "Rakib", "Shahid",
                 "Faisal", "Tariq", "Hassan"],
           "f": ["Fatima", "Aisha", "Priya", "Anjali", "Sunita", "Nasrin", "Rukhsana", "Farzana", "Sadia", "Yasmin"],
           "l": ["Rahman", "Hossain", "Chowdhury", "Islam", "Uddin", "Siddiqui", "Qureshi", "Khan", "Ali", "Begum", "Akhtar",
                 "Sharma", "Patel", "Singh", "Kumar", "Das", "Gupta", "Mukherjee", "Bhattacharya"]},
    "ME": {"m": ["Mohammed", "Ahmed", "Hussein", "Hassan", "Yusuf", "Ibrahim", "Mustafa", "Karim", "Omar", "Khalid", "Abdullah",
                 "Tariq", "Walid", "Samir", "Rashid", "Faisal"],
           "f": ["Fatima", "Aisha", "Zainab", "Mariam", "Nour", "Leila", "Yasmin", "Amina", "Samira", "Rania", "Hana", "Shirin",
                 "Nasrin"],
           "l": ["Haddad", "Mansour", "Nasser", "Saleh", "Abdallah", "Al-Masri", "Haidar", "Yilmaz", "Karimi", "Hosseini",
                 "Mohammadi", "Rezaei", "Jafari", "Nouri", "Soltani", "Ahmed" if False else "Hassan", "Ali", "Khan", "Hossain"]},
}
# each citizenship's own names: a person's forename and surname come from the country they hold citizenship of
_ARAB = {"m": ["Mohammed", "Ahmed", "Hussein", "Hassan", "Yusuf", "Ibrahim", "Mustafa", "Karim", "Omar", "Khalid", "Abdullah",
               "Tariq", "Walid", "Samir", "Rashid", "Faisal"],
         "f": ["Fatima", "Aisha", "Zainab", "Mariam", "Nour", "Leila", "Yasmin", "Amina", "Samira", "Rania", "Hana"],
         "l": ["Haddad", "Mansour", "Nasser", "Saleh", "Abdallah", "Al-Masri", "Haidar", "Hassan", "Ali", "Ibrahim", "Hussein"]}
TRANS_BY = {
    "IN": {"m": ["Rahul", "Arjun", "Vikram", "Sanjay", "Rajesh", "Anil", "Suresh", "Mohammed", "Imran"],
           "f": ["Priya", "Anjali", "Sunita", "Fatima", "Yasmin"],
           "l": ["Sharma", "Patel", "Singh", "Kumar", "Das", "Gupta", "Mukherjee", "Bhattacharya", "Khan", "Ali", "Siddiqui"]},
    "BD": {"m": ["Mohammed", "Rakib", "Shahid", "Imran", "Tariq", "Hassan", "Faisal"],
           "f": ["Fatima", "Nasrin", "Rukhsana", "Farzana", "Sadia", "Aisha", "Yasmin"],
           "l": ["Rahman", "Hossain", "Chowdhury", "Islam", "Uddin", "Begum", "Akhtar", "Ali", "Khan", "Das"]},
    "PK": {"m": ["Mohammed", "Imran", "Shahid", "Tariq", "Faisal", "Hassan", "Khalid", "Omar"],
           "f": ["Fatima", "Aisha", "Rukhsana", "Sadia", "Yasmin", "Farzana", "Samira"],
           "l": ["Khan", "Ali", "Qureshi", "Siddiqui", "Akhtar", "Chowdhury", "Hossain", "Rahman"]},
    "LK": {"m": ["Nuwan", "Chaminda", "Kasun", "Dinesh", "Suresh", "Anil"],
           "f": ["Dilani", "Kumari", "Nadeesha", "Sanduni", "Priya"],
           "l": ["Perera", "Fernando", "Silva", "Jayasinghe", "Wickramasinghe", "Bandara", "Rajapaksa"]},
    "IR": {"m": ["Mohammed", "Hussein", "Mustafa", "Karim", "Ibrahim", "Reza", "Mehdi", "Hamid", "Saeed"],
           "f": ["Mariam", "Shirin", "Nasrin", "Leila", "Zainab", "Fatima", "Zahra", "Yasmin"],
           "l": ["Karimi", "Hosseini", "Mohammadi", "Rezaei", "Jafari", "Nouri", "Soltani"]},
    "SY": _ARAB, "IQ": _ARAB, "EG": _ARAB, "SD": _ARAB, "JO": _ARAB,
}
COUNTRY_LOCALES = {"PL": ["pl_PL"], "LT": ["lt_LT"], "RO": ["ro_RO"], "LV": ["lv_LV"], "SK": ["sk_SK"],
                   "DE": ["de_DE"], "FR": ["fr_FR"], "IT": ["it_IT"], "ES": ["es_ES"], "NL": ["nl_NL"], "PT": ["pt_PT"],
                   "BE": ["nl_BE", "fr_BE"], "BR": ["pt_BR"], "CO": ["es_CO"], "MX": ["es_MX"], "AR": ["es_AR"]}
WESTERN_LOCALES = ["de_DE", "fr_FR", "it_IT", "es_ES", "nl_NL"]
EASTERN_LOCALES = ["pl_PL", "pl_PL", "lt_LT", "ro_RO", "lv_LV"]
LATIN_LOCALES = ["pt_BR", "pt_BR", "es_CO", "es_MX"]


def strip_accents(s):
    s = s.replace("ł", "l").replace("Ł", "L").replace("ß", "ss").replace("ø", "o").replace("Ø", "O")
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))


def _pool(locales, seed, n, kind):
    out, seen = [], set()
    for i, loc in enumerate(locales):
        fk = Faker(loc)
        fk.seed_instance(seed + 97 * i)
        for _ in range(n):
            v = getattr(fk, kind)()
            v = v.split()[0] if kind != "last_name" else v
            if v not in seen and v.replace("-", "").replace(" ", "").replace("'", "").isalpha():
                seen.add(v)
                out.append(v)
    return out


class Names:
    def __init__(self, seed):
        self.rng = np.random.default_rng(seed)
        self.nat_m = _pool(["en_IE", "en_IE", "en_GB"], seed, 400, "first_name_male")
        self.nat_f = _pool(["en_IE", "en_IE", "en_GB"], seed + 1, 400, "first_name_female")
        self.nat_l = _pool(["en_IE", "en_IE", "en_IE", "en_GB"], seed + 2, 900, "last_name")
        self.pools = {}
        for k, (cc, locs) in enumerate(sorted(COUNTRY_LOCALES.items())):
            sd = seed + 11 + 3 * k
            self.pools[cc] = (_pool(locs, sd, 300, "first_name_male"), _pool(locs, sd + 1, 300, "first_name_female"),
                              _pool(locs, sd + 2, 500, "last_name"))
        # names a reader of this pack would take for something other than a person's name are swapped in place,
        # so every other draw is unchanged
        swap = {"Claude": "Clement", "Claudie": "Clemence", "Whitney": "Winifred", "Handshake": "Hanshaw"}
        self.nat_m = [swap.get(x, x) for x in self.nat_m]
        self.nat_f = [swap.get(x, x) for x in self.nat_f]
        self.nat_l = [swap.get(x, x) for x in self.nat_l]
        for code in self.pools:
            self.pools[code] = tuple([swap.get(x, x) for x in pool] for pool in self.pools[code])
        # Faker weights its pools by frequency; a Zipf-like draw keeps common surnames common
        self._w = {}

    def _zipf(self, n, k):
        key = (n, k)
        if key not in self._w:
            w = 1.0 / np.arange(1, n + 1) ** k
            self._w[key] = w / w.sum()
        return self._w[key]

    def canonical(self, sex, origin, country=None):
        """One person's name, drawn from the names of the country they hold citizenship of: forename, surname, and the
        variants other systems use."""
        r = self.rng
        if origin == 0:
            fpool = self.nat_m if sex == 1 else self.nat_f
            f = fpool[r.choice(len(fpool), p=self._zipf(len(fpool), 0.9))]
            l = self.nat_l[r.choice(len(self.nat_l), p=self._zipf(len(self.nat_l), 0.35))]
            return {"f": f, "l": l, "fv": None, "lv": None}
        code = PR.ORIGINS[origin - 1][0]
        if code in ("SA", "ME"):
            t = TRANS_BY.get(country, TRANS[code])
            fp = t["m"] if sex == 1 else t["f"]
            fk = fp[r.choice(len(fp), p=self._zipf(len(fp), 0.6))]
            lk = t["l"][r.choice(len(t["l"]), p=self._zipf(len(t["l"]), 0.5))]
            return {"f": _G[fk][0], "l": _G[lk][0], "fv": _G[fk], "lv": _G[lk]}
        fm, ff, ll = self.pools[country]
        fp = fm if sex == 1 else ff
        f = fp[r.choice(len(fp), p=self._zipf(len(fp), 0.8))]
        l = ll[r.choice(len(ll), p=self._zipf(len(ll), 0.7))]
        if code == "LA" and r.random() < 0.6:
            l = l + " " + ll[r.integers(len(ll))]
        return {"f": f, "l": l, "fv": None, "lv": None}

    def render(self, nm, sex, origin, age, system):
        """The name as one system holds it."""
        r = self.rng
        f, l = nm["f"], nm["l"]
        code = PR.ORIGINS[origin - 1][0] if origin else "NAT"
        if nm["fv"] and r.random() < PR.TRANSLIT:
            f = nm["fv"][r.integers(len(nm["fv"]))]
        if nm["lv"] and r.random() < PR.TRANSLIT:
            l = nm["lv"][r.integers(len(nm["lv"]))]
        if code in ("EE", "WE", "LA") and system in ("register", "border") and r.random() < 0.7:
            f, l = strip_accents(f), strip_accents(l)
        if code == "LA" and " " in l and r.random() < 0.4:
            l = l.split(" ")[0] if r.random() < 0.6 else l.replace(" ", "-")
        if code == "NAT" and f in NICK and system == "survey" and r.random() < PR.NICKNAME * 2.5:
            f = NICK[f][r.integers(len(NICK[f]))]
        elif code == "NAT" and system == "survey" and strip_accents(f) in IRISH and r.random() < PR.IRISH_FORM:
            f = IRISH[strip_accents(f)]
        if code == "NAT" and system == "survey":
            u = r.random()
            if l in GAELIC and u < PR.GAELIC_FORM:
                l = GAELIC[l]
            elif u < PR.GAELIC_FORM + PR.PREFIX_DROP and (l.startswith("O'") or l.startswith("Mac") or l.startswith("Mc")):
                l = l[2:] if l.startswith("O'") else (l[3:] if l.startswith("Mac") else l[2:])
        if code in ("EE", "SA", "ME") and system in ("survey", "he") and r.random() < PR.USED_NAME:
            pool = USED_NAME["m" if sex == 1 else "f"]
            f = pool[r.integers(len(pool))]
        if r.random() < PR.TYPO:
            f = _typo(r, f)
        if r.random() < PR.TYPO:
            l = _typo(r, l)
        return f, l


def _typo(r, s):
    if len(s) < 4:
        return s
    i = int(r.integers(1, len(s) - 1))
    k = r.random()
    if k < 0.35:
        return s[:i] + s[i + 1:]                      # a letter dropped
    if k < 0.65:
        return s[:i] + s[i + 1] + s[i] + s[i + 2:]    # two letters swapped
    if k < 0.85:
        return s[:i] + s[i] + s[i:]                   # a letter doubled
    return s[:i] + "aeiou"[int(r.integers(5))] + s[i + 1:]   # a vowel misheard


def dob_variant(r, dob_day, origin, system):
    """The date of birth as one system holds it: (day, month, year)."""
    import datetime as dt
    d = PR.date_of(dob_day)
    day, month, year = d.day, d.month, d.year
    if origin and r.random() < PR.DOB_JAN1_NN and system in ("register", "border"):
        return 1, 1, year
    u = r.random()
    if u < PR.DOB_SWAP and day <= 12 and day != month:
        return month, day, year
    if u < PR.DOB_SWAP + PR.DOB_TYPO:
        k = r.random()
        if k < 0.4:
            day = max(1, min(28, day + int(r.choice([-1, 1, 10, -10]))))
        elif k < 0.7:
            year = year + int(r.choice([-1, 1]))
        else:
            month = max(1, min(12, month + int(r.choice([-1, 1]))))
    return day, month, year


def proxy_dob(r, day, month, year):
    """A date of birth given by another member of the household: the year, the day or the month misremembered."""
    k = r.random()
    if k < 0.45:
        return day, month, year + int(r.choice([-1, 1, -2]))
    if k < 0.75:
        return max(1, min(28, day + int(r.integers(-6, 7)) or 1)), month, year
    return day, max(1, min(12, month + int(r.choice([-1, 1, 2, -2])))), year
