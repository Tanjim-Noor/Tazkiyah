# Streaks API

> Consistency and daily engagement tracking  
> **Base Path:** `/api/v1/streaks`

---

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/streaks` | Get streak information |
| GET | `/streaks/history` | Get streak history |

---

## Get Streaks

Retrieve current streak status.

```
GET /streaks
```

### Response (200)

```json
{
  "success": true,
  "data": {
    "currentStreak": 15,
    "longestStreak": 42,
    "lastActivityDate": "2023-01-21",
    "todayCompleted": true,
    "weeklyProgress": [true, true, true, true, true, false, false]
  }
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `currentStreak` | integer | Consecutive active days |
| `longestStreak` | integer | All-time best streak |
| `lastActivityDate` | date | Last recorded activity |
| `todayCompleted` | boolean | Today's goal met |
| `weeklyProgress` | boolean[] | Last 7 days status |

---

## Get Streak History

Retrieve historical streak data.

```
GET /streaks/history
```

### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `startDate` | date | History start date |
| `endDate` | date | History end date |

### Response (200)

```json
{
  "success": true,
  "data": {
    "entries": [
      {
        "date": "2023-01-21",
        "completed": true,
        "pagesRead": 5,
        "versesRead": 120
      }
    ]
  }
}
```

---

*[Back to User APIs](README.md) | [Back to Main Index](../README.md)*
