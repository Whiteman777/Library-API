# Library API
Library API that manipulate Books data (CRUD) such as:
* List
* Update
* Delete
*  Borrow
* Return

## File Structure

```
libraryApi
├── env 
├── main.py
├── __pycache__
├── README.md
└── Screenshots
```

## Installation

### Create virtual enviorment 

```bash
python -m venv .venv

source .venv/bin/activate
```

### Install requirements

```bash
pip install fastapi uvicorn
```

### Run the server

```bash
uvicorn main:server --reload
```

> To see the API output go to http://127.0.0.1:8000

## API Endpoints
 * [/](#10---)
 * [/books](#20--books)
 * [/borrow](#30--borrow)
 * [/return](#40--return)

### 1.0- / :
### 1.1- / in "GET"
`GET /` check health 

Response `200 Ok`

```json
{
    "status": "success",
    "message": "Library API is running seccessfully"
}
```

### 2.0- /books:

### 2.1- /books in "GET"
`GET /books` return all available books

Response `200 Ok`

```json
{
    "books": {
        "1": {
            "id": 1,
            "title": "Clean Code",
            "author": "Robert C. Martin",
            "available_copies": 4
        },
        "2": {
            "id": 2,
            "title": "Python Basics",
            "author": "Jane Doe",
            "available_copies": 8
        },
        "3": {
            "id": 3,
            "title": "Git Guide",
            "author": "John Smith",
            "available_copies": 6
        }
    },
    "status": "success"
}
```

### 2.1.1 /books/{BookId} in "GET"
Triggered when the `bookId` does not exist in the library.
Response <mark style="background-color: red;">404 Not Found</mark>

```json
{
    "detail": "Book not found"
}
```

### 2.2 /books/{BookId} in "GET"
`GET /books/{bookId}` return specific book by ID

Response `200 Ok`

```json
{
    "book": {
        "id": 2,
        "title": "Git Guide",
        "author": "John Smith",
        "available_copies": 6
    },
    "status": "success"
}
```

### 2.3- /books in "POST"
`POST /books` add books to library

Response `201 Created`

```json
{
    "message": "Book added successfully",
    "book": {
        "id": 4,
        "title": "The Pragmatic Programmer",
        "author": "Andrew Hunt, David Thomas",
        "available_copies": 3
    },
    "status": "success"
}
```
### 2.3.1- Database schema
Database schema for adding and updating books

```python
class bookinfo(BaseModel):
    id: int
    title: str
    author: str
    available_copies: int
```

### 2.4- /books/{bookId} in "PUT"
`PUT /books/{bookId}` update book by ID

`200 Ok`

```json
{
    "message": "Book updated successfully",
    "book": {
        "id": 2,
        "title": "The Pragmatic Programmer",
        "author": "Andrew Hunt, David Thomas",
        "available_copies": 3
    },
    "status": "success"
}
```

### 2.4.1- books/{bookId} in "PUT"
Triggered when the `bookId` in the URL does not match the id in the request body

Response <mark style="background-color: red">400 Bad Request</mark>

```json
{
    "detail": "Book not found"
}
```

    

### 2.5- /books/{bookId} in "PATCH"
`PATCH /books/{bookId}` partially update book by ID

Response `200 Ok`

```json
{
    "message": "Book updated successfully",
    "book": {
        "id": 2,
        "title": "The Pragmatic Programmer",
        "author": "Andrew Hunt, David Thomas",
        "available_copies": 4
    },
    "status": "success"
}
```
### 2.5.1- Database schema 
Database schema for updating book partially

```python
class updateBookinfo(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None
    author: Optional[str] = None
    available_copies: Optional[int] = None
```

### 2.5.2- /books/{bookId} in "PATCH"
Triggered when the `bookId` in the URL does not match the id 

Response <mark style="background-color: red;">400 Bad Request</mark>

```json
{
    "detail": "Book not found"
}
```


### 2.6- /books in "DELETE"
`DELETE /books` clear book library

Response `200 Ok`

```json
{
    "message": "All books have been deleted successfully",
    "books": {},
    "status": "success"
}
```

### 2.7- /books/{bookId} in "DELETE"
`DELETE /books/{booksId}` delete specific book in the library by ID

Response `200 Ok`

```json
{
    "message": "Book deleted successfully"
}
```

### 2.7.1 /books/{bookId} in "DELETE"
Triggered when the `bookId` does not exist in the library.

Response <mark style="background-color: red">404 Not Found</mark>

```json
{
    "detail": "Book not found"
}
```
    

### 3.0- /borrow

### 3.1- /borrow in "GET"
`GET /borrow` return all  books available to borrow

Response `200 Ok`

```json
{
    "Available books to borrow": [
        {
            "id": 1,
            "title": "Clean Code",
            "author": "Robert C. Martin",
            "available_copies": 4
        },
        {
            "id": 2,
            "title": "The Pragmatic Programmer",
            "author": "Andrew Hunt, David Thomas",
            "available_copies": 4
        },
        {
            "id": 3,
            "title": "Git Guide",
            "author": "John Smith",
            "available_copies": 6
        }
    ],
    "status": "success"
}
```

### 3.1.1- /borrow in "GET"
Triggered when no `books` in the library have any available copies

Response <mark style="background-color: red;">404 Not Found</mark>

```json
{
    "detail": "No books available to borrow"
}
```

### 3.2- /borrow/{bookId} in "GET"
`GET /borrow/{bookId}` return specific book available to borrow by ID

Response `200 Ok`

```json
{
    "book": {
        "id": 2,
        "title": "The Pragmatic Programmer",
        "author": "Andrew Hunt, David Thomas",
        "available_copies": 4
    },
    "status": "success"
}
```
### 3.2.1 /borrow/{bookId} in "GET"
Triggered if the `book` does not exist OR if it has 0 available copies

Response <mark style="background-color: red">404 Not Found</mark>

```json
{
    "detail": "Book not available to borrow"
}
```

### 3.3- /borrow/{bookId} in "POST"
`POST /borrow/{bookId}` establish a borrow proccess by ID

Response `200 Ok`

```json
{
    "message": "Book borrowed successfully",
    "book": {
        "id": 2,
        "title": "The Pragmatic Programmer",
        "author": "Andrew Hunt, David Thomas",
        "available_copies": 3
    },
    "status": "success"
}
```

### 3.3.1 /borrow/{bookId} in "POST"
Triggered if the `bookId` does not exist in the library

Response <mark style="background-color: red">404 Not Found</mark>

```json
{
    "detail": "Book not available to borrow"
}
```

    

### 4.0- /return:

### 4.1- /return/{bookId}
`POST /return/{bookId}` establish a return proccess by ID

Response `200 Ok`

```json
{
    "message": "Book returned successfully",
    "book": {
        "id": 2,
        "title": "The Pragmatic Programmer",
        "author": "Andrew Hunt, David Thomas",
        "available_copies": 4
    },
    "status": "success"
}
```

### 4.1.1 /return/{bookId}
Triggered if the `bookId` does not exist in the library

Response <mark style="background-color: red">404 Not Found</mark>

```json
{
    "detail": "Book not found in library"
}
```

    









