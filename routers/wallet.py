from typing import List

from fastapi import APIRouter, HTTPException

from nasdaq import Wallet
from utils import Firestore

router = APIRouter()


@router.post("/wallets", response_model=Wallet)
async def create_wallet(wallet: Wallet) -> Wallet:
    """
    Create a new wallet.
    """
    with Firestore() as firestore:
        return firestore.add_document(wallet)


@router.get("/wallets/{wallet_id}", response_model=Wallet)
async def read_wallet(wallet_id: str) -> Wallet:
    """
    Get a wallet by ID.
    """
    with Firestore() as firestore:
        wallet = firestore.get_document('Wallet', wallet_id)
        if wallet:
            return Wallet(**wallet)
        else:
            raise HTTPException(status_code=404, detail="Wallet not found")


@router.put("/wallets/{wallet_id}", response_model=Wallet)
async def update_wallet(wallet_id: str, name: str, description: str = "") -> Wallet:
    """
    Update a wallet by ID.
    """
    with Firestore() as firestore:
        wallet = firestore.get_document('Wallet', wallet_id)
        if wallet:
            wallet.update({"name": name, "description": description})
            updated = firestore.update_document("Wallet", wallet_id, wallet)
            if updated:
                return Wallet(**wallet)
            else:
                raise HTTPException(status_code=500, detail="Failed to update wallet")
        else:
            raise HTTPException(status_code=404, detail="Wallet not found")


@router.delete("/wallets/{wallet_id}")
async def delete_wallet(wallet_id: str):
    """
    Delete a wallet by ID.
    """
    with Firestore() as firestore:
        deleted = firestore.delete_document('Wallet', wallet_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Wallet not found")


@router.get("/wallets", response_model=List[Wallet])
async def list_wallets() -> List[Wallet]:
    """
    List all wallets.
    """
    with Firestore() as firestore:
        wallets = firestore.list_document('Wallet')
        return [Wallet(**wallet) for wallet in wallets]
