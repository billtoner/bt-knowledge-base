# html-snippets

Boilerplates and patterns worth a copy-paste. Not a tutorial — the things you forget exactly how to type each time.

**Tags:** html · docs

## Modern HTML5 page

```html
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Page</title>
    <link rel="icon" href="data:,">                  <!-- silence the favicon 404 -->
</head>
<body>
    <h1>Hello</h1>
</body>
</html>
```

## Single-file demo with classless CSS

```html
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://cdn.simplecss.org/simple.min.css">
    <title>Demo</title>
</head>
<body>
    <main>
        <h1>Demo</h1>
        <p>No classes, no build step — just write semantic HTML.</p>
    </main>
</body>
</html>
<!-- simple.css, pico.css, water.css all work the same way -->
```

## Native collapsible (no JS)

```html
<details>
    <summary>Click to expand</summary>
    <p>Hidden content.</p>
</details>
```

## Native modal (no JS for open-from-button)

```html
<dialog id="d">
    <p>This is a real, focus-trapping modal.</p>
    <form method="dialog"><button>Close</button></form>
</dialog>
<button onclick="document.getElementById('d').showModal()">Open</button>
```

## Form with sensible defaults

```html
<form>
    <label>Email <input type="email" name="email" required autocomplete="email"></label>
    <label>Password <input type="password" name="pw" required minlength="8" autocomplete="new-password"></label>
    <button type="submit">Sign in</button>
</form>
<!-- type=email gives validation + mobile keyboard -->
<!-- autocomplete hints help password managers -->
```

## Iframe sandbox

```html
<iframe src="untrusted.html"
        sandbox="allow-scripts"
        referrerpolicy="no-referrer"
        loading="lazy"></iframe>
<!-- omit allow-same-origin to prevent cookie/storage access -->
```

## Meta tags worth remembering

```html
<meta name="description" content="...">                  <!-- search results -->
<meta name="theme-color" content="#0f172a">              <!-- mobile browser chrome -->
<meta property="og:title" content="...">                 <!-- link previews (Slack, FB, etc.) -->
<meta property="og:image" content="https://...png">      <!-- ditto -->
<link rel="canonical" href="https://example.com/page">   <!-- dedup for search engines -->
```

## Quick local preview

```bash
python3 -m http.server 8000      # serve cwd; open http://localhost:8000
                                 # (see tool-notes/python-one-liners.md)
```
