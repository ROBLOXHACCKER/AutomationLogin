# Dati di input
#email:password
credenziali_varie = """
simonazzica@gmail.com:ET21busa
drisdcristin055@gmail.com:Kilsa214
"""

emails = []
passwords = []

for line in credenziali_varie.strip().split('\n'):
    email, password = line.split(':')
    emails.append(email)
    passwords.append(password)

EMAIL_DIVISE = ','.join(emails)
PASSWORD_DIVISE = ','.join(passwords)

with open('targetCredential.txt', 'w') as file:
    file.write(f"EMAIL={EMAIL_DIVISE}\n")
    file.write(f"PASSWORD={PASSWORD_DIVISE}\n")

