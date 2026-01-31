# Audio API

> Recitations and audio files for Quran chapters and verses  
> **Base Path:** `/recitations`, `/chapter_recitations`

---

## Endpoints Overview

| Endpoint | Description |
|----------|-------------|
| `GET /resources/recitations` | List all available reciters |
| `GET /chapter_recitations/{id}` | Get all chapter audio files for a reciter |
| `GET /chapter_recitations/{id}/{chapter_number}` | Get audio for specific chapter |
| `GET /recitations/{recitation_id}/by_chapter/{chapter_number}` | Verse-by-verse audio |
| `GET /recitations/{recitation_id}/by_juz/{juz_number}` | Audio by Juz |
| `GET /recitations/{recitation_id}/by_page/{page_number}` | Audio by page |
| `GET /recitations/{recitation_id}/by_hizb/{hizb_number}` | Audio by Hizb |
| `GET /recitations/{recitation_id}/by_ayah/{ayah_key}` | Audio for single verse |
| `GET /recitations/{recitation_id}/by_rub/{rub_el_hizb_number}` | Audio by Rub El Hizb |

---

## List Available Reciters

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
    },
    {
      "id": 7,
      "reciter_name": "Mishari Rashid al-`Afasy",
      "style": null,
      "translated_name": {
        "name": "Mishari Rashid al-`Afasy",
        "language_name": "english"
      }
    }
  ]
}
```

---

## Get Chapter Audio Files

Get audio file URLs for all chapters by a specific reciter.

```
GET /chapter_recitations/{id}
```

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | integer | ✓ | Recitation/Reciter ID |

**Response (200):**

```json
{
  "audio_files": [
    {
      "id": 1,
      "chapter_id": 1,
      "file_size": 1234567,
      "format": "mp3",
      "audio_url": "https://..."
    }
  ]
}
```

---

## Get Specific Chapter Audio

Get audio file for a specific chapter.

```
GET /chapter_recitations/{id}/{chapter_number}
```

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | integer | ✓ | Recitation ID |
| `chapter_number` | integer | ✓ | Chapter number (1-114) |

**Response (200):**

```json
{
  "audio_file": {
    "id": 1,
    "chapter_id": 1,
    "file_size": 1024000,
    "format": "mp3",
    "audio_url": "https://audio.qurancdn.com/..."
  }
}
```

---

## Get Verse-by-Verse Audio

Get individual audio segments for each verse.

```
GET /recitations/{recitation_id}/by_chapter/{chapter_number}
```

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `recitation_id` | integer | ✓ | Recitation ID |
| `chapter_number` | integer | ✓ | Chapter number (1-114) |

**Response (200):**

```json
{
  "audio_files": [
    {
      "verse_key": "1:1",
      "url": "https://verses.quran.com/..."
    },
    {
      "verse_key": "1:2",
      "url": "https://verses.quran.com/..."
    }
  ],
  "pagination": {
    "per_page": 10,
    "current_page": 1,
    "next_page": null,
    "total_pages": 1,
    "total_records": 7
  }
}
```

---

## Get Audio by Juz

```
GET /recitations/{recitation_id}/by_juz/{juz_number}
```

**Path Parameters:**

| Parameter | Type | Required | Range |
|-----------|------|----------|-------|
| `recitation_id` | integer | ✓ | Reciter ID |
| `juz_number` | integer | ✓ | 1-30 |

---

## Get Audio by Page

```
GET /recitations/{recitation_id}/by_page/{page_number}
```

**Path Parameters:**

| Parameter | Type | Required | Range |
|-----------|------|----------|-------|
| `recitation_id` | integer | ✓ | Reciter ID |
| `page_number` | integer | ✓ | 1-604 |

---

## Get Audio by Hizb

```
GET /recitations/{recitation_id}/by_hizb/{hizb_number}
```

**Path Parameters:**

| Parameter | Type | Required | Range |
|-----------|------|----------|-------|
| `recitation_id` | integer | ✓ | Reciter ID |
| `hizb_number` | integer | ✓ | 1-60 |

---

## Get Audio for Single Ayah

```
GET /recitations/{recitation_id}/by_ayah/{ayah_key}
```

**Path Parameters:**

| Parameter | Type | Required | Format |
|-----------|------|----------|--------|
| `recitation_id` | integer | ✓ | Reciter ID |
| `ayah_key` | string | ✓ | `{chapter}:{verse}` (e.g., `2:255`) |

**Response (200):**

```json
{
  "audio_files": [
    {
      "verse_key": "2:255",
      "url": "https://verses.quran.com/AbdulBaset/Mujawwad/mp3/002255.mp3"
    }
  ]
}
```

---

## Get Audio by Rub El Hizb

```
GET /recitations/{recitation_id}/by_rub/{rub_el_hizb_number}
```

**Path Parameters:**

| Parameter | Type | Required | Range |
|-----------|------|----------|-------|
| `recitation_id` | integer | ✓ | Reciter ID |
| `rub_el_hizb_number` | integer | ✓ | 1-240 |

---

## Popular Reciters Reference

| ID | Reciter | Style |
|----|---------|-------|
| 1 | AbdulBaset AbdulSamad | Mujawwad |
| 2 | AbdulBaset AbdulSamad | Murattal |
| 7 | Mishari Rashid al-`Afasy | - |
| 5 | Abu Bakr al-Shatri | - |

---

## Examples

### List All Reciters

```bash
curl "https://apis-prelive.quran.foundation/content/api/v4/resources/recitations"
```

### Get Al-Fatihah Audio by Mishari

```bash
curl "https://apis-prelive.quran.foundation/content/api/v4/chapter_recitations/7/1"
```

### Get Verse-by-Verse Audio for Surah Yasin

```bash
curl "https://apis-prelive.quran.foundation/content/api/v4/recitations/7/by_chapter/36"
```

### Get Audio for Ayat al-Kursi

```bash
curl "https://apis-prelive.quran.foundation/content/api/v4/recitations/7/by_ayah/2:255"
```

---

*[Back to Content APIs](README.md) | [Back to Main Index](../README.md)*
