# Portafolio con Python

Este portafolio se genera con un script en Python y produce un sitio estatico en la carpeta `public/`.

## Como usar

1. Edita `content.json` con tu informacion real.
2. Ejecuta el generador:

   ```bash
   python site_generator.py
   ```

3. Abre `public/index.html` en tu navegador.

## Hosting 24/7 (opciones simples)

- GitHub Pages: sube la carpeta `public/` a un repositorio y publica desde esa carpeta.
- Netlify: arrastra `public/` al panel o conecta el repo y usa `public` como directorio de publicacion.
- Render: crea un Static Site y usa `public` como directorio de build.

## Preview local rapido

```bash
python -m http.server --directory public 8000
```
