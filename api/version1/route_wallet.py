from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends,HTTPException,status
from db.repository.wallet import create_new_wallet,retreive_wallet,list_wallets, update_wallet_balance_by_id,update_wallet_by_id,delete_wallet_by_id, get_wallet_history
from typing import List 

from db.session import get_db
from db.models.wallet import Wallet
from schemas.wallet import UpdateWalletBalance, WalletCreate,ShowWallet

from db.models.users import User
from api.version1.route_auth import get_current_user_from_token

router = APIRouter()

#wallet routes
#wallets are created automatically when a user is created
#user must have only one wallet

@router.post("/create-wallet/", response_model=WalletCreate)
def create_wallet(wallet: WalletCreate, db: Session = Depends(get_db),current_user:User = Depends(get_current_user_from_token)):  #new dependency here
    wallet = create_new_wallet(wallet=wallet, db=db, user_id=current_user.id)
    return wallet

@router.get("/get/{id}",response_model=ShowWallet) # if we keep just "{id}" . it would stat catching all routes
def read_wallet(id:int,db:Session = Depends(get_db)):
    wallet = retreive_wallet(id=id,db=db)
    if not wallet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Wallet with this id {id} does not exist")
    return wallet

@router.get("/all",response_model=List[ShowWallet])
def read_wallets(db:Session = Depends(get_db)):
    wallets = list_wallets(db=db)
    return wallets

@router.put("/update/{id}")
def update_wallet(id: int,wallet: WalletCreate,db: Session = Depends(get_db)):
    current_user = 1
    message = update_wallet_by_id(id=id,wallet=wallet,db=db,owner_id=current_user)
    if not message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Wallet with id {id} not found")
    return {"msg":"Successfully updated data."}

@router.delete("/delete/{id}")
def delete_wallet(id: int,db: Session = Depends(get_db),current_user: User = Depends(get_current_user_from_token)):
    wallet = retreive_wallet(id =id,db=db)
    if not wallet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Wallet with id {id} not found")
    message = delete_wallet_by_id(id=id,db=db,user_id=current_user.id)
    if not message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Wallet with id {id} not found")
    return {"msg":"Successfully deleted."}

 #update wallet balance after getting the current balance

@router.patch("/update-balance/{userid}")
def update_wallet_balance(userid: int, amount: float, reference: str = None, method: str = None, db: Session = Depends(get_db)):
    current_user = 1
    message = update_wallet_balance_by_id(id=userid,db=db, amount=amount, reference=reference, method=method)
    if not message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Wallet with id {id} not found")
    return {"msg":"Successfully updated data."}

# get wallet history
@router.get("/history/{userid}")
def fetch_wallet_history(userid: int, db: Session = Depends(get_db)):
    current_user = 1
    wallet_history = get_wallet_history(id=userid,db=db)
    if not wallet_history:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Wallet with id {id} not found")
    return wallet_history






