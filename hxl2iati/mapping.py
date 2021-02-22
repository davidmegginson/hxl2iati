DAC_SECTOR_INFO = {
    "72010": {
        "name_en": "Material relief assistance and services",
    },
    "72011": {
        "name_en": "Basic Health Care Services in Emergencies",
    },
    "72012": {
        "name_en": "Education in emergencies",
    },
    "72040": {
        "name_en": "Emergency food assistance",
    },
    "72050": {
        "name_en": "Relief co-ordination and support services",
    },
    "73010": {
        "name_en": "Immediate post-emergency reconstruction and rehabilitation",
    },
    "74020": {
        "name_en": "Multi-hazard response preparedness",
    },
}
""" Info for humanitarian DAC sector codes. Source: https://iatistandard.org/en/iati-standard/203/codelists/sector/ """


CLUSTER_INFO = {
    "CCCM": {
        "code": "CCM",
        "name_en": "Camp Coordination / Management",
        "name_fr": "Coordination et gestion des camps",
        "url": "http://www.globalcccmcluster.org",
        "dac_codes": ["72010"],
    },
    "Education": {
        "code": "EDU",
        "name_en": "Education",
        "name_fr": "Education",
        "url": "http://educationcluster.net/",
        "dac_codes": ["72012"],
    },
    "FSC": {
        "code": "FSC",
        "name_en": "Food Security",
        "name_fr": "Sécurité alimentaire",
        "url": "http://foodsecuritycluster.net/",
        "dac_codes": ["72040"],
    },
    "Health": {
        "code": "HEA",
        "name_en": "Health",
        "name_fr": "Santé",
        "url": "http://www.who.int/health-cluster/en/",
        "dac_codes": ["72011"],
    },
    "Nutrition": {
        "code": "NUT",
        "name_en": "Nutrition",
        "name_fr": "Nutrition",
        "url": "http://nutritioncluster.net/",
        "dac_codes": ["72040"],
    },
    "Protection": {
        "code": "PRO",
        "name_en": "Protection",
        "name_fr": "Protection",
        "url": "http://www.globalprotectioncluster.org/",
        "dac_codes": ["72010"],
    },
    "Shelter/ NFI": {
        "code": "SHL",
        "name_en": "Emergency Shelter and NFI",
        "name_fr": "Abris d'urgence et NFI",
        "url": "https://www.sheltercluster.org/",
        "dac_codes": ["72010"],
    },
    "WASH": {
        "code": "WSH",
        "name_en": "Water Sanitation Hygiene",
        "name_fr": "Eau, assainissement et hygiène",
        "url": "http://washcluster.net/",
        "dac_codes": ["72010"],
    },
}
""" Information about humanitarian clusters. Source: https://data.humdata.org/dataset/global-coordination-groups-beta """
