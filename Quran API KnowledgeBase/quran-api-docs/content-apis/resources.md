# Resources API

> Languages, recitations, scripts, and metadata  
> **Base Path:** `/resources`

---

## Endpoints

### List Languages

Get all available languages for translations and UI.

```
GET /resources/languages
```

**Response (200):**

```json
{
  "languages": [
    {
      "id": 174,
      "name": "English",
      "iso_code": "en",
      "native_name": "English",
      "direction": "ltr",
      "translations_count": 25,
      "translated_name": {
        "name": "English",
        "language_name": "english"
      }
    },
    {
      "id": 20,
      "name": "Arabic",
      "iso_code": "ar",
      "native_name": "العربية",
      "direction": "rtl",
      "translations_count": 5
    }
  ]
}
```

---

### List Recitations

Get all available recitation options.

```
GET /resources/recitations
```

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `language` | string | Language for reciter names |

**Response (200):**

```json
{
  "recitations": [
    {
      "id": 1,
      "reciter_name": "AbdulBaset AbdulSamad",
      "style": "Mujawwad",
      "translated_name": {
        "name": "AbdulBaset AbdulSamad",
        "language_name": "english"
      }
    }
  ]
}
```

---

### List Translations

Get all available translation resources.

```
GET /resources/translations
```

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `language` | string | Filter by language code |

See [translations.md](translations.md) for detailed documentation.

---

### List Tafsirs

Get all available tafsir resources.

```
GET /resources/tafsirs
```

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `language` | string | Filter by language code |

See [tafsirs.md](tafsirs.md) for detailed documentation.

---

### List Chapter Reciters

Get reciters who have complete chapter-level recitations.

```
GET /resources/chapter_reciters
```

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `language` | string | Language for names |

---

### List Verse Media

Get available verse-level media (images, audio markers).

```
GET /resources/verse_media
```

---

## Language Object Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Language ID |
| `name` | string | Language name |
| `iso_code` | string | ISO 639-1 code |
| `native_name` | string | Name in native script |
| `direction` | string | `ltr` or `rtl` |
| `translations_count` | integer | Available translations |

---

## Examples

### Get All Languages

```bash
curl "https://apis-prelive.quran.foundation/content/api/v4/resources/languages"
```

### Get All Reciters

```bash
curl "https://apis-prelive.quran.foundation/content/api/v4/resources/recitations"
```

### Get English Translations List

```bash
curl "https://apis-prelive.quran.foundation/content/api/v4/resources/translations?language=en"
```

---

*[Back to Content APIs](README.md) | [Back to Main Index](../README.md)*
