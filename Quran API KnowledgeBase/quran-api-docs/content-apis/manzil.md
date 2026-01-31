# Manzil API

> 7-day reading division for weekly completion  
> **Base Path:** `/verses`

---

## Overview

Manzil (plural: Manazil) divides the Quran into 7 parts for reading completion in one week. This is a traditional division used for regular recitation practice.

---

## Manzil Structure

| Manzil | Chapters | Common Name |
|--------|----------|-------------|
| 1 | 1-4 | Al-Fatihah to An-Nisa |
| 2 | 5-9 | Al-Ma'idah to At-Tawbah |
| 3 | 10-16 | Yunus to An-Nahl |
| 4 | 17-25 | Al-Isra to Al-Furqan |
| 5 | 26-36 | Ash-Shu'ara to Ya-Sin |
| 6 | 37-49 | As-Saffat to Al-Hujurat |
| 7 | 50-114 | Qaf to An-Nas |

---

## Accessing Manzil Data

### Via Verse Objects

Each verse includes its Manzil number:

```json
{
  "verse": {
    "id": 1,
    "verse_key": "1:1",
    "manzil_number": 1,
    ...
  }
}
```

### Filtering by Manzil

Currently, filtering verses directly by Manzil requires fetching verses and checking the `manzil_number` field, or using chapter-based queries based on the Manzil structure above.

---

## Example: Get First Manzil

Since Manzil 1 covers chapters 1-4:

```bash
# Get Al-Fatihah (Chapter 1)
curl "https://apis-prelive.quran.foundation/content/api/v4/verses/by_chapter/1"

# Get Al-Baqarah (Chapter 2)
curl "https://apis-prelive.quran.foundation/content/api/v4/verses/by_chapter/2"

# Get Al-Imran (Chapter 3)
curl "https://apis-prelive.quran.foundation/content/api/v4/verses/by_chapter/3"

# Get An-Nisa (Chapter 4)
curl "https://apis-prelive.quran.foundation/content/api/v4/verses/by_chapter/4"
```

---

## Weekly Reading Schedule

| Day | Manzil | Approx. Pages |
|-----|--------|---------------|
| Sunday | 1 | 1-76 |
| Monday | 2 | 77-120 |
| Tuesday | 3 | 121-190 |
| Wednesday | 4 | 191-265 |
| Thursday | 5 | 266-355 |
| Friday | 6 | 356-435 |
| Saturday | 7 | 436-604 |

---

*[Back to Content APIs](README.md) | [Back to Main Index](../README.md)*
