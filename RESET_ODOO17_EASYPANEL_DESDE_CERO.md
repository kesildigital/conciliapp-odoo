# Reset y Setup limpio de Odoo 17 en EasyPanel (desde cero)

Guía repetible para borrar Odoo + PostgreSQL, evitar reutilización de volúmenes, montar addons propios, configurar addons_path y DB, e instalar el módulo correctamente.

---

## 1. Detener y borrar SOLO el stack de Odoo

### 1.1 Identificar contenedores
```bash
docker ps -a | grep conciliapp-odoo
```

### 1.2 Detener y eliminar contenedores
```bash
docker stop <odoo_container> <db_container>
docker rm <odoo_container> <db_container>
```

---

## 2. Borrar volúmenes (PASO CRÍTICO)

### 2.1 Listar volúmenes de Odoo
```bash
docker volume ls | grep conciliapp-odoo
```

### 2.2 Borrarlos
```bash
docker volume rm \
  conciliapp-odoo_odoo-db_odoo-db-data \
  conciliapp-odoo_odoo_odoo-addons \
  conciliapp-odoo_odoo_odoo-config \
  conciliapp-odoo_odoo_odoo-web-data
```

### 2.3 Verificación
```bash
docker volume ls | grep conciliapp-odoo || echo "OK: limpio"
```

---

## 3. Deploy nuevo en EasyPanel

- Deploy template Odoo + PostgreSQL
- Abrir URL → debe salir Create Database
- Si no sale, el reset no fue correcto

---

## 4. Crear base de datos desde la UI

- Database name: odoo
- Demo data: NO
- Crear DB

---

## 5. Preparar carpeta de addons en el VPS

Ejemplo de ruta:
```
/opt/conciliapp/odoo/odoo-addons/conciliapp-odoo/addons
```

Debe existir:
```
conciliapp_connector/__manifest__.py
```

---

## 6. Bind mount del addon

En EasyPanel → Servicio Odoo → Volumes

- Eliminar cualquier mount en /mnt/extra-addons
- Agregar Bind mount:
  - Host: /opt/conciliapp/odoo/odoo-addons/conciliapp-odoo/addons
  - Container: /mnt/extra-addons

Redeploy.

Verificar:
```bash
ls -la /mnt/extra-addons
ls -la /mnt/extra-addons/conciliapp_connector/__manifest__.py
```

---

## 7. Configurar /etc/odoo/odoo.conf

```ini
[options]
addons_path = /usr/lib/python3/dist-packages/odoo/addons,/var/lib/odoo/addons/17.0,/mnt/extra-addons
data_dir = /var/lib/odoo
admin_passwd = <hash existente>

db_host = <nombre_servicio_postgres>
db_port = 5432
db_user = odoo
db_password = <password postgres>
```

---

## 8. Command en EasyPanel

- Command: VACÍO
- Restart / Redeploy

---

## 9. Instalar el módulo

```bash
odoo -d odoo -i conciliapp_connector --stop-after-init
```

O desde Apps → Update Apps List → Install.

---

## 10. Verificación final

- Menú visible en waffle
- Addon instalado
- DB limpia
