from sqlalchemy.orm import Session
from schemas.transactions import TransactionBase
from db.models.transactions import Transaction

#add new transaction
def create_new_transaction(transaction: TransactionBase,db: Session,owner_id:int):
    transaction_object = Transaction(**transaction.dict(),owner_id=owner_id)
    db.add(transaction_object)
    db.commit()
    db.refresh(transaction_object)
    return transaction_object

# get transaction by id
def retreive_transaction(id:int,db:Session):
    item = db.query(Transaction).filter(Transaction.id == id).first()
    return item

# list all transactions in the database
def list_transactions(db:Session):
    transactions = db.query(Transaction).all()
    return transactions

# delete transaction by id
def delete_transaction_by_id(id: int,db: Session,owner_id):
    existing_transaction = db.query(Transaction).filter(Transaction.id == id)
    if not existing_transaction.first():
        return 0
    existing_transaction.delete(synchronize_session=False)
    db.commit()
    return 1

# update transaction by id
def update_transaction_by_id(id:int, transaction: TransactionBase,db: Session,owner_id):
    existing_transaction = db.query(Transaction).filter(Transaction.id == id)
    if not existing_transaction.first():
        return 0
    transaction.__dict__.update(owner_id=owner_id)  #update dictionary with new key value of owner_id
    existing_transaction.update(transaction.__dict__)
    db.commit()
    return 1

# list all transactions of a user
def list_transactions_by_user(db:Session,owner_id):
    transactions = db.query(Transaction).filter(Transaction.owner_id == owner_id).all()
    return transactions

# get transaction by reference
def retreive_transaction_by_reference(reference:str,db:Session):
    item = db.query(Transaction).filter(Transaction.reference == reference).first()
    return item

#get transaction by type
def retreive_transaction_by_type(transaction_type:str,db:Session):
    item = db.query(Transaction).filter(Transaction.transaction_type == transaction_type).all()
    return item

# get transaction by status
def retreive_transaction_by_status(status:str,db:Session):
    item = db.query(Transaction).filter(Transaction.status == status).first()
    return item

#delete transaction by reference
def delete_transaction_by_reference(reference: str,db: Session,owner_id):
    existing_transaction = db.query(Transaction).filter(Transaction.reference == reference)
    if not existing_transaction.first():
        return 0
    existing_transaction.delete(synchronize_session=False)
    db.commit()
    return 1