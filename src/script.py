import os
from datetime import datetime
from pprint import pprint

from intradel_my_container import Informations, IntradelMyContainer, Organic, Residual

LOGIN = os.getenv("INTRADEL_LOGIN", "missing_login_env")
PASSWORD = os.environ.get("INTRADEL_PASSWORD", "missing_password_env")
MUNICIPALITY = os.environ.get("MUNICIPALITY", "missing_municipality_env")

data: IntradelMyContainer = IntradelMyContainer(
    login=LOGIN,
    password=PASSWORD,
    municipality=MUNICIPALITY,
    start_date=datetime.today().replace(year=2014, month=1, day=1),
)

informations: Informations = data.my_informations
organic: Organic = data.organic
residual: Residual = data.residual

print(informations.name)
print(
    f"Organic: Collects: {organic.total_collects()} - Kilograms: {organic.total_kilograms()}"
)
print(
    f"Residual: Collects: {residual.total_collects()} - Kilograms: {residual.total_kilograms()}"
)

pprint(residual.total_kilograms_per_year())
pprint(organic.total_kilograms_per_year())
print("The end")
