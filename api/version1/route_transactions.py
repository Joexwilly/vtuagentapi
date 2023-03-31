from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends,HTTPException,status
from db.repository.transactions import create_new_transaction,retreive_transaction,list_transactions,update_transaction_by_id,delete_transaction_by_id, retreive_transaction_by_reference, retreive_transaction_by_type, retreive_transaction_by_status, list_transactions_by_user, delete_transaction_by_reference
from typing import List 

from db.session import get_db
from schemas.transactions import TransactionBase, ShowTransaction

from db.models.users import User
from api.version1.route_auth import get_current_user_from_token

router = APIRouter()

#add new transaction
@router.post("/create-transaction/", response_model=ShowTransaction)
def create_transaction(transaction: TransactionBase, db: Session = Depends(get_db),current_user:User = Depends(get_current_user_from_token)):  #new dependency here
    transaction = create_new_transaction(transaction=transaction, db=db, owner_id=current_user.id)
    return transaction



#get transaction by id
@router.get("/get/{id}",response_model=ShowTransaction) # TAKE NOTEif we keep just "{id}" . it would stat catching all routes
def read_transaction(id:int,db:Session = Depends(get_db)):
    transaction = retreive_transaction(id=id,db=db)
    if not transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Transaction with this id {id} does not exist")
    return transaction

#get all transactions by id
@router.get("/all",response_model=List[ShowTransaction])
def read_transactions(db:Session = Depends(get_db)):
    transactions = list_transactions(db=db)
    return transactions

#update transaction by id
@router.put("/update/{id}")
def update_transaction(id: int,transaction: TransactionBase,db: Session = Depends(get_db)):
    current_user = 1
    message = update_transaction_by_id(id=id,transaction=transaction,db=db,owner_id=current_user)
    if not message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Transaction with id {id} not found")
    return {"msg":"Successfully updated data."}

#delete transaction by id
@router.delete("/delete/{id}")
def delete_transaction(id: int,db: Session = Depends(get_db),current_user: User = Depends(get_current_user_from_token)):
    transaction = retreive_transaction(id =id,db=db)
    if not transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Transaction with id {id} not found")
    message = delete_transaction_by_id(id=id,db=db,owner_id=current_user.id)
    if not message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Transaction with id {id} not found")
    return {"msg":"Successfully deleted."}

#get transaction by user id
@router.get("/user/{id}",response_model=List[ShowTransaction])
def read_transactions_by_user(id:int,db:Session = Depends(get_db)):
    transactions = list_transactions_by_user(db=db,owner_id=id)
    return transactions

#get transaction by reference
@router.get("/reference/{reference}",response_model=ShowTransaction)
def read_transaction_by_reference(reference:str,db:Session = Depends(get_db)):
    transaction = retreive_transaction_by_reference(reference=reference,db=db)
    if not transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Transaction with this reference {reference} does not exist")
    return transaction

#update transaction by reference
@router.put("/update/reference/{reference}")
def update_transaction_by_reference(reference: str,transaction: TransactionBase,db: Session = Depends(get_db)):
    current_user = 1
    message = update_transaction_by_id(reference=reference,transaction=transaction,db=db,owner_id=current_user)
    if not message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Transaction with reference {reference} not found")
    return {"msg":"Successfully updated data."}

#delete transaction by reference
# @router.delete("/delete/reference/{reference}")
# def delete_transaction_by_reference(reference: str,db: Session = Depends(get_db),current_user: User = Depends(get_current_user_from_token)):
#     transaction = retreive_transaction(reference =reference,db=db)
#     if not transaction:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"Transaction with reference {reference} not found")
#     message = delete_transaction_by_id(reference=reference,db=db,owner_id=current_user.id)
#     if not message:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"Transaction with reference {reference} not found")
#     return {"msg":"Successfully deleted."}

@router.delete("/delete/reference/{reference}")
def delete_transaction(reference: str,db: Session = Depends(get_db),current_user: User = Depends(get_current_user_from_token)):
    transaction = retreive_transaction_by_reference(reference =reference,db=db)
    if not transaction:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Job with {reference} does not exist")
    print(transaction.owner_id,current_user.id,current_user.is_superuser)
    if transaction.owner_id == current_user.id or current_user.is_superuser:
        delete_transaction_by_reference(reference=reference,db=db,owner_id=current_user.id)
        return {"msg":"Successfully deleted."}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"You are not permitted!!!!")

#get transaction by type
@router.get("/type/{type}",response_model=List[ShowTransaction])
def read_transactions_by_type(transaction_type:str,db:Session = Depends(get_db)):
    transactions = retreive_transaction_by_type(db=db,transaction_type=transaction_type)
    return transactions




