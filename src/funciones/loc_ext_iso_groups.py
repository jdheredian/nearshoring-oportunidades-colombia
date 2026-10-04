"""
### Definición de los diccionarios de mapeo de países

Esta celda define dos diccionarios clave para la posterior integración de datos internacionales:

1. **`name_to_group`**  
   - Asocia el nombre de cada país al grupo económico o geopolítico correspondiente:
     - Unión Europea
     - Reino Unido
     - Estados Unidos
     - Canadá
     - APEC Asia
     - América Latina y el Caribe
     - Otros
   - Este diccionario permite homogeneizar los análisis regionales, agrupar mercados y segmentar oportunidades por bloque comercial.

2. **`name_to_iso3`**  
   - Convierte los nombres de países (según las convenciones utilizadas en los archivos de Naciones Unidas y bases de comercio internacional) a sus códigos ISO3.
   - Este mapeo es necesario para hacer los merges correctos con bases de comercio, aranceles, NTMs, logística, etc., ya que muchos de estos archivos usan códigos ISO3 en lugar de nombres de país.

Ambos diccionarios son esenciales para automatizar los procesos de limpieza, integración y agrupación de bases de datos internacionales a lo largo de los diferentes módulos de análisis.
"""

name_to_group = {
    # ——— Unión Europea ———
    "Austria": "Unión Europea", "Belgium": "Unión Europea", "Bulgaria": "Unión Europea", "Croatia": "Unión Europea",
    "Cyprus": "Unión Europea", "Czechia": "Unión Europea", "Denmark": "Unión Europea", "Estonia": "Unión Europea",
    "Finland": "Unión Europea", "France": "Unión Europea", "Germany": "Unión Europea", "Greece": "Unión Europea",
    "Hungary": "Unión Europea", "Ireland": "Unión Europea", "Italy": "Unión Europea", "Latvia": "Unión Europea",
    "Lithuania": "Unión Europea", "Luxembourg": "Unión Europea", "Malta": "Unión Europea",
    "Netherlands (Kingdom of the)": "Unión Europea", "Poland": "Unión Europea", "Portugal": "Unión Europea",
    "Romania": "Unión Europea", "Slovakia": "Unión Europea", "Slovenia": "Unión Europea",
    "Spain": "Unión Europea", "Sweden": "Unión Europea",

    # ——— Reino Unido, USA, Canadá ———
    "United Kingdom": "Reino Unido",
    "United States of America": "Estados Unidos",
    "Canada": "CAN",                                # (no figura en tu lista)

    # ——— APEC (solo los miembros “asiáticos”) ———
    "China": "APEC Asia", "China, Hong Kong SAR": "APEC Asia",
    "Indonesia": "APEC Asia", "Japan": "APEC Asia",
    "Korea, Republic of": "APEC Asia", "Malaysia": "APEC Asia",
    "Philippines": "APEC Asia", "Singapore": "APEC Asia",
    "Thailand": "APEC Asia", "Viet Nam": "APEC Asia",
    "Russian Federation": "APEC Asia",

    # ——— América Latina y el Caribe ———
    "Antigua and Barbuda": "América Latina y el Caribe", "Argentina": "América Latina y el Caribe", "Bahamas": "América Latina y el Caribe",
    "Barbados": "América Latina y el Caribe", "Belize": "América Latina y el Caribe", "Bolivia (Plurinational State of)": "América Latina y el Caribe",
    "Brazil": "América Latina y el Caribe", "Cayman Islands": "América Latina y el Caribe", "Chile": "América Latina y el Caribe",
    "Colombia": "América Latina y el Caribe", "Costa Rica": "América Latina y el Caribe", "Cuba": "América Latina y el Caribe",
    "Dominican Republic": "América Latina y el Caribe", "Ecuador": "América Latina y el Caribe", "El Salvador": "América Latina y el Caribe",
    "Grenada": "América Latina y el Caribe", "Guatemala": "América Latina y el Caribe", "Guyana": "América Latina y el Caribe",
    "Haiti": "América Latina y el Caribe", "Honduras": "América Latina y el Caribe", "Jamaica": "América Latina y el Caribe",
    "Mexico": "América Latina y el Caribe", "Nicaragua": "América Latina y el Caribe", "Panama": "América Latina y el Caribe",
    "Paraguay": "América Latina y el Caribe", "Peru": "América Latina y el Caribe", "Saint Kitts and Nevis": "América Latina y el Caribe",
    "Saint Lucia": "América Latina y el Caribe", "Saint Vincent and the Grenadines": "América Latina y el Caribe",
    "Suriname": "América Latina y el Caribe", "Trinidad and Tobago": "América Latina y el Caribe", "Uruguay": "América Latina y el Caribe",
    "Venezuela": "América Latina y el Caribe", "Aruba": "América Latina y el Caribe", "Bermuda": "América Latina y el Caribe",
    "Montserrat": "América Latina y el Caribe",

    # ─ América Latina y el Caribe ─
    "Anguilla": "América Latina y el Caribe",
    "Bonaire, Sint Eustatius and Saba": "América Latina y el Caribe",
    "British Virgin Islands": "América Latina y el Caribe",
    "Curaçao": "América Latina y el Caribe",
    "Dominica": "América Latina y el Caribe",
    "Haiti": "América Latina y el Caribe",
    "Saint Barthélemy": "América Latina y el Caribe",
    "Sint Maarten (Dutch part)": "América Latina y el Caribe",
    "Turks and Caicos Islands": "América Latina y el Caribe",
    "Venezuela (Bolivarian Rep. of)": "América Latina y el Caribe",

    # ─ APEC (asiáticos) ─
    "China, Taiwan Province of": "APEC Asia",

    # ─ Otros ─
    "Afghanistan": "Otro",
    "American Samoa": "Otro",
    "Central African Republic": "Otro",
    "Christmas Island": "Otro",
    "Cook Islands": "Otro",
    "Falkland Islands (Malvinas)": "Otro",
    "Faroe Islands": "Otro",
    "Gibraltar": "Otro",
    "Guam": "Otro",
    "Guinea-Bissau": "Otro",
    "Korea, Dem. People's Rep. of": "Otro",
    "Marshall Islands": "Otro",
    "Micronesia (Federated States of)": "Otro",
    "Nauru": "Otro",
    "New Caledonia": "Otro",
    "Niue": "Otro",
    "Norfolk Island": "Otro",
    "Northern Mariana Islands": "Otro",
    "Papua New Guinea": "Otro",
    "Saint Helena": "Otro",
    "Saint Pierre and Miquelon": "Otro",
    "San Marino": "Otro",
    "Solomon Islands": "Otro",
    "South Sudan": "Otro",
    "Tokelau": "Otro",
    "Tonga": "Otro",
    "Tuvalu": "Otro",
    "Vanuatu": "Otro",
    "Western Sahara": "Otro"
}

name_to_iso3 = {
    "Albania": "ALB", "Algeria": "DZA", "Andorra": "AND", "Angola": "AGO",
    "Antigua and Barbuda": "ATG", "Argentina": "ARG", "Armenia": "ARM",
    "Aruba": "ABW", "Australia": "AUS", "Austria": "AUT", "Azerbaijan": "AZE",
    "Bahamas": "BHS", "Bahrain": "BHR", "Bangladesh": "BGD", "Barbados": "BRB",
    "Belarus": "BLR", "Belgium": "BEL", "Belize": "BLZ", "Benin": "BEN",
    "Bermuda": "BMU", "Bhutan": "BTN", "Bolivia (Plurinational State of)": "BOL",
    "Bosnia and Herzegovina": "BIH", "Botswana": "BWA", "Brazil": "BRA",
    "Brunei Darussalam": "BRN", "Bulgaria": "BGR", "Burkina Faso": "BFA",
    "Burundi": "BDI", "Cabo Verde": "CPV", "Cambodia": "KHM",
    "Cameroon": "CMR", "Canada": "CAN", "Cayman Islands": "CYM", "Chad": "TCD",
    "Chile": "CHL", "China": "CHN", "China, Hong Kong SAR": "HKG",
    "China, Macao SAR": "MAC", "Colombia": "COL", "Comoros": "COM",
    "Congo, Dem. Rep. of the": "COD", "Costa Rica": "CRI",
    "Côte d'Ivoire": "CIV", "Croatia": "HRV", "Cuba": "CUB", "Cyprus": "CYP",
    "Czechia": "CZE", "Denmark": "DNK", "Djibouti": "DJI",
    "Dominican Republic": "DOM", "Ecuador": "ECU", "Egypt": "EGY",
    "El Salvador": "SLV", "Equatorial Guinea": "GNQ", "Eritrea": "ERI",
    "Estonia": "EST", "Eswatini": "SWZ", "Ethiopia": "ETH", "Fiji": "FJI",
    "Finland": "FIN", "France": "FRA", "French Polynesia": "PYF", "Gabon": "GAB",
    "Gambia": "GMB", "Georgia": "GEO", "Germany": "DEU", "Ghana": "GHA",
    "Greece": "GRC", "Greenland": "GRL", "Grenada": "GRD", "Guatemala": "GTM",
    "Guinea": "GIN", "Guyana": "GUY", "Honduras": "HND", "Hungary": "HUN",
    "Iceland": "ISL", "India": "IND", "Indonesia": "IDN",
    "Iran (Islamic Republic of)": "IRN", "Iraq": "IRQ", "Ireland": "IRL",
    "Israel": "ISR", "Italy": "ITA", "Jamaica": "JAM", "Japan": "JPN",
    "Jordan": "JOR", "Kazakhstan": "KAZ", "Kenya": "KEN", "Kiribati": "KIR",
    "Korea, Republic of": "KOR", "Kuwait": "KWT", "Kyrgyzstan": "KGZ",
    "Lao People's Dem. Rep.": "LAO", "Latvia": "LVA", "Lebanon": "LBN",
    "Lesotho": "LSO", "Liberia": "LBR", "Libya": "LBY", "Lithuania": "LTU",
    "Luxembourg": "LUX", "Madagascar": "MDG", "Malawi": "MWI",
    "Malaysia": "MYS", "Maldives": "MDV", "Mali": "MLI", "Malta": "MLT",
    "Mauritania": "MRT", "Mauritius": "MUS", "Mexico": "MEX",
    "Moldova, Republic of": "MDA", "Mongolia": "MNG", "Montenegro": "MNE",
    "Morocco": "MAR", "Mozambique": "MOZ", "Myanmar": "MMR", "Namibia": "NAM",
    "Nepal": "NPL", "Netherlands (Kingdom of the)": "NLD", "New Zealand": "NZL",
    "Nicaragua": "NIC", "Niger": "NER", "Nigeria": "NGA",
    "North Macedonia": "MKD", "Norway": "NOR", "Oman": "OMN", "Pakistan": "PAK",
    "Palau": "PLW", "Panama": "PAN", "Paraguay": "PRY", "Peru": "PER",
    "Philippines": "PHL", "Poland": "POL", "Portugal": "PRT", "Qatar": "QAT",
    "Romania": "ROU", "Russian Federation": "RUS", "Rwanda": "RWA",
    "Saint Kitts and Nevis": "KNA", "Saint Lucia": "LCA",
    "Saint Vincent and the Grenadines": "VCT", "Samoa": "WSM",
    "Sao Tome and Principe": "STP", "Saudi Arabia": "SAU", "Senegal": "SEN",
    "Serbia": "SRB", "Seychelles": "SYC", "Sierra Leone": "SLE",
    "Singapore": "SGP", "Slovakia": "SVK", "Slovenia": "SVN", "Somalia": "SOM",
    "South Africa": "ZAF", "Spain": "ESP", "Sri Lanka": "LKA",
    "State of Palestine": "PSE", "Sudan": "SDN", "Suriname": "SUR",
    "Sweden": "SWE", "Switzerland, Liechtenstein": "CHE", "Syrian Arab Republic": "SYR",
    "Tajikistan": "TJK", "Tanzania, United Republic of": "TZA",
    "Thailand": "THA", "Timor-Leste": "TLS", "Togo": "TGO",
    "Trinidad and Tobago": "TTO", "Tunisia": "TUN", "Türkiye": "TUR",
    "Turkmenistan": "TKM", "Uganda": "UGA", "Ukraine": "UKR",
    "United Arab Emirates": "ARE", "United Kingdom": "GBR",
    "United States of America": "USA", "Uruguay": "URY", "Uzbekistan": "UZB",
    "Viet Nam": "VNM", "Yemen": "YEM", "Zambia": "ZMB", "Zimbabwe": "ZWE",
    "World": "WLD",
    "Afghanistan": "AFG",
    "American Samoa": "ASM",
    "Anguilla": "AIA",
    "Bonaire, Sint Eustatius and Saba": "BES",
    "British Virgin Islands": "VGB",
    "Central African Republic": "CAF",
    "China, Taiwan Province of": "TWN",
    "Christmas Island": "CXR",
    "Cook Islands": "COK",
    "Curaçao": "CUW",
    "Dominica": "DMA",
    "Falkland Islands (Malvinas)": "FLK",
    "Faroe Islands": "FRO",
    "Gibraltar": "GIB",
    "Guam": "GUM",
    "Guinea-Bissau": "GNB",
    "Haiti": "HTI",
    "Korea, Dem. People's Rep. of": "PRK",
    "Marshall Islands": "MHL",
    "Micronesia (Federated States of)": "FSM",
    "Nauru": "NRU",
    "New Caledonia": "NCL",
    "Niue": "NIU",
    "Norfolk Island": "NFK",
    "Northern Mariana Islands": "MNP",
    "Papua New Guinea": "PNG",
    "Saint Barthélemy": "BLM",
    "Saint Helena": "SHN",
    "Saint Pierre and Miquelon": "SPM",
    "San Marino": "SMR",
    "Sint Maarten (Dutch part)": "SXM",
    "Solomon Islands": "SLB",
    "South Sudan": "SSD",
    "Tokelau": "TKL",
    "Tonga": "TON",
    "Turks and Caicos Islands": "TCA",
    "Tuvalu": "TUV",
    "Vanuatu": "VUT",
    "Venezuela (Bolivarian Rep. of)": "VEN",
    "Western Sahara": "ESH"
}
