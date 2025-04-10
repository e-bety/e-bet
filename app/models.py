from sqlalchemy import Column, Integer, String, ForeignKey, Float, Numeric, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base  # ✅ Garde seulement cet import
from datetime import datetime

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    balance = Column(Numeric, default=0.0)  # Solde de l'utilisateur
    referer_id = Column(Integer, ForeignKey('users.id'))  # Si l'utilisateur a un parrain
    total_winnings = Column(Numeric, default=0.0)  # Gagné total
    referral_earnings = Column(Numeric, default=0.0)  # Gains de parrainage
    recharge_requests = relationship("RechargeRequest", back_populates="user")
    
    # Relations avec le parrain et les filleuls
    referrals = relationship("User", remote_side=[id], back_populates="referrer")
    referrer = relationship("User", back_populates="referrals")
    
    # Relations avec les bonus de parrainage (utilisation de "ReferralBonus" entre guillemets)
    referral_bonuses_received = relationship("ReferralBonus", back_populates="referrer", foreign_keys="[ReferralBonus.referrer_id]", cascade="all, delete-orphan")
    referral_bonuses_given = relationship("ReferralBonus", back_populates="referred", foreign_keys="[ReferralBonus.referred_id]", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, balance={self.balance})>"

class ReferralBonus(Base):
    __tablename__ = "referral_bonus"

    id = Column(Integer, primary_key=True, index=True)
    referrer_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)  # Parrain
    referred_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)  # Filleul
    amount = Column(Numeric(10, 2), nullable=False)
    level = Column(Integer, nullable=False)  # 1, 2 ou 3
    created_at = Column(DateTime, default=func.now(), nullable=False)

    # Liens vers l'utilisateur (parrain et filleul)
    referrer = relationship("User", foreign_keys=[referrer_id], back_populates="referral_bonuses_received")
    referred = relationship("User", foreign_keys=[referred_id], back_populates="referral_bonuses_given")

    def __repr__(self):
        return f"<ReferralBonus(id={self.id}, referrer_id={self.referrer_id}, referred_id={self.referred_id}, amount={self.amount}, level={self.level})>"

class RechargeRequest(Base):
    __tablename__ = 'recharge_requests'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))  # L'utilisateur qui fait la demande
    referrer_id = Column(Integer, ForeignKey('users.id'))  # L'utilisateur qui a référé (le parrain)
    amount = Column(Numeric, default=0.0)  # Montant de la recharge
    status = Column(String, default='pending')  # Statut de la demande (ex: en attente, validée, rejetée)
    
    user = relationship("User", foreign_keys=[user_id], back_populates="recharge_requests")
    referrer = relationship("User", foreign_keys=[referrer_id], back_populates="referral_requests")

    # Suivi des gains via parrainage
    referral_earnings = Column(Numeric(10, 2), default=0.00, nullable=False)

    # Relations avec les transactions
    transactions = relationship("Transaction", back_populates="user", cascade="all, delete-orphan")

    # Relations avec les mises (bets)
    bets = relationship("Bet", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<RechargeRequest(id={self.id}, user_id={self.user_id}, referrer_id={self.referrer_id}, amount={self.amount}, status={self.status})>"

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    transaction_type = Column(String, nullable=False)  # "deposit" ou "withdrawal"
    timestamp = Column(DateTime, default=func.now(), index=True)

    user = relationship("User", back_populates="transactions")

    def __repr__(self):
        return f"<Transaction(id={self.id}, user_id={self.user_id}, amount={self.amount}, type={self.transaction_type})>"

class Bet(Base):
    __tablename__ = "bets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    bet_amount = Column(Numeric(10, 2), nullable=False)
    numbers = Column(String, nullable=False)  # Ex: "12,45;8,23"
    timestamp = Column(DateTime, default=func.now(), index=True)
    result = Column(String, nullable=True)  # Ex: "win_1000x", "win_100x", "win_50x", "lose"
    winnings = Column(Numeric(10, 2), default=0.00, nullable=False)  # Gain remporté
    is_demo = Column(Integer, default=0, nullable=False)  # 0 = Partie normale, 1 = Mode démo
    first_group = Column(String, nullable=False)  # Numéros générés en haut
    second_group = Column(String, nullable=False)  # Numéros générés en bas

    user = relationship("User", back_populates="bets")

    def __repr__(self):
        return f"<Bet(id={self.id}, user_id={self.user_id}, amount={self.bet_amount}, result={self.result})>"
