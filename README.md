# Blog: Obsolescència i dret a reparar

Blog del grup 10 de PEF1 (curs 26-27), dentro del proyecto VINCLE DIGITAL. Está hecho con [Quarto](https://quarto.org) y se publica solo en GitHub Pages cada vez que alguien sube cambios a `main`.

## Cómo está organizado

```
_quarto.yml          configuración: título, menú, tema (casi nunca hay que tocarlo)
index.qmd            portada; lista las entradas automáticamente
referencies.qmd      lista de todas las referencias (se genera sola)
credits.qmd          quién ha hecho qué y uso de IA (rellenar a mano)
references.bib       TODAS las referencias del blog, en un solo archivo
posts/
  _plantilla/        plantilla para copiar (no se publica)
  nombre-entrada/
    index.qmd        el texto de la entrada
    foto.jpg         sus imágenes, en la misma carpeta
```

## Escribir una entrada nueva

1. Copia la carpeta `posts/_plantilla` y renómbrala con un nombre corto, sin espacios ni acentos, por ejemplo `posts/casos-judicials`. El guion bajo inicial es lo que impide que la plantilla se publique, así que la carpeta nueva no debe llevarlo.
2. Abre `index.qmd` y rellena la cabecera (`title`, `description`, `author`, `date`, `categories`).
3. Escribe debajo en Markdown: `## Título de sección`, `**negrita**`, `*cursiva*`, `[texto](https://enlace)`, listas con `-`.
4. Las imágenes van en la misma carpeta que la entrada:

   ```markdown
   ![Pie de figura. Font: elaboració pròpia.](foto.jpg)
   ```

5. Sube los cambios a GitHub. En uno o dos minutos la entrada aparece en la portada.

## Citar referencias

Todas las referencias viven en `references.bib`. Para añadir una:

1. Busca la referencia en Google Scholar, pulsa "Citar" y luego "BibTeX", o expórtala desde Zotero.
2. Pégala **al final** de `references.bib`. Si todos añadís siempre al final, git casi nunca da conflictos.
3. La primera línea, `@article{makov2019,`, define la clave. Debe ser única. Usad `apellidoaño`, por ejemplo `makov2019` o `ocu2025`.

Para citar en el texto:

| Escribes | Sale |
|---|---|
| `[@makov2019]` | (Makov et al. 2019) |
| `[@makov2019, p. 552]` | (Makov et al. 2019, 552) |
| `[@makov2019; @ocu2025]` | (Makov et al. 2019; OCU 2025) |
| `@makov2019 troben que...` | Makov et al. (2019) troben que... |

La bibliografía se añade sola al final de cada entrada, y la página Referències recoge todas las de `references.bib`.

Para webs, informes y noticias, el tipo es `@online`:

```bibtex
@online{repaireu2026,
  author  = {{Right to Repair Europe}},
  title   = {One year into EU ecodesign rules},
  year    = {2026},
  url     = {https://repair.eu/news/...},
  urldate = {2026-11-01},
}
```

Las dobles llaves `{{...}}` hacen que un nombre de organización no se trate como "apellido, nombre".

## Subir los cambios

### Desde la web de GitHub

No hay que instalar nada. Entra en el archivo, pulsa el lápiz, edita y pulsa "Commit changes". Para subir fotos, entra en la carpeta de la entrada y usa "Add file" → "Upload files".

### Desde tu ordenador

```bash
git pull                 # SIEMPRE antes de empezar
# ... editar ...
git add .
git commit -m "Entrada casos judicials"
git push
```

Si `git push` falla porque otra persona ha subido algo mientras tanto, haz `git pull` y vuelve a hacer `git push`.

En la pestaña Actions del repositorio se ve si la publicación ha ido bien (verde) o ha fallado (rojo). Cuando falla, casi siempre es por una clave de cita que no existe en `references.bib` o por un error de formato en ese archivo.

## Ver el blog en local antes de subir (opcional)

Instala Quarto desde <https://quarto.org/docs/get-started/> y, dentro de la carpeta del repositorio:

```bash
quarto preview
```

Se abre el navegador y la página se actualiza cada vez que guardas un archivo.

## Normas del grupo

- Cada entrada la escribe una persona, que pone su nombre en `author`.
- Toda imagen o gráfico lleva pie con la fuente ("Font: elaboració pròpia" si es nuestro).
- Antes de citar una cifra, comprobadla en la fuente original.
- Apuntad en `credits.qmd` qué habéis hecho y qué IA habéis usado, para qué y cómo lo habéis verificado.
