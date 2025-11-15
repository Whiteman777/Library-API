#Youssef Waleed Mohamed SE1
from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from typing import Optional

#Database Examples
books= {
        1:{"id": 1,
           "title": "Clean Code",
           "author": "Robert C. Martin",
           "available_copies": 4
          },
        2:{"id": 2,
           "title": "Python Basics",
           "author": "Jane Doe",
           "available_copies": 8
          },
        3:{"id": 3,
           "title": "Git Guide",
           "author": "John Smith",
           "available_copies": 6
          }
       }

#Object declaration
server =FastAPI()

################ /books APIS ################

#GET method to display health of API
@server.get("/")
def chechHealth():
    return{"status": "success","message": "Library API is running seccessfully"}

#GET method to display all books
@server.get("/books",status_code=status.HTTP_200_OK)
def displayBooks():
    if not books:
        return{"message": "No books available","status": "success"}
    else:
        return{"books": books,"status": "success"}

#GET method to display specific book by ID
@server.get("/books/{bookId}",status_code=status.HTTP_200_OK)
def displaySpecificBook(bookId: int):
    if bookId not in books:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    else:
        return{"book": books[bookId],"status": "success"}

#DB schema for adding and updating books
class bookinfo(BaseModel):
    id: int
    title: str
    author: str
    available_copies: int
 
#POST method to add new book
@server.post("/books",status_code=status.HTTP_201_CREATED)
def addBook(bookinfo:bookinfo):
    bookId = max(books.keys()) + 1
    book = bookinfo.model_dump()
    books[bookId] = book
    books[bookId]["id"]= bookId
    return{"message": "Book added successfully","book": books[bookId],"status": "success"}

#PUT method to update existing book
@server.put("/books/{bookId}",status_code=status.HTTP_200_OK)
def updateBook(bookId: int, bookinfo: bookinfo):
    if bookId in books:
        books[bookId] = bookinfo.model_dump()
        books[bookId]["id"]= bookId
        return{"message": "Book updated successfully","book": books[bookId],"status": "success"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    

#DB schema for updating book partially
class updateBookinfo(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None
    author: Optional[str] = None
    available_copies: Optional[int] = None

#PATCH method to update existing book partially
@server.patch("/books/{bookId}",status_code=status.HTTP_200_OK)
def patchBook(bookId: int,bookinfo: updateBookinfo):
    if bookId in books:
        book = bookinfo.model_dump(exclude_unset=True)
        books[bookId].update(book)
        books[bookId]["id"]= bookId
        return{"message": "Book updated successfully","book": books[bookId],"status": "success"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

#DELETE method to delete all books    
@server.delete("/books",status_code=status.HTTP_200_OK)
def deleteBooks():
  if not books:
    return{"message": "No books to delete","status": "success"}
  else:
    books.clear()
    return{"message": "All books have been deleted successfully","books": books,"status": "success"}

#DELETE method to delete specific book by ID    
@server.delete("/books/{bookId}",status_code=status.HTTP_200_OK)
def deleteSpecificBook(bookId: int):
    if bookId in books:
        books.pop(bookId)
        return{"message": "Book deleted successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found") 
    
################ /borrow APIS ################

#GET method to display all available books to borrow
@server.get("/borrow",status_code=status.HTTP_200_OK)
def displayAllAvailableBooks():
    availableBooks = list()
    for i in books:
        if books[i]["available_copies"] > 0:
            availableBooks.append(books[i])
        else:
            continue
    if not availableBooks:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No books available to borrow")
    else:
        return{"Available books to borrow": availableBooks,"status": "success"}
    
#GET method to display specific book to borrow by ID
@server.get("/borrow/{bookId}",status_code=status.HTTP_200_OK)
def displaySpecificAvailableBook(bookId: int):
    if bookId in books and books[bookId]["available_copies"] > 0:
        return{"book": books[bookId],"status": "success"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book is not available to borrow")

#POST method to borrow specific book by ID
@server.post("/borrow/{bookId}",status_code=status.HTTP_200_OK)
def borrowBook(bookId: int):
    if bookId in books and books[bookId]["available_copies"] >0:
        books[bookId]["available_copies"] -= 1
        return{"message": "Book borrowed successfully","book": books[bookId],"status": "success"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book is not available to borrow")

################ /return APIS ################

#POST method to return specific book by ID
@server.post("/return/{bookId}",status_code=status.HTTP_200_OK)
def returnBook(bookId: int):
    if bookId in books:
        books[bookId]["available_copies"] += 1
        return{"message": "Book returned successfully","book": books[bookId],"status": "success"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
