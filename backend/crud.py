from sqlalchemy.orm import Session # session faz a operação do orm. faz as queries no banco
from schemas import ProductUpdate, ProductCreate
from models import ProductModel

# get all ( select * from)
def get_products(db: Session):
    return db.query(ProductModel).all()

# get where id = 1
def get_product(db: Session, product_id: int):
    return db.query(ProductModel).filter(ProductModel.id == product_id).first()

#insert into (create)
def create_product(db: Session, product: ProductCreate):
    #transformar minha view para ORM, adicionar na tabela, fazer commit, 
    #fazer refresh no banco, retormar para o usuário o item criado
    db_product = ProductModel(**product.model_dump()) #desempacotar o produto  e baixar  modelo
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product



# delete where id = 1

def delete_product(db: Session, product_id: int):
    db_product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    db.delete(db_product)
    db.commit()
    return db_product

#update where id =1

def update_product(db: Session, product_id: int, product: ProductUpdate):
    db_product = db.query(ProductModel).filter(ProductModel.id == product_id).first()

    if db_product is None:
        return None

    if product.name is not None:
        db_product.name = product.name

    
    if product.description is not None:
        db_product.description = product.description

    
    if product.price is not None:
        db_product.price = product.price

    
    if product.categoria is not None:
        db_product.categoria = product.categoria

    
    if product.email_fornecedor is not None:
        db_product.email_fornecedor = product.email_fornecedor

    db.commit()
    db.refresh(db_product)
    return db_product
