"""task16 world constants: Port Calder, Texas, and the two hospital groups that merged into Calder Rosario Health in
2025. Every number the simulation draws from is here; world.py turns them into the clean truth: the people of the two
patient indexes, their families, homes and identifiers, what registrars typed at each registration, what Calder Bay's
2019 registration rule merged, and the clinical events each record carries."""
import datetime as dt

SEED = 16031
EXTRACT = dt.date(2026, 11, 2)                 # every extract cut on this Monday
AS_OF = dt.date(2026, 11, 4)
MERGER = dt.date(2025, 7, 1)
CONVERSION = dt.date(2027, 4, 5)
A_AUTOMERGE_FROM = dt.datetime(2019, 3, 4, 6, 0)   # Calder Bay registration merges on last name, birth date, sex
B_SUBSCRIBER_SSN_UNTIL = dt.date(2021, 6, 14)      # Rosario's screen took the SSN off the insurance card until then
FIRST_REG = dt.date(2006, 1, 1)                     # both indexes were rebuilt in 2006 (earlier charts not loaded)
PILOT = (dt.date(2026, 5, 4), dt.date(2026, 6, 26))

# the policy and the candidate rules
CAP_PER = 2000                                   # one false merge per 2,000 automatic links
RULES = ["A", "B", "C", "D"]

# people of Port Calder who ever registered with either group since 2006
N_FAMILIES = 68000
GROUPS = ["H", "W", "B", "V", "O"]               # Hispanic, white, Black, Vietnamese, other
GROUP_P = [0.585, 0.265, 0.07, 0.05, 0.03]
NORTH_P = {"H": 0.48, "W": 0.62, "B": 0.55, "V": 0.40, "O": 0.60}   # north of the ship channel (Calder Bay's side)
USE_A = {"north": 0.86, "south": 0.36}
USE_B = {"north": 0.34, "south": 0.87}

# foreign-born shares by group and birth year band, and birth dates recorded from foreign documents
FOREIGN = {"H": [(1900, 1969, 0.42), (1970, 1989, 0.30), (1990, 2030, 0.08)],
           "V": [(1900, 1974, 0.88), (1975, 1989, 0.52), (1990, 2030, 0.08)],
           "W": [(1900, 2030, 0.03)], "B": [(1900, 2030, 0.04)], "O": [(1900, 2030, 0.35)]}
JAN1_FOREIGN = {"H": 0.10, "V": 0.31, "W": 0.02, "B": 0.03, "O": 0.06}
JUL1_FOREIGN = {"H": 0.012, "V": 0.03, "W": 0.0, "B": 0.0, "O": 0.01}

TWIN_RATE = 0.0165                               # twin deliveries per delivery
TWIN_SAME_SEX = 0.66
TWIN_MZ_GIVEN_SAME_SEX = 0.45
TWIN_SIMILAR_NAMES = 0.28
TWIN_SAME_NAME = 0.002

# blood groups by community (ABO and Rh)
ABO_RH = {"H": {"O+": 0.555, "A+": 0.305, "B+": 0.075, "AB+": 0.02, "O-": 0.02, "A-": 0.018, "B-": 0.005, "AB-": 0.002},
          "W": {"O+": 0.37, "A+": 0.33, "B+": 0.09, "AB+": 0.03, "O-": 0.08, "A-": 0.07, "B-": 0.02, "AB-": 0.01},
          "B": {"O+": 0.47, "A+": 0.24, "B+": 0.18, "AB+": 0.04, "O-": 0.04, "A-": 0.02, "B-": 0.01, "AB-": 0.0},
          "V": {"O+": 0.39, "A+": 0.27, "B+": 0.25, "AB+": 0.07, "O-": 0.01, "A-": 0.005, "B-": 0.004, "AB-": 0.001},
          "O": {"O+": 0.40, "A+": 0.31, "B+": 0.12, "AB+": 0.04, "O-": 0.06, "A-": 0.05, "B-": 0.015, "AB-": 0.005}}
WBIT = 1 / 2600                                  # wrong blood in tube, per specimen

# registration: what a registrar types
P_NICKNAME = 0.055
P_TYPO_FIRST = 0.011
P_TYPO_LAST = 0.009
P_DOB_SWAP = 0.0035
P_DOB_YEAR = 0.0016
P_DOB_DAY = 0.0016
P_SEX_ERR = 0.0009
P_VIET_ORDER_SWAP = 0.13
COMPOUND_SURNAME = {"H": 0.36}                   # people carrying both parents' surnames
COMPOUND_FORMS = [("both", 0.44), ("hyphen", 0.15), ("paternal", 0.36), ("maternal", 0.05)]
TAKES_SPOUSE_NAME = {"H": 0.36, "W": 0.80, "B": 0.70, "V": 0.18, "O": 0.60}
P_SSN_ADULT = {"A": 0.86, "B": 0.88}
P_SUBSCRIBER_SSN_CHILD = 0.82                    # Rosario dependents before the 2021 change
P_SSN_TYPO = 0.004
P_SSN_PLACEHOLDER = {"A": 0.004, "B": 0.012}
DUP_BASE = {"A": 0.045, "B": 0.085}
DUP_COMPOUND = 0.11
DUP_VIET = 0.07
DUP_NICK = 0.03
P_MARRIED_NEW_RECORD = 0.42
P_ADDR_UPDATE = 0.72                             # a later visit updates the address after a move
P_PHONE_UPDATE = 0.66
P_UNIT_DROPPED = 0.35                            # an apartment's unit left off at registration
B_HIM_MERGE = 0.58                               # share of Rosario duplicates its HIM staff merged from the monthly report

# first names: name, peak birth year, spread in years, weight (fashion curves by community and sex)
# the share of each community's children given an uncommon first name (drawn from the Census 1990 frequencies)
FIRST_TAIL = {"H": 0.12, "W": 0.22, "B": 0.30, "V": 0.15, "O": 0.25}
FIRST_NAMES = {
("H", "F"): """Maria 1950 22 10;Guadalupe 1955 18 3;Juana 1945 15 1.6;Rosa 1950 16 2.2;Martha 1955 12 1.8;Gloria 1953 11 1.6;
Yolanda 1958 10 1.7;Elizabeth 1970 25 2.2;Irma 1955 11 1.3;Alicia 1960 14 1.3;Teresa 1958 13 1.4;Dolores 1945 12 0.9;
Josefina 1945 13 0.9;Carmen 1950 16 1.3;Raquel 1965 13 0.9;Sylvia 1958 11 1.1;Norma 1957 10 1.2;Olga 1955 12 0.7;
Leticia 1965 11 1.2;Rebecca 1972 12 0.9;Diana 1975 12 1.2;Sandra 1968 10 1.4;Patricia 1962 12 1.6;Veronica 1977 9 1.9;
Monica 1977 9 1.5;Laura 1975 13 1.1;Adriana 1982 9 1.3;Claudia 1978 10 1.2;Cynthia 1975 9 1.4;Erika 1983 8 1.1;
Vanessa 1988 8 1.5;Jessica 1987 7 2.2;Jennifer 1980 8 1.8;Melissa 1983 8 1.2;Stephanie 1988 7 1.4;Priscilla 1986 8 0.9;
Brenda 1979 9 1.0;Elena 1965 20 0.7;Isabel 1965 25 0.6;Lucia 1990 25 0.5;Ana 1975 25 1.6;Alejandra 1988 9 1.0;
Gabriela 1990 10 1.0;Daniela 1997 8 1.0;Andrea 1993 9 1.1;Mariana 2000 8 0.8;Karina 1988 8 0.8;Esmeralda 1990 10 0.8;
Mayra 1988 8 0.8;Araceli 1985 10 0.6;Maribel 1980 10 0.6;Natalie 2000 8 1.0;Jasmine 1997 7 1.0;Destiny 2000 6 0.8;
Ashley 1993 7 1.3;Samantha 1998 7 0.9;Alyssa 1999 7 0.9;Isabella 2011 6 1.9;Sofia 2012 7 1.5;Camila 2014 6 1.6;
Valeria 2011 6 1.1;Ximena 2013 6 1.0;Mia 2015 6 1.1;Valentina 2016 5 0.9;Emily 2006 7 1.2;Victoria 2005 9 0.9;
Genesis 2008 6 0.8;Aaliyah 2010 6 0.8;Abigail 2011 7 0.8;Allison 2007 7 0.8;Evelyn 2017 6 0.8;Luciana 2018 5 0.6;
Regina 2015 7 0.5;Graciela 1950 13 0.8;Consuelo 1945 12 0.6;Esperanza 1950 14 0.6;Margarita 1950 15 0.7;Angelica 1980 10 0.8""",
("H", "M"): """Jose 1952 22 9;Juan 1952 20 5;Jesus 1955 20 3;Manuel 1955 18 2;Francisco 1955 18 2.2;Pedro 1950 16 1.5;
Antonio 1955 20 2;Luis 1965 22 3;Carlos 1968 20 2.6;Ramon 1950 14 1.2;Ruben 1958 13 1.3;Raul 1958 13 1.3;Ricardo 1965 15 1.4;
Roberto 1960 15 1.6;Arturo 1958 13 1.1;Mario 1958 14 1.2;Hector 1960 13 1.1;Armando 1955 13 1.0;Alfredo 1955 14 1.0;
Rogelio 1955 12 0.8;Gilberto 1955 12 0.7;Rodolfo 1950 12 0.7;Enrique 1958 14 0.9;Fernando 1970 14 1.1;Javier 1975 12 1.5;
Eduardo 1972 13 1.2;Jorge 1968 14 1.4;Sergio 1972 11 1.1;Oscar 1975 12 1.0;Victor 1970 15 1.0;Gerardo 1975 11 0.9;
Alejandro 1983 10 1.3;Daniel 1985 15 2.0;David 1975 18 2.2;Michael 1978 12 1.6;Joseph 1980 15 1.0;Richard 1968 12 1.1;
Frank 1955 14 0.9;Christopher 1987 8 1.6;Jonathan 1988 8 1.5;Joshua 1990 8 1.3;Anthony 1990 12 1.4;Adrian 1992 10 1.0;
Andres 1992 12 0.7;Ivan 1990 10 0.8;Isaac 2002 9 1.0;Angel 1995 12 1.3;Diego 2000 9 1.0;Gabriel 2000 11 1.1;Julian 2005 9 0.9;
Sebastian 2010 7 1.3;Santiago 2014 6 1.4;Mateo 2016 5 1.5;Matthew 2000 9 1.0;Jayden 2010 5 1.0;Liam 2018 5 0.9;
Leonardo 2015 7 0.9;Emiliano 2015 6 0.9;Gael 2015 6 0.8;Elias 2014 8 0.7;Josue 2005 8 0.6;Aaron 1998 10 0.8;
Ezequiel 2008 9 0.4;Alexander 2008 9 1.0;Benjamin 2012 8 0.8;Kevin 1993 7 1.0;Brian 1990 7 0.9;Steven 1985 9 0.9;
Eric 1985 9 0.8;Ignacio 1950 14 0.6;Rafael 1965 16 0.9;Guillermo 1958 14 0.7;Alberto 1960 15 0.9;Ernesto 1958 14 0.6""",
("W", "F"): """Mary 1945 18 6;Patricia 1950 12 3;Linda 1950 9 3.5;Barbara 1945 12 2.6;Margaret 1940 16 1.8;Dorothy 1935 13 1.6;
Betty 1938 11 1.8;Shirley 1940 10 1.4;Judith 1948 9 1.4;Carol 1950 10 2;Sharon 1952 9 1.8;Susan 1957 10 2.6;Deborah 1957 8 2.2;
Donna 1958 9 1.6;Nancy 1950 12 1.8;Karen 1962 9 2.4;Kimberly 1972 8 2.4;Lisa 1966 7 2.6;Michelle 1972 9 2.0;Amy 1976 8 1.9;
Angela 1974 9 1.8;Melissa 1979 8 2.0;Jennifer 1977 8 3.5;Stephanie 1985 9 1.8;Heather 1978 7 1.6;Amanda 1986 7 2.2;
Sarah 1988 13 2.0;Jessica 1987 7 2.6;Ashley 1990 6 2.4;Brittany 1990 5 1.6;Emily 2000 10 1.8;Hannah 2001 7 1.4;
Madison 2003 6 1.4;Taylor 1995 6 1.0;Lauren 1993 8 1.2;Megan 1990 7 1.2;Rachel 1985 10 1.2;Katherine 1985 20 1.0;
Elizabeth 1975 25 1.8;Emma 2012 7 1.8;Olivia 2014 7 1.8;Ava 2013 6 1.4;Sophia 2012 6 1.2;Isabella 2010 6 1.2;Harper 2017 5 1.0;
Abigail 2009 7 1.2;Avery 2015 7 0.9;Ella 2015 7 0.9;Chloe 2012 7 0.9;Addison 2010 6 0.8;Brooklyn 2013 6 0.8;Kaylee 2009 6 0.7;
Kayla 1995 7 0.9;Haley 1998 7 0.8;Lily 2014 8 0.9;Grace 2008 10 0.8;Natalie 2005 8 0.8;Zoey 2012 6 0.6;Paisley 2016 4 0.6;
Ruth 1935 15 0.9;Helen 1935 15 1.0;Joyce 1945 11 1.0;Debra 1958 7 1.2;Pamela 1958 8 1.4;Cynthia 1962 9 1.1;Tammy 1968 6 1.1;
Christy 1975 7 0.8;Crystal 1983 7 0.9;Tiffany 1986 6 1.0;Kristen 1983 7 0.8;Lindsey 1987 6 0.8;Courtney 1988 7 0.8;
Morgan 1996 7 0.8;Kaitlyn 1996 6 0.8;Rebecca 1975 13 1.0;Christina 1980 9 1.1;Laura 1970 12 1.0;Julie 1968 8 1.0""",
("W", "M"): """James 1955 22 5;John 1950 20 5;Robert 1950 18 5;William 1950 22 3.6;Charles 1945 18 2.4;Richard 1950 14 3;
Thomas 1955 16 2.6;Donald 1945 12 2;Ronald 1948 11 1.8;Larry 1950 10 1.6;Gary 1953 9 1.8;Kenneth 1955 12 1.8;Steven 1960 10 2.2;
Mark 1962 9 2.2;Michael 1970 14 4.5;David 1962 15 3.6;Jeffrey 1965 9 1.8;Timothy 1965 10 1.6;Scott 1968 8 1.4;Brian 1972 9 1.8;
Kevin 1972 9 1.4;Jason 1977 7 2.4;Christopher 1982 9 3.0;Matthew 1985 9 2.4;Joshua 1987 8 2.2;Justin 1988 7 1.6;
Brandon 1990 7 1.6;Tyler 1993 6 1.4;Austin 1995 7 1.3;Andrew 1990 12 1.6;Daniel 1985 14 1.8;Ryan 1988 9 1.4;Jacob 1999 9 2.0;
Ethan 2003 8 1.6;Logan 2005 7 1.3;Noah 2010 8 1.6;Liam 2015 6 1.8;Mason 2010 6 1.4;Jackson 2012 7 1.3;Aiden 2009 6 1.2;
Caleb 2005 8 1.0;Wyatt 2014 7 1.0;Hunter 2002 7 0.9;Cody 1993 6 0.9;Travis 1983 8 1.0;Dustin 1985 7 0.9;Kyle 1990 7 1.1;
Benjamin 2005 12 1.1;Samuel 2005 14 0.9;Henry 2016 8 0.9;Oliver 2017 6 1.0;Elijah 2013 7 1.0;Lucas 2014 7 1.0;Grayson 2017 5 0.7;
Carter 2014 6 0.7;George 1940 16 1.2;Harold 1935 12 1.0;Walter 1935 14 0.9;Jerry 1950 11 1.1;Dennis 1952 9 1.1;Terry 1955 9 1.0;
Randy 1960 7 0.9;Todd 1967 7 0.8;Troy 1970 7 0.8;Shane 1978 8 0.8;Chad 1978 6 0.8;Eric 1975 9 1.2;Adam 1985 9 1.0;
Nathan 1990 11 1.0;Zachary 1993 7 1.0;Jordan 1995 8 0.9;Dylan 2000 8 0.9;Connor 2002 7 0.8;Hayden 2005 7 0.6;Joseph 1975 20 1.6""",
("B", "F"): """Mary 1945 18 3;Annie 1940 15 1.2;Willie 1940 14 0.8;Dorothy 1940 14 1.3;Shirley 1945 12 1.2;Gloria 1952 12 1.2;
Brenda 1960 9 1.6;Linda 1952 10 1.4;Patricia 1955 13 1.6;Barbara 1950 13 1.3;Gwendolyn 1955 11 0.8;Sandra 1962 10 1.3;
Tonya 1972 6 1.2;Felicia 1972 7 1.1;Tracy 1970 7 1.0;Angela 1972 9 1.6;Kimberly 1975 9 1.6;Latoya 1981 5 1.2;Lakisha 1978 5 0.9;
Tamika 1978 6 0.9;Keisha 1980 6 0.9;Shanice 1990 5 0.8;Ebony 1983 7 1.0;Jasmine 1993 7 1.3;Brittany 1990 6 1.3;Ashley 1990 6 1.3;
Tiara 1993 6 0.8;Destiny 1998 6 1.0;Diamond 1995 6 0.8;Imani 2000 8 0.9;Aaliyah 2003 7 1.1;Kayla 1997 7 1.0;Jada 2002 6 0.9;
Nevaeh 2009 5 0.8;Makayla 2004 6 0.8;Madison 2005 6 0.8;Zoe 2010 8 0.7;Amari 2012 6 0.6;Londyn 2015 5 0.6;Ava 2014 6 0.8;
Paris 2006 6 0.4;Alexis 1997 6 0.8;Taylor 1996 6 0.7;Mya 2008 6 0.6;Denise 1965 9 1.0;Monique 1978 8 0.9;Crystal 1983 7 0.8""",
("B", "M"): """James 1950 22 3;John 1948 18 2.5;Willie 1945 15 2;Robert 1952 18 2.6;Charles 1950 17 1.6;Johnny 1952 12 1.0;
Larry 1958 11 1.2;Michael 1972 13 3.0;Anthony 1975 14 2.0;Kevin 1977 10 1.6;Derrick 1978 7 1.2;Marcus 1983 8 1.3;
Antonio 1983 9 1.1;Terrell 1983 7 0.9;Deandre 1988 6 0.8;Jamal 1985 7 1.0;Darnell 1978 8 0.8;Tyrone 1972 7 0.8;
Reginald 1965 9 0.9;Christopher 1985 9 1.8;Brandon 1991 7 1.3;Justin 1992 7 1.1;Jordan 1997 8 1.1;Jalen 1999 5 0.9;
Isaiah 2004 7 1.1;Elijah 2008 8 1.2;Jayden 2010 5 1.3;Josiah 2010 6 0.9;Jeremiah 2006 7 0.9;Kingston 2016 5 0.7;
Camden 2014 5 0.6;Malik 1995 8 0.8;Darius 1993 8 0.8;Cameron 1997 8 0.8;Joshua 1990 8 1.0;Aaron 1993 9 0.8;Kendrick 1995 7 0.6;
Xavier 2000 9 0.8;Carter 2015 6 0.6;Aiden 2011 6 0.7;Cedric 1975 9 0.7;Curtis 1965 10 0.8;Eddie 1958 11 0.8""",
("V", "F"): """Lan 1955 15 2.2;Mai 1960 16 2.4;Hoa 1955 15 2.0;Huong 1960 14 2.0;Hanh 1958 14 1.6;Thu 1960 15 2.0;Thuy 1960 14 2.2;
Hang 1965 14 1.6;Linh 1975 18 2.4;Ngoc 1965 18 2.0;Phuong 1965 16 1.8;Trang 1975 14 1.8;Thao 1972 15 1.6;Hien 1960 14 1.3;
Loan 1958 13 1.3;Nga 1960 13 1.2;Dung 1958 14 1.2;Tuyet 1955 13 1.0;Kim 1960 16 1.6;Anh 1985 18 1.6;Vy 1995 10 1.4;
Nhi 1995 10 1.0;Tiffany 1988 7 1.2;Vivian 1990 9 1.0;Jennifer 1985 8 1.2;Kimberly 1988 8 1.0;Amy 1985 9 1.0;Christine 1987 9 0.8;
Jessica 1992 7 0.9;Michelle 1988 8 0.8;Emily 2006 7 1.0;Sophia 2012 6 1.0;Emma 2013 6 0.9;Olivia 2015 6 0.9;Chloe 2011 6 0.9;
Hannah 2005 7 0.8;Kaylee 2010 6 0.7;Ivy 2012 7 0.6""",
("V", "M"): """Hung 1955 15 2.4;Thanh 1955 16 2.6;Minh 1965 18 2.4;Tuan 1968 14 2.2;Dung 1960 14 1.6;Hai 1960 15 1.8;Long 1965 15 1.6;
Nam 1968 15 1.6;Son 1962 14 1.4;Quang 1960 14 1.4;Duc 1960 14 1.6;Phong 1962 13 1.2;Hoang 1965 15 1.3;Binh 1958 13 1.2;
Cuong 1965 13 1.1;Khanh 1970 15 1.1;Vinh 1965 14 1.1;Tam 1960 14 1.0;Thang 1962 13 1.0;Tri 1970 14 0.9;Huy 1985 14 1.3;
Khoa 1990 12 1.0;Bao 1995 12 1.0;Kevin 1988 8 1.4;David 1985 10 1.2;Michael 1987 9 1.0;Peter 1980 12 0.8;Andrew 1993 8 0.9;
Jason 1985 7 0.8;Daniel 1992 9 0.9;Brian 1990 8 0.8;Ethan 2006 7 1.0;Ryan 2004 8 0.9;Nathan 2006 8 1.0;Lucas 2014 6 0.9;
Liam 2016 6 0.9;Jayden 2010 5 0.8;Aiden 2010 6 0.7""",
}
FIRST_NAMES[("O", "F")] = FIRST_NAMES[("W", "F")]
FIRST_NAMES[("O", "M")] = FIRST_NAMES[("W", "M")]

# Vietnamese surnames and their shares in the community (the Census counts give the rest)
VIET_SURNAMES = ["NGUYEN", "TRAN", "LE", "PHAM", "HUYNH", "HOANG", "PHAN", "VU", "VO", "DANG", "BUI", "DO", "HO", "NGO",
                 "DUONG", "LY", "DINH", "TRUONG", "LAM", "LUU", "MAI", "TRINH", "CAO", "TA", "DOAN", "LU", "HA", "DAO",
                 "TANG", "QUACH", "THAI", "LA", "TONG", "TON", "CHAU", "LAI", "TIEU", "LIEU", "VUONG", "KIEU"]
# South Texas surnames more common locally than in the national Hispanic distribution
SOUTH_TEXAS_BOOST = {"GARZA": 3.0, "TREVINO": 2.5, "CANTU": 2.5, "SALINAS": 2.2, "VILLARREAL": 2.2, "GUERRA": 2.0,
                     "PENA": 1.8, "SAENZ": 2.4, "HINOJOSA": 2.6, "LONGORIA": 2.5, "CAVAZOS": 2.5, "ALANIZ": 2.2,
                     "GONZALES": 1.8, "RAMIREZ": 1.4, "GARCIA": 1.5, "HERNANDEZ": 1.3, "MARTINEZ": 1.4, "GONZALEZ": 1.3,
                     "RODRIGUEZ": 1.3, "LOPEZ": 1.3, "PEREZ": 1.2, "SANCHEZ": 1.2, "FLORES": 1.3, "DELEON": 2.0,
                     "DELAGARZA": 3.0, "BARRERA": 2.0, "OLIVAREZ": 2.4, "YBARRA": 2.2, "ZAMORA": 1.6, "TIJERINA": 3.0}

STREETS = ["Ocean", "Bay", "Harbor", "Gulf", "Shoreline", "Mesquite", "Huisache", "Anaqua", "Retama", "Ebony",
           "Palo Verde", "Bluebonnet", "Primrose", "Magnolia", "Laurel", "Cedar", "Pecan", "Live Oak", "Willow", "Pelican",
           "Heron", "Egret", "Tern", "Sandpiper", "Mustang", "Seagull", "Dolphin", "Marlin", "Tarpon", "Redfish",
           "Lighthouse", "Anchor", "Compass", "Coral", "Sand Dollar", "Driftwood", "Saltgrass", "Dune", "Bayview",
           "Seaside", "Lagoon", "Inlet", "Channel", "Harbor View", "Calder", "Rosario", "Santa Elena", "San Jacinto",
           "Alamo", "Bowie", "Travis", "Crockett", "Lamar", "Fannin", "Main", "Church", "Market", "Mill", "Commerce",
           "Center", "Park", "Lake", "River", "Oak", "Elm", "Pine", "Cypress", "Sycamore", "Hackberry", "Agarita",
           "Yucca", "Sabal", "Jasmine", "Gardenia", "Hibiscus", "Oleander", "Plumeria", "Azalea", "Camellia", "Dogwood"]
SUFFIX = ["St", "Dr", "Ave", "Blvd", "Ln", "Rd", "Ct", "Cir", "Pkwy", "Way"]
