# Quran Text API

> Direct Quran text retrieval in various scripts  
> **Base Path:** `/quran`

---

## Endpoints

### Get Uthmani Script

Retrieve Quran text in Uthmani script.

```
GET /quran/verses/uthmani
```

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `chapter_number` | integer | Filter by chapter |
| `juz_number` | integer | Filter by Juz |
| `page_number` | integer | Filter by page |
| `hizb_number` | integer | Filter by Hizb |
| `rub_el_hizb_number` | integer | Filter by Rub |
| `verse_key` | string | Specific verse (e.g., `2:255`) |
| `per_page` | integer | Results per page |
| `page` | integer | Page number |

**Response (200):**

```json
{
  "verses": [
    {
      "id": 1,
      "verse_key": "1:1",
      "text_uthmani": "بِسْمِ ٱللَّهِ ٱلرَّحْمَـٰنِ ٱلرَّحِيمِ"
    }
  ],
  "pagination": {...}
}
```

---

### Get Uthmani Simple Script

Simplified Uthmani without diacritical marks.

```
GET /quran/verses/uthmani_simple
```

---

### Get Imlaei Script

Modern Arabic orthography (Imlaei style).

```
GET /quran/verses/imlaei
```

---

### Get Indopak Script

Indo-Pakistani script style.

```
GET /quran/verses/indopak
```

---

### Get QPC Uthmani Hafs

King Fahad Quran Printing Complex Uthmani Hafs.

```
GET /quran/verses/qpc_uthmani_hafs
```

---

### Get Code V1

Quran Complex Font V1 encoded text.

```
GET /quran/verses/code_v1
```

---

### Get Code V2

Quran Complex Font V2 encoded text.

```
GET /quran/verses/code_v2
```

---

## Script Comparison

| Script | Description | Use Case |
|--------|-------------|----------|
| `uthmani` | Traditional Uthmani | Classical rendering |
| `uthmani_simple` | Simplified Uthmani | Simplified display |
| `imlaei` | Modern orthography | Modern Arabic readers |
| `indopak` | Indo-Pakistani style | South Asian readers |
| `qpc_uthmani_hafs` | KFQPC Hafs | Standard printing |
| `code_v1` | QCF v1 font | Font rendering |
| `code_v2` | QCF v2 font | Font rendering |

---

## Examples

### Get Al-Fatihah in Uthmani

```bash
curl "https://apis-prelive.quran.foundation/content/api/v4/quran/verses/uthmani?chapter_number=1"
```

### Get Ayat al-Kursi in Indopak Script

```bash
curl "https://apis-prelive.quran.foundation/content/api/v4/quran/verses/indopak?verse_key=2:255"
```

### Get First Juz in Imlaei

```bash
curl "https://apis-prelive.quran.foundation/content/api/v4/quran/verses/imlaei?juz_number=1"
```

---

*[Back to Content APIs](README.md) | [Back to Main Index](../README.md)*
