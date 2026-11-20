"""Construit la V6 locale : un seul HTML, bibliothèques intégrées, réseau interdit par CSP."""
import re, sys, hashlib
src, libs, pdflib, out = sys.argv[1:5]
s = open(src, encoding='utf-8').read()
read = lambda p: open(p, encoding='utf-8').read()
pdfjs = read(f'{libs}/pdf.min.js')
worker = read(f'{libs}/pdf.worker.min.js')
xlsx = read(f'{libs}/xlsx.full.min.js')
plib = re.sub(r'\n?//# sourceMappingURL=\S+\s*$', '\n', read(pdflib))
for name, code in [('pdf.js', pdfjs), ('worker', worker), ('xlsx', xlsx), ('pdf-lib', plib)]:
    assert '</script' not in code.lower() and '<script' not in code.lower(), name

def rep(old, new, count=1):
    global s
    n = s.count(old)
    assert n == count, (old[:70], n)
    s = s.replace(old, new)

# 1. Politique de sécurité : aucune connexion réseau possible depuis la page.
csp = ("default-src 'none'; script-src 'unsafe-inline' blob:; worker-src blob:; "
       "style-src 'unsafe-inline'; img-src data: blob:; font-src data: blob:; "
       "connect-src 'none'; media-src 'none'; object-src 'none'; frame-src 'none'; "
       "form-action 'none'; base-uri 'none'")
rep('<meta charset="utf-8">',
    '<meta charset="utf-8"><meta http-equiv="Content-Security-Policy" content="' + csp + '">'
    '<meta name="referrer" content="no-referrer">')

# 2. Bibliothèques intégrées à la place des CDN.
banner = lambda n, v, lic: f'/* ===== {n} {v} — intégré tel quel ({lic}) ===== */\n'
rep('<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js"></script>'
    '<script src="https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js"></script>',
    '<script>\n' + banner('PDF.js', '3.11.174', 'Apache-2.0') + pdfjs + '\n</script>\n'
    '<script id="pdfjs-worker-src" type="text/plain">\n' + worker + '\n</script>\n'
    '<script>\n' + banner('SheetJS', '0.18.5', 'Apache-2.0') + xlsx + '\n</script>')
rep('<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf-lib/1.17.1/pdf-lib.min.js"></script>',
    '<script>\n' + banner('pdf-lib', '1.17.1', 'MIT') + plib + '\n</script>\n'
    "<script>\n// Worker PDF.js créé en mémoire (blob:) : fonctionne en file:// sans aucun téléchargement.\n"
    "(function(){try{const code=document.getElementById('pdfjs-worker-src').textContent;"
    "pdfjsLib.GlobalWorkerOptions.workerSrc=URL.createObjectURL(new Blob([code],{type:'text/javascript'}));}"
    "catch(e){console.error('Worker PDF.js indisponible',e)}})();\n</script>")
rep("pdfjsLib.GlobalWorkerOptions.workerSrc='https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';", '')

# 3. PDF.js : pas d'eval (compatible CSP), pas de chargement externe de polices.
rep("pdfjsLib.getDocument({data:", "pdfjsLib.getDocument({isEvalSupported:false,useSystemFonts:true,disableFontFace:false,data:", 2)

# 4. Libellés.
rep('<title>Éditeur technique — Schémas, nomenclature et fonctions V6</title>',
    '<title>Éditeur technique — Schémas, nomenclature et fonctions V6 local</title>')
rep('V6</span>', 'V6 local · 100 % hors ligne</span>')
rep('Connexion Internet requise pour charger PDF.js et SheetJS depuis les CDN.',
    'Fonctionne 100 % hors ligne : bibliothèques intégrées, connexions réseau bloquées par le navigateur.')
rep("(connexion requise)", "(fichier HTML incomplet)", 2)
rep("vérifier la connexion Internet.", "fichier HTML incomplet.")
assert 'cdnjs' not in s and 'https://' not in s.split('<script>')[0]
open(out, 'w', encoding='utf-8').write(s)
print(out, f'{len(s.encode())/1e6:.2f} Mo', hashlib.sha256(s.encode()).hexdigest()[:16])
