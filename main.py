from fastapi import FastAPI, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime

from database import get_db, Advertisement as AdvertisementModel
from schemas import AdvertisementCreate, AdvertisementUpdate, AdvertisementResponse

app = FastAPI(title="Advertisement Service", description="API for buy/sell advertisements")

@app.post("/advertisement", response_model=AdvertisementResponse, status_code=201)
async def create_advertisement(
    advertisement: AdvertisementCreate, 
    db: Session = Depends(get_db)
):
    """
    Create a new advertisement
    """
    db_advertisement = AdvertisementModel(**advertisement.model_dump())
    db.add(db_advertisement)
    db.commit()
    db.refresh(db_advertisement)
    return db_advertisement

@app.get("/advertisement/{advertisement_id}", response_model=AdvertisementResponse)
async def get_advertisement(
    advertisement_id: int, 
    db: Session = Depends(get_db)
):
    """
    Get advertisement by ID
    """
    advertisement = db.query(AdvertisementModel).filter(
        AdvertisementModel.id == advertisement_id
    ).first()
    
    if not advertisement:
        raise HTTPException(status_code=404, detail="Advertisement not found")
    
    return advertisement

@app.patch("/advertisement/{advertisement_id}", response_model=AdvertisementResponse)
async def update_advertisement(
    advertisement_id: int, 
    advertisement_update: AdvertisementUpdate,
    db: Session = Depends(get_db)
):
    """
    Update advertisement by ID
    """
    advertisement = db.query(AdvertisementModel).filter(
        AdvertisementModel.id == advertisement_id
    ).first()
    
    if not advertisement:
        raise HTTPException(status_code=404, detail="Advertisement not found")
    
    # Используем model_dump() для Pydantic v2
    update_data = advertisement_update.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(advertisement, field, value)
    
    db.commit()
    db.refresh(advertisement)
    return advertisement

@app.delete("/advertisement/{advertisement_id}", status_code=204)
async def delete_advertisement(
    advertisement_id: int, 
    db: Session = Depends(get_db)
):
    """
    Delete advertisement by ID
    """
    advertisement = db.query(AdvertisementModel).filter(
        AdvertisementModel.id == advertisement_id
    ).first()
    
    if not advertisement:
        raise HTTPException(status_code=404, detail="Advertisement not found")
    
    db.delete(advertisement)
    db.commit()
    return None

@app.get("/advertisement", response_model=List[AdvertisementResponse])
async def search_advertisements(
    title: Optional[str] = Query(None, description="Filter by title"),
    description: Optional[str] = Query(None, description="Filter by description"),
    author: Optional[str] = Query(None, description="Filter by author"),
    min_price: Optional[float] = Query(None, description="Minimum price filter"),
    max_price: Optional[float] = Query(None, description="Maximum price filter"),
    created_after: Optional[datetime] = Query(None, description="Filter advertisements created after this date"),
    created_before: Optional[datetime] = Query(None, description="Filter advertisements created before this date"),
    db: Session = Depends(get_db)
):
    """
    Search advertisements by various fields
    """
    query = db.query(AdvertisementModel)
    
    # Фильтр по title (case-insensitive partial match)
    if title:
        query = query.filter(AdvertisementModel.title.ilike(f"%{title}%"))
    
    # Фильтр по description (case-insensitive partial match)
    if description:
        query = query.filter(AdvertisementModel.description.ilike(f"%{description}%"))
    
    # Фильтр по author (case-insensitive partial match)
    if author:
        query = query.filter(AdvertisementModel.author.ilike(f"%{author}%"))
    
    # Фильтр по диапазону цен
    if min_price is not None:
        query = query.filter(AdvertisementModel.price >= min_price)
    
    if max_price is not None:
        query = query.filter(AdvertisementModel.price <= max_price)
    
    # Фильтр по диапазону дат
    if created_after:
        query = query.filter(AdvertisementModel.created_at >= created_after)
    
    if created_before:
        query = query.filter(AdvertisementModel.created_at <= created_before)
    
    advertisements = query.all()
    return advertisements

@app.get("/")
async def root():
    """
    Root endpoint with API documentation
    """
    return {
        "message": "Advertisement Service API",
        "version": "1.0.0",
        "description": "API for creating and managing buy/sell advertisements",
        "endpoints": {
            "POST /advertisement": "Create new advertisement",
            "GET /advertisement/{id}": "Get advertisement by ID",
            "PATCH /advertisement/{id}": "Update advertisement by ID", 
            "DELETE /advertisement/{id}": "Delete advertisement by ID",
            "GET /advertisement": "Search advertisements with filters",
            "GET /docs": "Interactive API documentation (Swagger)",
            "GET /redoc": "API documentation (ReDoc)"
        },
        "search_filters": {
            "title": "Filter by title (partial match)",
            "description": "Filter by description (partial match)",
            "author": "Filter by author (partial match)",
            "min_price": "Minimum price filter",
            "max_price": "Maximum price filter",
            "created_after": "Filter advertisements created after this date (ISO format)",
            "created_before": "Filter advertisements created before this date (ISO format)"
        },
        "examples": {
            "create_advertisement": {
                "method": "POST",
                "url": "/advertisement",
                "body": {
                    "title": "iPhone 15 Pro",
                    "description": "New iPhone 15 Pro, excellent condition",
                    "price": 999.99,
                    "author": "John Doe"
                }
            },
            "search_by_description": {
                "method": "GET", 
                "url": "/advertisement?description=iphone&min_price=500&max_price=1500"
            },
            "get_by_id": {
                "method": "GET",
                "url": "/advertisement/1"
            },
            "update_advertisement": {
                "method": "PATCH",
                "url": "/advertisement/1", 
                "body": {
                    "price": 899.99
                }
            }
        },
        "database": "SQLite with SQLAlchemy ORM",
        "features": [
            "Integer auto-increment IDs",
            "Full-text search in title, description, author",
            "Price range filtering", 
            "Date range filtering",
            "Pydantic v2 validation",
            "RESTful API design"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
