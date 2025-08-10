# Todo List App - Django

Una aplicación de gestión de tareas moderna construida con Django y Tailwind CSS, con funcionalidades de Kanban board, categorías, notas y drag & drop.

## 🚀 Características

- **Dashboard Kanban**: Vista de tablero con drag & drop entre columnas
- **Vista Lista**: Vista tradicional de lista de tareas
- **Categorías**: Organización por categorías con colores personalizados
- **Notas**: Sistema de notas dentro de cada tarea
- **Autenticación**: Sistema de login/registro de usuarios
- **Responsive**: Diseño adaptativo para móviles y desktop
- **Dark Theme**: Interfaz moderna con tema oscuro

## 🛠️ Tecnologías

- **Backend**: Django 5.2.5
- **Frontend**: Tailwind CSS
- **Base de Datos**: PostgreSQL (producción) / SQLite (desarrollo)
- **JavaScript**: Vanilla JS + SortableJS para drag & drop
- **Servidor**: Gunicorn (producción)

## 📦 Instalación Local

### Prerrequisitos
- Python 3.13+
- pip
- virtualenv

### Pasos

1. **Clonar el repositorio**
```bash
git clone <tu-repositorio>
cd first-django-app
```

2. **Crear entorno virtual**
```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar base de datos**
```bash
python manage.py migrate
```

5. **Crear superusuario (opcional)**
```bash
python manage.py createsuperuser
```

6. **Ejecutar servidor de desarrollo**
```bash
python manage.py runserver
```

7. **Acceder a la aplicación**
- URL: http://localhost:8000
- Admin: http://localhost:8000/admin

## 🚀 Despliegue en Render

### Opción 1: Despliegue Automático con render.yaml

1. **Subir código a GitHub**
```bash
git add .
git commit -m "Preparar para despliegue en Render"
git push origin main
```

2. **Conectar con Render**
- Ve a [render.com](https://render.com)
- Crea una cuenta o inicia sesión
- Haz clic en "New +" → "Blueprint"
- Conecta tu repositorio de GitHub
- Render detectará automáticamente el archivo `render.yaml`

3. **Configurar variables de entorno**
- `SECRET_KEY`: Se genera automáticamente
- `DATABASE_URL`: Se configura automáticamente desde la base de datos PostgreSQL

### Opción 2: Despliegue Manual

1. **Crear base de datos PostgreSQL**
- En Render Dashboard: "New +" → "PostgreSQL"
- Nombre: `todo-list-db`
- Plan: Free

2. **Crear Web Service**
- "New +" → "Web Service"
- Conecta tu repositorio de GitHub
- Configuración:
  - **Build Command**: `./build.sh`
  - **Start Command**: `gunicorn todo_list.wsgi:application`
  - **Environment Variables**:
    - `SECRET_KEY`: Genera una clave secreta
    - `DATABASE_URL`: URL de tu base de datos PostgreSQL

## 🔧 Configuración de Producción

### Variables de Entorno Requeridas

```bash
SECRET_KEY=tu-clave-secreta-aqui
DATABASE_URL=postgresql://usuario:password@host:puerto/database
```

### Archivos de Configuración

- `build.sh`: Script de construcción para Render
- `render.yaml`: Configuración de despliegue automático
- `requirements.txt`: Dependencias de Python
- `todo_list/settings.py`: Configuración de Django

## 📁 Estructura del Proyecto

```
first-django-app/
├── app/                    # Aplicación principal
│   ├── models.py          # Modelos de datos
│   ├── views.py           # Vistas y lógica
│   ├── urls.py            # URLs de la app
│   └── admin.py           # Configuración del admin
├── todo_list/             # Configuración del proyecto
│   ├── settings.py        # Configuración de Django
│   ├── urls.py            # URLs principales
│   └── wsgi.py            # Configuración WSGI
├── templates/             # Plantillas HTML
│   ├── app/               # Plantillas de la app
│   └── registration/      # Plantillas de autenticación
├── static/                # Archivos estáticos
├── build.sh               # Script de construcción
├── render.yaml            # Configuración de Render
└── requirements.txt       # Dependencias
```

## 🎨 Características de la UI

### Drag & Drop Intuitivo
- **Click en tarjeta**: Navega a detalles de la tarea
- **Drag desde handle**: Mueve tarea entre columnas
- **Área específica**: Solo el icono de líneas permite drag

### Responsive Design
- **Mobile-first**: Optimizado para dispositivos móviles
- **Breakpoints**: Adaptativo a diferentes tamaños de pantalla
- **Touch-friendly**: Áreas de toque apropiadas para móviles

### Dark Theme
- **Colores modernos**: Paleta de colores oscura
- **Contraste optimizado**: Legibilidad mejorada
- **Efectos visuales**: Hover states y transiciones suaves

## 🔒 Seguridad

- **Autenticación**: Sistema de usuarios con Django Auth
- **CSRF Protection**: Protección contra ataques CSRF
- **SQL Injection**: Prevención mediante ORM de Django
- **XSS Protection**: Headers de seguridad configurados
- **HTTPS**: Forzado en producción

## 📊 Base de Datos

### Modelos Principales

- **User**: Usuarios del sistema (Django Auth)
- **Category**: Categorías de tareas con colores
- **Todo**: Tareas con estado, prioridad y descripción
- **Note**: Notas asociadas a cada tarea

### Migraciones

```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate
```

## 🧪 Testing

```bash
# Ejecutar tests
python manage.py test

# Tests específicos
python manage.py test app.tests
```

## 📝 Licencia

Este proyecto está bajo la Licencia MIT.

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📞 Soporte

Si tienes problemas o preguntas:
- Abre un issue en GitHub
- Revisa la documentación de Django
- Consulta la documentación de Render

---

**¡Disfruta organizando tus tareas! 🎯**
