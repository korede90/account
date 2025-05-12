import re
import json

# Sample messages as a list of strings
sample_texts = [
    """Account holder
AGEH STEWART EMMANUEL
Bank name
UNION BANK OF NIGERIA PLC
Account number
0131952914""",

    """access bank
1234567890
olayemi""",

    """Account holder
AGEH STEWART EMMANUEL
Bank name
FIRST BANK OF NIGERIA LTD
Account number
0131952914""",

    """8105287737
OPay 
Choose Harrison 
Urgent pay pls""",

    """Account holder
Emmanuel Edet isaac
Bank name
KUDA Microfinance Bank
Account number
2032190849""",

    """6097077772
Chipper cash 
John Joseph""",

    """Sheu Abdullateef
Opay Bank (Paycom)
9066786803""",

    """James Adegboye isreal 
8142939410
Palmpay""",

    """Account holder
Favor chukwuemeka Ibe
Bank name
Opay Bank (Paycom)
Account number
9151640987""",

    """Shuaib Adrian Abraham
Opay Bank (Paycom)
8140760850""",

    """Gbolahan Ayomide
UNITED BANK FOR AFRICA PLC
2209609028""",

    """Gbolahan Ayomide
Opay Bank (Paycom)
9123556584""",

    """9027907662 OPay Ifada Tennison""",

    """Prince Ukatu
KUDA Microfinance Bank
2010138577""",

    """peculiar Enebeli
KUDA Microfinance Bank
2013033594""",

    """9040091005
Opay
Oselusi Damilola""",

    """ORODE PROMISE
Opay Bank (Paycom)
7051803658""",

    """Efajueme Godfrey Goodness
KUDA Microfinance Bank
2058696220""",

    """Tobore ogoh oke
ZENITH BANK PLC
2546824267""",

    """9115097097
Oghenevwede governor 
Moniepoint""",

    """Adekoya Akeem
KUDA Microfinance Bank
2047862993""",

    """2069190571
Kuda 
Isaac benjamin""",

    """Imafidon Kingsley osas
FIRST BANK OF NIGERIA LTD
3121107595""",

    """Dada Daramola
UNITED BANK FOR AFRICA PLC
2101179250""",

    """OPay joy Esther Erhiama 8101570292""",

    """Olumide OSUNSINA
KUDA Microfinance Bank
2010323588""",

    """9065469595 Jude nentawe gogin opay""",

    """Emmanuel Edet isaac
KUDA Microfinance Bank
2032190849""",

    """Sheu Abdullateef
Opay Bank (Paycom)
9066786803""",

    """Olanrewaju olamilekan afeez
UNITED BANK FOR AFRICA PLC
2087648025""",

    """7032084691
PalmPay 
Adebayo taofeek abolanle""",

    """Idowu Timothy oluwatobi
Opay Bank (Paycom)
8106247983""",

    """9031533930 Adeniyi kayode Remi Moniepoint""",

    """Olaleru Oyeniyi Adegoke
Opay Bank (Paycom)
9072430320""",

    """8143131220… opay … Moshood Ayobami""",

    """Opeyemi rilwan
KUDA Microfinance Bank
2042904577""",

    """Awoleye Adeyemi Roseline
2018486308
Kuda""",

    """Dairo tunde
KUDA Microfinance Bank
2003061989""",

    """8100369884
OPay 
Oladiran Odunayo""",

"""Aje Oluwashina
VFD MicroFinance Bank
1000351807""",

"""8075234353
opay 
omasan Festus """,

"""7035606753
opay
olajide Johnson """,

"""OPay joy Esther Erhiama 8101570292""",

"""9135733150 OPay opeyemi Ismail arimiyau """,

"""Daniel samuel gbenga
KUDA Microfinance Bank
2023263361""",

"""Hamzat teslim
KUDA Microfinance Bank
2003037832"""

"""9027986443 opay adeyemo malik Babatunde """,

"""Adeshina Sulaimon Taofeek
Opay Bank (Paycom)
9135784844""",

"""Agbajelola Olakunle muhammed
Opay Bank (Paycom)
6130082830""",

"""Damilare Opaleye
KUDA Microfinance Bank
2001823796""",

"""Faruq Olamilekan
VFD MicroFinance Bank
1003311903""",

"""Samuel Uduma
Opay Bank (Paycom)
7066780665""",

"""Fagbemi emmanuel 
PalmPay
9066025532""",

"""Osayamhen Emmanuel praise
UNITED BANK FOR AFRICA PLC
2175927379""",

"""Adekoya Akeem
KUDA Microfinance Bank
2047862993
""",

"""8102318584

Moniepoint

sofiat""",

"""Akinsanya sodiq
KUDA Microfinance Bank
2002075994""",

"""Idowu Timothy oluwatobi
Opay Bank (Paycom)
8106247983""",

"""Emmanuel Duncan
Opay Bank (Paycom)
7044266703""",

"""Akinsanya sodiq
KUDA Microfinance Bank
2002075994""",

"""Osayamhen Emmanuel praise UNITED BANK FOR AFRICA PLC 2175927379""",

"""Adekoya Akeem
from
KUDA Microfinance Bank
2047862993""",

"""No account info provided here.""",

"""hello what's your account info?""",

"""I need your account details.""",

"""Please provide your bank account number."""

]

# Function to extract account details
def extract_account_details(message):
    message = message.strip()
    bank_pattern = r'\b(Access|GTBank|Zenith|UBA|First Bank|Fidelity|Stanbic|Wema|Opay|Moniepoint|PalmPay|Kuda|Union Bank|Heritage|Chipper Cash|Paycom|Microfinance)\b'
    account_number_pattern = r'\b\d{10,12}\b'
    name_pattern = r'\b([A-Z][a-z]+(?: [A-Z][a-z]+){1,3})\b'

    acc_no_match = re.search(account_number_pattern, message)
    bank_match = re.search(bank_pattern, message, re.IGNORECASE)

    account_name = None

    if acc_no_match:
        cleaned_msg = message.replace(acc_no_match.group(), '')
    else:
        cleaned_msg = message

    if bank_match:
        cleaned_msg = cleaned_msg.replace(bank_match.group(), '')

    # Match first proper name (1-4 words)
    name_matches = re.findall(name_pattern, cleaned_msg, re.IGNORECASE)
    if name_matches:
        account_name = name_matches[0].strip().title()

    fields_filled = sum(x is not None for x in [account_name, acc_no_match, bank_match])
    if fields_filled < 2:
        return None

    return {
        'account_name': account_name,
        'bank_name': bank_match.group().title() if bank_match else None,
        'account_number': acc_no_match.group() if acc_no_match else None
    }

# Generate dataset for training
def generate_training_data(messages):
    dataset = []

    for msg in messages:
        data = extract_account_details(msg)
        if data:
            entities = []
            for label, value in data.items():
                if value:
                    start = msg.lower().find(value.lower())
                    end = start + len(value)
                    if start != -1:
                        entities.append([start, end, label.upper()])
            dataset.append({
                "text": msg,
                "entities": entities
            })
    return dataset

# Generate and save
training_data = generate_training_data(sample_texts)
with open("account_training_data.json", "w") as f:
    json.dump(training_data, f, indent=2)

print("Training data saved to account_training_data.json")
