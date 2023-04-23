from datetime import datetime
from decimal import ROUND_DOWN, Decimal
from fastapi import HTTPException
from sqlalchemy.orm import Session

from schemas.wallet import WalletCreate, ShowWallet, WalletBase
from db.models.wallet import Wallet, WalletHistory
from db.repository.datetime import formatted_datetime, ref


#user must have only one wallet
def create_new_wallet(wallet: WalletCreate, db: Session, user_id: int):
    wallet_object = Wallet(user_id = user_id, balance = 0)
    #get user_id from Wallet
    method = "created"
   # wallet_object.user_id = user_id
    db.add(wallet_object)
    db.commit()
    db.refresh(wallet_object)
    # add wallet history
    

    record_wallet_balance_history(wallet_object.id, wallet_object.user_id, wallet_object.balance, wallet_object.balance, 0, ref, method, db,)
    return wallet_object



def retreive_wallet(id: int, db: Session):
    item = db.query(Wallet).filter(Wallet.id == id).first()
    return item


# list all wallets in the database
def list_wallets(db: Session):
    wallets = db.query(Wallet).all()
    return wallets


def update_wallet_by_id(id: int, wallet: WalletCreate, db: Session, user_id):
    existing_wallet = db.query(Wallet).filter(Wallet.id == id)
    if not existing_wallet.first():
        return 0
    wallet.__dict__.update(user_id=user_id)  # update dictionary with new key value of user_id
    existing_wallet.update(wallet.__dict__)
    db.commit()
    return 1


def delete_wallet_by_id(id: int, db: Session, user_id):
    existing_wallet = db.query(Wallet).filter(Wallet.id == id)
    if not existing_wallet.first():
        return 0
    existing_wallet.delete(synchronize_session=False)
    db.commit()
    return 1

#add or subtract balance from wallet
def update_wallet_balance(id: int, wallet: WalletBase, db: Session, user_id):
    existing_wallet = db.query(Wallet).filter(Wallet.id == id)
    if not existing_wallet.first():
        return 0
    wallet.__dict__.update(user_id=user_id)  # update dictionary with new key value of user_id
    existing_wallet.update(wallet.__dict__)
    db.commit()
    return 1

#get current balance of wallet
def get_wallet_balance(id: int, db: Session):
    item = db.query(Wallet).filter(Wallet.id == id).first()
    return item.balance

#update wallet balance after getting the current balance
# def update_wallet_balance(id: int, amount: int, db: Session):
#     item = db.query(Wallet).filter(Wallet.id == id).first()
#     item.balance = item.balance + amount
#     db.commit()
#     return item

def update_wallet_balance_by_id(id: int, reference: str, amount: int, method:str, db: Session):
    item = db.query(Wallet).filter(Wallet.user_id == id).first()

    if item is None:
        raise HTTPException(status_code=404, detail="Wallet not found")
    # Update balance with truncated amount
    balance_before = item.balance
    amount = Decimal(str(amount)).quantize(Decimal('0.00'), rounding=ROUND_DOWN)
    item.balance = (item.balance + amount)
    balance_after = item.balance

    db.commit()

    # Add balance history if balance has changed
    reference = reference if reference is not None else ref,
    if balance_before != balance_after:

        balance_history = WalletHistory(
            wallet_id=item.id,
            user_id=item.user_id,
            balance_before=balance_before,
            balance_after=balance_after,
            amount = amount,
            #add reference, if reference is empty then generate a random string
            #reference = reference if reference is not None else ref,
            reference = reference,
            method=method,



            date_time=formatted_datetime
        )
        db.add(balance_history)
    db.commit()
    db.refresh(item)

    return item

#see wallet history
def get_wallet_history(id: int, db: Session):
    item = db.query(WalletHistory).filter(WalletHistory.user_id == id).all()
    if item is None:
        raise HTTPException(status_code=404, detail="Wallet not found")
    
    return item


def record_wallet_balance_history( wallet_id: int, user_id: int, balance_before: Decimal,
                                  balance_after: Decimal, amount: Decimal, reference: str, method: str, db: Session):
    """
    Record wallet balance history in the database.

    :param db: SQLAlchemy database session
    :type db: Session
    :param wallet_id: ID of the wallet
    :type wallet_id: int
    :param balance_before: Balance before the update
    :type balance_before: Decimal
    :param balance_after: Balance after the update
    :type balance_after: Decimal
    :param amount: Amount updated
    :type amount: Decimal
    """
    balance_history = WalletHistory(
        wallet_id=wallet_id,
        user_id=user_id,
        balance_before=balance_before,
        balance_after=balance_after,
        amount=amount,
        #add reference, if reference is empty then generate a random string
        reference = reference if reference is not None else ref,
        method=method,
        date_time=formatted_datetime
    )
    db.add(balance_history)
    db.commit()

    



