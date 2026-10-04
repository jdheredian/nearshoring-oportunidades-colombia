def iso3(name_or_iterable):
    """
    Devuelve el código ISO-3 para uno o varios países/territorios.

    Parameters
    ----------
    name_or_iterable : str | list | tuple | pandas.Series
        Nombre (o nombres) exactamente como en tu DataFrame.

    Returns
    -------
    str  | list[str]
        ISO-3 si la entrada es str, o lista de ISO-3 en el mismo orden.
    """

    # ── 1. Diccionario base (lo esencial que ya tenías) ──────────────────
    _map = {
        "Germany": "EUU", "Bolivia": "BOL", "Hong Kong, China": "HKG",
        "Suriname": "SUR", "Grenada": "GRD", "Denmark": "EUU",
        "Dominican Republic": "DOM", "St. Lucia": "LCA",
        "Trinidad and Tobago": "TTO", "Argentina": "ARG", "Brazil": "BRA",
        "Chile": "CHL", "Taiwan, China": "TWN", "Colombia": "COL",
        "Cuba": "CUB", "Dominica": "DMA", "Ecuador": "ECU",
        "Guyana": "GUY", "Mexico": "MEX", "Paraguay": "PRY",
        "Peru": "PER", "Singapore": "SGP", "Estonia": "EUU",
        "Uruguay": "URY", "Venezuela": "VEN", "Hungary": "EUU",
        "Austria": "EUU", "Belgium": "EUU", "Belize": "BLZ",
        "Bulgaria": "EUU", "Canada": "CAN", "China": "CHN",
        "Finland": "EUU", "Costa Rica": "CRI", "Greece": "EUU",
        "Croatia": "EUU", "Cyprus": "EUU", "Czech Republic": "EUU",
        "France": "EUU", "Guatemala": "GTM", "Honduras": "HND",
        "Indonesia": "IDN", "Ireland": "EUU", "Italy": "EUU",
        "Jamaica": "JAM", "Japan": "JPN", "Korea, Rep.": "KOR",
        "Latvia": "EUU", "Lithuania": "EUU", "Luxembourg": "EUU",
        "Malaysia": "MYS", "Malta": "EUU", "Netherlands": "EUU",
        "Nicaragua": "NIC", "Panama": "PAN", "Philippines": "PHL",
        "Poland": "EUU", "Portugal": "EUU", "Romania": "EUU",
        "St. Kitts and Nevis": "KNA", "St. Vincent and the Grenadines": "VCT",
        "Slovak Republic": "EUU", "Vietnam": "VNM", "Slovenia": "EUU",
        "Spain": "EUU", "Sweden": "EUU", "Thailand": "THA",
        "United Kingdom": "GBR", "United States": "USA",
    }

    # ── 2. Nuevas entradas (todo lo adicional que solicitaste) ───────────
    additions = {
        "South Africa": "ZAF", "Switzerland": "CHE", "Togo": "TGO",
        "United Arab Emirates": "ARE", "Turkey": "TUR", "Unspecified": "UNK",

        # A
        "Afghanistan": "AFG", "Albania": "ALB", "Algeria": "DZA",
        "Andorra": "AND", "Angola": "AGO", "Anguila": "AIA",
        "Antigua and Barbuda": "ATG", "Argentina": "ARG", "Armenia": "ARM",
        "Aruba": "ABW", "Australia": "AUS", "Austria": "EUU", "Azerbaijan": "AZE",

        # B
        "Bahamas, The": "BHS", "Bahrain": "BHR", "Bangladesh": "BGD",
        "Barbados": "BRB", "Belarus": "BLR", "Belgium": "EUU",
        "Benin": "BEN", "Bermuda": "BMU", "Bhutan": "BTN", "Bolivia": "BOL",
        "Bosnia and Herzegovina": "BIH", "Botswana": "BWA",
        "Brazil": "BRA", "Brunei": "BRN", "Bulgaria": "EUU", "Burkina Faso": "BFA",
        "Burundi": "BDI", "Bahrain": "BHR",

        # C
        "Cambodia": "KHM", "Cameroon": "CMR", "Canada": "CAN",
        "Cape Verde": "CPV", "Central African Republic": "CAF",
        "Chad": "TCD", "Chile": "CHL", "China": "CHN",
        "Cocos (Keeling) Islands": "CCK", "Colombia": "COL", "Comoros": "COM",
        "Congo, Dem. Rep.": "COD", "Congo, Rep.": "COG", "Cook Islands": "COK",
        "Costa Rica": "CRI", "Cote d'Ivoire": "CIV", "Croatia": "EUU",
        "Cuba": "CUB", "Curacao": "CUW", "Curaçao": "CUW", "Cyprus": "EUU",
        "Czech Republic": "EUU",

        # D
        "Denmark": "EUU", "Djibouti": "DJI", "Dominica": "DMA",
        "Dominican Republic": "DOM",

        # E
        "East Timor": "TLS", "Ecuador": "ECU", "Egypt, Arab Rep.": "EGY",
        "El Salvador": "SLV", "Equatorial Guinea": "GNQ", "Eritrea": "ERI",
        "Estonia": "EUU", "Eswatini": "SWZ", "Ethiopia(excludes Eritrea)": "ETH",

        # F
        "Faeroe Islands": "FRO", "Falkland Island": "FLK",
        "Fiji": "FJI", "Finland": "EUU", "France": "EUU",
        "French Polynesia": "PYF", "Fr. So. Ant. Tr": "ATF",

        # G
        "Gabon": "GAB", "Gambia, The": "GMB", "Georgia": "GEO",
        "Germany": "EUU", "Ghana": "GHA", "Gibraltar": "GIB",
        "Greece": "EUU", "Greenland": "GRL", "Grenada": "GRD",
        "Guadeloupe": "GLP", "Guam": "GUM", "Guatemala": "GTM",
        "Guinea": "GIN", "Guinea-Bissau": "GNB", "Guyana": "GUY",

        # H
        "Haiti": "HTI", "Heard Island and McDonald Isla": "HMD",
        "Honduras": "HND", "Hong Kong, China": "HKG",
        "Hungary": "EUU",

        # I
        "Iceland": "ISL", "India": "IND", "Indonesia": "IDN",
        "Iran, Islamic Rep.": "IRN", "Iraq": "IRQ", "Ireland": "EUU",
        "Israel": "ISR", "Italy": "EUU",

        # J
        "Jamaica": "JAM", "Japan": "JPN", "Jordan": "JOR",

        # K
        "Kazakhstan": "KAZ", "Kenya": "KEN", "Kiribati": "KIR",
        "Korea, Dem. Rep.": "PRK", "Korea, Rep.": "KOR",
        "Kosovo": "XKX", "Kuwait": "KWT", "Kyrgyz Republic": "KGZ",

        # L
        "Lao PDR": "LAO", "Latvia": "EUU", "Lebanon": "LBN",
        "Lesotho": "LSO", "Liberia": "LBR", "Libya": "LBY",
        "Liechtenstein": "LIE", "Lithuania": "EUU", "Luxembourg": "EUU",

        # M
        "Macao": "MAC", "Madagascar": "MDG", "Malawi": "MWI",
        "Malaysia": "MYS", "Maldives": "MDV", "Mali": "MLI",
        "Malta": "EUU", "Marshall Islands": "MHL",
        "Martinique": "MTQ", "Mauritania": "MRT", "Mauritius": "MUS",
        "Mayotte": "MYT", "Mexico": "MEX", "Micronesia, Fed. Sts.": "FSM",
        "Moldova": "MDA", "Monaco": "MCO", "Mongolia": "MNG",
        "Montenegro": "MNE", "Montserrat": "MSR", "Morocco": "MAR",
        "Mozambique": "MOZ", "Myanmar": "MMR",

        # N
        "Namibia": "NAM", "Nauru": "NRU", "Nepal": "NPL", "Netherlands": "EUU",
        "New Caledonia": "NCL", "New Zealand": "NZL", "Nicaragua": "NIC",
        "Niger": "NER", "Nigeria": "NGA", "Niue": "NIU", "Norfolk Island": "NFK",
        "North Macedonia": "MKD", "Northern Mariana Islands": "MNP",
        "Norway": "NOR",

        # O
        "Oman": "OMN", "Occ.Pal.Terr": "PSE",

        # P
        "Pakistan": "PAK", "Palau": "PLW", "Panama": "PAN",
        "Papua New Guinea": "PNG", "Paraguay": "PRY", "Peru": "PER",
        "Philippines": "PHL", "Pitcairn": "PCN", "Poland": "EUU",
        "Portugal": "EUU",

        # Q
        "Qatar": "QAT",

        # R
        "Romania": "EUU", "Russian Federation": "RUS", "Rwanda": "RWA",

        # S
        "Samoa": "WSM", "San Marino": "SMR", "Sao Tome and Principe": "STP",
        "Saudi Arabia": "SAU", "Senegal": "SEN", "Serbia, FR(Serbia/Montenegro)": "SRB",
        "Seychelles": "SYC", "Sierra Leone": "SLE", "Singapore": "SGP",
        "Sint Maarten (Dutch part)": "SXM", "Slovak Republic": "EUU",
        "Slovenia": "EUU", "Solomon Islands": "SLB", "Somalia": "SOM",
        "South Africa": "ZAF", "South Georgia and the South Sa": "SGS",
        "South Sudan": "SSD", "Spain": "EUU", "Sri Lanka": "LKA",
        "Sudan": "SDN", "Suriname": "SUR", "Swaziland": "SWZ",
        "Sweden": "EUU", "Switzerland": "CHE", "Syrian Arab Republic": "SYR",

        # T
        "Tajikistan": "TJK", "Tanzania": "TZA", "Thailand": "THA",
        "Timor-Leste": "TLS", "Togo": "TGO", "Tokelau": "TKL",
        "Tonga": "TON", "Trinidad and Tobago": "TTO", "Tunisia": "TUN",
        "Turkey": "TUR", "Turkmenistan": "TKM",
        "Turks and Caicos Isl.": "TCA", "Tuvalu": "TUV",

        # U
        "Uganda": "UGA", "Ukraine": "UKR",
        "United Arab Emirates": "ARE", "United Kingdom": "GBR",
        "United States": "USA",
        "United States Minor Outlying I": "UMI", "Unspecified": "UNK",
        "Uruguay": "URY", "Uzbekistan": "UZB",

        # V
        "Vanuatu": "VUT", "Venezuela": "VEN", "Vietnam": "VNM",

        # W
        "Wallis and Futura Isl.": "WLF", "Western Sahara": "ESH",

        # Y-Z
        "Yemen": "YEM", "Zambia": "ZMB", "Zimbabwe": "ZWE",
        "Bouvet Island": "BVT", "Free Zones": "UNK", "Special Categories": "UNK",
        "Bunkers": "UNK"
    }

    # Añadir todas las nuevas entradas al diccionario base
    _map.update(additions)

    # ── 3. Lógica de salida ──────────────────────────────────────────────
    if isinstance(name_or_iterable, str):
        return _map.get(name_or_iterable, "UNK")        # un solo país
    return [_map.get(n, "UNK") for n in name_or_iterable]  # lista/Series
