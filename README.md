# Todo List App con Django y Tailwind CSS

Una aplicación simple de lista de tareas construida con Django y estilizada con Tailwind CSS.

## 🚀 Características

- ✅ Agregar nuevas tareas
- ✅ Marcar tareas como completadas
- ✅ Eliminar tareas
- 🎨 Interfaz moderna y responsive con Tailwind CSS
- 📱 Diseño mobile-first
- ⚡ Interacciones suaves y animaciones

## 🛠️ Tecnologías Utilizadas

- **Backend**: Django 5.2.5
- **Frontend**: Tailwind CSS (via CDN)
- **Base de Datos**: SQLite (por defecto)
- **Python**: 3.x

## 📦 Instalación

1. **Clona el repositorio**
   ```bash
   git clone <tu-repositorio>
   cd first-django-app
   ```

2. **Crea un entorno virtual**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # En Linux/Mac
   # o
   venv\Scripts\activate  # En Windows
   ```

3. **Instala las dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecuta las migraciones**
   ```bash
   python manage.py migrate
   ```

5. **Inicia el servidor de desarrollo**
   ```bash
   python manage.py runserver
   ```

6. **Abre tu navegador**
   Ve a `http://127.0.0.1:8000/`

## 🎯 Cómo Usar

1. **Agregar una tarea**: Escribe el título de la tarea en el campo de texto y presiona "Agregar"
2. **Marcar como completada**: Haz clic en el círculo vacío junto a la tarea
3. **Eliminar tarea**: Haz clic en el ícono de papelera
4. **Ver estadísticas**: Las estadísticas se muestran en la parte inferior

## 📁 Estructura del Proyecto

```
first-django-app/
├── app/                    # Aplicación principal
│   ├── models.py          # Modelo Todo
│   ├── views.py           # Vistas de la aplicación
│   ├── urls.py            # URLs de la aplicación
│   └── migrations/        # Migraciones de la base de datos
├── todo_list/             # Configuración del proyecto
│   ├── settings.py        # Configuración de Django
│   ├── urls.py            # URLs principales
│   └── wsgi.py           # Configuración WSGI
├── templates/             # Templates HTML
│   └── app/
│       └── todo_list.html # Template principal
├── static/                # Archivos estáticos
├── manage.py             # Script de gestión de Django
├── requirements.txt      # Dependencias del proyecto
├── render.yaml           # Configuración para Render
└── README.md            # Este archivo
```

## 🎨 Tailwind CSS

La aplicación utiliza Tailwind CSS a través de CDN para un desarrollo rápido. Las clases principales utilizadas incluyen:

- **Layout**: `container`, `flex`, `grid`, `space-y-3`
- **Spacing**: `px-4`, `py-8`, `mb-8`, `gap-2`
- **Colors**: `bg-gray-100`, `text-gray-800`, `bg-primary`
- **Components**: `rounded-lg`, `shadow-md`, `hover:shadow-lg`
- **Responsive**: `max-w-md`, `mx-auto`

## 🔧 Personalización

### Cambiar colores
Edita la configuración de Tailwind en `templates/app/todo_list.html`:

```javascript
tailwind.config = {
    theme: {
        extend: {
            colors: {
                primary: '#3B82F6',    // Azul
                secondary: '#10B981',  // Verde
            }
        }
    }
}
```

### Agregar nuevas funcionalidades
1. Modifica el modelo en `app/models.py`
2. Actualiza las vistas en `app/views.py`
3. Añade nuevas URLs en `app/urls.py`
4. Actualiza el template en `templates/app/todo_list.html`

## 🚀 Despliegue en Render

### Configuración Automática (Recomendado)

1. **Conecta tu repositorio a Render**
   - Ve a [render.com](https://render.com)
   - Crea una nueva cuenta o inicia sesión
   - Haz clic en "New +" y selecciona "Web Service"
   - Conecta tu repositorio de GitHub

2. **Configura el servicio**
   - **Name**: `first-django-app` (o el nombre que prefieras)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python manage.py collectstatic --noinput && python manage.py migrate && gunicorn todo_list.wsgi:application`

3. **Variables de Entorno**
   - `DEBUG`: `False`
   - `SECRET_KEY`: Render generará automáticamente una clave segura

4. **Deploy**
   - Haz clic en "Create Web Service"
   - Render detectará automáticamente el archivo `render.yaml` y configurará todo

### Configuración Manual

Si prefieres configurar manualmente:

1. **Crea un nuevo Web Service en Render**
2. **Configura las variables de entorno**:
   ```
   DEBUG=False
   SECRET_KEY=<tu-clave-secreta>
   ```
3. **Build Command**: `pip install -r requirements.txt`
4. **Start Command**: `python manage.py collectstatic --noinput && python manage.py migrate && gunicorn todo_list.wsgi:application`

### Variables de Entorno Disponibles

- `DEBUG`: Controla el modo debug (True/False)
- `SECRET_KEY`: Clave secreta de Django (Render la genera automáticamente)
- `CSRF_TRUSTED_ORIGINS`: Dominios confiables para CSRF (configurado automáticamente)
- `DATABASE_URL`: URL de la base de datos (opcional, por defecto usa SQLite)

### Notas Importantes

- ✅ El archivo `render.yaml` ya está configurado para el deploy automático
- ✅ `gunicorn` está incluido en `requirements.txt`
- ✅ Los archivos estáticos se configuran automáticamente
- ✅ `ALLOWED_HOSTS` incluye dominios de Render
- ✅ `CSRF_TRUSTED_ORIGINS` configurado para dominios de Render
- ✅ Las migraciones se ejecutan automáticamente en el deploy

## 📝 Licencia

Este proyecto está bajo la Licencia MIT.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o un pull request.

---

¡Disfruta organizando tus tareas! 📝✨
