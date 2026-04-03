# Finance Management API

Simple API to manage your money - track income, expenses, and see where your money goes.

## What This Does

- Create users with different access levels (viewer, analyst, admin)
- Add, update, delete financial records
- Filter transactions by date, category, amount
- Dashboard shows totals , category breakdowns , monthly trends and recent activity
- Only admins can delete stuff, viewers can only look
- Pagination
- Search functionality
- Swagger API documentation inbuilt
- Input validation
- Useful error responses
- Status codes used appropriately
- Testing done


## Tech Stack

- FastAPI (Python)
- SQLite database
- JWT for authentication
- Bcrypt for passwords

## Why FastAPI? Not Node.js

| Feature | FastAPI | Node.js/Express |
|---------|---------|-----------------|
| Input validation | Built-in with Pydantic | Need Joi or Zod |
| API docs | Auto generates Swagger | Manual or third party |
| Type hints | Native Python | TypeScript needed |
| Performance | Very fast | Fast |
| Role based auth | Easy with dependencies | Manual middleware |
| Async support | Built-in | Need callbacks/promises |

FastAPI just works out of the box. No extra libraries for validation, no manual docs writing, no fighting with types.

## Routes

### Auth

| Method | Route | What it does | Who can use |
|--------|-------|--------------|-------------|
| POST | /auth/register | Create new account | Anyone |
| POST | /auth/login | Get access token | Anyone |
| GET | /auth/me | Your profile | Logged in users |

### Records

| Method | Route | What it does | Who can use |
|--------|-------|--------------|-------------|
| GET | /records/ | List all records (paginated) | Analyst, Admin |
| GET | /records/{id} | Get one record | Analyst, Admin |
| POST | /records/ | Create record | Admin only |
| PUT | /records/{id} | Update record | Admin only |
| DELETE | /records/{id} | Delete record | Admin only |
| GET | /records/filter | Search with filters | Analyst, Admin |

### Dashboard

| Method | Route | What it does | Who can use |
|--------|-------|--------------|-------------|
| GET | /dashboard/summary | Total income, expense, balance | All roles |
| GET | /dashboard/category-breakdown | Spend by category | All roles |
| GET | /dashboard/monthly-trends | Shows it | All roles
| GET | /dashboard/recent-activity | In year / month | Shows it | All roles


## Role Permissions

| Action | Viewer | Analyst | Admin |
|--------|--------|---------|-------|
| View records | No | Yes | Yes (all) |
| Create record | No | No | Yes |
| Update record | No | No | Yes |
| Delete record | No | No | Yes |
| View dashboard | Yes | Yes | Yes |
| Category insights | Yes | Yes | Yes |

## Setup

###  Clone , install and run
 
```bash
git clone https://github.com/nandinideshmukh/FINANCE_FastAPI
cd FINANCE_FastAPI
pip install -r requirements.txt
```

```
# create env file
SECRET_KEY=your-secret-key-minimum-32-chars
ALGORITHM=HS256
ACCESS_TIME_HOURS=24
```

```
run uvicorn app:app --reload --port 8000
```

```
Docs available at http://localhost:8000/docs

```