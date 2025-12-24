# Odoo 17 Community – Setup de Desarrollo con Docker + Addons Propios

Este documento describe, paso a paso, el **proceso que SÍ funcionó** para levantar
Odoo 17 Community en un VPS usando Docker, resolver errores de DB y CSS,
y dejar el entorno listo para desarrollar addons propios (ej: Conciliapp).

---

## Requisitos

- VPS Linux (Ubuntu recomendado)
- Docker y Docker Compose
- Acceso por IP o dominio
- Repositorio en GitHub
- (Opcional) EasyPanel para deploy visual

---

## PASO 1 – Crear repositorio

Repositorio ejemplo:

```
conciliapp-odoo
```

Estructura base:

```
.
├── Dockerfile
├── docker-compose.yml
├── addons/
│   └── (aquí irán los addons)
```

---

## PASO 2 – Dockerfile (Odoo 17 + assets)

**Dockerfile**

```dockerfile
FROM odoo:17.0

# Copiar addons personalizados
COPY ./addons /mnt/extra-addons

# Instalar dependencias necesarias para compilar assets (CSS/JS)
RUN apt-get update && apt-get install -y --no-install-recommends \
    nodejs npm \
 && npm install -g rtlcss sass \
 && rm -rf /var/lib/apt/lists/*

# Ejecutar Odoo con addons custom
CMD ["odoo", "--addons-path=/usr/lib/python3/dist-packages/odoo/addons,/mnt/extra-addons"]
```

📌 Esto evita el error:

> Style compilation failed / Undefined SCSS variables

---

## PASO 3 – docker-compose.yml (versión funcional)

```yaml
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: postgres
      POSTGRES_USER: odoo
      POSTGRES_PASSWORD: odoo_password
    volumes:
      - odoo_db:/var/lib/postgresql/data
    healthcheck:
      test: ['CMD-SHELL', 'pg_isready -U odoo -d postgres']
      interval: 5s
      timeout: 5s
      retries: 20

  odoo:
    image: ghcr.io/kesildigital/conciliapp-odoo:main
    depends_on:
      db:
        condition: service_healthy
    volumes:
      - odoo_data:/var/lib/odoo
    ports:
      - '19069:8069'
    command:
      - odoo
      - '--config=/dev/null'
      - '--addons-path=/usr/lib/python3/dist-packages/odoo/addons,/mnt/extra-addons'
      - '--db_host=db'
      - '--db_port=5432'
      - '--db_user=odoo'
      - '--db_password=odoo_password'
      - '--http-port=8069'

volumes:
  odoo_db:
  odoo_data:
```

---

## PASO 4 – Deploy

### Opción A: Docker puro

```bash
docker compose up -d
```

### Opción B: EasyPanel

- Crear servicio tipo **Compose**
- Pegar el `docker-compose.yml`
- Deploy

Ver logs:

```bash
docker logs -f conciliapp-odoo_odoo-1
```

Debe aparecer:

```
HTTP service (werkzeug) running on ...:8069
```

---

## PASO 5 – Acceder a Odoo

Abrir en navegador:

```
http://IP_DEL_VPS:19069
```

⚠️ IMPORTANTE  
**NO usar la base de datos `postgres` para trabajar.**

---

## PASO 6 – Crear base de datos correcta

En la pantalla de login, hacer clic en:

👉 **Manage Databases Powered by Odoo**

Crear una nueva DB:

- Database name: `odoo17`
- Email: admin
- Password: a elección
- Demo data: opcional

📌 Este paso:

- Soluciona errores de CSS
- Inicializa correctamente `web`, `base`, `assets`
- Evita estados inconsistentes

---

## PASO 7 – Verificación

Todo está bien si:

- El login carga con estilos
- Entras al backend
- Ves la pantalla **Apps**

---

## NOTA IMPORTANTE – Studio

- Odoo **Community NO incluye Studio**
- Studio requiere **Enterprise / Upgrade**
- Por tanto:
  - ❌ No botones visuales
  - ❌ No lógica tipo WeWeb desde UI
  - ✅ Todo se hace vía **addons en Python**

---

## PASO 8 – Camino correcto para el proyecto

Para Conciliapp:

✔️ Crear addon propio en Python  
✔️ Heredar modelos (`account.payment`, etc.)  
✔️ Agregar botón “Conciliar”  
✔️ Llamar API de Conciliapp con `requests`  
✔️ Guardar estado del pago

Esto funciona en:

- Odoo Community
- Odoo.sh
- Odoo Online

---

## Estado final

✅ Odoo 17 Community funcionando  
✅ Docker estable  
✅ DB correcta  
✅ Assets compilando bien  
✅ Listo para desarrollar addons

---

## Próximo paso sugerido

👉 Crear el addon `conciliapp_connector` (esqueleto mínimo).
