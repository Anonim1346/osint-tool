#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Database Module - SQLAlchemy ORM for data storage
"""

import os
from sqlalchemy import create_engine, Column, String, Integer, DateTime, Boolean, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class SearchResult(Base):
    """Store search results"""
    __tablename__ = 'search_results'
    
    id = Column(Integer, primary_key=True)
    query = Column(String(255), index=True)
    query_type = Column(String(50), index=True)
    result_data = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class PersonRecord(Base):
    """Store person records"""
    __tablename__ = 'person_records'
    
    id = Column(Integer, primary_key=True)
    full_name = Column(String(255), index=True)
    phone = Column(String(20), index=True)
    email = Column(String(255), index=True)
    address = Column(String(500))
    birthdate = Column(String(20))
    data = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

class PhoneRecord(Base):
    """Store phone records"""
    __tablename__ = 'phone_records'
    
    id = Column(Integer, primary_key=True)
    phone = Column(String(20), unique=True, index=True)
    operator = Column(String(100))
    country_code = Column(String(5))
    region = Column(String(100))
    status = Column(String(50))
    owner_name = Column(String(255))
    data = Column(JSON)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class CarRecord(Base):
    """Store car records"""
    __tablename__ = 'car_records'
    
    id = Column(Integer, primary_key=True)
    registration_number = Column(String(20), unique=True, index=True)
    vin = Column(String(20), index=True)
    owner = Column(String(255))
    model = Column(String(200))
    year = Column(Integer)
    color = Column(String(50))
    status = Column(String(50))
    data = Column(JSON)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class PassportRecord(Base):
    """Store passport records"""
    __tablename__ = 'passport_records'
    
    id = Column(Integer, primary_key=True)
    passport_number = Column(String(20), unique=True, index=True)
    full_name = Column(String(255), index=True)
    birthdate = Column(String(20))
    birthplace = Column(String(255))
    issued_date = Column(String(20))
    expiry_date = Column(String(20))
    status = Column(String(50))
    data = Column(JSON)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class EmailRecord(Base):
    """Store email records"""
    __tablename__ = 'email_records'
    
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, index=True)
    in_breaches = Column(Boolean, default=False)
    breach_count = Column(Integer, default=0)
    breaches = Column(JSON)
    data = Column(JSON)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class IPRecord(Base):
    """Store IP records"""
    __tablename__ = 'ip_records'
    
    id = Column(Integer, primary_key=True)
    ip_address = Column(String(50), unique=True, index=True)
    country = Column(String(100))
    city = Column(String(100))
    latitude = Column(String(20))
    longitude = Column(String(20))
    isp = Column(String(200))
    is_proxy = Column(Boolean)
    is_vpn = Column(Boolean)
    data = Column(JSON)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class SocialMediaProfile(Base):
    """Store social media profiles"""
    __tablename__ = 'social_media_profiles'
    
    id = Column(Integer, primary_key=True)
    platform = Column(String(100), index=True)
    username = Column(String(255), index=True)
    user_id = Column(String(255), index=True)
    name = Column(String(255))
    verified = Column(Boolean, default=False)
    followers = Column(Integer)
    url = Column(String(500))
    data = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class BreachRecord(Base):
    """Store data breach records"""
    __tablename__ = 'breach_records'
    
    id = Column(Integer, primary_key=True)
    email = Column(String(255), index=True)
    breach_name = Column(String(255))
    breach_date = Column(String(20))
    compromised_data = Column(JSON)
    data = Column(JSON)
    discovered_at = Column(DateTime, default=datetime.utcnow)

class Database:
    """Database manager"""
    
    def __init__(self, db_path='data/osint.db'):
        self.db_path = db_path
        self.engine = self._create_engine()
        self.Session = sessionmaker(bind=self.engine)
        self._init_db()
    
    def _create_engine(self):
        """Create database engine"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        return create_engine(f'sqlite:///{self.db_path}')
    
    def _init_db(self):
        """Initialize database tables"""
        Base.metadata.create_all(self.engine)
    
    def get_session(self):
        """Get new database session"""
        return self.Session()
    
    def add_search_result(self, query, query_type, result_data):
        """Add search result to database"""
        session = self.get_session()
        try:
            result = SearchResult(query=query, query_type=query_type, result_data=result_data)
            session.add(result)
            session.commit()
            return result.id
        finally:
            session.close()
    
    def get_search_results(self, query, limit=10):
        """Get search results from database"""
        session = self.get_session()
        try:
            results = session.query(SearchResult).filter(SearchResult.query == query).limit(limit).all()
            return [{'id': r.id, 'data': r.result_data, 'created_at': r.created_at} for r in results]
        finally:
            session.close()
    
    def add_person_record(self, **kwargs):
        """Add person record"""
        session = self.get_session()
        try:
            person = PersonRecord(**kwargs)
            session.add(person)
            session.commit()
            return person.id
        finally:
            session.close()
    
    def get_person_by_name(self, name):
        """Get person by name"""
        session = self.get_session()
        try:
            person = session.query(PersonRecord).filter(PersonRecord.full_name.ilike(f'%{name}%')).first()
            return person
        finally:
            session.close()
    
    def get_person_by_phone(self, phone):
        """Get person by phone"""
        session = self.get_session()
        try:
            person = session.query(PersonRecord).filter(PersonRecord.phone == phone).first()
            return person
        finally:
            session.close()
