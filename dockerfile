FROM odoo:17.0

USER root

# Dependencias para assets (CSS/SCSS)
RUN apt-get update && apt-get install -y --no-install-recommends \
    nodejs npm \
 && npm install -g rtlcss sass \
 && rm -rf /var/lib/apt/lists/*

# Copiamos tus addons al path de addons extra
COPY ./addons /mnt/extra-addons

# (Opcional) dar permisos si hiciera falta
RUN chown -R odoo:odoo /mnt/extra-addons

USER odoo

# Aseguramos que Odoo cargue tus addons
CMD ["odoo", "--addons-path=/usr/lib/python3/dist-packages/odoo/addons,/mnt/extra-addons"]
