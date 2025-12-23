FROM odoo:17.0

# Copiamos tus addons al path de addons extra
COPY ./addons /mnt/extra-addons

# Aseguramos que Odoo cargue tus addons
CMD ["odoo", "--addons-path=/usr/lib/python3/dist-packages/odoo/addons,/mnt/extra-addons"]
