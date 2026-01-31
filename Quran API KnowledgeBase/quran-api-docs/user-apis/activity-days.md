# Activity Days API

> Daily engagement metrics  
> **Base Path:** `/api/v1/activity-days`

---

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/activity-days` | Get activity days |
| POST | `/activity-days` | Record activity |
| PUT | `/activity-days` | Update activity |

---

## Get Activity Days

Retrieve activity history.

```
GET /activity-days
```

### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `startDate` | date | Start of range |
| `endDate` | date | End of range |
| `limit` | integer | Max results |

### Response (200)

```json
{
  "success": true,
  "data": [
    {
      "date": "2023-01-21",
      "pagesRead": 5,
      "versesRead": 120,
      "minutesRead": 30,
      "goalCompleted": true
    }
  ]
}
```

---

## Record Activity

Log reading activity for a day.

```
POST /activity-days
Content-Type: application/json
```

### Request Body

```json
{
  "date": "2023-01-21",
  "pagesRead": 5,
  "versesRead": 120,
  "minutesRead": 30
}
```

---

## Update Activity

Modify recorded activity.

```
PUT /activity-days
Content-Type: application/json
```

### Request Body

```json
{
  "date": "2023-01-21",
  "pagesRead": 6,
  "versesRead": 140,
  "minutesRead": 35
}
```

---

*[Back to User APIs](README.md) | [Back to Main Index](../README.md)*
