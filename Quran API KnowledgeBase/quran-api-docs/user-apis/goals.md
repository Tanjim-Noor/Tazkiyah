# Goals API

> Reading targets and progress tracking  
> **Base Path:** `/api/v1/goals`

---

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/goals/today` | Get today's goal plan |
| GET | `/goals` | Get all goals |
| POST | `/goals` | Create a goal |
| PUT | `/goals/{goalId}` | Update goal |
| DELETE | `/goals/{goalId}` | Delete goal |

---

## Get Today's Goal Plan

Retrieve current day's reading plan.

```
GET /goals/today
```

### Response (200)

```json
{
  "success": true,
  "data": {
    "targetType": "pages",
    "targetAmount": 5,
    "completedAmount": 3,
    "percentage": 60,
    "verses": [
      {
        "startVerseKey": "2:1",
        "endVerseKey": "2:40"
      }
    ]
  }
}
```

---

## Get All Goals

List user's reading goals.

```
GET /goals
```

### Response (200)

```json
{
  "success": true,
  "data": [
    {
      "id": "goal123",
      "type": "daily",
      "targetType": "pages",
      "targetAmount": 5,
      "startDate": "2023-01-01",
      "endDate": "2023-12-31",
      "isActive": true
    }
  ]
}
```

---

## Create Goal

Set a new reading goal.

```
POST /goals
Content-Type: application/json
```

### Request Body

```json
{
  "type": "daily",
  "targetType": "pages",
  "targetAmount": 5,
  "startDate": "2023-01-01",
  "endDate": "2023-12-31"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | `daily`, `weekly`, `monthly` |
| `targetType` | string | `pages`, `verses`, `juz`, `minutes` |
| `targetAmount` | integer | Target quantity |
| `startDate` | date | Goal start date |
| `endDate` | date | Goal end date |

---

## Update Goal

Modify an existing goal.

```
PUT /goals/{goalId}
```

---

## Delete Goal

Remove a goal.

```
DELETE /goals/{goalId}
```

---

*[Back to User APIs](README.md) | [Back to Main Index](../README.md)*
