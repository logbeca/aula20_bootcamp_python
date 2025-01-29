from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, get_db
from schemas import ProductResponse,ProductUpdate, ProductCreate
from typing import List
from crud import (
    create_product,
    get_products,
    get_product,
    delete_product,
    update_product
)

router = APIRouter()

# criar rota de buscar 1 item
#sempre vamos ter 2 atributos obrigatórios, o path e o response
@router.get("/products/", response_model = List[ProductResponse])
def read_all_products(db: Session = Depends(get_db)): #depende do getdb do database.py -- abre sessão
    """ Minha rota para a leitura de todos os produtos do banco de dados"""
    products = get_products(db)
    return products

# criar rota de buscar todosositems
@router.get("/products/{product_id}", response_model = ProductResponse)
def read_one_product(product_id: int, db: Session = Depends(get_db)):
    """ Minha rota para a leitura de um produto do banco de dados"""
    db_product = get_product(db=db, product_id = product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail= "Você está buscando um produto que não está na tabela")
    return db_product

# criar rota de adicionar um item

@router.post("/products/", response_model=ProductResponse)
def create_product_route(product: ProductCreate, db: Session = Depends(get_db)):
    return create_product(db=db, product=product)



@router.delete("/products/{product_id}", response_model=ProductResponse)
def delete_product_route(product_id: int, db: Session = Depends(get_db)):
    db_product = delete_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


    
# criar rota de update de items


@router.put("/products/{product_id}", response_model=ProductResponse)
def update_product_route(
    product_id: int, product: ProductUpdate, db: Session = Depends(get_db)
):
    db_product = update_product(db, product_id=product_id, product=product)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product